# Account Aggregator Data

This directory contains validated user and transaction data for the Credify backend system.

## Files

- **users.json**: User account information including personal details and linked bank accounts
- **statements.json**: Complete transaction history for all user accounts

## Data Status

✅ **100% Validated and Accurate**

All data has been validated for consistency between users.json and statements.json.

## Quick Stats

- **Users**: 5
- **Bank Accounts**: 9
- **Total Transactions**: 1,970
- **Date Range**: Nov 2024 - Nov 2025

## Validation

To validate data consistency, run:

```bash
python3 ../validate_data.py
```

## User Summary

| User ID | Name | Email | Accounts | Transactions |
|---------|------|-------|----------|--------------|
| U001 | Devesh Rawat | devesh08rawat@gmail.com | 2 | 357 |
| U002 | Jyoti Negi | jn503971@gmail.com | 1 | 260 |
| U003 | Deepika Chauhan | deepika5204chauhan@gmail.com | 3 | 726 |
| U004 | Pranjal Arya | pranjal19082004@gmail.com | 1 | 151 |
| U005 | Swati Rawat | devesh1996rawat@gmail.com | 2 | 476 |

## Transaction Categories

Transactions include the following categories:
- INCOME (Salary, Freelance, Transfer)
- GROCERIES
- ENTERTAINMENT
- CLOTHING
- HEALTH
- HOUSING (Rent, Mortgage, Property Tax)
- UTILITIES (Electricity, Water, Gas, Internet)
- TRAVEL
- DEBT (Loan EMI, Credit Card Payment)
- SAVINGS (FD Deposits)
- EDUCATION
- GAMBLING
- FINES
- TAX

## Data Structure

### users.json
```json
{
  "U001": {
    "user_id": "U001",
    "full_name": "Devesh Rawat",
    "email": "devesh08rawat@gmail.com",
    "aadhaar": "123456789012",
    "pan": "ABCD1234A",
    "accounts": [...]
  }
}
```

### statements.json
```json
{
  "ACC-HDFC-01": {
    "account_id": "ACC-HDFC-01",
    "bank_id": "B220",
    "branch_id": "HDFC_BRANCH",
    "transactions": [...]
  }
}
```

## Last Updated

2025-11-22

## Notes

- All bank_id and branch_id values are consistent between users.json and statements.json
- Transaction balances are calculated and included
- All accounts have realistic transaction patterns
- Data covers a 12-month period for comprehensive analysis
