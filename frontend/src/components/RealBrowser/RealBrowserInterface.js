import React, { useState, useEffect, useRef } from 'react';
import { Globe, Plus, X, ArrowLeft, ArrowRight, RotateCcw, Search, Home, Bookmark } from 'lucide-react';
import realBrowserService from '../../services/RealBrowserService';

const RealBrowserInterface = ({ isVisible, onClose }) => {
  const [tabs, setTabs] = useState([]);
  const [activeTabId, setActiveTabId] = useState(null);
  const [urlInput, setUrlInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [browserHealth, setBrowserHealth] = useState(null);
  const urlInputRef = useRef(null);

  // Initialize browser when component mounts
  useEffect(() => {
    if (isVisible) {
      initializeBrowser();
      checkBrowserHealth();
    }
    
    return () => {
      // Cleanup when component unmounts
      if (tabs.length > 0) {
        realBrowserService.cleanup();
      }
    };
  }, [isVisible]);

  const initializeBrowser = async () => {
    try {
      // Create a new session if needed
      if (!realBrowserService.getCurrentSession()) {
        await realBrowserService.createSession();
      }
      
      // Create initial tab
      await createNewTab();
    } catch (error) {
      console.error('Failed to initialize browser:', error);
    }
  };

  const checkBrowserHealth = async () => {
    try {
      const health = await realBrowserService.getBrowserHealth();
      setBrowserHealth(health);
    } catch (error) {
      console.error('Failed to check browser health:', error);
    }
  };

  const createNewTab = async (url = 'about:blank') => {
    try {
      setIsLoading(true);
      const result = await realBrowserService.createNewTab(url);
      
      if (result.success) {
        const newTab = {
          id: result.tab_id,
          url: result.url,
          title: result.title || 'New Tab',
          isLoading: false,
          favicon: null
        };
        
        setTabs(prev => [...prev, newTab]);
        setActiveTabId(result.tab_id);
        setUrlInput(result.url === 'about:blank' ? '' : result.url);
      }
    } catch (error) {
      console.error('Failed to create new tab:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const closeTab = async (tabId) => {
    try {
      await realBrowserService.closeTab(tabId);
      
      setTabs(prev => {
        const newTabs = prev.filter(tab => tab.id !== tabId);
        if (activeTabId === tabId && newTabs.length > 0) {
          setActiveTabId(newTabs[newTabs.length - 1].id);
        } else if (newTabs.length === 0) {
          setActiveTabId(null);
        }
        return newTabs;
      });
    } catch (error) {
      console.error('Failed to close tab:', error);
    }
  };

  const navigateToUrl = async (url, tabId = null) => {
    if (!url.trim()) return;
    
    try {
      setIsLoading(true);
      const processedUrl = realBrowserService.processUrl(url);
      const targetTabId = tabId || activeTabId;
      
      const result = await realBrowserService.navigateToUrl(processedUrl, targetTabId);
      
      if (result.success) {
        // Update tab info
        setTabs(prev => prev.map(tab => 
          tab.id === result.tab_id 
            ? { ...tab, url: result.url, title: result.title, isLoading: false }
            : tab
        ));
        
        setUrlInput(result.url);
      }
    } catch (error) {
      console.error('Failed to navigate:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    if (urlInput.trim()) {
      navigateToUrl(urlInput);
    }
  };

  const goBack = async () => {
    if (!activeTabId) return;
    
    try {
      const result = await realBrowserService.goBack(activeTabId);
      if (result.success) {
        setTabs(prev => prev.map(tab => 
          tab.id === activeTabId 
            ? { ...tab, url: result.url, title: result.title }
            : tab
        ));
        setUrlInput(result.url);
      }
    } catch (error) {
      console.error('Failed to go back:', error);
    }
  };

  const goForward = async () => {
    if (!activeTabId) return;
    
    try {
      const result = await realBrowserService.goForward(activeTabId);
      if (result.success) {
        setTabs(prev => prev.map(tab => 
          tab.id === activeTabId 
            ? { ...tab, url: result.url, title: result.title }
            : tab
        ));
        setUrlInput(result.url);
      }
    } catch (error) {
      console.error('Failed to go forward:', error);
    }
  };

  const reload = async () => {
    if (!activeTabId) return;
    
    try {
      setIsLoading(true);
      const result = await realBrowserService.reload(activeTabId);
      if (result.success) {
        setTabs(prev => prev.map(tab => 
          tab.id === activeTabId 
            ? { ...tab, url: result.url, title: result.title }
            : tab
        ));
        setUrlInput(result.url);
      }
    } catch (error) {
      console.error('Failed to reload:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const switchTab = (tabId) => {
    setActiveTabId(tabId);
    const tab = tabs.find(t => t.id === tabId);
    if (tab) {
      setUrlInput(tab.url === 'about:blank' ? '' : tab.url);
    }
  };

  const quickNavigate = (site) => {
    realBrowserService.openPopularSite(site);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-slate-900 bg-opacity-95 backdrop-blur-sm z-50">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-700">
          <div className="flex items-center space-x-3">
            <Globe className="w-6 h-6 text-blue-400" />
            <h2 className="text-xl font-semibold text-white">Real Browser Engine</h2>
            {browserHealth && (
              <span className={`px-2 py-1 rounded text-xs ${
                browserHealth.status === 'healthy' 
                  ? 'bg-green-500/20 text-green-400' 
                  : 'bg-yellow-500/20 text-yellow-400'
              }`}>
                {browserHealth.status}
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-700 rounded-lg text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center bg-slate-800 border-b border-slate-700">
          <div className="flex-1 flex items-center overflow-x-auto">
            {tabs.map(tab => (
              <div
                key={tab.id}
                className={`flex items-center min-w-0 max-w-xs cursor-pointer border-r border-slate-700 ${
                  activeTabId === tab.id 
                    ? 'bg-slate-700' 
                    : 'hover:bg-slate-700/50'
                }`}
                onClick={() => switchTab(tab.id)}
              >
                <div className="flex items-center space-x-2 px-4 py-3 min-w-0 flex-1">
                  <Globe className="w-4 h-4 text-gray-400 flex-shrink-0" />
                  <span className="text-sm text-white truncate">
                    {tab.title || 'Loading...'}
                  </span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    closeTab(tab.id);
                  }}
                  className="p-2 hover:bg-red-500/20 text-gray-400 hover:text-red-400"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
          
          <button
            onClick={() => createNewTab()}
            className="p-3 hover:bg-slate-700 text-gray-400 hover:text-white flex-shrink-0"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation Bar */}
        <div className="flex items-center space-x-2 p-3 bg-slate-800 border-b border-slate-700">
          <button
            onClick={goBack}
            disabled={!activeTabId}
            className="p-2 hover:bg-slate-700 rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-400 hover:text-white"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          
          <button
            onClick={goForward}
            disabled={!activeTabId}
            className="p-2 hover:bg-slate-700 rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-400 hover:text-white"
          >
            <ArrowRight className="w-4 h-4" />
          </button>
          
          <button
            onClick={reload}
            disabled={!activeTabId || isLoading}
            className="p-2 hover:bg-slate-700 rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-400 hover:text-white"
          >
            <RotateCcw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
          
          <form onSubmit={handleUrlSubmit} className="flex-1 flex items-center">
            <div className="relative flex-1 max-w-2xl">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                ref={urlInputRef}
                type="text"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="Enter URL or search term..."
                className="w-full pl-10 pr-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
              />
            </div>
          </form>
        </div>

        {/* Quick Access Bar */}
        <div className="flex items-center space-x-2 p-2 bg-slate-800/50 border-b border-slate-700">
          <button
            onClick={() => createNewTab('https://www.google.com')}
            className="px-3 py-1 text-sm bg-slate-700 hover:bg-slate-600 text-white rounded flex items-center space-x-1"
          >
            <Home className="w-3 h-3" />
            <span>Home</span>
          </button>
          
          {['Google', 'YouTube', 'GitHub', 'Reddit'].map(site => (
            <button
              key={site}
              onClick={() => navigateToUrl(`https://www.${site.toLowerCase()}.com`)}
              className="px-3 py-1 text-sm bg-slate-700/50 hover:bg-slate-700 text-gray-300 hover:text-white rounded"
            >
              {site}
            </button>
          ))}
          
          <div className="flex-1" />
          
          <button
            onClick={() => {/* Add bookmark functionality */}}
            className="p-1 hover:bg-slate-700 rounded text-gray-400 hover:text-white"
          >
            <Bookmark className="w-4 h-4" />
          </button>
        </div>

        {/* Browser View Area */}
        <div className="flex-1 bg-white">
          {activeTabId ? (
            <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
              <div className="text-center">
                <Globe className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-slate-700 mb-2">
                  Real Chromium Browser Active
                </h3>
                <p className="text-slate-600 mb-4">
                  A separate browser window has been opened for real browsing.
                </p>
                <p className="text-sm text-slate-500">
                  URL: {tabs.find(t => t.id === activeTabId)?.url || 'Loading...'}
                </p>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
              <div className="text-center">
                <Globe className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-slate-700 mb-2">
                  No Active Tab
                </h3>
                <p className="text-slate-600 mb-4">
                  Create a new tab to start browsing the web.
                </p>
                <button
                  onClick={() => createNewTab()}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
                >
                  Create New Tab
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Status Bar */}
        {activeTabId && (
          <div className="p-2 bg-slate-800 border-t border-slate-700 text-xs text-gray-400">
            <div className="flex items-center justify-between">
              <span>
                Active Tab: {tabs.find(t => t.id === activeTabId)?.title || 'Loading...'}
              </span>
              <span>
                {tabs.length} tab{tabs.length !== 1 ? 's' : ''} open
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RealBrowserInterface;