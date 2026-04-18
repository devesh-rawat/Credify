from fastapi import APIRouter, Depends, HTTPException, status
from database.mongo import db
from models.admin import AdminCreate, AdminLogin, AdminResponse
from models.user import Token
from core.security import get_password_hash, verify_password, create_access_token
from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Allow login with email as username
    db_admin = db.get_db().admins.find_one({"email": form_data.username})
    if not db_admin or not verify_password(form_data.password, db_admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        subject=db_admin["admin_id"], 
        role="admin",
        bank_id=db_admin["bank_id"],
        branch_id=db_admin["branch_id"]
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_admin["admin_id"], "role": "admin"}

@router.post("/signup", response_model=Token)
def admin_signup(admin: AdminCreate):
    existing_admin = db.get_db().admins.find_one({"email": admin.email})
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    admin_dict = admin.dict()
    admin_dict["password"] = get_password_hash(admin.password)
    admin_dict["admin_id"] = f"A{datetime.now().timestamp()}"
    
    db.get_db().admins.insert_one(admin_dict)
    
    access_token = create_access_token(
        subject=admin_dict["admin_id"], 
        role="admin",
        bank_id=admin.bank_id,
        branch_id=admin.branch_id
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": admin_dict["admin_id"], "role": "admin"}

@router.post("/login", response_model=Token)
def admin_login(admin: AdminLogin):
    db_admin = db.get_db().admins.find_one({"email": admin.email})
    if not db_admin or not verify_password(admin.password, db_admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    access_token = create_access_token(
        subject=db_admin["admin_id"], 
        role="admin",
        bank_id=db_admin["bank_id"],
        branch_id=db_admin["branch_id"]
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_admin["admin_id"], "role": "admin"}
