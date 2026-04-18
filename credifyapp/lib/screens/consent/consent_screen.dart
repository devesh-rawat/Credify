import 'package:credifyapp/routes/app_routes.dart';
import 'package:flutter/material.dart';

class ConsentScreen extends StatefulWidget {
  const ConsentScreen({super.key});

  @override
  State<ConsentScreen> createState() => _ConsentScreenState();
}

class _ConsentScreenState extends State<ConsentScreen> {
  bool isChecked = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(height: 36,),
              Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 5),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: theme.cardColor.withValues(alpha:0.15),
                  ),
                  child: Icon(
                    Icons.verified_user_rounded,
                    color: theme.primaryColor,
                    size: 64,
                  ),
                ),
              ),
        
              const SizedBox(height: 8),
        
              Text(
                "Data Access Consent",
                style: theme.textTheme.bodyLarge!.copyWith(
                  fontSize: 26,
                  fontWeight: FontWeight.w600,
                ),
              ),
        
              const SizedBox(height: 10),
        
              Text(
                "To generate your credit score, we require your permission to access your financial behavior and transaction patterns.",
                style: theme.textTheme.bodyMedium!.copyWith(height: 1.5),
              ),
        
              const SizedBox(height: 24),
        
              
              permissionCard(
                icon: Icons.account_balance,
                title: "Bank Transactions",
                subtitle: "Access your transaction history",
                theme: theme,
              ),
        
              const SizedBox(height: 14),
        
              permissionCard(
                icon: Icons.show_chart_sharp,
                title: "Financial Profile",
                subtitle: "Analyze your spending patterns",
                theme: theme,
              ),
        
              const SizedBox(height: 14),
        
              permissionCard(
                icon: Icons.file_copy_rounded,
                title: "Document Verification",
                subtitle: "Securely store your documents",
                theme: theme,
              ),
        
              const SizedBox(height: 26),
        
              // CHECKBOX — theme driven
              Row(
                children: [
                  Checkbox(
                    value: isChecked,
                    onChanged: (v) => setState(() => isChecked = v!),
                    activeColor: theme.primaryColor,
                  ),
                  Expanded(
                    child: Text(
                      "I agree to share my data for analysis and credit score generation",
                      style: theme.textTheme.bodyLarge,
                    ),
                  ),
                ],
              ),
        
              const SizedBox(height: 16),
        
              // SECURITY BANNER
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.green.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: Colors.green),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.lock, color: Colors.green),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        "Your data is encrypted and stored securely",
                        style: theme.textTheme.bodyLarge,
                      ),
                    ),
                  ],
                ),
              ),
        
              const SizedBox(height: 28),
        
              // THEME-BASED BUTTON
              ElevatedButton(
                onPressed: isChecked ? () {
                  Navigator.pushReplacementNamed(context,AppRoutes.verifyAccount);
                } : null,
                child: const Text("Continue"),
              ),
        
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }


  Widget permissionCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required ThemeData theme,
  }) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: theme.cardColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Icon(icon, color: theme.primaryColor, size: 28),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: theme.textTheme.bodyLarge!.copyWith(
                    fontWeight: FontWeight.w600,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: theme.textTheme.bodyMedium!.copyWith(fontSize: 13),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
