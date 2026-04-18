import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Shield, TrendingUp, Clock, Users, CheckCircle, AlertTriangle,
  BarChart3, Zap, Lock, Award, ChevronRight, X
} from 'lucide-react';

const Home = ({ onNavigate }) => {
  const { user } = useAuth();
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    company: '',
    message: ''
  });

  const handleContactSubmit = () => {
    if (contactForm.name && contactForm.email && contactForm.message) {
      alert('Message sent! We will get back to you soon.');
      setContactForm({ name: '', email: '', company: '', message: '' });
    } else {
      alert('Please fill in all required fields.');
    }
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    element?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section id="home" className="py-20 px-4 bg-gradient-to-br from-slate-50 via-white to-blue-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h1 className="text-5xl md:text-6xl font-bold text-slate-900 leading-tight">
                Unlock Credit for All
              </h1>
              <p className="text-2xl text-slate-600 font-medium">
                See beyond documents — verify digitally.
              </p>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => onNavigate(user ? 'dashboard' : 'login')}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 flex items-center gap-2 shadow-lg"
                >
                  {user ? 'View Profile' : 'Start Now'}
                  <ChevronRight className="w-5 h-5" />
                </button>
                <button
                  onClick={() => scrollToSection('features')}
                  className="border-2 border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-4 rounded-lg font-semibold transition-all duration-200"
                >
                  Learn More
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-blue-900 to-slate-900 rounded-2xl p-8 shadow-2xl">
                <div className="relative">
                  <Shield className="w-32 h-32 text-blue-400 mx-auto mb-4 opacity-90" />
                  <div className="absolute inset-0 bg-blue-400 blur-3xl opacity-20"></div>
                </div>
                <div className="space-y-4 mt-6">
                  <div className="flex items-center gap-3 text-white">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                    <span className="text-lg">AI-Powered Trust Scoring</span>
                  </div>
                  <div className="flex items-center gap-3 text-white">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                    <span className="text-lg">Instant Verification</span>
                  </div>
                  <div className="flex items-center gap-3 text-white">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                    <span className="text-lg">DPDP & RBI Compliant</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="problem" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">The Credit Invisibility Challenge</h2>
            <p className="text-xl md:text-2xl text-slate-600">70% of India's workforce is locked out of credit</p>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-8 border-2 border-red-200 shadow-lg">
              <div className="flex items-center gap-3 mb-6">
                <AlertTriangle className="w-10 h-10 text-red-600" />
                <h3 className="text-2xl md:text-3xl font-bold text-slate-900">Credit Invisible</h3>
              </div>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 bg-white rounded-xl flex items-center justify-center shadow-md">
                    <span className="text-xl font-bold text-red-600">₹1.2L</span>
                  </div>
                  <p className="text-lg text-slate-700 font-medium">Cr Unmet Demand</p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 bg-white rounded-xl flex items-center justify-center shadow-md">
                    <span className="text-xl font-bold text-red-600">18-22%</span>
                  </div>
                  <p className="text-lg text-slate-700 font-medium">NPA Risk</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 border-2 border-blue-200 shadow-lg">
              <div className="flex items-center gap-3 mb-6">
                <Users className="w-10 h-10 text-blue-600" />
                <h3 className="text-2xl md:text-3xl font-bold text-slate-900">Excluded Groups</h3>
              </div>
              <ul className="space-y-4 text-slate-700">
                <li className="flex items-start gap-3">
                  <X className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                  <span className="text-lg">No CIBIL score or credit history</span>
                </li>
                <li className="flex items-start gap-3">
                  <X className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                  <span className="text-lg">No formal payslips or income proof</span>
                </li>
                <li className="flex items-start gap-3">
                  <X className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                  <span className="text-lg">Rejected despite being creditworthy</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="solution" className="py-20 px-4 bg-gradient-to-br from-slate-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">Credify: AI-Powered Trust Scoring</h2>
            <p className="text-xl md:text-2xl text-blue-200">Convert digital behavior into verified creditworthiness</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 hover:bg-white/20 transition-all duration-200 transform hover:scale-105 border border-white/20">
              <div className="w-16 h-16 bg-blue-500 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <Shield className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-3">Trust Score AI Engine</h3>
              <p className="text-blue-100">Advanced ML models analyze income patterns, digital behavior, and utility payments</p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 hover:bg-white/20 transition-all duration-200 transform hover:scale-105 border border-white/20">
              <div className="w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <BarChart3 className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-3">Instant Onboarding</h3>
              <p className="text-blue-100">UPI, wallet & bill data aggregation provides instant verification without paperwork</p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 hover:bg-white/20 transition-all duration-200 transform hover:scale-105 border border-white/20">
              <div className="w-16 h-16 bg-purple-500 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <Award className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-3">RBI Compliant</h3>
              <p className="text-blue-100">GDPR & DPDP compliant architecture ensures regulatory readiness</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">Features</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow duration-200 border border-gray-100">
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center">
                    <Shield className="w-7 h-7 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Income Verification</h3>
                </div>
                <p className="text-slate-600 text-lg">90+ lenders & fintech integration friendly</p>
              </div>

              <div className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow duration-200 border border-gray-100">
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-14 h-14 bg-green-100 rounded-xl flex items-center justify-center">
                    <TrendingUp className="w-7 h-7 text-green-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Instant Onboarding</h3>
                </div>
                <p className="text-slate-600 text-lg">Sessions threshold management</p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow duration-200 border border-gray-100">
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-14 h-14 bg-purple-100 rounded-xl flex items-center justify-center">
                    <BarChart3 className="w-7 h-7 text-purple-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Lender Dashboard</h3>
                </div>
                <p className="text-slate-600 text-lg">Realtime decisioning workspace</p>
              </div>

              <div className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow duration-200 border border-gray-100">
                <div className="flex items-center gap-4 mb-3">
                  <div className="w-14 h-14 bg-orange-100 rounded-xl flex items-center justify-center">
                    <Clock className="w-7 h-7 text-orange-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Decision Time</h3>
                </div>
                <p className="text-slate-600 text-lg">2-3 hrs faster manual credit</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-3xl font-bold shadow-lg">
                1
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 shadow-lg border border-blue-200">
                <Users className="w-10 h-10 text-blue-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-900 mb-2 text-lg">User Consent</h3>
                <p className="text-sm text-slate-600">Link financial data</p>
              </div>
            </div>

            <div className="text-center">
              <div className="w-24 h-24 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-3xl font-bold shadow-lg">
                2
              </div>
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 shadow-lg border border-green-200">
                <Zap className="w-10 h-10 text-green-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-900 mb-2 text-lg">Data Extraction</h3>
                <p className="text-sm text-slate-600">2 Data Annotation</p>
              </div>
            </div>

            <div className="text-center">
              <div className="w-24 h-24 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-3xl font-bold shadow-lg">
                3
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 shadow-lg border border-purple-200">
                <Shield className="w-10 h-10 text-purple-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-900 mb-2 text-lg">AI Scoring</h3>
                <p className="text-sm text-slate-600">2 Rollout</p>
              </div>
            </div>

            <div className="text-center">
              <div className="w-24 h-24 bg-orange-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-3xl font-bold shadow-lg">
                4
              </div>
              <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-6 shadow-lg border border-orange-200">
                <Award className="w-10 h-10 text-orange-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-900 mb-2 text-lg">Decision</h3>
                <p className="text-sm text-slate-600">Lender approval</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">Impact</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-10 border-2 border-green-300 shadow-xl">
              <h3 className="text-6xl md:text-7xl font-bold text-green-600 mb-4">+25%</h3>
              <p className="text-xl text-slate-700 mb-2 font-semibold">Approval Uplift</p>
              <p className="text-slate-600 text-lg">Default reduction via verified income</p>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-10 border-2 border-blue-300 shadow-xl">
              <h3 className="text-6xl md:text-7xl font-bold text-blue-600 mb-4">-15%</h3>
              <p className="text-xl text-slate-700 mb-2 font-semibold">Default Reduction</p>
              <p className="text-slate-600 text-lg">2 Days → 2 Mins Decision Time</p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">About Us / Team</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-8 shadow-xl text-center hover:shadow-2xl transition-shadow duration-200 border border-blue-200">
              <div className="w-28 h-28 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                AE
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-1">Aasam Evansan</h3>
              <p className="text-slate-600 font-medium">CEO & Co-Founder</p>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-8 shadow-xl text-center hover:shadow-2xl transition-shadow duration-200 border border-green-200">
              <div className="w-28 h-28 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                CS
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-1">Chad Start</h3>
              <p className="text-slate-600 font-medium">CTO</p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-8 shadow-xl text-center hover:shadow-2xl transition-shadow duration-200 border border-purple-200">
              <div className="w-28 h-28 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-3xl font-bold shadow-lg">
                L
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-1">Lender</h3>
              <p className="text-slate-600 font-medium">Business Head</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">Testimonials / Proof & Validation</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-2xl p-8 border-l-4 border-blue-600 shadow-xl">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                  GK
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">Gig Worker</h3>
                  <p className="text-sm text-slate-600">Delivery Partner</p>
                </div>
              </div>
              <p className="text-slate-700 italic text-lg">"Finally got loan approval after 3 rejections. Credify verified my UPI earnings in minutes!"</p>
            </div>

            <div className="bg-white rounded-2xl p-8 border-l-4 border-green-600 shadow-xl">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                  SM
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">Samantha Moore</h3>
                  <p className="text-sm text-slate-600">10 Years from NBFCs</p>
                </div>
              </div>
              <p className="text-slate-700 italic text-lg">"Reduced onboarding by 87% and cut defaults by 15%. Game changer!"</p>
            </div>
          </div>
        </div>
      </section>

      {/* Risks & Mitigations */}
      <section className="py-20 px-4 bg-gradient-to-br from-slate-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-12">Risks & Mitigations</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="flex items-center gap-3 mb-3 text-red-300">
                <AlertTriangle className="w-6 h-6" />
                <h3 className="font-bold text-lg">Data Privacy</h3>
              </div>
              <div className="flex items-center gap-3 text-green-300">
                <Shield className="w-6 h-6" />
                <p className="text-sm">Consent & Anonymization</p>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="flex items-center gap-3 mb-3 text-red-300">
                <AlertTriangle className="w-6 h-6" />
                <h3 className="font-bold text-lg">Bias</h3>
              </div>
              <div className="flex items-center gap-3 text-green-300">
                <CheckCircle className="w-6 h-6" />
                <p className="text-sm">Fairness Audits</p>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="flex items-center gap-3 mb-3 text-red-300">
                <AlertTriangle className="w-6 h-6" />
                <h3 className="font-bold text-lg">Regulatory</h3>
              </div>
              <div className="flex items-center gap-3 text-green-300">
                <Lock className="w-6 h-6" />
                <p className="text-sm">DPDP & RBI Compliant</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 bg-white">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-900 mb-12">Contact</h2>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-2xl p-8 border border-blue-200">
            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Name *</label>
                  <input
                    type="text"
                    value={contactForm.name}
                    onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Email *</label>
                  <input
                    type="email"
                    value={contactForm.email}
                    onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
                    placeholder="your@email.com"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Company</label>
                <input
                  type="text"
                  value={contactForm.company}
                  onChange={(e) => setContactForm({ ...contactForm, company: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
                  placeholder="Your company"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Message *</label>
                <textarea
                  rows="4"
                  value={contactForm.message}
                  onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
                  placeholder="Tell us about your lending needs..."
                ></textarea>
              </div>
              <button
                onClick={handleContactSubmit}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                Send Message
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;