import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings
from core.security import get_password_hash, verify_password
from datetime import datetime, timedelta

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    return get_password_hash(otp)

def verify_otp_hash(otp: str, hashed_otp: str) -> bool:
    return verify_password(otp, hashed_otp)

def send_otp_email(email: str, otp: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Your Credify Verification OTP"

        body = f"Your OTP for Credify verification is: {otp}\n\nThis OTP expires in 5 minutes."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        if settings.EMAIL_PASS:
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(settings.EMAIL_USER, email, text)
        server.quit()
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
        # For dev/demo purposes, print OTP to console if email fails
        print(f"DEBUG OTP for {email}: {otp}")
