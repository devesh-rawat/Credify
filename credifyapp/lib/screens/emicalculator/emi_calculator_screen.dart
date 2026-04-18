import 'dart:math';
import 'package:flutter/material.dart';
import 'package:credifyapp/theme/theme.dart';

class EmiCalculatorScreen extends StatefulWidget {
  const EmiCalculatorScreen({super.key});

  @override
  State<EmiCalculatorScreen> createState() => _EmiCalculatorScreenState();
}

class _EmiCalculatorScreenState extends State<EmiCalculatorScreen> {
  double loanAmount = 500000;
  int loanTenure = 10;
  double interestRate = 10;
  
  final TextEditingController _loanAmountController = TextEditingController();
  
  @override
  void initState() {
    super.initState();
    _loanAmountController.text = loanAmount.toStringAsFixed(0);
  }
  
  @override
  void dispose() {
    _loanAmountController.dispose();
    super.dispose();
  }

  double calculateEMI() {
    double principal = loanAmount;
    double monthlyRate = interestRate / (12 * 100);
    int months = loanTenure * 12;

    double emi =
        principal * monthlyRate * pow((1 + monthlyRate), months) /
            (pow((1 + monthlyRate), months) - 1);

    return emi.isFinite ? emi : 0;
  }

  double calculateTotalInterest() {
    double emi = calculateEMI();
    int months = loanTenure * 12;
    return (emi * months) - loanAmount;
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final emi = calculateEMI();
    final totalInterest = calculateTotalInterest();
    final totalPayment = totalInterest + loanAmount;

    final principalPercentage = (loanAmount / totalPayment) * 100;
    final interestPercentage = 100 - principalPercentage;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          "EMI Calculator",
          style: TextStyle(
            color: isDark ? AppColors.darkText : AppColors.lightText,
          ),
        ),
        backgroundColor:
            isDark ? AppColors.darkBackground : AppColors.lightBackground,
        iconTheme: IconThemeData(
          color: isDark ? AppColors.darkText : AppColors.lightText,
        ),
        elevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              
              // Back button
      
             

              const SizedBox(height: 20),

              /// Input Section
              _buildInputCard(isDark),

              const SizedBox(height: 28),

              /// Result Section
              _buildResultCard(
                isDark,
                emi,
                totalInterest,
                totalPayment,
                principalPercentage,
                interestPercentage,
              ),
            ],
          ),
        ),
      ),
    );
  }

  // -------------------------------------------------------
  //                   INPUT SECTION (MOBILE)
  // -------------------------------------------------------
  Widget _buildInputCard(bool isDark) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: isDark ? Colors.black26 : Colors.grey.shade300,
            blurRadius: 10,
            spreadRadius: 1,
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _label("Loan Amount", isDark),
          _editableAmountField(isDark),

          Slider(
            min: 0,
            max: 1500000,
            divisions: 150,
            value: loanAmount,
            onChanged: (v) {
              setState(() {
                loanAmount = v;
                _loanAmountController.text = v.toStringAsFixed(0);
              });
            },
            activeColor: AppColors.lightPrimaryBlue,
            inactiveColor: isDark ? AppColors.darkMuted : Colors.grey.shade300,
          ),

          const SizedBox(height: 24),

          _label("Loan Tenure (Years)", isDark),
          _displayBox("$loanTenure Years", isDark),

          Slider(
            min: 1,
            max: 30,
            divisions: 30,
            value: loanTenure.toDouble(),
            onChanged: (v) => setState(() => loanTenure = v.toInt()),
            activeColor: AppColors.lightPrimaryBlue,
            inactiveColor: isDark ? AppColors.darkMuted : Colors.grey.shade300,
          ),

          const SizedBox(height: 24),

          _label("Interest Rate (%)", isDark),
          _displayBox("${interestRate.toStringAsFixed(1)} %", isDark),

          Slider(
            min: 1,
            max: 25,
            divisions: 48,
            value: interestRate,
            onChanged: (v) => setState(() => interestRate = v),
            activeColor: AppColors.lightPrimaryBlue,
            inactiveColor: isDark ? AppColors.darkMuted : Colors.grey.shade300,
          ),
        ],
      ),
    );
  }

  Widget _label(String text, bool isDark) {
    return Text(
      text,
      style: TextStyle(
        fontSize: 15,
        fontWeight: FontWeight.bold,
        color: isDark ? AppColors.darkText : AppColors.lightText,
      ),
    );
  }

  Widget _displayBox(String value, bool isDark) {
    return Container(
      margin: const EdgeInsets.only(top: 10, bottom: 12),
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 14),
      width: double.infinity,
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkInput : AppColors.lightInput,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        value,
        textAlign: TextAlign.right,
        style: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: isDark ? AppColors.darkText : AppColors.lightText,
        ),
      ),
    );
  }
  
  Widget _editableAmountField(bool isDark) {
    return Container(
      margin: const EdgeInsets.only(top: 10, bottom: 12),
      padding: const EdgeInsets.symmetric(horizontal: 14),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkInput : AppColors.lightInput,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: AppColors.lightPrimaryBlue.withOpacity(0.3),
          width: 1.5,
        ),
      ),
      child: TextField(
        controller: _loanAmountController,
        keyboardType: TextInputType.number,
        textAlign: TextAlign.right,
        style: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: isDark ? AppColors.darkText : AppColors.lightText,
        ),
        decoration: InputDecoration(
          border: InputBorder.none,
          prefixText: '₹ ',
          prefixStyle: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
          ),
          hintText: '500000',
          hintStyle: TextStyle(
            color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
          ),
        ),
        onChanged: (value) {
          final amount = double.tryParse(value.replaceAll(',', ''));
          if (amount != null && amount >= 0 && amount <= 1500000) {
            setState(() {
              loanAmount = amount;
            });
          }
        },
      ),
    );
  }

  // -------------------------------------------------------
  //               RESULT SECTION (MOBILE)
  // -------------------------------------------------------
  Widget _buildResultCard(
    bool isDark,
    double emi,
    double totalInterest,
    double totalPayment,
    double principalPercentage,
    double interestPercentage,
  ) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppColors.lightPrimaryBlue.withOpacity(0.08),
            AppColors.lightPrimaryBlue.withOpacity(0.14),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: AppColors.lightPrimaryBlue.withOpacity(0.25)),
        boxShadow: [
          BoxShadow(
            color: isDark ? Colors.black45 : Colors.grey.shade300,
            blurRadius: 12,
            spreadRadius: 1,
          )
        ],
      ),
      child: Column(
        children: [
          Text(
            "Monthly EMI",
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: isDark ? AppColors.darkText : AppColors.lightText,
            ),
          ),

          const SizedBox(height: 12),

          Text(
            "₹ ${emi.toStringAsFixed(0)}",
            style: TextStyle(
              fontSize: 40,
              fontWeight: FontWeight.bold,
              color: AppColors.lightPrimaryBlue,
            ),
          ),

          const SizedBox(height: 24),

          Row(
            children: [
              Expanded(child: _infoCard("Total Interest", totalInterest, isDark)),
              const SizedBox(width: 14),
              Expanded(child: _infoCard("Total Payment", totalPayment, isDark)),
            ],
          ),

          const SizedBox(height: 30),

          Text(
            "Payment Breakdown",
            style: TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.bold,
              color: isDark ? AppColors.darkText : AppColors.lightText,
            ),
          ),

          const SizedBox(height: 16),

          SizedBox(
            height: 150,
            width: 150,
            child: CustomPaint(
              painter: DoughnutChartPainter(
                principalPercentage,
                interestPercentage,
              ),
            ),
          ),

          const SizedBox(height: 16),

          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _legend(color: Colors.orange, label: "Interest"),
              const SizedBox(width: 16),
              _legend(color: Colors.blue, label: "Principal"),
            ],
          ),
        ],
      ),
    );
  }

  Widget _infoCard(String title, double value, bool isDark) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        children: [
          Text(
            title,
            style: TextStyle(
                color: isDark ? AppColors.darkMuted : AppColors.lightTextSecondary,
                fontSize: 12),
          ),
          const SizedBox(height: 6),
          Text(
            "₹ ${value.toStringAsFixed(0)}",
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: isDark ? AppColors.darkText : AppColors.lightText,
            ),
          ),
        ],
      ),
    );
  }

  Widget _legend({required Color color, required String label}) {
    return Row(
      children: [
        Container(
          width: 14,
          height: 14,
          decoration:
              BoxDecoration(color: color, borderRadius: BorderRadius.circular(4)),
        ),
        const SizedBox(width: 6),
        Text(label),
      ],
    );
  }
}

// -------------------------------------------------------
//                   CUSTOM DOUGHNUT CHART
// -------------------------------------------------------

class DoughnutChartPainter extends CustomPainter {
  final double principalPercent;
  final double interestPercent;

  DoughnutChartPainter(this.principalPercent, this.interestPercent);

  @override
  void paint(Canvas canvas, Size size) {
    final rect = Offset.zero & size;

    final principalPaint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 18
      ..style = PaintingStyle.stroke;

    final interestPaint = Paint()
      ..color = Colors.orange
      ..strokeWidth = 18
      ..style = PaintingStyle.stroke;

    double principalAngle = 2 * pi * (principalPercent / 100);
    double interestAngle = 2 * pi * (interestPercent / 100);

    canvas.drawArc(rect, -pi / 2, principalAngle, false, principalPaint);
    canvas.drawArc(rect, -pi / 2 + principalAngle, interestAngle, false,
        interestPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
