import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PublicRoute = ({ children }) => {
    const { token, isAdmin, loading } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (token) {
        // If user is already logged in, redirect to appropriate dashboard
        if (isAdmin) {
            return <Navigate to="/dashboard" replace />;
        }
        return <Navigate to="/user-dashboard" replace />;
    }

    return children;
};

export default PublicRoute;
