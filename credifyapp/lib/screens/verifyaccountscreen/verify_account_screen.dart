import 'package:credifyapp/routes/app_routes.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../services/otp_service.dart';
import '../../services/api_client.dart';

class VerifyAccountScreen extends StatefulWidget {
  const VerifyAccountScreen({super.key});

  @override
  State<VerifyAccountScreen> createState() => _VerifyAccountScreenState();
}

class _VerifyAccountScreenState extends State<VerifyAccountScreen> {
  final TextEditingController aadhaarController = TextEditingController();
  final TextEditingController panController = TextEditingController();
  final TextEditingController loanAmountController = TextEditingController();
  
  bool _isLoading = false;
  String? _errorMessage;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 30),
            
                /// Title
                Center(
                  child: Text(
                    "Verify Your Identity",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.w600,
                      color: isDark ? AppColors.darkText : AppColors.lightText,
                    ),
                  ),
                ),
            
                const SizedBox(height: 30),
            
                /// Top Icon
                Center(
                  child: Icon(
                    Icons.verified_user_rounded,
                    size: 68,
                    color: AppColors.darkAccentBlue,
                  ),
                ),
            
                const SizedBox(height: 20),
            
                /// Aadhaar Field
                Text(
                  "Aadhaar Number",
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: isDark ? AppColors.darkText : AppColors.lightText,
                  ),
                ),
                const SizedBox(height: 10),
            
                TextField(
                  controller: aadhaarController,
                  keyboardType: TextInputType.number,
                  maxLength: 12,
                  decoration: InputDecoration(
                    counterText: "",
                    hintText: "Enter your Aadhaar number",
                    hintStyle: TextStyle(
                      color: isDark
                          ? AppColors.darkMuted
                          : AppColors.lightTextSecondary,
                    ),
                  ),
                ),
            
                const SizedBox(height: 20),
            
                /// PAN Field
                Text(
                  "PAN Number",
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: isDark ? AppColors.darkText : AppColors.lightText,
                  ),
                ),
                const SizedBox(height: 10),
            
                TextField(
                  controller: panController,
                  textCapitalization: TextCapitalization.characters,
                  maxLength: 10,
                  decoration: InputDecoration(
                    counterText: "",
                    hintText: "ABCDE1234F",
                    hintStyle: TextStyle(
                      color: isDark
                          ? AppColors.darkMuted
                          : AppColors.lightTextSecondary,
                    ),
                  ),
                ),
            
                const SizedBox(height: 20),
            
                /// Loan Amount Field (NEW)
                Text(
                  "Loan Amount Required",
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: isDark ? AppColors.darkText : AppColors.lightText,
                  ),
                ),
                const SizedBox(height: 10),
            
                TextField(
                  controller: loanAmountController,
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    hintText: "Enter loan amount (₹)",
                    hintStyle: TextStyle(
                      color: isDark
                          ? AppColors.darkMuted
                          : AppColors.lightTextSecondary,
                    ),
                  ),
                ),
            
                const SizedBox(height: 28),
            
                /// Error Message
                if (_errorMessage != null)
                  Container(
                    padding: const EdgeInsets.all(12),
                    margin: const EdgeInsets.only(bottom: 16),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.red.withOpacity(0.3)),
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.error_outline, color: Colors.red, size: 20),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            _errorMessage!,
                            style: TextStyle(
                              color: Colors.red,
                              fontSize: 14,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
            
                /// Button
                ElevatedButton(
                  onPressed: _isLoading ? null : _handleProceed,
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : const Text(
                          "Proceed",
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                        ),
                ),
            
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Handle proceed button press
  Future<void> _handleProceed() async {
    // Clear previous error
    setState(() {
      _errorMessage = null;
    });

    // Validate inputs
    final aadhaar = aadhaarController.text.trim();
    final pan = panController.text.trim().toUpperCase();
    final loanAmountText = loanAmountController.text.trim();

    if (aadhaar.isEmpty || pan.isEmpty || loanAmountText.isEmpty) {
      setState(() {
        _errorMessage = 'Please fill in all fields';
      });
      return;
    }

    // Validate Aadhaar (12 digits)
    if (aadhaar.length != 12 || !RegExp(r'^\d+$').hasMatch(aadhaar)) {
      setState(() {
        _errorMessage = 'Aadhaar must be exactly 12 digits';
      });
      return;
    }

    
    if (pan.length != 10 || !RegExp(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$').hasMatch(pan)) {
      setState(() {
        _errorMessage = 'Invalid PAN format (e.g., ABCD1234F)';
      });
      return;
    }

    
    final loanAmount = double.tryParse(loanAmountText);
    if (loanAmount == null || loanAmount <= 0) {
      setState(() {
        _errorMessage = 'Please enter a valid loan amount';
      });
      return;
    }

    // Get auth token
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final token = authProvider.token?.accessToken;

    if (token == null) {
      setState(() {
        _errorMessage = 'Authentication required. Please login again.';
      });
      return;
    }

    // Request OTP
    setState(() {
      _isLoading = true;
    });

    try {
      await OTPService.requestOTP(
        token: token,
        aadhaar: aadhaar,
        pan: pan,
        loanAmount: loanAmount,
      );

      // Success - navigate to OTP verification screen
      if (mounted) {
        Navigator.pushReplacementNamed(
          context,
          AppRoutes.verifyOTP,
          arguments: {
            'aadhaar': aadhaar,
            'pan': pan,
            'loanAmount': loanAmount,
          },
        );
      }
    } on ApiException catch (e) {
      setState(() {
        _errorMessage = e.message;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to request OTP: ${e.toString()}';
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    aadhaarController.dispose();
    panController.dispose();
    loanAmountController.dispose();
    super.dispose();
  }
}
