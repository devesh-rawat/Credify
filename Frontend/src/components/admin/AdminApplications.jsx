import React from 'react';
import { FileText } from 'lucide-react';

const AdminApplications = () => {
    return (
        <div className="text-center py-12">
            <FileText className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-slate-900 mb-2">All Applications</h3>
            <p className="text-slate-600">View and manage all loan applications</p>
        </div>
    );
};

export default AdminApplications;
