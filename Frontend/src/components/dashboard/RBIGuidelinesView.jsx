import React from 'react';
import { ArrowLeft, ChevronRight, Shield, CheckCircle, Zap, Award } from 'lucide-react';

const RBIGuidelinesView = ({ setView, expandedGuideline, setExpandedGuideline }) => {
    const guidelines = [
        {
            id: 'disclosures',
            title: 'Loan Disclosures',
            content: `• RBI mandates lenders to provide a Key Fact Statement (KFS) including APR, interest rate breakdown, processing fees, penalty charges, and total repayment amount.

• Digital lenders must clearly disclose algorithms used for creditworthiness evaluation.

• No hidden charges are allowed.

• Borrowers must receive digital copies of loan agreements, sanction letters, and repayment schedules.`
        },
        {
            id: 'rates',
            title: 'Interest Rates & Fair Pricing',
            content: `• Effective annual interest rate must be clearly shown before loan approval.

• Processing fees, GST, and any penalties must be mentioned separately.

• Floating-rate loans must disclose benchmark (such as repo rate) and reset frequency.

• Banks must maintain fair pricing policies approved by their board.

Focus on comparing total repayment, not just the EMI.`
        },
        {
            id: 'privacy',
            title: 'Data Privacy & Digital Lending',
            content: `• Apps cannot access SMS, contacts, gallery, or files without explicit consent.

• Only essential financial data (such as bank statements) may be used for underwriting.

• Borrowers can request correction or deletion of stored data.

• Data shared with credit bureaus or verification partners must be disclosed.

Credify evaluates income stability from bank statements without intrusive access.`
        },
        {
            id: 'recovery',
            title: 'Recovery & Collection Standards',
            content: `• Recovery agents must follow respectful conduct; harassment is prohibited.

• Calls and visits must follow permitted timings (generally 8 AM to 7 PM).

• Borrowers must receive written notices before escalation.

• All recovery procedures must follow RBI's Fair Practice Code.

Keep copies of all documents for your own protection.`
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-4xl mx-auto">
                <button onClick={() => setView('dashboard')} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="text-center mb-10">
                    <div className="w-28 h-28 mx-auto mb-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-3xl flex items-center justify-center shadow-2xl">
                        <span className="text-6xl">🏛️</span>
                    </div>
                    <h2 className="text-4xl font-bold text-gray-900 mb-3">RBI Guidelines</h2>
                    <p className="text-gray-600 text-lg">Know your rights as a borrower</p>
                </div>

                <div className="space-y-4 mb-8">
                    {guidelines.map((guideline) => (
                        <div key={guideline.id} className="bg-white border-2 border-gray-200 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-all">
                            <button
                                onClick={() => setExpandedGuideline(expandedGuideline === guideline.id ? null : guideline.id)}
                                className="w-full px-6 py-5 flex items-center justify-between hover:bg-gray-50 transition-colors"
                            >
                                <span className="font-bold text-gray-900 text-lg text-left">{guideline.title}</span>
                                <ChevronRight className={`w-6 h-6 text-gray-400 transition-transform ${expandedGuideline === guideline.id ? 'rotate-90' : ''}`} />
                            </button>

                            {expandedGuideline === guideline.id && (
                                <div className="px-6 py-5 bg-gradient-to-br from-gray-50 to-blue-50 border-t-2 border-gray-200">
                                    <div className="prose prose-sm max-w-none">
                                        {guideline.content.split('\n\n').map((paragraph, idx) => (
                                            <p key={idx} className="text-gray-700 mb-4 whitespace-pre-line leading-relaxed">{paragraph}</p>
                                        ))}
                                    </div>
                                    <a
                                        href="https://www.rbi.org.in"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-bold text-sm mt-4 hover:underline"
                                    >
                                        Read Official Source →
                                    </a>
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-8 border-2 border-blue-200 shadow-xl">
                    <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-3 text-2xl">
                        <Shield className="w-7 h-7 text-blue-600" />
                        Salary-Slip-Free Personal Loan Criteria
                    </h3>
                    <p className="text-gray-700 mb-6 leading-relaxed">
                        Top banks accept applications with bank statements instead of salary slips. Here are common criteria:
                    </p>

                    <div className="space-y-4">
                        {[
                            {
                                name: 'State Bank of India (SBI)',
                                points: ['6-12 months bank statements with consistent income', 'PAN, Aadhaar, and address proof required', 'Tenure up to 5 years']
                            },
                            {
                                name: 'HDFC Bank',
                                points: ['6 months statements, ID and address proof', 'Focus on inflow patterns and credit history', 'Tenure up to 5 years']
                            },
                            {
                                name: 'ICICI Bank',
                                points: ['6-12 months statements and ID proofs', 'Evaluates monthly balance and spending behavior']
                            },
                            {
                                name: 'Axis Bank',
                                points: ['Statement-based income verification', 'May request alternative proofs like receipts']
                            },
                            {
                                name: 'Kotak Mahindra Bank',
                                points: ['6-month statements and basic KYC', 'Quick digital disbursal for stable inflows']
                            }
                        ].map((bank, idx) => (
                            <div key={idx} className="bg-white rounded-2xl p-5 border-2 border-blue-100 shadow-md">
                                <h4 className="font-bold text-gray-900 mb-3 text-lg">{bank.name}</h4>
                                <ul className="space-y-2">
                                    {bank.points.map((point, pidx) => (
                                        <li key={pidx} className="flex items-start gap-2">
                                            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                            <span className="text-sm text-gray-700">{point}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    <div className="mt-6 p-5 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl">
                        <h4 className="font-bold text-green-800 mb-3 text-lg flex items-center gap-2">
                            <Zap className="w-5 h-5" />
                            Practical Tips
                        </h4>
                        <ul className="space-y-2">
                            {[
                                'Maintain steady inflows and avoid overdrafts',
                                'Keep at least 6 months of clean statement history',
                                'Ensure transactions clearly show income source',
                                'Use Credify\'s analysis for a clean financial summary'
                            ].map((tip, idx) => (
                                <li key={idx} className="flex items-start gap-2">
                                    <Award className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-sm text-green-800 font-medium">{tip}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RBIGuidelinesView;
