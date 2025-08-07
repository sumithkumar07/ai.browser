import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import EnhancedBubbleTab from './EnhancedBubbleTab';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Grid3x3, List, Maximize2, Settings, Search, Filter, Zap } from 'lucide-react';

export default function EnhancedBubbleTabWorkspace() {
  const { tabs, bubblePositions, updateBubblePosition, activeTab, setActiveTab, addTab, closeTab } = useBrowser();
  const { addToAutomationQueue } = useAI();
  const workspaceRef = useRef(null);
  const [workspaceDimensions, setWorkspaceDimensions] = useState({ width: 0, height: 0 });
  const [viewMode, setViewMode] = useState('bubble'); // bubble, grid, list
  const [searchTerm, setSearchTerm] = useState('');
  const [filterBy, setFilterBy] = useState('all'); // all, active, analyzed, recent
  const [isWorkspaceMenuOpen, setIsWorkspaceMenuOpen] = useState(false);
  const [draggedTab, setDraggedTab] = useState(null);
  const [groupedTabs, setGroupedTabs] = useState({});

  useEffect(() => {
    const updateDimensions = () => {
      if (workspaceRef.current) {
        const rect = workspaceRef.current.getBoundingClientRect();
        setWorkspaceDimensions({
          width: rect.width,
          height: rect.height
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  // Auto-organize tabs based on AI analysis
  useEffect(() => {
    const organizeTabsByContent = () => {
      const groups = {
        'Work': [],
        'Shopping': [],
        'Research': [],
        'Entertainment': [],
        'Other': []
      };

      tabs.forEach(tab => {
        const url = tab.url.toLowerCase();
        const title = tab.title.toLowerCase();
        
        if (url.includes('github') || url.includes('stackoverflow') || title.includes('code') || title.includes('dev')) {
          groups['Work'].push(tab);
        } else if (url.includes('shop') || url.includes('amazon') || url.includes('ebay') || title.includes('buy')) {
          groups['Shopping'].push(tab);
        } else if (url.includes('wiki') || url.includes('research') || title.includes('learn') || title.includes('study')) {
          groups['Research'].push(tab);
        } else if (url.includes('youtube') || url.includes('netflix') || url.includes('music') || title.includes('video')) {
          groups['Entertainment'].push(tab);
        } else {
          groups['Other'].push(tab);
        }
      });

      // Remove empty groups
      Object.keys(groups).forEach(key => {
        if (groups[key].length === 0) {
          delete groups[key];
        }
      });

      setGroupedTabs(groups);
    };

    organizeTabsByContent();
  }, [tabs]);

  const handleTabPositionUpdate = useCallback((tabId, x, y) => {
    const boundedX = Math.max(50, Math.min(x, workspaceDimensions.width - 250));
    const boundedY = Math.max(80, Math.min(y, workspaceDimensions.height - 180));
    
    updateBubblePosition(tabId, boundedX, boundedY);
  }, [workspaceDimensions, updateBubblePosition]);

  const handleCreateNewTab = (type = 'blank') => {
    const positions = [
      { x: 200, y: 200 },
      { x: 400, y: 250 },
      { x: 300, y: 350 },
      { x: 500, y: 300 },
      { x: 150, y: 400 }
    ];

    const position = positions[tabs.length % positions.length];
    
    const newTab = {
      id: `tab-${Date.now()}`,
      url: type === 'blank' ? 'about:blank' : 'https://google.com',
      title: type === 'blank' ? 'New Tab' : 'Google Search',
      position_x: position.x + Math.random() * 50,
      position_y: position.y + Math.random() * 50,
      is_active: false,
      created_at: new Date().toISOString(),
      metadata: {
        type: type,
        ai_analyzed: false
      }
    };
    
    addTab(newTab);
  };

  const filteredTabs = tabs.filter(tab => {
    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      if (!tab.title.toLowerCase().includes(searchLower) && 
          !tab.url.toLowerCase().includes(searchLower)) {
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
      default:
        return true;
    }
  });

  const handleBatchAnalyzeAI = async () => {
    const urls = filteredTabs.map(tab => tab.url).filter(url => url !== 'about:blank');
    
    if (urls.length === 0) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/batch-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          urls: urls.slice(0, 5), // Limit to 5 URLs
          analysis_type: 'comprehensive'
        })
      });

      const results = await response.json();
      console.log('Batch analysis results:', results);
      
      // Mark tabs as analyzed
      filteredTabs.forEach(tab => {
        if (tab.url !== 'about:blank') {
          tab.metadata = { ...tab.metadata, ai_analyzed: true };
        }
      });

    } catch (error) {
      console.error('Batch analysis failed:', error);
    }
  };

  const organizeTabsInCircle = () => {
    const centerX = workspaceDimensions.width / 2;
    const centerY = workspaceDimensions.height / 2;
    const radius = Math.min(centerX, centerY) * 0.6;

    tabs.forEach((tab, index) => {
      const angle = (index / tabs.length) * 2 * Math.PI;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      handleTabPositionUpdate(tab.id, x, y);
    });
  };

  const organizeTabsInGrid = () => {
    const cols = Math.ceil(Math.sqrt(tabs.length));
    const startX = 100;
    const startY = 120;
    const spacingX = 280;
    const spacingY = 200;

    tabs.forEach((tab, index) => {
      const col = index % cols;
      const row = Math.floor(index / cols);
      
      const x = startX + col * spacingX;
      const y = startY + row * spacingY;
      
      handleTabPositionUpdate(tab.id, x, y);
    });
  };

  if (viewMode === 'grid') {
    return (
      <div className="enhanced-bubble-workspace grid-view p-6 h-full">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <Grid3x3 className="mr-2" /> Grid View ({filteredTabs.length} tabs)
          </h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setViewMode('bubble')}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
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
                className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-4 hover:bg-gray-700/50 transition-all cursor-pointer"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => setActiveTab(tab.id)}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    {tab.title.charAt(0).toUpperCase()}
                  </div>
                  {tab.metadata?.ai_analyzed && (
                    <span className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded-full">
                      AI Analyzed
                    </span>
                  )}
                </div>
                
                <h3 className="text-white font-medium mb-2 line-clamp-2">{tab.title || 'Untitled'}</h3>
                <p className="text-gray-400 text-sm truncate">{tab.url}</p>
                
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {new Date(tab.created_at || Date.now()).toLocaleTimeString()}
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
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    );
  }

  if (viewMode === 'list') {
    return (
      <div className="enhanced-bubble-workspace list-view p-6 h-full">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <List className="mr-2" /> List View ({filteredTabs.length} tabs)
          </h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setViewMode('bubble')}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              Bubble View
            </button>
          </div>
        </div>

        <div className="space-y-3">
          <AnimatePresence>
            {Object.entries(groupedTabs).map(([group, groupTabs]) => (
              <div key={group} className="mb-6">
                <h3 className="text-lg font-semibold text-gray-300 mb-3 flex items-center">
                  {group} <span className="ml-2 text-sm text-gray-500">({groupTabs.length})</span>
                </h3>
                
                {groupTabs.filter(tab => filteredTabs.includes(tab)).map((tab, index) => (
                  <motion.div
                    key={tab.id}
                    className={`flex items-center p-4 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg hover:bg-gray-700/50 transition-all cursor-pointer ${
                      activeTab === tab.id ? 'ring-2 ring-purple-500' : ''
                    }`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold mr-4">
                      {tab.title.charAt(0).toUpperCase()}
                    </div>
                    
                    <div className="flex-1">
                      <h4 className="text-white font-medium">{tab.title || 'Untitled'}</h4>
                      <p className="text-gray-400 text-sm truncate">{tab.url}</p>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      {tab.metadata?.ai_analyzed && (
                        <span className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded-full">
                          AI
                        </span>
                      )}
                      
                      <span className="text-xs text-gray-500">
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

  return (
    <div 
      ref={workspaceRef}
      className="enhanced-bubble-workspace absolute inset-0 top-16 overflow-hidden bg-gradient-to-br from-gray-900 via-purple-900/10 to-blue-900/10"
    >
      {/* Enhanced Workspace Controls */}
      <div className="absolute top-4 left-4 right-4 z-10 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Search tabs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 bg-gray-800/80 backdrop-blur-sm border border-gray-700/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 transition-colors w-64"
            />
          </div>

          {/* Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <select
              value={filterBy}
              onChange={(e) => setFilterBy(e.target.value)}
              className="pl-10 pr-8 py-2 bg-gray-800/80 backdrop-blur-sm border border-gray-700/50 rounded-lg text-white focus:outline-none focus:border-purple-500 transition-colors appearance-none"
            >
              <option value="all">All Tabs</option>
              <option value="active">Active Tab</option>
              <option value="analyzed">AI Analyzed</option>
              <option value="recent">Recent</option>
            </select>
          </div>

          <span className="text-gray-400 text-sm">
            {filteredTabs.length} of {tabs.length} tabs
          </span>
        </div>

        <div className="flex items-center space-x-2">
          {/* AI Batch Analysis */}
          {filteredTabs.length > 0 && (
            <button
              onClick={handleBatchAnalyzeAI}
              className="flex items-center px-3 py-2 bg-purple-600/80 hover:bg-purple-600 text-white rounded-lg transition-colors text-sm backdrop-blur-sm"
            >
              <Zap size={14} className="mr-1" />
              AI Analyze All
            </button>
          )}

          {/* View Mode Toggle */}
          <div className="flex items-center bg-gray-800/80 backdrop-blur-sm rounded-lg p-1 border border-gray-700/50">
            {[
              { mode: 'bubble', icon: Plus, label: 'Bubble' },
              { mode: 'grid', icon: Grid3x3, label: 'Grid' },
              { mode: 'list', icon: List, label: 'List' }
            ].map(({ mode, icon: Icon, label }) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                className={`flex items-center px-3 py-1.5 rounded text-sm transition-colors ${
                  viewMode === mode
                    ? 'bg-purple-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
                }`}
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
              className="flex items-center px-3 py-2 bg-gray-800/80 hover:bg-gray-700/80 text-white rounded-lg transition-colors text-sm backdrop-blur-sm border border-gray-700/50"
            >
              <Settings size={14} className="mr-1" />
              Organize
            </button>

            {isWorkspaceMenuOpen && (
              <motion.div
                className="absolute right-0 top-12 bg-gray-800/95 backdrop-blur-xl border border-gray-700/50 rounded-lg shadow-xl p-2 min-w-48 z-20"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <button
                  onClick={() => {
                    organizeTabsInCircle();
                    setIsWorkspaceMenuOpen(false);
                  }}
                  className="w-full text-left px-3 py-2 text-white hover:bg-gray-700/50 rounded text-sm transition-colors"
                >
                  🔄 Arrange in Circle
                </button>
                <button
                  onClick={() => {
                    organizeTabsInGrid();
                    setIsWorkspaceMenuOpen(false);
                  }}
                  className="w-full text-left px-3 py-2 text-white hover:bg-gray-700/50 rounded text-sm transition-colors"
                >
                  📐 Grid Layout
                </button>
                <button
                  onClick={() => {
                    // Random positions
                    tabs.forEach(tab => {
                      const x = Math.random() * (workspaceDimensions.width - 300) + 150;
                      const y = Math.random() * (workspaceDimensions.height - 200) + 100;
                      handleTabPositionUpdate(tab.id, x, y);
                    });
                    setIsWorkspaceMenuOpen(false);
                  }}
                  className="w-full text-left px-3 py-2 text-white hover:bg-gray-700/50 rounded text-sm transition-colors"
                >
                  🎲 Random Scatter
                </button>
              </motion.div>
            )}
          </div>
        </div>
      </div>

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
          />
        ))}
      </AnimatePresence>

      {/* Empty State */}
      {tabs.length === 0 && (
        <motion.div 
          className="flex items-center justify-center h-full"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-center max-w-md mx-auto px-6">
            <div className="text-8xl mb-6">🌌</div>
            <h2 className="text-3xl font-bold text-white mb-4">
              Welcome to Your AI Workspace
            </h2>
            <p className="text-gray-400 text-lg mb-8">
              Create your first floating tab and experience the future of browsing
            </p>
            
            <div className="space-y-3">
              <button
                onClick={() => handleCreateNewTab('blank')}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-4 px-8 rounded-xl font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
              >
                ✨ Create Your First Tab
              </button>
              
              <button
                onClick={() => handleCreateNewTab('search')}
                className="w-full bg-gray-800/50 hover:bg-gray-700/50 text-white py-3 px-6 rounded-xl font-medium transition-colors border border-gray-700/50"
              >
                🔍 Start with Search
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Floating Add Button */}
      {tabs.length > 0 && (
        <motion.button
          onClick={() => handleCreateNewTab()}
          className="fixed bottom-24 right-24 w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-full shadow-2xl text-white text-2xl z-20 transition-all transform hover:scale-110"
          whileHover={{ scale: 1.1, rotate: 90 }}
          whileTap={{ scale: 0.9 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
        >
          <Plus size={24} />
        </motion.button>
      )}

      {/* Connection Lines (Optional Visual Enhancement) */}
      {tabs.length > 1 && viewMode === 'bubble' && (
        <svg className="absolute inset-0 pointer-events-none" style={{ zIndex: 0 }}>
          {tabs.map((tab, index) => {
            if (index === 0) return null;
            
            const currentPos = bubblePositions[tab.id] || { x: tab.position_x || 200, y: tab.position_y || 150 };
            const prevTab = tabs[index - 1];
            const prevPos = bubblePositions[prevTab.id] || { x: prevTab.position_x || 200, y: prevTab.position_y || 150 };
            
            return (
              <motion.line
                key={`line-${tab.id}`}
                x1={prevPos.x + 100}
                y1={prevPos.y + 75}
                x2={currentPos.x + 100}
                y2={currentPos.y + 75}
                stroke="rgba(147, 51, 234, 0.1)"
                strokeWidth="1"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              />
            );
          })}
        </svg>
      )}
    </div>
  );
}