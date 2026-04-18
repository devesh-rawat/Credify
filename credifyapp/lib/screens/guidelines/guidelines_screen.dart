// rbi_guidelines_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:credifyapp/theme/theme.dart';

class RBIGuidelinesScreen extends StatelessWidget {
  const RBIGuidelinesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    
    final textColor = Theme.of(context).textTheme.bodyLarge!.color;

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,

      appBar: AppBar(
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        elevation: 0,
        centerTitle: true,
        title: Text(
          "RBI Guidelines",
          style: TextStyle(
            color: textColor,
            fontSize: 20,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
        child: Column(
          children: [

            // ---------------- INTRO CARD ----------------
            _introCard(context),

            const SizedBox(height: 16),

            // ---------------- EXPANDABLE CARD SECTIONS ----------------
            _expansionCard(
              context,
              title: "Loan Disclosure Rules (Must-Know)",
              markdown: _loanDisclosureMarkdown,
            ),

            const SizedBox(height: 12),

            _expansionCard(
              context,
              title: "Interest Rates & Fair Pricing",
              markdown: _interestRatesMarkdown,
            ),

            const SizedBox(height: 12),

            _expansionCard(
              context,
              title: "Data Privacy & Digital Lending",
              markdown: _dataPrivacyMarkdown,
            ),

            const SizedBox(height: 12),

            _expansionCard(
              context,
              title: "Recovery & Collection Standards",
              markdown: _recoveryMarkdown,
            ),

            const SizedBox(height: 12),

            _expansionCard(
              context,
              title: "Salary-Slip-Free Loan Criteria (Top 5 Banks)",
              markdown: _personalLoanMarkdown,
            ),

            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------------------
  // INTRO CARD
  // -------------------------------------------------------------------------
  Widget _introCard(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardColor = isDark ? AppColors.darkCard : AppColors.lightCard;

    return Card(
      color: cardColor,
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          children: [
            Image.asset("assets/images/rbi.png",height: 120,width: 120,),
            SizedBox(height: 5,),
            MarkdownBody(
              
          data: _introMarkdown,
          styleSheet: _markdownStyle(context),
        ),
          ],
        )
      ),
    );
  }

  
  Widget _expansionCard(
    BuildContext context, {
    required String title,
    required String markdown,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardColor = isDark ? AppColors.darkCard : AppColors.lightCard;

    return Card(
      elevation: 0,
      color: cardColor,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          childrenPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),

          iconColor: Theme.of(context).primaryColor,
          collapsedIconColor: Theme.of(context).primaryColor,

          title: Text(
            title,
            style: TextStyle(
              color: Theme.of(context).textTheme.bodyLarge!.color,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),

          children: [
            MarkdownBody(
              data: markdown,
              styleSheet: _markdownStyle(context),
            ),
          ],
        ),
      ),
    );
  }

  // -------------------------------------------------------------------------
  // MARKDOWN STYLE
  // -------------------------------------------------------------------------
  MarkdownStyleSheet _markdownStyle(BuildContext context) {
    return MarkdownStyleSheet(
      h2: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w700,
        color: Theme.of(context).textTheme.bodyLarge!.color,
      ),
      p: TextStyle(
        fontSize: 14,
        height: 1.55,
        color: Theme.of(context).textTheme.bodyMedium!.color,
      ),
      listBullet: TextStyle(
        color: Theme.of(context).textTheme.bodyMedium!.color,
      ),
    );
  }

  // -------------------------------------------------------------------------
  // -------------------- MARKDOWN CONTENT (CLEAN, NO EMOJIS) -----------------
  // -------------------------------------------------------------------------

  final String _introMarkdown = """

This page provides a simplified version of essential RBI lending rules along with practical guidance.

Credify uses bank-statement analysis to predict loan eligibility for users who do not have traditional salary slips. These guidelines help you understand how lenders legally evaluate borrowers using digital financial footprints.
""";

  final String _loanDisclosureMarkdown = """
## Key Disclosure Requirements

- Lenders must provide a **Key Fact Statement (KFS)** showing APR, total cost, EMI schedule and all fees.
- No hidden or undisclosed charges are allowed at any stage.
- EMI repayment schedule must be given at the time of sanction.
- Digital lenders must clearly explain what statement data points are used for scoring.
- Borrowers must receive digital copies of the loan agreement and sanction letter.

These disclosures exist to ensure transparency and fairness.
""";

  final String _interestRatesMarkdown = """
## Interest & Pricing Rules

- Effective annual interest rate must be clearly shown before loan approval.
- Processing fees, GST, and any penalties must be mentioned separately.
- Floating-rate loans must disclose benchmark (such as repo rate) and reset frequency.
- Banks must maintain fair pricing policies approved by their board.

Focus on comparing **total repayment**, not just the EMI.
""";

  final String _dataPrivacyMarkdown = """
## Data Privacy Standards

- Apps cannot access SMS, contacts, gallery, or files without explicit consent.
- Only essential financial data (such as bank statements) may be used for underwriting.
- Borrowers can request correction or deletion of stored data.
- Data shared with credit bureaus or verification partners must be disclosed.

Credify evaluates income stability from bank statements without intrusive access.
""";

  final String _recoveryMarkdown = """
## Recovery & Collection Rules

- Recovery agents must follow respectful conduct; harassment is prohibited.
- Calls and visits must follow permitted timings (generally 8 AM to 7 PM).
- Borrowers must receive written notices before escalation.
- All recovery procedures must follow RBI's Fair Practice Code.

Keep copies of all documents for your own protection.
""";

  final String _personalLoanMarkdown = """
## Salary-Slip-Free Personal Loan Criteria (Top Banks)

These are simplified criteria that banks commonly consider when a borrower does not provide salary slips, relying mainly on **bank statements**.

---

### 1. State Bank of India (SBI)
- Requires 6–12 months of bank statements showing consistent income credits.
- PAN, Aadhaar, and address proof required.
- May check employer details or nature of income deposits.
- Tenure usually up to 5 years.

---

### 2. HDFC Bank
- Focuses heavily on bank-statement inflow patterns.
- Needs 6 months of statements, ID and address proof.
- Consistent income credits and good credit history increase approval chances.
- Tenure up to 5 years depending on product.

---

### 3. ICICI Bank
- Uses statement-based underwriting for selected personal loan products.
- Requires 6–12 months of statements and standard ID proofs.
- Evaluates monthly average balance, inflow stability, and spending behaviour.

---

### 4. Axis Bank
- Accepts applicants through bank-statement income verification.
- Requires statements, PAN, Aadhaar, and minimal supporting documents.
- May request alternative income proofs like receipts or contracts.

---

### 5. Kotak Mahindra Bank
- Digital personal loan products evaluate income directly from bank statements.
- Requires 6-month statements and basic KYC documents.
- Quick digital disbursal if inflows are stable and consistent.

---

### Practical Tips
- Maintain steady inflows and avoid frequent overdrafts.
- Keep at least 6 months of clean statement history.
- Ensure transactions clearly show your income source.
- Use Credify's analysis to generate a clean financial summary for lenders.
""";
}
