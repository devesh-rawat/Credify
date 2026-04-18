import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';
import '../services/storage_service.dart';
import '../services/api_client.dart';

class AuthProvider extends ChangeNotifier {
  bool _isLoading = false;
  String? _errorMessage;
  Token? _token;
  bool _isAuthenticated = false;
  String? _fullName;

  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Token? get token => _token;
  bool get isAuthenticated => _isAuthenticated;
  String? get fullName => _fullName;

  /// Initialize provider and check for existing token
  Future<void> initialize() async {
    print('🔍 [AuthProvider] Initializing...');
    final savedToken = await StorageService.getToken();
    final savedUserId = await StorageService.getUserId();
    final savedRole = await StorageService.getRole();
    final savedFullName = await StorageService.getFullName();

    print('🔑 [AuthProvider] Saved token: ${savedToken != null ? "Found" : "Not found"}');
    print('👤 [AuthProvider] Saved userId: ${savedUserId ?? "None"}');

    if (savedToken != null && savedUserId != null) {
      _token = Token(
        accessToken: savedToken,
        tokenType: 'bearer',
        userId: savedUserId,
        role: savedRole,
        fullName: savedFullName,
      );
      _fullName = savedFullName;
      _isAuthenticated = true;
      print('✅ [AuthProvider] User authenticated');
      notifyListeners();
    } else {
      print('❌ [AuthProvider] User not authenticated');
    }
  }

  /// Sign up a new user
  Future<bool> signUp({
    required String email,
    required String password,
    required String fullName,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final token = await AuthService.signup(
        email: email,
        password: password,
        fullName: fullName,
      );

      print('🔐 [AuthProvider] Signup token received: fullName=${token.fullName}');
      await _saveTokenData(token);
      _token = token;
      _fullName = token.fullName;
      _isAuthenticated = true;
      _setLoading(false);
      return true;
    } on ApiException catch (e) {
      _setError(e.message);
      _setLoading(false);
      return false;
    } catch (e) {
      _setError('An unexpected error occurred: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  /// Login an existing user
  Future<bool> login({
    required String email,
    required String password,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final token = await AuthService.login(
        email: email,
        password: password,
      );

      print('🔐 [AuthProvider] Login token received: fullName=${token.fullName}');
      await _saveTokenData(token);
      _token = token;
      _fullName = token.fullName;
      _isAuthenticated = true;
      _setLoading(false);
      return true;
    } on ApiException catch (e) {
      _setError(e.message);
      _setLoading(false);
      return false;
    } catch (e) {
      _setError('An unexpected error occurred: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  /// Logout user
  Future<void> logout(BuildContext context) async {
    await StorageService.clearAll();
    _token = null;
    _fullName = null;
    _isAuthenticated = false;
    notifyListeners();
    
    // Navigate to login screen
    if (context.mounted) {
      Navigator.of(context).pushNamedAndRemoveUntil(
        '/login',
        (route) => false,
      );
    }
  }

  /// Save token data to storage
  Future<void> _saveTokenData(Token token) async {
    await StorageService.saveToken(token.accessToken);
    if (token.userId != null) {
      await StorageService.saveUserId(token.userId!);
    }
    if (token.role != null) {
      await StorageService.saveRole(token.role!);
    }
    if (token.fullName != null) {
      print('💾 [AuthProvider] Saving fullName: ${token.fullName}');
      await StorageService.saveFullName(token.fullName!);
    } else {
      print('⚠️ [AuthProvider] No fullName in token to save');
    }
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  void _setError(String message) {
    _errorMessage = message;
    notifyListeners();
  }

  void _clearError() {
    _errorMessage = null;
  }

  /// Clear error message
  void clearError() {
    _clearError();
    notifyListeners();
  }
}
