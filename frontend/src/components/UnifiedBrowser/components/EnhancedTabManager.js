import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  X, Plus, MoreHorizontal, Globe, Lock, Volume2, VolumeX,
  Pin, PinOff, Archive, RotateCcw, Search, Layers, ChevronDown,
  Clock, Star, Bookmark, Download
} from 'lucide-react';

export default function EnhancedTabManager({ 
  tabs, 
  activeTabId, 
  onSwitchTab, 
  onCloseTab, 
  onCreateTab,
  tabGroups,
  showGroups,
  recentlyClosedTabs,
  onReopenTab
}) {
  const [draggedTab, setDraggedTab] = useState(null);
  const [dropTarget, setDropTarget] = useState(null);
  const [showTabMenu, setShowTabMenu] = useState(null);
  const [showNewTabMenu, setShowNewTabMenu] = useState(false);
  const [showRecentTabs, setShowRecentTabs] = useState(false);
  const [tabSearch, setTabSearch] = useState('');
  const [showTabSearch, setShowTabSearch] = useState(false);

  const tabBarRef = useRef(null);
  const searchInputRef = useRef(null);

  // Filter tabs based on search
  const filteredTabs = tabs.filter(tab => 
    tab.title.toLowerCase().includes(tabSearch.toLowerCase()) ||
    tab.url.toLowerCase().includes(tabSearch.toLowerCase())
  );

  const handleTabDragStart = (e, tabId) => {
    setDraggedTab(tabId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleTabDragOver = (e, targetTabId) => {
    e.preventDefault();
    if (draggedTab && draggedTab !== targetTabId) {
      setDropTarget(targetTabId);
    }
  };

  const handleTabDrop = (e, targetTabId) => {
    e.preventDefault();
    if (draggedTab && draggedTab !== targetTabId) {
      // Reorder tabs logic would go here
      console.log('Reorder tabs:', draggedTab, 'to', targetTabId);
    }
    setDraggedTab(null);
    setDropTarget(null);
  };

  const toggleTabPin = (tabId) => {
    // Pin/unpin tab logic
    console.log('Toggle pin for tab:', tabId);
  };

  const duplicateTab = (tab) => {
    onCreateTab(tab.url, `Copy of ${tab.title}`, true);
  };

  const muteTab = (tabId) => {
    // Mute/unmute tab logic
    console.log('Toggle mute for tab:', tabId);
  };

  const getTotalTabsWidth = () => {
    const minTabWidth = 180;
    const maxTabWidth = 240;
    const availableWidth = tabBarRef.current?.offsetWidth - 200; // Reserve space for controls
    const idealWidth = availableWidth / tabs.length;
    
    return Math.max(minTabWidth, Math.min(maxTabWidth, idealWidth));
  };

  const getTabDisplayTitle = (tab) => {
    if (tab.title.length > 20) {
      return tab.title.substring(0, 20) + '...';
    }
    return tab.title;
  };

  const getFaviconUrl = (url) => {
    try {
      const domain = new URL(url).hostname;
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=16`;
    } catch {
      return null;
    }
  };

  const getTabSecurityIcon = (url) => {
    if (url.startsWith('https://')) return <Lock size={12} className="text-green-400" />;
    if (url.startsWith('http://')) return <Globe size={12} className="text-yellow-400" />;
    return null;
  };

  useEffect(() => {
    if (showTabSearch && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [showTabSearch]);

  return (
    <div className="tab-bar bg-gray-800/60 border-b border-gray-700/40 relative" ref={tabBarRef}>
      
      {/* Tab Search */}
      <AnimatePresence>
        {showTabSearch && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-b border-gray-700/30 px-4 py-2"
          >
            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                ref={searchInputRef}
                type="text"
                value={tabSearch}
                onChange={(e) => setTabSearch(e.target.value)}
                placeholder="Search tabs..."
                className="w-full pl-9 pr-4 py-2 bg-gray-700/50 border border-gray-600/50 rounded text-white placeholder-gray-400 text-sm focus:outline-none focus:border-blue-500/50"
                onKeyDown={(e) => {
                  if (e.key === 'Escape') {
                    setShowTabSearch(false);
                    setTabSearch('');
                  }
                }}
              />
              <button
                onClick={() => {
                  setShowTabSearch(false);
                  setTabSearch('');
                }}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-600 rounded text-gray-400 hover:text-white"
              >
                <X size={12} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Tab Bar */}
      <div className="flex items-center min-h-[40px]">
        
        {/* Tab List */}
        <div className="flex-1 flex items-center overflow-x-auto scrollbar-thin scrollbar-track-transparent scrollbar-thumb-gray-600">
          {(showTabSearch ? filteredTabs : tabs).map((tab) => {
            const isActive = tab.id === activeTabId;
            const isDragging = draggedTab === tab.id;
            const isDropTarget = dropTarget === tab.id;
            
            return (
              <motion.div
                key={tab.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: isDragging ? 0.5 : 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9, width: 0 }}
                className={`tab-item relative flex items-center min-w-[120px] max-w-[240px] h-[36px] mx-0.5 rounded-t-lg cursor-pointer transition-all duration-200 group ${
                  isActive 
                    ? 'bg-gray-700 text-white border-t-2 border-blue-500 z-10' 
                    : 'bg-gray-800/40 text-gray-300 hover:bg-gray-700/60 border-t-2 border-transparent'
                } ${
                  isDropTarget ? 'ring-2 ring-blue-500/50' : ''
                } ${
                  tab.isPinned ? 'min-w-[40px] max-w-[40px]' : ''
                }`}
                style={{ width: tab.isPinned ? '40px' : `${getTotalTabsWidth()}px` }}
                draggable
                onDragStart={(e) => handleTabDragStart(e, tab.id)}
                onDragOver={(e) => handleTabDragOver(e, tab.id)}
                onDrop={(e) => handleTabDrop(e, tab.id)}
                onClick={() => onSwitchTab(tab.id)}
                onContextMenu={(e) => {
                  e.preventDefault();
                  setShowTabMenu(showTabMenu === tab.id ? null : tab.id);
                }}
              >
                {/* Tab Content */}
                <div className="flex items-center space-x-2 px-3 py-2 flex-1 min-w-0">
                  
                  {/* Favicon & Security */}
                  <div className="flex items-center space-x-1 flex-shrink-0">
                    {tab.isPinned && <Pin size={8} className="text-blue-400" />}
                    
                    {getFaviconUrl(tab.url) ? (
                      <img 
                        src={getFaviconUrl(tab.url)} 
                        alt="" 
                        className="w-4 h-4" 
                        onError={(e) => e.target.style.display = 'none'}
                      />
                    ) : (
                      <Globe size={12} className="text-gray-400" />
                    )}
                    
                    {getTabSecurityIcon(tab.url)}
                  </div>

                  {/* Tab Title */}
                  {!tab.isPinned && (
                    <div className="flex-1 min-w-0">
                      <div className="text-sm truncate" title={tab.title}>
                        {tab.isLoading ? (
                          <div className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                            <span>Loading...</span>
                          </div>
                        ) : (
                          getTabDisplayTitle(tab)
                        )}
                      </div>
                    </div>
                  )}

                  {/* Tab Indicators */}
                  <div className="flex items-center space-x-1 flex-shrink-0">
                    {tab.hasAudio && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          muteTab(tab.id);
                        }}
                        className="p-0.5 hover:bg-gray-600 rounded"
                        title={tab.isMuted ? 'Unmute tab' : 'Mute tab'}
                      >
                        {tab.isMuted ? 
                          <VolumeX size={12} className="text-red-400" /> : 
                          <Volume2 size={12} className="text-blue-400" />
                        }
                      </button>
                    )}
                  </div>
                </div>

                {/* Close Button */}
                {!tab.isPinned && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onCloseTab(tab.id);
                    }}
                    className="p-1 hover:bg-gray-600 rounded text-gray-400 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity mr-1"
                    title="Close tab"
                  >
                    <X size={12} />
                  </button>
                )}

                {/* Context Menu */}
                <AnimatePresence>
                  {showTabMenu === tab.id && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9, y: -10 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.9, y: -10 }}
                      className="absolute top-full left-0 mt-1 bg-gray-800/95 backdrop-blur-sm border border-gray-600/50 rounded-lg shadow-xl z-50 min-w-[180px]"
                      onMouseLeave={() => setShowTabMenu(null)}
                    >
                      <div className="py-1">
                        <button
                          onClick={() => duplicateTab(tab)}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                        >
                          <Plus size={14} />
                          <span>Duplicate Tab</span>
                        </button>
                        
                        <button
                          onClick={() => toggleTabPin(tab.id)}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                        >
                          {tab.isPinned ? <PinOff size={14} /> : <Pin size={14} />}
                          <span>{tab.isPinned ? 'Unpin Tab' : 'Pin Tab'}</span>
                        </button>
                        
                        <button
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                        >
                          <Bookmark size={14} />
                          <span>Bookmark Tab</span>
                        </button>
                        
                        <div className="border-t border-gray-700/50 my-1"></div>
                        
                        <button
                          onClick={() => onCloseTab(tab.id)}
                          className="w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-red-500/10 flex items-center space-x-2"
                        >
                          <X size={14} />
                          <span>Close Tab</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>

        {/* Tab Controls */}
        <div className="flex items-center space-x-1 px-2 border-l border-gray-700/30">
          
          {/* New Tab Button */}
          <div className="relative">
            <button
              onClick={() => setShowNewTabMenu(!showNewTabMenu)}
              className="p-2 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors"
              title="New tab options"
            >
              <ChevronDown size={14} />
            </button>
            
            <AnimatePresence>
              {showNewTabMenu && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9, y: -10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: -10 }}
                  className="absolute top-full right-0 mt-1 bg-gray-800/95 backdrop-blur-sm border border-gray-600/50 rounded-lg shadow-xl z-50 min-w-[200px]"
                  onMouseLeave={() => setShowNewTabMenu(false)}
                >
                  <div className="py-1">
                    <button
                      onClick={() => {
                        onCreateTab();
                        setShowNewTabMenu(false);
                      }}
                      className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                    >
                      <Plus size={14} />
                      <span>New Tab</span>
                    </button>
                    
                    <button
                      onClick={() => {
                        onCreateTab('', 'Private Tab', true);
                        setShowNewTabMenu(false);
                      }}
                      className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                    >
                      <Lock size={14} />
                      <span>New Private Tab</span>
                    </button>
                    
                    <div className="border-t border-gray-700/50 my-1"></div>
                    
                    <button
                      onClick={() => {
                        setShowTabSearch(!showTabSearch);
                        setShowNewTabMenu(false);
                      }}
                      className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                    >
                      <Search size={14} />
                      <span>Search Tabs</span>
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
          
          <button
            onClick={onCreateTab}
            className="p-2 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors"
            title="New tab (Ctrl+T)"
          >
            <Plus size={14} />
          </button>

          {/* Recently Closed Tabs */}
          {recentlyClosedTabs.length > 0 && (
            <div className="relative">
              <button
                onClick={() => setShowRecentTabs(!showRecentTabs)}
                className="p-2 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors"
                title="Recently closed tabs"
              >
                <RotateCcw size={14} />
              </button>
              
              <AnimatePresence>
                {showRecentTabs && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: -10 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: -10 }}
                    className="absolute top-full right-0 mt-1 bg-gray-800/95 backdrop-blur-sm border border-gray-600/50 rounded-lg shadow-xl z-50 min-w-[250px] max-h-64 overflow-y-auto"
                    onMouseLeave={() => setShowRecentTabs(false)}
                  >
                    <div className="py-1">
                      <div className="px-3 py-2 text-xs text-gray-400 border-b border-gray-700/50">
                        Recently Closed
                      </div>
                      {recentlyClosedTabs.map((tab, index) => (
                        <button
                          key={index}
                          onClick={() => {
                            onReopenTab(tab);
                            setShowRecentTabs(false);
                          }}
                          className="w-full px-3 py-2 text-left text-sm text-gray-300 hover:bg-gray-700/50 flex items-center space-x-2"
                        >
                          <img 
                            src={getFaviconUrl(tab.url)} 
                            alt="" 
                            className="w-4 h-4" 
                            onError={(e) => e.target.style.display = 'none'}
                          />
                          <div className="flex-1 min-w-0">
                            <div className="truncate">{tab.title}</div>
                            <div className="text-xs text-gray-500 truncate">{tab.url}</div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}

          {/* Tab Groups Toggle */}
          <button
            onClick={() => {/* Toggle tab groups */}}
            className="p-2 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors"
            title="Tab groups"
          >
            <Layers size={14} />
          </button>
        </div>
      </div>

      {/* Tab Groups Bar */}
      {showGroups && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="border-t border-gray-700/30 px-4 py-2"
        >
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-gray-400">Groups:</span>
            {/* Tab groups would be rendered here */}
            <div className="px-2 py-1 bg-blue-600/20 text-blue-300 rounded">
              Work (3)
            </div>
            <div className="px-2 py-1 bg-green-600/20 text-green-300 rounded">
              Research (2)
            </div>
            <button className="px-2 py-1 bg-gray-700/50 text-gray-400 rounded hover:bg-gray-600/50">
              + New Group
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}