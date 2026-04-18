import React from 'react';
import { FileText, CheckCircle, Clock, XCircle } from 'lucide-react';

const AdminStats = ({ applications }) => {
    const stats = [
        {
            title: 'Applications Today',
            value: applications.length.toString(),
            change: '+12%',
            icon: FileText,
            color: 'blue'
        },
        {
            title: 'Approved',
            value: applications.filter(app => app.status === 'Approved').length.toString(),
            change: '+8%',
            icon: CheckCircle,
            color: 'green'
        },
        {
            title: 'Pending Review',
            value: applications.filter(app => app.status === 'Pending').length.toString(),
            change: '-3%',
            icon: Clock,
            color: 'yellow'
        },
        {
            title: 'Rejected',
            value: applications.filter(app => app.status === 'Rejected').length.toString(),
            change: '-15%',
            icon: XCircle,
            color: 'red'
        },
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => {
                const Icon = stat.icon;
                const colorClasses = {
                    blue: 'bg-blue-100 text-blue-600',
                    green: 'bg-green-100 text-green-600',
                    yellow: 'bg-yellow-100 text-yellow-600',
                    red: 'bg-red-100 text-red-600'
                };

                return (
                    <div key={index} className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-200">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${colorClasses[stat.color]}`}>
                                <Icon className="w-6 h-6" />
                            </div>
                            <span className={`text-sm font-semibold ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                                {stat.change}
                            </span>
                        </div>
                        <h3 className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</h3>
                        <p className="text-slate-600 text-sm">{stat.title}</p>
                    </div>
                );
            })}
        </div>
    );
};

export default AdminStats;
