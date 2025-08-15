import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, ArrowRight, RotateCcw, Home, Star, Download, 
  History, Bookmark, Settings, HelpCircle, Plus, X, Search,
  Globe, Shield, ExternalLink, Menu, BookOpen, Clock, Activity, Zap
} from 'lucide-react';
import HybridBrowserPanel from '../HybridBrowser/HybridBrowserPanel';
import HybridBrowserService from '../../services/HybridBrowserService';
import RealBrowserInterface from '../RealBrowser/RealBrowserInterface';

export default function SimplifiedBrowser() {
  // Simplified state management - focusing only on essentials
  const [tabs, setTabs] = useState([]);
  const [activeTab, setActiveTab] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [onboardingStep, setOnboardingStep] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [showHybridPanel, setShowHybridPanel] = useState(false);
  
  const urlInputRef = useRef(null);

  // Initialize with onboarding
  useEffect(() => {
    initializeSimplifiedBrowser();
  }, []);

  const initializeSimplifiedBrowser = async () => {
    try {
      // Start personalized onboarding
      const onboardingResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/onboarding`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_data: { first_time: true } })
      });
      
      if (onboardingResponse.ok) {
        const onboarding = await onboardingResponse.json();
        console.log('✅ Personalized onboarding started:', onboarding.onboarding.user_type);
      }

      // Create first tab
      createNewTab('about:blank');
      
    } catch (error) {
      console.error('Initialization error:', error);
      // Fallback: create basic tab
      createNewTab('about:blank');
    }
  };

  const createNewTab = async (url = 'about:blank') => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/tabs/new`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, position: { x: 200, y: 150 } })
      });

      if (response.ok) {
        const result = await response.json();
        const newTab = result.tab;
        
        setTabs(prev => [...prev, newTab]);
        setActiveTab(newTab.id);
        
        if (url !== 'about:blank') {
          setCurrentUrl(url);
        }
        
        console.log('✅ New tab created:', newTab.id);
      }
    } catch (error) {
      console.error('Tab creation error:', error);
      
      // Fallback: create local tab
      const fallbackTab = {
        id: `tab-${Date.now()}`,
        url: url,
        title: url === 'about:blank' ? 'New Tab' : 'Loading...',
        isLoading: url !== 'about:blank',
        created_at: new Date().toISOString()
      };
      
      setTabs(prev => [...prev, fallbackTab]);
      setActiveTab(fallbackTab.id);
    }
  };

  const navigateToUrl = async (url) => {
    if (!url.trim() || !activeTab) return;
    
    setIsLoading(true);
    setShowSuggestions(false);
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/navigate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim(), tab_id: activeTab })
      });

      if (response.ok) {
        const result = await response.json();
        
        // Update tab with navigation result
        setTabs(prev => prev.map(tab => 
          tab.id === activeTab 
            ? { ...tab, url: result.navigation.url, title: result.navigation.page_title, isLoading: false }
            : tab
        ));
        
        setCurrentUrl(result.navigation.url);
        console.log('✅ Navigation successful:', result.navigation.url);
      }
    } catch (error) {
      console.error('Navigation error:', error);
      
      // Fallback: update tab locally
      setTabs(prev => prev.map(tab => 
        tab.id === activeTab 
          ? { ...tab, url: url, title: 'Error Loading', isLoading: false }
          : tab
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const closeTab = async (tabId) => {
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/tabs/${tabId}`, {
        method: 'DELETE'
      });
      
      setTabs(prev => {
        const remaining = prev.filter(tab => tab.id !== tabId);
        
        // If closing active tab, switch to another or create new one
        if (tabId === activeTab) {
          if (remaining.length > 0) {
            setActiveTab(remaining[0].id);
          } else {
            createNewTab('about:blank');
            return remaining;
          }
        }
        
        return remaining;
      });
      
    } catch (error) {
      console.error('Tab close error:', error);
    }
  };

  const getSmartSuggestions = async (query) => {
    if (!query || query.length < 2) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/smart-suggestions`);
      
      if (response.ok) {
        const result = await response.json();
        setSuggestions(result.suggestions.slice(0, 4));
      }
    } catch (error) {
      console.error('Suggestions error:', error);
      
      // Fallback suggestions
      setSuggestions([
        { text: `Search for "${query}"`, action: 'search', icon: 'search' },
        { text: `Go to ${query}.com`, action: 'navigate', icon: 'globe' },
        { text: 'Open bookmarks', action: 'bookmarks', icon: 'bookmark' },
        { text: 'View history', action: 'history', icon: 'history' }
      ]);
    }
  };

  const handleUrlChange = (e) => {
    const value = e.target.value;
    setCurrentUrl(value);
    
    if (value.length > 1) {
      setShowSuggestions(true);
      getSmartSuggestions(value);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      navigateToUrl(currentUrl);
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  // Quick action handlers
  const handleQuickAction = async (action) => {
    switch (action) {
      case 'new_tab':
        createNewTab();
        break;
      case 'bookmarks':
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/bookmarks`);
          if (response.ok) {
            const bookmarks = await response.json();
            console.log('Bookmarks:', bookmarks);
            // In a real implementation, this would open bookmarks panel
          }
        } catch (error) {
          console.error('Bookmarks error:', error);
        }
        break;
      case 'history':
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/history`);
          if (response.ok) {
            const history = await response.json();
            console.log('History:', history);
            // In a real implementation, this would open history panel
          }
        } catch (error) {
          console.error('History error:', error);
        }
        break;
      case 'downloads':
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/browser/enhanced/downloads`);
          if (response.ok) {
            const downloads = await response.json();
            console.log('Downloads:', downloads);
            // In a real implementation, this would open downloads panel
          }
        } catch (error) {
          console.error('Downloads error:', error);
        }
        break;
      case 'hybrid_features':
        setShowHybridPanel(true);
        break;
      default:
        console.log('Quick action:', action);
    }
  };

  return (
    <div className="simplified-browser h-screen w-screen flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      
      {/* Simplified Navigation Bar - Real Browser Style */}
      <div className="navigation-bar bg-gray-900/90 backdrop-blur-sm border-b border-gray-700/50 p-3">
        <div className="flex items-center space-x-3">
          
          {/* Browser Controls */}
          <div className="flex items-center space-x-1">
            <button className="nav-btn" title="Back">
              <ArrowLeft size={16} />
            </button>
            <button className="nav-btn" title="Forward">
              <ArrowRight size={16} />
            </button>
            <button 
              className="nav-btn"
              onClick={() => navigateToUrl(currentUrl)}
              title="Refresh"
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

          {/* URL Bar - Core Browser Feature */}
          <div className="flex-1 relative">
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                <Shield size={14} className="text-green-400" />
              </div>
              
              <input
                ref={urlInputRef}
                type="text"
                value={currentUrl}
                onChange={handleUrlChange}
                onKeyDown={handleKeyPress}
                onFocus={() => currentUrl && setShowSuggestions(true)}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
                placeholder="Search or enter URL..."
                className="w-full h-9 pl-10 pr-20 bg-gray-800/70 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500/50 focus:bg-gray-800/90 text-sm"
              />
              
              {/* URL Bar Actions */}
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
                {currentUrl && (
                  <button
                    onClick={() => handleQuickAction('bookmark')}
                    className="p-1 hover:bg-gray-700 rounded"
                    title="Bookmark"
                  >
                    <Star size={12} className="text-gray-400 hover:text-yellow-400" />
                  </button>
                )}
                <div className="w-4 h-4 flex items-center justify-center">
                  <Globe size={10} className="text-gray-500" />
                </div>
              </div>
            </div>

            {/* Smart Suggestions */}
            <AnimatePresence>
              {showSuggestions && suggestions.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="absolute top-full left-0 right-0 mt-1 bg-gray-800/95 backdrop-blur-sm border border-gray-600/50 rounded-lg shadow-xl z-50"
                >
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        if (suggestion.action === 'search') {
                          navigateToUrl(currentUrl);
                        } else if (suggestion.action === 'navigate') {
                          navigateToUrl(suggestion.text.split(' ').pop());
                        } else {
                          handleQuickAction(suggestion.action);
                        }
                      }}
                      className="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-gray-700/50 first:rounded-t-lg last:rounded-b-lg flex items-center space-x-2"
                    >
                      <Search size={12} className="text-gray-500" />
                      <span>{suggestion.text}</span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center space-x-2">
            <button 
              className="nav-btn"
              onClick={() => createNewTab()}
              title="New Tab (Ctrl+T)"
            >
              <Plus size={16} />
            </button>
            
            <button 
              className="nav-btn"
              onClick={() => handleQuickAction('downloads')}
              title="Downloads"
            >
              <Download size={16} />
            </button>
            
            {/* Hybrid Browser Access Button */}
            <button 
              className="nav-btn bg-gradient-to-r from-purple-600/20 to-blue-600/20 hover:from-purple-600/30 hover:to-blue-600/30 border border-purple-500/30"
              onClick={() => setShowHybridPanel(true)}
              title="Hybrid Browser Features"
            >
              <Activity size={16} className="text-purple-300" />
            </button>
            
            {/* Mobile Menu Toggle */}
            <button 
              className="nav-btn md:hidden"
              onClick={() => setShowMobileMenu(!showMobileMenu)}
            >
              <Menu size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Tab Bar - Real Browser Tabs */}
      {tabs.length > 0 && (
        <div className="tab-bar bg-gray-800/50 border-b border-gray-700/30 px-3 py-1 flex items-center space-x-1 overflow-x-auto">
          {tabs.map((tab) => (
            <div
              key={tab.id}
              className={`tab flex items-center space-x-2 px-3 py-1 rounded-t-lg cursor-pointer transition-colors min-w-[120px] max-w-[200px] ${
                tab.id === activeTab 
                  ? 'bg-gray-700 text-white border-t-2 border-blue-500' 
                  : 'bg-gray-800/30 text-gray-400 hover:bg-gray-700/50'
              }`}
              onClick={() => setActiveTab(tab.id)}
            >
              <div className="flex-1 min-w-0">
                <div className="text-xs truncate">
                  {tab.isLoading ? (
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      <span>Loading...</span>
                    </div>
                  ) : (
                    tab.title || 'New Tab'
                  )}
                </div>
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  closeTab(tab.id);
                }}
                className="p-0.5 hover:bg-gray-600 rounded text-gray-500 hover:text-white"
              >
                <X size={12} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 relative">
        {tabs.length === 0 ? (
          /* Welcome Screen - Simplified */
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-6 max-w-2xl mx-auto p-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                <h1 className="text-4xl font-bold text-white">
                  Welcome to Your Simplified AI Browser
                </h1>
                <p className="text-gray-400 text-lg">
                  Real browsing made simple with AI assistance
                </p>
              </motion.div>

              {/* Quick Start Actions */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {[
                  { icon: Plus, text: 'New Tab', action: 'new_tab' },
                  { icon: Bookmark, text: 'Bookmarks', action: 'bookmarks' },
                  { icon: History, text: 'History', action: 'history' }, 
                  { icon: Download, text: 'Downloads', action: 'downloads' },
                  { icon: Activity, text: 'Hybrid AI', action: 'hybrid_features', special: true }
                ].map((item, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleQuickAction(item.action)}
                    className={`p-4 rounded-xl border border-gray-700/30 transition-colors ${
                      item.special 
                        ? 'bg-gradient-to-r from-purple-600/20 to-blue-600/20 hover:from-purple-600/30 hover:to-blue-600/30 border-purple-500/30'
                        : 'bg-gray-800/50 hover:bg-gray-700/50'
                    }`}
                  >
                    <item.icon size={24} className={`mx-auto mb-2 ${item.special ? 'text-purple-300' : 'text-gray-400'}`} />
                    <div className={`text-sm ${item.special ? 'text-purple-200' : 'text-gray-300'}`}>{item.text}</div>
                  </motion.button>
                ))}
              </div>

              {/* Getting Started */}
              <div className="text-center">
                <button
                  onClick={() => {
                    createNewTab();
                    setTimeout(() => urlInputRef.current?.focus(), 100);
                  }}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                >
                  Start Browsing
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Active Tab Content */
          <div className="h-full bg-gray-900/30">
            <div className="h-full flex items-center justify-center">
              <div className="text-center space-y-4">
                <Globe size={48} className="mx-auto text-gray-600" />
                <div className="text-gray-400">
                  <p className="text-lg">Browser Content Area</p>
                  <p className="text-sm">In a real browser, web content would be displayed here</p>
                  <p className="text-xs text-gray-500 mt-2">
                    Current URL: {currentUrl || 'about:blank'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {showMobileMenu && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            className="fixed right-0 top-0 bottom-0 w-80 bg-gray-900/95 backdrop-blur-sm border-l border-gray-700/50 z-50 p-4"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-white font-medium">Browser Menu</h3>
              <button
                onClick={() => setShowMobileMenu(false)}
                className="p-2 hover:bg-gray-800 rounded"
              >
                <X size={20} className="text-gray-400" />
              </button>
            </div>

            <div className="space-y-3">
              {[
                { icon: Bookmark, text: 'Bookmarks', action: 'bookmarks' },
                { icon: History, text: 'History', action: 'history' },
                { icon: Download, text: 'Downloads', action: 'downloads' },
                { icon: Settings, text: 'Settings', action: 'settings' },
                { icon: HelpCircle, text: 'Help', action: 'help' }
              ].map((item, index) => (
                <button
                  key={index}
                  onClick={() => {
                    handleQuickAction(item.action);
                    setShowMobileMenu(false);
                  }}
                  className="w-full flex items-center space-x-3 p-3 hover:bg-gray-800/50 rounded-lg text-left"
                >
                  <item.icon size={20} className="text-gray-400" />
                  <span className="text-gray-300">{item.text}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Simplified Status Bar */}
      <div className="status-bar bg-gray-900/70 border-t border-gray-700/30 px-4 py-1 flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center space-x-4">
          <span>Tabs: {tabs.length}</span>
          <span className="flex items-center space-x-1">
            <Shield size={10} className="text-green-400" />
            <span>Secure</span>
          </span>
        </div>
        <div>
          AI Browser v2.0 Enhanced
        </div>
      </div>

      {/* Hybrid Browser Panel */}
      <HybridBrowserPanel 
        isVisible={showHybridPanel}
        onClose={() => setShowHybridPanel(false)}
      />
    </div>
  );
}