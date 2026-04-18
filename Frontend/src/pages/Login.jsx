import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { API_ENDPOINTS } from '../config';
import credifyLogo from '../assets/credify-logo.jpg';

const LoginPage = ({ onNavigate }) => {
  const { login } = useAuth();
  const [loginType, setLoginType] = useState('user');
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validatePassword = (password) => {
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasSpecial = /[@_]/.test(password);
    return password.length >= 6 && hasLetter && hasSpecial;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Please fill in all fields!');
      return;
    }

    if (!validatePassword(formData.password)) {
      setError('Password must be at least 6 characters and contain letters and @_ symbols');
      return;
    }

    setLoading(true);

    try {
      const endpoint = loginType === 'admin' ? API_ENDPOINTS.ADMIN_LOGIN : API_ENDPOINTS.USER_LOGIN;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Prepare user data
      const userData = {
        user_id: data.user_id,
        email: formData.email,
        full_name: data.full_name || (loginType === 'admin' ? 'Admin' : 'User'),
        role: data.role || loginType,
      };

      // Login with token
      login(userData, data.access_token, loginType === 'admin');

      // Navigate to appropriate dashboard
      if (loginType === 'admin') {
        onNavigate('dashboard');
      } else {
        onNavigate('user-dashboard');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-20 pb-12 px-4 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          {/* ✅ Only logo above the heading */}
          <img
            src={credifyLogo}
            alt="Credify Logo"
            className="mx-auto w-24 h-24 rounded-full shadow-lg mb-6 object-cover"
          />

          <h1 className="text-4xl font-bold text-slate-900 mb-2">Welcome Back</h1>
          <p className="text-slate-600">Sign in to your account</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex gap-2 mb-6 bg-slate-100 rounded-lg p-1">
            <button
              onClick={() => setLoginType('user')}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${loginType === 'user'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-slate-600 hover:bg-slate-200'
                }`}
              disabled={loading}
            >
              User
            </button>
            <button
              onClick={() => setLoginType('admin')}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${loginType === 'admin'
                  ? 'bg-slate-700 text-white shadow-md'
                  : 'text-slate-600 hover:bg-slate-200'
                }`}
              disabled={loading}
            >
              Admin
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Email Address</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none"
                placeholder="john@company.com"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none"
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 shadow-lg ${loading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
            >
              {loading ? 'Signing In...' : `Sign In as ${loginType === 'admin' ? 'Admin' : 'User'}`}
            </button>
          </form>

          {loginType === 'user' && (
            <div className="mt-6 text-center">
              <p className="text-slate-600">
                Don't have an account?{' '}
                <button
                  onClick={() => onNavigate('register')}
                  className="text-blue-600 hover:text-blue-700 font-semibold"
                  disabled={loading}
                >
                  Register
                </button>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
