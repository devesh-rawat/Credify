"""
Verify credit scores for all users using the ML model
"""
import json
import sys
sys.path.append('.')

from services.feature_service import feature_service
from services.ml_service import ml_service

# Load statements
with open('aa_data/statements.json', 'r') as f:
    statements = json.load(f)

# User to accounts mapping
user_accounts = {
    'U001': ['ACC-HDFC-01', 'ACC-SBI-02'],
    'U002': ['ACC-ICICI-03'],
    'U003': ['ACC-AXIS-04', 'ACC-HDFC-05', 'ACC-KOTAK-06'],
    'U004': ['ACC-SBI-07'],
    'U005': ['ACC-ICICI-08', 'ACC-YES-09']
}

# Expected scores
expected_scores = {
    'U003': (850, 900, 'Deepika Chauhan'),
    'U004': (700, 800, 'Pranjal Arya'),
    'U002': (500, 600, 'Jyoti Negi'),
    'U005': (400, 450, 'Swati Rawat'),
    'U001': (300, 350, 'Devesh Rawat')
}

print("=" * 80)
print("CREDIT SCORE VERIFICATION")
print("=" * 80)

results = []

for user_id, account_ids in user_accounts.items():
    print(f"\n{'='*80}")
    print(f"User: {user_id} ({expected_scores[user_id][2]})")
    print(f"Accounts: {', '.join(account_ids)}")
    print(f"Expected Score Range: {expected_scores[user_id][0]}-{expected_scores[user_id][1]}")
    print(f"{'='*80}")
    
    # Aggregate all transactions from user's accounts
    all_transactions = []
    for acc_id in account_ids:
        if acc_id in statements:
            all_transactions.extend(statements[acc_id]['transactions'])
    
    print(f"Total Transactions: {len(all_transactions)}")
    
    # Calculate totals
    total_credits = sum(tx['amount'] for tx in all_transactions if tx['type'] == 'CREDIT')
    total_debits = sum(tx['amount'] for tx in all_transactions if tx['type'] == 'DEBIT')
    
    print(f"Total Credits: ₹{total_credits:,}")
    print(f"Total Debits: ₹{total_debits:,}")
    print(f"Net Balance: ₹{total_credits - total_debits:,}")
    
    # Extract features
    features = feature_service.extract_features(all_transactions)
    
    # Key features
    print(f"\nKey Financial Metrics:")
    print(f"  Income (monthly): ₹{features.get('INCOME', 0):,.0f}")
    print(f"  Debt: ₹{features.get('DEBT', 0):,.0f}")
    print(f"  Savings: ₹{features.get('SAVINGS', 0):,.0f}")
    print(f"  Debt-to-Income Ratio: {features.get('R_DEBT_INCOME', 0):.2f}")
    print(f"  Savings-to-Income Ratio: {features.get('R_SAVINGS_INCOME', 0):.2f}")
    print(f"  DEFAULT Flag: {features.get('DEFAULT', 0)}")
    
    # Check for gambling and fines
    gambling_total = features.get('T_GAMBLING_12', 0)
    fines_total = features.get('T_FINES_12', 0)
    print(f"  Gambling (12m): ₹{gambling_total:,.0f}")
    print(f"  Fines (12m): ₹{fines_total:,.0f}")
    
    # Predict score
    score_result = ml_service.predict(features)
    
    predicted_score = score_result['credit_score']
    min_expected, max_expected, name = expected_scores[user_id]
    
    in_range = min_expected <= predicted_score <= max_expected
    status = "✓ PASS" if in_range else "❌ FAIL"
    
    print(f"\n{'='*80}")
    print(f"PREDICTED CREDIT SCORE: {predicted_score}")
    print(f"Risk Label: {score_result['risk_label']}")
    print(f"Default Probability: {score_result['default_probability']:.2%}")
    print(f"Status: {status}")
    print(f"{'='*80}")
    
    results.append({
        'user_id': user_id,
        'name': name,
        'predicted_score': predicted_score,
        'expected_range': (min_expected, max_expected),
        'in_range': in_range
    })

# Summary
print(f"\n\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"{'User':<10} {'Name':<20} {'Predicted':<12} {'Expected':<15} {'Status':<10}")
print(f"{'-'*80}")

all_pass = True
for r in results:
    status = "✓ PASS" if r['in_range'] else "❌ FAIL"
    if not r['in_range']:
        all_pass = False
    print(f"{r['user_id']:<10} {r['name']:<20} {r['predicted_score']:<12} "
          f"{r['expected_range'][0]}-{r['expected_range'][1]:<10} {status:<10}")

print(f"{'='*80}")
if all_pass:
    print("✓ ALL USERS PASSED - Credit scores are in expected ranges!")
else:
    print("❌ SOME USERS FAILED - Adjustments needed")
print(f"{'='*80}")
