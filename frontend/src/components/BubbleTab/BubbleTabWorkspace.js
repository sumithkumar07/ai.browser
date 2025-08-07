import React, { useState, useRef, useEffect } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import BubbleTab from './BubbleTab';

export default function BubbleTabWorkspace() {
  const { tabs, bubblePositions, updateBubblePosition } = useBrowser();
  const workspaceRef = useRef(null);
  const [workspaceDimensions, setWorkspaceDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const updateDimensions = () => {
      if (workspaceRef.current) {
        setWorkspaceDimensions({
          width: workspaceRef.current.clientWidth,
          height: workspaceRef.current.clientHeight
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const handleTabPositionUpdate = (tabId, x, y) => {
    // Boundary checking
    const boundedX = Math.max(0, Math.min(x, workspaceDimensions.width - 200));
    const boundedY = Math.max(60, Math.min(y, workspaceDimensions.height - 150));
    
    updateBubblePosition(tabId, boundedX, boundedY);
  };

  return (
    <div 
      ref={workspaceRef}
      className="bubble-workspace absolute inset-0 top-16"
    >
      {tabs.map((tab) => (
        <BubbleTab
          key={tab.id}
          tab={tab}
          position={bubblePositions[tab.id] || { x: tab.position_x || 200, y: tab.position_y || 150 }}
          onPositionChange={handleTabPositionUpdate}
          workspaceDimensions={workspaceDimensions}
        />
      ))}
      
      {tabs.length === 0 && (
        <div className="flex items-center justify-center h-full text-gray-500">
          <div className="text-center">
            <div className="text-6xl mb-4">🌐</div>
            <p className="text-xl">No tabs open</p>
            <p className="text-sm mt-2">Click the + button to create a new tab</p>
          </div>
        </div>
      )}
    </div>
  );
}