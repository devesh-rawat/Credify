import 'package:credifyapp/routes/app_routes.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {

  late AnimationController _controller;
  late Animation<double> _logoScale;
  late Animation<double> _fadeText;
  late Animation<Offset> _slideTagline;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _logoScale = Tween<double>(begin: 0.5, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );

    _fadeText = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: const Interval(0.4, 1.0)),
    );

    _slideTagline = Tween<Offset>(
      begin: const Offset(0, 0.5),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOut),
    );

    _controller.forward();

    // Navigate after animation and auth check
    _navigateAfterDelay();
  }

  Future<void> _navigateAfterDelay() async {
    // Wait for animation to complete
    await Future.delayed(const Duration(seconds: 3));
    
    if (!mounted) return;
    
    // Get the auth provider
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    
    // IMPORTANT: Wait a bit to ensure initialization is complete
    // The initialize() is called in main.dart but might not be finished yet
    await Future.delayed(const Duration(milliseconds: 100));
    
    if (!mounted) return;
    
    // Check authentication state and navigate
    print('🚀 [SplashScreen] Checking auth state...');
    print('🔐 [SplashScreen] isAuthenticated: ${authProvider.isAuthenticated}');
    
    if (authProvider.isAuthenticated) {
      // User is already logged in, go to dashboard
      print('✅ [SplashScreen] Navigating to dashboard');
      Navigator.pushReplacementNamed(context, AppRoutes.dashboard);
    } else {
      // User is not logged in, go to login screen
      print('❌ [SplashScreen] Navigating to login');
      Navigator.pushReplacementNamed(context, AppRoutes.login);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Theme.of(context).scaffoldBackgroundColor,
              Theme.of(context).primaryColorDark,
            ],
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ScaleTransition(
                scale: _logoScale,
                child: Padding(
                  padding: const EdgeInsets.only(bottom: 12.0),
                  child: Image.asset(
                    "assets/images/logo.png",
                    height: 200,
                  ),
                ),
              ),

              FadeTransition(
                opacity: _fadeText,
                child: Text(
                  "Credify",
                  style: GoogleFonts.eagleLake(
                    fontWeight: FontWeight.w900,
                    fontSize: 36,
                  ),
                ),
              ),

              const SizedBox(height: 8),

              SlideTransition(
                position: _slideTagline,
                child: FadeTransition(
                  opacity: _fadeText,
                  child: Text(
                    "See Beyond Documents, Verify Digitally",
                    style: GoogleFonts.eagleLake(fontSize: 16),
                    textAlign: TextAlign.center,
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
