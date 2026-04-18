import 'package:credifyapp/routes/app_routes.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../services/otp_service.dart';
import '../../services/api_client.dart';
import '../../services/storage_service.dart';

class VerifyOtpScreen extends StatefulWidget {
  const VerifyOtpScreen({super.key});

  @override
  State<VerifyOtpScreen> createState() => _VerifyOtpScreenState();
}

class _VerifyOtpScreenState extends State<VerifyOtpScreen> {
  List<TextEditingController> otpControllers =
      List.generate(6, (index) => TextEditingController());
  
  bool _isLoading = false;
  String? _errorMessage;
  
  String? _aadhaar;
  double? _loanAmount;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    
    // Get arguments passed from previous screen
    final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    if (args != null) {
      _aadhaar = args['aadhaar'] as String?;
      _loanAmount = args['loanAmount'] as double?;
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final textColor = theme.textTheme.bodyLarge!.color;

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),
          
              // Top Verify Icon
              Icon(
                Icons.verified_rounded,
                size: 60,
                color: Theme.of(context).primaryColor,
              ),
          
              const SizedBox(height: 25),
          
              // Heading
              Text(
                "Verify Your Account",
                style: theme.textTheme.bodyLarge?.copyWith(
                  fontSize: 26,
                  fontWeight: FontWeight.w600,
                ),
              ),
          
              const SizedBox(height: 30),
          
              // Email Info
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "Enter OTP",
                  style: theme.textTheme.bodyLarge?.copyWith(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              const SizedBox(height: 8),
          
              Text(
                "A 6-digit code has been sent to your registered email",
                style: theme.textTheme.bodyMedium,
              ),
          
              const SizedBox(height: 25),
          
              // OTP Boxes
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: List.generate(6, (index) {
                  return SizedBox(
                    width: 48,
                    height: 55,
                    child: TextField(
                      controller: otpControllers[index],
                      keyboardType: TextInputType.number,
                      textAlign: TextAlign.center,
                      maxLength: 1,
                      style: TextStyle(
                        fontSize: 18,
                        color: textColor,
                        fontWeight: FontWeight.w600,
                      ),
                      decoration: InputDecoration(
                        counterText: "",
                        filled: true,
                        fillColor: Theme.of(context).inputDecorationTheme.fillColor,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      onChanged: (value) {
                        if (value.isNotEmpty && index < 5) {
                          FocusScope.of(context).nextFocus();
                        }
                        if (value.isEmpty && index > 0) {
                          FocusScope.of(context).previousFocus();
                        }
                      },
                    ),
                  );
                }),
              ),
          
              const SizedBox(height: 20),
          
              /// Error Message
              if (_errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  margin: const EdgeInsets.only(top: 16),
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
          
              const Spacer(),
          
              // Verify Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleVerify,
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : const Text("Verify"),
                ),
              ),
          
              const SizedBox(height: 36),
            ],
          ),
        ),
      ),
    );
  }

  /// Handle verify button press
  Future<void> _handleVerify() async {
    // Clear previous error
    setState(() {
      _errorMessage = null;
    });

    // Get OTP from controllers
    final otp = otpControllers.map((c) => c.text).join();

    // Validate OTP
    if (otp.length != 6) {
      setState(() {
        _errorMessage = 'Please enter the complete 6-digit OTP';
      });
      return;
    }

    if (_aadhaar == null) {
      setState(() {
        _errorMessage = 'Aadhaar information missing. Please go back and try again.';
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

    // Verify OTP
    setState(() {
      _isLoading = true;
    });

    try {
      final response = await OTPService.verifyOTP(
        token: token,
        aadhaar: _aadhaar!,
        otp: otp,
      );

      // Success - navigate to dashboard
      if (mounted) {
        // Save loan amount if available
        if (_loanAmount != null) {
          await StorageService.saveLoanAmount(_loanAmount!);
        }

        // Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(response['message'] ?? 'OTP verified successfully'),
            backgroundColor: Colors.green,
            behavior: SnackBarBehavior.floating,
          ),
        );

        // Navigate to dashboard
        Navigator.pushReplacementNamed(context, AppRoutes.dashboard);
      }
    } on ApiException catch (e) {
      setState(() {
        _errorMessage = e.message;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to verify OTP: ${e.toString()}';
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    for (var controller in otpControllers) {
      controller.dispose();
    }
    super.dispose();
  }
}
