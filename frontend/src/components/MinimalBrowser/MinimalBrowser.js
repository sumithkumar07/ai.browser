import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, ArrowRight, RotateCcw, Settings, Plus, 
  Search, Globe, Brain, Zap, Sparkles, Mic
} from 'lucide-react';

// Minimal components
import MinimalHeader from './components/MinimalHeader';
import MinimalTabStrip from './components/MinimalTabStrip';
import SmartUrlBar from './components/SmartUrlBar';
import FloatingAI from './components/FloatingAI';
import ContextualMenu from './components/ContextualMenu';
import VoiceCommandOverlay from './components/VoiceCommandOverlay';

// Services
import MinimalBrowserService from '../../services/MinimalBrowserService';

export default function MinimalBrowser() {
  // Minimal state - only essentials visible
  const [tabs, setTabs] = useState([]);
  const [activeTabId, setActiveTabId] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Intelligent features (invisible to user)
  const [aiContext, setAiContext] = useState(null);
  const [smartSuggestions, setSmartSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  
  // Minimal UI state
  const [showAI, setShowAI] = useState(false);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [showVoiceCommands, setShowVoiceCommands] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });
  
  const urlBarRef = useRef(null);

  useEffect(() => {
    initializeMinimalBrowser();
  }, []);

  const initializeMinimalBrowser = async () => {
    try {
      console.log('🚀 Initializing Minimal AI Browser...');
      
      // Create welcome tab
      await createNewTab('about:welcome');
      
      // Initialize background intelligence
      await MinimalBrowserService.initializeIntelligentFeatures();
      
      console.log('✅ Minimal Browser Ready with Invisible Intelligence');
      
    } catch (error) {
      console.error('Minimal browser initialization failed:', error);
      createLocalTab('Welcome', 'about:welcome');
    }
  };

  const createNewTab = async (url = 'about:blank') => {
    try {
      setIsLoading(true);
      
      const result = await MinimalBrowserService.createTab(url);
      
      if (result.success) {
        const newTab = {
          id: result.tab_id,
          url: result.url,
          title: result.title || getPageTitle(result.url),
          isLoading: false,
          favicon: result.favicon
        };
        
        setTabs(prev => [...prev, newTab]);
        setActiveTabId(newTab.id);
        setCurrentUrl(newTab.url);
        
        // Background: Analyze context and activate intelligent features
        await analyzeTabContext(newTab.id, newTab.url);
      }
    } catch (error) {
      console.error('Tab creation failed:', error);
      createLocalTab('New Tab', url);
    } finally {
      setIsLoading(false);
    }
  };

  const createLocalTab = (title, url) => {
    const newTab = {
      id: `local-${Date.now()}`,
      title,
      url,
      isLoading: false,
      isLocal: true
    };
    
    setTabs(prev => [...prev, newTab]);
    setActiveTabId(newTab.id);
    setCurrentUrl(url);
  };

  const navigateToUrl = async (url) => {
    if (!url.trim() || !activeTabId) return;
    
    try {
      setIsLoading(true);
      const processedUrl = MinimalBrowserService.processUrl(url);
      
      // Update UI immediately
      updateTabUrl(activeTabId, processedUrl);
      
      // Navigate in background
      const result = await MinimalBrowserService.navigate(activeTabId, processedUrl);
      
      if (result.success) {
        updateTabFromResult(activeTabId, result);
        setCurrentUrl(result.url);
        
        // Background: Intelligent content analysis
        await analyzeTabContext(activeTabId, result.url, result.content);
      }
    } catch (error) {
      console.error('Navigation failed:', error);
      updateTabTitle(activeTabId, 'Failed to load');
    } finally {
      setIsLoading(false);
      setShowSuggestions(false);
    }
  };

  const analyzeTabContext = async (tabId, url, content = null) => {
    try {
      // Background intelligence - invisible to user
      const context = await MinimalBrowserService.analyzeContext(tabId, url, content);
      setAiContext(context);
      
      // Auto-activate features based on context
      await MinimalBrowserService.activateContextualFeatures(context);
      
    } catch (error) {
      console.error('Context analysis failed:', error);
    }
  };

  const handleUrlInput = async (query) => {
    if (query.length > 1) {
      setShowSuggestions(true);
      
      // Get smart suggestions from backend intelligence
      const suggestions = await MinimalBrowserService.getSmartSuggestions(query, aiContext);
      setSmartSuggestions(suggestions);
    } else {
      setShowSuggestions(false);
      setSmartSuggestions([]);
    }
  };

  const handleSuggestionSelect = async (suggestion) => {
    switch (suggestion.type) {
      case 'navigate':
        await navigateToUrl(suggestion.action_data.url);
        break;
      case 'search':
        await navigateToUrl(`https://www.google.com/search?q=${encodeURIComponent(suggestion.action_data.query)}`);
        break;
      case 'ai_analyze':
        setShowAI(true);
        break;
      case 'smart_bookmark':
        await MinimalBrowserService.activateFeature('smart_bookmark', aiContext);
        break;
      default:
        console.log('Unknown suggestion type:', suggestion.type);
    }
    setShowSuggestions(false);
  };

  const switchTab = (tabId) => {
    const tab = tabs.find(t => t.id === tabId);
    if (!tab) return;
    
    setActiveTabId(tabId);
    setCurrentUrl(tab.url);
    
    // Background: Update context for new tab
    analyzeTabContext(tabId, tab.url);
  };

  const closeTab = async (tabId) => {
    try {
      await MinimalBrowserService.closeTab(tabId);
      
      setTabs(prev => {
        const remaining = prev.filter(tab => tab.id !== tabId);
        
        if (tabId === activeTabId) {
          if (remaining.length > 0) {
            const nextTab = remaining[remaining.length - 1];
            setActiveTabId(nextTab.id);
            setCurrentUrl(nextTab.url);
          } else {
            createNewTab();
            return remaining;
          }
        }
        
        return remaining;
      });
    } catch (error) {
      console.error('Tab close failed:', error);
    }
  };

  const handleContextMenu = (event) => {
    event.preventDefault();
    setContextMenuPosition({ x: event.clientX, y: event.clientY });
    setShowContextMenu(true);
  };

  const handleVoiceCommand = async (command) => {
    try {
      const result = await MinimalBrowserService.processVoiceCommand(command, aiContext);
      
      if (result.action === 'navigate') {
        await navigateToUrl(result.url);
      } else if (result.action === 'analyze') {
        setShowAI(true);
      } else if (result.action === 'organize') {
        // Background feature activation - invisible to user
        await MinimalBrowserService.activateFeature('tab_organization', aiContext);
      }
    } catch (error) {
      console.error('Voice command failed:', error);
    }
  };

  // Helper functions
  const updateTabUrl = (tabId, url) => {
    setTabs(prev => prev.map(tab => 
      tab.id === tabId ? { ...tab, url, isLoading: true } : tab
    ));
  };

  const updateTabFromResult = (tabId, result) => {
    setTabs(prev => prev.map(tab => 
      tab.id === tabId 
        ? { ...tab, url: result.url, title: result.title, isLoading: false, favicon: result.favicon }
        : tab
    ));
  };

  const updateTabTitle = (tabId, title) => {
    setTabs(prev => prev.map(tab => 
      tab.id === tabId ? { ...tab, title, isLoading: false } : tab
    ));
  };

  const getPageTitle = (url) => {
    if (url === 'about:blank') return 'New Tab';
    if (url === 'about:welcome') return 'Welcome';
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch {
      return 'Loading...';
    }
  };

  const activeTab = tabs.find(tab => tab.id === activeTabId);

  return (
    <div className="minimal-browser h-screen w-screen flex flex-col bg-white" onContextMenu={handleContextMenu}>
      
      {/* Minimal Header - Fellou.ai Style */}
      <MinimalHeader>
        {/* Essential Navigation Controls */}
        <div className="flex items-center space-x-2">
          <button 
            className="minimal-nav-btn"
            onClick={() => MinimalBrowserService.goBack(activeTabId)}
            disabled={!activeTab || isLoading}
            title="Back"
          >
            <ArrowLeft size={16} />
          </button>
          <button 
            className="minimal-nav-btn"
            onClick={() => MinimalBrowserService.goForward(activeTabId)}
            disabled={!activeTab || isLoading}
            title="Forward"
          >
            <ArrowRight size={16} />
          </button>
          <button 
            className="minimal-nav-btn"
            onClick={() => navigateToUrl(currentUrl)}
            disabled={!activeTab || isLoading}
            title="Refresh"
          >
            <RotateCcw size={16} className={isLoading ? 'animate-spin' : ''} />
          </button>
        </div>

        {/* Smart URL Bar - Core Function */}
        <SmartUrlBar 
          ref={urlBarRef}
          value={currentUrl}
          onInput={handleUrlInput}
          onSubmit={navigateToUrl}
          suggestions={smartSuggestions}
          showSuggestions={showSuggestions}
          onSuggestionSelect={handleSuggestionSelect}
          isLoading={isLoading}
          placeholder="Search or enter URL..."
        />

        {/* Essential Actions */}
        <div className="flex items-center space-x-2">
          {/* Voice Command Trigger */}
          <button 
            className="minimal-nav-btn"
            onClick={() => setShowVoiceCommands(true)}
            title="Voice Commands (Hey Browser)"
          >
            <Mic size={16} />
          </button>
          
          {/* Settings Menu */}
          <button 
            className="minimal-nav-btn"
            title="Settings"
          >
            <Settings size={16} />
          </button>
        </div>
      </MinimalHeader>

      {/* Minimal Tab Strip */}
      <MinimalTabStrip 
        tabs={tabs}
        activeTabId={activeTabId}
        onSwitchTab={switchTab}
        onCloseTab={closeTab}
        onNewTab={() => createNewTab()}
      />

      {/* Main Content Area - Full Screen */}
      <div className="flex-1 relative bg-gray-50">
        {activeTab ? (
          activeTab.url === 'about:welcome' ? (
            <WelcomeScreen onNavigate={navigateToUrl} onNewTab={() => createNewTab()} />
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center space-y-4">
                <Globe size={48} className="mx-auto text-gray-400" />
                <div className="text-gray-600">
                  <p className="text-lg font-medium">Clean Browsing Experience</p>
                  <p className="text-sm">All advanced features work invisibly in the background</p>
                  <p className="text-xs text-gray-400 mt-2">Current: {currentUrl}</p>
                </div>
              </div>
            </div>
          )
        ) : (
          <div className="h-full flex items-center justify-center">
            <button
              onClick={() => createNewTab()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              Create New Tab
            </button>
          </div>
        )}
      </div>

      {/* Floating AI Assistant - Context-Aware */}
      <FloatingAI 
        isVisible={showAI}
        onToggle={setShowAI}
        context={aiContext}
        currentUrl={currentUrl}
        onFeatureActivate={(feature) => MinimalBrowserService.activateFeature(feature, aiContext)}
      />

      {/* Contextual Right-Click Menu */}
      <ContextualMenu 
        isVisible={showContextMenu}
        position={contextMenuPosition}
        context={aiContext}
        onClose={() => setShowContextMenu(false)}
        onFeatureSelect={(feature) => MinimalBrowserService.activateFeature(feature, aiContext)}
      />

      {/* Voice Commands Overlay */}
      <VoiceCommandOverlay 
        isVisible={showVoiceCommands}
        onClose={() => setShowVoiceCommands(false)}
        onCommand={handleVoiceCommand}
      />
    </div>
  );
}

// Welcome Screen Component
function WelcomeScreen({ onNavigate, onNewTab }) {
  const quickActions = [
    { name: 'Google', url: 'https://google.com', icon: Search },
    { name: 'GitHub', url: 'https://github.com', icon: Globe },
    { name: 'New Tab', action: onNewTab, icon: Plus }
  ];

  return (
    <div className="h-full flex items-center justify-center">
      <div className="text-center max-w-2xl mx-auto p-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          <div>
            <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <Brain size={32} className="text-white" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Minimal AI Browser
            </h1>
            <p className="text-gray-600 text-lg">
              Clean interface, intelligent features working invisibly
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 max-w-md mx-auto">
            {quickActions.map((action, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => action.url ? onNavigate(action.url) : action.action()}
                className="p-6 bg-white rounded-xl border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all"
              >
                <action.icon size={24} className="mx-auto mb-3 text-gray-600" />
                <div className="text-sm text-gray-700 font-medium">{action.name}</div>
              </motion.button>
            ))}
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-500 mb-4">
              17 intelligent features active in background
            </p>
            <div className="flex justify-center space-x-2">
              <Sparkles size={16} className="text-green-500" />
              <span className="text-xs text-gray-400">
                AI Analysis • Smart Bookmarking • Performance Optimization
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}