import React, { useEffect, useState } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { useUser } from '../../contexts/UserContext';
import EnhancedBubbleTabWorkspace from '../BubbleTab/EnhancedBubbleTabWorkspace';
import EnhancedAIAssistant from '../AIAssistant/EnhancedAIAssistant';
import ResponsiveNavigationBar from '../Navigation/ResponsiveNavigationBar';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Brain, Sparkles, Zap, TrendingUp, Globe } from 'lucide-react';

export default function MainBrowser() {
  const { currentSession, tabs, addTab } = useBrowser();
  const { isAssistantVisible, toggleAssistant } = useAI();
  const { user } = useUser();
  const [isInitializing, setIsInitializing] = useState(true);
  const [showWelcomeAnimation, setShowWelcomeAnimation] = useState(false);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);

  useEffect(() => {
    // Initialize browser session
    const initializeBrowser = async () => {
      try {
        // Create initial session if none exists
        if (!currentSession) {
          // For now, create a mock session
          const mockSession = {
            id: 'session-1',
            user_id: user.id,
            name: 'Default Session',
            tabs: [],
            created_at: new Date().toISOString()
          };
        }
        
        // Load performance metrics
        loadPerformanceMetrics();
        
      } catch (error) {
        console.error('Error initializing browser:', error);
      } finally {
        setIsInitializing(false);
        if (tabs.length === 0) {
          setShowWelcomeAnimation(true);
        }
      }
    };

    if (user) {
      initializeBrowser();
    }
  }, [user, currentSession]);

  const loadPerformanceMetrics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/performance-metrics`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
      
      if (response.ok) {
        const metrics = await response.json();
        setPerformanceMetrics(metrics);
      }
    } catch (error) {
      console.error('Could not load performance metrics:', error);
    }
  };

  const handleNewTab = (type = 'blank') => {
    const newTab = {
      id: `tab-${Date.now()}`,
      url: type === 'blank' ? 'about:blank' : 'https://google.com',
      title: type === 'blank' ? 'New Tab' : 'Google Search',
      position_x: Math.random() * 400 + 200,
      position_y: Math.random() * 300 + 150,
      is_active: false,
      created_at: new Date().toISOString(),
      metadata: {
        type: type,
        ai_analyzed: false
      }
    };
    addTab(newTab);
    setShowWelcomeAnimation(false);
  };

  if (isInitializing) {
    return (
      <motion.div 
        className="flex items-center justify-center h-screen bg-gradient-to-br from-ai-dark via-slate-800 to-ai-dark"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="text-center">
          <motion.div
            className="w-16 h-16 border-4 border-ai-primary border-t-transparent rounded-full mx-auto mb-6"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-2xl font-bold text-white mb-2 flex items-center justify-center">
              <Brain className="mr-2 text-purple-400" />
              Initializing AI Browser...
            </h2>
            <p className="text-gray-400">Setting up your intelligent workspace</p>
          </motion.div>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="browser-container relative bg-gradient-to-br from-ai-dark via-purple-900/10 to-blue-900/10 min-h-screen">
      {/* Enhanced Navigation Bar */}
      <ResponsiveNavigationBar />
      
      {/* Main Content Area */}
      <div className="main-content-area">
        {/* Enhanced Bubble Tab Workspace */}
        <EnhancedBubbleTabWorkspace />
        
        {/* Enhanced AI Assistant */}
        <EnhancedAIAssistant />
      </div>

      {/* Welcome Screen for First-time Users */}
      <AnimatePresence>
        {showWelcomeAnimation && tabs.length === 0 && (
          <motion.div 
            className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-ai-dark/95 via-purple-900/20 to-blue-900/20 backdrop-blur-sm z-30"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div 
              className="text-center max-w-2xl mx-auto px-6"
              initial={{ scale: 0.8, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6, type: "spring", stiffness: 100 }}
            >
              {/* Animated Logo */}
              <motion.div
                className="relative mb-8"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, duration: 0.8, type: "spring", bounce: 0.4 }}
              >
                <div className="w-24 h-24 mx-auto bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mb-4 shadow-2xl">
                  <Brain size={48} className="text-white" />
                </div>
                <motion.div
                  className="absolute inset-0 w-24 h-24 mx-auto bg-gradient-to-r from-purple-600/30 to-blue-600/30 rounded-full"
                  animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0, 0.5] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                />
              </motion.div>

              <motion.h1 
                className="text-6xl font-bold text-white mb-6"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
              >
                Welcome to the <span className="text-gradient">Future</span>
              </motion.h1>
              
              <motion.p 
                className="text-xl text-gray-300 mb-8 leading-relaxed"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.8 }}
              >
                Your AI-powered browser with floating bubble tabs, intelligent automation, 
                and advanced capabilities that adapt to your workflow
              </motion.p>

              {/* Enhanced Feature Highlights */}
              <motion.div
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.0 }}
              >
                {[
                  { icon: Globe, title: "3D Bubble Tabs", desc: "Physics-based floating workspace" },
                  { icon: Brain, title: "AI Assistant", desc: "GROQ-powered intelligent automation" },
                  { icon: Zap, title: "Smart Automation", desc: "Form filling, shopping, analysis" }
                ].map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    className="p-4 glass rounded-xl"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1.2 + index * 0.2 }}
                  >
                    <feature.icon className="w-8 h-8 text-purple-400 mx-auto mb-3" />
                    <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
                    <p className="text-gray-400 text-sm">{feature.desc}</p>
                  </motion.div>
                ))}
              </motion.div>

              {/* Enhanced Action Buttons */}
              <motion.div 
                className="space-y-4"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.6 }}
              >
                <motion.button
                  onClick={() => handleNewTab('blank')}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-4 px-8 rounded-2xl font-semibold text-lg transition-all transform hover:scale-105 shadow-2xl flex items-center justify-center"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Sparkles className="mr-2" size={24} />
                  Create Your First Bubble Tab
                </motion.button>
                
                <div className="flex space-x-4">
                  <motion.button
                    onClick={() => handleNewTab('search')}
                    className="flex-1 bg-gray-800/50 hover:bg-gray-700/50 text-white py-3 px-6 rounded-xl font-medium transition-all border border-gray-700/50 hover:border-purple-500/30 flex items-center justify-center"
                    whileHover={{ scale: 1.02 }}
                  >
                    <Globe className="mr-2" size={20} />
                    Start with Search
                  </motion.button>
                  
                  <motion.button
                    onClick={toggleAssistant}
                    className="flex-1 bg-gray-800/50 hover:bg-gray-700/50 text-white py-3 px-6 rounded-xl font-medium transition-all border border-gray-700/50 hover:border-purple-500/30 flex items-center justify-center"
                    whileHover={{ scale: 1.02 }}
                  >
                    <Brain className="mr-2" size={20} />
                    Meet ARIA AI
                  </motion.button>
                </div>
              </motion.div>

              {/* Performance Info */}
              {performanceMetrics && (
                <motion.div
                  className="mt-8 p-4 bg-gray-800/30 rounded-lg border border-gray-700/30"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 2.0 }}
                >
                  <div className="flex items-center justify-center text-sm text-gray-400 space-x-6">
                    <div className="flex items-center">
                      <TrendingUp className="w-4 h-4 mr-1" />
                      Enhanced Performance
                    </div>
                    <div className="flex items-center">
                      <Zap className="w-4 h-4 mr-1" />
                      AI Cache Ready
                    </div>
                    <div className="flex items-center">
                      <Brain className="w-4 h-4 mr-1" />
                      GROQ Powered
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced User Mode Indicator */}
      <motion.div 
        className="fixed top-20 right-6 bg-gray-900/80 backdrop-blur-xl border border-gray-700/50 rounded-lg px-4 py-2 text-sm text-white z-30 shadow-lg"
        initial={{ x: 100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="font-medium">{user?.user_mode || 'Guest'} Mode</span>
          <span className="text-gray-400">•</span>
          <span className="text-gray-400 text-xs">Enhanced v2.0</span>
        </div>
      </motion.div>

      {/* Performance Metrics Overlay (Debug) */}
      {performanceMetrics && process.env.NODE_ENV === 'development' && (
        <motion.div
          className="fixed bottom-6 left-6 bg-gray-900/80 backdrop-blur-xl border border-gray-700/50 rounded-lg p-3 text-xs text-gray-300 z-30"
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.0 }}
        >
          <div className="space-y-1">
            <div>Cache: {performanceMetrics.cache_status?.entries || 0} entries</div>
            <div>Status: {performanceMetrics.cache_status?.enabled ? '✅ Enabled' : '❌ Disabled'}</div>
          </div>
        </motion.div>
      )}
    </div>
  );
}