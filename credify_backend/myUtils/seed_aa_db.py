import json
import os
from database.mongo import db
from core.config import settings

def seed_aa_data():
    print("Connecting to MongoDB...")
    db.connect()
    
    # 1. Seed Users
    users_file = "aa_data/users.json"
    if os.path.exists(users_file):
        print(f"Seeding users from {users_file}...")
        with open(users_file, "r") as f:
            users_data = json.load(f)
            
        # Clear existing collection
        db.get_db().aa_users.delete_many({})
        
        # Insert new data
        # users_data is a dict with user_id as key, we want a list of docs
        user_docs = list(users_data.values())
        if user_docs:
            db.get_db().aa_users.insert_many(user_docs)
            print(f"Inserted {len(user_docs)} users into aa_users collection.")
    else:
        print(f"File not found: {users_file}")

    # 2. Seed Statements
    statements_file = "aa_data/statements.json"
    if os.path.exists(statements_file):
        print(f"Seeding statements from {statements_file}...")
        with open(statements_file, "r") as f:
            statements_data = json.load(f)
            
        # Clear existing collection
        db.get_db().aa_statements.delete_many({})
        
        # Insert new data
        # statements_data is a dict with account_id as key
        # We want to store each statement document, maybe with account_id as a field if it's not already
        statement_docs = []
        for acc_id, data in statements_data.items():
            # Ensure account_id is in the document
            data["account_id"] = acc_id
            statement_docs.append(data)
            
        if statement_docs:
            db.get_db().aa_statements.insert_many(statement_docs)
            print(f"Inserted {len(statement_docs)} statements into aa_statements collection.")
    else:
        print(f"File not found: {statements_file}")

    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_aa_data()
