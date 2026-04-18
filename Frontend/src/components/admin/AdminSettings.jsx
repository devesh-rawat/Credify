import React from 'react';
import { Shield } from 'lucide-react';

const AdminSettings = ({ user }) => {
    return (
        <div className="text-center py-12">
            <Shield className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Settings</h3>
            <p className="text-slate-600 mb-8">Configure your account and preferences</p>
            <div className="space-y-4 max-w-md mx-auto text-left">
                <div className="bg-slate-50 rounded-lg p-4">
                    <span className="font-semibold text-slate-900 text-sm sm:text-base">Name: {user?.name || 'Admin User'}</span>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                    <span className="font-semibold text-slate-900 text-sm sm:text-base break-all">Email: {user?.email || 'admin@credify.com'}</span>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                    <span className="font-semibold text-slate-900 text-sm sm:text-base">Role: {user?.role || 'Administrator'}</span>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                    <span className="font-semibold text-slate-900 text-sm sm:text-base">Admin ID: {user?.user_id || 'ADM-001'}</span>
                </div>
            </div>
        </div>
    );
};

export default AdminSettings;
