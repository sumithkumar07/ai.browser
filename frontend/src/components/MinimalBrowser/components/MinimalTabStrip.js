import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, X, Globe } from 'lucide-react';

export default function MinimalTabStrip({ 
  tabs, 
  activeTabId, 
  onSwitchTab, 
  onCloseTab, 
  onNewTab 
}) {
  if (tabs.length === 0) return null;

  return (
    <div className="minimal-tab-strip bg-gray-50 border-b border-gray-200 px-4 py-1">
      <div className="flex items-center space-x-1 overflow-x-auto">
        {tabs.map((tab) => (
          <motion.div
            key={tab.id}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className={`minimal-tab flex items-center space-x-2 px-3 py-2 rounded-lg cursor-pointer transition-all min-w-[120px] max-w-[200px] ${
              tab.id === activeTabId 
                ? 'bg-white border border-gray-300 shadow-sm' 
                : 'hover:bg-gray-100'
            }`}
            onClick={() => onSwitchTab(tab.id)}
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                {tab.favicon ? (
                  <img src={tab.favicon} alt="" className="w-4 h-4" />
                ) : (
                  <Globe size={12} className="text-gray-400" />
                )}
                <span className="text-sm text-gray-700 truncate">
                  {tab.isLoading ? 'Loading...' : (tab.title || 'New Tab')}
                </span>
              </div>
            </div>
            
            {tabs.length > 1 && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onCloseTab(tab.id);
                }}
                className="p-0.5 hover:bg-gray-200 rounded text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X size={12} />
              </button>
            )}
          </motion.div>
        ))}
        
        {/* New Tab Button */}
        <button
          onClick={onNewTab}
          className="minimal-nav-btn p-2"
          title="New Tab"
        >
          <Plus size={16} />
        </button>
      </div>
    </div>
  );
}