
import 'package:credifyapp/theme/theme.dart';
import 'package:credifyapp/models/credit_score_model.dart';
import 'package:credifyapp/services/score_service.dart';
import 'package:credifyapp/services/storage_service.dart';
import 'package:credifyapp/routes/app_routes.dart';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';


class ScoreScreen extends StatefulWidget {
  const ScoreScreen({super.key});

  @override
  State<ScoreScreen> createState() => _ScoreScreenState();
}

class _ScoreScreenState extends State<ScoreScreen> {
  CreditScore? _creditScore;
  bool _isLoading = true;
  String? _errorMessage;
  // ignore: unused_field
  String _userName = 'User';

  @override
  void initState() {
    super.initState();
    _loadScoreData();
  }

  Future<void> _loadScoreData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      // Get token from storage
      final token = await StorageService.getToken();
      if (token == null) {
        setState(() {
          _errorMessage = 'Not authenticated';
          _isLoading = false;
        });
        return;
      }

      // Get user name from storage
      final fullName = await StorageService.getFullName();
      if (fullName != null) {
        setState(() {
          _userName = fullName;
        });
      }

      // Fetch credit score
      final score = await ScoreService.fetchUserScore(token);
      
      setState(() {
        _creditScore = score;
        _isLoading = false;
      });
    } catch (e) {
      print('❌ [ScoreScreen] Error loading score: $e');
      setState(() {
        _errorMessage = 'Failed to load credit score';
        _isLoading = false;
      });
    }
  }

  pw.Widget _buildMarkdownPdfText(String text, {double fontSize = 12}) {
    final List<pw.InlineSpan> spans = [];
    final RegExp boldPattern = RegExp(r'\*\*(.*?)\*\*');
    
    int lastMatchEnd = 0;
    for (final match in boldPattern.allMatches(text)) {
      if (match.start > lastMatchEnd) {
        spans.add(pw.TextSpan(
          text: text.substring(lastMatchEnd, match.start),
          style: pw.TextStyle(fontSize: fontSize),
        ));
      }
      
      spans.add(pw.TextSpan(
        text: match.group(1),
        style: pw.TextStyle(fontSize: fontSize, fontWeight: pw.FontWeight.bold),
      ));
      
      lastMatchEnd = match.end;
    }
    
    if (lastMatchEnd < text.length) {
      spans.add(pw.TextSpan(
        text: text.substring(lastMatchEnd),
        style: pw.TextStyle(fontSize: fontSize),
      ));
    }
    
    return pw.RichText(
      text: pw.TextSpan(children: spans),
      textAlign: pw.TextAlign.justify,
    );
  }

  Future<void> _saveScreenAsPDF() async {
    if (_creditScore == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No credit score data available'),
          duration: Duration(seconds: 2),
        ),
      );
      return;
    }

    try {
      print('📄 [ScoreScreen] Generating PDF from data...');
      
      final score = _creditScore!;
      final pdf = pw.Document();

      // Add page with credit score report
      pdf.addPage(
        pw.MultiPage(
          pageFormat: PdfPageFormat.a4,
          margin: const pw.EdgeInsets.all(32),
          build: (pw.Context context) {
            return [
              // Header
              pw.Header(
                level: 0,
                child: pw.Text(
                  'Credit Score Report',
                  style: pw.TextStyle(
                    fontSize: 28,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
              ),
              
              pw.SizedBox(height: 20),
              
              // User Info
              pw.Row(
                mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                children: [
                  pw.Text(
                    'Name: $_userName',
                    style: const pw.TextStyle(fontSize: 14),
                  ),
                  pw.Text(
                    'Date: ${DateTime.now().day}/${DateTime.now().month}/${DateTime.now().year}',
                    style: const pw.TextStyle(fontSize: 14),
                  ),
                ],
              ),
              
              pw.SizedBox(height: 30),
              
              // Credit Score Box
              pw.Container(
                padding: const pw.EdgeInsets.all(20),
                decoration: pw.BoxDecoration(
                  border: pw.Border.all(color: PdfColors.grey400, width: 2),
                  borderRadius: const pw.BorderRadius.all(pw.Radius.circular(8)),
                ),
                child: pw.Column(
                  children: [
                    pw.Text(
                      'Credit Score',
                      style: pw.TextStyle(
                        fontSize: 16,
                        fontWeight: pw.FontWeight.bold,
                      ),
                    ),
                    pw.SizedBox(height: 10),
                    pw.Text(
                      '${score.creditScore}',
                      style: pw.TextStyle(
                        fontSize: 48,
                        fontWeight: pw.FontWeight.bold,
                      ),
                    ),
                    pw.Text(
                      'out of 900',
                      style: const pw.TextStyle(fontSize: 14, color: PdfColors.grey700),
                    ),
                    pw.SizedBox(height: 10),
                    pw.Container(
                      padding: const pw.EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                      decoration: pw.BoxDecoration(
                        color: PdfColors.grey300,
                        borderRadius: const pw.BorderRadius.all(pw.Radius.circular(4)),
                      ),
                      child: pw.Text(
                        '${score.riskLabel} Risk',
                        style: pw.TextStyle(
                          fontSize: 14,
                          fontWeight: pw.FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              
              pw.SizedBox(height: 30),
              
              // Metrics Section
              pw.Text(
                'Key Metrics',
                style: pw.TextStyle(
                  fontSize: 18,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.SizedBox(height: 10),
              
              pw.Table(
                border: pw.TableBorder.all(color: PdfColors.grey400),
                children: [
                  pw.TableRow(
                    decoration: const pw.BoxDecoration(color: PdfColors.grey300),
                    children: [
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Metric', style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                      ),
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Value', style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                      ),
                    ],
                  ),
                  pw.TableRow(
                    children: [
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Creditworthiness'),
                      ),
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('${score.creditScore} / 900'),
                      ),
                    ],
                  ),
                  pw.TableRow(
                    children: [
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Payment Discipline'),
                      ),
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text(score.getPaymentDisciplinePercent()),
                      ),
                    ],
                  ),
                  pw.TableRow(
                    children: [
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Default Probability'),
                      ),
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('${(score.defaultProbability * 100).toStringAsFixed(1)}%'),
                      ),
                    ],
                  ),
                  pw.TableRow(
                    children: [
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text('Recommendation'),
                      ),
                      pw.Padding(
                        padding: const pw.EdgeInsets.all(8),
                        child: pw.Text(score.recommendation),
                      ),
                    ],
                  ),
                ],
              ),
              
              pw.SizedBox(height: 30),
              
              // AI Insights
              if (score.summary.isNotEmpty) ...[
                pw.Text(
                  'AI Insights',
                  style: pw.TextStyle(
                    fontSize: 18,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
                pw.SizedBox(height: 10),
                pw.Container(
                  padding: const pw.EdgeInsets.all(12),
                  decoration: pw.BoxDecoration(
                    color: PdfColors.blue50,
                    borderRadius: const pw.BorderRadius.all(pw.Radius.circular(4)),
                  ),
                  child: _buildMarkdownPdfText(score.summary, fontSize: 12),
                ),
                pw.SizedBox(height: 20),
              ],
              
              // Key Factors
              if (score.keyFactors.isNotEmpty) ...[
                pw.Text(
                  'Key Factors',
                  style: pw.TextStyle(
                    fontSize: 18,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
                pw.SizedBox(height: 10),
                ...score.keyFactors.map((factor) => pw.Padding(
                  padding: const pw.EdgeInsets.only(bottom: 6),
                  child: pw.Row(
                    crossAxisAlignment: pw.CrossAxisAlignment.start,
                    children: [
                      pw.Text('• ', style: const pw.TextStyle(fontSize: 12)),
                      pw.Expanded(
                        child: _buildMarkdownPdfText(factor, fontSize: 12),
                      ),
                    ],
                  ),
                )),
                pw.SizedBox(height: 20),
              ],
              
              // Recommendations
              if (score.recommendations.isNotEmpty) ...[
                pw.Text(
                  'Recommendations',
                  style: pw.TextStyle(
                    fontSize: 18,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
                pw.SizedBox(height: 10),
                ...score.recommendations.map((recommendation) => pw.Padding(
                  padding: const pw.EdgeInsets.only(bottom: 6),
                  child: pw.Row(
                    crossAxisAlignment: pw.CrossAxisAlignment.start,
                    children: [
                      pw.Text('• ', style: const pw.TextStyle(fontSize: 12)),
                      pw.Expanded(
                        child: _buildMarkdownPdfText(recommendation, fontSize: 12),
                      ),
                    ],
                  ),
                )),
                pw.SizedBox(height: 20),
              ],
              
              // Footer
              pw.SizedBox(height: 30),
              pw.Divider(),
              pw.SizedBox(height: 10),
              pw.Text(
                'This report was generated on ${DateTime.now().day}/${DateTime.now().month}/${DateTime.now().year} at ${DateTime.now().hour}:${DateTime.now().minute.toString().padLeft(2, '0')}',
                style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700),
                textAlign: pw.TextAlign.center,
              ),
            ];
          },
        ),
      );

      print('✅ [ScoreScreen] PDF created, opening share dialog...');

      // Show share/save dialog
      await Printing.sharePdf(
        bytes: await pdf.save(),
        filename: 'credit_score_report_${_userName.replaceAll(' ', '_')}_${DateTime.now().millisecondsSinceEpoch}.pdf',
      );

      print('✅ [ScoreScreen] PDF shared successfully');
      
    } catch (e) {
      print('❌ [ScoreScreen] Error saving PDF: $e');
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error saving PDF: $e'),
          duration: const Duration(seconds: 3),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;


    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: SafeArea(
        child: _isLoading
            ? _buildLoadingState()
            : _creditScore == null
                ? _buildNoScoreState(isDark)
                : _buildScoreContent(isDark),
      ),
    );
  }

  Widget _buildLoadingState() {
    return const Center(
      child: CircularProgressIndicator(),
    );
  }

  Widget _buildNoScoreState(bool isDark) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.credit_score_outlined,
              size: 80,
              color: Theme.of(context).textTheme.bodyMedium!.color,
            ),
            const SizedBox(height: 20),
            Text(
              _errorMessage ?? 'No Credit Score Available',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Theme.of(context).textTheme.bodyLarge!.color,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(
              'Complete the verification process to get your credit score',
              style: TextStyle(
                fontSize: 14,
                color: Theme.of(context).textTheme.bodyMedium!.color,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              onPressed: _loadScoreData,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
              style: ElevatedButton.styleFrom(
                backgroundColor: isDark
                    ? AppColors.darkAccentBlue
                    : AppColors.lightPrimaryBlue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildScoreContent(bool isDark) {
    final score = _creditScore!;

    return RefreshIndicator(
      onRefresh: _loadScoreData,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Heading
            Text(
              "Credit Score Report",
              style: TextStyle(
                color: Theme.of(context).textTheme.bodyLarge!.color,
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 20),

            // Creditworthiness Card
            Container(
              width: double.infinity,
              padding:
                  const EdgeInsets.symmetric(horizontal: 18, vertical: 18),
              decoration: BoxDecoration(
                color: isDark ? AppColors.darkCard : AppColors.lightCard,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Your Creditworthiness",
                    style: TextStyle(
                      color: Theme.of(context).textTheme.bodyMedium!.color,
                    ),
                  ),
                  const SizedBox(height: 6),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            score.creditScore.toString(),
                            style: TextStyle(
                              fontSize: 32,
                              fontWeight: FontWeight.bold,
                              color: isDark
                                  ? AppColors.darkAccentBlue
                                  : AppColors.lightPrimaryBlue,
                            ),
                          ),
                          Text(
                            " / 900",
                            style: TextStyle(
                              fontSize: 14,
                              color:
                                  Theme.of(context).textTheme.bodyMedium!.color,
                            ),
                          ),
                        ],
                      ),

                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: score.getScoreColor().withOpacity(0.15),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Icon(
                          score.creditScore >= 650
                              ? Icons.trending_up
                              : Icons.trending_down,
                          color: score.getScoreColor(),
                        ),
                      ),
                    ],
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // Risk Label Badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 6),
                    decoration: BoxDecoration(
                      color: score.getScoreColor().withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      "${score.riskLabel} Risk",
                      style: TextStyle(
                        color: score.getScoreColor(),
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 25),

            // Payment Discipline Metric
            _metricCard(
              context,
              icon: Icons.payment,
              title: "Payment Discipline",
              value: score.getPaymentDisciplinePercent(),
            ),

            const SizedBox(height: 25),

            // AI Summary Section
            if (score.summary.isNotEmpty) ...[
              Text(
                "AI Insights",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).textTheme.bodyLarge!.color,
                ),
              ),
              const SizedBox(height: 12),
              _infoCard(
                context,
                icon: Icons.auto_awesome,
                text: score.summary,
                isDark: isDark,
              ),
              const SizedBox(height: 20),
            ],

            // Key Factors Section
            if (score.keyFactors.isNotEmpty) ...[
              Text(
                "Key Factors",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).textTheme.bodyLarge!.color,
                ),
              ),
              const SizedBox(height: 12),
              ...score.keyFactors.map((factor) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: _infoCard(
                      context,
                      icon: Icons.check_circle_outline,
                      text: factor,
                      isDark: isDark,
                      iconColor: isDark
                          ? AppColors.darkAccentBlue
                          : AppColors.lightPrimaryBlue,
                    ),
                  )),
              const SizedBox(height: 20),
            ],

            // Recommendations Section
            if (score.recommendations.isNotEmpty) ...[
              Text(
                "Recommendations",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).textTheme.bodyLarge!.color,
                ),
              ),
              const SizedBox(height: 12),
              ...score.recommendations.map((recommendation) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: _infoCard(
                      context,
                      icon: Icons.lightbulb_outline,
                      text: recommendation,
                      isDark: isDark,
                      iconColor: Colors.amber,
                    ),
                  )),
              const SizedBox(height: 20),
            ],

            // Account Info
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: isDark ? AppColors.darkCard : AppColors.lightCard,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Score Details",
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Theme.of(context).textTheme.bodyLarge!.color,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Recommendation:",
                        style: TextStyle(
                          color: Theme.of(context).textTheme.bodyMedium!.color,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: score.recommendation == 'APPROVE'
                              ? Colors.green.withOpacity(0.2)
                              : score.recommendation == 'REJECT'
                                  ? Colors.red.withOpacity(0.2)
                                  : Colors.orange.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          score.recommendation,
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            color: score.recommendation == 'APPROVE'
                                ? Colors.green
                                : score.recommendation == 'REJECT'
                                    ? Colors.red
                                    : Colors.orange,
                          ),
                        ),
                      ),
                    ],
                  ),
                  if (score.createdAt != null) ...[
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          "Last Updated:",
                          style: TextStyle(
                            color:
                                Theme.of(context).textTheme.bodyMedium!.color,
                          ),
                        ),
                        Text(
                          "${score.createdAt!.day}/${score.createdAt!.month}/${score.createdAt!.year}",
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            color:
                                Theme.of(context).textTheme.bodyLarge!.color,
                          ),
                        ),
                      ],
                    ),
                  ],
                ],
              ),
            ),

            const SizedBox(height: 30),

            // Action Buttons Row
            Row(
              children: [
                // Download Report Button
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      await _saveScreenAsPDF();
                    },
                    icon: const Icon(Icons.download),
                    label: const Text('Save as PDF'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isDark
                          ? AppColors.darkAccentBlue
                          : AppColors.lightPrimaryBlue,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
                
                const SizedBox(width: 12),
                
                // Regenerate Report Button
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      // Navigate to consent screen to restart the flow
                      Navigator.pushNamed(context, AppRoutes.consent);
                    },
                    icon: Icon(
                      Icons.refresh,
                      color: isDark
                          ? AppColors.darkAccentBlue
                          : AppColors.lightPrimaryBlue,
                    ),
                    label: Text(
                      'Regenerate',
                      style: TextStyle(
                        color: isDark
                            ? AppColors.darkAccentBlue
                            : AppColors.lightPrimaryBlue,
                      ),
                    ),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      side: BorderSide(
                        color: isDark
                            ? AppColors.darkAccentBlue
                            : AppColors.lightPrimaryBlue,
                        width: 1.5,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 25),
          ],
        ),
      ),
    );
  }

  Widget _metricCard(BuildContext context,
      {required IconData icon,
      required String title,
      required String value}) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isDark
                  ? Colors.white.withOpacity(0.07)
                  : Colors.blue.withOpacity(0.08),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon,
                size: 28,
                color: isDark
                    ? AppColors.darkAccentBlue
                    : AppColors.lightPrimaryBlue),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: Theme.of(context).textTheme.bodyMedium!.color,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: TextStyle(
                    color: Theme.of(context).textTheme.bodyLarge!.color,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget _infoCard(
    BuildContext context, {
    required IconData icon,
    required String text,
    required bool isDark,
    Color? iconColor,
  }) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightCard,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            icon,
            size: 24,
            color: iconColor ??
                (isDark
                    ? AppColors.darkAccentBlue
                    : AppColors.lightPrimaryBlue),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: MarkdownBody(
              data: text,
              styleSheet: MarkdownStyleSheet(
                p: TextStyle(
                  fontSize: 14,
                  color: Theme.of(context).textTheme.bodyMedium!.color,
                  height: 1.4,
                ),
                strong: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
