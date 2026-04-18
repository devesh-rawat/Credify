import React from 'react';
import { ArrowLeft, FileText } from 'lucide-react';

const ApplicationsView = ({ setView, applications, user }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-24 pb-12 px-4">
            <div className="max-w-5xl mx-auto">
                <button onClick={() => setView('dashboard')} className="mb-6 p-2 hover:bg-white rounded-lg transition-all">
                    <ArrowLeft className="w-6 h-6" />
                </button>

                <div className="bg-white rounded-3xl shadow-2xl p-8">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900">Your Loan Applications</h2>
                            <p className="text-gray-600 mt-2">Track the status of your loan applications</p>
                        </div>
                        <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full">
                            <span className="font-bold">{applications.length}</span> Application{applications.length !== 1 ? 's' : ''}
                        </div>
                    </div>

                    {applications.length === 0 ? (
                        <div className="text-center py-16">
                            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <FileText className="w-12 h-12 text-gray-400" />
                            </div>
                            <h3 className="text-2xl font-bold text-gray-900 mb-3">No Applications Yet</h3>
                            <p className="text-gray-600 mb-8">Start by generating your Credify score and apply for loans</p>
                            <button
                                onClick={() => setView('dashboard')}
                                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold px-8 py-4 rounded-xl transition-all shadow-lg transform hover:scale-[1.02]"
                            >
                                Go to Dashboard
                            </button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {applications.map((app) => (
                                <div key={app.id} className="bg-gradient-to-r from-white to-blue-50 border-2 border-blue-200 rounded-2xl p-6 hover:shadow-xl transition-all">
                                    <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-4">
                                        <div className="flex items-center gap-4">
                                            <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">
                                                {user.name.split(' ').map(n => n[0]).join('')}
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500 font-medium mb-1">Application ID</p>
                                                <p className="font-bold text-gray-900 text-lg font-mono">{app.id}</p>
                                            </div>
                                        </div>
                                        <div className={`px-5 py-2 rounded-full text-sm font-bold shadow-md ${app.status === 'Approved' ? 'bg-green-500 text-white' :
                                                app.status === 'Pending' ? 'bg-yellow-500 text-white' :
                                                    'bg-red-500 text-white'
                                            }`}>
                                            {app.status}
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-3 gap-6">
                                        <div className="bg-white rounded-xl p-4 shadow-md">
                                            <p className="text-sm text-gray-500 mb-1">Trust Score</p>
                                            <p className="text-3xl font-bold text-blue-600">{app.score}</p>
                                        </div>
                                        <div className="bg-white rounded-xl p-4 shadow-md">
                                            <p className="text-sm text-gray-500 mb-1">Amount</p>
                                            <p className="text-xl font-bold text-gray-900">{app.amount}</p>
                                        </div>
                                        <div className="bg-white rounded-xl p-4 shadow-md">
                                            <p className="text-sm text-gray-500 mb-1">Applied</p>
                                            <p className="text-sm text-gray-700 font-medium">{app.time}</p>
                                            <p className="text-xs text-gray-500 mt-1">{app.date}</p>
                                        </div>
                                    </div>

                                    <div className="mt-4 bg-gray-50 rounded-xl p-4">
                                        <p className="text-sm text-gray-700">
                                            <span className="font-bold">Applicant:</span> {app.applicant || user.name}
                                        </p>
                                        <p className="text-sm text-gray-700 mt-1">
                                            <span className="font-bold">Email:</span> {app.email || user.email}
                                        </p>
                                        {app.status === 'Pending' && (
                                            <p className="text-xs text-gray-500 mt-3 italic">
                                                ⏳ Your application is under review. Admin will approve/reject soon.
                                            </p>
                                        )}
                                        {app.status === 'Approved' && (
                                            <p className="text-xs text-green-700 mt-3 font-semibold">
                                                ✅ Congratulations! Your loan has been approved.
                                            </p>
                                        )}
                                        {app.status === 'Rejected' && (
                                            <p className="text-xs text-red-700 mt-3 font-semibold">
                                                ❌ Your application was not approved. Please contact support.
                                            </p>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ApplicationsView;
