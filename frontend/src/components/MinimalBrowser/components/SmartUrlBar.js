import React, { forwardRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, Globe, Shield, Star, Clock, Zap, 
  Brain, Bookmark, TrendingUp 
} from 'lucide-react';

const SmartUrlBar = forwardRef(({
  value,
  onInput,
  onSubmit,
  suggestions,
  showSuggestions,
  onSuggestionSelect,
  isLoading,
  placeholder
}, ref) => {
  const [focused, setFocused] = useState(false);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSubmit(value);
    } else if (e.key === 'Escape') {
      setFocused(false);
    }
  };

  const getSuggestionIcon = (type) => {
    switch (type) {
      case 'search': return Search;
      case 'navigate': return Globe;
      case 'bookmark': return Bookmark;
      case 'ai_analyze': return Brain;
      case 'optimize': return Zap;
      default: return Globe;
    }
  };

  return (
    <div className="smart-url-bar flex-1 relative max-w-2xl">
      <div className="relative">
        <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
          <Shield size={16} className="text-green-500" />
        </div>
        
        <input
          ref={ref}
          type="text"
          value={value}
          onChange={(e) => onInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setFocused(true)}
          onBlur={() => setTimeout(() => setFocused(false), 200)}
          placeholder={placeholder}
          className={`w-full h-10 pl-10 pr-12 bg-gray-50 border rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
            focused ? 'border-blue-300 bg-white shadow-sm' : 'border-gray-300'
          }`}
        />
        
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
          {isLoading && (
            <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          )}
          <Globe size={14} className="text-gray-400" />
        </div>
      </div>

      {/* Smart Suggestions Dropdown */}
      <AnimatePresence>
        {showSuggestions && suggestions.length > 0 && focused && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden"
          >
            {suggestions.map((suggestion, index) => {
              const Icon = getSuggestionIcon(suggestion.type);
              return (
                <motion.button
                  key={index}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => onSuggestionSelect(suggestion)}
                  className="w-full text-left px-4 py-3 hover:bg-gray-50 flex items-center space-x-3 transition-colors"
                >
                  <Icon size={16} className="text-gray-500 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm text-gray-900 truncate">
                      {suggestion.suggestion}
                    </div>
                    <div className="text-xs text-gray-500">
                      {suggestion.type === 'search' && 'Search with Google'}
                      {suggestion.type === 'navigate' && 'Navigate to URL'}
                      {suggestion.type === 'ai_analyze' && 'AI Analysis'}
                      {suggestion.type === 'bookmark' && 'Smart Bookmark'}
                      {suggestion.type === 'optimize' && 'Performance Boost'}
                    </div>
                  </div>
                  <div className="text-xs text-gray-400">
                    {Math.round(suggestion.confidence * 100)}%
                  </div>
                </motion.button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

export default SmartUrlBar;