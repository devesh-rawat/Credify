import 'dart:convert';
import 'package:flutter/services.dart';
import 'gemini_service.dart';

class ChatController {
  late List<Map<String, dynamic>> localData;
  final GeminiService gemini;

  ChatController(this.gemini);

  Future<void> loadData() async {
    final String jsonStr =
        await rootBundle.loadString("assets/data/fintech_data.json");
    localData = List<Map<String, dynamic>>.from(jsonDecode(jsonStr));
  }

  /// Calculate Levenshtein distance for typo tolerance
  int _levenshteinDistance(String s1, String s2) {
    if (s1 == s2) return 0;
    if (s1.isEmpty) return s2.length;
    if (s2.isEmpty) return s1.length;

    List<int> v0 = List<int>.generate(s2.length + 1, (i) => i);
    List<int> v1 = List<int>.filled(s2.length + 1, 0);

    for (int i = 0; i < s1.length; i++) {
      v1[0] = i + 1;
      for (int j = 0; j < s2.length; j++) {
        int cost = (s1[i] == s2[j]) ? 0 : 1;
        v1[j + 1] = [
          v1[j] + 1,
          v0[j + 1] + 1,
          v0[j] + cost,
        ].reduce((a, b) => a < b ? a : b);
      }
      List<int> temp = v0;
      v0 = v1;
      v1 = temp;
    }
    return v0[s2.length];
  }

  /// Calculate similarity score (0-100) based on Levenshtein distance
  double _similarityScore(String s1, String s2) {
    int distance = _levenshteinDistance(s1.toLowerCase(), s2.toLowerCase());
    int maxLen = s1.length > s2.length ? s1.length : s2.length;
    if (maxLen == 0) return 100.0;
    return ((maxLen - distance) / maxLen) * 100;
  }

  /// Enhanced context retrieval with fuzzy matching and typo tolerance
  List<String> getBestContext(String question) {
    question = question.toLowerCase().trim();
    
    // Remove common filler words
    final fillerWords = ['what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'does', 'do', 'can', 'will', 'should'];
    List<String> questionWords = question.split(RegExp(r'\s+'))
        .where((word) => word.length > 2 && !fillerWords.contains(word))
        .toList();

    List<Map<String, dynamic>> scored = [];

    for (var item in localData) {
      final q = item["question"].toString().toLowerCase();
      final a = item["answer"].toString().toLowerCase();
      
      double score = 0;

      // 1. Exact phrase match (highest priority)
      if (q.contains(question)) {
        score += 100;
      }

      // 2. Fuzzy match on full question
      double fullSimilarity = _similarityScore(question, q);
      if (fullSimilarity > 60) {
        score += fullSimilarity * 0.8;
      }

      // 3. Keyword matching with typo tolerance
      for (var userWord in questionWords) {
        // Exact word match
        if (q.contains(userWord)) {
          score += 15;
        } else {
          // Fuzzy match for typos
          for (var qWord in q.split(RegExp(r'\s+'))) {
            if (qWord.length > 2) {
              double wordSimilarity = _similarityScore(userWord, qWord);
              if (wordSimilarity > 70) {
                score += wordSimilarity * 0.1;
              }
            }
          }
        }
        
        // Check in answer too
        if (a.contains(userWord)) {
          score += 5;
        }
      }

      // 4. Partial word matching (for compound words)
      for (var word in q.split(RegExp(r'\s+'))) {
        if (word.length > 4) {
          final prefix = word.substring(0, (word.length * 0.6).toInt());
          if (question.contains(prefix)) {
            score += 8;
          }
        }
      }

      // 5. Common bigram/trigram matching
      if (questionWords.length >= 2) {
        for (int i = 0; i < questionWords.length - 1; i++) {
          String bigram = '${questionWords[i]} ${questionWords[i + 1]}';
          if (q.contains(bigram)) {
            score += 20;
          }
        }
      }

      // 6. Acronym matching (e.g., "CIBIL", "EMI", "KYC")
      final acronyms = question.split(RegExp(r'\s+')).where((w) => 
          w.length >= 2 && w == w.toUpperCase()
      );
      for (var acronym in acronyms) {
        if (q.toUpperCase().contains(acronym)) {
          score += 25;
        }
      }

      // Ensure minimum score for fallback
      if (score == 0) {
        score = 1;
      }

      scored.add({"data": item, "score": score});
    }

    // Sort by score descending
    scored.sort((a, b) => (b["score"] as double).compareTo(a["score"] as double));

    // Return top 5 contexts for better coverage
    return scored.take(5).map((e) => e["data"]["answer"] as String).toList();
  }

  Future<String> askGemini(String question) async {
    final bestContexts = getBestContext(question);

    final mergedContext = bestContexts.join("\n\n");

    return gemini.generateAnswer(question, mergedContext);
  }
}
