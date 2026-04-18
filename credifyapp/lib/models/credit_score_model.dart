import 'package:flutter/material.dart';

class CreditScore {
  final String userId;
  final int creditScore;
  final double defaultProbability;
  final String riskLabel;
  final String summary;
  final List<String> keyFactors;
  final List<String> recommendations;
  final List<String> underwritingNote;
  final String recommendation;
  final String reportPath;
  final DateTime? createdAt;
  final String accountId;

  CreditScore({
    required this.userId,
    required this.creditScore,
    required this.defaultProbability,
    required this.riskLabel,
    required this.summary,
    required this.keyFactors,
    required this.recommendations,
    required this.underwritingNote,
    required this.recommendation,
    required this.reportPath,
    this.createdAt,
    required this.accountId,
  });

  factory CreditScore.fromJson(Map<String, dynamic> json) {
    // Handle both int and double from backend
    final scoreValue = json['credit_score'];
    final score = scoreValue is int ? scoreValue : (scoreValue as num).toInt();
    
    // Handle default_probability
    final defaultProbValue = json['default_probability'];
    final defaultProb = defaultProbValue is double 
        ? defaultProbValue 
        : (defaultProbValue as num).toDouble();
    
    return CreditScore(
      userId: json['user_id'] as String? ?? '',
      creditScore: score,
      defaultProbability: defaultProb,
      riskLabel: json['risk_label'] as String,
      summary: json['summary'] as String? ?? '',
      keyFactors: (json['key_factors'] as List<dynamic>?)
          ?.map((e) => e.toString())
          .toList() ?? [],
      recommendations: (json['recommendations'] as List<dynamic>?)
          ?.map((e) => e.toString())
          .toList() ?? [],
      underwritingNote: (json['underwriting_note'] as List<dynamic>?)
          ?.map((e) => e.toString())
          .toList() ?? [],
      recommendation: json['recommendation'] as String? ?? 'REVIEW',
      reportPath: json['report_path'] as String? ?? '',
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at'] as String)
          : null,
      accountId: json['account_id'] as String? ?? 'ALL_ACCOUNTS',
    );
  }

  Map<String, dynamic> toJson() => {
        'user_id': userId,
        'credit_score': creditScore,
        'default_probability': defaultProbability,
        'risk_label': riskLabel,
        'summary': summary,
        'key_factors': keyFactors,
        'recommendations': recommendations,
        'underwriting_note': underwritingNote,
        'recommendation': recommendation,
        'report_path': reportPath,
        if (createdAt != null) 'created_at': createdAt!.toIso8601String(),
        'account_id': accountId,
      };

  /// Calculate progress value for circular indicator (0.0 to 1.0)
  /// Score range: 300-900
  double getProgress() {
    const minScore = 300;
    const maxScore = 900;
    
    if (creditScore <= minScore) return 0.0;
    if (creditScore >= maxScore) return 1.0;
    
    return (creditScore - minScore) / (maxScore - minScore);
  }

  /// Get color based on score value
  Color getScoreColor() {
    if (creditScore >= 750) {
      return Colors.green; // Excellent
    } else if (creditScore >= 650) {
      return Colors.lightGreen; // Good
    } else if (creditScore >= 550) {
      return Colors.orange; // Fair
    } else if (creditScore >= 450) {
      return Colors.deepOrange; // Poor
    } else {
      return Colors.red; // Very Poor
    }
  }

  /// Get score category label
  String getScoreCategory() {
    if (creditScore >= 750) {
      return 'Excellent';
    } else if (creditScore >= 650) {
      return 'Good';
    } else if (creditScore >= 550) {
      return 'Fair';
    } else if (creditScore >= 450) {
      return 'Poor';
    } else {
      return 'Very Poor';
    }
  }

  /// Get formatted score string
  String getFormattedScore() {
    return creditScore.toString();
  }

  /// Calculate creditworthiness score (0-100)
  /// Based on credit score normalized to 100 scale
  double getCreditworthiness() {
    // Map 300-900 range to 0-100
    const minScore = 300;
    const maxScore = 900;
    
    if (creditScore <= minScore) return 0.0;
    if (creditScore >= maxScore) return 100.0;
    
    return ((creditScore - minScore) / (maxScore - minScore)) * 100;
  }

  /// Get payment discipline as percentage string
  /// Based on inverse of default probability
  String getPaymentDisciplinePercent() {
    final discipline = (1 - defaultProbability) * 100;
    return '${discipline.toStringAsFixed(1)}%';
  }

  /// Get report URL (for backward compatibility)
  String? get reportUrl => reportPath.isNotEmpty ? reportPath : null;
}
