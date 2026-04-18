import React from 'react';
import { Menu, Shield, Zap, CheckCircle, Building2, CreditCard, FileText, Award } from 'lucide-react';
import ProfileMenu from './ProfileMenu';

const InitialDashboard = ({
    user,
    showProfileMenu,
    setShowProfileMenu,
    setStep,
    applications,
    banks,
    setView,
    creditScore,
    aadhar,
    pan
}) => {
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
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
                    <div>
                        <p className="text-sm text-gray-500 mb-1">Welcome back,</p>
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
                    <div className="lg:col-span-2">
                        <div className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 rounded-3xl p-8 md:p-10 text-white shadow-2xl relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-32 -mt-32"></div>
                            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-5 rounded-full -ml-24 -mb-24"></div>

                            <div className="relative z-10">
                                <div className="flex items-center gap-3 mb-6">
                                    <Shield className="w-8 h-8" />
                                    <h2 className="text-2xl font-bold">Credify Score</h2>
                                </div>

                                <div className="flex flex-col md:flex-row items-center gap-8">
                                    <div className="flex-shrink-0">
                                        <div className="w-40 h-40 rounded-full border-8 border-white/30 flex items-center justify-center bg-white/10 backdrop-blur-sm">
                                            <div className="text-center">
                                                <div className="text-6xl font-bold mb-1">—</div>
                                                <div className="text-sm opacity-80">Not Generated</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex-1 text-center md:text-left">
                                        <h3 className="text-xl font-semibold mb-3">Generate Your Trust Score</h3>
                                        <p className="text-blue-100 mb-6 max-w-md">
                                            Get instant credit evaluation based on your financial behavior and unlock better loan offers.
                                        </p>
                                        <button
                                            onClick={() => setStep('consent')}
                                            className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl transition-all shadow-lg transform hover:scale-105 inline-flex items-center gap-2"
                                        >
                                            <Zap className="w-5 h-5" />
                                            Generate Score Now
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                                    <CheckCircle className="w-6 h-6 text-green-600" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-600">Applications</p>
                                    <p className="text-2xl font-bold text-gray-900">{applications.length}</p>
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
                                    <p className="text-2xl font-bold text-gray-900">{banks.length}</p>
                                </div>
                            </div>
                        </div>
                    </div>
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
                            <p className="text-xs text-gray-500 mt-1">Manage linked banks</p>
                        </button>

                        <button
                            onClick={() => setView('emi')}
                            className="bg-white hover:bg-gradient-to-br hover:from-orange-50 hover:to-orange-100 border-2 border-gray-200 hover:border-orange-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-orange-100 group-hover:bg-orange-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <CreditCard className="w-7 h-7 text-orange-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">EMI Calculator</p>
                            <p className="text-xs text-gray-500 mt-1">Plan your loan</p>
                        </button>

                        <button
                            onClick={() => setView('applications')}
                            className="bg-white hover:bg-gradient-to-br hover:from-green-50 hover:to-green-100 border-2 border-gray-200 hover:border-green-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-green-100 group-hover:bg-green-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <FileText className="w-7 h-7 text-green-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">Applications</p>
                            <p className="text-xs text-gray-500 mt-1">Track status</p>
                        </button>

                        <button
                            onClick={() => setView('rbi')}
                            className="bg-white hover:bg-gradient-to-br hover:from-purple-50 hover:to-purple-100 border-2 border-gray-200 hover:border-purple-300 rounded-2xl p-6 transition-all shadow-md hover:shadow-xl group"
                        >
                            <div className="w-14 h-14 bg-purple-100 group-hover:bg-purple-200 rounded-xl flex items-center justify-center mb-4 mx-auto transition-colors">
                                <Shield className="w-7 h-7 text-purple-600" />
                            </div>
                            <p className="text-sm font-bold text-gray-900">RBI Guidelines</p>
                            <p className="text-xs text-gray-500 mt-1">Know your rights</p>
                        </button>
                    </div>
                </div>

                {/* Info Banner */}
                <div className="mt-8 bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 rounded-2xl p-6">
                    <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0">
                            <Award className="w-6 h-6 text-indigo-600" />
                        </div>
                        <div>
                            <h4 className="font-bold text-gray-900 mb-2">Why Credify Score?</h4>
                            <p className="text-sm text-gray-700 mb-3">
                                Get loans without traditional documents. Our AI analyzes your financial behavior to generate a trust score that lenders accept.
                            </p>
                            <div className="flex flex-wrap gap-2">
                                <span className="text-xs bg-white px-3 py-1 rounded-full text-gray-700 font-medium">No salary slips needed</span>
                                <span className="text-xs bg-white px-3 py-1 rounded-full text-gray-700 font-medium">Instant verification</span>
                                <span className="text-xs bg-white px-3 py-1 rounded-full text-gray-700 font-medium">RBI compliant</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default InitialDashboard;
