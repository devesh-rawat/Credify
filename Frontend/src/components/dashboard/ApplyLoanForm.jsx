import React, { useState, useEffect } from 'react';
import { X, Building2, CreditCard, FileText, AlertCircle } from 'lucide-react';
import { API_ENDPOINTS, apiRequest } from '../../config';

const ApplyLoanForm = ({ user, loanAmount: initialLoanAmount, onClose, onSuccess }) => {
    const [selectedAccount, setSelectedAccount] = useState('');
    const [amount, setAmount] = useState(initialLoanAmount || '');
    const [purpose, setPurpose] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [banks, setBanks] = useState([]);
    const [isLoadingBanks, setIsLoadingBanks] = useState(true);

    useEffect(() => {
        // Fetch AA banks
        const fetchBanks = async () => {
            setIsLoadingBanks(true);
            try {
                const response = await apiRequest(API_ENDPOINTS.BANKS);
                if (response.ok) {
                    const banksData = await response.json();
                    setBanks(banksData);
                    // Auto-select first bank account if available
                    if (banksData && banksData.length > 0) {
                        setSelectedAccount(banksData[0].account_id);
                    }
                } else {
                    setError('Failed to load bank accounts');
                }
            } catch (err) {
                setError('Network error. Please try again.');
            } finally {
                setIsLoadingBanks(false);
            }
        };

        fetchBanks();
    }, []);

    const validateForm = () => {
        if (!selectedAccount) {
            setError('Please select a bank account');
            return false;
        }
        if (!amount || parseFloat(amount) <= 0) {
            setError('Please enter a valid loan amount');
            return false;
        }
        if (!purpose || purpose.trim().length < 5) {
            setError('Purpose must be at least 5 characters');
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateForm()) return;

        setIsSubmitting(true);

        try {
            const response = await apiRequest(API_ENDPOINTS.APPLICATIONS_APPLY, {
                method: 'POST',
                body: JSON.stringify({
                    account_id: selectedAccount,
                    amount: parseFloat(amount),
                    purpose: purpose.trim()
                })
            });

            if (response.ok) {
                const data = await response.json();
                onSuccess && onSuccess(data);
                onClose();
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Failed to submit application');
            }
        } catch (err) {
            setError('Network error. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                {/* Header */}
                <div className="sticky top-0 bg-white border-b border-gray-200 px-8 py-6 flex items-center justify-between rounded-t-3xl">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Apply for Loan</h2>
                        <p className="text-sm text-gray-500 mt-1">Fill in the details below to apply for a new loan</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-xl transition-all"
                    >
                        <X className="w-6 h-6 text-gray-500" />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-8 space-y-6">
                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
                            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                            <p className="text-sm text-red-800">{error}</p>
                        </div>
                    )}

                    {/* Bank Account Selection */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-900 mb-2">
                            Select Bank Account
                        </label>
                        {isLoadingBanks ? (
                            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-center gap-3">
                                <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                                <p className="text-sm text-blue-800">Loading bank accounts...</p>
                            </div>
                        ) : banks && banks.length > 0 ? (
                            <div className="relative">
                                <Building2 className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <select
                                    value={selectedAccount}
                                    onChange={(e) => setSelectedAccount(e.target.value)}
                                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all bg-gray-50"
                                    required
                                >
                                    {banks.map((bank) => (
                                        <option key={bank.account_id} value={bank.account_id}>
                                            {bank.bank_name} - {bank.account_number?.slice(-4) || 'N/A'}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        ) : (
                            <div className="bg-orange-50 border border-orange-200 rounded-xl p-4 flex items-start gap-3">
                                <AlertCircle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
                                <p className="text-sm text-orange-800">
                                    No linked bank accounts found. Please link a bank account first.
                                </p>
                            </div>
                        )}
                    </div>

                    {/* Loan Amount */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-900 mb-2">
                            Loan Amount (₹)
                        </label>
                        <div className="relative">
                            <CreditCard className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="number"
                                value={amount}
                                readOnly
                                className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl bg-gray-200 cursor-not-allowed text-gray-700"
                                required
                            />
                        </div>
                        <p className="text-xs text-gray-500 mt-2">Amount entered during KYC verification</p>
                    </div>

                    {/* Purpose */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-900 mb-2">
                            Purpose of Loan
                        </label>
                        <div className="relative">
                            <FileText className="absolute left-4 top-4 w-5 h-5 text-gray-400" />
                            <textarea
                                value={purpose}
                                onChange={(e) => setPurpose(e.target.value)}
                                placeholder="e.g. Home renovation, Education, Business expansion, etc."
                                className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all bg-gray-50 resize-none"
                                rows="3"
                                required
                                minLength="5"
                            />
                        </div>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isSubmitting || isLoadingBanks || !banks || banks.length === 0}
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02] disabled:transform-none disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {isSubmitting ? (
                            <>
                                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                Submitting...
                            </>
                        ) : (
                            'Submit Application'
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ApplyLoanForm;
