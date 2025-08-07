import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence, useDragControls } from 'framer-motion';
import { X, ExternalLink, Star, Bot, Maximize2, Zap, Eye, Clock, Link } from 'lucide-react';

export default function EnhancedBubbleTab({ 
  tab, 
  position, 
  onPositionChange, 
  workspaceDimensions,
  isActive,
  onActivate,
  onClose,
  searchTerm = ''
}) {
  const [isHovered, setIsHovered] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const dragControls = useDragControls();
  const tabRef = useRef(null);

  // Highlight search term in title
  const getHighlightedTitle = (title, searchTerm) => {
    if (!searchTerm) return title;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    const parts = title.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-300/30 text-yellow-200 rounded px-1">
          {part}
        </mark>
      ) : part
    );
  };

  const handleAIAnalysis = async () => {
    if (tab.url === 'about:blank') return;
    
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/smart-content-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          url: tab.url,
          analysis_type: 'comprehensive'
        })
      });

      if (response.ok) {
        const analysis = await response.json();
        console.log('AI Analysis:', analysis);
        
        // Update tab metadata
        if (tab.metadata) {
          tab.metadata.ai_analyzed = true;
          tab.metadata.analysis_result = analysis;
        }
      }
    } catch (error) {
      console.error('AI Analysis failed:', error);
    }
  };

  const getDomainFavicon = (url) => {
    try {
      const domain = new URL(url).hostname;
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
    } catch {
      return null;
    }
  };

  const getTabColor = () => {
    if (isActive) return 'from-purple-600 to-blue-600';
    if (tab.metadata?.ai_analyzed) return 'from-green-500 to-emerald-600';
    if (isHovered) return 'from-purple-500/80 to-blue-500/80';
    return 'from-gray-700 to-gray-600';
  };

  const getBorderColor = () => {
    if (isActive) return 'border-purple-400/50';
    if (tab.metadata?.ai_analyzed) return 'border-green-400/50';
    return 'border-gray-600/30';
  };

  return (
    <motion.div
      ref={tabRef}
      className={`absolute select-none cursor-grab active:cursor-grabbing z-10 group ${
        isDragging ? 'z-50' : ''
      }`}
      style={{
        left: position.x,
        top: position.y,
      }}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ 
        scale: isDragging ? 1.1 : isActive ? 1.05 : 1, 
        opacity: 1,
        rotate: isDragging ? Math.random() * 6 - 3 : 0
      }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ 
        type: "spring", 
        stiffness: 260, 
        damping: 20,
        opacity: { duration: 0.2 }
      }}
      drag
      dragControls={dragControls}
      dragElastic={0.1}
      dragMomentum={false}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={(event, info) => {
        setIsDragging(false);
        const newX = position.x + info.offset.x;
        const newY = position.y + info.offset.y;
        onPositionChange(tab.id, newX, newY);
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {/* Main Tab Container */}
      <div
        className={`relative w-64 bg-gray-900/90 backdrop-blur-xl border-2 ${getBorderColor()} rounded-2xl shadow-2xl transition-all duration-300 overflow-hidden`}
        onClick={() => !isDragging && onActivate()}
      >
        {/* Background Gradient */}
        <div className={`absolute inset-0 bg-gradient-to-br ${getTabColor()} opacity-10`} />
        
        {/* Active Tab Pulse Effect */}
        {isActive && (
          <motion.div
            className="absolute inset-0 bg-gradient-to-br from-purple-400/20 to-blue-400/20 rounded-2xl"
            animate={{ opacity: [0.2, 0.4, 0.2] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        )}

        {/* Tab Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700/50">
          <div className="flex items-center space-x-3 flex-1 min-w-0">
            {/* Favicon */}
            <div className="w-8 h-8 rounded-lg bg-gray-800 flex items-center justify-center flex-shrink-0 overflow-hidden">
              {getDomainFavicon(tab.url) ? (
                <img 
                  src={getDomainFavicon(tab.url)} 
                  alt="" 
                  className="w-6 h-6"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
              ) : null}
              <div className="w-6 h-6 text-gray-400 flex items-center justify-center text-sm font-bold">
                {tab.title ? tab.title.charAt(0).toUpperCase() : '🌐'}
              </div>
            </div>

            {/* Tab Title */}
            <div className="flex-1 min-w-0">
              <h3 className="text-white font-medium text-sm truncate leading-tight">
                {getHighlightedTitle(tab.title || 'Untitled Tab', searchTerm)}
              </h3>
              <p className="text-gray-400 text-xs truncate">
                {tab.url === 'about:blank' ? 'New Tab' : tab.url}
              </p>
            </div>
          </div>

          {/* Status Indicators */}
          <div className="flex items-center space-x-1 flex-shrink-0">
            {tab.metadata?.ai_analyzed && (
              <motion.div
                className="w-2 h-2 bg-green-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                title="AI Analyzed"
              />
            )}
            {isActive && (
              <motion.div
                className="w-2 h-2 bg-purple-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 1.5 }}
                title="Active Tab"
              />
            )}
          </div>
        </div>

        {/* Tab Content/Preview */}
        <div className="p-4">
          {/* URL Preview */}
          {tab.url !== 'about:blank' && (
            <div className="flex items-center space-x-2 mb-3 text-xs text-gray-400">
              <Link size={12} />
              <span className="truncate flex-1">{tab.url}</span>
            </div>
          )}

          {/* Metadata Display */}
          {tab.metadata?.analysis_result && (
            <div className="mb-3 p-2 bg-green-500/10 border border-green-500/20 rounded-lg">
              <div className="flex items-center text-green-400 text-xs font-medium mb-1">
                <Bot size={12} className="mr-1" />
                AI Analysis Available
              </div>
              <p className="text-gray-300 text-xs line-clamp-2">
                {typeof tab.metadata.analysis_result === 'object' ? 
                  JSON.stringify(tab.metadata.analysis_result).substring(0, 100) + '...' :
                  tab.metadata.analysis_result
                }
              </p>
            </div>
          )}

          {/* Tab Actions */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {/* AI Analysis Button */}
              {tab.url !== 'about:blank' && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAIAnalysis();
                  }}
                  className="flex items-center px-2 py-1 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded text-xs transition-colors"
                  title="AI Analysis"
                >
                  <Zap size={10} className="mr-1" />
                  AI
                </button>
              )}

              {/* Timestamp */}
              <div className="flex items-center text-gray-500 text-xs">
                <Clock size={10} className="mr-1" />
                {new Date(tab.created_at || Date.now()).toLocaleTimeString()}
              </div>
            </div>

            <div className="flex items-center space-x-1">
              {/* External Link */}
              {tab.url !== 'about:blank' && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    window.open(tab.url, '_blank');
                  }}
                  className="w-6 h-6 rounded bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                  title="Open in New Window"
                >
                  <ExternalLink size={12} />
                </button>
              )}

              {/* Maximize */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onActivate();
                }}
                className="w-6 h-6 rounded bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                title="Activate Tab"
              >
                <Maximize2 size={12} />
              </button>

              {/* Close */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onClose();
                }}
                className="w-6 h-6 rounded bg-red-500/20 hover:bg-red-500/40 flex items-center justify-center text-red-400 hover:text-red-300 transition-colors"
                title="Close Tab"
              >
                <X size={12} />
              </button>
            </div>
          </div>
        </div>

        {/* Enhanced Hover Effects */}
        <AnimatePresence>
          {(isHovered || isActive) && (
            <motion.div
              className="absolute inset-0 pointer-events-none"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Glow Effect */}
              <div className={`absolute inset-0 rounded-2xl shadow-lg ${
                isActive ? 'shadow-purple-500/25' : 'shadow-blue-500/20'
              }`} />
              
              {/* Animated Border */}
              <motion.div
                className={`absolute inset-0 rounded-2xl border-2 ${
                  isActive ? 'border-purple-400/50' : 'border-blue-400/30'
                }`}
                animate={{ 
                  borderColor: isActive ? 
                    ['rgba(168, 85, 247, 0.5)', 'rgba(59, 130, 246, 0.5)', 'rgba(168, 85, 247, 0.5)'] :
                    ['rgba(59, 130, 246, 0.3)', 'rgba(168, 85, 247, 0.3)', 'rgba(59, 130, 246, 0.3)']
                }}
                transition={{ repeat: Infinity, duration: 3 }}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Drag Handle Indicator */}
        {(isHovered || isDragging) && (
          <motion.div
            className="absolute top-2 right-2 flex space-x-0.5 opacity-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
          >
            <div className="w-1 h-1 bg-gray-400 rounded-full" />
            <div className="w-1 h-1 bg-gray-400 rounded-full" />
            <div className="w-1 h-1 bg-gray-400 rounded-full" />
          </motion.div>
        )}

        {/* Connection Node (for future link visualization) */}
        {isActive && (
          <motion.div
            className="absolute -right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 bg-purple-500 rounded-full border-2 border-gray-900"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
          />
        )}
      </div>

      {/* Tab Details Popup (On Right Click or Long Press) */}
      <AnimatePresence>
        {showDetails && (
          <motion.div
            className="absolute top-full left-0 mt-2 w-80 bg-gray-900/95 backdrop-blur-xl border border-gray-700/50 rounded-xl shadow-2xl p-4 z-20"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <div className="flex justify-between items-start mb-3">
              <h4 className="text-white font-semibold text-sm">Tab Details</h4>
              <button
                onClick={() => setShowDetails(false)}
                className="text-gray-400 hover:text-white"
              >
                <X size={14} />
              </button>
            </div>
            
            <div className="space-y-2 text-xs">
              <div>
                <span className="text-gray-400">URL:</span>
                <p className="text-gray-300 break-all">{tab.url}</p>
              </div>
              <div>
                <span className="text-gray-400">Created:</span>
                <p className="text-gray-300">{new Date(tab.created_at || Date.now()).toLocaleString()}</p>
              </div>
              {tab.metadata?.ai_analyzed && (
                <div>
                  <span className="text-gray-400">AI Analysis:</span>
                  <p className="text-green-300">Available</p>
                </div>
              )}
              <div className="flex space-x-2 mt-3">
                <button className="px-2 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded text-xs transition-colors">
                  Bookmark
                </button>
                <button className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-xs transition-colors">
                  Duplicate
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}