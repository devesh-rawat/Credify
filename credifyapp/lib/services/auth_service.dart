import '../models/user_model.dart';
import '../models/user_profile_model.dart';
import '../models/bank_account_model.dart';
import '../models/credit_score_model.dart';
import 'api_client.dart';
import 'api_config.dart';

class AuthService {
  /// Sign up a new user
  static Future<Token> signup({
    required String email,
    required String password,
    required String fullName,
  }) async {
    final userCreate = UserCreate(
      email: email,
      password: password,
      fullName: fullName,
    );

    final response = await ApiClient.post(
      ApiConfig.signupEndpoint,
      userCreate.toJson(),
    );

    print('🔑 [AuthService] Signup response: $response');
    final token = Token.fromJson(response);
    print('🔑 [AuthService] Parsed token - fullName: ${token.fullName}');
    return token;
  }

  /// Login an existing user
  static Future<Token> login({
    required String email,
    required String password,
  }) async {
    final userLogin = UserLogin(
      email: email,
      password: password,
    );

    final response = await ApiClient.post(
      ApiConfig.loginEndpoint,
      userLogin.toJson(),
    );

    print('🔑 [AuthService] Login response: $response');
    final token = Token.fromJson(response);
    print('🔑 [AuthService] Parsed token - fullName: ${token.fullName}');
    return token;
  }

  /// Get current user profile
  static Future<UserProfile> getUserProfile(String token) async {
    final response = await ApiClient.get(
      '/auth_user/me',
      token: token,
    );

    print('👤 [AuthService] User profile response: $response');
    return UserProfile.fromJson(response);
  }

  /// Get user's bank accounts
  static Future<List<BankAccount>> getUserBankAccounts(String token) async {
    final response = await ApiClient.get(
      '/aa/banks',
      token: token,
    );

    print('🏦 [AuthService] Bank accounts response: $response');
    
    if (response is List) {
      return response.map((json) => BankAccount.fromJson(json as Map<String, dynamic>)).toList();
    }
    
    return [];
  }

  /// Get user's credit score
  static Future<CreditScore?> getUserScore(String token) async {
    try {
      final response = await ApiClient.get(
        '/scoring/me',
        token: token,
      );

      return CreditScore.fromJson(response as Map<String, dynamic>);
    } catch (e) {
      // Return null if 404 (no score found)
      if (e.toString().contains('404') || e.toString().contains('No score found')) {
        return null;
      }
      rethrow;
    }
  }
}
