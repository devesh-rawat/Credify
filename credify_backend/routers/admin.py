from fastapi import APIRouter, Depends, HTTPException
from database.mongo import db
from models.application import ApplicationDecision
from core.security import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import List
from services.email_service import email_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_admin/token", scheme_name="AdminAuth")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        role: str = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Not an admin")
        return payload # Returns dict with bank_id, branch_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/applications")
def get_branch_applications(admin: dict = Depends(get_current_admin)):
    """
    Get all applications for the admin's branch with full scoring details.
    Includes credit score, risk assessment, AI insights, and report URL.
    """
    bank_id = admin.get("bank_id")
    branch_id = admin.get("branch_id")
    
    query = {"bank_id": bank_id, "branch_id": branch_id}
    apps = list(db.get_db().applications.find(query).sort("created_at", -1))
    
    # Enrich each application with full scoring details
    for app in apps:
        app["_id"] = str(app["_id"])
        
        # Fetch the latest scoring result for this user
        user_id = app.get("user_id")
        if user_id:
            score_result = db.get_db().scoring_results.find_one(
                {"user_id": user_id},
                sort=[("created_at", -1)]
            )
            
            if score_result:
                # Extract insights (same logic as /scoring/me)
                insights = score_result.get("insights", {})
                if not isinstance(insights, dict):
                    insights = {}
                
                # Build scoring details matching /scoring/me format
                app["scoring_details"] = {
                    "credit_score": score_result.get("credit_score"),
                    "default_probability": score_result.get("default_probability"),
                    "risk_label": score_result.get("risk_label"),
                    "summary": (
                        insights.get("summary") or 
                        score_result.get("summary") or 
                        score_result.get("ai_insight", "")
                    ),
                    "key_factors": (
                        insights.get("key_factors") or 
                        score_result.get("key_factors", [])
                    ),
                    "recommendations": (
                        insights.get("recommendations") or 
                        score_result.get("recommendations", [])
                    ),
                    "underwriting_note": score_result.get("underwriting_note", []),
                    "recommendation": score_result.get("recommendation", "REVIEW"),
                    "report_path": score_result.get("report_path", ""),
                    "created_at": score_result.get("created_at").isoformat() if score_result.get("created_at") else None
                }
                
                # Also update the top-level report_url for backward compatibility
                app["report_url"] = score_result.get("report_path", "")
            else:
                app["scoring_details"] = None
                app["report_url"] = ""
        else:
            app["scoring_details"] = None
            app["report_url"] = ""
    
    return apps


@router.get("/applications/{app_id}")
def get_application_with_review(app_id: str, with_agent_review: bool = False, admin: dict = Depends(get_current_admin)):
    """
    Get application details with optional agent-based review
    
    Query params:
    - with_agent_review: If true, includes AI-generated review and recommendation
    """
    bank_id = admin.get("bank_id")
    branch_id = admin.get("branch_id")
    
    app = db.get_db().applications.find_one({"application_id": app_id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Access Control
    if app["bank_id"] != bank_id or app["branch_id"] != branch_id:
        raise HTTPException(status_code=403, detail="Access denied to this application")
    
    app["_id"] = str(app["_id"])
    
    # Add agent review if requested
    if with_agent_review:
        from agent.credify_agent import run_agent_task
        
        try:
            review_result = run_agent_task({
                "task": "admin_review",
                "payload": {
                    "application_id": app_id,
                    "admin_id": admin.get("sub"),
                    "admin_bank_id": bank_id,
                    "admin_branch_id": branch_id
                }
            })
            
            if review_result["status"] == "completed":
                app["agent_review"] = review_result.get("data", {})
            else:
                app["agent_review"] = {"error": review_result.get("error")}
        except Exception as e:
            app["agent_review"] = {"error": str(e)}
    
    return app


@router.post("/applications/{app_id}/decision")
def decide_application(app_id: str, decision: ApplicationDecision, admin: dict = Depends(get_current_admin)):
    bank_id = admin.get("bank_id")
    branch_id = admin.get("branch_id")
    
    app = db.get_db().applications.find_one({"application_id": app_id})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Access Control
    if app["bank_id"] != bank_id or app["branch_id"] != branch_id:
        raise HTTPException(status_code=403, detail="Access denied to this application")
        
    db.get_db().applications.update_one(
        {"application_id": app_id},
        {"$set": {"status": decision.status, "admin_notes": decision.notes}}
    )
    
    decision_status = (decision.status or "").upper()
    if decision_status in {"APPROVED", "REJECTED"}:
        user = db.get_db().users.find_one({"user_id": app["user_id"]})
        if user and user.get("email"):
            user_name = user.get("name") or user.get("full_name") or "there"
            subject = "Your loan application has been approved!" if decision_status == "APPROVED" else "Update on your loan application"
            amount_value = app.get("amount", 0)
            try:
                amount_display = f"Rs. {float(amount_value):,.2f}"
            except (TypeError, ValueError):
                amount_display = str(amount_value)
            context = {
                "user_name": user_name,
                "amount": amount_display,
                "purpose": app.get("purpose", "N/A"),
                "bank_id": app.get("bank_id"),
                "branch_id": app.get("branch_id"),
                "status": decision_status,
                "notes": decision.notes or "",
            }
            email_service.send_templated_email(
                user["email"],
                subject,
                "application_decision.html",
                context
            )
    
    return {"message": "Decision recorded"}


