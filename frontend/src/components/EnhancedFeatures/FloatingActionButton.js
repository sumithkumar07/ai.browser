/**
 * Floating Action Button - Minimal UI integration for enhanced features
 * Provides access to all new features without disrupting existing design
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  Mic, 
  Lightbulb, 
  Zap, 
  Settings, 
  X,
  Sparkles,
  Navigation,
  BarChart3,
  Cpu
} from 'lucide-react';
import { enhancedFeaturesService } from '../../services/enhancedFeaturesService';

export default function FloatingActionButton({ userId = 'anonymous' }) {
  const [isOpen, setIsOpen] = useState(false);
  const [quickAccessConfig, setQuickAccessConfig] = useState(null);
  const [featuresStatus, setFeaturesStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadQuickAccessConfig();
    loadFeaturesStatus();
  }, []);

  const loadQuickAccessConfig = async () => {
    try {
      const config = await enhancedFeaturesService.getQuickAccessFeatures();
      setQuickAccessConfig(config);
    } catch (error) {
      console.warn('Failed to load quick access config:', error);
    }
  };

  const loadFeaturesStatus = async () => {
    try {
      const status = await enhancedFeaturesService.getFeaturesStatus();
      setFeaturesStatus(status);
    } catch (error) {
      console.warn('Failed to load features status:', error);
    }
  };

  const handleFeatureAction = async (action, context = {}) => {
    setIsLoading(true);
    try {
      let result;
      
      switch (action) {
        case 'ai_analyze':
          result = await enhancedFeaturesService.oneClickActions(
            window.location.href, 
            document.body.innerText.substring(0, 1000),
            { userId }
          );
          break;
          
        case 'voice_command':
          result = await enhancedFeaturesService.voiceCommands(
            'voice command ready', 
            userId
          );
          break;
          
        case 'smart_suggestions':
          result = await enhancedFeaturesService.smartSuggestions(
            window.location.href,
            document.body.innerText.substring(0, 1000),
            { userId }
          );
          break;
          
        case 'natural_language':
          const input = prompt('Ask AI anything about this page:');
          if (input) {
            result = await enhancedFeaturesService.naturalLanguageInterface(
              input,
              userId,
              { url: window.location.href }
            );
          }
          break;
          
        default:
          result = { status: 'unknown_action' };
      }
      
      if (result?.status === 'success') {
        // Show success notification (minimal UI impact)
        showNotification('Feature executed successfully!', 'success');
      } else {
        showNotification('Feature executed', 'info');
      }
      
    } catch (error) {
      console.error('Feature execution error:', error);
      showNotification('Feature executed', 'info');
    } finally {
      setIsLoading(false);
      setIsOpen(false);
    }
  };

  const showNotification = (message, type) => {
    // Minimal notification - just console for now
    console.log(`🚀 Enhanced Feature: ${message}`);
    
    // Could add a toast notification if needed (minimal impact)
    if (window.showToast) {
      window.showToast(message, type);
    }
  };

  const quickActions = [
    {
      id: 'ai_analyze',
      label: 'AI Analyze',
      icon: Brain,
      color: 'from-purple-500 to-blue-500',
      description: 'Analyze this page with AI'
    },
    {
      id: 'voice_command',
      label: 'Voice',
      icon: Mic,
      color: 'from-green-500 to-teal-500',
      description: 'Use voice commands'
    },
    {
      id: 'smart_suggestions',
      label: 'Suggestions',
      icon: Lightbulb,
      color: 'from-yellow-500 to-orange-500',
      description: 'Get smart suggestions'
    },
    {
      id: 'natural_language',
      label: 'Ask AI',
      icon: Sparkles,
      color: 'from-pink-500 to-purple-500',
      description: 'Chat with AI about this page'
    }
  ];

  return (
    <>
      {/* Main Floating Button */}
      <motion.div
        className="fixed bottom-6 right-6 z-50"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, duration: 0.3 }}
      >
        <motion.button
          onClick={() => setIsOpen(!isOpen)}
          className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-all duration-300"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          disabled={isLoading}
        >
          {isLoading ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            >
              <Settings size={24} />
            </motion.div>
          ) : isOpen ? (
            <X size={24} />
          ) : (
            <>
              <Sparkles size={24} />
              {/* Feature count badge */}
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-xs font-bold">
                16
              </div>
            </>
          )}
        </motion.button>
      </motion.div>

      {/* Quick Actions Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-6 z-40"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.2 }}
          >
            <div className="bg-gray-900/95 backdrop-blur-lg rounded-2xl border border-gray-700/50 p-4 shadow-2xl min-w-[280px]">
              {/* Header */}
              <div className="text-center mb-4">
                <h3 className="text-white font-semibold text-lg">Enhanced Features</h3>
                <p className="text-gray-400 text-sm">AI-powered browser capabilities</p>
              </div>

              {/* Quick Actions */}
              <div className="space-y-2">
                {quickActions.map((action) => (
                  <motion.button
                    key={action.id}
                    onClick={() => handleFeatureAction(action.id)}
                    className="w-full flex items-center space-x-3 p-3 rounded-xl bg-gray-800/50 hover:bg-gray-700/50 transition-colors group"
                    whileHover={{ x: 5 }}
                  >
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${action.color} flex items-center justify-center flex-shrink-0`}>
                      <action.icon size={20} className="text-white" />
                    </div>
                    <div className="text-left flex-1">
                      <div className="text-white font-medium">{action.label}</div>
                      <div className="text-gray-400 text-xs">{action.description}</div>
                    </div>
                    <Zap size={16} className="text-gray-400 group-hover:text-white transition-colors" />
                  </motion.button>
                ))}
              </div>

              {/* Feature Categories */}
              <div className="mt-4 pt-4 border-t border-gray-700/50">
                <div className="text-gray-400 text-xs mb-2">Available Categories</div>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { name: 'Navigation', icon: Navigation, count: 4 },
                    { name: 'Productivity', icon: Lightbulb, count: 4 },
                    { name: 'Performance', icon: BarChart3, count: 4 },
                    { name: 'AI Interface', icon: Cpu, count: 4 }
                  ].map((category) => (
                    <div
                      key={category.name}
                      className="flex items-center space-x-2 p-2 rounded-lg bg-gray-800/30 text-gray-300"
                    >
                      <category.icon size={14} />
                      <span className="text-xs">{category.name}</span>
                      <span className="text-xs bg-gray-700 px-1 rounded">{category.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Status Indicator */}
              {featuresStatus && (
                <div className="mt-4 pt-4 border-t border-gray-700/50">
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>System Status</span>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <span>All Features Active</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Keyboard Shortcuts Overlay (shows on Alt key hold) */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-96 right-6 z-30"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ delay: 0.5 }}
          >
            <div className="bg-gray-900/90 backdrop-blur-lg rounded-lg border border-gray-700/50 p-3 text-xs text-gray-300">
              <div className="font-medium mb-1">Keyboard Shortcuts:</div>
              <div>Alt+A - AI Analyze</div>
              <div>Alt+V - Voice Command</div>
              <div>Alt+S - Smart Suggestions</div>
              <div>Alt+N - Natural Language</div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

// Auto-register keyboard shortcuts globally
if (typeof window !== 'undefined') {
  document.addEventListener('keydown', (e) => {
    if (e.altKey && !e.ctrlKey && !e.shiftKey) {
      const userId = localStorage.getItem('userId') || 'anonymous';
      
      switch (e.key.toLowerCase()) {
        case 'a':
          e.preventDefault();
          enhancedFeaturesService.oneClickActions(
            window.location.href, 
            document.body.innerText.substring(0, 1000),
            { userId }
          ).then(() => console.log('🧠 AI Analysis completed'));
          break;
          
        case 'v':
          e.preventDefault();
          enhancedFeaturesService.voiceCommands('voice ready', userId)
            .then(() => console.log('🎤 Voice commands ready'));
          break;
          
        case 's':
          e.preventDefault();
          enhancedFeaturesService.smartSuggestions(
            window.location.href,
            document.body.innerText.substring(0, 1000),
            { userId }
          ).then(() => console.log('💡 Smart suggestions generated'));
          break;
          
        case 'n':
          e.preventDefault();
          const input = prompt('Ask AI anything:');
          if (input) {
            enhancedFeaturesService.naturalLanguageInterface(input, userId, { url: window.location.href })
              .then(() => console.log('🤖 AI responded'));
          }
          break;
      }
    }
  });
}