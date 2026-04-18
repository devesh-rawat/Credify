import React, { useState } from 'react';
import { ArrowLeft, Shield, CheckCircle, Lock, IndianRupee, Loader2 } from 'lucide-react';
import { apiRequest, API_ENDPOINTS } from '../../config';

const KYCVerification = ({ setStep, aadhar, setAadhar, pan, setPan, loanAmount, setLoanAmount }) => {
    const [loading, setLoading] = useState(false);

    const handleVerify = async () => {
        try {
            setLoading(true);
            const response = await apiRequest(API_ENDPOINTS.REQUEST_OTP, {
                method: 'POST',
                body: JSON.stringify({
                    aadhaar: aadhar,
                    pan,
                    loan_amount: parseFloat(loanAmount)
                })
            });

            if (response.ok) {
                setStep('otp');
            } else {
                const errorData = await response.json();
                alert(errorData.detail || 'Failed to send OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error requesting OTP:', error);
            alert('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-2xl mx-auto">
                <button onClick={() => setStep('consent')} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10">
                    <div className="text-center mb-8">
                        <div className="w-24 h-24 bg-gradient-to-br from-green-500 to-green-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <Shield className="w-12 h-12 text-white" />
                        </div>
                        <h2 className="text-3xl font-bold text-gray-900 mb-3">Identity Verification</h2>
                        <p className="text-gray-600">Please provide your KYC details for verification</p>
                    </div>

                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-bold text-gray-900 mb-3">Aadhaar Number</label>
                            <div className="relative">
                                <input
                                    type="text"
                                    value={aadhar}
                                    onChange={(e) => setAadhar(e.target.value.replace(/\D/g, '').slice(0, 12))}
                                    className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:bg-white focus:outline-none text-gray-900 text-lg transition-all"
                                    placeholder="Enter 12-digit Aadhaar"
                                    maxLength="12"
                                />
                                {aadhar.length === 12 && (
                                    <CheckCircle className="absolute right-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-green-500" />
                                )}
                            </div>
                            <p className="text-xs text-gray-500 mt-2">Your Aadhaar is encrypted and secure</p>
                        </div>

                        <div>
                            <label className="block text-sm font-bold text-gray-900 mb-3">PAN Number</label>
                            <div className="relative">
                                <input
                                    type="text"
                                    value={pan}
                                    onChange={(e) => setPan(e.target.value.toUpperCase().slice(0, 10))}
                                    className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:bg-white focus:outline-none text-gray-900 text-lg transition-all uppercase"
                                    placeholder="ABCDE1234F"
                                    maxLength="10"
                                />
                                {pan.length === 10 && (
                                    <CheckCircle className="absolute right-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-green-500" />
                                )}
                            </div>
                            <p className="text-xs text-gray-500 mt-2">Format: 5 letters, 4 digits, 1 letter</p>
                        </div>

                        <div>
                            <label className="block text-sm font-bold text-gray-900 mb-3">Loan Amount Required</label>
                            <div className="relative">
                                <div className="absolute left-5 top-1/2 transform -translate-y-1/2">
                                    <IndianRupee className="w-5 h-5 text-gray-500" />
                                </div>
                                <input
                                    type="number"
                                    value={loanAmount}
                                    onChange={(e) => setLoanAmount(e.target.value)}
                                    className="w-full pl-12 pr-5 py-4 bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:bg-white focus:outline-none text-gray-900 text-lg transition-all"
                                    placeholder="Enter amount"
                                />
                            </div>
                        </div>

                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                            <div className="flex items-start gap-3">
                                <Lock className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                <p className="text-sm text-blue-900">
                                    We use government-verified KYC to ensure secure and legitimate credit assessment
                                </p>
                            </div>
                        </div>

                        <button
                            onClick={handleVerify}
                            disabled={aadhar.length !== 12 || pan.length !== 10 || !loanAmount || loading}
                            className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02] disabled:transform-none flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Verifying...
                                </>
                            ) : (
                                'Verify Identity'
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default KYCVerification;
