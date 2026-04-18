import React from 'react';
import { ArrowLeft, User, TrendingUp, CheckCircle, LogOut } from 'lucide-react';

const ProfileMenu = ({ user, setShowProfileMenu, creditScore, aadhar, pan, banks }) => {
    return (
        <div
            className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-2 z-50"
            onClick={() => setShowProfileMenu(false)}
        >
            <div
                className="w-full max-w-sm bg-white rounded-2xl shadow-2xl overflow-hidden scale-95"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header with Back Button */}
                <div className="bg-gray-100 px-3 py-2 flex items-center gap-2 border-b border-gray-200">
                    <button
                        onClick={() => setShowProfileMenu(false)}
                        className="p-1.5 hover:bg-gray-200 rounded-full transition-all"
                    >
                        <ArrowLeft className="w-4 h-4 text-gray-700" />
                    </button>
                    <h3 className="font-bold text-gray-900 text-sm">Profile</h3>
                </div>

                {/* Blue Gradient Card with User Info */}
                <div className="p-4">
                    <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-5 text-white shadow-lg">
                        <div className="text-center">
                            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-3 shadow">
                                <User className="w-8 h-8 text-blue-600" />
                            </div>
                            <h2 className="text-lg font-bold mb-2">{user?.name || 'User Name'}</h2>
                            <div className="space-y-1 text-blue-100 text-xs">
                                <p>
                                    <span className="font-medium">Aadhaar:</span> {aadhar || '•••• •••• ••••'}
                                </p>
                                <p>
                                    <span className="font-medium">PAN:</span> {pan || '••••••••••'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Credit Score Row */}
                <div className="px-4 pb-2">
                    <div className="bg-white border-2 border-gray-200 rounded-lg p-3 flex items-center justify-between hover:border-blue-300 transition-all">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                <TrendingUp className="w-4 h-4 text-blue-600" />
                            </div>
                            <span className="text-gray-700 font-semibold text-sm">Credit Score</span>
                        </div>
                        <span className="text-xl font-bold text-blue-600">{creditScore || '—'}</span>
                    </div>
                </div>

                {/* KYC Status Row */}
                <div className="px-4 pb-2">
                    <div className="bg-white border-2 border-gray-200 rounded-lg p-3 flex items-center justify-between hover:border-blue-300 transition-all">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                <CheckCircle className="w-4 h-4 text-blue-600" />
                            </div>
                            <span className="text-gray-700 font-semibold text-sm">KYC Status</span>
                        </div>
                        <span className="text-blue-600 font-bold text-sm">{(aadhar && pan) ? 'Verified' : 'Not Verified'}</span>
                    </div>
                </div>

                {/* Linked Bank Accounts Section */}
                <div className="px-4 pb-3">
                    <h4 className="text-gray-500 font-semibold mb-2 text-center text-xs">Linked Bank Accounts</h4>
                    <div className="space-y-2">
                        {banks.slice(0, 2).map((bank) => (
                            <div
                                key={bank.id}
                                className="bg-white border-2 border-gray-200 rounded-lg p-3 flex items-center justify-between hover:border-blue-300 transition-all"
                            >
                                <div className="flex items-center gap-2">
                                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-base">
                                        {bank.logo}
                                    </div>
                                    <div>
                                        <p className="font-semibold text-gray-900 text-xs">{bank.name}</p>
                                        <p className="text-[10px] text-gray-500">{bank.type}</p>
                                    </div>
                                </div>
                                <p className="text-gray-600 font-mono text-xs">{bank.account}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Email Section */}
                <div className="px-4 pb-2">
                    <div className="bg-gray-50 rounded-lg p-3">
                        <p className="text-[10px] text-gray-500 mb-1">Email Address</p>
                        <p className="font-semibold text-gray-900 text-xs">{user?.email || 'user@credify.com'}</p>
                    </div>
                </div>

                {/* Logout Button */}
                <div className="p-4 pt-0">
                    <button
                        onClick={() => {
                            // Clear authentication data
                            localStorage.removeItem('authToken');
                            localStorage.removeItem('user');
                            // Redirect to login page
                            window.location.href = '/';
                        }}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 rounded-lg text-white font-bold text-sm shadow-md"
                    >
                        <LogOut className="w-4 h-4" />
                        Log Out
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ProfileMenu;
