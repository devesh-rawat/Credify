import React from 'react';
import { ArrowLeft, Check, X, FileText } from 'lucide-react';
import { API_ENDPOINTS } from '../../config';

const ApplicationDetailsModal = ({
    application,
    onClose,
    onApprove,
    onReject,
    getStatusColor,
    getScoreColor
}) => {
    if (!application) return null;

    const scoringDetails = application.originalData?.scoring_details;

    return (
        <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
            <div className="max-w-4xl mx-auto">
                <button
                    onClick={onClose}
                    className="mb-6 p-2 hover:bg-white rounded-lg transition-all flex items-center gap-2"
                >
                    <ArrowLeft className="w-6 h-6" />
                    <span className="font-semibold">Back to Applications</span>
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-4 sm:p-8">
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
                        <div>
                            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Application Details</h2>
                            <p className="text-gray-600">ID: {application.id}</p>
                        </div>
                        <div className={`px-5 py-2 rounded-full text-sm font-bold ${getStatusColor(application.status)}`}>
                            {application.status}
                        </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6 mb-8">
                        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                                    {application.name.split(' ').map(n => n[0]).join('')}
                                </div>
                                <div>
                                    <p className="text-xs text-gray-600 mb-1">Applicant Name</p>
                                    <p className="font-bold text-gray-900 text-lg sm:text-xl">{application.name}</p>
                                </div>
                            </div>
                            <div className="space-y-3">
                                <div>
                                    <p className="text-xs text-gray-600 mb-1">Email Address</p>
                                    <p className="font-semibold text-gray-900 break-all">{application.email}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-gray-600 mb-1">Application Time</p>
                                    <p className="font-semibold text-gray-900">{application.time}</p>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border border-green-200">
                                <p className="text-sm text-gray-600 mb-2">Trust Score</p>
                                <p className={`text-5xl font-bold ${getScoreColor(application.score)}`}>
                                    {application.score}
                                </p>
                                <p className="text-xs text-gray-600 mt-2">out of 100</p>
                            </div>

                            <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-6 border border-orange-200">
                                <p className="text-sm text-gray-600 mb-2">Loan Amount</p>
                                <p className="text-3xl font-bold text-gray-900">{application.amount}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-gray-50 rounded-2xl p-6 mb-8">
                        <h3 className="font-bold text-gray-900 mb-4 text-lg">Financial Profile</h3>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Risk Label</p>
                                <p className="font-bold text-gray-900">
                                    {application.originalData?.scoring_details?.risk_label ||
                                        (application.score >= 75 ? 'Low Risk' : application.score >= 60 ? 'Medium Risk' : 'High Risk')}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Recommendation</p>
                                <p className="font-bold text-gray-900">
                                    {application.originalData?.scoring_details?.recommendation ||
                                        (application.score >= 75 ? 'APPROVE' : 'REVIEW')}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Default Probability</p>
                                <p className="font-bold text-gray-900">
                                    {scoringDetails?.default_probability
                                        ? `${(scoringDetails.default_probability * 100).toFixed(1)}%`
                                        : 'N/A'}
                                </p>
                            </div>
                        </div>

                        {/* AI Summary */}
                        {scoringDetails?.summary && (
                            <div className="mt-4 pt-4 border-t border-gray-200">
                                <p className="text-xs text-gray-500 mb-2 font-semibold uppercase tracking-wider">AI Summary</p>
                                <p className="text-sm text-gray-700 leading-relaxed">
                                    {scoringDetails.summary}
                                </p>
                            </div>
                        )}

                        {/* Key Factors */}
                        {scoringDetails?.key_factors && scoringDetails.key_factors.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-gray-200">
                                <p className="text-xs text-gray-500 mb-2 font-semibold uppercase tracking-wider">Key Factors</p>
                                <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {scoringDetails.key_factors.map((factor, index) => (
                                        <li key={index}>{typeof factor === 'string' ? factor : factor.factor || JSON.stringify(factor)}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Recommendations */}
                        {scoringDetails?.recommendations && scoringDetails.recommendations.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-gray-200">
                                <p className="text-xs text-gray-500 mb-2 font-semibold uppercase tracking-wider">Recommendations</p>
                                <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {scoringDetails.recommendations.map((rec, index) => (
                                        <li key={index}>{typeof rec === 'string' ? rec : rec.text || JSON.stringify(rec)}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Underwriting Notes */}
                        {scoringDetails?.underwriting_note && scoringDetails.underwriting_note.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-gray-200">
                                <p className="text-xs text-gray-500 mb-2 font-semibold uppercase tracking-wider">Underwriting Notes</p>
                                <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {scoringDetails.underwriting_note.map((note, index) => (
                                        <li key={index}>{note}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Download Report Button */}
                        {scoringDetails?.report_path && (
                            <div className="mt-6 pt-4 border-t border-gray-200 flex justify-end">
                                <button
                                    onClick={() => {
                                        const filename = scoringDetails.report_path.split('/').pop();
                                        window.open(API_ENDPOINTS.REPORTS_DOWNLOAD(filename), '_blank');
                                    }}
                                    className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors font-semibold text-sm"
                                >
                                    <FileText className="w-4 h-4" />
                                    Download Full Report
                                </button>
                            </div>
                        )}
                    </div>

                    {application.status === 'Pending' && (
                        <div className="flex flex-col sm:flex-row gap-4">
                            <button
                                onClick={() => onApprove(application.id)}
                                className="flex-1 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02] flex items-center justify-center gap-2"
                            >
                                <Check className="w-5 h-5" />
                                Approve Application
                            </button>
                            <button
                                onClick={() => onReject(application.id)}
                                className="flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02] flex items-center justify-center gap-2"
                            >
                                <X className="w-5 h-5" />
                                Reject Application
                            </button>
                        </div>
                    )}

                    {application.status !== 'Pending' && (
                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center">
                            <p className="text-blue-900 font-semibold">
                                This application has already been {application.status.toLowerCase()}.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ApplicationDetailsModal;
