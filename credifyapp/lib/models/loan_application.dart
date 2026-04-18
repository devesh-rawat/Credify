class LoanApplication {
  final String applicationId;
  final String userId;
  final String userName;
  final String bankId;
  final String branchId;
  final String status;
  final double score;
  final String riskLabel;
  final String reportUrl;
  final DateTime createdAt;
  final double amount;
  final String purpose;
  final String? adminNotes;

  LoanApplication({
    required this.applicationId,
    required this.userId,
    required this.userName,
    required this.bankId,
    required this.branchId,
    required this.status,
    required this.score,
    required this.riskLabel,
    required this.reportUrl,
    required this.createdAt,
    this.amount = 0.0,
    this.purpose = '',
    this.adminNotes,
  });

  factory LoanApplication.fromJson(Map<String, dynamic> json) {
    return LoanApplication(
      applicationId: json['application_id'] ?? '',
      userId: json['user_id'] ?? '',
      userName: json['user_name'] ?? '',
      bankId: json['bank_id'] ?? '',
      branchId: json['branch_id'] ?? '',
      status: json['status'] ?? 'PENDING',
      score: (json['score'] ?? 0).toDouble(),
      riskLabel: json['risk_label'] ?? '',
      reportUrl: json['report_url'] ?? '',
      createdAt: DateTime.parse(json['created_at']),
      amount: (json['amount'] ?? 0).toDouble(),
      purpose: json['purpose'] ?? '',
      adminNotes: json['admin_notes'],
    );
  }
}
