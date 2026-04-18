from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ScoringResult(BaseModel):
    user_id: str
    credit_score: float
    default_probability: float
    risk_label: str
    ai_insight: str
    underwriting_note: List[str]
    report_url: str
    created_at: datetime

class ApplicationCreate(BaseModel):
    account_id: str  # User selects which account to apply with

class ApplicationResponse(BaseModel):
    application_id: str
    user_id: str
    user_name: str
    bank_id: str
    branch_id: str
    status: str  # PENDING, APPROVED, REJECTED
    score: float
    risk_label: str
    report_url: str
    created_at: datetime
    admin_notes: Optional[str] = None

class ApplicationDecision(BaseModel):
    status: str # APPROVED, REJECTED
    notes: Optional[str] = None
