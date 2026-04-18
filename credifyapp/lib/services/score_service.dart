import 'package:credifyapp/models/credit_score_model.dart';
import 'package:credifyapp/services/api_client.dart';

class ScoreService {
  /// Fetch the user's credit score from the backend
  static Future<CreditScore> fetchUserScore(String token) async {
    try {
      print('📊 [ScoreService] Fetching user score...');
      
      final response = await ApiClient.get(
        '/scoring/me',
        token: token,
      );
      
      print('✅ [ScoreService] Score data received: $response');
      
      return CreditScore.fromJson(response as Map<String, dynamic>);
    } catch (e) {
      print('❌ [ScoreService] Error fetching score: $e');
      rethrow;
    }
  }
}
