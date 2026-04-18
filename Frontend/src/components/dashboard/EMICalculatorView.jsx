import React, { useState } from 'react';
import { CreditCard } from 'lucide-react';

const EMICalculator = () => {
    const [loanAmount, setLoanAmount] = useState(500000);
    const [loanTenure, setLoanTenure] = useState(5);
    const [tenureType, setTenureType] = useState('years');
    const [interestRate, setInterestRate] = useState(10.5);

    const calculateEMI = () => {
        const P = loanAmount;
        const r = interestRate / 12 / 100;
        const n = tenureType === 'years' ? loanTenure * 12 : loanTenure;
        if (r === 0) return Math.round(P / n);
        const emi = P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
        return Math.round(emi);
    };

    const calculateTotalInterest = () => {
        const emi = calculateEMI();
        const n = tenureType === 'years' ? loanTenure * 12 : loanTenure;
        const totalPayment = emi * n;
        return Math.round(totalPayment - loanAmount);
    };

    const emi = calculateEMI();
    const totalInterest = calculateTotalInterest();
    const n = tenureType === 'years' ? loanTenure * 12 : loanTenure;
    const totalPayment = emi * n;
    const principalPercentage = (loanAmount / totalPayment) * 100;
    const interestPercentage = 100 - principalPercentage;

    const maxLoanAmount = 1500000; // 15 Lakhs
    const maxTenure = tenureType === 'years' ? 5 : 60;

    const formatCurrency = (amount) => {
        if (amount >= 100000) {
            return `₹ ${(amount / 100000).toFixed(2)} L`;
        } else {
            return `₹ ${amount.toLocaleString('en-IN')}`;
        }
    };

    const handleLoanAmountChange = (e) => {
        const value = Number(e.target.value);
        if (value >= 0 && value <= maxLoanAmount) {
            setLoanAmount(value);
        }
    };

    const handleTenureChange = (e) => {
        const value = Number(e.target.value);
        if (value >= 1 && value <= maxTenure) {
            setLoanTenure(value);
        }
    };

    const handleInterestRateChange = (e) => {
        const value = Number(e.target.value);
        if (value >= 1 && value <= 25) {
            setInterestRate(value);
        }
    };

    const handleTenureTypeChange = (type) => {
        if (type === 'months' && tenureType === 'years') {
            // Convert years to months
            setLoanTenure(loanTenure * 12);
        } else if (type === 'years' && tenureType === 'months') {
            // Convert months to years
            setLoanTenure(Math.ceil(loanTenure / 12));
        }
        setTenureType(type);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 pt-24 pb-8 px-4">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-900 to-indigo-900 mb-2">
                        Personal Loan EMI Calculator
                    </h1>
                    <p className="text-gray-600 text-lg">Calculate your personal loan EMI with ease</p>
                </div>

                <div className="grid lg:grid-cols-2 gap-8">
                    {/* Input Section */}
                    <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-blue-100 hover:shadow-blue-200/50 transition-all duration-300">
                        <div className="flex items-center justify-center gap-3 mb-8">
                            <div className="bg-gradient-to-r from-blue-800 to-blue-900 p-4 rounded-2xl shadow-xl">
                                <CreditCard className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800">Personal Loan</h3>
                        </div>

                        <div className="space-y-8">
                            {/* Loan Amount */}
                            <div>
                                <label className="block text-gray-800 font-bold mb-4 text-lg">Personal Loan Amount</label>
                                <div className="relative mb-4">
                                    <input
                                        type="text"
                                        value={formatCurrency(loanAmount)}
                                        readOnly
                                        className="w-full px-6 py-4 border-2 border-blue-200 rounded-xl text-right text-2xl font-bold bg-gradient-to-r from-blue-50 to-indigo-50"
                                    />
                                </div>
                                <input
                                    type="range"
                                    min="0"
                                    max={maxLoanAmount}
                                    step="10000"
                                    value={loanAmount}
                                    onChange={handleLoanAmountChange}
                                    className="w-full h-3 rounded-lg appearance-none cursor-pointer"
                                    style={{
                                        background: `linear-gradient(to right, #1e40af 0%, #1e3a8a ${(loanAmount / maxLoanAmount) * 100}%, #dbeafe ${(loanAmount / maxLoanAmount) * 100}%, #dbeafe 100%)`
                                    }}
                                />
                                <div className="flex justify-between text-sm text-gray-600 mt-2">
                                    <span>₹0</span>
                                    <span className="text-right">₹15L</span>
                                </div>
                            </div>

                            {/* Loan Tenure */}
                            <div>
                                <label className="block text-gray-800 font-bold mb-4 text-lg">Loan Tenure</label>
                                <div className="flex gap-4 mb-4">
                                    <input
                                        type="number"
                                        value={loanTenure}
                                        onChange={handleTenureChange}
                                        min="1"
                                        max={maxTenure}
                                        className="flex-1 px-6 py-4 border-2 border-blue-200 rounded-xl text-center text-2xl font-bold bg-gradient-to-r from-blue-50 to-indigo-50"
                                    />
                                    <div className="flex rounded-xl overflow-hidden border-2 border-blue-900 shadow-lg">
                                        <button
                                            onClick={() => handleTenureTypeChange('years')}
                                            className={`px-6 py-4 font-bold transition-all duration-300 ${tenureType === 'years'
                                                    ? 'bg-gradient-to-r from-blue-800 to-blue-900 text-white'
                                                    : 'bg-white text-blue-900 hover:bg-blue-50'
                                                }`}
                                        >
                                            Years
                                        </button>
                                        <button
                                            onClick={() => handleTenureTypeChange('months')}
                                            className={`px-6 py-4 font-bold transition-all duration-300 ${tenureType === 'months'
                                                    ? 'bg-gradient-to-r from-blue-800 to-blue-900 text-white'
                                                    : 'bg-white text-blue-900 hover:bg-blue-50'
                                                }`}
                                        >
                                            Months
                                        </button>
                                    </div>
                                </div>
                                <input
                                    type="range"
                                    min="1"
                                    max={maxTenure}
                                    step="1"
                                    value={loanTenure}
                                    onChange={handleTenureChange}
                                    className="w-full h-3 rounded-lg appearance-none cursor-pointer"
                                    style={{
                                        background: `linear-gradient(to right, #1e40af 0%, #1e3a8a ${(loanTenure / maxTenure) * 100}%, #dbeafe ${(loanTenure / maxTenure) * 100}%, #dbeafe 100%)`
                                    }}
                                />
                                <div className="flex justify-between text-sm text-gray-600 mt-2">
                                    <span>1{tenureType === 'years' ? 'Y' : 'M'}</span>
                                    <span>{maxTenure}{tenureType === 'years' ? 'Y' : 'M'}</span>
                                </div>
                            </div>

                            {/* Interest Rate */}
                            <div>
                                <label className="block text-gray-800 font-bold mb-4 text-lg">Interest Rate</label>
                                <div className="relative mb-4">
                                    <input
                                        type="text"
                                        value={`${interestRate.toFixed(1)} %`}
                                        readOnly
                                        className="w-full px-6 py-4 border-2 border-blue-200 rounded-xl text-right text-2xl font-bold bg-gradient-to-r from-blue-50 to-indigo-50"
                                    />
                                </div>
                                <input
                                    type="range"
                                    min="1"
                                    max="25"
                                    step="0.5"
                                    value={interestRate}
                                    onChange={handleInterestRateChange}
                                    className="w-full h-3 rounded-lg appearance-none cursor-pointer"
                                    style={{
                                        background: `linear-gradient(to right, #1e40af 0%, #1e3a8a ${(interestRate / 25) * 100}%, #dbeafe ${(interestRate / 25) * 100}%, #dbeafe 100%)`
                                    }}
                                />
                                <div className="flex justify-between text-sm text-gray-600 mt-2">
                                    <span>1%</span>
                                    <span>25%</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Result Section */}
                    <div className="bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 rounded-3xl p-8 shadow-2xl border-2 border-blue-700">
                        <h3 className="text-3xl font-bold text-white mb-4">Personal Loan EMI</h3>
                        <div className="text-5xl lg:text-6xl font-bold text-yellow-300 mb-8 drop-shadow-lg break-words">
                            ₹ {emi.toLocaleString('en-IN')}
                        </div>

                        <div className="grid grid-cols-2 gap-6 mb-8">
                            <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                                <p className="text-sm text-blue-700 mb-2 font-semibold">Total Interest Payable</p>
                                <p className="text-xl lg:text-2xl font-bold text-blue-900 break-words">
                                    ₹ {totalInterest.toLocaleString('en-IN')}
                                </p>
                            </div>
                            <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                                <p className="text-sm text-blue-700 mb-2 font-semibold">Total Payment<br />(Principal + Interest)</p>
                                <p className="text-xl lg:text-2xl font-bold text-blue-900 break-words">
                                    ₹ {totalPayment.toLocaleString('en-IN')}
                                </p>
                            </div>
                        </div>

                        <div>
                            <h4 className="font-bold text-white mb-6 text-xl">Break-up of Total Payment</h4>
                            <div className="relative w-64 h-64 mx-auto mb-6 bg-white/10 backdrop-blur-sm rounded-full p-4">
                                <svg viewBox="0 0 100 100" className="transform -rotate-90 drop-shadow-2xl">
                                    <circle
                                        cx="50"
                                        cy="50"
                                        r="40"
                                        fill="none"
                                        stroke="#dbeafe"
                                        strokeWidth="20"
                                        strokeDasharray={`${principalPercentage * 2.51} ${251 - principalPercentage * 2.51}`}
                                    />
                                    <circle
                                        cx="50"
                                        cy="50"
                                        r="40"
                                        fill="none"
                                        stroke="#fde047"
                                        strokeWidth="20"
                                        strokeDasharray={`${interestPercentage * 2.51} ${251 - interestPercentage * 2.51}`}
                                        strokeDashoffset={`-${principalPercentage * 2.51}`}
                                    />
                                </svg>
                            </div>
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                                    <div className="w-5 h-5 bg-yellow-300 rounded shadow-lg"></div>
                                    <span className="text-sm text-white font-semibold">Total Interest ({interestPercentage.toFixed(1)}%)</span>
                                </div>
                                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                                    <div className="w-5 h-5 bg-blue-200 rounded shadow-lg"></div>
                                    <span className="text-sm text-white font-semibold">Principal Loan Amount ({principalPercentage.toFixed(1)}%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EMICalculator;