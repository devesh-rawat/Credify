class ApiConfig {
  // Backend base URL - change this if your backend runs on a different host/port
  static const String baseUrl = 'https://e4c7e0dd096b.ngrok-free.app';
  
  // API endpoints
  static const String signupEndpoint = '/auth_user/signup';
  static const String loginEndpoint = '/auth_user/login';
  static const String myApplications = '/applications/my-applications';
  static const String applyLoan = '/applications/apply';
  
  // Timeout duration
  static const Duration timeout = Duration(seconds: 30);
  
  // Common headers
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // Headers with authentication token
  static Map<String, String> headersWithAuth(String token) => {
    ...headers,
    'Authorization': 'Bearer $token',
  };
}
