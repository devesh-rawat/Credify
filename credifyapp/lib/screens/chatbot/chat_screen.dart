import 'package:credifyapp/theme/theme.dart';
import 'package:flutter/material.dart';
import 'chat_controller.dart';
import 'gemini_service.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  late ChatController controller;
  final TextEditingController textController = TextEditingController();

  final ScrollController _scrollController = ScrollController();

  bool isLoading = false;

  /// For typewriter animation
  String animatedBotText = "";

  List<Map<String, String>> messages = [];
  
  /// Show suggestion chips only on first load
  bool showSuggestionChips = true;
  
  /// Suggested questions for quick start
  final List<String> suggestedQuestions = [
    "What is a credit score?",
    "How to improve my CIBIL score?",
    "What are loan interest rates?",
    "How does credit history work?",
  ];

  @override
  void initState() {
    super.initState();

    controller = ChatController(
      GeminiService("AIzaSyCVVSg_q5EQkS9-u8zb4HJz9hcWvXAKvIE"),
    );

    controller.loadData();

    // Initial welcome message
    messages.add({
      "sender": "bot",
      "text":
          "Hello! I'm Credify AI, your personal finance assistant. Ask me anything about credit score, loans, CIBIL, or interest rates!"
    });

    Future.delayed(const Duration(milliseconds: 100), scrollToBottom);
  }

  void scrollToBottom() {
    if (!_scrollController.hasClients || !mounted) return;
    Future.delayed(const Duration(milliseconds: 100), () {
      if (!mounted || !_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 350),
        curve: Curves.easeOut,
      );
    });
  }

  Future<void> sendMessage() async {
    final question = textController.text.trim();
    if (question.isEmpty || isLoading) return;

    // Add the user message
    if (!mounted) return; // Check before setState
    setState(() {
      messages.add({"sender": "user", "text": question});
      isLoading = true;
      showSuggestionChips = false; // Hide chips after first message
    });
    scrollToBottom();

    textController.clear();

    final answer = await controller.askGemini(question);

    // Hide loading indicator and start animated typewriter reply
    if (!mounted) return; // Check before setState
    setState(() {
      animatedBotText = "";
      isLoading = false;  // Hide progress indicator when typing starts
    });

    await animateBotText(answer);

    scrollToBottom();
  }

  Future<void> animateBotText(String fullText) async {
    for (int i = 0; i < fullText.length; i++) {
      await Future.delayed(const Duration(milliseconds: 14));
      if (!mounted) return; // Fix crash when exiting during animation
      setState(() {
        animatedBotText = fullText.substring(0, i + 1);
      });
      scrollToBottom();
    }

    // After animation ends, add final message
    if (!mounted) return; // Fix crash when exiting during animation
    setState(() {
      messages.add({"sender": "bot", "text": fullText});
      animatedBotText = "";
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Credify AI Assistant",
          style: TextStyle(
            fontWeight: FontWeight.w600,
            color: isDark ? AppColors.darkText : AppColors.lightText,
          ),
        ),
      ),

      body: Column(
        children: [
          // MESSAGES LIST
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount:
                  messages.length + (animatedBotText.isNotEmpty ? 1 : 0) + (showSuggestionChips ? 1 : 0),
              itemBuilder: (context, index) {
                // Show suggestion chips at the end (after welcome message)
                if (showSuggestionChips && index == messages.length) {
                  return Padding(
                    padding: const EdgeInsets.only(top: 16, bottom: 8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "💡 Quick questions:",
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 8,
                          runSpacing: 10,
                          children: suggestedQuestions.map((question) {
                            return InkWell(
                              onTap: () {
                                textController.text = question;
                                sendMessage();
                              },
                              borderRadius: BorderRadius.circular(20),
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 14,
                                  vertical: 10,
                                ),
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    colors: [
                                      isDark 
                                          ? AppColors.darkCard
                                          : AppColors.lightCard,
                                      isDark
                                          ? AppColors.darkAccentBlue.withOpacity(0.1)
                                          : AppColors.lightPrimaryBlue.withOpacity(0.08),
                                    ],
                                  ),
                                  borderRadius: BorderRadius.circular(20),
                                  border: Border.all(
                                    color: isDark 
                                        ? AppColors.darkAccentBlue.withOpacity(0.4)
                                        : AppColors.lightPrimaryBlue.withOpacity(0.4),
                                    width: 1.5,
                                  ),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(
                                      Icons.lightbulb_outline,
                                      size: 16,
                                      color: isDark 
                                          ? AppColors.darkAccentBlue
                                          : AppColors.lightPrimaryBlue,
                                    ),
                                    const SizedBox(width: 6),
                                    Flexible(
                                      child: Text(
                                        question,
                                        style: TextStyle(
                                          fontSize: 13,
                                          fontWeight: FontWeight.w500,
                                          color: isDark ? AppColors.darkText : AppColors.lightText,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  );
                }
                
                // Adjust index for regular messages
                final messageIndex = showSuggestionChips && index > messages.length ? index - 1 : index;
                
                // Regular messages
                if (messageIndex < messages.length) {
                  final msg = messages[messageIndex];
                  final isUser = msg["sender"] == "user";
                  return _buildChatBubble(msg["text"]!, isUser, isDark);
                }

                // Typewriter animation bubble
                if (animatedBotText.isNotEmpty &&
                    messageIndex == messages.length) {
                  return _buildChatBubble(animatedBotText, false, isDark);
                }

                return const SizedBox();
              },
            ),
          ),

          // Linear Progress Loader above input box
          if (isLoading)
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: LinearProgressIndicator(),
            ),

          const SizedBox(height: 8),

          // INPUT BOX
          Container(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: textController,
                    enabled: !isLoading,
                    style: TextStyle(
                      color:
                          isDark ? AppColors.darkText : AppColors.lightText,
                    ),
                    decoration: InputDecoration(
                      hintText: isLoading
                          ? "Credify is generating..."
                          : "Ask something...",
                      hintStyle: TextStyle(
                        color: isDark
                            ? AppColors.darkMuted
                            : AppColors.lightTextSecondary,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                GestureDetector(
                  onTap: isLoading ? null : sendMessage,
                  child: CircleAvatar(
                    radius: 24,
                    backgroundColor: isLoading
                        ? Colors.grey
                        : (isDark
                            ? AppColors.darkAccentBlue
                            : AppColors.lightPrimaryBlue),
                    child: const Icon(Icons.send, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // Chat Bubble Widget
  Widget _buildChatBubble(String text, bool isUser, bool isDark) {
    return Column(
      crossAxisAlignment:
          isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: Text(
            isUser ? "You" : "Credify AI",
            style: TextStyle(
              fontSize: 12,
              color:
                  isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
            ),
          ),
        ),
        Align(
          alignment:
              isUser ? Alignment.centerRight : Alignment.centerLeft,
          child: Container(
            margin: const EdgeInsets.symmetric(vertical: 6),
            padding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * 0.78,
            ),
            decoration: BoxDecoration(
              color: isUser
                  ? (isDark
                      ? AppColors.darkPrimaryBlue
                      : AppColors.lightPrimaryBlue)
                  : (isDark
                      ? AppColors.darkCard
                      : AppColors.lightCard),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              text,
              style: TextStyle(
                color: isUser
                    ? Colors.white
                    : (isDark
                        ? AppColors.darkText
                        : AppColors.lightText),
                fontSize: 15,
                height: 1.35,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
