import React, { useState } from 'react';
import { useUser } from '../../contexts/UserContext';
import AuthModal from './AuthModal';

export default function AuthWrapper({ children }) {
  const { isAuthenticated, isLoading } = useUser();
  const [showAuthModal, setShowAuthModal] = useState(false);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-ai-dark">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-primary mx-auto"></div>
          <p className="text-white mt-4">Loading AI Browser...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-ai-dark via-slate-800 to-ai-dark">
        <div className="text-center max-w-md mx-auto px-6">
          <div className="ai-glow-strong rounded-2xl p-8 bg-gray-900/50 backdrop-blur-xl border border-gray-700">
            <h1 className="text-4xl font-bold text-white mb-4">
              AI Agentic Browser
            </h1>
            <p className="text-gray-300 mb-8">
              Experience the future of browsing with AI-powered automation, bubble tabs, and intelligent assistance.
            </p>
            <button
              onClick={() => setShowAuthModal(true)}
              className="w-full bg-gradient-to-r from-ai-primary to-ai-secondary text-white py-3 px-6 rounded-lg font-semibold hover:opacity-90 transition-opacity"
            >
              Get Started
            </button>
            <div className="mt-4 text-sm text-gray-400">
              No account? We'll create one for you!
            </div>
          </div>
        </div>
        
        {showAuthModal && (
          <AuthModal onClose={() => setShowAuthModal(false)} />
        )}
      </div>
    );
  }

  return children;
}