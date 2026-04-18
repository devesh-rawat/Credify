import React from 'react';
import { Shield, Twitter, Linkedin, Github } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-white py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6" />
              </div>
              <span className="text-xl font-bold">Credify</span>
            </div>
            <p className="text-slate-400 text-sm">
              See beyond documents — verify digitally.
            </p>
          </div>

          <div>
            <h3 className="font-bold mb-4">Product</h3>
            <ul className="space-y-2 text-slate-400 text-sm">
              <li><a href="#features" className="hover:text-orange-400 transition-colors">Features</a></li>
              <li><a href="#solution" className="hover:text-orange-400 transition-colors">Solution</a></li>
              <li><a href="#how-it-works" className="hover:text-orange-400 transition-colors">How It Works</a></li>
              <li><Link to="/dashboard" className="hover:text-orange-400 transition-colors">Dashboard</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold mb-4">Company</h3>
            <ul className="space-y-2 text-slate-400 text-sm">
              <li><a href="#team" className="hover:text-orange-400 transition-colors">About Us</a></li>
              <li><a href="#team" className="hover:text-orange-400 transition-colors">Team</a></li>
              <li><a href="#contact" className="hover:text-orange-400 transition-colors">Contact</a></li>
              <li><Link to="/register" className="hover:text-orange-400 transition-colors">Join Us</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold mb-4">Legal</h3>
            <ul className="space-y-2 text-slate-400 text-sm">
              <li><a href="#" className="hover:text-orange-400 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-orange-400 transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-orange-400 transition-colors">Data Security</a></li>
              <li><a href="#" className="hover:text-orange-400 transition-colors">Compliance</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-400 text-sm">
              © 2025 Credify AI. Made with ❤️ in India
            </p>
            <div className="flex gap-4">
              <a 
                href="https://twitter.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-10 h-10 bg-slate-800 hover:bg-blue-600 rounded-full flex items-center justify-center transition-colors"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a 
                href="https://linkedin.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-10 h-10 bg-slate-800 hover:bg-blue-700 rounded-full flex items-center justify-center transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </a>
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-10 h-10 bg-slate-800 hover:bg-gray-700 rounded-full flex items-center justify-center transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;