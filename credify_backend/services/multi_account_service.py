"""
Multi-Account Statement Aggregator
Fetches and combines statements from all user bank accounts
"""

from typing import List, Dict, Any
from services.aa_service import aa_service


def fetch_all_user_statements(user_id: str) -> Dict[str, Any]:
    """
    Fetch bank statements from ALL user accounts and aggregate them.
    
    This function fetches transactions based on the user's PAN and Aadhaar,
    not the user_id. This allows any user with matching PAN/Aadhaar to access
    the transaction data (simulating real Account Aggregator behavior).
    
    Args:
        user_id: User ID to fetch statements for
        
    Returns:
        Dictionary with aggregated transactions and account metadata
    """
    try:
        from database.mongo import db
        
        # First, get user details to find their PAN/Aadhaar
        user = db.get_db().users.find_one({"user_id": user_id})
        if not user:
            # Try aa_users collection as fallback
            user = db.get_db().aa_users.find_one({"user_id": user_id})
        
        if not user:
            return {
                "success": False,
                "data": None,
                "error": f"User {user_id} not found in database"
            }
        
        # Get user's PAN and Aadhaar
        pan = user.get("pan")
        aadhaar = user.get("aadhaar")
        
        if not pan or not aadhaar:
            return {
                "success": False,
                "data": None,
                "error": f"User {user_id} does not have PAN and Aadhaar configured. Please complete OTP verification first."
            }
        
        # Find accounts by PAN and Aadhaar (from aa_users collection)
        # This allows any user with matching PAN/Aadhaar to access the data
        aa_user = db.get_db().aa_users.find_one({"pan": pan, "aadhaar": aadhaar})
        
        if not aa_user:
            error_msg = f"No account aggregator data found for PAN: {pan}, Aadhaar: {aadhaar}."
            error_msg += " This user's credentials don't match any seeded AA data."
            error_msg += " For demo/testing, use seeded users (U001-U005) or ensure PAN/Aadhaar match seeded data."
            
            return {
                "success": False,
                "data": None,
                "error": error_msg
            }
        
        # Get accounts from aa_user
        accounts = aa_user.get("accounts", [])
        
        if not accounts:
            return {
                "success": False,
                "data": None,
                "error": f"No bank accounts found for PAN: {pan}, Aadhaar: {aadhaar}"
            }
        
        all_transactions = []
        account_summaries = []
        total_accounts = len(accounts)
        
        # Fetch statements from each account
        for account in accounts:
            account_id = account.get("account_id")
            bank_name = account.get("bank_name", "Unknown")
            
            # Fetch statement for this account from aa_statements
            statement = aa_service.get_account_statement(account_id)
            transactions = statement.get("transactions", [])
            
            # Add account metadata to each transaction
            for txn in transactions:
                txn["account_id"] = account_id
                txn["bank_name"] = bank_name
                txn["bank_id"] = account.get("bank_id")
                txn["branch_id"] = account.get("branch_id")
            
            all_transactions.extend(transactions)
            
            # Track account summary
            account_summaries.append({
                "account_id": account_id,
                "bank_name": bank_name,
                "bank_id": account.get("bank_id"),
                "branch_id": account.get("branch_id"),
                "transaction_count": len(transactions)
            })
        
        # Sort all transactions by date (most recent first)
        all_transactions.sort(
            key=lambda x: x.get("date", ""), 
            reverse=True
        )
        
        # Check if we actually got any transactions
        if not all_transactions:
            return {
                "success": False,
                "data": None,
                "error": f"No transaction data found for PAN: {pan}, Aadhaar: {aadhaar}. Found {total_accounts} bank account(s) but no transaction history. The accounts may not have any transactions in the aa_statements collection."
            }
        
        return {
            "success": True,
            "data": {
                "transactions": all_transactions,
                "total_transactions": len(all_transactions),
                "total_accounts": total_accounts,
                "account_summaries": account_summaries,
                "pan": pan,
                "aadhaar": aadhaar,
                "aa_user_id": aa_user.get("user_id")  # Original AA user_id for reference
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Error fetching statements: {str(e)}"
        }


def aggregate_account_features(user_id: str) -> Dict[str, Any]:
    """
    Fetch statements from all accounts and extract aggregated features.
    
    This is a convenience function that combines fetching and feature extraction
    for multi-account analysis.
    
    Args:
        user_id: User ID
        
    Returns:
        Aggregated features from all accounts
    """
    from services.feature_service import feature_service
    
    try:
        # Fetch all statements
        result = fetch_all_user_statements(user_id)
        
        if not result["success"]:
            return result
        
        transactions = result["data"]["transactions"]
        
        # Extract features from combined transactions
        features = feature_service.extract_features(transactions)
        
        return {
            "success": True,
            "data": {
                "features": features,
                "account_summaries": result["data"]["account_summaries"],
                "total_transactions": result["data"]["total_transactions"],
                "total_accounts": result["data"]["total_accounts"]
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Error aggregating features: {str(e)}"
        }
