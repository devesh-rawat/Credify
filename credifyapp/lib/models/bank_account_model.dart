class BankAccount {
  final String accountId;
  final String bankName;
  final String accountNumber;
  final String ifsc;
  final String accountType;
  final String? bankId;
  final String? branchId;

  BankAccount({
    required this.accountId,
    required this.bankName,
    required this.accountNumber,
    required this.ifsc,
    required this.accountType,
    this.bankId,
    this.branchId,
  });

  factory BankAccount.fromJson(Map<String, dynamic> json) {
    return BankAccount(
      accountId: json['account_id'] as String,
      bankName: json['bank_name'] as String,
      accountNumber: json['account_number'] as String,
      ifsc: json['ifsc'] as String,
      accountType: json['account_type'] as String,
      bankId: json['bank_id'] as String?,
      branchId: json['branch_id'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'account_id': accountId,
        'bank_name': bankName,
        'account_number': accountNumber,
        'ifsc': ifsc,
        'account_type': accountType,
        if (bankId != null) 'bank_id': bankId,
        if (branchId != null) 'branch_id': branchId,
      };

  /// Get masked account number (shows last 4 digits)
  String getMaskedAccountNumber() {
    if (accountNumber.length >= 4) {
      final lastFour = accountNumber.substring(accountNumber.length - 4);
      return 'XXXX $lastFour';
    }
    return accountNumber;
  }

  /// Get account type display name
  String getAccountTypeDisplay() {
    switch (accountType.toUpperCase()) {
      case 'SAVINGS':
        return 'Savings';
      case 'CURRENT':
        return 'Current';
      case 'SALARY':
        return 'Salary';
      default:
        return accountType;
    }
  }
}
