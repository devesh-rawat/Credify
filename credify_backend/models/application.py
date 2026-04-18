from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    account_id: str
    amount: float = Field(..., gt=0, description="Loan amount requested (must be greater than 0)")
    purpose: str = Field(..., min_length=1, description="Purpose of the loan")

class ApplicationResponse(BaseModel):
    application_id: str
    user_id: str
    user_name: str
    bank_id: str
    branch_id: str
    status: str
    score: float
    risk_label: str
    report_url: str
    created_at: datetime
    amount: Optional[float] = 0.0
    purpose: Optional[str] = ""
    admin_notes: Optional[str] = None

class ApplicationDecision(BaseModel):
    status: str
    notes: Optional[str] = None
