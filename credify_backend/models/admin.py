from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    bank_id: str
    branch_id: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(BaseModel):
    admin_id: str
    name: str
    email: EmailStr
    bank_id: str
    branch_id: str
