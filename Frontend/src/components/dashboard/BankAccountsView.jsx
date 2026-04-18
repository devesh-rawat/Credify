import React from 'react';
import { ArrowLeft } from 'lucide-react';

const BankAccountsView = ({ setView, banks }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-4xl mx-auto">
                <button onClick={() => setView('dashboard')} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-3">Your Linked Accounts</h2>
                    <p className="text-gray-600 mb-8">
                        These accounts are used to fetch statements for credit analysis
                    </p>

                    <div className="space-y-4">
                        {banks.map((bank) => (
                            <div
                                key={bank.id}
                                className="border-2 border-gray-200 hover:border-blue-300 rounded-2xl p-6 transition-all hover:shadow-lg"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center text-3xl shadow-md flex-shrink-0">
                                        {bank.logo}
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="font-bold text-gray-900 text-lg mb-2">{bank.name}</h3>
                                        <div className="grid grid-cols-2 gap-2 text-sm">
                                            <p className="text-gray-600">
                                                <span className="font-medium">Account:</span> {bank.account}
                                            </p>
                                            <p className="text-gray-600">
                                                <span className="font-medium">Type:</span> {bank.type}
                                            </p>
                                            <p className="text-gray-600">
                                                <span className="font-medium">IFSC:</span> {bank.ifsc}
                                            </p>
                                            <p className="text-gray-600">
                                                <span className="font-medium">Branch:</span> {bank.branch}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex-shrink-0">
                                        <span className="bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-semibold">
                                            Active
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BankAccountsView;
