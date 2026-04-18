import 'package:credifyapp/models/user_profile_model.dart';
import 'package:credifyapp/models/bank_account_model.dart';
import 'package:credifyapp/providers/auth_provider.dart';
import 'package:credifyapp/services/auth_service.dart';
import 'package:flutter/material.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:provider/provider.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  UserProfile? _userProfile;
  List<BankAccount>? _bankAccounts;
  bool _isLoading = true;
  bool _isLoadingAccounts = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadUserProfile();
  }

  Future<void> _loadUserProfile() async {
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

      final profile = await AuthService.getUserProfile(token);
      setState(() {
        _userProfile = profile;
        _isLoading = false;
      });

      // If user has KYC, fetch bank accounts
      if (profile.hasKyc()) {
        _loadBankAccounts(token);
      }
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
        displayMessage = 'Failed to load profile';
      }
      
      setState(() {
        _errorMessage = displayMessage;
        _isLoading = false;
      });
    }
  }

  Future<void> _loadBankAccounts(String token) async {
    setState(() {
      _isLoadingAccounts = true;
    });

    try {
      final accounts = await AuthService.getUserBankAccounts(token);
      setState(() {
        _bankAccounts = accounts;
        _isLoadingAccounts = false;
      });
    } catch (e) {
      print('❌ [ProfileScreen] Failed to load bank accounts: $e');
      setState(() {
        _bankAccounts = [];
        _isLoadingAccounts = false;
      });
    }
  }

  Future<void> _handleLogout() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    await authProvider.logout(context);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    if (_isLoading) {
      return Scaffold(
        backgroundColor:
            isDark ? AppColors.darkBackground : AppColors.lightBackground,
        appBar: AppBar(
          elevation: 0,
          title: Text(
            "Profile",
            style: TextStyle(
              color: isDark ? AppColors.darkText : AppColors.lightText,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        body: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (_errorMessage != null) {
      final isNetworkError = _errorMessage == 'No internet connection';
      
      return Scaffold(
        backgroundColor:
            isDark ? AppColors.darkBackground : AppColors.lightBackground,
        appBar: AppBar(
          elevation: 0,
          title: Text(
            "Profile",
            style: TextStyle(
              color: isDark ? AppColors.darkText : AppColors.lightText,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(20),
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
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  isNetworkError 
                      ? 'Please check your connection and try again'
                      : 'Something went wrong',
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  onPressed: _loadUserProfile,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Retry'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    final profile = _userProfile!;
    final hasKyc = profile.hasKyc();

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.darkBackground : AppColors.lightBackground,

      appBar: AppBar(
        elevation: 0,
        title: Text(
          "Profile",
          style: TextStyle(
            color: isDark ? AppColors.darkText : AppColors.lightText,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),

      body: SingleChildScrollView(
        child: Column(
          children: [
            // ----- Top Section with Avatar -----
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 30),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: isDark
                      ? [
                          AppColors.darkPrimaryBlue,
                          AppColors.darkAccentBlue,
                        ]
                      : [
                          AppColors.lightPrimaryBlue,
                          AppColors.lightPrimaryBlue.withOpacity(0.7),
                        ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(28),
                  bottomRight: Radius.circular(28),
                ),
              ),

              child: Column(
                children: [
                  CircleAvatar(
                    radius: 48,
                    backgroundColor: Colors.white,
                    child: Icon(
                      Icons.person,
                      size: 50,
                      color: isDark
                          ? AppColors.darkPrimaryBlue
                          : AppColors.lightPrimaryBlue,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    profile.fullName,
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 6),

                  // Email
                  Text(
                    profile.email,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.white.withOpacity(0.95),
                    ),
                  ),

                  const SizedBox(height: 12),

                  // Aadhaar Number
                  Text(
                    "Aadhaar: ${profile.getFormattedAadhaar()}",
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.white.withOpacity(0.95),
                    ),
                  ),

                  const SizedBox(height: 6),

                  // PAN Number
                  Text(
                    "PAN: ${profile.getFormattedPan()}",
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.white.withOpacity(0.95),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // ----- KYC Status Card -----
            _buildCard(
              title: "KYC Status",
              value: hasKyc ? "Verified" : "Not Verified",
              icon: hasKyc ? Icons.verified_rounded : Icons.warning_rounded,
              isDark: isDark,
              valueColor: hasKyc ? Colors.green : Colors.orange,
            ),

            // ----- Bank Accounts Section -----
            if (hasKyc) ...[
              _buildSectionHeader("Linked Bank Accounts", isDark),
              if (_isLoadingAccounts)
                const Padding(
                  padding: EdgeInsets.all(20),
                  child: Center(child: CircularProgressIndicator()),
                )
              else if (_bankAccounts == null || _bankAccounts!.isEmpty)
                _buildEmptyAccountsCard(isDark)
              else
                ..._bankAccounts!.map((account) => _buildBankTile(
                      account.bankName,
                      account.getMaskedAccountNumber(),
                      account.getAccountTypeDisplay(),
                      isDark,
                    )),
            ] else ...[
              const SizedBox(height: 20),
              _buildKycWarningCard(isDark),
            ],

            const SizedBox(height: 20),

            // ----- Logout Button -----
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                children: [
                  _buildButton(
                    text: "Log Out",
                    icon: Icons.logout,
                    isDark: isDark,
                    color: Colors.red,
                    onTap: _handleLogout,
                  ),
                ],
              ),
            ),

            const SizedBox(height: 35),
          ],
        ),
      ),
    );
  }

  // ----- EMPTY ACCOUNTS CARD -----
  Widget _buildEmptyAccountsCard(bool isDark) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Icon(
            Icons.account_balance_outlined,
            size: 28,
            color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              "No bank accounts linked",
              style: TextStyle(
                fontSize: 15,
                color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ----- KYC WARNING CARD -----
  Widget _buildKycWarningCard(bool isDark) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: Colors.orange.withOpacity(0.5),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.info_outline,
            size: 28,
            color: Colors.orange,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "KYC Not Completed",
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: isDark ? AppColors.darkText : AppColors.lightText,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  "Complete KYC verification to view bank accounts",
                  style: TextStyle(
                    fontSize: 13,
                    color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ----- CREDIT / KYC CARD -----
  Widget _buildCard({
    required String title,
    required String value,
    required IconData icon,
    required bool isDark,
    Color? valueColor,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(16),
      ),

      child: Row(
        children: [
          Icon(icon,
              size: 28,
              color: valueColor ??
                  (isDark
                      ? AppColors.darkAccentBlue
                      : AppColors.lightPrimaryBlue)),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              title,
              style: TextStyle(
                fontSize: 16,
                color:
                    isDark ? AppColors.darkText : AppColors.lightText,
              ),
            ),
          ),
          Text(
            value,
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: valueColor ??
                  (isDark
                      ? AppColors.darkPrimaryBlue
                      : AppColors.lightPrimaryBlue),
            ),
          ),
        ],
      ),
    );
  }

  // ----- SECTION HEADER -----
  Widget _buildSectionHeader(String title, bool isDark) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 18, 20, 6),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 15,
          color:
              isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  // ----- BANK ACCOUNT TILE -----
  Widget _buildBankTile(String bank, String number, String accountType, bool isDark) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(14),
      ),

      child: Row(
        children: [
          Icon(Icons.account_balance_rounded,
              size: 28,
              color: isDark
                  ? AppColors.darkAccentBlue
                  : AppColors.lightPrimaryBlue),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  bank,
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                    color:
                        isDark ? AppColors.darkText : AppColors.lightText,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  accountType,
                  style: TextStyle(
                    fontSize: 12,
                    color: isDark
                        ? AppColors.darkMuted
                        : AppColors.lightTextSecondary,
                  ),
                ),
              ],
            ),
          ),
          Text(
            number,
            style: TextStyle(
              fontSize: 14,
              color: isDark
                  ? AppColors.darkMuted
                  : AppColors.lightTextSecondary,
            ),
          ),
        ],
      ),
    );
  }

  // ----- SINGLE BUTTON -----
  Widget _buildButton({
    required String text,
    required IconData icon,
    required VoidCallback onTap,
    required bool isDark,
    Color? color,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),

      child: Container(
        height: 55,
        decoration: BoxDecoration(
          color: color ??
              (isDark
                  ? AppColors.darkPrimaryBlue
                  : AppColors.lightPrimaryBlue),
          borderRadius: BorderRadius.circular(14),
        ),

        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: Colors.white, size: 22),
            const SizedBox(width: 8),
            Text(
              text,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
