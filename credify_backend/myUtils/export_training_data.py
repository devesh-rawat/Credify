"""
Export the training data used for the credit score model to CSV format.
This allows you to inspect the data and make modifications as needed.
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import sys
sys.path.append('.')

from services.feature_service import feature_service

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_user(score_range, num_months=12):
    """
    Generate synthetic transaction data for a user in a specific score range.
    
    Score ranges and their characteristics:
    - 850-900: Very high income, minimal debt, high savings, no risky behavior
    - 750-850: High income, low debt, good savings, minimal risk
    - 650-750: Good income, moderate debt, decent savings
    - 550-650: Moderate income, moderate-high debt, some savings
    - 450-550: Lower income, high debt, low savings, some risky behavior
    - 350-450: Low income, very high debt, minimal savings, risky behavior
    - 300-350: Very low income, extreme debt, negative/zero savings, high risk
    """
    min_score, max_score = score_range
    target_score = random.randint(min_score, max_score)
    
    # Define financial profiles based on score
    if target_score >= 850:
        monthly_income = random.randint(200000, 300000)
        debt_payment = random.randint(500, 1500)
        expense_ratio = random.uniform(0.20, 0.30)
        gambling_prob = 0.0
        fines_prob = 0.0
        starting_balance = random.randint(400000, 600000)
    elif target_score >= 750:
        monthly_income = random.randint(150000, 200000)
        debt_payment = random.randint(1500, 2500)
        expense_ratio = random.uniform(0.30, 0.40)
        gambling_prob = 0.0
        fines_prob = random.uniform(0.0, 0.05)
        starting_balance = random.randint(200000, 400000)
    elif target_score >= 650:
        monthly_income = random.randint(100000, 150000)
        debt_payment = random.randint(2500, 4000)
        expense_ratio = random.uniform(0.40, 0.50)
        gambling_prob = random.uniform(0.0, 0.1)
        fines_prob = random.uniform(0.05, 0.15)
        starting_balance = random.randint(100000, 200000)
    elif target_score >= 550:
        monthly_income = random.randint(60000, 100000)
        debt_payment = random.randint(4000, 6000)
        expense_ratio = random.uniform(0.50, 0.60)
        gambling_prob = random.uniform(0.1, 0.25)
        fines_prob = random.uniform(0.15, 0.30)
        starting_balance = random.randint(60000, 100000)
    elif target_score >= 450:
        monthly_income = random.randint(40000, 60000)
        debt_payment = random.randint(6000, 8000)
        expense_ratio = random.uniform(0.60, 0.75)
        gambling_prob = random.uniform(0.25, 0.50)
        fines_prob = random.uniform(0.30, 0.50)
        starting_balance = random.randint(40000, 60000)
    elif target_score >= 350:
        monthly_income = random.randint(25000, 40000)
        debt_payment = random.randint(8000, 12000)
        expense_ratio = random.uniform(0.75, 0.90)
        gambling_prob = random.uniform(0.50, 0.80)
        fines_prob = random.uniform(0.50, 0.80)
        starting_balance = random.randint(30000, 50000)
    else:  # 300-350
        monthly_income = random.randint(20000, 30000)
        debt_payment = random.randint(12000, 18000)
        expense_ratio = random.uniform(0.90, 1.10)
        gambling_prob = random.uniform(0.80, 1.0)
        fines_prob = random.uniform(0.80, 1.0)
        starting_balance = random.randint(20000, 40000)
    
    # Generate transactions
    transactions = []
    current_balance = starting_balance
    start_date = datetime(2024, 5, 1)
    
    for month in range(num_months):
        month_date = start_date + timedelta(days=month * 30)
        
        # Income
        income_variance = random.uniform(0.90, 1.10)
        income = int(monthly_income * income_variance)
        transactions.append({
            'date': (month_date + timedelta(days=1)).isoformat(),
            'amount': income,
            'type': 'CREDIT',
            'category': 'INCOME',
            'sub_category': 'SALARY',
            'merchant': 'Employer',
            'mode': 'NEFT',
            'narration': 'SALARY credit',
            'balance': current_balance + income
        })
        current_balance += income
        
        # Debt payment
        debt_variance = random.uniform(0.90, 1.10)
        debt = int(debt_payment * debt_variance)
        transactions.append({
            'date': (month_date + timedelta(days=5)).isoformat(),
            'amount': debt,
            'type': 'DEBIT',
            'category': 'DEBT',
            'sub_category': 'DEBT',
            'merchant': random.choice(['Loan EMI', 'Credit Card Payment', 'Personal Loan']),
            'mode': 'NEFT',
            'narration': 'DEBT - Loan EMI',
            'balance': current_balance - debt
        })
        current_balance -= debt
        
        # Regular expenses
        total_expenses = int(income * expense_ratio)
        categories = [
            ('GROCERIES', 0.25), ('UTILITIES', 0.10), ('HEALTH', 0.08),
            ('ENTERTAINMENT', 0.12), ('CLOTHING', 0.08), ('TRAVEL', 0.10),
            ('HOUSING', 0.20), ('EDUCATION', 0.05), ('TAX', 0.02)
        ]
        
        for cat, ratio in categories:
            amount = int(total_expenses * ratio * random.uniform(0.8, 1.2))
            day = random.randint(5, 28)
            transactions.append({
                'date': (month_date + timedelta(days=day)).isoformat(),
                'amount': amount,
                'type': 'DEBIT',
                'category': cat,
                'sub_category': cat,
                'merchant': f'{cat} Store',
                'mode': random.choice(['UPI', 'CARD', 'NEFT', 'CASH']),
                'narration': f'{cat} - Purchase',
                'balance': current_balance - amount
            })
            current_balance -= amount
        
        # Gambling
        if random.random() < gambling_prob:
            amount = random.randint(500, 5000)
            transactions.append({
                'date': (month_date + timedelta(days=random.randint(10, 25))).isoformat(),
                'amount': amount,
                'type': 'DEBIT',
                'category': 'GAMBLING',
                'sub_category': 'GAMBLING',
                'merchant': 'Casino',
                'mode': 'CARD',
                'narration': 'GAMBLING - Casino',
                'balance': current_balance - amount
            })
            current_balance -= amount
        
        # Fines
        if random.random() < fines_prob:
            amount = random.randint(200, 1500)
            transactions.append({
                'date': (month_date + timedelta(days=random.randint(10, 25))).isoformat(),
                'amount': amount,
                'type': 'DEBIT',
                'category': 'FINES',
                'sub_category': 'FINES',
                'merchant': 'Late Fee',
                'mode': 'UPI',
                'narration': 'FINES - Late Fee',
                'balance': current_balance - amount
            })
            current_balance -= amount
    
    return transactions, target_score

def export_training_data_to_csv(samples_per_range=150):
    """Generate and export training data to CSV"""
    score_ranges = [
        (850, 900),
        (750, 850),
        (650, 750),
        (550, 650),
        (450, 550),
        (350, 450),
        (300, 350)
    ]
    
    all_data = []
    
    print("Generating training data for export...")
    for score_range in score_ranges:
        print(f"  Generating {samples_per_range} samples for score range {score_range[0]}-{score_range[1]}...")
        for i in range(samples_per_range):
            transactions, target_score = generate_synthetic_user(score_range)
            features = feature_service.extract_features(transactions)
            
            if features:
                # Add target score to features
                features['TARGET_SCORE'] = target_score
                all_data.append(features)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Reorder columns to put TARGET_SCORE first
    cols = ['TARGET_SCORE'] + [col for col in df.columns if col != 'TARGET_SCORE']
    df = df[cols]
    
    # Export to CSV
    output_file = 'training_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Training data exported to: {output_file}")
    print(f"  Total samples: {len(df)}")
    print(f"  Total features: {len(df.columns) - 1}")  # -1 for TARGET_SCORE
    print(f"\nScore distribution:")
    print(df['TARGET_SCORE'].describe())
    
    return df

if __name__ == "__main__":
    export_training_data_to_csv(samples_per_range=150)
