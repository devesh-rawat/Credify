from pydantic import BaseModel

class OTPRequest(BaseModel):
    aadhaar: str
    pan: str
    loan_amount: float

class OTPVerifyRequest(BaseModel):
    aadhaar: str
    otp: str

class ConsentRequest(BaseModel):
    consent_granted: bool
