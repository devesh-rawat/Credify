from fpdf import FPDF
import os
from datetime import datetime

class PDFService:
    def __init__(self):
        self.output_dir = "reports/generated"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _safe_get(self, data: dict, key: str, default: str = "N/A") -> str:
        """Safely get value with default"""
        value = data.get(key, default)
        return str(value) if value is not None else default
    
    def _sanitize_text(self, text: str) -> str:
        """Convert Unicode characters to ASCII-safe equivalents for PDF"""
        if not text:
            return ""
        # Replace Indian Rupee symbol with Rs.
        text = text.replace('₹', 'Rs. ')
        # Remove other problematic Unicode characters
        return text.encode('ascii', 'ignore').decode('ascii')
    
    def _format_currency(self, amount) -> str:
        """Format amount as Indian currency (ASCII-safe for PDF)"""
        if amount is None:
            return "Rs. 0"
        try:
            # Format in Indian numbering system (lakhs, crores)
            amt = float(amount)
            if amt >= 10000000:  # 1 crore
                return f"Rs. {amt/10000000:.2f} Cr"
            elif amt >= 100000:  # 1 lakh
                return f"Rs. {amt/100000:.2f} L"
            else:
                return f"Rs. {amt:,.0f}"
        except (ValueError, TypeError):
            return "Rs. 0"
    
    def _format_percentage(self, value) -> str:
        """Format value as percentage"""
        if value is None:
            return "0.00%"
        try:
            return f"{float(value) * 100:.2f}%"
        except (ValueError, TypeError):
            return "0.00%"
    
    def _format_ratio(self, value) -> str:
        """Format value as ratio (decimal)"""
        if value is None:
            return "0.00"
        try:
            return f"{float(value):.2f}"
        except (ValueError, TypeError):
            return "0.00"
    
    def _get_user_name(self, user_data: dict) -> str:
        """Extract user name from various possible fields"""
        name = user_data.get('name') or user_data.get('full_name') or user_data.get('user_name')
        if name:
            return str(name)
        
        # Try to fetch from database if user_id is available
        user_id = user_data.get('user_id')
        if user_id:
            try:
                from database.mongo import db
                user = db.get_db().users.find_one({"user_id": user_id})
                if user:
                    return user.get('name', user.get('full_name', 'User'))
            except:
                pass
        
        return "User"

    def _write_markdown(self, pdf, text: str, line_height: int = 5):
        """
        Parse text for **bold** markdown and write to PDF.
        Supports simple **bold** tags.
        """
        if not text:
            return

        # Split by ** to separate bold parts
        # Example: "This is **bold** text" -> ["This is ", "bold", " text"]
        parts = text.split('**')
        
        # Save original font settings
        original_font = pdf.font_family
        original_style = pdf.font_style
        original_size = pdf.font_size_pt
        
        for i, part in enumerate(parts):
            if not part:
                continue
                
            # Even index = Normal text, Odd index = Bold text
            if i % 2 == 1:
                pdf.set_font(original_font, 'B', original_size)
            else:
                pdf.set_font(original_font, original_style, original_size)
            
            # Write text
            # Note: write() doesn't automatically wrap lines like multi_cell
            # But for simple lists and short texts, it works well.
            # For longer text blocks, we might need a more complex approach,
            # but fpdf's write() handles wrapping reasonably well for flow text.
            pdf.write(line_height, part)
            
        # Restore original font
        pdf.set_font(original_font, original_style, original_size)
        # Add a new line after the block if it was a multi_cell replacement
        pdf.ln(line_height)

    def generate_report(self, user_data: dict, account_data: dict, score_data: dict, features: dict) -> str:
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Credify Credit Report", ln=True, align="C")
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", ln=True, align="C")
        pdf.ln(10)
        
        # User Details
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "User Details", ln=True)
        pdf.set_font("Arial", "", 10)
        
        user_name = self._sanitize_text(self._get_user_name(user_data))
        user_id = self._sanitize_text(self._safe_get(user_data, 'user_id', 'Unknown'))
        
        pdf.cell(0, 8, f"Name: {user_name}", ln=True)
        pdf.cell(0, 8, f"User ID: {user_id}", ln=True)
        
        # Account Details - Show all accounts
        all_accounts = user_data.get('all_accounts', [])
        
        if all_accounts and len(all_accounts) > 0:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 8, f"Bank Accounts ({len(all_accounts)}):", ln=True)
            pdf.set_font("Arial", "", 10)
            
            for idx, acc in enumerate(all_accounts, 1):
                bank_name = self._sanitize_text(acc.get('bank_name', 'Unknown Bank'))
                account_type = self._sanitize_text(acc.get('account_type', 'SAVINGS'))
                account_num = acc.get('account_number', 'XXXX')
                account_mask = account_num[-4:] if account_num else 'XXXX'
                
                # Highlight the primary account used for scoring
                is_primary = acc.get('account_id') == account_data.get('account_id')
                if is_primary:
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 8, f"  {idx}. {bank_name} - ****{account_mask} ({account_type}) [Primary]", ln=True)
                    pdf.set_font("Arial", "", 10)
                else:
                    pdf.cell(0, 8, f"  {idx}. {bank_name} - ****{account_mask} ({account_type})", ln=True)
        else:
            # Fallback to single account if all_accounts not available
            bank_name = self._sanitize_text(self._safe_get(account_data, 'bank_name', 'Bank'))
            account_mask = account_data.get('account_mask') or account_data.get('account_number', 'XXXX')[-4:] if account_data.get('account_number') else 'XXXX'
            account_type = self._sanitize_text(self._safe_get(account_data, 'account_type', 'SAVINGS'))
            
            pdf.cell(0, 8, f"Bank: {bank_name}", ln=True)
            pdf.cell(0, 8, f"Account: ****{account_mask} ({account_type})", ln=True)
        
        pdf.ln(5)

        # Credit Score Section
        pdf.set_font("Arial", "B", 14)
        pdf.set_fill_color(230, 230, 250)
        pdf.cell(0, 10, "Credit Score & Risk Assessment", ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.ln(2)
        
        credit_score = score_data.get('credit_score', 0)
        default_prob = score_data.get('default_probability', 0)
        risk_label = self._sanitize_text(self._safe_get(score_data, 'risk_label', 'Unknown'))
        
        # Score with color coding
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 8, "Credit Score:", ln=False)
        pdf.set_font("Arial", "B", 14)
        
        # Color code based on score
        if credit_score >= 750:
            pdf.set_text_color(0, 128, 0)  # Green
        elif credit_score >= 650:
            pdf.set_text_color(255, 165, 0)  # Orange
        else:
            pdf.set_text_color(255, 0, 0)  # Red
        
        pdf.cell(0, 8, f"{int(credit_score)}", ln=True)
        pdf.set_text_color(0, 0, 0)  # Reset to black
        
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Default Probability: {self._format_percentage(default_prob)}", ln=True)
        pdf.cell(0, 8, f"Risk Category: {risk_label}", ln=True)
        pdf.ln(5)

        # Calculate financial metrics EARLY so they're available throughout
        debt = features.get('DEBT', 0)
        savings = features.get('SAVINGS', 0)
        income = features.get('INCOME', 0)
        
        # If income not directly available, try to estimate from ratios
        if not income and debt:
            debt_income_ratio = features.get('R_DEBT_INCOME', 0)
            if debt_income_ratio and debt_income_ratio > 0:
                income = debt / debt_income_ratio
        
        # Get loan amount early too
        loan_amount = user_data.get('loan_amount', 0)

        # Financial Summary
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 250, 230)
        pdf.cell(0, 10, "Financial Summary", ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.ln(2)
        
        pdf.cell(0, 8, f"Total Debt: {self._format_currency(debt)}", ln=True)
        pdf.cell(0, 8, f"Total Savings: {self._format_currency(savings)}", ln=True)
        pdf.cell(0, 8, f"Estimated Monthly Income: {self._format_currency(income)}", ln=True)
        
        # Loan amount requested
        if loan_amount:
            pdf.cell(0, 8, f"Requested Loan Amount: {self._format_currency(loan_amount)}", ln=True)
        
        # Key ratios
        debt_income = features.get('R_DEBT_INCOME', 0)
        savings_income = features.get('R_SAVINGS_INCOME', 0)
        
        pdf.ln(3)
        pdf.set_font("Arial", "I", 9)
        pdf.cell(0, 6, f"Debt-to-Income Ratio: {self._format_ratio(debt_income)}", ln=True)
        pdf.cell(0, 6, f"Savings-to-Income Ratio: {self._format_ratio(savings_income)}", ln=True)
        
        # Loan-to-Income ratio if loan amount is present
        if loan_amount and income and income > 0:
            loan_to_income_ratio = loan_amount / income
            pdf.cell(0, 6, f"Loan-to-Income Ratio: {self._format_ratio(loan_to_income_ratio)}", ln=True)
        pdf.ln(5)

        pdf.ln(3)
        
        # ==================== AI-BASED DECISION ====================
        pdf.set_font("Arial", "B", 14)
        pdf.set_fill_color(240, 240, 255)
        pdf.cell(0, 12, "AI-POWERED LENDING DECISION", ln=True, fill=True, align='C')
        pdf.ln(2)
        
        # Determine AI recommendation based on score
        credit_score = score_data.get('credit_score', 0)
        ai_decision = "APPROVE"
        decision_color = (0, 150, 0)  # Green
        decision_reasoning = ""
        
        if credit_score >= 700:
            ai_decision = "APPROVE"
            decision_color = (0, 150, 0)  # Green
            decision_reasoning = f"Strong credit profile with score of {credit_score}/900. Low default risk. Recommended for approval with standard terms."
        elif credit_score >= 600:
            ai_decision = "APPROVE WITH CONDITIONS"
            decision_color = (200, 150, 0)  # Orange
            decision_reasoning = f"Moderate credit profile with score of {credit_score}/900. Approve with moderate interest rate or additional security."
        elif credit_score >= 500:
            ai_decision = "REVIEW REQUIRED"
            decision_color = (200, 100, 0)  # Dark Orange
            decision_reasoning = f"Fair credit profile with score of {credit_score}/900. Manual review recommended. Consider approval with higher interest or collateral."
        else:
            ai_decision = "REJECT"
            decision_color = (200, 0, 0)  # Red
            decision_reasoning = f"Poor credit profile with score of {credit_score}/900. High default risk. Recommend rejection or secured loan only."
        
        # Display decision prominently
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(*decision_color)
        pdf.cell(0, 10, f"DECISION: {ai_decision}", ln=True, align='C')
        pdf.set_text_color(0, 0, 0)  # Reset to black
        
        pdf.ln(2)
        pdf.set_font("Arial", "I", 10)
        pdf.set_fill_color(250, 250, 250)
        # Use markdown writer for reasoning
        self._write_markdown(pdf, decision_reasoning, line_height=6)
        
        pdf.ln(3)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, "AI Analysis Summary:", ln=True)
        pdf.set_font("Arial", "", 9)
        
        # Show concise AI summary
        ai_summary = score_data.get('summary') or score_data.get('ai_insight', '')
        if ai_summary:
            sanitized_summary = self._sanitize_text(ai_summary)
            self._write_markdown(pdf, sanitized_summary, line_height=5)
        
        # Show key factors
        key_factors = score_data.get('key_factors', [])
        if key_factors:
            pdf.ln(2)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 6, "Key Factors:", ln=True)
            pdf.set_font("Arial", "", 9)
            for i, factor in enumerate(key_factors, 1):
                sanitized_factor = self._sanitize_text(factor)
                pdf.write(5, f"{i}. ")
                self._write_markdown(pdf, sanitized_factor, line_height=5)
        
        # Show recommendations
        recommendations = score_data.get('recommendations', [])
        if recommendations:
            pdf.ln(2)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 6, "Recommendations:", ln=True)
            pdf.set_font("Arial", "", 9)
            for i, rec in enumerate(recommendations, 1):
                sanitized_rec = self._sanitize_text(rec)
                pdf.write(5, f"{i}. ")
                self._write_markdown(pdf, sanitized_rec, line_height=5)

        
        pdf.ln(5)
        
        pdf.ln(3)

        # Underwriting Notes (Technical Details)
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(250, 230, 230)
        pdf.cell(0, 10, "Technical Underwriting Notes", ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.ln(2)
        
        # Calculate loan-to-income ratio and apply policy-based lending logic
        # Note: loan_amount and income are already calculated at the top of this function
        loan_to_income_ratio = 0
        recommendation = score_data.get('recommendation', 'REVIEW')
        underwriting_notes = score_data.get('underwriting_note', [])
        
        # Debug logging
        print(f"[PDF Service] Loan Amount: {loan_amount}, Income: {income}")
        print(f"[PDF Service] Initial Recommendation: {recommendation}")
        
        if loan_amount and income and income > 0:
            loan_to_income_ratio = loan_amount / income
            print(f"[PDF Service] Calculated Loan-to-Income Ratio: {loan_to_income_ratio:.2f}x income")
            
            # POLICY-BASED LENDING RULES:
            # If ratio exceeds 25x income, reject the loan
            # If ratio is within 25x but score is low, mark as "RISKY BUT WITHIN POLICY"
            if loan_to_income_ratio > 25:
                print(f"[PDF Service] REJECTING: Ratio {loan_to_income_ratio:.2f}x exceeds 25x threshold")
                recommendation = 'REJECT'
                rejection_message = f"Loan rejected: Requested loan amount ({self._format_currency(loan_amount)}) is too high compared to income ({self._format_currency(income)}). Loan-to-Income ratio: {self._format_ratio(loan_to_income_ratio)}x (exceeds 25x policy limit)."
                if isinstance(underwriting_notes, list):
                    underwriting_notes = [rejection_message] + underwriting_notes
                else:
                    underwriting_notes = [rejection_message]
            elif loan_to_income_ratio <= 25 and credit_score < 550:
                # Within policy but risky due to low credit score
                print(f"[PDF Service] POLICY OVERRIDE: Ratio {loan_to_income_ratio:.2f}x within 25x limit, but score is low ({credit_score})")
                recommendation = 'APPROVE_WITH_CONDITIONS'
                policy_note = f"POLICY-BASED LENDING: Loan-to-Income ratio of {self._format_ratio(loan_to_income_ratio)}x is within the 25x policy limit. Despite low credit score ({credit_score}/900), this loan can be considered with additional safeguards: higher interest rate, guarantor, or collateral required."
                if isinstance(underwriting_notes, list):
                    underwriting_notes = [policy_note] + underwriting_notes
                else:
                    underwriting_notes = [policy_note]
            else:
                print(f"[PDF Service] Ratio {loan_to_income_ratio:.2f}x is within acceptable range")
        else:
            print(f"[PDF Service] Cannot calculate ratio - missing loan_amount or income")

        
        # Ensure underwriting_notes is a list
        if underwriting_notes is None:
            underwriting_notes = []
        elif not isinstance(underwriting_notes, list):
            underwriting_notes = [str(underwriting_notes)]

        if underwriting_notes:
            for note in underwriting_notes:
                sanitized_note = self._sanitize_text(str(note))
                pdf.write(6, "- ")
                self._write_markdown(pdf, sanitized_note, line_height=6)
        else:
            pdf.cell(0, 6, "Standard underwriting guidelines apply.", ln=True)
        
        # Recommendation (now potentially overridden by ratio logic)
        pdf.ln(3)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(50, 8, "Recommendation:", ln=False)
        
        # Color code recommendation
        if recommendation == 'APPROVE':
            pdf.set_text_color(0, 128, 0)
        elif recommendation == 'APPROVE_WITH_CONDITIONS':
            pdf.set_text_color(255, 140, 0)  # Dark orange for conditional approval
        elif recommendation == 'REJECT':
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(255, 165, 0)
        
        pdf.cell(0, 8, recommendation, ln=True)
        pdf.set_text_color(0, 0, 0)
        
        # Footer
        pdf.ln(10)
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 5, "This report is generated by Credify AI-powered credit scoring system.", ln=True, align="C")
        pdf.cell(0, 5, "For internal use only. Confidential information.", ln=True, align="C")

        # Save
        filename = f"{user_id}_{account_data.get('account_id', 'ACC')}_{int(datetime.now().timestamp())}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            pdf.output(filepath)
            print(f"[PDF Service] Report generated successfully: {filepath}")
            return filepath
        except Exception as e:
            print(f"[PDF Service] ERROR generating PDF: {str(e)}")
            # Return a dummy path or raise to let caller handle
            raise Exception(f"Failed to write PDF file: {str(e)}")

pdf_service = PDFService()
