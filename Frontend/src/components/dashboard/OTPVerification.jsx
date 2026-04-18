import React, { useState } from 'react';
import { ArrowLeft, Phone, Loader2 } from 'lucide-react';
import { apiRequest, API_ENDPOINTS } from '../../config';

const OTPVerification = ({
    setStep,
    otp,
    setOtp,
    otpInputs,
    handleOtpChange,
    handleOtpKeyDown,
    setCreditScore,
    setView,
    user,
    aadhar, // Assuming aadhar is passed down or available in context/props
    setScoreGenerating
}) => {
    const [loading, setLoading] = useState(false);

    const handleVerify = async () => {
        let success = false;
        try {
            setLoading(true);
            const otpValue = otp.join('');

            // 1. Verify OTP
            const verifyRes = await apiRequest(API_ENDPOINTS.VERIFY_OTP, {
                method: 'POST',
                body: JSON.stringify({
                    aadhaar: aadhar, // Use aadhaar from prop
                    otp: otpValue
                })
            });

            if (verifyRes.ok) {
                success = true;
                // 2. Fetch Credit Score
                // Poll for score or wait a bit as scoring might be async background task
                // For now, let's try to fetch immediately, if not ready, maybe show a "processing" state or just the score if available

                // Trigger parent loading state for score generation animation
                if (setScoreGenerating) {
                    setScoreGenerating(true);
                }

                // Wait a moment for background task to potentially start/finish (optional, better to have polling or socket)
                await new Promise(resolve => setTimeout(resolve, 2000));

                const scoreRes = await apiRequest(API_ENDPOINTS.SCORING_ME);
                if (scoreRes.ok) {
                    const scoreData = await scoreRes.json();
                    setCreditScore(scoreData.credit_score);
                } else {
                    // If score not ready yet, maybe set a default or handle accordingly
                    // For demo, let's assume it might take a moment or use a placeholder if 404
                    console.log("Score might be generating...");
                    // You might want to navigate to a "Processing" screen here instead
                }

                // Turn off parent loading state after we have the score or handled it
                if (setScoreGenerating) {
                    setScoreGenerating(false);
                }

                setStep('initial');
                // setView('dashboard'); // Removed as it navigates to incorrect route
            } else {
                const errorData = await verifyRes.json();
                alert(errorData.detail || 'Invalid OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error verifying OTP:', error);
            alert('An error occurred. Please try again.');
        } finally {
            if (!success) {
                setLoading(false);
            }
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-2xl mx-auto">
                <button onClick={() => setStep('kyc')} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10">
                    <div className="text-center mb-8">
                        <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-purple-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                            <Phone className="w-12 h-12 text-white" />
                        </div>
                        <h2 className="text-3xl font-bold text-gray-900 mb-3">Verify OTP</h2>
                        <p className="text-gray-600">
                            Enter the 6-digit code sent to<br />
                            <span className="font-semibold text-gray-900">{user?.email}</span>
                        </p>
                    </div>

                    <div className="mb-8">
                        <div className="flex gap-3 justify-center mb-6">
                            {otp.map((digit, index) => (
                                <input
                                    key={index}
                                    ref={(el) => (otpInputs.current[index] = el)}
                                    type="text"
                                    value={digit}
                                    onChange={(e) => handleOtpChange(index, e.target.value)}
                                    onKeyDown={(e) => handleOtpKeyDown(index, e)}
                                    maxLength="1"
                                    className="w-14 h-16 text-center text-2xl font-bold bg-gray-100 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:bg-white focus:outline-none text-gray-900 transition-all"
                                />
                            ))}
                        </div>
                    </div>

                    <button
                        onClick={handleVerify}
                        disabled={otp.some(digit => !digit) || loading}
                        className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02] disabled:transform-none flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" />
                                Verifying...
                            </>
                        ) : (
                            'Verify & Generate Score'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default OTPVerification;
