from fastapi import APIRouter, Depends, HTTPException
from services.agent_service import agent_service
from database.mongo import db
from routers.aa import get_current_user
from typing import Dict, Any
from agent.credify_agent import run_agent_task
from agent.agent_tasks import TaskType

router = APIRouter()

@router.get("/me")
def get_my_score(user_id: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get the latest credit score for the authenticated user.
    Returns detailed score data with AI insights and recommendations.
    Note: The score is calculated based on ALL user accounts for a comprehensive financial assessment.
    """
    # Get latest score from database
    result = db.get_db().scoring_results.find_one(
        {"user_id": user_id}, 
        sort=[("created_at", -1)]
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="No score found. Please complete credit scoring first.")
    
    # Convert ObjectId to string
    result["_id"] = str(result["_id"])
    
    # Ensure insights are properly structured
    # Check both nested 'insights' field and top-level fields
    insights = result.get("insights", {})
    if not isinstance(insights, dict):
        insights = {}
    
    # Extract summary from multiple possible locations
    summary = (
        insights.get("summary") or 
        result.get("summary") or 
        result.get("ai_insight", "")
    )
    
    # Extract key_factors from multiple possible locations
    key_factors = (
        insights.get("key_factors") or 
        result.get("key_factors", [])
    )
    
    # Extract recommendations from multiple possible locations
    recommendations = (
        insights.get("recommendations") or 
        result.get("recommendations", [])
    )
    
    # Build standardized response matching agent format
    response = {
        "user_id": result.get("user_id"),
        "credit_score": result.get("credit_score"),
        "default_probability": result.get("default_probability"),
        "risk_label": result.get("risk_label"),
        "summary": summary,
        "key_factors": key_factors,
        "recommendations": recommendations,
        "underwriting_note": result.get("underwriting_note", []),
        "recommendation": result.get("recommendation", "REVIEW"),
        "report_path": result.get("report_path", ""),
        "created_at": result.get("created_at").isoformat() if result.get("created_at") else None,
        "account_id": result.get("account_id", "ALL_ACCOUNTS")  # Default to ALL_ACCOUNTS if not specified
    }
    
    return response


@router.post("/generate")
def generate_score(user_id: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Trigger the AI agent to generate a credit score for the authenticated user.
    This runs the full scoring pipeline: fetch statements -> extract features -> predict score -> generate insights.
    """
    result = run_agent_task({
        "task": TaskType.RUN_SCORING,
        "payload": {
            "user_id": user_id
        }
    })
    
    if result.get("status") == "failed":
        raise HTTPException(status_code=500, detail=f"Scoring failed: {result.get('error')}")
        
    return result.get("data", {})


