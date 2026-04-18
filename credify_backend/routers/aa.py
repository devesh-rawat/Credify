from fastapi import APIRouter, Depends, HTTPException
from services.aa_service import aa_service
from core.security import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from database.mongo import db
from bson import ObjectId

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

@router.get("/banks")
def get_banks(user_id: str = Depends(get_current_user)):
    # Fetch user from DB to get email
    user = db.get_db().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return aa_service.get_user_accounts_by_email(user["email"])


