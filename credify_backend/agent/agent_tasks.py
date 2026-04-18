"""
Agent Tasks for Credify Backend
Defines task templates and execution logic for the Credify orchestrator agent
"""

from typing import Dict, Any, List
from enum import Enum


class TaskType(str, Enum):
    """Supported task types"""
    RUN_SCORING = "run_scoring"
    APPLY_FOR_LOAN = "apply_for_loan"
    EXPLAIN_SCORE = "explain_score"
    ADMIN_REVIEW = "admin_review"
    DETECT_ANOMALIES = "detect_anomalies"
    RESCORE_USER = "rescore_user"


# Task definitions with required parameters and tool sequences
TASK_DEFINITIONS = {
    TaskType.RUN_SCORING: {
        "description": "Complete credit scoring pipeline: fetch statements from ALL accounts, extract features, predict score, generate insights, create PDF, and save results",
        "required_params": ["user_id"],
        "optional_params": ["account_id"],
        "tools_sequence": [
            "fetch_all_user_statements",
            "extract_features",
            "predict_score",
            "generate_ai_insight",
            "generate_underwriting_note",
            "create_pdf",
            "save_score_in_db"
        ],
        "system_prompt": """You are the Credify Orchestrator executing a credit scoring pipeline.
Your task is to:
1. Fetch bank statements from ALL user accounts for comprehensive analysis
2. Extract financial features from combined transactions
3. Predict credit score using ML model
4. Generate AI insights about financial health
5. Create underwriting notes for loan officers
5. Create underwriting notes for loan officers
6. Generate a PDF report
7. Save all results to database

Execute each step in sequence and handle any errors gracefully.
Return a structured JSON response with the final credit score and report location."""
    },
    
    TaskType.APPLY_FOR_LOAN: {
        "description": "Loan application workflow: validate user, select account, generate application summary, and save application",
        "required_params": ["user_id", "account_id", "amount", "purpose"],
        "optional_params": [],
        "tools_sequence": [
            "fetch_aa_accounts",
            "get_latest_score",
            "save_application_in_db",
            "send_email"
        ],
        "system_prompt": """You are the Credify Orchestrator processing a loan application.
Your task is to:
1. Fetch user's bank accounts to verify the account_id
2. Get the user's latest credit score
3. Create and save the loan application in the database
4. Send confirmation email to the user using their user_id

Execute each step and return the application details.
Return a structured JSON with application_id, status, and confirmation."""
    },
    
    TaskType.EXPLAIN_SCORE: {
        "description": "Explain credit score in simple, user-friendly language",
        "required_params": ["user_id"],
        "optional_params": [],
        "tools_sequence": [
            "get_latest_score"
        ],
        "system_prompt": """You are the Credify Orchestrator explaining a credit score to a user.
Your task is to:
1. Fetch the user's latest credit score
2. Explain what the score means in simple, non-technical language
3. Explain the risk label (Low/Medium/High)
4. Provide actionable advice for improvement

Use friendly, encouraging language. Avoid jargon.
Return a structured explanation with score interpretation and improvement tips."""
    },
    
    TaskType.ADMIN_REVIEW: {
        "description": "Admin application review with AI-generated insights and recommendations",
        "required_params": ["application_id", "admin_bank_id", "admin_branch_id"],
        "optional_params": ["admin_id"],
        "tools_sequence": [
            "check_admin_access",
            "get_application_by_id",
            "get_latest_score"
        ],
        "system_prompt": """You are the Credify Orchestrator assisting an admin with application review.
Your task is to:
1. Verify the admin has access to this application (branch isolation)
2. Fetch the application details
3. Retrieve the applicant's credit score and insights
4. Generate a comprehensive review with recommendation (APPROVE/REVIEW/REJECT)

Consider credit score, risk label, and financial patterns.
Provide clear reasoning for your recommendation.
Return structured JSON with review summary and decision recommendation."""
    },
    
    TaskType.DETECT_ANOMALIES: {
        "description": "Detect anomalies and suspicious patterns in transaction data across ALL accounts",
        "required_params": ["user_id"],
        "optional_params": ["account_id"],
        "tools_sequence": [
            "fetch_all_user_statements",
            "extract_features"
        ],
        "system_prompt": """You are the Credify Orchestrator detecting financial anomalies.
Your task is to:
1. Fetch the user's bank statements from ALL accounts
2. Extract financial features
3. Analyze for suspicious patterns such as:
   - Sudden large transactions
   - Unusual spending categories
   - Irregular income patterns
   - High gambling or risky spending
   - Debt accumulation patterns

Return a structured report of detected anomalies with severity levels (LOW/MEDIUM/HIGH).
Include specific transaction patterns that triggered alerts."""
    },
    
    TaskType.RESCORE_USER: {
        "description": "Re-run credit scoring for an existing user with updated data from ALL accounts",
        "required_params": ["user_id"],
        "optional_params": ["account_id"],
        "tools_sequence": [
            "fetch_all_user_statements",
            "extract_features",
            "predict_score",
            "generate_ai_insight",
            "generate_underwriting_note",
            "create_pdf",
            "save_score_in_db"
        ],
        "system_prompt": """You are the Credify Orchestrator re-scoring a user.
Your task is to:
1. Fetch the latest bank statements from ALL user accounts
2. Extract updated financial features from combined transactions
3. Generate new credit score prediction
4. Create fresh AI insights
5. Generate updated underwriting notes
5. Generate updated underwriting notes
6. Create new PDF report
7. Save the updated score to database

This is identical to run_scoring but explicitly for re-evaluation.
Return the new credit score and comparison with previous score if available."""
    }
}


def get_task_definition(task_type: str) -> Dict[str, Any]:
    """Get task definition by type"""
    if task_type not in TaskType.__members__.values():
        return None
    return TASK_DEFINITIONS.get(task_type)


def validate_task_params(task_type: str, params: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate that all required parameters are present for a task
    Returns (is_valid, error_message)
    """
    task_def = get_task_definition(task_type)
    if not task_def:
        return False, f"Unknown task type: {task_type}"
    
    required = task_def["required_params"]
    missing = [p for p in required if p not in params]
    
    if missing:
        return False, f"Missing required parameters: {', '.join(missing)}"
    
    return True, ""


def get_task_system_prompt(task_type: str) -> str:
    """Get the system prompt for a specific task"""
    task_def = get_task_definition(task_type)
    if not task_def:
        return "You are the Credify Orchestrator. Execute the requested task."
    return task_def["system_prompt"]


def get_task_tools(task_type: str) -> List[str]:
    """Get the recommended tool sequence for a task"""
    task_def = get_task_definition(task_type)
    if not task_def:
        return []
    return task_def["tools_sequence"]


def create_task_response(status: str, task: str, data: Any = None, error: str = None) -> Dict[str, Any]:
    """
    Create a standardized task response
    
    Args:
        status: "completed" or "failed"
        task: Task type that was executed
        data: Result data (if successful)
        error: Error message (if failed)
    """
    return {
        "status": status,
        "task": task,
        "data": data,
        "error": error
    }


# Task execution templates for common patterns
TASK_EXECUTION_TEMPLATES = {
    TaskType.RUN_SCORING: """
Execute the credit scoring pipeline:
1. Call fetch_all_user_statements with user_id={user_id} to get transactions from ALL accounts
2. Extract the transactions array from the result
3. Call extract_features with the combined transactions
4. Call predict_score with the features from step 3
5. Call generate_ai_insight with features and score data
6. Merge the insights into score_data
7. Call generate_underwriting_note with the complete score_data
8. Merge underwriting notes into score_data
9. Call create_pdf with user_id, account_id (use first account from results), score_data, and features
10. Add the report_path to score_data
11. Call save_score_in_db with user_id, account_id="ALL_ACCOUNTS", and complete score_data

Return the final score_data with all components.
""",

    
    TaskType.APPLY_FOR_LOAN: """
Execute the loan application workflow:
1. Call fetch_aa_accounts with user_id={user_id} to verify account access
2. Check that account_id={account_id} exists in the user's accounts
3. Call get_latest_score with user_id={user_id}
4. If no score exists, return error "User must complete credit scoring first"
5. Call save_application_in_db with user_id, account_id, amount={amount}, purpose={purpose}
6. Call send_email with user_id={user_id}, subject="Loan Application Submitted", body="Your loan application has been submitted successfully"

Return the created application details.
""",
    
    TaskType.ADMIN_REVIEW: """
Execute the admin review workflow:
1. Call check_admin_access with admin_id={admin_id}, application_id={application_id}, admin_bank_id={admin_bank_id}, admin_branch_id={admin_branch_id}
2. If access denied, return error immediately
3. Call get_application_by_id with application_id={application_id}
4. Call get_latest_score with the user_id from the application
5. Analyze the score, risk label, and insights
6. Generate a recommendation: APPROVE (score >= 650), REVIEW (550-649), or REJECT (< 550)
7. Create a detailed review summary with reasoning

Return the review with recommendation and reasoning.
"""
}


def get_task_execution_template(task_type: str, params: Dict[str, Any]) -> str:
    """
    Get the execution template for a task with parameters filled in
    """
    template = TASK_EXECUTION_TEMPLATES.get(task_type, "")
    if not template:
        return ""
    
    # Fill in parameters
    try:
        return template.format(**params)
    except KeyError:
        return template
