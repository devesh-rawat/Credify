import React from 'react';
import { Search, Eye, Check, X } from 'lucide-react';

const AdminOverview = ({
    applications,
    onViewDetails,
    onApprove,
    onReject,
    getStatusColor,
    getScoreColor
}) => {
    return (
        <div className="space-y-6">
            {/* Search Bar */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
                <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search applications by ID, name, or email..."
                        className="w-full pl-10 pr-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none text-sm sm:text-base"
                    />
                </div>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200">
                    Search
                </button>
            </div>

            {/* Recent Applications */}
            <div>
                <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-4">Recent Applications</h2>

                {/* Desktop Table View */}
                <div className="hidden lg:block overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b-2 border-slate-200">
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">ID</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Applicant</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Trust Score</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Amount</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Status</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Time</th>
                                <th className="text-left py-3 px-4 font-semibold text-slate-700">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {applications.map((app) => (
                                <tr key={app.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="py-4 px-4">
                                        <span className="font-mono text-sm text-slate-600">{app.id}</span>
                                    </td>
                                    <td className="py-4 px-4">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                                                {app.name.split(' ').map(n => n[0]).join('')}
                                            </div>
                                            <span className="font-semibold text-slate-900">{app.name}</span>
                                        </div>
                                    </td>
                                    <td className="py-4 px-4">
                                        <span className={`text-2xl font-bold ${getScoreColor(app.score)}`}>
                                            {app.score}
                                        </span>
                                    </td>
                                    <td className="py-4 px-4">
                                        <span className="font-semibold text-slate-900">{app.amount}</span>
                                    </td>
                                    <td className="py-4 px-4">
                                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(app.status)}`}>
                                            {app.status}
                                        </span>
                                    </td>
                                    <td className="py-4 px-4">
                                        <span className="text-slate-600 text-sm">{app.time}</span>
                                    </td>
                                    <td className="py-4 px-4">
                                        {app.status === 'Pending' ? (
                                            <div className="flex flex-wrap gap-2">
                                                <button
                                                    onClick={() => onViewDetails(app)}
                                                    className="flex items-center gap-1 bg-blue-500 hover:bg-blue-600 text-white px-3 py-1.5 rounded-lg font-semibold text-sm transition-all duration-200"
                                                >
                                                    <Eye className="w-4 h-4" />
                                                    View
                                                </button>
                                                <button
                                                    onClick={() => onApprove(app.id)}
                                                    className="flex items-center gap-1 bg-green-500 hover:bg-green-600 text-white px-3 py-1.5 rounded-lg font-semibold text-sm transition-all duration-200"
                                                >
                                                    <Check className="w-4 h-4" />
                                                    Approve
                                                </button>
                                                <button
                                                    onClick={() => onReject(app.id)}
                                                    className="flex items-center gap-1 bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg font-semibold text-sm transition-all duration-200"
                                                >
                                                    <X className="w-4 h-4" />
                                                    Reject
                                                </button>
                                            </div>
                                        ) : (
                                            <button
                                                onClick={() => onViewDetails(app)}
                                                className="text-blue-600 hover:text-blue-700 font-semibold text-sm hover:underline"
                                            >
                                                View Details
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Mobile Card View */}
                <div className="lg:hidden space-y-4">
                    {applications.map((app) => (
                        <div key={app.id} className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
                            <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                                        {app.name.split(' ').map(n => n[0]).join('')}
                                    </div>
                                    <div>
                                        <p className="font-bold text-slate-900">{app.name}</p>
                                        <p className="text-xs font-mono text-slate-500">{app.id}</p>
                                    </div>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-xs font-bold ${getStatusColor(app.status)}`}>
                                    {app.status}
                                </span>
                            </div>

                            <div className="grid grid-cols-2 gap-3 mb-3">
                                <div>
                                    <p className="text-xs text-slate-500 mb-1">Trust Score</p>
                                    <p className={`text-2xl font-bold ${getScoreColor(app.score)}`}>{app.score}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500 mb-1">Amount</p>
                                    <p className="text-xl font-bold text-slate-900">{app.amount}</p>
                                </div>
                            </div>

                            <div className="text-xs text-slate-500 mb-3">{app.time}</div>

                            {app.status === 'Pending' ? (
                                <div className="flex flex-col gap-2">
                                    <button
                                        onClick={() => onViewDetails(app)}
                                        className="flex items-center justify-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-200 w-full"
                                    >
                                        <Eye className="w-4 h-4" />
                                        View Details
                                    </button>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => onApprove(app.id)}
                                            className="flex-1 flex items-center justify-center gap-1 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-200"
                                        >
                                            <Check className="w-4 h-4" />
                                            Approve
                                        </button>
                                        <button
                                            onClick={() => onReject(app.id)}
                                            className="flex-1 flex items-center justify-center gap-1 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-200"
                                        >
                                            <X className="w-4 h-4" />
                                            Reject
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                <button
                                    onClick={() => onViewDetails(app)}
                                    className="w-full text-blue-600 hover:text-blue-700 font-semibold text-sm hover:underline text-center py-2"
                                >
                                    View Details
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdminOverview;
