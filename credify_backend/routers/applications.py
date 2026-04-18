from fastapi import APIRouter, Depends, HTTPException
from database.mongo import db
from models.application import ApplicationCreate, ApplicationResponse
from routers.aa import get_current_user
from services.aa_service import aa_service
from datetime import datetime
import re
import json

router = APIRouter()

@router.post("/apply", response_model=ApplicationResponse)
def apply_for_loan(app: ApplicationCreate, user_id: str = Depends(get_current_user)):
    # Use Gemini agent to handle loan application
    from agent.credify_agent import run_agent_task
    
    try:
        # 0. Check for existing pending applications
        existing_pending = db.get_db().applications.find_one({
            "user_id": user_id,
            "status": "PENDING"
        })
        
        if existing_pending:
            raise HTTPException(
                status_code=400,
                detail="You already have a pending loan application. Please wait for it to be processed before applying for another loan."
            )
        
        # 1. Verify account exists and belongs to user
        # Fetch user details first to get email/PAN/Aadhaar
        user = db.get_db().users.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Use email to find accounts (consistent with aa.py)
        accounts = aa_service.get_user_accounts_by_email(user["email"])
        
        # If no accounts found by email, try PAN/Aadhaar if available
        if not accounts and user.get("pan") and user.get("aadhaar"):
             accounts = aa_service.get_accounts_by_pan_aadhaar(user["pan"], user["aadhaar"])
             
        account = next((acc for acc in accounts if acc["account_id"] == app.account_id), None)
        if not account:
            raise HTTPException(status_code=400, detail="Invalid account ID or account does not belong to user")

        # 2. Check if credit score exists
        score_res = db.get_db().scoring_results.find_one({"user_id": user_id}, sort=[("created_at", -1)])
        if not score_res:
            raise HTTPException(
                status_code=400, 
                detail="Credit score not generated yet. Please complete the credit scoring process first by verifying your account with OTP."
            )

        # 3. Trigger Agent Task
        result = run_agent_task({
            "task": "apply_for_loan",
            "payload": {
                "user_id": user_id,
                "account_id": app.account_id,
                "amount": app.amount,
                "purpose": app.purpose,
                "bank_id": account["bank_id"],
                "branch_id": account["branch_id"]
            }
        })
        
        if result["status"] == "failed":
            raise HTTPException(status_code=400, detail=result.get("error", "Application failed"))
        
        # Debug: Log the result structure
        print(f"[DEBUG] Agent result keys: {list(result.keys())}")
        print(f"[DEBUG] Agent result data type: {type(result.get('data'))}")
        if isinstance(result.get("data"), dict):
            print(f"[DEBUG] Agent result data keys: {list(result.get('data', {}).keys())}")
        
        # Extract application data from agent result
        application_data = result.get("data", {})
        
        # Handle case where agent returns JSON as a string (wrapped in markdown code blocks)
        if isinstance(application_data, dict) and "result" in application_data:
            result_value = application_data["result"]
            if isinstance(result_value, str):
                # Try to parse JSON from string (may be wrapped in ```json ... ```)
                # Remove markdown code blocks
                cleaned = re.sub(r'```json\s*|\s*```', '', result_value).strip()
                try:
                    parsed_data = json.loads(cleaned)
                    print(f"[DEBUG] Parsed JSON from string, keys: {list(parsed_data.keys())}")
                    application_data = parsed_data
                except json.JSONDecodeError as e:
                    print(f"[ERROR] Failed to parse JSON: {e}")
        
        # The agent might return the application data directly or nested
        # Check if application_id is in the data, if not, check if data itself is the application
        if "application_id" not in application_data:
            # Check if the data contains a nested structure from save_application_in_db
            # The tool returns {success, data, error} where data contains the application
            if isinstance(application_data, dict):
                # Try to find application_id in nested structures
                for key in ["data", "application", "result", "application_details"]:
                    if key in application_data and isinstance(application_data[key], dict):
                        print(f"[DEBUG] Found nested key '{key}' with keys: {list(application_data[key].keys())}")
                        if "application_id" in application_data[key]:
                            application_data = application_data[key]
                            print(f"[DEBUG] Extracted application from nested key '{key}'")
                            break
        
        # Final validation
        if "application_id" not in application_data:
            print(f"[ERROR] No application_id found. Full data structure: {application_data}")
            raise HTTPException(
                status_code=500,
                detail=f"Agent failed to create application properly. Response structure: {list(application_data.keys()) if isinstance(application_data, dict) else type(application_data)}"
            )
        
        print(f"[DEBUG] Successfully extracted application: {application_data.get('application_id')}")
        return application_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Application error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Application error: {str(e)}")

@router.get("/my-applications", response_model=list[ApplicationResponse])
def get_my_applications(user_id: str = Depends(get_current_user)):
    """
    Get all loan applications for the current user.
    """
    applications = list(db.get_db().applications.find({"user_id": user_id}).sort("created_at", -1))
    
    # Convert ObjectId to string for Pydantic model compatibility if needed, 
    # though response_model usually handles it if we map it right. 
    # But let's be safe and ensure _id is handled or ignored.
    for app in applications:
        app["_id"] = str(app["_id"])
        
    return applications
