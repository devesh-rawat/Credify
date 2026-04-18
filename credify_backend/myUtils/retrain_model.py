"""
Retrain the credit score model with synthetic data to achieve 300-900 score range.

This script:
1. Generates synthetic transaction data for different score ranges
2. Extracts features using the existing feature service
3. Trains a RandomForest model with proper scaling
4. Saves the model and scaler
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
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
        debt_payment = random.randint(500, 1500)  # Very low (will be *20)
        expense_ratio = random.uniform(0.20, 0.30)  # 20-30% of income
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
        expense_ratio = random.uniform(0.90, 1.10)  # May exceed income
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

def generate_training_data(samples_per_range=100):
    """Generate training data across all score ranges"""
    score_ranges = [
        (850, 900),
        (750, 850),
        (650, 750),
        (550, 650),
        (450, 550),
        (350, 450),
        (300, 350)
    ]
    
    X_data = []
    y_data = []
    
    print("Generating synthetic training data...")
    for score_range in score_ranges:
        print(f"  Generating {samples_per_range} samples for score range {score_range[0]}-{score_range[1]}...")
        for i in range(samples_per_range):
            transactions, target_score = generate_synthetic_user(score_range)
            features = feature_service.extract_features(transactions)
            
            if features:  # Only add if features were extracted
                X_data.append(features)
                y_data.append(target_score)
    
    print(f"Generated {len(X_data)} training samples")
    return X_data, y_data

def train_model():
    """Train the credit score model"""
    print("="*80)
    print("CREDIT SCORE MODEL RETRAINING")
    print("="*80)
    
    # Generate training data
    X_data, y_data = generate_training_data(samples_per_range=150)
    
    # Define the exact features used by ml_service.py
    TOP_FEATURES = [
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
        'R_GAMBLING_SAVINGS', 'SAVINGS', 'T_GAMBLING_6', 'T_GAMBLING_12'
    ]
    
    # Convert to DataFrame with only the features used by ml_service
    X_df = pd.DataFrame(X_data)
    # Select only the TOP_FEATURES
    X_df = X_df[[f for f in TOP_FEATURES if f in X_df.columns]]
    
    # Fill any missing features with 0
    for feature in TOP_FEATURES:
        if feature not in X_df.columns:
            X_df[feature] = 0
    
    # Reorder to match TOP_FEATURES
    X_df = X_df[TOP_FEATURES]
    
    y = np.array(y_data)
    
    print(f"\nDataset shape: {X_df.shape}")
    print(f"Features: {len(TOP_FEATURES)}")
    print(f"Score distribution:")
    print(f"  Min: {y.min()}")
    print(f"  Max: {y.max()}")
    print(f"  Mean: {y.mean():.2f}")
    print(f"  Std: {y.std():.2f}")
    
    # Add engineered features (same as in ml_service.py)
    X_df['DEBT_SAVINGS_INTERACTION'] = X_df['DEBT'] * X_df['SAVINGS']
    X_df['DEBT_INCOME_SQUARED'] = X_df['R_DEBT_INCOME'] ** 2
    X_df['SAVINGS_INCOME_SQUARED'] = X_df['R_SAVINGS_INCOME'] ** 2
    X_df['HIGH_RISK_SPENDING'] = (X_df['R_GAMBLING_INCOME'] + X_df['R_ENTERTAINMENT_INCOME']) / 2
    X_df['FINANCIAL_STABILITY'] = X_df['R_SAVINGS_INCOME'] - X_df['R_DEBT_INCOME']
    
    print(f"Final feature count (with engineered): {X_df.shape[1]}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_df, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\nTraining RandomForest model...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Clip predictions to valid range
    y_train_pred = np.clip(y_train_pred, 300, 900)
    y_test_pred = np.clip(y_test_pred, 300, 900)
    
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"\nTraining Performance:")
    print(f"  MAE: {train_mae:.2f}")
    print(f"  R²: {train_r2:.4f}")
    
    print(f"\nTest Performance:")
    print(f"  MAE: {test_mae:.2f}")
    print(f"  R²: {test_r2:.4f}")
    
    print(f"\nTest Predictions Distribution:")
    print(f"  Min: {y_test_pred.min():.2f}")
    print(f"  Max: {y_test_pred.max():.2f}")
    print(f"  Mean: {y_test_pred.mean():.2f}")
    print(f"  Std: {y_test_pred.std():.2f}")
    
    # Save model and scaler
    print("\nSaving model and scaler...")
    joblib.dump(model, 'ml_models/credit_score_model.pkl')
    joblib.dump(scaler, 'ml_models/scaler.pkl')
    
    # Save metadata
    metadata = {
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'train_mae': float(train_mae),
        'test_mae': float(test_mae),
        'train_r2': float(train_r2),
        'test_r2': float(test_r2),
        'feature_count': X_df.shape[1],
        'base_features': len(TOP_FEATURES),
        'trained_at': datetime.now().isoformat()
    }
    joblib.dump(metadata, 'ml_models/model_metadata.pkl')
    
    print("\n" + "="*80)
    print("✓ Model training complete!")
    print("="*80)
    print(f"\nModel saved to: ml_models/credit_score_model.pkl")
    print(f"Scaler saved to: ml_models/scaler.pkl")
    print(f"Metadata saved to: ml_models/model_metadata.pkl")
    print(f"\nFeature count: {len(TOP_FEATURES)} base + 5 engineered = {X_df.shape[1]} total")
    
    return model, scaler, metadata

if __name__ == "__main__":
    train_model()
