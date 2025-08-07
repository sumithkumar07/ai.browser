import React, { useState, useRef, useEffect } from 'react';
import { useDrag } from 'react-dnd';
import { useSpring, animated } from 'react-spring';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { X, ExternalLink, Star, Bot, Zap, FileText, Maximize2, Minimize2 } from 'lucide-react';

export default function EnhancedBubbleTab({ tab, position, onPositionChange, workspaceDimensions }) {
  const { activeTab, setActiveTab, closeTab, updateTab } = useBrowser();
  const { addToAutomationQueue, setCurrentAnalysis } = useAI();
  const [isDragging, setIsDragging] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [velocity, setVelocity] = useState({ x: 0, y: 0 });
  const dragRef = useRef(null);
  const lastMousePos = useRef({ x: 0, y: 0 });

  const isActive = activeTab === tab.id;
  const isAIAnalyzed = tab.metadata?.ai_analyzed;

  // Physics-based spring animation
  const [springProps, setSpring] = useSpring(() => ({
    x: position.x,
    y: position.y,
    scale: 1,
    rotation: 0,
    opacity: 1,
    glow: isAIAnalyzed ? 1 : 0,
    config: { tension: 300, friction: 30 }
  }));

  // Update spring when position changes
  useEffect(() => {
    setSpring({
      x: position.x,
      y: position.y,
      scale: isActive ? 1.1 : isHovered ? 1.05 : 1,
      rotation: isActive ? 360 : 0,
      glow: isAIAnalyzed ? 1 : 0
    });
  }, [position, isActive, isHovered, isAIAnalyzed, setSpring]);

  // Drag and drop with physics
  const [{ isDraggingState }, drag] = useDrag({
    type: 'bubble-tab',
    item: { id: tab.id, x: position.x, y: position.y },
    begin: (monitor) => {
      setIsDragging(true);
      const clientOffset = monitor.getInitialClientOffset();
      lastMousePos.current = { x: clientOffset.x, y: clientOffset.y };
      return { id: tab.id, x: position.x, y: position.y };
    },
    drag: (item, monitor) => {
      const clientOffset = monitor.getClientOffset();
      if (!clientOffset) return;

      // Calculate velocity for physics effects
      const deltaX = clientOffset.x - lastMousePos.current.x;
      const deltaY = clientOffset.y - lastMousePos.current.y;
      setVelocity({ x: deltaX, y: deltaY });
      lastMousePos.current = { x: clientOffset.x, y: clientOffset.y };

      // Update position with momentum
      const newX = item.x + (clientOffset.x - lastMousePos.current.x);
      const newY = item.y + (clientOffset.y - lastMousePos.current.y);
      
      onPositionChange(tab.id, newX, newY);
    },
    end: (item, monitor) => {
      setIsDragging(false);
      
      // Apply momentum after drag ends
      const finalX = Math.max(0, Math.min(item.x + velocity.x * 0.3, workspaceDimensions.width - 200));
      const finalY = Math.max(60, Math.min(item.y + velocity.y * 0.3, workspaceDimensions.height - 150));
      
      setTimeout(() => {
        onPositionChange(tab.id, finalX, finalY);
      }, 100);
    },
    collect: (monitor) => ({
      isDraggingState: monitor.isDragging(),
    }),
  });

  // Collision detection with other tabs
  useEffect(() => {
    // This would be implemented with a collision detection system
    // For now, we'll simulate magnetic attraction when tabs are near each other
  }, [position]);

  const handleTabClick = () => {
    if (!isDragging) {
      setActiveTab(tab.id);
    }
  };

  const handleCloseTab = (e) => {
    e.stopPropagation();
    // Add close animation
    setSpring({
      scale: 0,
      opacity: 0,
      onRest: () => closeTab(tab.id)
    });
  };

  const handleAIAnalysis = async (e) => {
    e.stopPropagation();
    
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/content/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          url: tab.url,
          analysis_types: ['summary', 'keywords', 'sentiment']
        })
      });

      const analysis = await response.json();
      
      // Update tab with AI analysis
      updateTab({
        ...tab,
        metadata: {
          ...tab.metadata,
          ai_analyzed: true,
          analysis: analysis.analysis
        }
      });
      
      setCurrentAnalysis(analysis);
      
    } catch (error) {
      console.error('AI analysis failed:', error);
    }
  };

  const handleAddToAutomation = (e) => {
    e.stopPropagation();
    addToAutomationQueue({
      id: Date.now(),
      tabId: tab.id,
      url: tab.url,
      title: tab.title,
      automationType: 'general'
    });
  };

  const getTabTheme = () => {
    if (isActive) return 'bg-gradient-to-br from-ai-primary/30 to-ai-secondary/30 border-ai-primary';
    if (isAIAnalyzed) return 'bg-gradient-to-br from-purple-600/20 to-indigo-600/20 border-purple-400';
    return 'bg-gradient-to-br from-slate-700/30 to-slate-600/30 border-slate-500';
  };

  return (
    <animated.div
      ref={(node) => {
        dragRef.current = node;
        drag(node);
      }}
      className={`enhanced-bubble-tab ${isDragging || isDraggingState ? 'dragging' : ''} ${getTabTheme()}`}
      style={{
        position: 'absolute',
        left: springProps.x,
        top: springProps.y,
        transform: springProps.scale.to(s => `scale(${s})`),
        opacity: springProps.opacity,
        zIndex: isActive ? 100 : isDragging ? 1000 : 10,
        filter: springProps.glow.to(g => `drop-shadow(0 0 ${g * 20}px rgba(139, 92, 246, ${g * 0.6}))`),
        width: isExpanded ? '300px' : '200px',
        height: isExpanded ? '200px' : '140px',
        borderRadius: '20px',
        border: '2px solid',
        backdropFilter: 'blur(20px)',
        cursor: isDragging ? 'grabbing' : 'grab',
        transition: 'width 0.3s ease, height 0.3s ease'
      }}
      onClick={handleTabClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Header with controls */}
      <div className="tab-header flex justify-between items-center p-3 border-b border-white/10">
        <div className="tab-favicon-enhanced flex items-center space-x-2">
          {isAIAnalyzed ? (
            <Bot size={16} className="text-purple-400" />
          ) : (
            <span className="text-lg">🌐</span>
          )}
          {tab.is_pinned && <Star size={12} className="text-yellow-400 fill-current" />}
        </div>
        
        <div className="tab-controls flex space-x-1">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="tab-control-btn"
            title="Expand/Collapse"
          >
            {isExpanded ? <Minimize2 size={12} /> : <Maximize2 size={12} />}
          </button>
          
          <button
            onClick={handleCloseTab}
            className="tab-control-btn text-red-400 hover:text-red-300"
            title="Close Tab"
          >
            <X size={12} />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="tab-content-enhanced p-3">
        <div className="tab-title-enhanced text-white font-medium text-sm mb-2 line-clamp-2">
          {tab.title || 'New Tab'}
        </div>
        
        <div className="tab-url-enhanced text-gray-300 text-xs mb-3 line-clamp-1">
          {tab.url === 'about:blank' ? 'New Tab' : tab.url}
        </div>

        {/* Progress bar for loading */}
        {isActive && (
          <div className="loading-bar w-full h-1 bg-gray-600 rounded mb-3 overflow-hidden">
            <div className="loading-progress h-full bg-gradient-to-r from-ai-primary to-ai-secondary rounded animate-pulse"></div>
          </div>
        )}

        {/* AI Analysis Results */}
        {isAIAnalyzed && tab.metadata?.analysis && isExpanded && (
          <div className="ai-analysis-preview bg-black/20 rounded-lg p-2 mb-3 text-xs">
            <div className="text-purple-300 font-medium mb-1">AI Analysis</div>
            <div className="text-gray-300 line-clamp-3">
              {typeof tab.metadata.analysis === 'string' 
                ? tab.metadata.analysis 
                : 'Content analyzed successfully'}
            </div>
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div className="tab-actions-enhanced absolute bottom-3 left-3 right-3 flex justify-between">
        <div className="flex space-x-2">
          {!isAIAnalyzed && tab.url !== 'about:blank' && (
            <button
              onClick={handleAIAnalysis}
              className="action-btn bg-purple-600/20 hover:bg-purple-600/40 border border-purple-400/30"
              title="AI Analysis"
            >
              <Bot size={12} />
            </button>
          )}
          
          <button
            onClick={handleAddToAutomation}
            className="action-btn bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30"
            title="Add to Automation"
          >
            <Zap size={12} />
          </button>
        </div>
        
        {tab.url !== 'about:blank' && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              window.open(tab.url, '_blank');
            }}
            className="action-btn bg-green-600/20 hover:bg-green-600/40 border border-green-400/30"
            title="Open in New Window"
          >
            <ExternalLink size={12} />
          </button>
        )}
      </div>

      {/* Physics effects */}
      {isDragging && (
        <div className="drag-trail absolute inset-0 rounded-20px bg-gradient-to-r from-ai-primary/10 to-ai-secondary/10 animate-pulse"></div>
      )}

      {/* Active tab indicator */}
      {isActive && (
        <div className="active-indicator absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-8 h-1 bg-gradient-to-r from-ai-primary to-ai-secondary rounded-full animate-pulse"></div>
      )}

      {/* Hover effects */}
      {isHovered && !isDragging && (
        <div className="hover-glow absolute inset-0 rounded-20px bg-white/5 pointer-events-none"></div>
      )}
    </animated.div>
  );
}