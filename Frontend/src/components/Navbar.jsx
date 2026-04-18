import React, { useState } from 'react';
import { Menu, X, LogOut, ArrowLeft, ArrowRight, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import credifyLogo from '../assets/credify-logo.jpg';

const Navbar = ({ onNavigate, currentPage }) => {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const goBack = () => {
    navigate(-1);
  };

  const goForward = () => {
    navigate(1);
  };

  const navigation = [
    { name: 'Problem', id: 'problem' },
    { name: 'Solution', id: 'solution' },
    { name: 'Features', id: 'features' },
    { name: 'How It Works', id: 'how-it-works' },
    { name: 'Team', id: 'team' },
    { name: 'Contact', id: 'contact' }
  ];

  const scrollToSection = (sectionId) => {
    setMobileMenuOpen(false);
    if (currentPage !== 'home') {
      onNavigate('home');
      setTimeout(() => {
        const element = document.getElementById(sectionId);
        element?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const element = document.getElementById(sectionId);
      element?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleLogout = () => {
    logout();
    setProfileMenuOpen(false);
    onNavigate('home');
  };

  return (
    <nav className="fixed top-0 w-full bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 text-white shadow-2xl z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-3">
            {/* working Back / Next buttons */}
            <div className="flex items-center gap-2 mr-2">
              <button
                onClick={goBack}
                className="p-2 rounded-lg transition hover:bg-white/10"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <button
                onClick={goForward}
                className="p-2 rounded-lg transition hover:bg-white/10"
              >
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>

            <button
              onClick={() => onNavigate('home')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              <img
                src={credifyLogo}
                alt="Credify Logo"
                className="w-10 h-10 object-contain"
              />
              <span className="text-2xl font-bold">Credify</span>
            </button>
          </div>

          <div className="hidden md:flex items-center gap-6">
            {currentPage === 'home' && !user && navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => scrollToSection(item.id)}
                className="hover:text-blue-300 transition-colors duration-200 font-medium"
              >
                {item.name}
              </button>
            ))}

            {user ? (
              <div className="relative">
                <button
                  onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                  className="bg-blue-600 hover:bg-blue-700 p-2 rounded-full transition-all duration-200"
                >
                  <User className="w-6 h-6 text-white" />
                </button>

                {profileMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-2 text-slate-800 border border-slate-100">
                    <button
                      onClick={handleLogout}
                      className="w-full px-4 py-2 text-left hover:bg-slate-50 flex items-center gap-2 text-red-600 font-medium"
                    >
                      <LogOut className="w-4 h-4" />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={() => onNavigate('login')}
                className="bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 px-6 py-2 rounded-full font-semibold transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                Login / Signup
              </button>
            )}
          </div>

          <button
            className="md:hidden p-2 hover:bg-white/10 rounded-lg"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden bg-slate-800 border-t border-slate-700">
          <div className="px-4 py-3 space-y-3">
            {currentPage === 'home' && !user && navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => scrollToSection(item.id)}
                className="block w-full text-left hover:text-blue-300 py-2 font-medium"
              >
                {item.name}
              </button>
            ))}

            {user ? (
              <button
                onClick={() => {
                  handleLogout();
                  setMobileMenuOpen(false);
                }}
                className="w-full bg-red-500 hover:bg-red-600 px-6 py-2 rounded-full font-semibold flex items-center justify-center gap-2"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            ) : (
              <button
                onClick={() => {
                  onNavigate('login');
                  setMobileMenuOpen(false);
                }}
                className="w-full bg-gradient-to-r from-orange-500 to-orange-600 px-6 py-2 rounded-full font-semibold text-center"
              >
                Login / Signup
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
