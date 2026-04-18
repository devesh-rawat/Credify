import 'package:flutter/material.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:credifyapp/models/loan_application.dart';
import 'package:credifyapp/services/application_service.dart';
import 'package:credifyapp/services/storage_service.dart';

class LoanApplicationsScreen extends StatefulWidget {
  const LoanApplicationsScreen({super.key});

  @override
  State<LoanApplicationsScreen> createState() => _LoanApplicationsScreenState();
}

class _LoanApplicationsScreenState extends State<LoanApplicationsScreen> {
  List<LoanApplication> _applications = [];
  bool _isLoading = true;
  String? _screenError;
  String _userName = "User";
  // ignore: unused_field
  String _userEmail = "";

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _screenError = null;
    });

    try {
      final token = await StorageService.getToken();
      if (token == null) {
        setState(() {
          _screenError = "Not authenticated";
          _isLoading = false;
        });
        return;
      }

      final name = await StorageService.getFullName();
      final email = await StorageService.getEmail();
      
      if (mounted) {
        setState(() {
          if (name != null) _userName = name;
          if (email != null) _userEmail = email;
        });
      }

      final apps = await ApplicationService.fetchMyApplications(token);
      
      if (mounted) {
        setState(() {
          _applications = apps;
          _isLoading = false;
        });
      }
    } catch (e) {
      print("Error loading applications: $e");
      if (mounted) {
        setState(() {
          _screenError = "Failed to load applications";
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _loadData,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Back Button + Title
                Row(
                  children: [
                    IconButton(
                      icon: Icon(
                        Icons.arrow_back,
                        color: isDark ? AppColors.darkText : AppColors.lightText,
                      ),
                      onPressed: () => Navigator.pop(context),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      "Your Loan Applications",
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: isDark ? AppColors.darkText : AppColors.lightText,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 10),

                // Count badge
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                    color: AppColors.lightPrimaryBlue.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    "${_applications.length} Application${_applications.length != 1 ? "s" : ""}",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: AppColors.lightPrimaryBlue,
                    ),
                  ),
                ),

                const SizedBox(height: 20),

                // Loading / Error / Empty / List
                if (_isLoading)
                  const Center(child: CircularProgressIndicator())
                else if (_screenError != null)
                  Center(
                    child: Column(
                      children: [
                        const Icon(Icons.error_outline, size: 48, color: Colors.red),
                        const SizedBox(height: 16),
                        Text(_screenError!, style: const TextStyle(color: Colors.red)),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadData,
                          child: const Text("Retry"),
                        ),
                      ],
                    ),
                  )
                else if (_applications.isEmpty)
                  _buildEmptyState(isDark)
                else
                  ListView.builder(
                    shrinkWrap: true,
                    itemCount: _applications.length,
                    physics: const NeverScrollableScrollPhysics(),
                    itemBuilder: (context, index) {
                      return _buildApplicationCard(_applications[index], isDark);
                    },
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // -----------------------------------------------------
  // EMPTY STATE
  // -----------------------------------------------------
  Widget _buildEmptyState(bool isDark) {
    return Container(
      padding: const EdgeInsets.all(26),
      margin: const EdgeInsets.only(top: 40),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(22),
        boxShadow: [
          BoxShadow(
            blurRadius: 12,
            color: isDark ? Colors.black26 : Colors.grey.shade300,
          )
        ],
      ),
      child: Column(
        children: [
          const Icon(Icons.folder_open_outlined, size: 80, color: Colors.grey),
          const SizedBox(height: 20),
          Text(
            "No Applications Yet",
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: isDark ? AppColors.darkText : AppColors.lightText,
            ),
          ),
          const SizedBox(height: 10),
          Text(
            "Start by generating your Credify score and apply for loans.",
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Go to Dashboard"),
          ),
        ],
      ),
    );
  }

  // -----------------------------------------------------
  // APPLICATION CARD
  // -----------------------------------------------------
  Widget _buildApplicationCard(LoanApplication app, bool isDark) {
    final String status = app.status;

    return Container(
      margin: const EdgeInsets.only(bottom: 18),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Theme.of(context).cardColor,
            AppColors.lightPrimaryBlue.withOpacity(0.07),
          ],
        ),
        borderRadius: BorderRadius.circular(22),
        border: Border.all(
          color: AppColors.lightPrimaryBlue.withOpacity(0.14),
        ),
        boxShadow: [
          BoxShadow(
            blurRadius: 12,
            color: isDark ? Colors.black38 : Colors.grey.shade200,
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // TOP ROW
          Row(
            children: [
              CircleAvatar(
                radius: 26,
                backgroundColor: AppColors.lightPrimaryBlue,
                child: Text(
                  _getInitials(_userName),
                  style: const TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),
              const SizedBox(width: 14),

              // Application ID
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("Application ID",
                        style: TextStyle(
                          color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                          fontSize: 12,
                        )),
                    const SizedBox(height: 4),
                    Text(
                      app.applicationId,
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14, // Slightly smaller for long IDs
                        fontFamily: "monospace",
                        color: isDark ? AppColors.darkText : AppColors.lightText,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),

              // STATUS CHIP
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                decoration: BoxDecoration(
                  color: _statusColor(status),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  status,
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ),
            ],
          ),

          const SizedBox(height: 18),

          // GRID → Score, Amount
          Row(
            children: [
              _smallInfoBox("Trust Score", app.score.toInt().toString(), AppColors.lightPrimaryBlue, isDark),
              const SizedBox(width: 12),
              _smallInfoBox("Amount", "₹ ${app.amount.toInt()}", isDark ? AppColors.darkText : AppColors.lightText, isDark),
            ],
          ),

          const SizedBox(height: 18),

          // APPLICANT DETAILS
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: isDark ? AppColors.darkInput : AppColors.lightCard,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _detail("Applicant", app.userName.isNotEmpty ? app.userName : _userName),
                if (app.purpose.isNotEmpty)
                  _detail("Purpose", app.purpose),

                if (status == "PENDING")
                  _infoMessage("⏳ Your application is under review.", isDark),
                if (status == "APPROVE" || status == "APPROVED")
                  _successMessage("✅ Congratulations! Your loan has been approved.", isDark),
                if (status == "APPROVE_WITH_CONDITIONS")
                  _successMessage("⚠️ Approved with conditions. Check email.", isDark),
                if (status == "REJECT" || status == "REJECTED")
                  _errorMessage("❌ Your application was not approved.", isDark),
              ],
            ),
          )
        ],
      ),
    );
  }

  // SMALL ITEMS ---------------------------------------------------

  Widget _smallInfoBox(String title, String value, Color color, bool isDark) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(14),
          boxShadow: [
            BoxShadow(
              blurRadius: 6,
              color: isDark ? Colors.black26 : Colors.grey.shade200,
            )
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title,
                style: TextStyle(
                  fontSize: 11,
                  color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                )),
            const SizedBox(height: 4),
            Text(
              value,
              style: TextStyle(
                fontSize: 18, // Adjusted size
                fontWeight: FontWeight.bold,
                color: color,
              ),
              overflow: TextOverflow.ellipsis,
            )
          ],
        ),
      ),
    );
  }



  Widget _detail(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: RichText(
        text: TextSpan(
          children: [
            TextSpan(
              text: "$label: ",
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: AppColors.lightPrimaryBlue,
              ),
            ),
            TextSpan(
              text: value,
              style: const TextStyle(
                color: Colors.grey, // Adjusted for visibility
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _infoMessage(String text, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 12,
          fontStyle: FontStyle.italic,
          color: isDark ? AppColors.darkMuted : Colors.grey.shade600,
        ),
      ),
    );
  }

  Widget _successMessage(String text, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.green,
        ),
      ),
    );
  }

  Widget _errorMessage(String text, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.red,
        ),
      ),
    );
  }

  // UTILS ---------------------------------------------------

  Color _statusColor(String status) {
    if (status == "APPROVE" || status == "APPROVED") return Colors.green;
    if (status == "APPROVE_WITH_CONDITIONS") return Colors.orange;
    if (status == "PENDING") return Colors.blue;
    return Colors.red;
  }

  String _getInitials(String name) {
    final parts = name.split(" ");
    if (parts.isEmpty) return "";
    return parts.map((e) => e.isNotEmpty ? e[0] : "").take(2).join().toUpperCase();
  }
}
