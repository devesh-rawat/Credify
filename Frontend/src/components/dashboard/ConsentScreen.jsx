import React from 'react';
import { ArrowLeft, Lock, Building2, TrendingUp, FileText, CheckCircle } from 'lucide-react';

const ConsentScreen = ({ setStep, setView }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-2xl mx-auto">
                <button onClick={() => {
                    setStep('initial');
                    setView('dashboard');
                }} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10">
                    <div className="text-center mb-8">
                        <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <Lock className="w-12 h-12 text-white" />
                        </div>
                        <h2 className="text-3xl font-bold text-gray-900 mb-3">Data Access Consent</h2>
                        <p className="text-gray-600 max-w-md mx-auto">
                            To generate your credit score, we need your permission to securely access your financial data
                        </p>
                    </div>

                    <div className="space-y-4 mb-8">
                        <div className="bg-gradient-to-r from-blue-50 to-blue-100 border border-blue-200 rounded-2xl p-5 flex items-start gap-4">
                            <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center flex-shrink-0">
                                <Building2 className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <p className="font-bold text-gray-900 mb-1">Bank Transactions</p>
                                <p className="text-sm text-gray-700">Access your transaction history to verify income patterns</p>
                            </div>
                        </div>

                        <div className="bg-gradient-to-r from-green-50 to-green-100 border border-green-200 rounded-2xl p-5 flex items-start gap-4">
                            <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center flex-shrink-0">
                                <TrendingUp className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <p className="font-bold text-gray-900 mb-1">Financial Profile</p>
                                <p className="text-sm text-gray-700">Analyze spending patterns and payment discipline</p>
                            </div>
                        </div>

                        <div className="bg-gradient-to-r from-purple-50 to-purple-100 border border-purple-200 rounded-2xl p-5 flex items-start gap-4">
                            <div className="w-12 h-12 bg-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
                                <FileText className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <p className="font-bold text-gray-900 mb-1">Identity Verification</p>
                                <p className="text-sm text-gray-700">Securely verify your identity with government documents</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-green-50 border-2 border-green-300 rounded-2xl p-4 mb-6">
                        <div className="flex items-start gap-3">
                            <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
                            <div>
                                <p className="font-bold text-green-900 mb-1">Your data is safe</p>
                                <p className="text-sm text-green-800">
                                    Bank-grade encryption • DPDP compliant • No data sharing without consent
                                </p>
                            </div>
                        </div>
                    </div>

                    <label className="flex items-start gap-3 cursor-pointer mb-6 p-4 hover:bg-gray-50 rounded-xl transition-colors">
                        <input type="checkbox" className="mt-1 w-5 h-5 text-blue-600 rounded" defaultChecked />
                        <span className="text-sm text-gray-700 leading-relaxed">
                            I authorize Credify to access my financial data for credit assessment. I understand this data will be used solely for generating my trust score and will be handled in accordance with RBI guidelines and data protection laws.
                        </span>
                    </label>

                    <button
                        onClick={() => setStep('kyc')}
                        className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02]"
                    >
                        I Agree - Continue
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConsentScreen;
