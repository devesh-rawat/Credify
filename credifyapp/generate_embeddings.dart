import 'dart:convert';
import 'dart:io';
import 'package:google_generative_ai/google_generative_ai.dart';

void main() async {
  final apiKey = "AIzaSyACo4Q4osNyAQH1bfzVIjbCN-rwYbT2_9c"; // 🔐 Put regenerated key here

  final model = GenerativeModel(
    model: "models/text-embedding-004",
    apiKey: apiKey,
  );

  final List items = [
    { "id": "1", "text": "Minimum credit score generally required for loan approval in India is around 650, but lenders may approve lower scores with additional verification." },
    { "id": "2", "text": "Documents required for digital lending include PAN, Aadhaar, basic KYC details, and access to your bank statements through secure consent." },
    { "id": "3", "text": "Loan eligibility is based on income stability, credit score, age, repayment history, and debt-to-income ratio." },
    { "id": "4", "text": "Account Aggregator (AA) allows users to share their bank transaction data securely with lenders using consent-based data sharing." },
    { "id": "5", "text": "Aadhaar and PAN verification is essential for KYC compliance before loan approval." },
    { "id": "6", "text": "Debt-to-Income ratio is calculated by dividing monthly loan EMIs by monthly income; lower is better." },
    { "id": "7", "text": "Default probability indicates the likelihood that a borrower may miss future repayments." },
    { "id": "8", "text": "RBI requires all digital lenders to follow strict KYC, data privacy, and consent-based data sharing norms." },
    { "id": "9", "text": "Income stability is measured by analyzing regular credits, salary deposits, or business cash flow patterns." },
    { "id": "10", "text": "Late payments reduce your creditworthiness and increase your risk category." },
    { "id": "11", "text": "Utility bill payment behavior can be used to estimate creditworthiness for borrowers with no financial history." },
    { "id": "12", "text": "Thin-file users are people who have little or no formal credit history." },
    { "id": "13", "text": "Loan amount approved depends on your income, repayment ability, and verified banking behavior." },
    { "id": "14", "text": "Credify uses AI to analyze bank statements, spending behavior, and income patterns to generate a Trust Score." },
    { "id": "15", "text": "Your Trust Score ranges from 0 to 100, where a higher score indicates stronger repayment capacity." },
    { "id": "16", "text": "Frequent EMI bounces, overdue bills, and cash withdrawals are risk indicators for lenders." },
    { "id": "17", "text": "Secured loans like gold loans or home loans may require lower credit scores than unsecured personal loans." },
    { "id": "18", "text": "Credify does not store your banking password or OTP; all data is fetched securely via AA under your consent." },
    { "id": "19", "text": "EMI affordability is calculated using monthly surplus after essential expenditures." },
    { "id": "20", "text": "High credit utilization (using more than 40% of limits) increases default risk." },
    { "id": "21", "text": "A borrower with irregular income may still qualify if they show positive cash flow and timely utility or rent payments." },
    { "id": "22", "text": "Loan rejection does not permanently impact your credit score unless a hard enquiry is recorded by bureaus." },
    { "id": "23", "text": "Credify's AI model predicts both credit score and default probability using ML algorithms." },
    { "id": "24", "text": "PAN is used to check financial identity, while Aadhaar is used for biometric or OTP-based eKYC verification." },
    { "id": "25", "text": "Total monthly income includes salary, business revenue, freelance earnings, and other recurring credits." },
    { "id": "26", "text": "Frequent gambling or speculation transactions negatively affect creditworthiness." },
    { "id": "27", "text": "RBI mandates that all loan repayments must go directly to the lender’s bank account to avoid fraud." },
    { "id": "28", "text": "Positive indicators include regular savings, timely bill payments, and consistent salary deposits." },
    { "id": "29", "text": "Credify helps lenders reduce NPAs by identifying unstable income patterns early." },
    { "id": "30", "text": "Users can improve creditworthiness by paying EMIs on time, reducing unnecessary spending, and maintaining savings." },
    { "id": "31", "text": "Your spending categories—food, rent, utilities, travel, and shopping—are analyzed to understand financial discipline." },
    { "id": "32", "text": "Salary-based users typically show higher stability scores compared to gig workers." },
    { "id": "33", "text": "Spikes in expenses or irregular withdrawals can indicate financial stress." },
    { "id": "34", "text": "High transaction bounce rate increases the risk label from Low → Moderate → High." },
    { "id": "35", "text": "Credify generates a PDF report summarizing your income, expenses, risk factors, and AI insights." },
    { "id": "36", "text": "The AI Insights explain why your score is high or low and provides personalised recommendations." },
    { "id": "37", "text": "Lenders use both your credit score and behavioural patterns to determine loan interest rates." },
    { "id": "38", "text": "Credify does not affect your credit score; it only predicts risk based on your provided data." },
    { "id": "39", "text": "Your bank data is encrypted and never shared without your explicit consent." },
    { "id": "40", "text": "A sudden drop in income or repeated overdrafts can increase your default probability." },
    { "id": "41", "text": "Having multiple active loans increases your debt burden and reduces eligibility." },
    { "id": "42", "text": "A good credit mix includes long-term loans, short-term loans, and low credit utilization." },
    { "id": "43", "text": "High-value cash withdrawals are considered risky because they lack transaction transparency." },
    { "id": "44", "text": "Credit score does not depend on your religion, caste, or location—only on financial behavior." },
    { "id": "45", "text": "Your AA-linked bank statements are used only during the scoring process and not stored permanently." },
    { "id": "46", "text": "If your Trust Score is above 85, you are eligible for fast-track loan approval." },
    { "id": "47", "text": "Loans with longer tenure have lower EMI but higher total interest." },
    { "id": "48", "text": "Irregular cash deposits without source proofs reduce credibility." },
    { "id": "49", "text": "Credify helps both lenders and borrowers by creating a transparent, AI-powered credit scoring process." },
    { "id": "50", "text": "Low-income borrowers can still get loans if utility bill patterns and spending discipline are positive." }
  ];

  final List output = [];

  for (var item in items) {
    final emb = await model.embedContent(
      Content.text(item["text"]),
    );

    output.add({
      "id": item["id"],
      "text": item["text"],
      "embedding": emb.embedding.values,
    });
  }

  final file = File("fintech_data_with_embeddings.json");
  await file.writeAsString(jsonEncode(output));

  print("DONE! Saved as fintech_data_with_embeddings.json");
}
