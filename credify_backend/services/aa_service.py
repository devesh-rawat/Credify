from database.mongo import db
from typing import List, Dict

class AAService:
    def get_user_accounts(self, user_id: str) -> List[Dict]:
        # Try to find user in users collection first
        user = db.get_db().users.find_one({"user_id": user_id})
        if user and user.get("pan") and user.get("aadhaar"):
            return self.get_accounts_by_pan_aadhaar(user["pan"], user["aadhaar"])
            
        # Fallback to aa_users (for seeded users)
        user_data = db.get_db().aa_users.find_one({"user_id": user_id})
        if user_data:
            return user_data.get("accounts", [])
        return []

    def get_user_accounts_by_email(self, email: str) -> List[Dict]:
        user_data = db.get_db().aa_users.find_one({"email": email})
        if user_data:
            return user_data.get("accounts", [])
        return []

    def get_accounts_by_pan_aadhaar(self, pan: str, aadhaar: str) -> List[Dict]:
        user_data = db.get_db().aa_users.find_one({"pan": pan, "aadhaar": aadhaar})
        if user_data:
            return user_data.get("accounts", [])
        return []

    def get_account_statement(self, account_id: str) -> Dict:
        statement = db.get_db().aa_statements.find_one({"account_id": account_id})
        if statement:
            # Remove _id
            statement.pop("_id", None)
            return statement
        return {}

    def reseed_data(self):
        pass

aa_service = AAService()
