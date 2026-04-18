import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_config.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, [this.statusCode]);

  @override
  String toString() => message;
}

class ApiClient {
  /// Make a POST request
  static Future<Map<String, dynamic>> post(
    String endpoint,
    Map<String, dynamic> body, {
    String? token,
  }) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      final headers = token != null 
          ? ApiConfig.headersWithAuth(token) 
          : ApiConfig.headers;
      
      final response = await http
          .post(
            url,
            headers: headers,
            body: jsonEncode(body),
          )
          .timeout(ApiConfig.timeout);

      return _handleResponse(response) as Map<String, dynamic>;
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Network error: ${e.toString()}');
    }
  }

  /// Make a GET request
  static Future<dynamic> get(
    String endpoint, {
    String? token,
  }) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      final headers = token != null 
          ? ApiConfig.headersWithAuth(token) 
          : ApiConfig.headers;

      final response = await http
          .get(url, headers: headers)
          .timeout(ApiConfig.timeout);

      return _handleResponse(response);
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Network error: ${e.toString()}');
    }
  }

  /// Handle HTTP response
  static dynamic _handleResponse(http.Response response) {
    final statusCode = response.statusCode;

    if (statusCode >= 200 && statusCode < 300) {
      // Success
      if (response.body.isEmpty) {
        return {};
      }
      final responseData = jsonDecode(response.body);
      print('📡 [ApiClient] Response: $responseData');
      return responseData;
    } else {
      // Error
      String errorMessage = 'Request failed with status $statusCode';
      
      try {
        final errorBody = jsonDecode(response.body);
        if (errorBody is Map && errorBody.containsKey('detail')) {
          errorMessage = errorBody['detail'].toString();
        }
      } catch (_) {
        // If we can't parse the error, use the default message
      }

      throw ApiException(errorMessage, statusCode);
    }
  }
}
