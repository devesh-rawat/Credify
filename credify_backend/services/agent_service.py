from services.aa_service import aa_service
from services.feature_service import feature_service
from services.ml_service import ml_service
from services.pdf_service import pdf_service
from database.mongo import db
from datetime import datetime

class AgentService:
    def run_pipeline(self, user_id: str, account_id: str):
        # 1. Fetch Data
        print(f"Agent: Fetching AA data for {account_id}...")
        statement_data = aa_service.get_account_statement(account_id)
        transactions = statement_data.get("transactions", [])
        
        # 2. Extract Features
        print("Agent: Extracting features...")
        features = feature_service.extract_features(transactions)
        
        # 3. ML Scoring
        print("Agent: Running ML Model...")
        score_result = ml_service.predict(features)
        
        # 4. LLM Insights (Removed)
        # print("Agent: Generating LLM Insights...")
        # llm_result = llm_service.generate_insights(features, score_result)
        
        # Combine results
        final_result = {**score_result}
        
        # 5. Generate PDF
        print("Agent: Generating PDF Report...")
        # Need user details and account details for PDF
        user_accounts = aa_service.get_user_accounts(user_id)
        account_info = next((acc for acc in user_accounts if acc["account_id"] == account_id), {})
        
        report_path = pdf_service.generate_report(
            user_data={"user_id": user_id},
            account_data=account_info,
            score_data=final_result,
            features=features
        )
        final_result["report_url"] = report_path
        final_result["created_at"] = datetime.utcnow()
        final_result["user_id"] = user_id
        final_result["account_id"] = account_id

        # 6. Save to DB
        print("Agent: Saving results to DB...")
        db.get_db().scoring_results.insert_one(final_result)
        
        return final_result

agent_service = AgentService()
