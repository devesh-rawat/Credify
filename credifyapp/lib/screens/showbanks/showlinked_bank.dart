import 'package:credifyapp/models/bank_account_model.dart';
import 'package:credifyapp/providers/auth_provider.dart';
import 'package:credifyapp/services/auth_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ShowLinkedBank extends StatefulWidget {
  const ShowLinkedBank({super.key});

  @override
  State<ShowLinkedBank> createState() => _ShowLinkedBankState();
}

class _ShowLinkedBankState extends State<ShowLinkedBank> {
  List<BankAccount>? _bankAccounts;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadBankAccounts();
  }

  Future<void> _loadBankAccounts() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final token = authProvider.token?.accessToken;

      if (token == null) {
        setState(() {
          _errorMessage = 'Not authenticated';
          _isLoading = false;
        });
        return;
      }

      final accounts = await AuthService.getUserBankAccounts(token);
      setState(() {
        _bankAccounts = accounts;
        _isLoading = false;
      });
    } catch (e) {
      final errorMsg = e.toString().toLowerCase();
      String displayMessage;
      
      // Check if it's a network error
      if (errorMsg.contains('network') || 
          errorMsg.contains('socket') || 
          errorMsg.contains('connection') ||
          errorMsg.contains('failed host lookup')) {
        displayMessage = 'No internet connection';
      } else {
        displayMessage = 'Failed to load bank accounts';
      }
      
      setState(() {
        _errorMessage = displayMessage;
        _isLoading = false;
      });
    }
  }

  // Mask account number
  String _maskAccountNumber(String number) {
    if (number.length >= 4) {
      return "••••••${number.substring(number.length - 4)}";
    }
    return number;
  }

  // Select icon based on account type
  IconData _getAccountIcon(String type) {
    switch (type.toUpperCase()) {
      case "SAVINGS":
        return Icons.account_balance_wallet_rounded;
      case "CURRENT":
        return Icons.account_balance_wallet_rounded;
      case "SALARY":
        return Icons.account_balance_wallet_rounded;
      default:
        return Icons.account_balance;
    }
  }

  // Auto-generate color based on bank name
  Color _getBankColor(String bankName) {
    if (bankName.contains("HDFC")) return Colors.redAccent;
    if (bankName.contains("SBI")) return Colors.blue;
    if (bankName.contains("ICICI")) return Colors.deepOrange;
    if (bankName.contains("Axis")) return Colors.purple;
    if (bankName.contains("Kotak")) return Colors.indigo;
    if (bankName.contains("Yes")) return Colors.teal;
    return Colors.green;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 10),

              // ------------------ TITLE ------------------
              Text(
                "Your Linked Accounts",
                style: theme.textTheme.bodyLarge!.copyWith(
                  fontSize: 26,
                  fontWeight: FontWeight.w600,
                ),
              ),

              const SizedBox(height: 10),

              // ------------------ SUBTITLE ------------------
              Text(
                "These accounts will be used to fetch statements for analysis.",
                style: theme.textTheme.bodyMedium!.copyWith(fontSize: 14),
              ),

              const SizedBox(height: 25),

              // ------------------ CONTENT ------------------
              Expanded(
                child: _buildContent(theme),
              ),

              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildContent(ThemeData theme) {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_errorMessage != null) {
      final isNetworkError = _errorMessage == 'No internet connection';
      
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              isNetworkError ? Icons.wifi_off : Icons.error_outline,
              size: 64,
              color: isNetworkError ? Colors.orange : Colors.red,
            ),
            const SizedBox(height: 16),
            Text(
              _errorMessage!,
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              isNetworkError 
                  ? 'Please check your connection and try again'
                  : 'Something went wrong',
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _loadBankAccounts,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_bankAccounts == null || _bankAccounts!.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.account_balance_outlined,
              size: 80,
              color: theme.disabledColor,
            ),
            const SizedBox(height: 16),
            Text(
              "No Bank Accounts Linked",
              style: theme.textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              "Complete KYC verification to link your bank accounts",
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium,
            ),
          ],
        ),
      );
    }

    return ListView.separated(
      physics: const BouncingScrollPhysics(),
      itemCount: _bankAccounts!.length,
      separatorBuilder: (_, __) => const SizedBox(height: 16),
      itemBuilder: (context, index) {
        final account = _bankAccounts![index];
        final bankColor = _getBankColor(account.bankName);

        return AnimatedContainer(
          duration: const Duration(milliseconds: 250),
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: theme.cardColor,
            borderRadius: BorderRadius.circular(16),
            boxShadow: const [
              BoxShadow(
                color: Colors.black12,
                spreadRadius: 1,
                blurRadius: 6,
              )
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ------------- BANK NAME WITH ICON -------------
              Row(
                children: [
                  Icon(Icons.account_balance, color: bankColor, size: 22),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      account.bankName,
                      style: theme.textTheme.bodyLarge!.copyWith(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  // Account Type Badge
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: bankColor.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      account.getAccountTypeDisplay(),
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: bankColor,
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              // ------------- ACCOUNT DETAILS -------------
              Row(
                children: [
                  CircleAvatar(
                    radius: 26,
                    backgroundColor: bankColor.withOpacity(0.18),
                    child: Icon(
                      _getAccountIcon(account.accountType),
                      size: 26,
                      color: bankColor,
                    ),
                  ),

                  const SizedBox(width: 16),

                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Account No: ${_maskAccountNumber(account.accountNumber)}",
                          style: theme.textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 2),
                        Text(
                          "IFSC: ${account.ifsc}",
                          style: theme.textTheme.bodyMedium,
                        ),
                        if (account.branchId != null) ...[
                          const SizedBox(height: 2),
                          Text(
                            "Branch: ${account.branchId}",
                            style: theme.textTheme.bodyMedium!.copyWith(
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
