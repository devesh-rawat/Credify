import 'package:google_generative_ai/google_generative_ai.dart';

class GeminiService {
  final GenerativeModel model;

  GeminiService(String apiKey)
      : model = GenerativeModel(
          model: "gemini-2.0-flash",
          apiKey: apiKey,
        );

  Future<String> generateAnswer(String question, String context) async {
    final prompt = """
You are Credify AI, a helpful financial assistant specializing in credit scores, loans, and financial services in India.

Your job:
1. Read the provided CONTEXT from the Credify knowledge base.
2. Answer the user's question using ONLY the information in the context.
3. Provide clear, concise, and helpful explanations.
4. If the context contains relevant information, use it to answer naturally.
5. If the question is completely unrelated to finance/credit (e.g., "What's the weather?"), politely say you can only help with Credify-related financial questions.
6. Never invent information - only use what's in the context.

—————————————
CONTEXT:
$context
—————————————

USER QUESTION:
$question

Provide a helpful, natural answer based on the context above.
""";

    final response = await model.generateContent([
      Content.text(prompt),
    ]);

    return response.text ?? "No response.";
  }
}
