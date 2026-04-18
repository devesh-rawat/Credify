"""
Credify Agent - Main Orchestrator
Uses Google Gemini with function calling to orchestrate backend tasks
"""

import os
import json
from typing import Dict, Any, List, Optional
import numbers
import numpy as np
from datetime import datetime, date
from decimal import Decimal
import google.generativeai as genai
from core.config import settings
from agent.agent_tools import get_tool_schemas, execute_tool, ALL_TOOLS
from agent.agent_tasks import (
    get_task_definition,
    validate_task_params,
    get_task_system_prompt,
    create_task_response,
    get_task_execution_template,
    TaskType
)
from agent.rate_limiter import rate_limited_call, get_rate_limiter
from database.mongo import db
from services.email_service import email_service


class CredifyAgent:
    """
    Main orchestrator agent for Credify backend
    Uses Gemini 2.0 Flash with function calling to execute tasks autonomously
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the Credify Agent
        
        Args:
            api_key: Gemini API key (if not provided, reads from settings)
            model_name: Gemini model to use (if not provided, reads from settings)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in settings")
        
        self.model_name = model_name or settings.GEMINI_MODEL
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model with function calling
        self.tool_schema_lookup = {}
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self._prepare_tools()
        )
        
        # Initialize rate limiter with config
        from agent.rate_limiter import RateLimiter
        global _rate_limiter
        _rate_limiter = RateLimiter(
            requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
            requests_per_day=settings.RATE_LIMIT_PER_DAY
        )
        
        print(f"[CredifyAgent] Initialized with model: {self.model_name}")
    
    def _prepare_tools(self) -> List[Dict]:
        """Prepare tools in Gemini-compatible format"""
        tool_schemas = get_tool_schemas()
        # Keep a lookup for quick runtime hints (used in error recovery)
        self.tool_schema_lookup = {
            schema["name"]: schema for schema in tool_schemas
        }
        
        # Convert to Gemini function declarations
        function_declarations = []
        for schema in tool_schemas:
            # Sanitize schema types to be uppercase for protobuf enum compatibility
            sanitized_parameters = self._sanitize_schema(schema["parameters"])
            
            function_declarations.append({
                "name": schema["name"],
                "description": schema["description"],
                "parameters": sanitized_parameters
            })
        
        return function_declarations

    def _sanitize_schema(self, schema: Dict) -> Dict:
        """Recursively convert schema types to uppercase for Gemini API"""
        if not isinstance(schema, dict):
            return schema
            
        new_schema = schema.copy()
        
        if "type" in new_schema and isinstance(new_schema["type"], str):
            new_schema["type"] = new_schema["type"].upper()
            
        if "properties" in new_schema:
            new_properties = {}
            for k, v in new_schema["properties"].items():
                new_properties[k] = self._sanitize_schema(v)
            new_schema["properties"] = new_properties
            
        if "items" in new_schema:
            new_schema["items"] = self._sanitize_schema(new_schema["items"])
            
        return new_schema

    def _normalize_data(self, value: Any) -> Any:
        """Convert numpy/pandas scalars and arrays into native Python types."""
        if isinstance(value, dict):
            return {k: self._normalize_data(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._normalize_data(v) for v in value]
        if isinstance(value, tuple):
            return tuple(self._normalize_data(v) for v in value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, numbers.Number):
            return value
        return value

    def _send_report_email(self, user_id: str, score_data: Dict[str, Any], report_path: Optional[str]) -> None:
        """Notify the user that a new report is available."""
        try:
            user = db.get_db().users.find_one({"user_id": user_id})
            if not user or not user.get("email"):
                return

            user_name = user.get("name") or user.get("full_name") or "there"
            subject = "Your new Credify credit report is ready"
            default_probability = score_data.get('default_probability', 0)
            try:
                default_percent = f"{float(default_probability) * 100:.2f}%"
            except (TypeError, ValueError):
                default_percent = str(default_probability)
            context = {
                "user_name": user_name,
                "credit_score": score_data.get('credit_score', 'N/A'),
                "risk_label": score_data.get('risk_label', 'N/A'),
                "default_probability": default_percent,
                "insights_summary": (score_data.get("insights") or {}).get("summary", ""),
            }
            attachments = [report_path] if report_path and os.path.exists(report_path) else []
            email_service.send_templated_email(
                user["email"],
                subject,
                "report_ready.html",
                context,
                attachments=attachments
            )
        except Exception as exc:
            print(f"[CredifyAgent] Failed to send report email: {exc}")

    def _make_json_safe(self, value: Any) -> Any:
        """Convert complex objects (datetime, numpy, Decimal) to JSON-friendly types."""
        if isinstance(value, dict):
            return {k: self._make_json_safe(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._make_json_safe(v) for v in value]
        if isinstance(value, tuple):
            return [self._make_json_safe(v) for v in value]
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except Exception:
                return value.hex()
        if isinstance(value, numbers.Number):
            return value
        return value

    def _execute_run_scoring_pipeline(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Deterministic implementation of the run_scoring task without extra LLM hops."""
        user_id = payload.get("user_id")
        if not user_id:
            return create_task_response(
                status="failed",
                task=TaskType.RUN_SCORING,
                error="user_id is required for run_scoring"
            )

        def _call_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
            print(f"[CredifyAgent] [local] {tool_name} -> {kwargs}")
            result = execute_tool(tool_name, **kwargs)
            if not result.get("success"):
                raise ValueError(f"{tool_name} failed: {result.get('error')}")
            return result.get("data") or {}

        try:
            statement_data = self._normalize_data(_call_tool("fetch_all_user_statements", user_id=user_id))
            transactions = statement_data.get("transactions", [])
            if not transactions:
                raise ValueError("No transactions found for user")

            features = self._normalize_data(_call_tool("extract_features", transactions=transactions))
            if not isinstance(features, dict) or not features:
                raise ValueError("Feature extraction returned empty data")

            score_data = self._normalize_data(_call_tool("predict_score", features=features))
            if not isinstance(score_data, dict):
                raise ValueError("Score prediction returned invalid data")

            insights = self._normalize_data(_call_tool("generate_ai_insight", features=features, score_data=score_data))
            if insights:
                score_data["insights"] = insights
                # Flatten insights for PDF generation and API response
                score_data["summary"] = insights.get("summary")
                score_data["key_factors"] = insights.get("key_factors")
                score_data["recommendations"] = insights.get("recommendations")
                score_data["ai_insight"] = insights.get("summary")  # For backward compatibility

            underwriting = self._normalize_data(_call_tool("generate_underwriting_note", score_data=score_data))
            if underwriting:
                score_data["underwriting_note"] = underwriting.get("underwriting_note")
                score_data["recommendation"] = underwriting.get("recommendation")

            account_summaries = statement_data.get("account_summaries", [])
            selected_account_id = payload.get("account_id")
            if not selected_account_id and account_summaries:
                selected_account_id = account_summaries[0].get("account_id")

            if not selected_account_id:
                raise ValueError("Unable to determine account_id for report generation")

            pdf_result = self._normalize_data(_call_tool(
                "create_pdf",
                user_id=user_id,
                account_id=selected_account_id,
                score_data=score_data,
                features=features
            ))
            report_path = pdf_result.get("report_path")
            if report_path:
                score_data["report_path"] = report_path
                self._send_report_email(user_id, score_data, report_path)

            save_result = self._normalize_data(_call_tool(
                "save_score_in_db",
                user_id=user_id,
                account_id=selected_account_id,
                score_data=score_data
            ))

            final_payload = self._normalize_data({
                "user_id": user_id,
                "account_id": selected_account_id,
                "score_data": score_data,
                "features": features,
                "report_path": report_path,
                "account_summaries": account_summaries,
                "total_transactions": statement_data.get("total_transactions"),
                "db_record": save_result
            })

            return create_task_response(
                status="completed",
                task=TaskType.RUN_SCORING,
                data=final_payload
            )
        except Exception as e:
            print(f"[CredifyAgent] Scoring pipeline failed: {str(e)}")
            return create_task_response(
                status="failed",
                task=TaskType.RUN_SCORING,
                error=str(e)
            )
    
    def run_task(self, task_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task using the agent
        
        Args:
            task_dict: Dictionary with 'task' (task type) and 'payload' (parameters)
            
        Returns:
            Standardized response with status, task, data, and error
        """
        # Retry configuration - optimized for rate limiting
        max_retries = 2  # Reduced retries to avoid quota exhaustion (User Fix)
        base_delay = 30  # Increased base delay (User Fix)
        
        for attempt in range(max_retries + 1):
            try:
                task_type = task_dict.get("task")
                payload = task_dict.get("payload", {})
                
                # Validate task
                task_def = get_task_definition(task_type)
                if not task_def:
                    return create_task_response(
                        status="failed",
                        task=task_type,
                        error=f"Unknown task type: {task_type}"
                    )
                
                # Validate parameters
                is_valid, error_msg = validate_task_params(task_type, payload)
                if not is_valid:
                    return create_task_response(
                        status="failed",
                        task=task_type,
                        error=error_msg
                    )

                # Fast-path deterministic tasks (reduces extra Gemini calls)
                if task_type == TaskType.RUN_SCORING:
                    return self._execute_run_scoring_pipeline(payload)
                
                print(f"[CredifyAgent] Executing task: {task_type} (Attempt {attempt + 1}/{max_retries + 1})")
                print(f"[CredifyAgent] Payload: {payload}")
                
                # Get task-specific system prompt
                system_prompt = get_task_system_prompt(task_type)
                
                # Get execution template
                execution_template = get_task_execution_template(task_type, payload)
                
                # Create user prompt with explicit parameter values
                user_prompt = f"""
Task: {task_type}
Description: {task_def['description']}

IMPORTANT: You have access to these parameters:
{json.dumps(payload, indent=2)}

{execution_template}

CRITICAL INSTRUCTIONS:
- When calling functions, you MUST pass the required parameters
- The user_id is: {payload.get('user_id', 'NOT_PROVIDED')}
- Always use the exact parameter values provided above
- For fetch_all_user_statements, you MUST call it as: fetch_all_user_statements(user_id="{payload.get('user_id', '')}")

Execute this task step by step using the available tools.
Return ONLY the final result data as a JSON object, no additional text.
"""
                
                # Start chat session WITHOUT automatic function calling
                # We'll handle function calls manually for better control
                chat = self.model.start_chat()
                
                # Send initial message
                def _send_message():
                    return chat.send_message(user_prompt)
                
                response = rate_limited_call(_send_message)
                
                # Manual function calling loop
                max_function_iterations = 10
                iteration = 0
                malformed_recovery_attempts = 0
                max_malformed_retries = 2

                def _handle_malformed_call(
                    malformed_tool_name: Optional[str] = None,
                    malformed_args: Optional[Dict[str, Any]] = None,
                    error_hint: Optional[str] = None
                ):
                    nonlocal malformed_recovery_attempts

                    if malformed_recovery_attempts >= max_malformed_retries:
                        error_msg = "Model made a malformed function call."
                        if malformed_tool_name:
                            error_msg += f" Attempted to call: {malformed_tool_name}"
                        if error_hint:
                            error_msg += f" Details: {error_hint}"
                        raise ValueError(error_msg)

                    malformed_recovery_attempts += 1

                    valid_tools = ", ".join(sorted(ALL_TOOLS.keys()))
                    correction_message = [
                        "Your previous tool call was rejected as malformed.",
                        "Call only the registered tools with valid JSON args.",
                        f"Available tools: {valid_tools}.",
                    ]

                    if error_hint:
                        correction_message.append(f"Error details: {error_hint}")

                    if malformed_tool_name:
                        correction_message.append(
                            f"Retry the call to `{malformed_tool_name}` with all required parameters."
                        )
                        schema = self.tool_schema_lookup.get(malformed_tool_name, {})
                        required_params = schema.get("parameters", {}).get("required", [])
                        if required_params:
                            correction_message.append(
                                f"Required params: {', '.join(required_params)}."
                            )

                    if malformed_args:
                        try:
                            args_str = json.dumps(malformed_args, ensure_ascii=True)
                        except TypeError:
                            args_str = str(malformed_args)
                        correction_message.append(f"Previous args: {args_str}")

                    correction_message.append("Respond again with a valid function call or the final JSON result.")
                    correction_prompt = "\n".join(correction_message)

                    def _send_correction():
                        return chat.send_message(correction_prompt)

                    return rate_limited_call(_send_correction)
                
                while iteration < max_function_iterations:
                    iteration += 1
                    
                    # Check for malformed function call
                    if hasattr(response, 'candidates') and response.candidates:
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'finish_reason'):
                            finish_reason = str(candidate.finish_reason)
                            if 'MALFORMED_FUNCTION_CALL' in finish_reason:
                                malformed_tool_name = None
                                malformed_args = None
                                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                                    for part in candidate.content.parts:
                                        if hasattr(part, 'function_call') and part.function_call:
                                            malformed_tool_name = getattr(part.function_call, "name", None)
                                            malformed_args = getattr(part.function_call, "args", None)
                                            break

                                response = _handle_malformed_call(
                                    malformed_tool_name=malformed_tool_name,
                                    malformed_args=malformed_args
                                )
                                continue
                    
                    # Check if we have function calls to execute
                    function_calls = []
                    if hasattr(response, 'candidates') and response.candidates:
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                function_calls.append(part.function_call)
                    
                    # If no function calls, we have the final response
                    if not function_calls:
                        # Extract text safely
                        try:
                            result_text = response.text
                        except Exception:
                            # Handle mixed content
                            parts = []
                            if hasattr(response, 'parts'):
                                for part in response.parts:
                                    if hasattr(part, 'text') and part.text:
                                        parts.append(part.text)
                            result_text = "".join(parts)
                        
                        if not result_text:
                            raise ValueError("Model returned no text response")
                        
                        # Try to parse as JSON
                        try:
                            result_data = json.loads(result_text)
                        except json.JSONDecodeError:
                            # If not JSON, wrap in data field
                            result_data = {"result": result_text}
                        
                        print(f"[CredifyAgent] Task completed: {task_type}")
                        
                        return create_task_response(
                            status="completed",
                            task=task_type,
                            data=result_data
                        )
                    
                    # Execute function calls
                    print(f"[CredifyAgent] Executing {len(function_calls)} function call(s)")
                    
                    function_responses = []
                    function_call_contexts = []
                    for fc in function_calls:
                        tool_name = fc.name
                        tool_args = dict(fc.args) if fc.args else {}
                        function_call_contexts.append({
                            "name": tool_name,
                            "args": tool_args
                        })
                        
                        print(f"[CredifyAgent] Calling tool: {tool_name} with args: {tool_args}")
                        
                        # Execute tool
                        tool_result = execute_tool(tool_name, **tool_args)
                        
                        print(f"[CredifyAgent] Tool result success: {tool_result.get('success', False)}")
                        
                        # Simplify the response - just send the data part if successful
                        # This helps the model understand what to do next
                        if tool_result.get('success'):
                            response_content = self._make_json_safe(tool_result.get('data', {}))
                        else:
                            response_content = self._make_json_safe({
                                "error": tool_result.get('error', 'Unknown error'),
                                "success": False
                            })
                        
                        # Create function response in Gemini format
                        from google.ai.generativelanguage_v1beta.types import content as glm_content
                        function_responses.append(
                            glm_content.Part(
                                function_response=glm_content.FunctionResponse(
                                    name=tool_name,
                                    response={"content": response_content}
                                )
                            )
                        )
                    
                    print(f"[CredifyAgent] Sending {len(function_responses)} function response(s) back to model")
                    
                    # Wrap parts in Content with function role
                    function_response_message = glm_content.Content(
                        role="function",
                        parts=function_responses
                    )
                    
                    # Send function responses back to model
                    def _send_function_response():
                        return chat.send_message(function_response_message)
                    
                    try:
                        response = rate_limited_call(_send_function_response)
                    except Exception as send_err:
                        error_text = str(send_err)
                        if "MALFORMED_FUNCTION_CALL" in error_text:
                            context_entry = function_call_contexts[0] if function_call_contexts else {}
                            response = _handle_malformed_call(
                                malformed_tool_name=context_entry.get("name"),
                                malformed_args=context_entry.get("args"),
                                error_hint=error_text
                            )
                            continue
                        raise
                
                # Max iterations reached
                raise ValueError(f"Max function calling iterations ({max_function_iterations}) reached")
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and attempt < max_retries:
                    import time
                    import random
                    import re
                    
                    # Try to extract wait time from error message
                    # Look for "Please retry in X.Xs" or "retry_delay { seconds: X }"
                    wait_time = 0
                    
                    # Pattern 1: "Please retry in 11.2329259s"
                    match1 = re.search(r"Please retry in (\d+(\.\d+)?)s", error_str)
                    if match1:
                        wait_time = float(match1.group(1))
                    
                    # Pattern 2: "retry_delay { seconds: 11 }"
                    if not wait_time:
                        match2 = re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)", error_str)
                        if match2:
                            wait_time = float(match2.group(1))
                    
                    # Calculate exponential backoff with more aggressive delays
                    backoff_delay = (base_delay * (3 ** attempt)) + random.uniform(0, 2)
                    
                    # Use the larger of the two, plus a larger buffer
                    final_delay = max(wait_time, backoff_delay) + 5.0  # Increased buffer
                    
                    print(f"[CredifyAgent] Rate limit hit. Retrying in {final_delay:.2f}s... (Attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(final_delay)
                    continue
                
                print(f"[CredifyAgent] Task failed: {error_str}")
                return create_task_response(
                    status="failed",
                    task=task_dict.get("task", "unknown"),
                    error=error_str
                )
    
    def run_task_manual(self, task_dict: Dict[str, Any], max_iterations: int = 10) -> Dict[str, Any]:
        """
        Execute a task with manual function calling control (fallback method)
        
        This method manually handles the function calling loop instead of using
        automatic function calling. Useful for debugging or when more control is needed.
        """
        try:
            task_type = task_dict.get("task")
            payload = task_dict.get("payload", {})
            
            # Validate task
            is_valid, error_msg = validate_task_params(task_type, payload)
            if not is_valid:
                return create_task_response(
                    status="failed",
                    task=task_type,
                    error=error_msg
                )
            
            # Get task prompt
            system_prompt = get_task_system_prompt(task_type)
            execution_template = get_task_execution_template(task_type, payload)
            
            user_prompt = f"""
{system_prompt}

Task: {task_type}
Parameters: {json.dumps(payload, indent=2)}

{execution_template}

Execute this task using the available tools.
"""
            
            # Manual function calling loop
            chat = self.model.start_chat()
            current_prompt = user_prompt
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                response = chat.send_message(current_prompt)
                
                # Check if function calls are requested
                if not response.candidates[0].content.parts:
                    break
                
                function_calls = []
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        function_calls.append(part.function_call)
                
                if not function_calls:
                    # No more function calls, we have final response
                    result_text = response.text
                    try:
                        result_data = json.loads(result_text)
                    except:
                        result_data = {"result": result_text}
                    
                    return create_task_response(
                        status="completed",
                        task=task_type,
                        data=result_data
                    )
                
                # Execute function calls
                function_responses = []
                for fc in function_calls:
                    tool_name = fc.name
                    tool_args = dict(fc.args)
                    
                    print(f"[CredifyAgent] Calling tool: {tool_name} with args: {tool_args}")
                    
                    # Execute tool
                    tool_result = execute_tool(tool_name, **tool_args)
                    
                    function_responses.append({
                        "name": tool_name,
                        "response": tool_result
                    })
                
                # Send function results back
                current_prompt = json.dumps(function_responses)
            
            # Max iterations reached
            return create_task_response(
                status="failed",
                task=task_type,
                error="Max iterations reached without completion"
            )
            
        except Exception as e:
            return create_task_response(
                status="failed",
                task=task_dict.get("task", "unknown"),
                error=str(e)
            )


# Global agent instance
_agent_instance: Optional[CredifyAgent] = None


def get_agent() -> CredifyAgent:
    """Get or create the global agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CredifyAgent()
    return _agent_instance


def run_agent_task(task_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to run a task using the global agent instance
    
    Args:
        task_dict: Dictionary with 'task' and 'payload'
        
    Returns:
        Task execution result
    """
    agent = get_agent()
    return agent.run_task(task_dict)
