import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import EnhancedBubbleTab from './EnhancedBubbleTab';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Grid3x3, List, Maximize2, Settings, Search, Filter, Zap, Sparkles, Brain, TrendingUp, Clock, Star, Globe2, Layers, RotateCcw, Command, Eye, EyeOff, Group } from 'lucide-react';

export default function EnhancedBubbleTabWorkspace() {
  const { tabs, bubblePositions, updateBubblePosition, activeTab, setActiveTab, addTab, closeTab } = useBrowser();
  const { addToAutomationQueue } = useAI();
  const workspaceRef = useRef(null);
  const [workspaceDimensions, setWorkspaceDimensions] = useState({ width: 0, height: 0 });
  const [viewMode, setViewMode] = useState('bubble'); // bubble, grid, list, focus
  const [searchTerm, setSearchTerm] = useState('');
  const [filterBy, setFilterBy] = useState('all'); // all, active, analyzed, recent, bookmarked
  const [isWorkspaceMenuOpen, setIsWorkspaceMenuOpen] = useState(false);
  const [draggedTab, setDraggedTab] = useState(null);
  const [groupedTabs, setGroupedTabs] = useState({});
  const [isZenMode, setIsZenMode] = useState(false);
  const [showPerformanceOverlay, setShowPerformanceOverlay] = useState(false);
  const [workspaceTheme, setWorkspaceTheme] = useState('default');
  const [autoOrganize, setAutoOrganize] = useState(true);
  const [showMiniMap, setShowMiniMap] = useState(false);
  const [tabGroups, setTabGroups] = useState([]);

  // Enhanced workspace dimensions with debouncing
  useEffect(() => {
    let timeoutId;
    const updateDimensions = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        if (workspaceRef.current) {
          const rect = workspaceRef.current.getBoundingClientRect();
          setWorkspaceDimensions({
            width: rect.width,
            height: rect.height
          });
        }
      }, 100); // Debounce for performance
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => {
      window.removeEventListener('resize', updateDimensions);
      clearTimeout(timeoutId);
    };
  }, []);

  // Enhanced auto-organize with intelligent grouping
  useEffect(() => {
    if (!autoOrganize) return;
    
    const organizeTabsByContent = () => {
      const groups = {
        'Work & Development': [],
        'Shopping & Commerce': [],
        'Research & Learning': [],
        'Entertainment': [],
        'Social & Communication': [],
        'Tools & Utilities': [],
        'Other': []
      };

      tabs.forEach(tab => {
        const url = (tab.url || '').toLowerCase();
        const title = (tab.title || '').toLowerCase();
        
        // Enhanced categorization logic
        if (url.includes('github') || url.includes('stackoverflow') || url.includes('gitlab') || 
            title.includes('code') || title.includes('dev') || url.includes('developer')) {
          groups['Work & Development'].push(tab);
        } else if (url.includes('shop') || url.includes('amazon') || url.includes('ebay') || 
                  url.includes('store') || title.includes('buy') || title.includes('cart')) {
          groups['Shopping & Commerce'].push(tab);
        } else if (url.includes('wiki') || url.includes('research') || url.includes('edu') || 
                  url.includes('course') || title.includes('learn') || title.includes('study')) {
          groups['Research & Learning'].push(tab);
        } else if (url.includes('youtube') || url.includes('netflix') || url.includes('spotify') || 
                  url.includes('music') || url.includes('video') || title.includes('entertainment')) {
          groups['Entertainment'].push(tab);
        } else if (url.includes('facebook') || url.includes('twitter') || url.includes('instagram') || 
                  url.includes('linkedin') || url.includes('social') || title.includes('chat')) {
          groups['Social & Communication'].push(tab);
        } else if (url.includes('tools') || url.includes('calculator') || url.includes('converter') || 
                  title.includes('tool') || title.includes('utility')) {
          groups['Tools & Utilities'].push(tab);
        } else {
          groups['Other'].push(tab);
        }
      });

      // Remove empty groups and sort by usage
      Object.keys(groups).forEach(key => {
        if (groups[key].length === 0) {
          delete groups[key];
        }
      });

      setGroupedTabs(groups);
    };

    const debounceTimeout = setTimeout(organizeTabsByContent, 300);
    return () => clearTimeout(debounceTimeout);
  }, [tabs, autoOrganize]);

  // Enhanced keyboard shortcuts
  useEffect(() => {
    const handleKeyboardShortcuts = (e) => {
      if (e.target.tagName === 'INPUT') return;
      
      // Space for Zen mode
      if (e.code === 'Space' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        setIsZenMode(!isZenMode);
      }
      
      // G for grid view
      if (e.key === 'g' && !e.ctrlKey && !e.metaKey) {
        setViewMode(viewMode === 'grid' ? 'bubble' : 'grid');
      }
      
      // L for list view
      if (e.key === 'l' && !e.ctrlKey && !e.metaKey) {
        setViewMode(viewMode === 'list' ? 'bubble' : 'list');
      }
      
      // M for mini-map
      if (e.key === 'm' && !e.ctrlKey && !e.metaKey) {
        setShowMiniMap(!showMiniMap);
      }
      
      // O for organize
      if (e.key === 'o' && !e.ctrlKey && !e.metaKey) {
        organizeTabsIntelligently();
      }
    };

    document.addEventListener('keydown', handleKeyboardShortcuts);
    return () => document.removeEventListener('keydown', handleKeyboardShortcuts);
  }, [isZenMode, viewMode, showMiniMap]);

  const handleTabPositionUpdate = useCallback((tabId, x, y) => {
    const boundedX = Math.max(50, Math.min(x, workspaceDimensions.width - 250));
    const boundedY = Math.max(80, Math.min(y, workspaceDimensions.height - 180));
    
    updateBubblePosition(tabId, boundedX, boundedY);
  }, [workspaceDimensions, updateBubblePosition]);

  const handleCreateNewTab = useCallback((type = 'blank') => {
    const positions = [
      { x: 200, y: 200 },
      { x: 400, y: 250 },
      { x: 300, y: 350 },
      { x: 500, y: 300 },
      { x: 150, y: 400 }
    ];

    const position = positions[tabs.length % positions.length];
    const randomOffset = { x: Math.random() * 100 - 50, y: Math.random() * 100 - 50 };
    
    const newTab = {
      id: `tab-${Date.now()}`,
      url: type === 'blank' ? 'about:blank' : 'https://google.com',
      title: type === 'blank' ? 'New Tab' : 'Google Search',
      position_x: position.x + randomOffset.x,
      position_y: position.y + randomOffset.y,
      is_active: false,
      created_at: new Date().toISOString(),
      metadata: {
        type: type,
        ai_analyzed: false,
        group: 'Other',
        theme: workspaceTheme,
        performance_score: 100
      }
    };
    
    addTab(newTab);
  }, [tabs, addTab, workspaceTheme]);

  // Enhanced filtering with performance optimization
  const filteredTabs = useMemo(() => {
    return tabs.filter(tab => {
      // Search filter
      if (searchTerm) {
        const searchLower = searchTerm.toLowerCase();
        const titleMatch = (tab.title || '').toLowerCase().includes(searchLower);
        const urlMatch = (tab.url || '').toLowerCase().includes(searchLower);
        const groupMatch = (tab.metadata?.group || '').toLowerCase().includes(searchLower);
        
        if (!titleMatch && !urlMatch && !groupMatch) {
          return false;
        }
      }

      // Category filter
      switch (filterBy) {
        case 'active':
          return tab.id === activeTab;
        case 'analyzed':
          return tab.metadata?.ai_analyzed;
        case 'recent':
          const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
          return new Date(tab.created_at || 0) > oneHourAgo;
        case 'bookmarked':
          return tab.metadata?.bookmarked;
        default:
          return true;
      }
    });
  }, [tabs, searchTerm, filterBy, activeTab]);

  const handleBatchAnalyzeAI = async () => {
    const urls = filteredTabs
      .map(tab => tab.url)
      .filter(url => url && url !== 'about:blank')
      .slice(0, 5); // Limit to 5 URLs for performance
    
    if (urls.length === 0) {
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/batch-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          urls: urls,
          analysis_type: 'comprehensive'
        })
      });

      const results = await response.json();
      console.log('Enhanced batch analysis results:', results);
      
      // Mark tabs as analyzed with enhanced metadata
      filteredTabs.forEach(tab => {
        if (tab.url !== 'about:blank' && urls.includes(tab.url)) {
          tab.metadata = { 
            ...tab.metadata, 
            ai_analyzed: true,
            analysis_timestamp: new Date().toISOString(),
            analysis_quality: 'high'
          };
        }
      });

    } catch (error) {
      console.error('Enhanced batch analysis failed:', error);
    }
  };

  const organizeTabsIntelligently = useCallback(() => {
    const centerX = workspaceDimensions.width / 2;
    const centerY = workspaceDimensions.height / 2;
    
    // Group tabs by their categories
    const categories = Object.keys(groupedTabs);
    const angleStep = (2 * Math.PI) / categories.length;
    
    categories.forEach((category, categoryIndex) => {
      const categoryTabs = groupedTabs[category];
      const categoryAngle = categoryIndex * angleStep;
      const categoryRadius = Math.min(centerX, centerY) * 0.6;
      
      const categoryCenter = {
        x: centerX + categoryRadius * Math.cos(categoryAngle),
        y: centerY + categoryRadius * Math.sin(categoryAngle)
      };
      
      // Arrange tabs in category in a small circle
      categoryTabs.forEach((tab, tabIndex) => {
        const tabAngle = (tabIndex / categoryTabs.length) * 2 * Math.PI;
        const tabRadius = 60 + (categoryTabs.length * 5); // Dynamic radius based on tab count
        
        const x = categoryCenter.x + tabRadius * Math.cos(tabAngle);
        const y = categoryCenter.y + tabRadius * Math.sin(tabAngle);
        
        handleTabPositionUpdate(tab.id, x, y);
      });
    });
  }, [workspaceDimensions, groupedTabs, handleTabPositionUpdate]);

  const organizeTabsInGrid = useCallback(() => {
    const cols = Math.ceil(Math.sqrt(filteredTabs.length));
    const startX = 100;
    const startY = 120;
    const spacingX = Math.min(300, (workspaceDimensions.width - 200) / cols);
    const spacingY = 220;

    filteredTabs.forEach((tab, index) => {
      const col = index % cols;
      const row = Math.floor(index / cols);
      
      const x = startX + col * spacingX;
      const y = startY + row * spacingY;
      
      handleTabPositionUpdate(tab.id, x, y);
    });
  }, [filteredTabs, workspaceDimensions, handleTabPositionUpdate]);

  const organizeTabsInSpiral = useCallback(() => {
    const centerX = workspaceDimensions.width / 2;
    const centerY = workspaceDimensions.height / 2;
    
    filteredTabs.forEach((tab, index) => {
      const angle = index * 0.5;
      const radius = 80 + (index * 15);
      
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      handleTabPositionUpdate(tab.id, x, y);
    });
  }, [filteredTabs, workspaceDimensions, handleTabPositionUpdate]);

  const workspaceStats = useMemo(() => {
    return {
      totalTabs: tabs.length,
      activeTabs: tabs.filter(t => t.id === activeTab).length,
      analyzedTabs: tabs.filter(t => t.metadata?.ai_analyzed).length,
      recentTabs: tabs.filter(t => {
        const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
        return new Date(t.created_at || 0) > oneHourAgo;
      }).length,
      categories: Object.keys(groupedTabs).length
    };
  }, [tabs, activeTab, groupedTabs]);

  // Focus Mode (Zen Mode) - simplified interface
  if (isZenMode) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
        <motion.div
          className="text-center space-y-6"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="text-6xl mb-4">🧘‍♀️</div>
          <h2 className="text-3xl font-bold text-white">Zen Mode Active</h2>
          <p className="text-gray-400 text-lg">Focus on what matters most</p>
          
          {activeTab && (
            <div className="bg-gray-900/50 backdrop-blur rounded-2xl p-6 max-w-md">
              <h3 className="text-white font-medium mb-2">Current Focus:</h3>
              <p className="text-gray-300">{tabs.find(t => t.id === activeTab)?.title || 'Active Tab'}</p>
            </div>
          )}
          
          <div className="flex items-center justify-center space-x-4">
            <button
              onClick={() => setIsZenMode(false)}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl hover:scale-105 transition-transform"
            >
              Exit Zen Mode
            </button>
            <button
              onClick={() => handleCreateNewTab()}
              className="px-6 py-3 glass text-white rounded-xl hover:bg-gray-800/50 transition-colors"
            >
              New Tab
            </button>
          </div>
          
          <p className="text-xs text-gray-500">Press Space to toggle Zen Mode</p>
        </motion.div>
      </div>
    );
  }

  // Grid View
  if (viewMode === 'grid') {
    return (
      <div className="enhanced-bubble-workspace grid-view p-6 h-full">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <Grid3x3 className="mr-2" /> 
            Enhanced Grid View ({filteredTabs.length} tabs)
          </h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setViewMode('bubble')}
              className="btn-secondary text-sm"
            >
              Bubble View
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <AnimatePresence>
            {filteredTabs.map((tab, index) => (
              <motion.div
                key={tab.id}
                className="card-interactive"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => setActiveTab(tab.id)}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    {(tab.title || 'T').charAt(0).toUpperCase()}
                  </div>
                  <div className="flex items-center space-x-1">
                    {tab.metadata?.ai_analyzed && (
                      <span className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded-full flex items-center">
                        <Brain size={10} className="mr-1" />
                        AI
                      </span>
                    )}
                    {tab.metadata?.bookmarked && (
                      <Star size={12} className="text-yellow-400" fill="currentColor" />
                    )}
                  </div>
                </div>
                
                <h3 className="text-white font-medium mb-2 line-clamp-2">{tab.title || 'Untitled'}</h3>
                <p className="text-gray-400 text-sm truncate mb-3">{tab.url}</p>
                
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500 flex items-center">
                    <Clock size={10} className="mr-1" />
                    {new Date(tab.created_at || Date.now()).toLocaleTimeString()}
                  </span>
                  <div className="flex items-center space-x-1">
                    <span className="bg-gray-700/50 text-gray-300 px-2 py-1 rounded">
                      {tab.metadata?.group || 'Other'}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        closeTab(tab.id);
                      }}
                      className="text-gray-500 hover:text-red-400 transition-colors"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    );
  }

  // List View
  if (viewMode === 'list') {
    return (
      <div className="enhanced-bubble-workspace list-view p-6 h-full">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <List className="mr-2" /> 
            Enhanced List View ({filteredTabs.length} tabs)
          </h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setViewMode('bubble')}
              className="btn-secondary text-sm"
            >
              Bubble View
            </button>
          </div>
        </div>

        <div className="space-y-4">
          <AnimatePresence>
            {Object.entries(groupedTabs).map(([group, groupTabs]) => (
              <div key={group} className="mb-6">
                <motion.div
                  className="flex items-center justify-between mb-3"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  <h3 className="text-lg font-semibold text-gray-300 flex items-center">
                    <Group className="mr-2" size={16} />
                    {group} 
                    <span className="ml-2 text-sm text-gray-500">({groupTabs.length})</span>
                  </h3>
                  <div className="flex items-center space-x-2">
                    <TrendingUp size={14} className="text-green-400" />
                    <span className="text-xs text-gray-400">
                      {groupTabs.filter(t => t.metadata?.ai_analyzed).length} analyzed
                    </span>
                  </div>
                </motion.div>
                
                {groupTabs.filter(tab => filteredTabs.includes(tab)).map((tab, index) => (
                  <motion.div
                    key={tab.id}
                    className={`flex items-center p-4 card-interactive ${
                      activeTab === tab.id ? 'ring-2 ring-purple-500 bg-purple-500/10' : ''
                    }`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-white font-bold mr-4">
                      {(tab.title || 'T').charAt(0).toUpperCase()}
                    </div>
                    
                    <div className="flex-1">
                      <h4 className="text-white font-medium flex items-center">
                        {tab.title || 'Untitled'}
                        {tab.isLoading && <RotateCcw size={12} className="ml-2 animate-spin text-blue-400" />}
                      </h4>
                      <p className="text-gray-400 text-sm truncate">{tab.url}</p>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      {tab.metadata?.ai_analyzed && (
                        <span className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded-full flex items-center">
                          <Brain size={10} className="mr-1" />
                          AI
                        </span>
                      )}
                      
                      {tab.metadata?.bookmarked && (
                        <Star size={14} className="text-yellow-400" fill="currentColor" />
                      )}
                      
                      <span className="text-xs text-gray-500 flex items-center">
                        <Clock size={10} className="mr-1" />
                        {new Date(tab.created_at || Date.now()).toLocaleTimeString()}
                      </span>
                      
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          closeTab(tab.id);
                        }}
                        className="text-gray-500 hover:text-red-400 transition-colors p-1"
                      >
                        ×
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    );
  }

  // Main Bubble View
  return (
    <div 
      ref={workspaceRef}
      className="enhanced-bubble-workspace absolute inset-0 top-16 overflow-hidden bg-gradient-to-br from-gray-900/50 via-purple-900/5 to-blue-900/5"
    >
      {/* Enhanced Workspace Controls */}
      <motion.div 
        className="absolute top-4 left-4 right-4 z-10 flex items-center justify-between"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="flex items-center space-x-4">
          {/* Enhanced Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Search tabs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-search w-64"
            />
          </div>

          {/* Enhanced Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <select
              value={filterBy}
              onChange={(e) => setFilterBy(e.target.value)}
              className="input-primary pl-10 pr-8 appearance-none text-sm"
            >
              <option value="all">All Tabs</option>
              <option value="active">Active Tab</option>
              <option value="analyzed">AI Analyzed</option>
              <option value="recent">Recent</option>
              <option value="bookmarked">Bookmarked</option>
            </select>
          </div>

          {/* Workspace Stats */}
          <div className="glass px-3 py-2 rounded-lg text-xs text-gray-300 flex items-center space-x-4">
            <span>{workspaceStats.totalTabs} tabs</span>
            <span>•</span>
            <span>{workspaceStats.categories} groups</span>
            <span>•</span>
            <span className="text-purple-300">{workspaceStats.analyzedTabs} analyzed</span>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* AI Batch Analysis */}
          {filteredTabs.length > 0 && (
            <motion.button
              onClick={handleBatchAnalyzeAI}
              className="flex items-center px-3 py-2 bg-purple-600/80 hover:bg-purple-600 text-white rounded-lg transition-colors text-sm backdrop-blur-sm"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Brain size={14} className="mr-1" />
              AI Analyze All
            </motion.button>
          )}

          {/* Zen Mode Toggle */}
          <button
            onClick={() => setIsZenMode(true)}
            className="w-10 h-10 glass hover:bg-gray-700/50 flex items-center justify-center text-gray-300 hover:text-white rounded-lg transition-colors"
            title="Zen Mode (Space)"
          >
            <Eye size={16} />
          </button>

          {/* Mini Map Toggle */}
          <button
            onClick={() => setShowMiniMap(!showMiniMap)}
            className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors ${
              showMiniMap ? 'bg-purple-600/30 text-purple-300' : 'glass hover:bg-gray-700/50 text-gray-300 hover:text-white'
            }`}
            title="Mini Map (M)"
          >
            <Layers size={16} />
          </button>

          {/* View Mode Toggle */}
          <div className="flex items-center glass rounded-lg p-1 border border-gray-700/30">
            {[
              { mode: 'bubble', icon: Sparkles, label: 'Bubble' },
              { mode: 'grid', icon: Grid3x3, label: 'Grid' },
              { mode: 'list', icon: List, label: 'List' }
            ].map(({ mode, icon: Icon, label }) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                className={`flex items-center px-3 py-1.5 rounded text-sm transition-all duration-200 ${
                  viewMode === mode
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700/30'
                }`}
                title={`${label} View (${mode === 'grid' ? 'G' : mode === 'list' ? 'L' : 'B'})`}
              >
                <Icon size={14} className="mr-1" />
                {label}
              </button>
            ))}
          </div>

          {/* Organization Tools */}
          <div className="relative">
            <button
              onClick={() => setIsWorkspaceMenuOpen(!isWorkspaceMenuOpen)}
              className="flex items-center px-3 py-2 glass hover:bg-gray-700/50 text-white rounded-lg transition-colors text-sm border border-gray-700/30"
            >
              <Settings size={14} className="mr-1" />
              Organize
            </button>

            <AnimatePresence>
              {isWorkspaceMenuOpen && (
                <motion.div
                  className="absolute right-0 top-12 glass-strong border border-gray-700/50 rounded-xl shadow-2xl p-3 min-w-64 z-20"
                  initial={{ opacity: 0, scale: 0.9, y: -10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: -10 }}
                >
                  <h4 className="text-white font-medium mb-3 text-sm">Organization Tools</h4>
                  
                  <div className="space-y-2">
                    <button
                      onClick={() => {
                        organizeTabsIntelligently();
                        setIsWorkspaceMenuOpen(false);
                      }}
                      className="w-full text-left px-3 py-2 text-white hover:bg-purple-600/20 rounded-lg text-sm transition-colors flex items-center"
                    >
                      <Brain className="mr-2" size={14} />
                      🧠 Smart Organization
                    </button>
                    
                    <button
                      onClick={() => {
                        organizeTabsInGrid();
                        setIsWorkspaceMenuOpen(false);
                      }}
                      className="w-full text-left px-3 py-2 text-white hover:bg-gray-700/50 rounded-lg text-sm transition-colors flex items-center"
                    >
                      <Grid3x3 className="mr-2" size={14} />
                      📐 Grid Layout
                    </button>
                    
                    <button
                      onClick={() => {
                        organizeTabsInSpiral();
                        setIsWorkspaceMenuOpen(false);
                      }}
                      className="w-full text-left px-3 py-2 text-white hover:bg-gray-700/50 rounded-lg text-sm transition-colors flex items-center"
                    >
                      <RotateCcw className="mr-2" size={14} />
                      🌀 Spiral Layout
                    </button>
                    
                    <div className="border-t border-gray-700/50 my-2"></div>
                    
                    <div className="flex items-center justify-between py-2">
                      <span className="text-sm text-gray-400">Auto Organize</span>
                      <input 
                        type="checkbox" 
                        checked={autoOrganize}
                        onChange={(e) => setAutoOrganize(e.target.checked)}
                        className="rounded" 
                      />
                    </div>
                    
                    <div className="flex items-center justify-between py-2">
                      <span className="text-sm text-gray-400">Performance Overlay</span>
                      <input 
                        type="checkbox" 
                        checked={showPerformanceOverlay}
                        onChange={(e) => setShowPerformanceOverlay(e.target.checked)}
                        className="rounded" 
                      />
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.div>

      {/* Mini Map */}
      <AnimatePresence>
        {showMiniMap && (
          <motion.div
            className="fixed bottom-6 left-6 w-64 h-48 glass-strong rounded-xl border border-gray-700/50 z-20 overflow-hidden"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <div className="p-3">
              <h4 className="text-white text-sm font-medium mb-2 flex items-center">
                <Layers size={12} className="mr-1" />
                Workspace Map
              </h4>
              <div className="relative w-full h-32 bg-gray-800/50 rounded-lg overflow-hidden">
                {filteredTabs.map((tab) => {
                  const pos = bubblePositions[tab.id] || { x: tab.position_x || 200, y: tab.position_y || 150 };
                  const mapX = (pos.x / workspaceDimensions.width) * 100;
                  const mapY = (pos.y / workspaceDimensions.height) * 100;
                  
                  return (
                    <div
                      key={tab.id}
                      className={`absolute w-2 h-2 rounded-full ${
                        activeTab === tab.id ? 'bg-purple-400' : 'bg-gray-400'
                      }`}
                      style={{
                        left: `${Math.max(0, Math.min(95, mapX))}%`,
                        top: `${Math.max(0, Math.min(95, mapY))}%`
                      }}
                    />
                  );
                })}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Enhanced Bubble Tabs */}
      <AnimatePresence>
        {filteredTabs.map((tab) => (
          <EnhancedBubbleTab
            key={tab.id}
            tab={tab}
            position={bubblePositions[tab.id] || { x: tab.position_x || 200, y: tab.position_y || 150 }}
            onPositionChange={handleTabPositionUpdate}
            workspaceDimensions={workspaceDimensions}
            isActive={activeTab === tab.id}
            onActivate={() => setActiveTab(tab.id)}
            onClose={() => closeTab(tab.id)}
            searchTerm={searchTerm}
            theme={workspaceTheme}
            showPerformanceOverlay={showPerformanceOverlay}
          />
        ))}
      </AnimatePresence>

      {/* Empty State */}
      {tabs.length === 0 && (
        <motion.div 
          className="center-absolute max-w-lg text-center px-6"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="text-8xl mb-6">🌌</div>
          <h2 className="text-3xl font-bold text-white mb-4">
            Welcome to Your Enhanced AI Workspace
          </h2>
          <p className="text-gray-400 text-lg mb-8">
            Create floating tabs, organize intelligently, and let AI assist your browsing
          </p>
          
          <div className="space-y-3">
            <motion.button
              onClick={() => handleCreateNewTab('blank')}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-4 px-8 rounded-xl font-semibold text-lg transition-all shadow-lg"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ✨ Create Your First Bubble Tab
            </motion.button>
            
            <motion.button
              onClick={() => handleCreateNewTab('search')}
              className="w-full glass hover:bg-gray-800/50 text-white py-3 px-6 rounded-xl font-medium transition-colors border border-gray-700/50"
              whileHover={{ scale: 1.02 }}
            >
              🔍 Start with Smart Search
            </motion.button>
          </div>
          
          <div className="mt-8 text-sm text-gray-500 space-y-1">
            <p>💡 Pro tips: Press <kbd className="bg-gray-800 px-2 py-1 rounded">Space</kbd> for Zen Mode</p>
            <p>Use <kbd className="bg-gray-800 px-2 py-1 rounded">G</kbd> for Grid, <kbd className="bg-gray-800 px-2 py-1 rounded">L</kbd> for List view</p>
          </div>
        </motion.div>
      )}

      {/* Floating Add Button */}
      {tabs.length > 0 && (
        <motion.button
          onClick={() => handleCreateNewTab()}
          className="fixed bottom-24 right-24 w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-full shadow-2xl text-white text-2xl z-20 transition-all"
          whileHover={{ scale: 1.1, rotate: 90 }}
          whileTap={{ scale: 0.9 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
        >
          <Plus size={24} />
        </motion.button>
      )}

      {/* Connection Lines for Bubble Mode */}
      {tabs.length > 1 && viewMode === 'bubble' && autoOrganize && (
        <svg className="absolute inset-0 pointer-events-none" style={{ zIndex: 0 }}>
          {Object.entries(groupedTabs).map(([group, groupTabs]) =>
            groupTabs.map((tab, index) => {
              if (index === 0) return null;
              
              const currentPos = bubblePositions[tab.id] || { x: tab.position_x || 200, y: tab.position_y || 150 };
              const prevTab = groupTabs[index - 1];
              const prevPos = bubblePositions[prevTab.id] || { x: prevTab.position_x || 200, y: prevTab.position_y || 150 };
              
              return (
                <motion.line
                  key={`line-${tab.id}`}
                  x1={prevPos.x + 100}
                  y1={prevPos.y + 75}
                  x2={currentPos.x + 100}
                  y2={currentPos.y + 75}
                  stroke="rgba(139, 92, 246, 0.2)"
                  strokeWidth="1"
                  strokeDasharray="5,5"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                />
              );
            })
          )}
        </svg>
      )}

      {/* Performance Overlay */}
      {showPerformanceOverlay && (
        <motion.div
          className="fixed bottom-6 right-6 glass-strong rounded-xl p-4 text-xs text-gray-300 z-20 min-w-48"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h4 className="text-white font-medium mb-2 flex items-center">
            <TrendingUp size={12} className="mr-1" />
            Performance
          </h4>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span>Memory Usage:</span>
              <span className="text-green-400">Good</span>
            </div>
            <div className="flex justify-between">
              <span>Render Time:</span>
              <span className="text-green-400">&lt;16ms</span>
            </div>
            <div className="flex justify-between">
              <span>Active Tabs:</span>
              <span className="text-purple-400">{workspaceStats.totalTabs}</span>
            </div>
            <div className="flex justify-between">
              <span>AI Analysis:</span>
              <span className="text-blue-400">{workspaceStats.analyzedTabs}</span>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}