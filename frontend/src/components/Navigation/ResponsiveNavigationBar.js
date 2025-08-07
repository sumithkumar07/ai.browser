import React, { useState, useEffect, useCallback } from 'react';
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
  TrendingUp,
  Shield,
  Bookmark,
  History,
  Plus,
  Command,
  Wifi,
  WifiOff
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
  const [isSecure, setIsSecure] = useState(true);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [searchHistory, setSearchHistory] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [showShortcuts, setShowShortcuts] = useState(false);

  // Enhanced responsive viewport detection
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

  // Enhanced keyboard shortcuts
  useEffect(() => {
    const handleKeyboardShortcuts = (e) => {
      // Ctrl/Cmd + T for new tab
      if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        handleNewTab();
      }
      
      // Ctrl/Cmd + L to focus URL bar
      if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        document.querySelector('input[type="text"]')?.focus();
      }
      
      // Ctrl/Cmd + K for AI assistant
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleAssistant();
      }
      
      // Escape to close mobile menu
      if (e.key === 'Escape' && isMobileMenuOpen) {
        setIsMobileMenuOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyboardShortcuts);
    return () => document.removeEventListener('keydown', handleKeyboardShortcuts);
  }, [toggleAssistant, isMobileMenuOpen]);

  // Update current URL based on active tab
  useEffect(() => {
    const activeTabData = tabs.find(tab => tab.id === activeTab);
    if (activeTabData) {
      const url = activeTabData.url === 'about:blank' ? '' : activeTabData.url;
      setCurrentUrl(url);
      
      // Check if URL is secure
      setIsSecure(!url || url.startsWith('https://') || url.startsWith('http://localhost'));
    }
  }, [activeTab, tabs]);

  // Load search history and bookmarks
  useEffect(() => {
    const savedHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    const savedBookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
    setSearchHistory(savedHistory.slice(0, 5)); // Last 5 searches
    setBookmarks(savedBookmarks.slice(0, 5)); // Top 5 bookmarks
  }, []);

  const handleNavigation = useCallback(async (url) => {
    if (!url.trim()) return;
    
    setIsLoading(true);
    
    try {
      // Enhanced URL validation and formatting
      let formattedUrl = url.trim();
      
      // Check if it's a search query or URL
      if (!formattedUrl.includes('.') || formattedUrl.includes(' ')) {
        // It's a search query
        formattedUrl = `https://www.google.com/search?q=${encodeURIComponent(formattedUrl)}`;
      } else if (!formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
        // Add https by default
        formattedUrl = `https://${formattedUrl}`;
      }

      // Save to search history
      const newHistory = [url, ...searchHistory.filter(h => h !== url)].slice(0, 10);
      setSearchHistory(newHistory);
      localStorage.setItem('searchHistory', JSON.stringify(newHistory));

      // Update current tab or create new one
      if (activeTab) {
        // Update existing tab (enhanced with better title extraction)
        const tabIndex = tabs.findIndex(tab => tab.id === activeTab);
        if (tabIndex !== -1) {
          tabs[tabIndex].url = formattedUrl;
          tabs[tabIndex].title = 'Loading...';
          tabs[tabIndex].isLoading = true;
          
          // Enhanced title extraction simulation
          setTimeout(() => {
            try {
              const domain = new URL(formattedUrl).hostname.replace('www.', '');
              const titleCase = domain.charAt(0).toUpperCase() + domain.slice(1);
              tabs[tabIndex].title = titleCase;
              tabs[tabIndex].isLoading = false;
            } catch {
              tabs[tabIndex].title = 'New Page';
              tabs[tabIndex].isLoading = false;
            }
          }, Math.random() * 1000 + 500); // Realistic loading time
        }
      } else {
        handleNewTab(formattedUrl);
      }

      setCurrentUrl(formattedUrl);
      setShowSearchSuggestions(false);
      
    } catch (error) {
      console.error('Navigation failed:', error);
      // Show user-friendly error
    } finally {
      setTimeout(() => setIsLoading(false), 800);
    }
  }, [activeTab, tabs, searchHistory]);

  const handleNewTab = useCallback((url = 'about:blank') => {
    const newTab = {
      id: `tab-${Date.now()}`,
      url: url,
      title: url === 'about:blank' ? 'New Tab' : 'Loading...',
      position_x: 200 + Math.random() * 200,
      position_y: 150 + Math.random() * 200,
      is_active: true,
      created_at: new Date().toISOString(),
      isLoading: url !== 'about:blank'
    };
    addTab(newTab);
  }, [addTab]);

  const generateEnhancedSearchSuggestions = useCallback(async (query) => {
    if (!query.trim() || query.length < 2) {
      setSearchSuggestions([]);
      return;
    }

    // Combine search history, bookmarks, and smart suggestions
    const suggestions = [];
    
    // Add matching search history
    const historyMatches = searchHistory
      .filter(item => item.toLowerCase().includes(query.toLowerCase()))
      .slice(0, 2);
    suggestions.push(...historyMatches.map(item => ({ type: 'history', text: item, icon: Clock })));
    
    // Add matching bookmarks
    const bookmarkMatches = bookmarks
      .filter(item => item.title?.toLowerCase().includes(query.toLowerCase()) || 
                     item.url?.toLowerCase().includes(query.toLowerCase()))
      .slice(0, 2);
    suggestions.push(...bookmarkMatches.map(item => ({ type: 'bookmark', text: item.title || item.url, icon: Bookmark })));
    
    // Add smart search suggestions
    const smartSuggestions = [
      { type: 'search', text: `${query}`, icon: Search },
      { type: 'search', text: `${query} tutorial`, icon: Search },
      { type: 'search', text: `${query} documentation`, icon: Search },
      { type: 'direct', text: `${query}.com`, icon: Globe }
    ].filter(item => !suggestions.some(s => s.text === item.text)).slice(0, 4);
    
    suggestions.push(...smartSuggestions);
    
    setSearchSuggestions(suggestions.slice(0, 6));
  }, [searchHistory, bookmarks]);

  const handleUrlChange = useCallback((e) => {
    const value = e.target.value;
    setCurrentUrl(value);
    generateEnhancedSearchSuggestions(value);
    setShowSearchSuggestions(value.length > 0);
  }, [generateEnhancedSearchSuggestions]);

  const handleBookmarkToggle = useCallback((url, title) => {
    const isBookmarked = bookmarks.some(b => b.url === url);
    let newBookmarks;
    
    if (isBookmarked) {
      newBookmarks = bookmarks.filter(b => b.url !== url);
    } else {
      newBookmarks = [{ url, title, addedAt: new Date().toISOString() }, ...bookmarks].slice(0, 20);
    }
    
    setBookmarks(newBookmarks);
    localStorage.setItem('bookmarks', JSON.stringify(newBookmarks));
  }, [bookmarks]);

  const getViewportIcon = () => {
    const iconProps = { size: 16, className: `${isOnline ? 'text-green-400' : 'text-red-400'}` };
    switch (viewportSize) {
      case 'mobile': return <Smartphone {...iconProps} />;
      case 'tablet': return <Tablet {...iconProps} />;
      default: return <Monitor {...iconProps} />;
    }
  };

  const shortcuts = [
    { key: '⌘T', action: 'New Tab', handler: handleNewTab },
    { key: '⌘L', action: 'Focus URL', handler: () => document.querySelector('input[type="text"]')?.focus() },
    { key: '⌘K', action: 'AI Assistant', handler: toggleAssistant },
    { key: 'Esc', action: 'Close Menu', handler: () => setIsMobileMenuOpen(false) }
  ];

  const NavigationControls = ({ isMobile = false }) => (
    <div className={`flex items-center ${isMobile ? 'space-x-4 w-full justify-between' : 'space-x-2'}`}>
      {/* Back/Forward/Refresh with enhanced states */}
      <div className="flex items-center space-x-1">
        <button
          className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200 disabled:opacity-30"
          title="Go Back (⌘←)"
          disabled={true} // Would be connected to navigation history
        >
          <ChevronLeft size={16} />
        </button>
        
        <button
          className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200 disabled:opacity-30"
          title="Go Forward (⌘→)"
          disabled={true}
        >
          <ChevronRight size={16} />
        </button>
        
        <motion.button
          className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200"
          title="Refresh (⌘R)"
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
          className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200"
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
            className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-200 ${
              isAssistantVisible 
                ? 'bg-purple-600/30 text-purple-400 animate-pulse' 
                : 'glass hover:bg-purple-600/20 text-purple-400 hover:text-purple-300'
            }`}
            title="AI Assistant (⌘K)"
            onClick={toggleAssistant}
          >
            <Brain size={16} />
          </button>
          
          <button
            className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-200"
            title="New Tab (⌘T)"
            onClick={() => handleNewTab()}
          >
            <Plus size={16} />
          </button>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Enhanced Main Navigation Bar */}
      <motion.div
        className={`fixed top-0 left-0 right-0 z-40 glass-strong border-b border-gray-800/30 ${
          viewportSize === 'mobile' ? 'h-16' : 'h-14'
        }`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.4, type: "spring", stiffness: 120 }}
      >
        <div className="flex items-center h-full px-4 space-x-4">
          {/* Mobile Menu Toggle */}
          {viewportSize === 'mobile' && (
            <motion.button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="w-10 h-10 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
              whileTap={{ scale: 0.95 }}
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </motion.button>
          )}

          {/* Desktop Navigation Controls */}
          {viewportSize !== 'mobile' && <NavigationControls />}

          {/* Enhanced URL/Search Bar */}
          <div className="flex-1 max-w-3xl relative">
            <div className="relative">
              {/* Security/Loading Indicator */}
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1 }}
                  >
                    <RotateCcw size={16} className="text-blue-400" />
                  </motion.div>
                ) : (
                  <>
                    {isSecure ? (
                      <Shield size={14} className="text-green-400" />
                    ) : (
                      <Shield size={14} className="text-red-400" />
                    )}
                    <Search size={16} className="text-gray-400" />
                  </>
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
                onBlur={() => setTimeout(() => setShowSearchSuggestions(false), 150)}
                placeholder="Search or enter URL..."
                className={`w-full ${
                  viewportSize === 'mobile' ? 'h-10 text-sm pl-12' : 'h-9 text-sm pl-12'
                } pr-24 glass border border-gray-700/50 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500/50 focus:bg-gray-800/90 transition-all duration-200`}
              />

              {/* Enhanced Right Side Icons */}
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
                {/* Bookmark Toggle */}
                {currentUrl && (
                  <motion.button
                    onClick={() => handleBookmarkToggle(currentUrl, tabs.find(t => t.id === activeTab)?.title || 'Bookmarked Page')}
                    className={`w-6 h-6 rounded flex items-center justify-center transition-colors ${
                      bookmarks.some(b => b.url === currentUrl)
                        ? 'text-yellow-400 hover:text-yellow-300'
                        : 'text-gray-400 hover:text-yellow-400'
                    }`}
                    whileTap={{ scale: 0.9 }}
                    title="Bookmark this page"
                  >
                    <Star size={12} fill={bookmarks.some(b => b.url === currentUrl) ? 'currentColor' : 'none'} />
                  </motion.button>
                )}
                
                {/* Clear URL */}
                {currentUrl && (
                  <button
                    onClick={() => {
                      setCurrentUrl('');
                      setShowSearchSuggestions(false);
                      document.querySelector('input[type="text"]')?.focus();
                    }}
                    className="w-6 h-6 rounded flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                    title="Clear"
                  >
                    <X size={12} />
                  </button>
                )}
                
                {/* Viewport/Connection Status */}
                <div className="flex items-center space-x-1">
                  {getViewportIcon()}
                  {!isOnline && <WifiOff size={12} className="text-red-400" />}
                </div>
              </div>
            </div>

            {/* Enhanced Search Suggestions Dropdown */}
            <AnimatePresence>
              {showSearchSuggestions && searchSuggestions.length > 0 && (
                <motion.div
                  className="absolute top-full left-0 right-0 mt-2 glass-strong border border-gray-700/50 rounded-xl shadow-2xl z-50"
                  initial={{ opacity: 0, y: -10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="py-2">
                    {searchSuggestions.map((suggestion, index) => (
                      <motion.button
                        key={index}
                        onClick={() => {
                          setCurrentUrl(suggestion.text);
                          handleNavigation(suggestion.text);
                        }}
                        className="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-gray-800/50 hover:text-white first:rounded-t-xl last:rounded-b-xl transition-colors flex items-center group"
                        whileHover={{ x: 4 }}
                      >
                        <suggestion.icon size={14} className="mr-3 text-gray-400 group-hover:text-purple-400" />
                        <div className="flex-1">
                          <span>{suggestion.text}</span>
                          {suggestion.type && (
                            <span className="ml-2 text-xs text-gray-500 capitalize">
                              {suggestion.type}
                            </span>
                          )}
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Desktop Right Actions */}
          {viewportSize !== 'mobile' && (
            <div className="flex items-center space-x-3">
              {/* Enhanced Tab Counter */}
              <div className="flex items-center space-x-2 px-3 py-1 glass rounded-lg border border-gray-700/30">
                <Globe size={14} className="text-gray-400" />
                <span className="text-sm text-gray-300">{tabs.length}</span>
              </div>

              {/* Keyboard Shortcuts */}
              <button
                onClick={() => setShowShortcuts(!showShortcuts)}
                className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                title="Keyboard Shortcuts"
              >
                <Command size={14} />
              </button>

              {/* Enhanced User Menu */}
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center relative">
                  <User size={14} className="text-white" />
                  {isOnline && (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border border-gray-900"></div>
                  )}
                </div>
                <div className="hidden lg:block">
                  <span className="text-sm text-gray-300">{user?.user_mode || 'Guest'}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Keyboard Shortcuts Panel */}
      <AnimatePresence>
        {showShortcuts && viewportSize !== 'mobile' && (
          <motion.div
            className="fixed top-16 right-4 glass-strong border border-gray-700/50 rounded-xl p-4 z-50 w-64"
            initial={{ opacity: 0, scale: 0.9, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: -10 }}
          >
            <h4 className="text-white font-medium mb-3 text-sm">⌨️ Keyboard Shortcuts</h4>
            <div className="space-y-2">
              {shortcuts.map((shortcut, index) => (
                <div key={index} className="flex items-center justify-between text-xs">
                  <span className="text-gray-300">{shortcut.action}</span>
                  <kbd className="bg-gray-800 text-gray-400 px-2 py-1 rounded border border-gray-700">
                    {shortcut.key}
                  </kbd>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Mobile Menu Sidebar */}
      <AnimatePresence>
        {isMobileMenuOpen && viewportSize === 'mobile' && (
          <>
            {/* Backdrop */}
            <motion.div
              className="fixed inset-0 bg-black/60 z-50"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileMenuOpen(false)}
            />

            {/* Enhanced Mobile Menu Panel */}
            <motion.div
              className="fixed left-0 top-0 bottom-0 w-80 glass-strong border-r border-gray-800/50 z-50"
              initial={{ x: -320 }}
              animate={{ x: 0 }}
              exit={{ x: -320 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              <div className="h-full flex flex-col">
                {/* Enhanced Mobile Menu Header */}
                <div className="p-4 border-b border-gray-800/50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center relative">
                        <Brain size={20} className="text-white" />
                        {isOnline && (
                          <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full"></div>
                        )}
                      </div>
                      <div>
                        <h2 className="text-white font-semibold">AI Browser</h2>
                        <p className="text-gray-400 text-sm flex items-center">
                          {user?.user_mode || 'Guest Mode'} 
                          {!isOnline && <WifiOff size={12} className="ml-2 text-red-400" />}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="w-8 h-8 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
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

                {/* Enhanced Quick Actions */}
                <div className="p-4 border-b border-gray-800/50">
                  <h3 className="text-gray-300 font-medium mb-3 text-sm">Quick Actions</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <motion.button
                      onClick={() => {
                        toggleAssistant();
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex flex-col items-center justify-center p-3 glass hover:bg-purple-600/20 text-purple-300 rounded-lg transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Brain size={20} className="mb-1" />
                      <span className="text-xs">AI Assistant</span>
                    </motion.button>
                    
                    <motion.button
                      onClick={() => {
                        handleNewTab();
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex flex-col items-center justify-center p-3 glass hover:bg-blue-600/20 text-blue-300 rounded-lg transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Plus size={20} className="mb-1" />
                      <span className="text-xs">New Tab</span>
                    </motion.button>
                    
                    <motion.button
                      onClick={() => {
                        // Open bookmarks view
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex flex-col items-center justify-center p-3 glass hover:bg-yellow-600/20 text-yellow-300 rounded-lg transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Bookmark size={20} className="mb-1" />
                      <span className="text-xs">Bookmarks</span>
                    </motion.button>
                    
                    <motion.button
                      onClick={() => {
                        // Open settings
                        setIsMobileMenuOpen(false);
                      }}
                      className="flex flex-col items-center justify-center p-3 glass hover:bg-gray-600/20 text-gray-300 rounded-lg transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Settings size={20} className="mb-1" />
                      <span className="text-xs">Settings</span>
                    </motion.button>
                  </div>
                </div>

                {/* Enhanced Tab Management */}
                <div className="flex-1 p-4 overflow-y-auto">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-gray-300 font-medium text-sm">Open Tabs ({tabs.length})</h3>
                    <div className="flex items-center space-x-1">
                      <TrendingUp size={12} className="text-green-400" />
                      <span className="text-xs text-green-400">{tabs.filter(t => !t.isLoading).length} loaded</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
                    <AnimatePresence>
                      {tabs.map((tab) => (
                        <motion.div
                          key={tab.id}
                          className={`flex items-center p-3 rounded-lg cursor-pointer transition-all ${
                            activeTab === tab.id 
                              ? 'glass border border-purple-600/30 bg-purple-600/10' 
                              : 'glass hover:bg-gray-800/50'
                          }`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          onClick={() => {
                            // Set active tab logic would go here
                            setIsMobileMenuOpen(false);
                          }}
                          whileHover={{ x: 4 }}
                        >
                          <div className="w-8 h-8 rounded-lg flex items-center justify-center mr-3 text-sm relative glass-light">
                            {tab.isLoading ? (
                              <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ repeat: Infinity, duration: 1 }}
                              >
                                <RotateCcw size={14} />
                              </motion.div>
                            ) : (
                              tab.title ? tab.title.charAt(0).toUpperCase() : '🌐'
                            )}
                          </div>
                          
                          <div className="flex-1 min-w-0">
                            <h4 className="text-white text-sm font-medium truncate">
                              {tab.title || 'Untitled'}
                            </h4>
                            <p className="text-gray-400 text-xs truncate">
                              {tab.url === 'about:blank' ? 'New Tab' : tab.url}
                            </p>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            {isSecure && tab.url.startsWith('https://') && (
                              <Shield size={10} className="text-green-400" />
                            )}
                            {activeTab === tab.id && (
                              <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" />
                            )}
                          </div>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Enhanced Footer */}
                <div className="p-4 border-t border-gray-800/50">
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <div className="flex items-center space-x-2">
                      <span>Viewport: {viewportSize}</span>
                      {isOnline ? (
                        <Wifi size={10} className="text-green-400" />
                      ) : (
                        <WifiOff size={10} className="text-red-400" />
                      )}
                    </div>
                    <span>Enhanced v2.0</span>
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