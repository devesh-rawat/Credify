import 'api_client.dart';

class OTPService {
  /// Request OTP for account verification
  /// Requires authentication token
  static Future<Map<String, dynamic>> requestOTP({
    required String token,
    required String aadhaar,
    required String pan,
    required double loanAmount,
  }) async {
    final response = await ApiClient.post(
      '/auth_user/request-otp',
      {
        'aadhaar': aadhaar,
        'pan': pan,
        'loan_amount': loanAmount,
      },
      token: token,
    );

    return response;
  }

  /// Verify OTP
  /// Requires authentication token
  static Future<Map<String, dynamic>> verifyOTP({
    required String token,
    required String aadhaar,
    required String otp,
  }) async {
    final response = await ApiClient.post(
      '/auth_user/verify-otp',
      {
        'aadhaar': aadhaar,
        'otp': otp,
      },
      token: token,
    );

    return response;
  }
}
