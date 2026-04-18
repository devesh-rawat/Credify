import React, { useState, useEffect } from 'react';
import { apiRequest, API_ENDPOINTS } from '../config';
import ApplicationDetailsModal from '../components/admin/ApplicationDetailsModal';
import AdminStats from '../components/admin/AdminStats';
import AdminOverview from '../components/admin/AdminOverview';
import AdminAnalytics from '../components/admin/AdminAnalytics';
import AdminSettings from '../components/admin/AdminSettings';

const AdminDashboard = ({ user, onUpdateApplications }) => {
  const [activeTab, setActiveTab] = useState('applications');
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [applications, setApplications] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setIsLoading(true);
      const response = await apiRequest(API_ENDPOINTS.ADMIN_APPLICATIONS);

      if (!response.ok) {
        throw new Error('Failed to fetch applications');
      }

      const data = await response.json();

      // Map backend data to frontend format
      const mappedApps = data.map(app => ({
        id: app.application_id,
        name: app.user_details?.name || app.user_id, // Fallback if name not available
        email: app.user_details?.email || 'N/A',
        score: app.scoring_details?.credit_score || 0,
        amount: `₹${app.amount.toLocaleString()}`,
        status: app.status.charAt(0).toUpperCase() + app.status.slice(1).toLowerCase(), // Capitalize
        time: new Date(app.created_at).toLocaleDateString(), // Simple formatting
        // Keep original data for details view
        originalData: app
      }));

      setApplications(mappedApps);
    } catch (err) {
      console.error('Failed to fetch applications:', err);
      setError('Failed to load applications. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDecision = async (appId, status, notes = '') => {
    try {
      const response = await apiRequest(API_ENDPOINTS.ADMIN_DECISION(appId), {
        method: 'POST',
        body: JSON.stringify({ status, notes }),
      });

      if (!response.ok) {
        throw new Error('Failed to update application status');
      }

      // Update local state
      const updatedApps = applications.map(app =>
        app.id === appId ? { ...app, status: status.charAt(0) + status.slice(1).toLowerCase() } : app
      );
      setApplications(updatedApps);

      if (onUpdateApplications) {
        onUpdateApplications(updatedApps);
      }

      alert(`Application ${appId} has been ${status.toLowerCase()}!`);
    } catch (err) {
      console.error(`Failed to ${status.toLowerCase()} application:`, err);
      alert(`Failed to ${status.toLowerCase()} application. Please try again.`);
    }
  };

  const handleApprove = (appId) => handleDecision(appId, 'APPROVED');
  const handleReject = (appId) => handleDecision(appId, 'REJECTED');

  const handleViewDetails = (app) => {
    setSelectedApplication(app);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Approved': return 'bg-green-100 text-green-700';
      case 'Pending': return 'bg-yellow-100 text-yellow-700';
      case 'Rejected': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  // Application Details Modal
  if (selectedApplication) {
    return (
      <ApplicationDetailsModal
        application={selectedApplication}
        onClose={() => setSelectedApplication(null)}
        onApprove={handleApprove}
        onReject={handleReject}
        getStatusColor={getStatusColor}
        getScoreColor={getScoreColor}
      />
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-2">
            Welcome back, {user?.name || 'Admin'}!
          </h1>
          <p className="text-slate-600">
            Here's your lending dashboard overview
          </p>
        </div>

        {/* Stats Grid */}
        <AdminStats applications={applications} />

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-8">
          <div className="border-b border-slate-200">
            <div className="flex gap-1 p-2 overflow-x-auto">
              {['applications', 'analytics', 'settings'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 sm:px-6 py-3 rounded-lg font-semibold transition-all duration-200 capitalize whitespace-nowrap text-sm sm:text-base ${activeTab === tab
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-600 hover:bg-slate-100'
                    }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>

          <div className="p-4 sm:p-6">
            {activeTab === 'applications' && (
              <AdminOverview
                applications={applications}
                onViewDetails={handleViewDetails}
                onApprove={handleApprove}
                onReject={handleReject}
                getStatusColor={getStatusColor}
                getScoreColor={getScoreColor}
              />
            )}

            {activeTab === 'analytics' && (
              <AdminAnalytics />
            )}

            {activeTab === 'settings' && (
              <AdminSettings user={user} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;