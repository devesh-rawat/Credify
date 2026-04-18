// ignore_for_file: deprecated_member_use

import 'package:credifyapp/models/credit_score_model.dart';
import 'package:credifyapp/providers/auth_provider.dart';
import 'package:credifyapp/routes/app_routes.dart';
import 'package:credifyapp/services/auth_service.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';


class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  CreditScore? _creditScore;
  bool _isLoadingScore = true;
  Color? _scoreColor;
  String? _scoreCategory;

  @override
  void initState() {
    super.initState();
    // Defer loading until after the first frame to ensure context is available
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadCreditScore();
    });
  }

  Future<void> _loadCreditScore() async {
    if (!mounted) return;
    
    setState(() {
      _isLoadingScore = true;
    });

    // Retry configuration: attempt every 2 seconds for up to 10 seconds (5 attempts)
    const maxAttempts = 6;
    const retryDelay = Duration(seconds: 2);
    
    for (int attempt = 0; attempt < maxAttempts; attempt++) {
      if (!mounted) return;
      
      try {
        final authProvider = Provider.of<AuthProvider>(context, listen: false);
        final token = authProvider.token?.accessToken;

        if (token != null) {
          final score = await AuthService.getUserScore(token);
          
          // If we got a score, process and display it
          if (score != null) {
            if (!mounted) return;
            
            // Pre-calculate color and category to avoid computation during build
            Color scoreColor = Colors.orange;
            String category = "Fair";
            
            if (score.creditScore >= 750) {
              scoreColor = Colors.green;
              category = "Excellent";
            } else if (score.creditScore >= 650) {
              scoreColor = Colors.lightGreen;
              category = "Good";
            } else if (score.creditScore >= 550) {
              scoreColor = Colors.orange;
              category = "Fair";
            } else if (score.creditScore >= 450) {
              scoreColor = Colors.deepOrange;
              category = "Poor";
            } else {
              scoreColor = Colors.red;
              category = "Very Poor";
            }
            
            setState(() {
              _creditScore = score;
              _scoreColor = scoreColor;
              _scoreCategory = category;
              _isLoadingScore = false;
            });
            return; // Success! Exit the retry loop
          }
        }
      } catch (e) {
        // Error occurred, but we'll retry
        print('Attempt ${attempt + 1} failed: $e');
      }
      
      // If this wasn't the last attempt, wait before retrying
      if (attempt < maxAttempts - 1) {
        await Future.delayed(retryDelay);
      }
    }
    
    // All attempts exhausted
    if (!mounted) return;
    setState(() {
      _isLoadingScore = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final authProvider = Provider.of<AuthProvider>(context);
    final userName = authProvider.fullName ?? 'User';

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,

      floatingActionButton: FloatingActionButton(
        backgroundColor: Theme.of(context).primaryColor,
        child: const Icon(Icons.chat),
        onPressed: () {
          Navigator.pushNamed(context, AppRoutes.chatbot);
         
        },
      ),

      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _loadCreditScore,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [

              // ---------- TOP GREETING + MENU ----------
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "Hello,",
                        style: TextStyle(
                          fontSize: 14,
                          color: Theme.of(context).textTheme.bodyMedium!.color,
                        ),
                      ),
                      Text(
                        userName,
                        style: TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).textTheme.bodyLarge!.color,
                        ),
                      ),
                    ],
                  ),

                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: isDark
                          ? AppColors.darkCard.withOpacity(0.95)
                          : AppColors.lightCard,
                      borderRadius: BorderRadius.circular(12),
                      boxShadow: [
                        BoxShadow(
                          color: isDark
                              ? Colors.black.withOpacity(0.25)
                              : Colors.grey.withOpacity(0.20),
                          blurRadius: 6,
                          offset: const Offset(0, 3),
                        ),
                      ],
                    ),
                    child: IconButton(onPressed: (){
                      Navigator.pushNamed(context,AppRoutes.profile);
                    }, icon: Icon(
                      Icons.menu,
                      color: Theme.of(context).textTheme.bodyLarge!.color,
                    )),
                  ),
                ],
              ),

              const SizedBox(height: 25),

              // ---------- SCORE CARD (DYNAMIC) ----------
              _isLoadingScore
                  ? _loadingScoreCard(context)
                  : _creditScore == null
                      ? _noScoreCard(context)
                      : _scoreCard(context, _creditScore!),

              const SizedBox(height: 30),

              Text(
                "Quick Actions",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  color: Theme.of(context).textTheme.bodyLarge!.color,
                ),
              ),

              const SizedBox(height: 18),

              // ---------- SQUARE CARDS (2 x 2) ----------
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                crossAxisCount: 2,
                childAspectRatio: 1.05,
                children: [
                  _featureSquareCard(
                    context,
                    icon: Icons.account_balance,
                    title: "Bank Accounts",
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.showLinkedBank);
                    },
                  ),
                  _featureSquareCard(
                    context,
                    icon: Icons.receipt_long,
                    title: "EMI Calculator",
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.calculator);
                    },
                  ),
                  _featureSquareCard(
                    context,
                    icon: Icons.insert_drive_file,
                    title: "Applications",
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.applications);
                    },
                  ),
                  _featureSquareCard(
                    context,
                    icon: Icons.gavel,
                    title: "RBI Guidelines",
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.guidelines);
                    },
                  ),
                ],
              ),

              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    ));
  }

  Widget _loadingScoreCard(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
      decoration: BoxDecoration(
        color: isDark
            ? AppColors.darkCard.withOpacity(0.97)
            : AppColors.lightCard,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: isDark
                ? Colors.black.withOpacity(0.30)
                : Colors.grey.withOpacity(0.25),
            blurRadius: 10,
            offset: const Offset(0, 4),
          )
        ],
      ),
      child: Column(
        children: [
          // Pulsing animated circle
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0.8, end: 1.0),
            duration: const Duration(milliseconds: 800),
            curve: Curves.easeInOut,
            builder: (context, value, child) {
              return Transform.scale(
                scale: value,
                child: Container(
                  height: 120,
                  width: 120,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: Theme.of(context).primaryColor.withOpacity(0.5),
                      width: 12,
                    ),
                    color: Theme.of(context).primaryColor.withOpacity(0.1),
                  ),
                  child: Center(
                    child: CircularProgressIndicator(
                      strokeWidth: 3,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        Theme.of(context).primaryColor,
                      ),
                    ),
                  ),
                ),
              );
            },
            onEnd: () {
              // Restart animation
              if (mounted && _isLoadingScore) {
                setState(() {});
              }
            },
          ),
          
          const SizedBox(height: 20),
          
          // Fetching message
          Text(
            "Fetching your score...",
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).textTheme.bodyLarge!.color,
            ),
          ),
          
          const SizedBox(height: 8),
          
          Text(
            "Please wait while we analyze your data",
            style: TextStyle(
              fontSize: 14,
              color: Theme.of(context).textTheme.bodyMedium!.color?.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _scoreCard(BuildContext context, CreditScore score) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    // Use pre-calculated values from state
    final scoreColor = _scoreColor ?? Colors.orange;
    final category = _scoreCategory ?? "Fair";

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 22),
      decoration: BoxDecoration(
        color: isDark
            ? AppColors.darkCard.withOpacity(0.97)
            : AppColors.lightCard,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: isDark
                ? Colors.black.withOpacity(0.30)
                : Colors.grey.withOpacity(0.25),
            blurRadius: 10,
            offset: const Offset(0, 4),
          )
        ],
      ),
      child: Column(
        children: [
          // Score Display Circle
          Container(
            height: 120,
            width: 120,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                color: scoreColor,
                width: 12,
              ),
              color: scoreColor.withOpacity(0.1),
            ),
            child: Center(
              child: Text(
                '${score.creditScore}',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: scoreColor,
                ),
              ),
            ),
          ),

          const SizedBox(height: 14),

          // Category Label
          Text(
            category,
            style: TextStyle(
              color: scoreColor,
              fontSize: 18,
              fontWeight: FontWeight.w600,
            ),
          ),

          const SizedBox(height: 4),

          const Text(
            "Credit Score",
            style: TextStyle(
              fontSize: 14,
            ),
          ),

          const SizedBox(height: 6),

          Text(
            "Range: 300 - 850",
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
          ),

          const SizedBox(height: 20),

          // Action Buttons
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Flexible(
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.pushNamed(context, AppRoutes.score);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: isDark ? AppColors.darkPrimaryBlue : AppColors.lightPrimaryBlue,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  icon: const Icon(Icons.assessment, size: 18),
                  label: const Text("View Report"),
                ),
              ),
              const SizedBox(width: 12),
              Flexible(
                child: OutlinedButton.icon(
                  onPressed: () {
                    Navigator.pushNamed(context, AppRoutes.applyLoan);
                  },
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    side: BorderSide(
                      color: isDark ? AppColors.darkPrimaryBlue : AppColors.lightPrimaryBlue,
                      width: 1.5,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  icon: Icon(
                    Icons.monetization_on_outlined,
                    size: 18,
                    color: isDark ? AppColors.darkPrimaryBlue : AppColors.lightPrimaryBlue,
                  ),
                  label: Text(
                    "Apply Loan",
                    style: TextStyle(
                      color: isDark ? AppColors.darkPrimaryBlue : AppColors.lightPrimaryBlue,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _noScoreCard(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 22),
      decoration: BoxDecoration(
        color: isDark
            ? AppColors.darkCard.withOpacity(0.97)
            : AppColors.lightCard,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: isDark
                ? Colors.black.withOpacity(0.30)
                : Colors.grey.withOpacity(0.25),
            blurRadius: 10,
            offset: const Offset(0, 4),
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [

          Center(
            child: Column(
              children: [
                Container(
                  height: 100,
                  width: 100,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: isDark
                          ? AppColors.darkAccentBlue.withOpacity(0.30)
                          : AppColors.lightPrimaryBlue.withOpacity(0.25),
                      width: 10,
                    ),
                  ),
                  child: Center(
                    child: Text(
                      "—",
                      style: TextStyle(
                        fontSize: 40,
                        fontWeight: FontWeight.bold,
                        color: isDark
                            ? AppColors.darkAccentBlue
                            : AppColors.lightPrimaryBlue,
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 14),

                Text(
                  "No Score Available",
                  style: TextStyle(
                    color: Theme.of(context).textTheme.bodyLarge!.color,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),

                const SizedBox(height: 8),

                Text(
                  "Generate your first Credify Score",
                  style: TextStyle(
                    color: Theme.of(context).textTheme.bodyMedium!.color,
                    fontSize: 14,
                  ),
                ),

                const SizedBox(height: 16),

                ElevatedButton(
                  onPressed: () {
                    Navigator.pushNamed(context, AppRoutes.consent);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Theme.of(context).primaryColor,
                    minimumSize: const Size(160, 45),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                    shadowColor: Theme.of(context).primaryColor.withOpacity(0.4),
                    elevation: 5,
                  ),
                  child: const Text("Generate Score"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _featureSquareCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: isDark
              ? AppColors.darkCard.withOpacity(0.97)
              : AppColors.lightCard,
          borderRadius: BorderRadius.circular(18),
          boxShadow: [
            BoxShadow(
              color: isDark
                  ? Colors.black.withOpacity(0.25)
                  : Colors.grey.withOpacity(0.20),
              blurRadius: 8,
              offset: const Offset(0, 3),
            )
          ],
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isDark
                    ? AppColors.darkAccentBlue.withOpacity(0.08)
                    : AppColors.lightPrimaryBlue.withOpacity(0.12),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(
                icon,
                size: 32,
                color: isDark
                    ? AppColors.darkAccentBlue
                    : AppColors.lightPrimaryBlue,
              ),
            ),

            const SizedBox(height: 14),

            Text(
              title,
              style: TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.w600,
                color: Theme.of(context).textTheme.bodyLarge!.color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
