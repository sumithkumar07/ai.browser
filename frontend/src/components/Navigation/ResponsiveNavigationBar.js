import React, { useState, useEffect } from 'react';
import { useUser } from '../../contexts/UserContext';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronLeft, 
  ChevronRight, 
  RotateCcw, 
  Home, 
  Search, 
  Menu, 
  X, 
  Settings, 
  User, 
  Brain, 
  Zap,
  Monitor,
  Smartphone,
  Tablet,
  Globe,
  Star,
  Clock,
  TrendingUp
} from 'lucide-react';

export default function ResponsiveNavigationBar() {
  const { user } = useUser();
  const { tabs, activeTab, addTab } = useBrowser();
  const { toggleAssistant, isAssistantVisible } = useAI();
  
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [viewportSize, setViewportSize] = useState('desktop');
  const [searchSuggestions, setSearchSuggestions] = useState([]);
  const [showSearchSuggestions, setShowSearchSuggestions] = useState(false);

  // Responsive viewport detection
  useEffect(() => {
    const checkViewportSize = () => {
      const width = window.innerWidth;
      if (width < 640) setViewportSize('mobile');
      else if (width < 1024) setViewportSize('tablet');
      else setViewportSize('desktop');
    };

    checkViewportSize();
    window.addEventListener('resize', checkViewportSize);
    return () => window.removeEventListener('resize', checkViewportSize);
  }, []);

  // Update current URL based on active tab
  useEffect(() => {
    const activeTabData = tabs.find(tab => tab.id === activeTab);
    if (activeTabData) {
      setCurrentUrl(activeTabData.url === 'about:blank' ? '' : activeTabData.url);
    }
  }, [activeTab, tabs]);

  const handleNavigation = async (url) => {
    if (!url.trim()) return;
    
    setIsLoading(true);
    
    try {
      // Validate and format URL
      let formattedUrl = url.trim();
      if (!formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
        if (formattedUrl.includes('.') && !formattedUrl.includes(' ')) {
          formattedUrl = `https://${formattedUrl}`;
        } else {
          formattedUrl = `https://www.google.com/search?q=${encodeURIComponent(formattedUrl)}`;
        }
      }

      // Update current tab or create new one
      if (activeTab) {
        // Update existing tab
        const tabIndex = tabs.findIndex(tab => tab.id === activeTab);
        if (tabIndex !== -1) {
          tabs[tabIndex].url = formattedUrl;
          tabs[tabIndex].title = 'Loading...';
          
          // Simulate loading and get page title
          setTimeout(() => {
            try {
              const domain = new URL(formattedUrl).hostname;
              tabs[tabIndex].title = domain.charAt(0).toUpperCase() + domain.slice(1);
            } catch {
              tabs[tabIndex].title = 'New Page';
            }
          }, 1000);
        }
      } else {
        // Create new tab
        const newTab = {
          id: `tab-${Date.now()}`,
          url: formattedUrl,
          title: 'Loading...',
          position_x: 200 + Math.random() * 200,
          position_y: 150 + Math.random() * 200,
          is_active: true,
          created_at: new Date().toISOString()
        };
        addTab(newTab);
      }

      setCurrentUrl(formattedUrl);
      setShowSearchSuggestions(false);
      
    } catch (error) {
      console.error('Navigation failed:', error);
    } finally {
      setTimeout(() => setIsLoading(false), 800);
    }
  };

  const generateSearchSuggestions = async (query) => {
    if (!query.trim() || query.length < 2) {
      setSearchSuggestions([]);
      return;
    }

    // Mock search suggestions (in real app, this would call a search API)
    const mockSuggestions = [
      `${query} - Google Search`,
      `${query} site:github.com`,
      `${query} tutorial`,
      `${query} documentation`,
      `what is ${query}`,
    ];

    setSearchSuggestions(mockSuggestions.slice(0, 5));
  };

  const handleUrlChange = (e) => {
    const value = e.target.value;
    setCurrentUrl(value);
    generateSearchSuggestions(value);
    setShowSearchSuggestions(value.length > 0);
  };

  const getViewportIcon = () => {
    switch (viewportSize) {
      case 'mobile': return <Smartphone size={16} className="text-green-400" />;
      case 'tablet': return <Tablet size={16} className="text-blue-400" />;
      default: return <Monitor size={16} className="text-purple-400" />;
    }
  };

  const NavigationControls = ({ isMobile = false }) => (
    <div className={`flex items-center ${isMobile ? 'space-x-4 w-full justify-between' : 'space-x-2'}`}>
      {/* Back/Forward/Refresh */}
      <div className="flex items-center space-x-1">
        <button
          className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200 disabled:opacity-50"
          title="Go Back"
          disabled={true} // In real implementation, track navigation history
        >
          <ChevronLeft size={16} />
        </button>
        
        <button
          className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200 disabled:opacity-50"
          title="Go Forward"
          disabled={true}
        >
          <ChevronRight size={16} />
        </button>
        
        <motion.button
          className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200"
          title="Refresh"
          whileTap={{ rotate: 180 }}
          onClick={() => {
            if (activeTab) {
              setIsLoading(true);
              setTimeout(() => setIsLoading(false), 1000);
            }
          }}
        >
          <RotateCcw size={16} className={isLoading ? 'animate-spin' : ''} />
        </motion.button>

        <button
          className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200"
          title="Home"
          onClick={() => handleNavigation('https://google.com')}
        >
          <Home size={16} />
        </button>
      </div>

      {/* Quick Actions (Desktop Only) */}
      {!isMobile && (
        <div className="flex items-center space-x-1">
          <button
            className="w-8 h-8 rounded-lg bg-purple-600/20 hover:bg-purple-600/30 flex items-center justify-center text-purple-400 hover:text-purple-300 transition-all duration-200"
            title="AI Assistant"
            onClick={toggleAssistant}
          >
            <Brain size={16} className={isAssistantVisible ? 'animate-pulse' : ''} />
          </button>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Main Navigation Bar */}
      <motion.div
        className={`fixed top-0 left-0 right-0 z-40 bg-gray-900/95 backdrop-blur-xl border-b border-gray-800/50 ${
          viewportSize === 'mobile' ? 'h-16' : 'h-14'
        }`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center h-full px-4 space-x-4">
          {/* Mobile Menu Toggle */}
          {viewportSize === 'mobile' && (
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="w-10 h-10 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          )}

          {/* Desktop Navigation Controls */}
          {viewportSize !== 'mobile' && <NavigationControls />}

          {/* URL/Search Bar */}
          <div className="flex-1 max-w-2xl relative">
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1 }}
                  >
                    <RotateCcw size={16} />
                  </motion.div>
                ) : (
                  <Search size={16} />
                )}
              </div>
              
              <input
                type="text"
                value={currentUrl}
                onChange={handleUrlChange}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleNavigation(currentUrl);
                  } else if (e.key === 'Escape') {
                    setShowSearchSuggestions(false);
                  }
                }}
                onFocus={() => setShowSearchSuggestions(currentUrl.length > 0)}
                placeholder="Search or enter URL..."
                className={`w-full ${
                  viewportSize === 'mobile' ? 'h-10 text-sm' : 'h-9 text-sm'
                } pl-10 pr-12 bg-gray-800/80 border border-gray-700/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500/50 focus:bg-gray-800 transition-all duration-200`}
              />

              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
                {currentUrl && (
                  <button
                    onClick={() => {
                      setCurrentUrl('');
                      setShowSearchSuggestions(false);
                    }}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    <X size={14} />
                  </button>
                )}
                {getViewportIcon()}
              </div>
            </div>

            {/* Search Suggestions Dropdown */}
            <AnimatePresence>
              {showSearchSuggestions && searchSuggestions.length > 0 && (
                <motion.div
                  className="absolute top-full left-0 right-0 mt-1 bg-gray-900/95 backdrop-blur-xl border border-gray-700/50 rounded-xl shadow-2xl z-50"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  {searchSuggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setCurrentUrl(suggestion);
                        handleNavigation(suggestion);
                      }}
                      className="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-gray-800/50 hover:text-white first:rounded-t-xl last:rounded-b-xl transition-colors flex items-center"
                    >
                      <Search size={14} className="mr-3 text-gray-400" />
                      {suggestion}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Desktop Right Actions */}
          {viewportSize !== 'mobile' && (
            <div className="flex items-center space-x-2">
              {/* Tab Counter */}
              <div className="flex items-center space-x-2 px-3 py-1 bg-gray-800/50 rounded-lg border border-gray-700/30">
                <Globe size={14} className="text-gray-400" />
                <span className="text-sm text-gray-300">{tabs.length}</span>
              </div>

              {/* User Menu */}
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                  <User size={14} className="text-white" />
                </div>
                <div className="hidden lg:block">
                  <span className="text-sm text-gray-300">{user?.user_mode || 'Guest'}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Mobile Menu Sidebar */}
      <AnimatePresence>
        {isMobileMenuOpen && viewportSize === 'mobile' && (
          <>
            {/* Backdrop */}
            <motion.div
              className="fixed inset-0 bg-black/50 z-50"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileMenuOpen(false)}
            />

            {/* Mobile Menu Panel */}
            <motion.div
              className="fixed left-0 top-0 bottom-0 w-80 bg-gray-900/98 backdrop-blur-xl border-r border-gray-800/50 z-50"
              initial={{ x: -320 }}
              animate={{ x: 0 }}
              exit={{ x: -320 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              <div className="h-full flex flex-col">
                {/* Mobile Menu Header */}
                <div className="p-4 border-b border-gray-800/50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                        <Brain size={20} className="text-white" />
                      </div>
                      <div>
                        <h2 className="text-white font-semibold">AI Browser</h2>
                        <p className="text-gray-400 text-sm">{user?.user_mode || 'Guest Mode'}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                    >
                      <X size={18} />
                    </button>
                  </div>
                </div>

                {/* Navigation Controls */}
                <div className="p-4 border-b border-gray-800/50">
                  <h3 className="text-gray-300 font-medium mb-3 text-sm">Navigation</h3>
                  <NavigationControls isMobile={true} />
                </div>

                {/* Quick Actions */}
                <div className="p-4 border-b border-gray-800/50">
                  <h3 className="text-gray-300 font-medium mb-3 text-sm">Quick Actions</h3>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => {
                        toggleAssistant();
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex items-center justify-center p-3 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 rounded-lg transition-colors"
                    >
                      <Brain size={16} className="mr-2" />
                      AI Assistant
                    </button>
                    
                    <button
                      onClick={() => {
                        // Add new tab
                        const newTab = {
                          id: `tab-${Date.now()}`,
                          url: 'about:blank',
                          title: 'New Tab',
                          position_x: 200,
                          position_y: 150,
                          is_active: false
                        };
                        addTab(newTab);
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex items-center justify-center p-3 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 rounded-lg transition-colors"
                    >
                      <Globe size={16} className="mr-2" />
                      New Tab
                    </button>
                  </div>
                </div>

                {/* Tab Management */}
                <div className="flex-1 p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-gray-300 font-medium text-sm">Open Tabs ({tabs.length})</h3>
                    <TrendingUp size={14} className="text-gray-400" />
                  </div>
                  
                  <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
                    {tabs.map((tab) => (
                      <div
                        key={tab.id}
                        className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                          activeTab === tab.id 
                            ? 'bg-purple-600/20 border border-purple-600/30' 
                            : 'bg-gray-800/30 hover:bg-gray-800/50'
                        }`}
                        onClick={() => {
                          // setActiveTab(tab.id);
                          setIsMobileMenuOpen(false);
                        }}
                      >
                        <div className="w-8 h-8 bg-gray-700 rounded-lg flex items-center justify-center mr-3 text-sm">
                          {tab.title ? tab.title.charAt(0).toUpperCase() : '🌐'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="text-white text-sm font-medium truncate">
                            {tab.title || 'Untitled'}
                          </h4>
                          <p className="text-gray-400 text-xs truncate">
                            {tab.url === 'about:blank' ? 'New Tab' : tab.url}
                          </p>
                        </div>
                        {activeTab === tab.id && (
                          <div className="w-2 h-2 bg-purple-400 rounded-full" />
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-gray-800/50">
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>Viewport: {viewportSize}</span>
                    <span>v2.0 Enhanced</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}