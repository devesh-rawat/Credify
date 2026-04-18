"""
Generate realistic transaction data for 5 users with 9 accounts
ensuring proper credit score distribution.
"""
import json
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
random.seed(42)

def generate_tx_id():
    """Generate unique transaction ID"""
    return f"T-{random.randint(10000, 99999)}"

def generate_transactions(account_config, start_date, num_months=12):
    """
    Generate transactions for an account based on configuration.
    
    account_config should have:
    - monthly_income: list of (amount, day_of_month) tuples
    - monthly_debt: list of (amount, category, day_of_month) tuples
    - monthly_expenses: list of (amount, category, subcategory, merchant, day_range) tuples
    - starting_balance: initial balance
    - gambling_freq: 0-1, probability of gambling transaction per month
    - fines_freq: 0-1, probability of fine per month
    """
    transactions = []
    current_balance = account_config['starting_balance']
    current_date = start_date
    
    for month in range(num_months):
        month_txs = []
        
        # Generate income transactions
        for income_amount, day in account_config.get('monthly_income', []):
            # Add some variance
            amount = int(income_amount * random.uniform(0.95, 1.05))
            tx_date = current_date + timedelta(days=day)
            
            month_txs.append({
                'date': tx_date,
                'amount': amount,
                'type': 'CREDIT',
                'category': 'INCOME',
                'sub_category': 'SALARY',
                'merchant': 'Tech Company Pvt Ltd',
                'mode': 'NEFT',
                'narration': 'SALARY credit'
            })
        
        # Generate debt payments
        for debt_amount, category, day in account_config.get('monthly_debt', []):
            amount = int(debt_amount * random.uniform(0.9, 1.1))
            tx_date = current_date + timedelta(days=day)
            
            merchants = {
                'DEBT': ['Loan EMI', 'Credit Card Payment', 'Personal Loan', 'Car Loan'],
            }
            
            month_txs.append({
                'date': tx_date,
                'amount': amount,
                'type': 'DEBIT',
                'category': category,
                'sub_category': category,
                'merchant': random.choice(merchants.get(category, ['Payment'])),
                'mode': random.choice(['NEFT', 'CARD', 'UPI']),
                'narration': f'{category} - Loan EMI'
            })
        
        # Generate regular expenses
        for expense_amount, category, subcategory, merchant, day_range in account_config.get('monthly_expenses', []):
            amount = int(expense_amount * random.uniform(0.8, 1.2))
            day = random.randint(day_range[0], day_range[1])
            tx_date = current_date + timedelta(days=day)
            
            month_txs.append({
                'date': tx_date,
                'amount': amount,
                'type': 'DEBIT',
                'category': category,
                'sub_category': subcategory,
                'merchant': merchant,
                'mode': random.choice(['UPI', 'CARD', 'NEFT', 'CASH']),
                'narration': f'{category} - {merchant}'
            })
        
        # Gambling transactions (if applicable)
        if random.random() < account_config.get('gambling_freq', 0):
            amount = random.randint(500, 3000)
            day = random.randint(1, 28)
            tx_date = current_date + timedelta(days=day)
            
            month_txs.append({
                'date': tx_date,
                'amount': amount,
                'type': 'DEBIT',
                'category': 'GAMBLING',
                'sub_category': 'GAMBLING',
                'merchant': random.choice(['Casino', 'Betting', 'Lottery']),
                'mode': random.choice(['CARD', 'UPI']),
                'narration': 'GAMBLING - Casino'
            })
        
        # Fines (if applicable)
        if random.random() < account_config.get('fines_freq', 0):
            amount = random.randint(200, 1000)
            day = random.randint(1, 28)
            tx_date = current_date + timedelta(days=day)
            
            month_txs.append({
                'date': tx_date,
                'amount': amount,
                'type': 'DEBIT',
                'category': 'FINES',
                'sub_category': 'FINES',
                'merchant': random.choice(['Late Fee', 'Penalty', 'Traffic Fine']),
                'mode': random.choice(['CARD', 'UPI']),
                'narration': 'FINES - Late Fee'
            })
        
        # Sort by date
        month_txs.sort(key=lambda x: x['date'])
        
        # Add to transactions with running balance
        for tx in month_txs:
            if tx['type'] == 'CREDIT':
                current_balance += tx['amount']
            else:
                current_balance -= tx['amount']
            
            tx['tx_id'] = generate_tx_id()
            tx['date'] = tx['date'].isoformat()
            tx['balance'] = current_balance
            transactions.append(tx)
        
        # Move to next month
        current_date = current_date + timedelta(days=30)
    
    return transactions

# Configuration for each account
# NOTE: Debt is calculated as loan_repayments * 20 in feature extraction!
# Model now trained for 300-900 range

# U003 - Deepika Chauhan (Target: 850+) - PASSING at 861 ✓
# Keep current configuration
acc_axis_04 = {
    'starting_balance': 500000,
    'monthly_income': [(250000, 1)],
    'monthly_debt': [(1000, 'DEBT', 5)],
    'monthly_expenses': [
        (12000, 'GROCERIES', 'GROCERIES', 'Supermarket', (5, 10)),
        (4000, 'UTILITIES', 'UTILITIES', 'Electricity', (10, 15)),
        (3000, 'HEALTH', 'HEALTH', 'Gym', (1, 5)),
        (7000, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Movies', (15, 20)),
        (6000, 'CLOTHING', 'CLOTHING', 'Fashion Store', (10, 20)),
        (5000, 'TRAVEL', 'TRAVEL', 'Fuel', (5, 25)),
        (25000, 'HOUSING', 'HOUSING', 'Rent', (1, 5)),
        (4000, 'EDUCATION', 'EDUCATION', 'Online Course', (10, 15)),
        (3000, 'TAX', 'TAX', 'Income Tax', (25, 28)),
    ],
    'gambling_freq': 0,
    'fines_freq': 0
}

acc_hdfc_05 = {
    'starting_balance': 200000,
    'monthly_income': [(20000, 3)],
    'monthly_debt': [(500, 'DEBT', 10)],
    'monthly_expenses': [
        (3000, 'UTILITIES', 'UTILITIES', 'Internet', (5, 10)),
        (2500, 'HEALTH', 'HEALTH', 'Medical', (15, 20)),
        (2000, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Streaming', (10, 15)),
    ],
    'gambling_freq': 0,
    'fines_freq': 0
}

acc_kotak_06 = {
    'starting_balance': 300000,
    'monthly_income': [(15000, 5)],
    'monthly_debt': [(300, 'DEBT', 15)],
    'monthly_expenses': [
        (2000, 'GROCERIES', 'GROCERIES', 'DMart', (10, 15)),
        (1500, 'HEALTH', 'HEALTH', 'Wellness', (20, 25)),
    ],
    'gambling_freq': 0,
    'fines_freq': 0
}

# U004 - Pranjal Arya (Target: 700-800) - Currently 696, need slight increase
# Reduce debt slightly, increase income
acc_sbi_07 = {
    'starting_balance': 150000,
    'monthly_income': [(130000, 1)],  # Increased from 120k
    'monthly_debt': [(2700, 'DEBT', 5)],  # Reduced from 3k
    'monthly_expenses': [
        (10000, 'GROCERIES', 'GROCERIES', 'BigBasket', (5, 10)),
        (3500, 'UTILITIES', 'UTILITIES', 'Electricity', (10, 15)),
        (2500, 'HEALTH', 'HEALTH', 'Gym', (1, 5)),
        (5000, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Netflix', (15, 20)),
        (4000, 'CLOTHING', 'CLOTHING', 'Apparel Shop', (10, 20)),
        (3500, 'TRAVEL', 'TRAVEL', 'Fuel', (5, 25)),
        (18000, 'HOUSING', 'HOUSING', 'Rent', (1, 5)),
        (2500, 'EDUCATION', 'EDUCATION', 'Books', (10, 15)),
        (2000, 'TAX', 'TAX', 'Income Tax', (20, 25)),
    ],
    'gambling_freq': 0,
    'fines_freq': 0
}

# U002 - Jyoti Negi (Target: 500-600) - Currently 603, almost there!
# Tiny increase in debt
acc_icici_03 = {
    'starting_balance': 80000,
    'monthly_income': [(68000, 1)],
    'monthly_debt': [(5800, 'DEBT', 5)],  # Increased tiny bit more
    'monthly_expenses': [
        (7000, 'GROCERIES', 'GROCERIES', 'Supermarket', (5, 10)),
        (3000, 'UTILITIES', 'UTILITIES', 'Electricity', (10, 15)),
        (1800, 'HEALTH', 'HEALTH', 'Doctor', (15, 20)),
        (3500, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Movies', (15, 20)),
        (3000, 'CLOTHING', 'CLOTHING', 'Store', (10, 20)),
        (3000, 'TRAVEL', 'TRAVEL', 'Fuel', (5, 25)),
        (12000, 'HOUSING', 'HOUSING', 'Rent', (1, 5)),
        (1500, 'EDUCATION', 'EDUCATION', 'Books', (10, 15)),
    ],
    'gambling_freq': 0.35,  # Increased from 0.3
    'fines_freq': 0.55  # Increased from 0.5
}

# U005 - Swati Rawat (Target: 400-450) - Currently 473, need slight decrease
# Reduce debt slightly
acc_icici_08 = {
    'starting_balance': 60000,
    'monthly_income': [(37000, 1)],  # Increased slightly
    'monthly_debt': [(8500, 'DEBT', 5)],  # Reduced slightly
    'monthly_expenses': [
        (5000, 'GROCERIES', 'GROCERIES', 'Local Store', (5, 10)),
        (2500, 'UTILITIES', 'UTILITIES', 'Electricity', (10, 15)),
        (1200, 'HEALTH', 'HEALTH', 'Pharmacy', (15, 20)),
        (2500, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Movies', (15, 20)),
        (1800, 'CLOTHING', 'CLOTHING', 'Store', (10, 20)),
        (2500, 'TRAVEL', 'TRAVEL', 'Bus', (5, 25)),
        (8000, 'HOUSING', 'HOUSING', 'Rent', (1, 5)),
    ],
    'gambling_freq': 0.8,  # Increased from 0.6
    'fines_freq': 0.9  # Increased from 0.7
}

acc_yes_09 = {
    'starting_balance': 60000,
    'monthly_income': [(10000, 3)],  # Reduced from 12k
    'monthly_debt': [(2000, 'DEBT', 10)],  # Increased from 1.5k
    'monthly_expenses': [
        (2000, 'GROCERIES', 'GROCERIES', 'Store', (10, 15)),
        (1200, 'UTILITIES', 'UTILITIES', 'Mobile', (5, 10)),
        (2500, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Gaming', (15, 20)),
    ],
    'gambling_freq': 0.9,  # Increased from 0.8
    'fines_freq': 0.8  # Increased from 0.6
}

# U001 - Devesh Rawat (Target: 300-350) - Currently 398, very close!
# Keep high debt, increase income enough to prevent negative balance
acc_hdfc_01 = {
    'starting_balance': 80000,  # Increased more
    'monthly_income': [(32000, 1)],  # Increased more to prevent negative
    'monthly_debt': [(14000, 'DEBT', 5)],  # Keep high
    'monthly_expenses': [
        (4000, 'GROCERIES', 'GROCERIES', 'Store', (5, 10)),
        (1800, 'UTILITIES', 'UTILITIES', 'Electricity', (10, 15)),
        (1000, 'HEALTH', 'HEALTH', 'Pharmacy', (15, 20)),
        (2000, 'ENTERTAINMENT', 'ENTERTAINMENT', 'Movies', (15, 20)),
        (1200, 'CLOTHING', 'CLOTHING', 'Store', (10, 20)),
        (1500, 'TRAVEL', 'TRAVEL', 'Auto', (5, 25)),
        (7000, 'HOUSING', 'HOUSING', 'Rent', (1, 5)),
    ],
    'gambling_freq': 1.0,
    'fines_freq': 1.0
}

acc_sbi_02 = {
    'starting_balance': 60000,
    'monthly_income': [(12000, 5)],  # Increased to prevent negative
    'monthly_debt': [(1800, 'DEBT', 15)],  # Increased
    'monthly_expenses': [
        (1500, 'GROCERIES', 'GROCERIES', 'Store', (10, 15)),
        (800, 'UTILITIES', 'UTILITIES', 'Mobile', (5, 10)),
    ],
    'gambling_freq': 1.0,
    'fines_freq': 1.0
}

# Generate transactions for all accounts
start_date = datetime(2024, 5, 1)

statements = {
    'ACC-AXIS-04': {
        'account_id': 'ACC-AXIS-04',
        'bank_id': 'B729',
        'branch_id': 'AXIS_BRANCH',
        'transactions': generate_transactions(acc_axis_04, start_date)
    },
    'ACC-HDFC-05': {
        'account_id': 'ACC-HDFC-05',
        'bank_id': 'B220',
        'branch_id': 'HDFC_BRANCH',
        'transactions': generate_transactions(acc_hdfc_05, start_date)
    },
    'ACC-KOTAK-06': {
        'account_id': 'ACC-KOTAK-06',
        'bank_id': 'B113',
        'branch_id': 'KOTA_BRANCH',
        'transactions': generate_transactions(acc_kotak_06, start_date)
    },
    'ACC-SBI-07': {
        'account_id': 'ACC-SBI-07',
        'bank_id': 'B480',
        'branch_id': 'SBI_BRANCH',
        'transactions': generate_transactions(acc_sbi_07, start_date)
    },
    'ACC-ICICI-03': {
        'account_id': 'ACC-ICICI-03',
        'bank_id': 'B372',
        'branch_id': 'ICIC_BRANCH',
        'transactions': generate_transactions(acc_icici_03, start_date)
    },
    'ACC-ICICI-08': {
        'account_id': 'ACC-ICICI-08',
        'bank_id': 'B372',
        'branch_id': 'ICIC_BRANCH',
        'transactions': generate_transactions(acc_icici_08, start_date)
    },
    'ACC-YES-09': {
        'account_id': 'ACC-YES-09',
        'bank_id': 'B136',
        'branch_id': 'YES_BRANCH',
        'transactions': generate_transactions(acc_yes_09, start_date)
    },
    'ACC-HDFC-01': {
        'account_id': 'ACC-HDFC-01',
        'bank_id': 'B220',
        'branch_id': 'HDFC_BRANCH',
        'transactions': generate_transactions(acc_hdfc_01, start_date)
    },
    'ACC-SBI-02': {
        'account_id': 'ACC-SBI-02',
        'bank_id': 'B480',
        'branch_id': 'SBI_BRANCH',
        'transactions': generate_transactions(acc_sbi_02, start_date)
    }
}

# Save to file
output_file = 'aa_data/statements.json'
with open(output_file, 'w') as f:
    json.dump(statements, f, indent=2)

print(f"Generated statements saved to {output_file}")

# Print summary
print("\n=== Summary ===")
for acc_id, data in statements.items():
    txs = data['transactions']
    total_credit = sum(tx['amount'] for tx in txs if tx['type'] == 'CREDIT')
    total_debit = sum(tx['amount'] for tx in txs if tx['type'] == 'DEBIT')
    min_balance = min(tx['balance'] for tx in txs)
    final_balance = txs[-1]['balance'] if txs else 0
    
    print(f"\n{acc_id}:")
    print(f"  Transactions: {len(txs)}")
    print(f"  Total Credits: ₹{total_credit:,}")
    print(f"  Total Debits: ₹{total_debit:,}")
    print(f"  Net: ₹{total_credit - total_debit:,}")
    print(f"  Min Balance: ₹{min_balance:,}")
    print(f"  Final Balance: ₹{final_balance:,}")
    print(f"  Negative Balance: {'YES ❌' if min_balance < 0 else 'NO ✓'}")
