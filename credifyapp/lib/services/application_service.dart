import 'package:credifyapp/models/loan_application.dart';
import 'package:credifyapp/services/api_client.dart';
import 'package:credifyapp/services/api_config.dart';

class ApplicationService {
  static Future<List<LoanApplication>> fetchMyApplications(String token) async {
    try {
      final dynamic data = await ApiClient.get(
        ApiConfig.myApplications,
        token: token,
      );

      if (data is List) {
        return data.map((json) => LoanApplication.fromJson(json)).toList();
      } else {
        throw Exception('Unexpected response format: expected List, got ${data.runtimeType}');
      }
    } catch (e) {
      print('❌ [ApplicationService] Error fetching applications: $e');
      rethrow;
    }
  }
  static Future<LoanApplication> applyForLoan(String token, Map<String, dynamic> data) async {
    try {
      final dynamic response = await ApiClient.post(
        ApiConfig.applyLoan,
        data,
        token: token,
      );

      return LoanApplication.fromJson(response);
    } catch (e) {
      print('❌ [ApplicationService] Error applying for loan: $e');
      rethrow;
    }
  }
}
