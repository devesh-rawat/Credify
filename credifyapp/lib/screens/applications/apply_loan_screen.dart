import 'package:credifyapp/models/bank_account_model.dart';
import 'package:credifyapp/providers/auth_provider.dart';
import 'package:credifyapp/services/application_service.dart';
import 'package:credifyapp/services/auth_service.dart';
import 'package:credifyapp/services/storage_service.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ApplyLoanScreen extends StatefulWidget {
  const ApplyLoanScreen({super.key});

  @override
  State<ApplyLoanScreen> createState() => _ApplyLoanScreenState();
}

class _ApplyLoanScreenState extends State<ApplyLoanScreen> {
  final _formKey = GlobalKey<FormState>();
  
  // Form fields
  BankAccount? _selectedAccount;
  final TextEditingController _amountController = TextEditingController();
  final TextEditingController _purposeController = TextEditingController();
  
  // State
  bool _isLoadingAccounts = true;
  bool _isSubmitting = false;
  bool _isAmountReadOnly = false;
  List<BankAccount> _accounts = [];
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadAccounts();
  }

  @override
  void dispose() {
    _amountController.dispose();
    _purposeController.dispose();
    super.dispose();
  }

  Future<void> _loadAccounts() async {
    setState(() {
      _isLoadingAccounts = true;
      _error = null;
    });

    try {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final token = authProvider.token?.accessToken;

      if (token != null) {
        final accounts = await AuthService.getUserBankAccounts(token);
        if (mounted) {
          setState(() {
            _accounts = accounts;
            _isLoadingAccounts = false;
            // Auto-select first account if available
            if (accounts.isNotEmpty) {
              _selectedAccount = accounts.first;
            }
          });
        }
      } else {
        setState(() => _isLoadingAccounts = false);
      }

      // Load saved loan amount
      final savedAmount = await StorageService.getLoanAmount();
      if (savedAmount != null && mounted) {
        setState(() {
          _amountController.text = savedAmount.toStringAsFixed(0);
          _isAmountReadOnly = true;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = "Failed to load bank accounts. Please check your connection.";
          _isLoadingAccounts = false;
        });
      }
    }
  }

  Future<void> _submitApplication() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedAccount == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select a bank account")),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final token = authProvider.token?.accessToken;

      if (token == null) throw Exception("Not authenticated");

      final amount = double.parse(_amountController.text);
      
      await ApplicationService.applyForLoan(token, {
        "account_id": _selectedAccount!.accountId,
        "amount": amount,
        "purpose": _purposeController.text,
      });

      if (mounted) {
        // Show success and go back
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Application submitted successfully!"),
            backgroundColor: Colors.green,
            behavior: SnackBarBehavior.floating,
          ),
          
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Failed to submit application: ${e.toString()}"),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
            
          ),
          
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Scaffold(
      appBar: AppBar(
        title: const Text("Apply for Loan"),
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: isDark ? Colors.white : Colors.black,
      ),
      body: _isLoadingAccounts
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(_error!, style: const TextStyle(color: Colors.red)),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadAccounts,
                        child: const Text("Retry"),
                      ),
                    ],
                  ),
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header
                        Text(
                          "New Application",
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: isDark ? AppColors.darkText : AppColors.lightText,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "Fill in the details below to apply for a new loan.",
                          style: TextStyle(
                            color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                          ),
                        ),
                        const SizedBox(height: 30),

                        // Bank Account Selection
                        Text(
                          "Select Bank Account",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: isDark ? AppColors.darkText : AppColors.lightText,
                          ),
                        ),
                        const SizedBox(height: 10),
                        if (_accounts.isEmpty)
                          Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.orange.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: Colors.orange.withOpacity(0.3)),
                            ),
                            child: const Row(
                              children: [
                                Icon(Icons.warning_amber_rounded, color: Colors.orange),
                                SizedBox(width: 12),
                                Expanded(
                                  child: Text("No linked bank accounts found. Please link a bank account first."),
                                ),
                              ],
                            ),
                          )
                        else
                          DropdownButtonFormField<BankAccount>(
                            initialValue: _selectedAccount,
                            decoration: InputDecoration(
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                              filled: true,
                              fillColor: isDark ? AppColors.darkInput : Colors.grey.shade50,
                            ),
                            items: _accounts.map((account) {
                              return DropdownMenuItem(
                                value: account,
                                child: Text(
                                  "${account.bankName} - ${account.accountNumber.substring(account.accountNumber.length - 4)}",
                                  overflow: TextOverflow.ellipsis,
                                ),
                              );
                            }).toList(),
                            onChanged: (value) {
                              setState(() {
                                _selectedAccount = value;
                              });
                            },
                            validator: (value) => value == null ? "Please select an account" : null,
                          ),

                        const SizedBox(height: 24),

                        // Amount Field
                        Text(
                          "Loan Amount (₹)",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: isDark ? AppColors.darkText : AppColors.lightText,
                          ),
                        ),
                        const SizedBox(height: 10),
                          TextFormField(
                            controller: _amountController,
                            keyboardType: TextInputType.number,
                            readOnly: _isAmountReadOnly,
                            decoration: InputDecoration(
                              hintText: "e.g. 50000",
                              prefixIcon: const Icon(Icons.currency_rupee),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                              filled: true,
                              fillColor: _isAmountReadOnly 
                                  ? (isDark ? Colors.grey.shade800 : Colors.grey.shade200)
                                  : (isDark ? AppColors.darkInput : Colors.grey.shade50),
                            ),
                          validator: (value) {
                            if (value == null || value.isEmpty) return "Please enter an amount";
                            final amount = double.tryParse(value);
                            if (amount == null || amount <= 0) return "Please enter a valid amount";
                            return null;
                          },
                        ),

                        const SizedBox(height: 24),

                        // Purpose Field
                        Text(
                          "Purpose of Loan",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: isDark ? AppColors.darkText : AppColors.lightText,
                          ),
                        ),
                        const SizedBox(height: 10),
                        TextFormField(
                          controller: _purposeController,
                          maxLines: 3,
                          decoration: InputDecoration(
                            hintText: "e.g. Home renovation, Education, etc.",
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            filled: true,
                            fillColor: isDark ? AppColors.darkInput : Colors.grey.shade50,
                          ),
                          validator: (value) {
                            if (value == null || value.isEmpty) return "Please enter a purpose";
                            if (value.length < 5) return "Purpose must be at least 5 characters";
                            return null;
                          },
                        ),

                        const SizedBox(height: 40),

                        // Submit Button
                        SizedBox(
                          width: double.infinity,
                          height: 54,
                          child: ElevatedButton(
                            onPressed: (_isSubmitting || _accounts.isEmpty) ? null : _submitApplication,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Theme.of(context).primaryColor,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(14),
                              ),
                              elevation: 4,
                            ),
                            child: _isSubmitting
                                ? const SizedBox(
                                    height: 24,
                                    width: 24,
                                    child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                                  )
                                : const Text(
                                    "Submit Application",
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.white,
                                    ),
                                  ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
    );
  }
}
