import React, { useState, useRef } from 'react';
import { useDrag } from 'react-dnd';
import { useBrowser } from '../../contexts/BrowserContext';
import { X, ExternalLink, Star } from 'lucide-react';

export default function BubbleTab({ tab, position, onPositionChange, workspaceDimensions }) {
  const { activeTab, setActiveTab, closeTab } = useBrowser();
  const [isDragging, setIsDragging] = useState(false);
  const dragRef = useRef(null);

  const [{ isDraggingState }, drag] = useDrag({
    type: 'bubble-tab',
    item: { id: tab.id, x: position.x, y: position.y },
    begin: () => {
      setIsDragging(true);
    },
    end: (item, monitor) => {
      setIsDragging(false);
      const delta = monitor.getDifferenceFromInitialOffset();
      if (delta) {
        const newX = Math.round(item.x + delta.x);
        const newY = Math.round(item.y + delta.y);
        onPositionChange(tab.id, newX, newY);
      }
    },
    collect: (monitor) => ({
      isDraggingState: monitor.isDragging(),
    }),
  });

  const handleTabClick = () => {
    setActiveTab(tab.id);
  };

  const handleCloseTab = (e) => {
    e.stopPropagation();
    closeTab(tab.id);
  };

  const isActive = activeTab === tab.id;
  const isTabDragging = isDragging || isDraggingState;

  return (
    <div
      ref={(node) => {
        dragRef.current = node;
        drag(node);
      }}
      className={`bubble-tab ${isActive ? 'active' : ''} ${isTabDragging ? 'dragging' : ''}`}
      style={{
        left: position.x,
        top: position.y,
        zIndex: isActive ? 100 : isTabDragging ? 1000 : 10
      }}
      onClick={handleTabClick}
    >
      <div className="tab-content">
        {/* Close button */}
        <button
          onClick={handleCloseTab}
          className="absolute top-2 right-2 w-6 h-6 rounded-full bg-red-500/20 hover:bg-red-500/40 flex items-center justify-center text-red-300 hover:text-red-100 transition-colors"
        >
          <X size={14} />
        </button>

        {/* Favicon */}
        <div className="tab-favicon bg-gray-700 rounded flex items-center justify-center">
          🌐
        </div>

        {/* Tab title */}
        <div className="tab-title">
          {tab.title || 'New Tab'}
        </div>

        {/* Tab URL */}
        <div className="tab-url">
          {tab.url === 'about:blank' ? 'New Tab' : tab.url}
        </div>

        {/* Tab actions */}
        <div className="flex justify-between items-center mt-2">
          <div className="flex space-x-1">
            {tab.is_pinned && (
              <Star size={12} className="text-yellow-400 fill-current" />
            )}
          </div>
          
          {tab.url !== 'about:blank' && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                window.open(tab.url, '_blank');
              }}
              className="w-5 h-5 rounded bg-blue-500/20 hover:bg-blue-500/40 flex items-center justify-center text-blue-300 hover:text-blue-100 transition-colors"
            >
              <ExternalLink size={10} />
            </button>
          )}
        </div>

        {/* Loading indicator for active tab */}
        {isActive && (
          <div className="absolute bottom-1 left-1 right-1 h-0.5 bg-gradient-to-r from-ai-primary to-ai-secondary rounded"></div>
        )}
      </div>

      {/* AI analysis indicator */}
      {tab.metadata?.ai_analyzed && (
        <div className="absolute -top-1 -right-1 w-4 h-4 bg-ai-secondary rounded-full flex items-center justify-center">
          <span className="text-xs">🤖</span>
        </div>
      )}
    </div>
  );
}