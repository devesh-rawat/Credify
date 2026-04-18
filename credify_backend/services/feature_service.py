import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class FeatureService:
    def extract_features(self, transactions: list) -> dict:
        """
        Extracts features from bank transactions for the ML model.
        """
        if not transactions:
            return {}

        # Convert to DataFrame
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Current date (mocking as the max date in transactions or today)
        if not df.empty:
            current_date = df['date'].max()
        else:
            current_date = datetime.now()
        
        # Time windows
        last_12m = current_date - timedelta(days=365)
        last_6m = current_date - timedelta(days=180)
        
        # Filter data
        df_12m = df[df['date'] >= last_12m]
        df_6m = df[df['date'] >= last_6m]
        
        # Basic aggregates - Calculate from ALL transactions (not just 12 months)
        # This ensures we get the complete financial picture
        all_income_txns = df[df['type'] == 'CREDIT']
        all_expense_txns = df[df['type'] == 'DEBIT']
        
        # For ML features, we use 12-month window
        income_txns = df_12m[df_12m['type'] == 'CREDIT']
        expense_txns = df_12m[df_12m['type'] == 'DEBIT']
        
        total_income = income_txns['amount'].sum()
        total_expenditure = expense_txns['amount'].sum()
        
        # SAVINGS CALCULATION FIX:
        # Calculate savings as net position (total credits - total debits) from ALL transactions
        # This ensures savings updates correctly when any transaction changes
        # Previously used df.iloc[-1]['balance'] which didn't update when historical transactions changed
        total_credits = all_income_txns['amount'].sum()
        total_debits = all_expense_txns['amount'].sum()
        savings = total_credits - total_debits
        
        # Ensure savings is non-negative for ratio calculations (treat overdraft as 0 for features)
        # We'll still track negative savings in the DEFAULT feature
        savings_for_ratios = max(0, savings)
        
        # Debt (Sum of LOAN_REPAYMENT or DEBT * 20 as proxy for total debt, or just 0 if none)
        # In a real scenario, we'd need a liability statement.
        loan_repayments = df_12m[df_12m['category'].isin(['LOAN_REPAYMENT', 'DEBT'])]['amount'].sum()
        debt = loan_repayments * 20 if loan_repayments > 0 else 0
        
        # Categories Mapping
        # Added FINES to the list
        categories = [
            'CLOTHING', 'EDUCATION', 'ENTERTAINMENT', 'GROCERIES', 'HEALTH', 
            'HOUSING', 'TAX', 'TRAVEL', 'UTILITIES', 'GAMBLING', 'FINES'
        ]
        
        def get_category_sum(dataframe, cat_name):
            # Check category or sub_category
            return dataframe[
                (dataframe['category'] == cat_name) | 
                (dataframe['sub_category'] == cat_name)
            ]['amount'].sum()

        # Calculate T_..._12 and T_..._6
        t_12 = {}
        t_6 = {}
        
        for cat in categories:
            t_12[cat] = get_category_sum(df_12m, cat)
            t_6[cat] = get_category_sum(df_6m, cat)
            
        # Calculate Ratios
        features = {}
        
        # Helper for safe division
        def safe_div(a, b):
            return a / b if b != 0 else 0
        
        # 1. Ratios - Use savings_for_ratios to avoid division issues with negative savings
        features['R_DEBT_INCOME'] = safe_div(debt, total_income)
        features['R_DEBT_SAVINGS'] = safe_div(debt, savings_for_ratios)
        features['R_EXPENDITURE_DEBT'] = safe_div(total_expenditure, debt)
        features['R_SAVINGS_INCOME'] = safe_div(savings_for_ratios, total_income)
        features['R_EXPENDITURE'] = safe_div(total_expenditure, total_income)
        features['R_EXPENDITURE_SAVINGS'] = safe_div(total_expenditure, savings_for_ratios)
        
        for cat in categories:
            features[f'R_{cat}_DEBT'] = safe_div(t_12[cat], debt)
            features[f'R_{cat}_SAVINGS'] = safe_div(t_12[cat], savings_for_ratios)
            features[f'R_{cat}_INCOME'] = safe_div(t_12[cat], total_income)
            features[f'R_{cat}'] = safe_div(t_12[cat], total_expenditure)
            
        # 2. Totals
        for cat in categories:
            features[f'T_{cat}_12'] = t_12[cat]
            features[f'T_{cat}_6'] = t_6[cat]
            
        # 3. CAT_ Features (Binary/Categorical)
        features['CAT_CREDIT_CARD'] = 1 if 'CREDIT_CARD' in df_12m['category'].values else 0
        features['CAT_DEBT'] = 1 if debt > 0 else 0
        features['CAT_SAVINGS_ACCOUNT'] = 1 if savings > 0 else 0  # Use actual savings (can be negative)
        features['CAT_DEPENDENTS'] = 0 # Cannot extract from statements
        
        # 4. Others
        # DEFAULT Heuristic: 1 if Savings < 0 (Overdraft) OR (Debt > 0 AND Income == 0)
        if savings < 0 or (debt > 0 and total_income == 0):
            features['DEFAULT'] = 1
        else:
            features['DEFAULT'] = 0
            
        features['DEBT'] = debt
        features['SAVINGS'] = savings  # Store actual savings (can be negative)
        features['INCOME'] = total_income / 12 if total_income > 0 else 0

        
        # Ensure all required features are present and in correct order
        required_features = [
            'R_DEBT_INCOME', 'R_DEBT_SAVINGS', 'DEFAULT', 'DEBT', 'R_EXPENDITURE_DEBT',
            'R_UTILITIES_DEBT', 'R_EDUCATION_INCOME', 'R_GROCERIES_DEBT', 'R_TAX_DEBT',
            'R_ENTERTAINMENT_DEBT', 'R_HEALTH_DEBT', 'R_SAVINGS_INCOME', 'R_CLOTHING_DEBT',
            'R_TRAVEL_DEBT', 'CAT_CREDIT_CARD', 'R_HOUSING_DEBT', 'R_UTILITIES_SAVINGS',
            'R_EDUCATION_SAVINGS', 'CAT_DEBT', 'R_HEALTH_SAVINGS', 'R_GROCERIES_SAVINGS',
            'R_GROCERIES_INCOME', 'R_EXPENDITURE', 'R_ENTERTAINMENT_INCOME', 'R_HEALTH_INCOME',
            'R_GAMBLING_INCOME', 'CAT_DEPENDENTS', 'R_ENTERTAINMENT', 'R_HOUSING_SAVINGS',
            'CAT_SAVINGS_ACCOUNT', 'R_TRAVEL', 'R_GROCERIES', 'R_EDUCATION_DEBT',
            'R_GAMBLING_DEBT', 'T_ENTERTAINMENT_12', 'T_EDUCATION_12', 'T_EDUCATION_6',
            'R_CLOTHING_SAVINGS', 'R_HEALTH', 'T_ENTERTAINMENT_6', 'T_GROCERIES_6',
            'R_GAMBLING_SAVINGS', 'SAVINGS', 'T_GAMBLING_6', 'T_GAMBLING_12',
            'R_ENTERTAINMENT_SAVINGS', 'R_EXPENDITURE_SAVINGS', 'T_GROCERIES_12',
            'R_CLOTHING', 'T_FINES_6', 'INCOME'
        ]
        
        # Fill missing with 0 and order
        final_features = {k: features.get(k, 0) for k in required_features}
        
        return final_features

feature_service = FeatureService()
