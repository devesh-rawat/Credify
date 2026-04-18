"""
Credify Chat Agent
Conversational AI assistant for credit score explanations and financial guidance
"""

import os
import json
from typing import Dict, Any, Optional
import google.generativeai as genai
from agent.agent_tools import execute_tool


class CredifyChatAgent:
    """
    Chatbot agent for user assistance and financial guidance
    Uses Gemini with grounded generation for accurate responses
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the Chat Agent
        
        Args:
            api_key: Gemini API key
            model_name: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.model_name = model_name
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # System instruction for the chatbot
        self.system_instruction = """You are Credify Assistant, a helpful and friendly financial advisor chatbot.

Your capabilities:
1. Explain credit scores in simple, easy-to-understand language
2. Interpret risk classifications (Low, Medium, High)
3. Provide actionable financial improvement guidance
4. Help admins understand user financial profiles
5. Answer questions about RBI regulations and Account Aggregator framework
6. Provide general financial literacy education

Guidelines:
- Use simple, non-technical language
- Be encouraging and supportive
- Provide specific, actionable advice
- Cite regulations accurately when discussing RBI/AA topics
- Never make promises about loan approval
- Protect user privacy - don't share specific user data unless authorized
- If you don't know something, admit it rather than guessing

Tone: Friendly, professional, educational, and empowering."""
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )
        
        # Chat sessions (keyed by user_id for context)
        self.sessions = {}
        
        print(f"[CredifyChatAgent] Initialized with model: {self.model_name}")
    
    def query(self, query: str, user_id: Optional[str] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a user query
        
        Args:
            query: User's question or message
            user_id: Optional user ID for personalized responses
            context: Optional context data (e.g., user's score data)
            
        Returns:
            Response with answer and metadata
        """
        try:
            # Get or create chat session
            if user_id and user_id in self.sessions:
                chat = self.sessions[user_id]
            else:
                chat = self.model.start_chat()
                if user_id:
                    self.sessions[user_id] = chat
            
            # Build enhanced query with context
            enhanced_query = self._build_query_with_context(query, user_id, context)
            
            # Send message
            response = chat.send_message(enhanced_query)
            
            return {
                "success": True,
                "answer": response.text,
                "query": query,
                "user_id": user_id
            }
            
        except Exception as e:
            print(f"[CredifyChatAgent] Error: {str(e)}")
            return {
                "success": False,
                "answer": "I apologize, but I encountered an error processing your question. Please try again.",
                "error": str(e)
            }
    
    def _build_query_with_context(self, query: str, user_id: Optional[str], context: Optional[Dict]) -> str:
        """Build an enhanced query with user context"""
        enhanced_parts = [query]
        
        # Add user context if available
        if user_id and not context:
            # Try to fetch user's score for context
            try:
                score_result = execute_tool("get_latest_score", user_id=user_id)
                if score_result.get("success"):
                    context = score_result.get("data")
            except:
                pass
        
        # Add context information
        if context:
            context_str = f"\n\nUser Context:\n"
            if "credit_score" in context:
                context_str += f"- Credit Score: {context['credit_score']}\n"
            if "risk_label" in context:
                context_str += f"- Risk Level: {context['risk_label']}\n"
            if "default_probability" in context:
                context_str += f"- Default Probability: {context['default_probability']:.2%}\n"
            
            enhanced_parts.append(context_str)
        
        return "\n".join(enhanced_parts)
    
    def explain_score(self, user_id: str) -> Dict[str, Any]:
        """
        Provide a detailed explanation of a user's credit score
        
        Args:
            user_id: User ID to explain score for
            
        Returns:
            Detailed score explanation
        """
        try:
            # Fetch user's score
            score_result = execute_tool("get_latest_score", user_id=user_id)
            
            if not score_result.get("success"):
                return {
                    "success": False,
                    "answer": "I couldn't find a credit score for this user. Please ensure they have completed the credit assessment.",
                    "error": score_result.get("error")
                }
            
            score_data = score_result.get("data", {})
            
            # Create explanation prompt
            prompt = f"""Please explain this credit score to the user in simple, friendly language:

Credit Score: {score_data.get('credit_score')}
Risk Level: {score_data.get('risk_label')}
Default Probability: {score_data.get('default_probability', 0):.2%}

Include:
1. What this score means (excellent/good/fair/poor)
2. What the risk level indicates
3. How this might affect loan applications
4. 3-5 specific tips for improving the score
5. Encouraging words

Keep it conversational and easy to understand."""
            
            chat = self.model.start_chat()
            response = chat.send_message(prompt)
            
            return {
                "success": True,
                "answer": response.text,
                "score_data": score_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": "I encountered an error explaining the score.",
                "error": str(e)
            }
    
    def financial_guidance(self, topic: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Provide financial guidance on a specific topic
        
        Args:
            topic: Topic for guidance (e.g., "saving", "debt management", "credit building")
            user_context: Optional user financial context
            
        Returns:
            Guidance response
        """
        try:
            prompt = f"Provide practical financial guidance on: {topic}"
            
            if user_context:
                prompt += f"\n\nUser's financial context:\n{json.dumps(user_context, indent=2)}"
            
            prompt += "\n\nProvide 5-7 actionable tips that are specific and practical."
            
            chat = self.model.start_chat()
            response = chat.send_message(prompt)
            
            return {
                "success": True,
                "answer": response.text,
                "topic": topic
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": "I encountered an error providing guidance.",
                "error": str(e)
            }
    
    def rbi_aa_info(self, question: str) -> Dict[str, Any]:
        """
        Answer questions about RBI regulations and Account Aggregator framework
        
        Args:
            question: Question about RBI/AA
            
        Returns:
            Answer with citations
        """
        try:
            prompt = f"""Answer this question about RBI regulations or the Account Aggregator framework:

{question}

Provide accurate information based on RBI guidelines. If you're not certain about specific regulations, 
indicate that the user should verify with official RBI sources. Be clear and educational."""
            
            chat = self.model.start_chat()
            response = chat.send_message(prompt)
            
            return {
                "success": True,
                "answer": response.text,
                "question": question
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": "I encountered an error answering your question.",
                "error": str(e)
            }
    
    def admin_user_insight(self, user_id: str, application_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Provide admin with insights about a user for application review
        
        Args:
            user_id: User ID to analyze
            application_id: Optional application ID for context
            
        Returns:
            Admin-focused insights
        """
        try:
            # Fetch user's score
            score_result = execute_tool("get_latest_score", user_id=user_id)
            
            if not score_result.get("success"):
                return {
                    "success": False,
                    "answer": "Could not fetch user data.",
                    "error": score_result.get("error")
                }
            
            score_data = score_result.get("data", {})
            
            # Create admin insight prompt
            prompt = f"""As an admin reviewing a loan application, provide insights about this user:

Credit Score: {score_data.get('credit_score')}
Risk Level: {score_data.get('risk_label')}
Default Probability: {score_data.get('default_probability', 0):.2%}

Key Financial Factors:
{json.dumps(score_data.get('key_factors', []), indent=2)}

Provide:
1. Overall risk assessment
2. Key strengths in the profile
3. Key concerns or red flags
4. Recommendation (Approve/Review/Reject) with reasoning
5. Suggested loan terms (if applicable)

Be professional and analytical."""
            
            chat = self.model.start_chat()
            response = chat.send_message(prompt)
            
            return {
                "success": True,
                "answer": response.text,
                "user_id": user_id,
                "score_data": score_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": "Error generating admin insights.",
                "error": str(e)
            }
    
    def clear_session(self, user_id: str):
        """Clear chat session for a user"""
        if user_id in self.sessions:
            del self.sessions[user_id]


# Global chat agent instance
_chat_agent_instance: Optional[CredifyChatAgent] = None


def get_chat_agent() -> CredifyChatAgent:
    """Get or create the global chat agent instance"""
    global _chat_agent_instance
    if _chat_agent_instance is None:
        _chat_agent_instance = CredifyChatAgent()
    return _chat_agent_instance


def chat_query(query: str, user_id: Optional[str] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Convenience function to query the chatbot
    
    Args:
        query: User's question
        user_id: Optional user ID
        context: Optional context data
        
    Returns:
        Chatbot response
    """
    agent = get_chat_agent()
    return agent.query(query, user_id, context)
