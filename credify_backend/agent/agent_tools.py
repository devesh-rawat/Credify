"""
Agent Tools for Credify Backend
Exposes backend services as GADK-compatible tool functions
"""

from typing import Dict, List, Any, Optional
from services.aa_service import aa_service
from services.feature_service import feature_service
from services.ml_service import ml_service
from services.pdf_service import pdf_service
from database.mongo import db
from datetime import datetime
import json
from services.email_service import email_service


# Tool function schemas for Gemini function calling
TOOL_SCHEMAS = []


def register_tool(func):
    """Decorator to register a function as a tool with its schema"""
    # Extract schema from function metadata
    schema = {
        "name": func.__name__,
        "description": func.__doc__ or "",
        "parameters": getattr(func, "_parameters_schema", {
            "type": "object",
            "properties": {},
            "required": []
        })
    }
    TOOL_SCHEMAS.append(schema)
    return func


def tool_schema(parameters: Dict):
    """Decorator to add parameter schema to a function"""
    def decorator(func):
        func._parameters_schema = parameters
        return func
    return decorator


# ==================== TOOL FUNCTIONS ====================

@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "The user ID to fetch accounts for"
        }
    },
    "required": ["user_id"]
})
def fetch_aa_accounts(user_id: str) -> Dict[str, Any]:
    """
    Fetches all bank accounts for a user from the Account Aggregator service.
    Returns a list of accounts with bank details, account IDs, and branch information.
    """
    try:
        accounts = aa_service.get_user_accounts(user_id)
        return {
            "success": True,
            "data": accounts,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "pan": {
            "type": "string",
            "description": "User PAN number"
        },
        "aadhaar": {
            "type": "string",
            "description": "User Aadhaar number"
        }
    },
    "required": ["pan", "aadhaar"]
})
def fetch_accounts_by_pan_aadhaar(pan: str, aadhaar: str) -> Dict[str, Any]:
    """
    Fetches bank accounts for a user based on PAN and Aadhaar numbers.
    Returns a list of accounts associated with the identity documents.
    """
    try:
        accounts = aa_service.get_accounts_by_pan_aadhaar(pan, aadhaar)
        return {
            "success": True,
            "data": accounts,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "The user ID"
        },
        "account_id": {
            "type": "string",
            "description": "The account ID to fetch statements for"
        }
    },
    "required": ["account_id"]
})
def fetch_statements(user_id: str, account_id: str) -> Dict[str, Any]:
    """
    Fetches bank statements (transactions) for a specific account.
    Returns transaction history with dates, amounts, categories, and balances.
    """
    try:
        statement_data = aa_service.get_account_statement(account_id)
        transactions = statement_data.get("transactions", [])
        return {
            "success": True,
            "data": {
                "account_id": account_id,
                "transactions": transactions,
                "transaction_count": len(transactions)
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "The user ID to fetch all statements for"
        }
    },
    "required": ["user_id"]
})
def fetch_all_user_statements(user_id: str) -> Dict[str, Any]:
    """
    Fetches bank statements from ALL user accounts and aggregates them.
    Returns combined transaction history from all banks for comprehensive credit analysis.
    This should be used for credit scoring to get a complete financial picture.
    """
    from services.multi_account_service import fetch_all_user_statements as fetch_all
    return fetch_all(user_id)


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "transactions": {
            "type": "array",
            "description": "List of transaction objects from bank statements",
            "items": {"type": "object"}
        }
    },
    "required": ["transactions"]
})
def extract_features(transactions: List[Dict]) -> Dict[str, Any]:
    """
    Extracts 45 financial features from bank transactions for ML model input.
    Calculates ratios, totals, and categorical features needed for credit scoring.
    """
    try:
        features = feature_service.extract_features(transactions)
        return {
            "success": True,
            "data": features,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "features": {
            "type": "object",
            "description": "Dictionary of extracted financial features"
        }
    },
    "required": ["features"]
})
def predict_score(features: Dict[str, float]) -> Dict[str, Any]:
    """
    Predicts credit score and default probability using the trained ML model.
    Returns credit score (300-900), default probability, and risk label (Low/Medium/High).
    """
    try:
        score_result = ml_service.predict(features)
        return {
            "success": True,
            "data": score_result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }



@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "features": {
            "type": "object",
            "description": "Extracted financial features"
        },
        "score_data": {
            "type": "object",
            "description": "Credit score and risk data"
        }
    },
    "required": ["features", "score_data"]
})
def generate_ai_insight(features: Dict, score_data: Dict) -> Dict[str, Any]:
    """
    Generates AI-driven insights about the user's financial health using Gemini.
    Analyzes spending patterns, ratios, and credit score to provide actionable advice.
    """
    try:
        import google.generativeai as genai
        from core.config import settings
        
        print("[AI Insights] Starting AI insight generation...")
        
        if not settings.GEMINI_API_KEY:
            print("[AI Insights] ERROR: Gemini API key not configured")
            return {
                "success": False,
                "data": None,
                "error": "Gemini API key not configured"
            }
        
        print(f"[AI Insights] Using Gemini model: {settings.GEMINI_MODEL}")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Prepare prompt with key financial metrics
        credit_score = score_data.get('credit_score', 0)
        risk_label = score_data.get('risk_label', 'Unknown')
        debt_income_ratio = features.get('R_DEBT_INCOME', 0)
        savings_income_ratio = features.get('R_SAVINGS_INCOME', 0)
        gambling_income = features.get('R_GAMBLING_INCOME', 0)
        debt = features.get('DEBT', 0)
        savings = features.get('SAVINGS', 0)
        income = features.get('INCOME', 0)
        expenditure_ratio = features.get('R_EXPENDITURE', 0)
        
        prompt = f"""You are a financial analyst for Credify. Analyze this user's financial profile and provide concise, actionable insights.

Financial Profile:
- Credit Score: {credit_score}/900 ({risk_label} Risk)
- Total Debt: ₹{debt:,.2f}
- Total Savings: ₹{savings:,.2f}
- Monthly Income: ₹{income:,.2f}
- Debt-to-Income Ratio: {debt_income_ratio:.4f} (decimal, not percentage)
- Savings-to-Income Ratio: {savings_income_ratio:.4f} (decimal, not percentage)
- Expenditure Ratio: {expenditure_ratio:.4f} (decimal, not percentage)
- Gambling Spending Ratio: {gambling_income:.4f} (decimal, not percentage)

Provide a JSON response with this EXACT structure:
{{
    "summary": "A concise 2-3 sentence analysis covering credit score ({credit_score}/900), key financial ratios, and overall creditworthiness.",
    "key_factors": [
        "3-4 specific factors affecting the credit score",
        "Mix positive and negative factors",
        "Be brief and specific with numbers"
    ],
    "recommendations": [
        "3-4 actionable recommendations",
        "Prioritize by impact",
        "Include specific targets"
    ]
}}

RULES:
1. Use ₹ for currency
2. Keep ratios as decimals (2.5x means 2.5 times income)
3. Be concise but specific
4. No generic advice - tailor to THIS user"""

        print("[AI Insights] Calling Gemini API...")
        response = model.generate_content(prompt)
        print(f"[AI Insights] Received response from Gemini")
        
        # Parse response
        try:
            text = response.text
            print(f"[AI Insights] Raw response preview: {text[:200]}...")
            
            # Clean up markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            insights = json.loads(text.strip())
            print(f"[AI Insights] ✓ Successfully parsed JSON insights")
            print(f"[AI Insights] Summary: {insights.get('summary', '')[:100]}...")
            
            return {
                "success": True,
                "data": insights,
                "error": None
            }
        except Exception as parse_err:
            print(f"[AI Insights] WARNING: JSON parsing failed: {parse_err}")
            print(f"[AI Insights] Falling back to raw text")
            # Fallback if JSON parsing fails
            return {
                "success": True,  # Return success with raw text to avoid pipeline failure
                "data": {
                    "summary": response.text[:500],
                    "key_factors": ["Analysis available in summary"],
                    "recommendations": ["Review full summary for details"]
                },
                "error": None
            }
            
    except Exception as e:
        print(f"[AI Insights] ERROR: {str(e)}")
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "score_data": {
            "type": "object",
            "description": "Complete score data including insights"
        }
    },
    "required": ["score_data"]
})
def generate_underwriting_note(score_data: Dict) -> Dict[str, Any]:
    """
    Generates underwriting notes for loan officers based on credit score and risk assessment.
    Returns actionable recommendations for loan approval decisions.
    """
    try:
        # Generate underwriting notes based on score
        credit_score = score_data.get("credit_score", 0)
        risk_label = score_data.get("risk_label", "Unknown")
        default_prob = score_data.get("default_probability", 0)
        
        notes = []
        
        if credit_score >= 750:
            notes.append("Excellent credit - Approve with standard terms")
        elif credit_score >= 650:
            notes.append("Good credit - Approve with moderate rate")
        elif credit_score >= 550:
            notes.append("Fair credit - Consider approval with higher rate/collateral")
        else:
            notes.append("Poor credit - High risk, secured loan only")
        
        if default_prob > 0.3:
            notes.append("High default risk - Additional security required")
        elif default_prob > 0.15:
            notes.append("Moderate risk - Standard mitigation")
        else:
            notes.append("Low risk - Minimal security needed")
        
        # Add top 2 key factors only
        if "key_factors" in score_data and score_data['key_factors']:
            top_factors = score_data['key_factors'][:2]
            notes.append(f"Key factors: {', '.join(top_factors)}")
        
        return {
            "success": True,
            "data": {
                "underwriting_note": notes,
                "recommendation": "APPROVE" if credit_score >= 650 else "REVIEW" if credit_score >= 550 else "REJECT"
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User ID"
        },
        "account_id": {
            "type": "string",
            "description": "Account ID"
        },
        "score_data": {
            "type": "object",
            "description": "Complete score data with insights and underwriting notes"
        },
        "features": {
            "type": "object",
            "description": "Extracted financial features"
        }
    },
    "required": ["user_id", "account_id", "score_data", "features"]
})
def create_pdf(user_id: str, account_id: str, score_data: Dict, features: Dict) -> Dict[str, Any]:
    """
    Generates a PDF credit report with score, insights, and recommendations.
    Returns the file path to the generated PDF report.
    """
    try:
        # Get user details from database (including loan_amount)
        # Try users collection first (for new users)
        user = db.get_db().users.find_one({"user_id": user_id})
        if not user:
            # Try aa_users collection (for seeded users)
            user = db.get_db().aa_users.find_one({"user_id": user_id})
            
        if not user:
            return {
                "success": False,
                "data": None,
                "error": f"User {user_id} not found"
            }
        
        # Get account details
        user_accounts = aa_service.get_user_accounts(user_id)
        account_info = next((acc for acc in user_accounts if acc["account_id"] == account_id), {})
        
        # Prepare user_data with loan_amount and all accounts
        user_data = {
            "user_id": user_id,
            "name": user.get("full_name") or user.get("name", "User"),  # Check full_name first
            "email": user.get("email", ""),
            "loan_amount": user.get("loan_amount", 0),  # Include loan_amount from DB
            "all_accounts": user_accounts  # Include all user accounts
        }
        
        print(f"[create_pdf] User data: {user_data}")
        print(f"[create_pdf] Total accounts: {len(user_accounts)}")
        
        report_path = pdf_service.generate_report(
            user_data=user_data,
            account_data=account_info,
            score_data=score_data,
            features=features
        )
        
        return {
            "success": True,
            "data": {"report_path": report_path},
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User ID"
        },
        "account_id": {
            "type": "string",
            "description": "Account ID"
        },
        "score_data": {
            "type": "object",
            "description": "Complete score data to save"
        }
    },
    "required": ["user_id", "account_id", "score_data"]
})
def save_score_in_db(user_id: str, account_id: str, score_data: Dict) -> Dict[str, Any]:
    """
    Saves the credit scoring results to the database.
    Stores score, risk label, insights, and report URL for future reference.
    """
    try:
        score_record = {
            **score_data,
            "user_id": user_id,
            "account_id": account_id,
            "created_at": datetime.utcnow()
        }
        
        result = db.get_db().scoring_results.insert_one(score_record)
        
        return {
            "success": True,
            "data": {
                "record_id": str(result.inserted_id),
                "user_id": user_id
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User ID applying for loan"
        },
        "account_id": {
            "type": "string",
            "description": "Bank account ID for the loan"
        },
        "amount": {
            "type": "number",
            "description": "Loan amount requested"
        },
        "purpose": {
            "type": "string",
            "description": "Purpose of the loan"
        }
    },
    "required": ["user_id", "account_id"]
})
def save_application_in_db(user_id: str, account_id: str, amount: float = 0, purpose: str = "") -> Dict[str, Any]:
    """
    Creates and saves a loan application to the database.
    Links the application to the user's latest credit score and bank account.
    """
    try:
        # Get user details first
        # Try users collection first (for new users)
        user = db.get_db().users.find_one({"user_id": user_id})
        if not user:
            # Try aa_users collection (for seeded users)
            user = db.get_db().aa_users.find_one({"user_id": user_id})
            
        if not user:
            return {
                "success": False,
                "data": None,
                "error": f"User {user_id} not found"
            }
        
        # Get account details using aa_service (handles both email and PAN/Aadhaar)
        accounts = []
        if user.get("email"):
            accounts = aa_service.get_user_accounts_by_email(user["email"])
        
        # Fallback to PAN/Aadhaar if no accounts found by email
        if not accounts and user.get("pan") and user.get("aadhaar"):
            accounts = aa_service.get_accounts_by_pan_aadhaar(user["pan"], user["aadhaar"])
        
        account = next((acc for acc in accounts if acc["account_id"] == account_id), None)
        
        if not account:
            return {
                "success": False,
                "data": None,
                "error": "Invalid account ID or no accounts found for user"
            }
        
        # Get latest score
        score_res = db.get_db().scoring_results.find_one(
            {"user_id": user_id}, 
            sort=[("created_at", -1)]
        )
        
        if not score_res:
            return {
                "success": False,
                "data": None,
                "error": "No credit score found for user"
            }
        
        # Create application
        application = {
            "application_id": f"APP{datetime.now().timestamp()}",
            "user_id": user_id,
            "user_name": user.get("full_name") or user.get("name") or "User Name",
            "bank_id": account["bank_id"],
            "branch_id": account["branch_id"],
            "status": "PENDING",
            "score": score_res["credit_score"],
            "risk_label": score_res["risk_label"],
            "report_url": score_res.get("report_path", score_res.get("report_url", "")),
            "amount": amount,
            "purpose": purpose,
            "created_at": datetime.utcnow(),
            "account_id": account_id
        }
        
        db.get_db().applications.insert_one(application)
        
        # Convert datetime to string for JSON response
        application["created_at"] = application["created_at"].isoformat()
        application["_id"] = str(application["_id"])
        
        return {
            "success": True,
            "data": application,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User ID to send email to"
        },
        "subject": {
            "type": "string",
            "description": "Email subject"
        },
        "body": {
            "type": "string",
            "description": "Email body content"
        }
    },
    "required": ["user_id", "subject", "body"]
})
def send_email(user_id: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Sends an email notification to the user.
    Fetches user's email from database.
    In production, this would integrate with an email service (SendGrid, SES, etc.).
    For now, it logs the email.
    """
    try:
        # Get user's email from database
        # Try users collection first
        user = db.get_db().users.find_one({"user_id": user_id})
        if not user:
            # Try aa_users collection
            user = db.get_db().aa_users.find_one({"user_id": user_id})
            
        if not user or not user.get("email"):
            return {
                "success": False,
                "data": None,
                "error": f"User {user_id} not found or has no email"
            }
        
        to_email = user["email"]
        user_name = user.get("name", "User")
        
        html_body = "<br/>".join(body.splitlines()) if body else ""
        success = email_service.send_email(
            to_email,
            subject,
            f"<p>Hi {user_name},</p><p>{html_body}</p><p>Regards,<br/>Credify</p>"
        )
        
        return {
            "success": success,
            "data": {
                "message": "Email sent successfully",
                "to": to_email,
                "user_name": user_name
            },
            "error": None if success else "Email service error"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "application_id": {
            "type": "string",
            "description": "Application ID to fetch"
        }
    },
    "required": ["application_id"]
})
def get_application_by_id(application_id: str) -> Dict[str, Any]:
    """
    Fetches a loan application by its ID.
    Returns application details including user info, score, and status.
    """
    try:
        app = db.get_db().applications.find_one({"application_id": application_id})
        
        if not app:
            return {
                "success": False,
                "data": None,
                "error": "Application not found"
            }
        
        app["_id"] = str(app["_id"])
        
        return {
            "success": True,
            "data": app,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "admin_id": {
            "type": "string",
            "description": "Admin user ID"
        },
        "application_id": {
            "type": "string",
            "description": "Application ID to check access for"
        },
        "admin_bank_id": {
            "type": "string",
            "description": "Admin's bank ID"
        },
        "admin_branch_id": {
            "type": "string",
            "description": "Admin's branch ID"
        }
    },
    "required": ["application_id", "admin_bank_id", "admin_branch_id"]
})
def check_admin_access(admin_id: str, application_id: str, admin_bank_id: str, admin_branch_id: str) -> Dict[str, Any]:
    """
    Validates that an admin has access to a specific application based on branch isolation.
    Returns access status and application details if authorized.
    """
    try:
        app = db.get_db().applications.find_one({"application_id": application_id})
        
        if not app:
            return {
                "success": False,
                "data": None,
                "error": "Application not found"
            }
        
        # Check branch access
        if app["bank_id"] != admin_bank_id or app["branch_id"] != admin_branch_id:
            return {
                "success": False,
                "data": None,
                "error": "Access denied: Application belongs to different branch"
            }
        
        app["_id"] = str(app["_id"])
        
        return {
            "success": True,
            "data": {
                "has_access": True,
                "application": app
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


@register_tool
@tool_schema({
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User ID to fetch score for"
        }
    },
    "required": ["user_id"]
})
def get_latest_score(user_id: str) -> Dict[str, Any]:
    """
    Fetches the most recent credit score for a user.
    Returns score data including insights and recommendations.
    """
    try:
        score_res = db.get_db().scoring_results.find_one(
            {"user_id": user_id},
            sort=[("created_at", -1)]
        )
        
        if not score_res:
            return {
                "success": False,
                "data": None,
                "error": "No score found for user"
            }
        
        score_res["_id"] = str(score_res["_id"])
        
        return {
            "success": True,
            "data": score_res,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


# Export all tools
ALL_TOOLS = {
    "fetch_aa_accounts": fetch_aa_accounts,
    "fetch_accounts_by_pan_aadhaar": fetch_accounts_by_pan_aadhaar,
    "fetch_statements": fetch_statements,
    "fetch_all_user_statements": fetch_all_user_statements,
    "extract_features": extract_features,
    "predict_score": predict_score,
    "generate_ai_insight": generate_ai_insight,
    "generate_underwriting_note": generate_underwriting_note,
    "create_pdf": create_pdf,
    "save_score_in_db": save_score_in_db,
    "save_application_in_db": save_application_in_db,
    "send_email": send_email,
    "get_application_by_id": get_application_by_id,
    "check_admin_access": check_admin_access,
    "get_latest_score": get_latest_score,
}


def get_tool_schemas() -> List[Dict]:
    """Returns all tool schemas for Gemini function calling"""
    return TOOL_SCHEMAS


def execute_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Execute a tool by name with given arguments"""
    if tool_name not in ALL_TOOLS:
        return {
            "success": False,
            "data": None,
            "error": f"Tool '{tool_name}' not found"
        }
    
    try:
        return ALL_TOOLS[tool_name](**kwargs)
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Tool execution error: {str(e)}"
        }
