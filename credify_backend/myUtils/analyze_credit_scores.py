#!/usr/bin/env python3
"""
Credit Score Distribution Analyzer
Analyzes current transaction patterns and suggests adjustments to create
diverse credit scores ranging from 300 to 900 across 5 users
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

def load_json(filepath: str) -> dict:
    """Load JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def calculate_credit_indicators(transactions: List[dict]) -> Dict:
    """Calculate key credit score indicators from transactions"""
    
    if not transactions:
        return {}
    
    # Sort by date
    sorted_txs = sorted(transactions, key=lambda x: x['date'])
    
    # Calculate various metrics
    total_credits = sum(tx['amount'] for tx in transactions if tx['type'] == 'CREDIT')
    total_debits = sum(tx['amount'] for tx in transactions if tx['type'] == 'DEBIT')
    
    # Income analysis
    income_txs = [tx for tx in transactions if tx['category'] == 'INCOME']
    monthly_income = total_credits / 12 if total_credits > 0 else 0
    
    # Debt analysis
    debt_txs = [tx for tx in transactions if tx['category'] == 'DEBT']
    total_debt_payments = sum(tx['amount'] for tx in debt_txs)
    
    # Spending categories
    categories = {}
    for tx in transactions:
        if tx['type'] == 'DEBIT':
            cat = tx['category']
            categories[cat] = categories.get(cat, 0) + tx['amount']
    
    # Calculate ratios
    debt_to_income = (total_debt_payments / total_credits * 100) if total_credits > 0 else 0
    savings_amount = sum(tx['amount'] for tx in transactions if tx.get('sub_category') == 'FD_DEPOSIT')
    savings_rate = (savings_amount / total_credits * 100) if total_credits > 0 else 0
    
    # Balance trend
    opening_balance = sorted_txs[0]['balance'] - (
        sorted_txs[0]['amount'] if sorted_txs[0]['type'] == 'CREDIT' 
        else -sorted_txs[0]['amount']
    )
    closing_balance = sorted_txs[-1]['balance']
    balance_growth = closing_balance - opening_balance
    
    # Payment consistency (check for regular income)
    income_dates = [tx['date'][:7] for tx in income_txs]  # YYYY-MM
    unique_months = len(set(income_dates))
    payment_consistency = (unique_months / 12 * 100)
    
    return {
        'total_income': total_credits,
        'total_expenses': total_debits,
        'monthly_income': monthly_income,
        'total_debt_payments': total_debt_payments,
        'debt_to_income_ratio': debt_to_income,
        'savings_amount': savings_amount,
        'savings_rate': savings_rate,
        'opening_balance': opening_balance,
        'closing_balance': closing_balance,
        'balance_growth': balance_growth,
        'payment_consistency': payment_consistency,
        'spending_categories': categories,
        'transaction_count': len(transactions),
        'has_negative_balance': any(tx['balance'] < 0 for tx in transactions)
    }

def estimate_credit_score(indicators: Dict) -> Tuple[int, str]:
    """Estimate credit score based on indicators (simplified model)"""
    
    score = 500  # Base score
    
    # Payment consistency (35% weight)
    score += int(indicators['payment_consistency'] * 1.4)
    
    # Debt to income ratio (30% weight) - lower is better
    if indicators['debt_to_income_ratio'] < 20:
        score += 150
    elif indicators['debt_to_income_ratio'] < 40:
        score += 100
    elif indicators['debt_to_income_ratio'] < 60:
        score += 50
    else:
        score -= 50
    
    # Savings rate (15% weight)
    score += int(indicators['savings_rate'] * 0.75)
    
    # Balance growth (10% weight)
    if indicators['balance_growth'] > 100000:
        score += 50
    elif indicators['balance_growth'] > 0:
        score += 25
    else:
        score -= 25
    
    # Monthly income (10% weight)
    if indicators['monthly_income'] > 80000:
        score += 50
    elif indicators['monthly_income'] > 50000:
        score += 30
    elif indicators['monthly_income'] > 30000:
        score += 15
    
    # Penalties
    if indicators['has_negative_balance']:
        score -= 200
    
    # Clamp to valid range
    score = max(300, min(900, score))
    
    # Categorize
    if score >= 750:
        category = "Excellent"
    elif score >= 650:
        category = "Good"
    elif score >= 550:
        category = "Fair"
    elif score >= 450:
        category = "Poor"
    else:
        category = "Very Poor"
    
    return score, category

def analyze_all_users():
    """Analyze all users and their credit indicators"""
    
    users = load_json('aa_data/users.json')
    statements = load_json('aa_data/statements.json')
    
    print("=" * 80)
    print("CREDIT SCORE DISTRIBUTION ANALYSIS")
    print("=" * 80)
    print()
    
    user_scores = []
    
    for user_id, user_data in sorted(users.items()):
        print(f"👤 {user_id}: {user_data['full_name']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Accounts: {len(user_data['accounts'])}")
        print()
        
        # Combine all transactions for this user
        all_transactions = []
        for account in user_data['accounts']:
            acc_id = account['account_id']
            if acc_id in statements:
                all_transactions.extend(statements[acc_id].get('transactions', []))
        
        # Calculate indicators
        indicators = calculate_credit_indicators(all_transactions)
        
        # Estimate credit score
        score, category = estimate_credit_score(indicators)
        
        user_scores.append({
            'user_id': user_id,
            'name': user_data['full_name'],
            'score': score,
            'category': category,
            'indicators': indicators
        })
        
        print(f"   📊 Credit Indicators:")
        print(f"      Monthly Income: ₹{indicators['monthly_income']:,.2f}")
        print(f"      Debt-to-Income: {indicators['debt_to_income_ratio']:.1f}%")
        print(f"      Savings Rate: {indicators['savings_rate']:.1f}%")
        print(f"      Balance Growth: ₹{indicators['balance_growth']:,.2f}")
        print(f"      Payment Consistency: {indicators['payment_consistency']:.1f}%")
        print(f"      Negative Balance: {'Yes ❌' if indicators['has_negative_balance'] else 'No ✅'}")
        print()
        print(f"   🎯 Estimated Credit Score: {score} ({category})")
        print()
        print("-" * 80)
        print()
    
    # Summary
    print("=" * 80)
    print("CREDIT SCORE DISTRIBUTION SUMMARY")
    print("=" * 80)
    print()
    
    user_scores.sort(key=lambda x: x['score'], reverse=True)
    
    for i, user in enumerate(user_scores, 1):
        print(f"{i}. {user['name']:20s} - Score: {user['score']:3d} ({user['category']})")
    
    print()
    print(f"Score Range: {user_scores[-1]['score']} - {user_scores[0]['score']}")
    print(f"Score Spread: {user_scores[0]['score'] - user_scores[-1]['score']} points")
    print()
    
    # Check distribution
    score_ranges = {
        'Excellent (750-900)': sum(1 for u in user_scores if u['score'] >= 750),
        'Good (650-749)': sum(1 for u in user_scores if 650 <= u['score'] < 750),
        'Fair (550-649)': sum(1 for u in user_scores if 550 <= u['score'] < 650),
        'Poor (450-549)': sum(1 for u in user_scores if 450 <= u['score'] < 550),
        'Very Poor (300-449)': sum(1 for u in user_scores if u['score'] < 450)
    }
    
    print("Distribution by Category:")
    for category, count in score_ranges.items():
        print(f"  {category}: {count} user(s)")
    
    print()
    print("=" * 80)
    
    # Recommendations
    print()
    print("📋 RECOMMENDATIONS FOR BETTER DISTRIBUTION")
    print("=" * 80)
    print()
    
    target_scores = [850, 700, 550, 400, 320]  # Excellent, Good, Fair, Poor, Very Poor
    
    for i, (user, target) in enumerate(zip(user_scores, target_scores)):
        current = user['score']
        diff = target - current
        
        print(f"{i+1}. {user['name']} (Current: {current}, Target: {target})")
        
        if abs(diff) < 50:
            print(f"   ✅ Already close to target range")
        elif diff > 0:
            print(f"   📈 Need to IMPROVE by {diff} points:")
            if user['indicators']['debt_to_income_ratio'] > 30:
                print(f"      - Reduce debt payments (currently {user['indicators']['debt_to_income_ratio']:.1f}%)")
            if user['indicators']['savings_rate'] < 5:
                print(f"      - Increase savings/FD deposits (currently {user['indicators']['savings_rate']:.1f}%)")
            if user['indicators']['balance_growth'] < 0:
                print(f"      - Improve balance growth (currently ₹{user['indicators']['balance_growth']:,.2f})")
        else:
            print(f"   📉 Need to DECREASE by {abs(diff)} points:")
            print(f"      - Increase debt payments or reduce income")
            print(f"      - Reduce savings rate")
            print(f"      - Add more spending categories")
        print()
    
    print("=" * 80)
    
    return user_scores

if __name__ == "__main__":
    import os
    os.chdir(Path(__file__).parent)
    analyze_all_users()
