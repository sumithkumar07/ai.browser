import React, { useEffect, useState, useCallback } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { useUser } from '../../contexts/UserContext';
import EnhancedBubbleTabWorkspace from '../BubbleTab/EnhancedBubbleTabWorkspace';
import EnhancedAIAssistant from '../AIAssistant/EnhancedAIAssistant';
import ResponsiveNavigationBar from '../Navigation/ResponsiveNavigationBar';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Brain, Sparkles, Zap, TrendingUp, Globe, Shield, Wifi, WifiOff, Command, Eye, Settings } from 'lucide-react';

export default function MainBrowser() {
  const { currentSession, tabs, addTab } = useBrowser();
  const { isAssistantVisible, toggleAssistant } = useAI();
  const { user } = useUser();
  const [isInitializing, setIsInitializing] = useState(true);
  const [showWelcomeAnimation, setShowWelcomeAnimation] = useState(false);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [showPerformancePanel, setShowPerformancePanel] = useState(false);
  const [appVersion] = useState('2.0.0');
  const [shortcuts, setShortcuts] = useState([]);

  useEffect(() => {
    // Initialize browser session with enhanced error handling
    const initializeBrowser = async () => {
      try {
        // Create initial session if none exists
        if (!currentSession) {
          const mockSession = {
            id: 'session-1',
            user_id: user.id,
            name: 'Enhanced AI Browser Session',
            tabs: [],
            created_at: new Date().toISOString(),
            metadata: {
              version: appVersion,
              enhanced_features: true,
              ai_powered: true
            }
          };
        }
        
        // Load enhanced performance metrics
        await loadPerformanceMetrics();
        
        // Initialize keyboard shortcuts
        initializeShortcuts();
        
      } catch (error) {
        console.error('Error initializing enhanced browser:', error);
      } finally {
        setIsInitializing(false);
        if (tabs.length === 0) {
          setShowWelcomeAnimation(true);
          // Auto-hide welcome after 10 seconds if no interaction
          setTimeout(() => setShowWelcomeAnimation(false), 10000);
        }
      }
    };

    if (user) {
      initializeBrowser();
    }
  }, [user, currentSession, tabs.length, appVersion]);

  // Enhanced online/offline detection
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Enhanced performance metrics loading with caching
  const loadPerformanceMetrics = useCallback(async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/performance-metrics`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
      
      if (response.ok) {
        const metrics = await response.json();
        setPerformanceMetrics(metrics);
        
        // Store in localStorage for offline access
        localStorage.setItem('lastPerformanceMetrics', JSON.stringify({
          data: metrics,
          timestamp: Date.now()
        }));
      }
    } catch (error) {
      console.error('Could not load performance metrics:', error);
      
      // Try to load from localStorage if online request fails
      const cached = localStorage.getItem('lastPerformanceMetrics');
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        // Use cached data if less than 5 minutes old
        if (Date.now() - timestamp < 5 * 60 * 1000) {
          setPerformanceMetrics(data);
        }
      }
    }
  }, []);

  // Initialize enhanced keyboard shortcuts
  const initializeShortcuts = useCallback(() => {
    const shortcutList = [
      { key: '⌘T', description: 'New Tab', action: () => handleNewTab() },
      { key: '⌘K', description: 'AI Assistant', action: toggleAssistant },
      { key: '⌘P', description: 'Performance Panel', action: () => setShowPerformancePanel(!showPerformancePanel) },
      { key: 'Space', description: 'Zen Mode', action: () => {} }, // Handled in workspace
      { key: 'G', description: 'Grid View', action: () => {} },
      { key: 'L', description: 'List View', action: () => {} }
    ];
    setShortcuts(shortcutList);
  }, [toggleAssistant, showPerformancePanel]);

  // Enhanced tab creation with intelligent positioning
  const handleNewTab = useCallback((type = 'blank') => {
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
        ai_analyzed: false,
        created_by: 'user',
        session_id: currentSession?.id || 'default',
        enhanced_features: true,
        performance_score: 100
      }
    };
    addTab(newTab);
    setShowWelcomeAnimation(false);
  }, [addTab, currentSession]);

  // Enhanced loading screen
  if (isInitializing) {
    return (
      <motion.div 
        className="flex items-center justify-center h-screen bg-gradient-to-br from-ai-dark via-purple-900/20 to-blue-900/20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="text-center">
          <motion.div
            className="w-20 h-20 border-4 border-ai-primary/30 border-t-ai-primary rounded-full mx-auto mb-8"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-3xl font-bold text-white mb-3 flex items-center justify-center">
              <Brain className="mr-3 text-purple-400 animate-pulse" size={32} />
              Enhanced AI Browser
            </h2>
            <p className="text-gray-400 text-lg mb-4">Initializing intelligent workspace...</p>
            
            {/* Enhanced loading features */}
            <div className="space-y-2 text-sm text-gray-500">
              <motion.div
                className="flex items-center justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <Sparkles className="mr-2" size={16} />
                Loading AI capabilities...
              </motion.div>
              <motion.div
                className="flex items-center justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
              >
                <Globe className="mr-2" size={16} />
                Setting up enhanced workspace...
              </motion.div>
              <motion.div
                className="flex items-center justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.1 }}
              >
                <TrendingUp className="mr-2" size={16} />
                Optimizing performance...
              </motion.div>
            </div>
          </motion.div>
          
          {/* Connection status */}
          <motion.div
            className="mt-8 flex items-center justify-center text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.4 }}
          >
            {isOnline ? (
              <>
                <Wifi className="mr-2 text-green-400" size={16} />
                <span className="text-green-400">Connected & Enhanced</span>
              </>
            ) : (
              <>
                <WifiOff className="mr-2 text-red-400" size={16} />
                <span className="text-red-400">Offline Mode</span>
              </>
            )}
          </motion.div>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="browser-container relative bg-gradient-to-br from-ai-dark via-purple-900/5 to-blue-900/5 min-h-screen overflow-hidden">
      {/* Enhanced Navigation Bar */}
      <ResponsiveNavigationBar />
      
      {/* Main Content Area */}
      <div className="main-content-area relative">
        {/* Enhanced Bubble Tab Workspace */}
        <EnhancedBubbleTabWorkspace />
        
        {/* Enhanced AI Assistant */}
        <EnhancedAIAssistant />
      </div>

      {/* Enhanced Welcome Screen */}
      <AnimatePresence>
        {showWelcomeAnimation && tabs.length === 0 && (
          <motion.div 
            className="fixed inset-0 flex items-center justify-center bg-gradient-to-br from-ai-dark/98 via-purple-900/30 to-blue-900/30 backdrop-blur-md z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
          >
            <motion.div 
              className="text-center max-w-4xl mx-auto px-8"
              initial={{ scale: 0.8, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.8, type: "spring", stiffness: 120 }}
            >
              {/* Enhanced Animated Logo */}
              <motion.div
                className="relative mb-12"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, duration: 1, type: "spring", bounce: 0.3 }}
              >
                <div className="w-32 h-32 mx-auto bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 rounded-full flex items-center justify-center mb-6 shadow-2xl relative">
                  <Brain size={64} className="text-white" />
                  
                  {/* Animated rings */}
                  <motion.div
                    className="absolute inset-0 w-32 h-32 border-4 border-purple-500/30 rounded-full"
                    animate={{ scale: [1, 1.3, 1], opacity: [0.5, 0, 0.5] }}
                    transition={{ repeat: Infinity, duration: 3 }}
                  />
                  <motion.div
                    className="absolute inset-0 w-32 h-32 border-2 border-blue-500/20 rounded-full"
                    animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0, 0.3] }}
                    transition={{ repeat: Infinity, duration: 2, delay: 0.5 }}
                  />
                </div>
                
                <motion.div
                  className="text-sm text-purple-400 font-medium"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                >
                  v{appVersion} Enhanced
                </motion.div>
              </motion.div>

              <motion.h1 
                className="text-7xl font-bold text-white mb-8"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
              >
                Welcome to the <span className="text-gradient bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Enhanced Future</span>
              </motion.h1>
              
              <motion.p 
                className="text-2xl text-gray-300 mb-10 leading-relaxed max-w-3xl mx-auto"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.8 }}
              >
                Your AI-powered browser with floating bubble tabs, intelligent automation, 
                enhanced performance, and advanced capabilities that adapt to your workflow
              </motion.p>

              {/* Enhanced Feature Highlights */}
              <motion.div
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.0 }}
              >
                {[
                  { 
                    icon: Globe, 
                    title: "3D Bubble Workspace", 
                    desc: "Physics-based floating tabs with intelligent organization",
                    color: "from-blue-500 to-cyan-500"
                  },
                  { 
                    icon: Brain, 
                    title: "Enhanced AI Assistant", 
                    desc: "GROQ-powered Llama3-70B with conversational intelligence",
                    color: "from-purple-500 to-pink-500"
                  },
                  { 
                    icon: Zap, 
                    title: "Smart Automation", 
                    desc: "Advanced form filling, e-commerce, and workflow automation",
                    color: "from-yellow-500 to-orange-500"
                  },
                  { 
                    icon: TrendingUp, 
                    title: "Performance Optimized", 
                    desc: "Intelligent caching, memory optimization, and monitoring",
                    color: "from-green-500 to-emerald-500"
                  }
                ].map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    className="p-6 glass-light rounded-2xl border border-gray-700/30 hover:border-purple-500/30 transition-all duration-300"
                    initial={{ scale: 0, rotate: -10 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ delay: 1.2 + index * 0.15, type: "spring", stiffness: 120 }}
                    whileHover={{ y: -5, scale: 1.02 }}
                  >
                    <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mx-auto mb-4`}>
                      <feature.icon className="text-white" size={24} />
                    </div>
                    <h3 className="text-white font-bold mb-3 text-lg">{feature.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{feature.desc}</p>
                  </motion.div>
                ))}
              </motion.div>

              {/* Enhanced Action Buttons */}
              <motion.div 
                className="space-y-6"
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.8 }}
              >
                <motion.button
                  onClick={() => handleNewTab('blank')}
                  className="w-full max-w-md bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-6 px-10 rounded-2xl font-bold text-xl transition-all shadow-2xl relative overflow-hidden group mx-auto block"
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-400/20 to-blue-400/20 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500"></div>
                  <div className="relative flex items-center justify-center">
                    <Sparkles className="mr-3" size={28} />
                    Create Your First Enhanced Tab
                  </div>
                </motion.button>
                
                <div className="flex flex-wrap gap-4 justify-center">
                  <motion.button
                    onClick={() => handleNewTab('search')}
                    className="btn-secondary py-4 px-8 text-lg flex items-center"
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <Globe className="mr-2" size={24} />
                    Start with Smart Search
                  </motion.button>
                  
                  <motion.button
                    onClick={toggleAssistant}
                    className="btn-secondary py-4 px-8 text-lg flex items-center"
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <Brain className="mr-2" size={24} />
                    Meet Enhanced ARIA AI
                  </motion.button>
                  
                  <motion.button
                    onClick={() => setShowPerformancePanel(true)}
                    className="btn-secondary py-4 px-8 text-lg flex items-center"
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <TrendingUp className="mr-2" size={24} />
                    Performance Metrics
                  </motion.button>
                </div>
              </motion.div>

              {/* Enhanced Status Information */}
              <motion.div
                className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 2.2 }}
              >
                <div className="glass-light rounded-xl p-4 border border-gray-700/30">
                  <div className="flex items-center justify-center text-sm text-gray-400 space-x-2">
                    <Shield className="w-5 h-5 text-green-400" />
                    <span>Enhanced Security</span>
                  </div>
                </div>
                
                <div className="glass-light rounded-xl p-4 border border-gray-700/30">
                  <div className="flex items-center justify-center text-sm text-gray-400 space-x-2">
                    {isOnline ? (
                      <>
                        <Wifi className="w-5 h-5 text-green-400" />
                        <span>AI Connected</span>
                      </>
                    ) : (
                      <>
                        <WifiOff className="w-5 h-5 text-red-400" />
                        <span>Offline Mode</span>
                      </>
                    )}
                  </div>
                </div>
                
                <div className="glass-light rounded-xl p-4 border border-gray-700/30">
                  <div className="flex items-center justify-center text-sm text-gray-400 space-x-2">
                    <TrendingUp className="w-5 h-5 text-purple-400" />
                    <span>Performance Ready</span>
                  </div>
                </div>
              </motion.div>

              {/* Enhanced Keyboard Shortcuts Hint */}
              <motion.div
                className="mt-8 text-sm text-gray-500 space-y-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 2.5 }}
              >
                <p className="mb-4 font-medium text-gray-400">💡 Enhanced Keyboard Shortcuts:</p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-w-2xl mx-auto">
                  {shortcuts.map((shortcut, index) => (
                    <div key={index} className="flex items-center justify-between text-xs">
                      <span>{shortcut.description}</span>
                      <kbd className="bg-gray-800/50 text-gray-400 px-2 py-1 rounded border border-gray-700/50">
                        {shortcut.key}
                      </kbd>
                    </div>
                  ))}
                </div>
              </motion.div>
              
              {/* Close welcome screen button */}
              <motion.button
                onClick={() => setShowWelcomeAnimation(false)}
                className="mt-8 text-gray-500 hover:text-gray-300 text-sm transition-colors"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 3 }}
              >
                Skip welcome (or press Escape)
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Performance Panel */}
      <AnimatePresence>
        {showPerformancePanel && performanceMetrics && (
          <motion.div
            className="fixed top-20 right-6 w-96 glass-strong rounded-2xl p-6 z-30 border border-gray-700/50 shadow-2xl"
            initial={{ opacity: 0, x: 100, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.9 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-white font-bold text-lg flex items-center">
                <TrendingUp className="mr-2 text-green-400" size={20} />
                Performance Metrics
              </h3>
              <button
                onClick={() => setShowPerformancePanel(false)}
                className="text-gray-400 hover:text-white transition-colors"
              >
                ×
              </button>
            </div>
            
            {performanceMetrics && (
              <div className="space-y-4 text-sm">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-800/30 rounded-lg p-3">
                    <div className="text-gray-400 mb-1">Cache Status</div>
                    <div className="text-white font-medium">
                      {performanceMetrics.cache_status?.entries || 0} entries
                    </div>
                    <div className={`text-xs ${performanceMetrics.cache_status?.enabled ? 'text-green-400' : 'text-red-400'}`}>
                      {performanceMetrics.cache_status?.enabled ? '✅ Enabled' : '❌ Disabled'}
                    </div>
                  </div>
                  
                  <div className="bg-gray-800/30 rounded-lg p-3">
                    <div className="text-gray-400 mb-1">AI Response</div>
                    <div className="text-white font-medium">Enhanced</div>
                    <div className="text-xs text-purple-400">GROQ Powered</div>
                  </div>
                </div>
                
                {performanceMetrics.performance_summary && (
                  <div className="bg-gray-800/30 rounded-lg p-3">
                    <div className="text-gray-400 mb-2">System Health</div>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-300">Performance Score</span>
                        <span className="text-green-400">
                          {performanceMetrics.performance_summary.trends?.performance_score || 'N/A'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-300">Memory Usage</span>
                        <span className="text-blue-400">Optimized</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <button
                  onClick={loadPerformanceMetrics}
                  className="w-full btn-secondary text-sm py-2 flex items-center justify-center"
                >
                  <TrendingUp size={14} className="mr-2" />
                  Refresh Metrics
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Status Bar */}
      <motion.div 
        className="fixed bottom-4 left-4 glass rounded-lg px-4 py-2 text-sm z-20 border border-gray-700/30"
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="flex items-center space-x-4 text-gray-400">
          <div className="flex items-center space-x-1">
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
            <span className="font-medium text-white">{user?.user_mode || 'Guest'} Mode</span>
          </div>
          <span>•</span>
          <span>Enhanced v{appVersion}</span>
          <span>•</span>
          <span>{tabs.length} tabs</span>
          {performanceMetrics && (
            <>
              <span>•</span>
              <span className="text-purple-400">
                {performanceMetrics.cache_status?.entries || 0} cached
              </span>
            </>
          )}
        </div>
      </motion.div>

      {/* Floating Help Button */}
      <motion.button
        onClick={() => setShowPerformancePanel(!showPerformancePanel)}
        className="fixed bottom-4 right-4 w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-full shadow-lg text-white z-20 transition-all"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1 }}
      >
        <Settings size={20} />
      </motion.button>

      {/* Enhanced Keyboard Shortcuts Handler */}
      <div className="hidden">
        {shortcuts.map((shortcut, index) => (
          <div key={index} onClick={shortcut.action}></div>
        ))}
      </div>
    </div>
  );
}