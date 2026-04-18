class UserProfile {
  final String userId;
  final String email;
  final String fullName;
  final String? pan;
  final String? aadhaar;

  UserProfile({
    required this.userId,
    required this.email,
    required this.fullName,
    this.pan,
    this.aadhaar,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      userId: json['user_id'] as String,
      email: json['email'] as String,
      fullName: json['full_name'] as String,
      pan: json['pan'] as String?,
      aadhaar: json['aadhaar'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'user_id': userId,
        'email': email,
        'full_name': fullName,
        if (pan != null) 'pan': pan,
        if (aadhaar != null) 'aadhaar': aadhaar,
      };

  /// Check if user has completed KYC (both PAN and Aadhaar)
  bool hasKyc() {
    return pan != null && pan!.isNotEmpty && aadhaar != null && aadhaar!.isNotEmpty;
  }

  /// Get formatted Aadhaar number (XXXX XXXX 1234)
  String getFormattedAadhaar() {
    if (aadhaar == null || aadhaar!.isEmpty) return 'Not Available';
    if (aadhaar!.length >= 4) {
      final lastFour = aadhaar!.substring(aadhaar!.length - 4);
      return 'XXXX XXXX $lastFour';
    }
    return aadhaar!;
  }

  /// Get formatted PAN number (XXXXX1234F)
  String getFormattedPan() {
    if (pan == null || pan!.isEmpty) return 'Not Available';
    if (pan!.length >= 5) {
      final lastFive = pan!.substring(pan!.length - 5);
      return 'XXXXX$lastFive';
    }
    return pan!;
  }
}
