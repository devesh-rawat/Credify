"""
Agent Routes for Credify Backend
FastAPI endpoints for agent and chatbot functionality
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from agent.credify_agent import run_agent_task
from agent.agent_runtime import log_agent_activity, get_metrics
from routers.admin import get_current_admin


router = APIRouter()


# ==================== REQUEST/RESPONSE MODELS ====================

class AgentTaskRequest(BaseModel):
    """Request model for agent task execution"""
    task: str = Field(..., description="Task type to execute")
    payload: Dict[str, Any] = Field(..., description="Task parameters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task": "run_scoring",
                "payload": {
                    "user_id": "U001",
                    "account_id": "ACC001"
                }
            }
        }


class AgentTaskResponse(BaseModel):
    """Response model for agent task execution"""
    status: str = Field(..., description="Task status: completed or failed")
    task: str = Field(..., description="Task type that was executed")
    data: Optional[Dict[str, Any]] = Field(None, description="Result data if successful")
    error: Optional[str] = Field(None, description="Error message if failed")


class ChatQueryRequest(BaseModel):
    """Request model for chatbot queries"""
    query: str = Field(..., description="User's question or message")
    user_id: Optional[str] = Field(None, description="Optional user ID for context")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional additional context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is a good credit score?",
                "user_id": "U001"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chatbot queries"""
    success: bool
    answer: str
    query: Optional[str] = None
    user_id: Optional[str] = None
    error: Optional[str] = None


class ExplainScoreRequest(BaseModel):
    """Request model for score explanation"""
    user_id: str = Field(..., description="User ID to explain score for")


class FinancialGuidanceRequest(BaseModel):
    """Request model for financial guidance"""
    topic: str = Field(..., description="Topic for guidance")
    user_context: Optional[Dict[str, Any]] = Field(None, description="Optional user context")


class RBIQuestionRequest(BaseModel):
    """Request model for RBI/AA questions"""
    question: str = Field(..., description="Question about RBI or AA framework")


class AdminInsightRequest(BaseModel):
    """Request model for admin user insights"""
    user_id: str = Field(..., description="User ID to analyze")
    application_id: Optional[str] = Field(None, description="Optional application ID")


# ==================== AGENT ENDPOINTS ====================




@router.get("/metrics")
def get_agent_metrics(admin: dict = Depends(get_current_admin)):
    """
    Get agent execution metrics
    
    Requires admin authentication.
    """
    metrics = get_metrics()
    return metrics.get_summary()



