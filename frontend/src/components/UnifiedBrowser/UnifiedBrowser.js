import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, ArrowRight, RotateCcw, Home, Star, Download, 
  History, Bookmark, Settings, HelpCircle, Plus, X, Search,
  Globe, Shield, ExternalLink, Menu, BookOpen, Clock, Activity, 
  Zap, Brain, Sparkles, ChevronDown, Layers, Eye, FileText,
  MessageSquare, Lightbulb, TrendingUp, BarChart3
} from 'lucide-react';

// Services
import realBrowserService from '../../services/RealBrowserService';
import HybridBrowserService from '../../services/HybridBrowserService';
import { useAI } from '../../contexts/AIContext';

// Enhanced AI Insights Panel
import AIInsightsPanel from './components/AIInsightsPanel';
import SmartUrlBar from './components/SmartUrlBar';
import EnhancedTabManager from './components/EnhancedTabManager';
import EmbeddedWebView from './components/EmbeddedWebView';
import ComprehensiveFeaturesPanel from '../ComprehensiveFeatures/ComprehensiveFeaturesPanel';
import { useParallelFeatures } from '../../contexts/ParallelFeaturesContext';
import comprehensiveFeaturesService from '../../services/comprehensiveFeaturesService';

export default function UnifiedBrowser() {
  // Core browser state
  const [tabs, setTabs] = useState([]);
  const [activeTabId, setActiveTabId] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [browserReady, setBrowserReady] = useState(false);

  // AI Integration state
  const [showAIPanel, setShowAIPanel] = useState(true);
  const [pageAnalysis, setPageAnalysis] = useState(null);
  const [aiInsights, setAiInsights] = useState([]);
  const [contextualActions, setContextualActions] = useState([]);

  // Enhanced features state
  const [tabGroups, setTabGroups] = useState(new Map());
  const [bookmarks, setBookmarks] = useState([]);
  const [recentlyClosedTabs, setRecentlyClosedTabs] = useState([]);
  const [showSmartSuggestions, setShowSmartSuggestions] = useState(false);
  const [showComprehensiveFeatures, setShowComprehensiveFeatures] = useState(false);
  const [showVoiceCommands, setShowVoiceCommands] = useState(false);
  const [comprehensiveFeatures, setComprehensiveFeatures] = useState(null);

  // UI state
  const [showBookmarkBar, setShowBookmarkBar] = useState(true);
  const [showTabGroups, setShowTabGroups] = useState(false);
  const [sidebarWidth, setSidebarWidth] = useState(350);

  const { aiCapabilities, hybridFeatures } = useAI();
  const parallelFeatures = useParallelFeatures();
  const urlInputRef = useRef(null);
  const webViewRef = useRef(null);

  // Initialize browser on mount
  useEffect(() => {
    initializeUnifiedBrowser();
    loadComprehensiveFeatures();
    return () => cleanup();
  }, []);

  // Load comprehensive features overview
  const loadComprehensiveFeatures = async () => {
    try {
      const features = await comprehensiveFeaturesService.getComprehensiveFeaturesOverview();
      setComprehensiveFeatures(features.data);
    } catch (error) {
      console.error('Failed to load comprehensive features:', error);
    }
  };

  // Real-time AI analysis when active tab changes
  useEffect(() => {
    if (activeTabId && browserReady) {
      analyzeCurrentPageWithAI();
    }
  }, [activeTabId, browserReady]);

  const initializeUnifiedBrowser = async () => {
    try {
      console.log('🚀 Initializing Unified AI Browser...');
      
      // Check browser health
      const health = await realBrowserService.getBrowserHealth();
      console.log('Browser Health:', health);
      
      // Initialize session
      await realBrowserService.createSession();
      
      // Create welcome tab
      await createNewTab('about:welcome');
      
      setBrowserReady(true);
      console.log('✅ Unified Browser Ready');
      
    } catch (error) {
      console.error('Browser initialization failed:', error);
      // Fallback: create local welcome tab
      createLocalTab('Welcome to AI Browser', 'about:welcome');
    }
  };

  const createNewTab = async (url = 'about:blank', title = null, inBackground = false) => {
    try {
      setIsLoading(true);
      
      // Create real browser tab
      const result = await realBrowserService.createNewTab(url);
      
      if (result.success) {
        const newTab = {
          id: result.tab_id,
          url: result.url,
          title: title || result.title || getDefaultTitle(result.url),
          isLoading: false,
          favicon: null,
          isPinned: false,
          groupId: null,
          createdAt: new Date(),
          lastActive: new Date()
        };
        
        setTabs(prev => [...prev, newTab]);
        
        if (!inBackground) {
          setActiveTabId(result.tab_id);
          setCurrentUrl(result.url);
        }
        
        // Trigger AI analysis for non-blank pages
        if (url !== 'about:blank' && !inBackground) {
          setTimeout(() => analyzePageContent(result.tab_id, result.url), 1000);
        }
        
        return newTab;
      }
    } catch (error) {
      console.error('Failed to create tab:', error);
      // Fallback: create local tab
      return createLocalTab(title || 'New Tab', url);
    } finally {
      setIsLoading(false);
    }
  };

  const createLocalTab = (title, url) => {
    const newTab = {
      id: `local-${Date.now()}`,
      url: url,
      title: title,
      isLoading: false,
      isPinned: false,
      isLocal: true,
      createdAt: new Date(),
      lastActive: new Date()
    };
    
    setTabs(prev => [...prev, newTab]);
    setActiveTabId(newTab.id);
    setCurrentUrl(url);
    
    return newTab;
  };

  const navigateToUrl = async (url, tabId = null) => {
    if (!url.trim()) return;
    
    const targetTabId = tabId || activeTabId;
    if (!targetTabId) return;
    
    try {
      setIsLoading(true);
      const processedUrl = realBrowserService.processUrl(url);
      
      // Update tab immediately for responsiveness
      setTabs(prev => prev.map(tab => 
        tab.id === targetTabId 
          ? { ...tab, isLoading: true, url: processedUrl }
          : tab
      ));
      
      // Navigate real browser
      const result = await realBrowserService.navigateToUrl(processedUrl, targetTabId);
      
      if (result.success) {
        // Update tab with results
        setTabs(prev => prev.map(tab => 
          tab.id === targetTabId 
            ? { 
                ...tab, 
                url: result.url, 
                title: result.title || getDefaultTitle(result.url),
                isLoading: false,
                lastActive: new Date()
              }
            : tab
        ));
        
        if (targetTabId === activeTabId) {
          setCurrentUrl(result.url);
        }
        
        // Trigger AI analysis
        setTimeout(() => analyzePageContent(targetTabId, result.url), 1500);
      }
    } catch (error) {
      console.error('Navigation failed:', error);
      
      // Update tab to show error
      setTabs(prev => prev.map(tab => 
        tab.id === targetTabId 
          ? { ...tab, title: 'Failed to load', isLoading: false }
          : tab
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const closeTab = async (tabId, addToRecent = true) => {
    try {
      const tabToClose = tabs.find(tab => tab.id === tabId);
      
      if (tabToClose && addToRecent) {
        setRecentlyClosedTabs(prev => [{
          ...tabToClose,
          closedAt: new Date()
        }, ...prev.slice(0, 9)]); // Keep last 10
      }
      
      // Close real browser tab
      if (!tabToClose?.isLocal) {
        await realBrowserService.closeTab(tabId);
      }
      
      setTabs(prev => {
        const remaining = prev.filter(tab => tab.id !== tabId);
        
        // Handle active tab switching
        if (tabId === activeTabId) {
          if (remaining.length > 0) {
            const nextTab = remaining[remaining.length - 1];
            setActiveTabId(nextTab.id);
            setCurrentUrl(nextTab.url);
          } else {
            createNewTab('about:blank');
            return remaining;
          }
        }
        
        return remaining;
      });
      
    } catch (error) {
      console.error('Failed to close tab:', error);
    }
  };

  const switchToTab = (tabId) => {
    const tab = tabs.find(t => t.id === tabId);
    if (!tab) return;
    
    setActiveTabId(tabId);
    setCurrentUrl(tab.url);
    
    // Update last active time
    setTabs(prev => prev.map(t => 
      t.id === tabId 
        ? { ...t, lastActive: new Date() }
        : t
    ));
  };

  const analyzePageContent = async (tabId, url) => {
    if (!tabId || url === 'about:blank' || url.startsWith('about:')) return;
    
    try {
      console.log(`🧠 Analyzing page: ${url}`);
      
      // Get page content
      const content = await realBrowserService.getPageContent(tabId);
      
      if (content.success) {
        // Send to hybrid AI service for analysis
        const analysis = await HybridBrowserService.analyzePageContent({
          url: url,
          content: content.content,
          title: content.title
        });
        
        if (analysis.success) {
          setPageAnalysis(analysis.analysis);
          setAiInsights(analysis.insights || []);
          setContextualActions(analysis.actions || []);
          
          console.log('✅ Page analysis complete');
        }
      }
    } catch (error) {
      console.error('Page analysis failed:', error);
    }
  };

  const analyzeCurrentPageWithAI = () => {
    const activeTab = tabs.find(tab => tab.id === activeTabId);
    if (activeTab && !activeTab.isLocal) {
      analyzePageContent(activeTabId, activeTab.url);
    }
  };

  const getDefaultTitle = (url) => {
    if (url === 'about:blank') return 'New Tab';
    if (url.startsWith('about:')) return 'Browser Page';
    try {
      const domain = new URL(url).hostname.replace('www.', '');
      return domain.charAt(0).toUpperCase() + domain.slice(1);
    } catch {
      return 'Loading...';
    }
  };

  const handleUrlSubmit = (url) => {
    if (url.trim()) {
      navigateToUrl(url);
      setShowSmartSuggestions(false);
    }
  };

  const cleanup = async () => {
    try {
      await realBrowserService.cleanup();
    } catch (error) {
      console.error('Cleanup failed:', error);
    }
  };

  // Get active tab for display
  const activeTab = tabs.find(tab => tab.id === activeTabId);

  return (
    <div className="unified-browser h-screen w-screen flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      
      {/* Enhanced Navigation Bar */}
      <div className="nav-bar bg-gray-900/95 backdrop-blur-sm border-b border-gray-700/50 px-4 py-2">
        <div className="flex items-center space-x-3">
          
          {/* Browser Controls */}
          <div className="flex items-center space-x-1">
            <button 
              className="nav-btn"
              onClick={() => realBrowserService.goBack(activeTabId)}
              disabled={!activeTab || isLoading}
              title="Back"
            >
              <ArrowLeft size={16} />
            </button>
            <button 
              className="nav-btn"
              onClick={() => realBrowserService.goForward(activeTabId)}
              disabled={!activeTab || isLoading}
              title="Forward"
            >
              <ArrowRight size={16} />
            </button>
            <button 
              className="nav-btn"
              onClick={() => realBrowserService.reload(activeTabId)}
              disabled={!activeTab || isLoading}
              title="Reload"
            >
              <RotateCcw size={16} className={isLoading ? 'animate-spin' : ''} />
            </button>
            <button 
              className="nav-btn"
              onClick={() => navigateToUrl('https://google.com')}
              title="Home"
            >
              <Home size={16} />
            </button>
          </div>

          {/* Smart URL Bar */}
          <div className="flex-1 max-w-2xl">
            <SmartUrlBar 
              value={currentUrl}
              onSubmit={handleUrlSubmit}
              onShowSuggestions={setShowSmartSuggestions}
              showSuggestions={showSmartSuggestions}
              isLoading={isLoading}
              ref={urlInputRef}
            />
          </div>

          {/* Enhanced Actions */}
          <div className="flex items-center space-x-2">
            <button 
              className="nav-btn"
              onClick={() => setShowBookmarkBar(!showBookmarkBar)}
              title="Toggle Bookmark Bar"
            >
              <Bookmark size={16} className={showBookmarkBar ? 'text-yellow-400' : ''} />
            </button>
            
            <button 
              className="nav-btn"
              onClick={() => createNewTab()}
              title="New Tab (Ctrl+T)"
            >
              <Plus size={16} />
            </button>
            
            {/* Comprehensive Features Button */}
            <button 
              className={`nav-btn ${showComprehensiveFeatures ? 'bg-green-600/30 border-green-500/30' : ''}`}
              onClick={() => setShowComprehensiveFeatures(!showComprehensiveFeatures)}
              title="🚀 All 17 Features Ready"
            >
              <Sparkles size={16} className={showComprehensiveFeatures ? 'text-green-300' : ''} />
              <span className="ml-1 text-xs">17</span>
            </button>
            
            {/* Voice Commands Toggle */}
            <button 
              className={`nav-btn ${showVoiceCommands ? 'bg-red-600/30 border-red-500/30' : ''}`}
              onClick={() => setShowVoiceCommands(!showVoiceCommands)}
              title="Voice Commands (Hey ARIA)"
            >
              <MessageSquare size={16} className={showVoiceCommands ? 'text-red-300' : ''} />
            </button>
            
            {/* AI Panel Toggle */}
            <button 
              className={`nav-btn ${showAIPanel ? 'bg-purple-600/30 border-purple-500/30' : ''}`}
              onClick={() => setShowAIPanel(!showAIPanel)}
              title="AI Insights Panel"
            >
              <Brain size={16} className={showAIPanel ? 'text-purple-300' : ''} />
            </button>
            
            {/* Tab Groups Toggle */}
            <button 
              className="nav-btn"
              onClick={() => setShowTabGroups(!showTabGroups)}
              title="Tab Groups"
            >
              <Layers size={16} />
            </button>
            
            <button 
              className="nav-btn"
              title="Settings"
            >
              <Settings size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Bookmark Bar */}
      <AnimatePresence>
        {showBookmarkBar && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="bookmark-bar bg-gray-800/50 border-b border-gray-700/30 px-4 py-2 flex items-center space-x-2 overflow-x-auto"
          >
            {bookmarks.length === 0 ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-400">Add bookmarks for quick access</span>
                <button 
                  className="text-xs bg-blue-600/20 text-blue-300 px-3 py-1 rounded-full hover:bg-blue-600/30 transition-colors"
                  onClick={() => {/* Add bookmark logic */}}
                >
                  + Bookmark Current Page
                </button>
              </div>
            ) : (
              bookmarks.map((bookmark, index) => (
                <button
                  key={index}
                  onClick={() => navigateToUrl(bookmark.url)}
                  className="flex items-center space-x-1 px-2 py-1 hover:bg-gray-700/50 rounded text-sm text-gray-300 hover:text-white transition-colors"
                >
                  <Globe size={12} />
                  <span>{bookmark.title}</span>
                </button>
              ))
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Tab Bar */}
      <EnhancedTabManager 
        tabs={tabs}
        activeTabId={activeTabId}
        onSwitchTab={switchToTab}
        onCloseTab={closeTab}
        onCreateTab={() => createNewTab()}
        tabGroups={tabGroups}
        showGroups={showTabGroups}
        recentlyClosedTabs={recentlyClosedTabs}
        onReopenTab={(tab) => createNewTab(tab.url, tab.title)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex relative overflow-hidden">
        
        {/* Web Content Area */}
        <div className={`flex-1 transition-all duration-300 ${showAIPanel ? `mr-${Math.floor(sidebarWidth/4)}` : ''}`}>
          {activeTab ? (
            activeTab.url.startsWith('about:') ? (
              <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
                <div className="text-center space-y-6 max-w-2xl mx-auto p-8">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                  >
                    <div className="w-24 h-24 mx-auto bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                      <Globe size={48} className="text-white" />
                    </div>
                    <h1 className="text-4xl font-bold text-white">
                      Welcome to AI Browser
                    </h1>
                    <p className="text-gray-400 text-lg">
                      The intelligent browser that enhances every aspect of your web experience
                    </p>
                  </motion.div>

                  {/* Quick Actions */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { icon: Search, text: 'Smart Search', url: 'https://google.com' },
                      { icon: BookOpen, text: 'AI Research', url: 'https://scholar.google.com' },
                      { icon: TrendingUp, text: 'News & Trends', url: 'https://news.google.com' },
                      { icon: BarChart3, text: 'Analytics', url: 'about:analytics' }
                    ].map((item, index) => (
                      <motion.button
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => navigateToUrl(item.url)}
                        className="p-6 rounded-xl bg-gray-800/50 border border-gray-700/30 hover:bg-gray-700/50 transition-colors group"
                      >
                        <item.icon size={32} className="mx-auto mb-3 text-gray-400 group-hover:text-purple-400 transition-colors" />
                        <div className="text-sm text-gray-300 group-hover:text-white transition-colors">{item.text}</div>
                      </motion.button>
                    ))}
                  </div>

                  {/* Feature Showcase */}
                  <div className="mt-8 pt-8 border-t border-gray-700/30">
                    <h3 className="text-xl font-semibold text-white mb-4 text-center">
                      🚀 All 17 Features Available
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                      {[
                        {
                          icon: '🧠',
                          title: 'Memory & Performance',
                          features: ['Smart Memory Management', 'Predictive Caching', 'Real-time Monitoring', 'Bandwidth Optimization'],
                          color: 'from-blue-500 to-cyan-500'
                        },
                        {
                          icon: '🎯',
                          title: 'Tab & Navigation',
                          features: ['3D Tab Workspace', 'Natural Language Navigation', 'AI-Powered Browsing'],
                          color: 'from-green-500 to-teal-500'
                        },
                        {
                          icon: '🤖',
                          title: 'AI Actions & Voice',
                          features: ['Hey ARIA Commands', 'One-Click Actions', 'Smart Context Menu', 'Quick Actions Bar'],
                          color: 'from-purple-500 to-pink-500'
                        }
                      ].map((category, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.5 + index * 0.1 }}
                          className="bg-gray-800/30 rounded-xl p-4 border border-gray-700/30"
                        >
                          <div className="text-center mb-3">
                            <div className="text-2xl mb-2">{category.icon}</div>
                            <h4 className="text-white font-medium text-sm">{category.title}</h4>
                          </div>
                          <ul className="space-y-1">
                            {category.features.map((feature, idx) => (
                              <li key={idx} className="text-xs text-gray-400 flex items-center">
                                <span className="w-1 h-1 bg-green-400 rounded-full mr-2"></span>
                                {feature}
                              </li>
                            ))}
                          </ul>
                        </motion.div>
                      ))}
                    </div>
                    
                    <div className="text-center">
                      <button
                        onClick={() => setShowComprehensiveFeatures(true)}
                        className="px-6 py-3 bg-gradient-to-r from-green-600 to-blue-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-green-500/25 transition-all duration-300 mr-4"
                      >
                        🚀 Explore All 17 Features
                      </button>
                      <button
                        onClick={() => setShowVoiceCommands(true)}
                        className="px-6 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-red-500/25 transition-all duration-300"
                      >
                        🎙️ Try Voice Commands
                      </button>
                    </div>
                  </div>

                  <div className="text-center">
                    <button
                      onClick={() => {
                        navigateToUrl('https://google.com');
                        setTimeout(() => urlInputRef.current?.focus(), 100);
                      }}
                      className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 transition-all duration-300"
                    >
                      Start Browsing with AI
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <EmbeddedWebView 
                ref={webViewRef}
                tabId={activeTabId}
                url={activeTab.url}
                title={activeTab.title}
                isLoading={activeTab.isLoading || isLoading}
                onTitleChange={(title) => {
                  setTabs(prev => prev.map(tab => 
                    tab.id === activeTabId ? { ...tab, title } : tab
                  ));
                }}
                onUrlChange={(url) => {
                  setCurrentUrl(url);
                  setTabs(prev => prev.map(tab => 
                    tab.id === activeTabId ? { ...tab, url } : tab
                  ));
                }}
              />
            )
          ) : (
            <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
              <div className="text-center">
                <Globe size={48} className="mx-auto mb-4 text-gray-600" />
                <p className="text-gray-400">No active tab</p>
                <button
                  onClick={() => createNewTab()}
                  className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                >
                  Create New Tab
                </button>
              </div>
            </div>
          )}
        </div>

        {/* AI Insights Panel */}
        <AnimatePresence>
          {showAIPanel && (
            <motion.div
              initial={{ x: sidebarWidth, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: sidebarWidth, opacity: 0 }}
              className="border-l border-gray-700/50"
              style={{ width: sidebarWidth }}
            >
              <AIInsightsPanel 
                pageAnalysis={pageAnalysis}
                insights={aiInsights}
                contextualActions={contextualActions}
                currentUrl={currentUrl}
                currentTab={activeTab}
                onActionExecute={(action) => {
                  console.log('Executing action:', action);
                  // Handle contextual AI actions using comprehensive features
                  if (action.type === 'smart_bookmark') {
                    comprehensiveFeaturesService.createSmartBookmark(currentUrl, { title: currentTab?.title });
                  } else if (action.type === 'voice_command') {
                    setShowVoiceCommands(true);
                  } else if (action.type === 'analyze_content') {
                    comprehensiveFeaturesService.getOneClickAIActions({ url: currentUrl, content: pageAnalysis });
                  } else if (action.type === 'organize_tabs') {
                    comprehensiveFeaturesService.advancedTabManagement('organize_3d_workspace', tabs);
                  }
                }}
                onClose={() => setShowAIPanel(false)}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Comprehensive Features Panel */}
      <ComprehensiveFeaturesPanel 
        isVisible={showComprehensiveFeatures}
        onClose={() => setShowComprehensiveFeatures(false)}
      />

      {/* Voice Commands Panel */}
      <AnimatePresence>
        {showVoiceCommands && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowVoiceCommands(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gray-900/95 backdrop-blur-md rounded-2xl border border-gray-700/50 shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-pink-500 rounded-lg flex items-center justify-center">
                      <MessageSquare size={20} className="text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Voice Commands</h3>
                      <p className="text-gray-400 text-sm">Say "Hey ARIA" to activate</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setShowVoiceCommands(false)}
                    className="p-2 hover:bg-gray-700/50 rounded-lg text-gray-400 hover:text-white transition-colors"
                  >
                    <X size={20} />
                  </button>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700/30">
                    <h4 className="text-white font-medium mb-3">Available Voice Commands</h4>
                    <div className="grid gap-2">
                      {[
                        { command: 'Hey ARIA, open Google', description: 'Navigate to Google search' },
                        { command: 'Hey ARIA, analyze this page', description: 'Get AI insights about current page' },
                        { command: 'Hey ARIA, summarize content', description: 'Create a summary of the page' },
                        { command: 'Hey ARIA, bookmark this page', description: 'Smart bookmark with AI categorization' },
                        { command: 'Hey ARIA, organize my tabs', description: 'Arrange tabs in 3D workspace' },
                        { command: 'Hey ARIA, boost performance', description: 'Optimize browser performance' }
                      ].map((item, index) => (
                        <div key={index} className="bg-gray-900/50 rounded-lg p-3">
                          <div className="text-green-300 font-medium text-sm mb-1">{item.command}</div>
                          <div className="text-gray-400 text-xs">{item.description}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="bg-red-600/10 border border-red-500/20 rounded-lg p-4">
                    <div className="flex items-center space-x-2 text-red-300 mb-2">
                      <MessageSquare size={16} />
                      <span className="font-medium">Status</span>
                    </div>
                    <p className="text-gray-300 text-sm">
                      Voice recognition is ready. Click the microphone button or say "Hey ARIA" to start.
                    </p>
                    
                    <button
                      onClick={async () => {
                        try {
                          const result = await parallelFeatures.processVoiceCommand('Hey ARIA, help me', { url: currentUrl });
                          console.log('Voice command result:', result);
                        } catch (error) {
                          console.error('Voice command error:', error);
                        }
                      }}
                      className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                    >
                      🎙️ Test Voice Command
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Status Bar */}
      <div className="status-bar bg-gray-900/80 border-t border-gray-700/30 px-4 py-1 flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center space-x-4">
          <span>Tabs: {tabs.length}</span>
          {browserReady && (
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span>Browser Ready</span>
            </span>
          )}
          {pageAnalysis && (
            <span className="flex items-center space-x-1">
              <Brain size={10} className="text-purple-400" />
              <span>AI Analysis Active</span>
            </span>
          )}
          {comprehensiveFeatures && (
            <span className="flex items-center space-x-1">
              <Sparkles size={10} className="text-green-400" />
              <span>17 Features Available</span>
            </span>
          )}
          {parallelFeatures.voiceActive && (
            <span className="flex items-center space-x-1">
              <MessageSquare size={10} className="text-red-400" />
              <span>Voice Commands Active</span>
            </span>
          )}
        </div>
        <div className="flex items-center space-x-4">
          <span>
            Unified AI Browser v3.0 - Powered by Real Chromium + Advanced AI
          </span>
          {comprehensiveFeatures?.implementation_summary && (
            <span className="text-green-400">
              {comprehensiveFeatures.implementation_summary.implementation_rate} Complete
            </span>
          )}
        </div>
      </div>
    </div>
  );
}