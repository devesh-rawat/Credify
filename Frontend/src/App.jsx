import React from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import UserDashboard from './pages/UserDashboard';
import Dashboard from './pages/Dashboard';
import { AuthProvider, useAuth } from './context/AuthContext';
import ChatBot from './chatbot/Chatbot';
import ProtectedRoute from './components/ProtectedRoute';
import PublicRoute from './components/PublicRoute';

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigate = (page) => {
    if (page === 'home') navigate('/');
    else if (page === 'login') navigate('/login');
    else if (page === 'register') navigate('/register');
    else if (page === 'user-dashboard') navigate('/user-dashboard');
    else if (page === 'dashboard') navigate('/dashboard');
    else navigate(page);

    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Wrapper to access auth context for User Dashboard
  const UserDashboardWrapper = () => {
    const { user } = useAuth();
    return <UserDashboard user={user} />;
  };

  // Wrapper to access auth context for Admin Dashboard
  const AdminDashboardWrapper = () => {
    const { user } = useAuth();
    return <Dashboard user={user} />;
  };

  // Determine current page for Navbar
  const getCurrentPage = () => {
    const path = location.pathname;
    if (path === '/') return 'home';
    if (path === '/login') return 'login';
    if (path === '/register') return 'register';
    if (path.startsWith('/user-dashboard')) return 'user-dashboard';
    if (path.startsWith('/dashboard')) return 'dashboard';
    return 'home';
  };

  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col bg-white relative">
        {/* Navbar */}
        <Navbar onNavigate={handleNavigate} currentPage={getCurrentPage()} />

        {/* Page Routing */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home onNavigate={handleNavigate} />} />

            {/* Public Routes (only accessible if NOT logged in) */}
            <Route path="/login" element={
              <PublicRoute>
                <Login onNavigate={handleNavigate} />
              </PublicRoute>
            } />
            <Route path="/register" element={
              <PublicRoute>
                <Register onNavigate={handleNavigate} />
              </PublicRoute>
            } />

            {/* Protected Routes (only accessible if logged in) */}
            <Route path="/user-dashboard/*" element={
              <ProtectedRoute>
                <UserDashboardWrapper />
              </ProtectedRoute>
            } />

            {/* Admin Route */}
            <Route path="/dashboard" element={
              <ProtectedRoute adminOnly={true}>
                <AdminDashboardWrapper />
              </ProtectedRoute>
            } />
          </Routes>
        </main>

        {/* Chatbot globally visible on all pages */}
        <ChatBot />
      </div>
    </AuthProvider>
  );
};

export default App;