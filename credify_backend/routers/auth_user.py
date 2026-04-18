from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.user import UserCreate, UserLogin, Token
from models.otp import OTPRequest, OTPVerifyRequest
from database.mongo import db
from core.security import get_password_hash, verify_password, create_access_token, settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from utils.otp_utils import generate_otp, hash_otp, verify_otp_hash, send_otp_email
from services.aa_service import aa_service
from services.agent_service import agent_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_user/token", scheme_name="UserAuth")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role != "user":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup", response_model=Token)
def signup(user: UserCreate):
    if db.get_db().users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    user_dict["user_id"] = f"U{datetime.now().timestamp()}"
    
    db.get_db().users.insert_one(user_dict)
    
    access_token = create_access_token(subject=user_dict["user_id"], role="user")
    return {"access_token": access_token, "token_type": "bearer", "user_id": user_dict["user_id"], "role": "user", "full_name": user_dict["full_name"]}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = db.get_db().users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    access_token = create_access_token(subject=db_user["user_id"], role="user")
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_user["user_id"], "role": "user", "full_name": db_user.get("full_name", "User")}

@router.post("/request-otp")
def request_otp(req: OTPRequest, user_id: str = Depends(get_current_user)):
    # Get user email
    user = db.get_db().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify if user has any bank accounts with provided PAN and Aadhaar
    accounts = aa_service.get_accounts_by_pan_aadhaar(req.pan, req.aadhaar)
    if not accounts:
        raise HTTPException(status_code=400, detail="No bank account found linked to these details")

    # Update user with provided PAN, Aadhaar, and loan_amount for future reference (e.g. in verify_otp)
    db.get_db().users.update_one(
        {"user_id": user_id},
        {"$set": {"pan": req.pan, "aadhaar": req.aadhaar, "loan_amount": req.loan_amount}}
    )
    
    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    otp_record = {
        "aadhaar": req.aadhaar,
        "otp_hash": otp_hash,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "user_id": user_id,
        "verified": False
    }
    
    # Upsert or Insert
    db.get_db().otps.update_one(
        {"user_id": user_id, "aadhaar": req.aadhaar},
        {"$set": otp_record},
        upsert=True
    )
    
    send_otp_email(user["email"], otp)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(req: OTPVerifyRequest, background_tasks: BackgroundTasks, user_id: str = Depends(get_current_user)):
    # Find the OTP record
    otp_record = db.get_db().otps.find_one({
        "user_id": user_id, 
        "aadhaar": req.aadhaar,
        "verified": False
    })
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP request or already verified")
    
    # Check expiry
    if datetime.utcnow() > otp_record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Verify hash
    if not verify_otp_hash(req.otp, otp_record["otp_hash"]):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Mark as verified
    db.get_db().otps.update_one(
        {"_id": otp_record["_id"]},
        {"$set": {"verified": True}}
    )
    
    # Trigger Agent-based Scoring Pipeline for ALL accounts
    user = db.get_db().users.find_one({"user_id": user_id})
    if user:
        # Use PAN and Aadhaar to verify accounts exist
        pan = user.get("pan")
        aadhaar = user.get("aadhaar")
        
        if pan and aadhaar:
            accounts = aa_service.get_accounts_by_pan_aadhaar(pan, aadhaar)
            
            if accounts:
                # Trigger multi-account scoring (no specific account_id needed)
                print(f"Triggering agent-based pipeline for user {user_id} on ALL accounts ({len(accounts)} total)")
                
                # Use Gemini agent to score all accounts
                from agent.credify_agent import run_agent_task
                
                def run_agent_scoring():
                    try:
                        result = run_agent_task({
                            "task": "run_scoring",
                            "payload": {
                                "user_id": user_id
                            }
                        })
                        print(f"Agent scoring result: {result['status']}")
                    except Exception as e:
                        print(f"Agent scoring error: {str(e)}")
                
                background_tasks.add_task(run_agent_scoring)
                
                return {
                    "message": "OTP verified successfully. Credit analysis started for all your bank accounts.",
                    "note": "This is a demo environment. For testing, please use seeded users (U001-U005) with email: user1@test.com to user5@test.com, password: password123"
                }
            else:
                print(f"No accounts found for user {user_id} with PAN {pan} and Aadhaar {aadhaar}")
        else:
            print(f"User {user_id} missing PAN or Aadhaar details")
            
    return {"message": "OTP verified successfully. Credit analysis started for all your bank accounts."}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_db().users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(subject=user["user_id"], role="user")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(user_id: str = Depends(get_current_user)):
    """Get current user's information"""
    user = db.get_db().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "full_name": user.get("full_name", "User"),
        "pan": user.get("pan"),
        "aadhaar": user.get("aadhaar")
    }
