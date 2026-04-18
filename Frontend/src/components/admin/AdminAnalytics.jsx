import React from 'react';
import { BarChart3 } from 'lucide-react';

const AdminAnalytics = () => {
    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="text-center py-8">
                <BarChart3 className="w-16 h-16 text-blue-500 mx-auto mb-4" />
                <h3 className="text-3xl font-bold text-slate-900 mb-2">Analytics & Insights</h3>
                <p className="text-slate-600">Performance metrics and system overview</p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100">
                    <p className="text-sm font-semibold text-slate-500 mb-1">Model Accuracy (R²)</p>
                    <p className="text-4xl font-bold text-blue-600 mb-2">97.9%</p>
                    <p className="text-xs text-slate-600 font-medium">Test Set Performance</p>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100">
                    <p className="text-sm font-semibold text-slate-500 mb-1">Mean Absolute Error</p>
                    <p className="text-4xl font-bold text-green-600 mb-2">23.2</p>
                    <p className="text-xs text-slate-600 font-medium">Score Points Deviation</p>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100">
                    <p className="text-sm font-semibold text-slate-500 mb-1">Training Samples</p>
                    <p className="text-4xl font-bold text-purple-600 mb-2">1,050</p>
                    <p className="text-xs text-slate-600 font-medium">840 Train + 210 Test</p>
                </div>
            </div>

            {/* Admin Guide */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-100">
                <h4 className="text-xl font-bold text-slate-900 mb-6">Admin Guide</h4>
                <div className="grid md:grid-cols-2 gap-8">
                    <div>
                        <h5 className="font-semibold text-slate-800 mb-3">Reviewing Applications</h5>
                        <ul className="space-y-3 text-slate-600 text-sm">
                            <li className="flex gap-2">
                                <span className="text-blue-500 font-bold">•</span>
                                Check the Trust Score and Risk Label first.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-blue-500 font-bold">•</span>
                                Read the AI Summary for a quick overview.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-blue-500 font-bold">•</span>
                                Verify income stability in Key Factors.
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h5 className="font-semibold text-slate-800 mb-3">Making Decisions</h5>
                        <ul className="space-y-3 text-slate-600 text-sm">
                            <li className="flex gap-2">
                                <span className="text-green-500 font-bold">•</span>
                                Approve: High score (&gt;750), Low Risk, Stable Income.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-yellow-500 font-bold">•</span>
                                Review: Medium score, specific risk factors flagged.
                            </li>
                            <li className="flex gap-2">
                                <span className="text-red-500 font-bold">•</span>
                                Reject: Low score, high default probability.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Project Info */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 text-white">
                <h4 className="text-xl font-bold mb-4">About Credify AI</h4>
                <p className="text-slate-300 mb-6 leading-relaxed">
                    Credify uses a Random Forest machine learning model to assess creditworthiness beyond traditional credit scores.
                    Our model analyzes 50 features including transaction patterns, income stability, debt ratios, and spending behavior to provide a holistic financial profile with 300-900 score range.
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 border-t border-slate-700 pt-6">
                    <div>
                        <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Model Type</p>
                        <p className="font-mono font-bold">Random Forest</p>
                    </div>
                    <div>
                        <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Estimators</p>
                        <p className="font-mono font-bold">200 Trees</p>
                    </div>
                    <div>
                        <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Features</p>
                        <p className="font-mono font-bold">50 Total</p>
                    </div>
                    <div>
                        <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Last Trained</p>
                        <p className="font-mono font-bold">Nov 2025</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminAnalytics;
