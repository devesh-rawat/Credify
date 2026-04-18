import React from 'react';
import { Menu, Award, FileText, Activity, TrendingUp, CheckCircle, CreditCard, Building2, Shield } from 'lucide-react';
import ProfileMenu from './ProfileMenu';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const ScoreDashboard = ({
    user,
    showProfileMenu,
    setShowProfileMenu,
    creditScore,
    setShowReport,
    handleRegenerateScore,
    handleApplyForLoan,
    setView,
    showReport,
    // handleDownloadReport, // We will implement local handler
    aadhar,
    pan,
    banks,
    applications,
    incomeStability,
    paymentDiscipline,
    scoringData
}) => {
    const handleDownloadReport = () => {
        const doc = new jsPDF();
        let yPos = 20;

        // Title
        doc.setFontSize(22);
        doc.setTextColor(44, 62, 80);
        doc.text('CREDIFY CREDIT REPORT', 105, yPos, { align: 'center' });
        yPos += 10;

        // Line
        doc.setLineWidth(0.5);
        doc.line(20, yPos, 190, yPos);
        yPos += 15;

        // User Details
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Name: ${user?.name || 'N/A'}`, 20, yPos);
        doc.text(`Email: ${user?.email || 'N/A'}`, 20, yPos + 8);
        const reportDate = scoringData?.created_at
            ? new Date(scoringData.created_at).toLocaleDateString()
            : new Date().toLocaleDateString();
        doc.text(`Date: ${reportDate}`, 150, yPos);
        yPos += 20;

        // Score Section
        doc.setFillColor(240, 240, 240);
        doc.rect(20, yPos, 170, 40, 'F');

        doc.setFontSize(16);
        doc.text('Credit Score', 30, yPos + 15);
        doc.setFontSize(24);
        doc.setTextColor(39, 174, 96);
        doc.text(`${creditScore}/900`, 30, yPos + 30);

        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);

        // Only show risk label if it exists in API response
        if (scoringData?.risk_label) {
            doc.text(`Risk Level: ${scoringData.risk_label}`, 120, yPos + 20);
        }

        if (scoringData?.default_probability !== undefined) {
            const defaultProb = (scoringData.default_probability * 100).toFixed(2);
            doc.setFontSize(10);
            doc.text(`Default Probability: ${defaultProb}%`, 120, yPos + 30);
        }
        yPos += 50;

        // Summary Section
        if (scoringData?.summary) {
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);
            doc.text('Summary', 20, yPos);
            yPos += 8;

            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            const summaryLines = doc.splitTextToSize(scoringData.summary, 170);
            doc.text(summaryLines, 20, yPos);
            yPos += (summaryLines.length * 5) + 10;
        }

        // Key Factors - only show if exists in API response
        if (scoringData?.key_factors && scoringData.key_factors.length > 0) {
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);
            doc.text('Key Factors', 20, yPos);
            yPos += 8;

            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            scoringData.key_factors.forEach(factor => {
                const text = typeof factor === 'string' ? factor : (factor.factor || factor.description || JSON.stringify(factor));
                const bulletText = text.startsWith('•') || text.startsWith('-') ? text : `• ${text}`;
                const lines = doc.splitTextToSize(bulletText, 165);

                // Check if we need a new page
                if (yPos + (lines.length * 5) > 270) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.text(lines, 25, yPos);
                yPos += (lines.length * 5) + 2;
            });
            yPos += 5;
        }

        // Recommendations - only show if exists in API response
        if (scoringData?.recommendations && scoringData.recommendations.length > 0) {
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);

            // Check if we need a new page
            if (yPos > 250) {
                doc.addPage();
                yPos = 20;
            }

            doc.text('Recommendations', 20, yPos);
            yPos += 8;

            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            scoringData.recommendations.forEach(rec => {
                const text = typeof rec === 'string' ? rec : (rec.text || rec.description || JSON.stringify(rec));
                const bulletText = text.startsWith('•') || text.startsWith('-') ? text : `• ${text}`;
                const lines = doc.splitTextToSize(bulletText, 165);

                // Check if we need a new page
                if (yPos + (lines.length * 5) > 270) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.text(lines, 25, yPos);
                yPos += (lines.length * 5) + 2;
            });
            yPos += 5;
        }

        // Underwriting Notes
        if (scoringData?.underwriting_note && scoringData.underwriting_note.length > 0) {
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);

            // Check if we need a new page
            if (yPos > 250) {
                doc.addPage();
                yPos = 20;
            }

            doc.text('Underwriting Notes', 20, yPos);
            yPos += 8;

            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            scoringData.underwriting_note.forEach(note => {
                const text = typeof note === 'string' ? note : JSON.stringify(note);
                const bulletText = text.startsWith('•') || text.startsWith('-') ? text : `• ${text}`;
                const lines = doc.splitTextToSize(bulletText, 165);

                // Check if we need a new page
                if (yPos + (lines.length * 5) > 270) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.text(lines, 25, yPos);
                yPos += (lines.length * 5) + 2;
            });
            yPos += 5;
        }

        // Final Decision
        if (scoringData?.recommendation) {
            // Check if we need a new page
            if (yPos > 250) {
                doc.addPage();
                yPos = 20;
            }

            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);
            doc.text('Decision', 20, yPos);
            yPos += 8;

            doc.setFontSize(10);
            const isApproved = scoringData.recommendation.toUpperCase() === 'APPROVE';
            doc.setTextColor(isApproved ? 39 : 220, isApproved ? 174 : 53, isApproved ? 96 : 69);
            doc.text(scoringData.recommendation.toUpperCase(), 20, yPos);
            yPos += 10;
        }

        // Footer
        doc.setFontSize(10);
        doc.setTextColor(150, 150, 150);
        doc.text('Generated by Credify AI', 105, 280, { align: 'center' });

        doc.save(`Credify_Report_${user?.name?.replace(/\s+/g, '_')}_${Date.now()}.pdf`);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 pt-24 pb-12 px-4">
            {showProfileMenu && (
                <ProfileMenu
                    user={user}
                    setShowProfileMenu={setShowProfileMenu}
                    creditScore={creditScore}
                    aadhar={aadhar}
                    pan={pan}
                    banks={banks}
                />
            )}
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
                    <div>
                        <p className="text-sm text-gray-500 mb-1">Hello,</p>
                        <h1 className="text-3xl md:text-4xl font-bold text-gray-900">{user?.name || 'User'}</h1>
                    </div>
                    <button
                        onClick={() => setShowProfileMenu(true)}
                        className="p-3 hover:bg-white rounded-xl transition-all shadow-sm"
                    >
                        <Menu className="w-6 h-6 text-gray-700" />
                    </button>
                </div>

                <div className="grid lg:grid-cols-3 gap-6">
                    {/* Score Display Card */}
                    <div className="lg:col-span-2">
                        <div className="bg-gradient-to-br from-green-500 via-emerald-600 to-teal-700 rounded-3xl p-8 md:p-10 text-white shadow-2xl relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32"></div>
                            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-10 rounded-full -ml-24 -mb-24"></div>

                            <div className="relative z-10">
                                <div className="flex items-center justify-between mb-6">
                                    <div className="flex items-center gap-3">
                                        <Award className="w-8 h-8" />
                                        <h2 className="text-2xl font-bold">Your Credify Score</h2>
                                    </div>
                                    <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-semibold">
                                        {creditScore >= 750 ? 'Excellent' : creditScore >= 650 ? 'Good' : 'Fair'}
                                    </span>
                                </div>

                                <div className="flex flex-col md:flex-row items-center gap-8">
                                    <div className="flex-shrink-0">
                                        <div className="w-44 h-44 rounded-full border-8 border-white/40 flex items-center justify-center bg-white/10 backdrop-blur-sm shadow-2xl">
                                            <div className="text-center">
                                                <div className="text-6xl font-bold mb-1">{creditScore}</div>
                                                <div className="text-sm opacity-90">out of 900</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex-1 text-center md:text-left space-y-4">
                                        <p className="text-green-100 text-lg">
                                            {creditScore >= 750
                                                ? 'Outstanding! You have excellent creditworthiness.'
                                                : creditScore >= 650
                                                    ? 'Good score! You qualify for most loan products.'
                                                    : 'Fair score. Consider improving your financial habits.'}
                                        </p>
                                        <div className="flex flex-wrap gap-3 justify-center md:justify-start">
                                            <button
                                                onClick={handleDownloadReport}
                                                className="bg-white text-green-700 hover:bg-green-50 font-bold px-6 py-3 rounded-xl transition-all shadow-lg flex items-center gap-2"
                                            >
                                                <FileText className="w-5 h-5" />
                                                Download Report
                                            </button>
                                            <button
                                                onClick={handleRegenerateScore}
                                                className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-bold px-6 py-3 rounded-xl transition-all border-2 border-white/40 flex items-center gap-2"
                                            >
                                                <Activity className="w-5 h-5" />
                                                Regenerate
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Quick Stats */}
                    <div className="space-y-4">
                        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                                    <CheckCircle className="w-6 h-6 text-green-600" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-600">Applications</p>
                                    <p className="text-2xl font-bold text-gray-900">{applications?.length || 0}</p>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                                    <Building2 className="w-6 h-6 text-blue-600" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-600">Linked Banks</p>
                                    <p className="text-2xl font-bold text-gray-900">{banks?.length || 0}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Apply for Loan CTA */}
                <div className="mt-6">
                    <button
                        onClick={handleApplyForLoan}
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-5 rounded-2xl transition-all shadow-xl transform hover:scale-[1.02] flex items-center justify-center gap-3 text-lg"
                    >
                        <CreditCard className="w-6 h-6" />
                        Apply for Loan Now
                    </button>
                </div>

                {/* Quick Actions */}
                <div className="mt-8">
                    <h3 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h3>
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                        <button
                            onClick={() => setView('banks')}
                            className="bg-white hover:bg-gradient-to-br hover:from-blue-50 hover:to-blue-100 border-2 border-gray-200 hover:border-blue-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-blue-100 group-hover:bg-blue-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <Building2 className="w-7 h-7 text-blue-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">Bank Accounts</p>
                        </button>

                        <button
                            onClick={() => setView('emi')}
                            className="bg-white hover:bg-gradient-to-br hover:from-orange-50 hover:to-orange-100 border-2 border-gray-200 hover:border-orange-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-orange-100 group-hover:bg-orange-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <CreditCard className="w-7 h-7 text-orange-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">EMI Calculator</p>
                        </button>

                        <button
                            onClick={() => setView('applications')}
                            className="bg-white hover:bg-gradient-to-br hover:from-green-50 hover:to-green-100 border-2 border-gray-200 hover:border-green-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-green-100 group-hover:bg-green-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <FileText className="w-7 h-7 text-green-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">Applications</p>
                        </button>

                        <button
                            onClick={() => setView('rbi')}
                            className="bg-white hover:bg-gradient-to-br hover:from-purple-50 hover:to-purple-100 border-2 border-gray-200 hover:border-purple-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-purple-100 group-hover:bg-purple-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <Shield className="w-7 h-7 text-purple-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">RBI Guidelines</p>
                        </button>
                    </div>
                </div>


                {showReport && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
                        <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                            {/*  Report Modal content */}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ScoreDashboard;
