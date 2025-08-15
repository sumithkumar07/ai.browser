import React, { useState, useEffect, forwardRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Globe, Clock, Bookmark, Zap, Brain, ChevronRight, Star } from 'lucide-react';

const SmartUrlBar = forwardRef(({ 
  value, 
  onSubmit, 
  onShowSuggestions, 
  showSuggestions, 
  isLoading 
}, ref) => {
  const [inputValue, setInputValue] = useState(value);
  const [suggestions, setSuggestions] = useState([]);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  useEffect(() => {
    setInputValue(value);
  }, [value]);

  const generateSmartSuggestions = useCallback(async (query) => {
    if (!query || query.length < 2) {
      setSuggestions([]);
      setAiSuggestions([]);
      return;
    }

    // Generate different types of suggestions
    const suggestions = [];
    const aiSuggestions = [];

    // URL detection
    if (query.includes('.') && !query.includes(' ')) {
      suggestions.push({
        type: 'url',
        text: `https://${query}`,
        description: 'Navigate to website',
        icon: Globe,
        action: () => onSubmit(`https://${query}`)
      });
    }

    // Search suggestions
    const searchQueries = generateSearchSuggestions(query);
    searchQueries.forEach(searchQuery => {
      suggestions.push({
        type: 'search',
        text: searchQuery,
        description: 'Search on Google',
        icon: Search,
        action: () => onSubmit(`https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`)
      });
    });

    // AI-powered suggestions
    const aiPoweredSuggestions = await generateAISuggestions(query);
    aiSuggestions.push(...aiPoweredSuggestions);

    // Popular sites
    const popularSites = getPopularSites(query);
    popularSites.forEach(site => {
      suggestions.push({
        type: 'popular',
        text: site.name,
        description: site.description,
        icon: Globe,
        url: site.url,
        action: () => onSubmit(site.url)
      });
    });

    // History suggestions (mock data for now)
    const historyItems = getHistorySuggestions(query);
    historyItems.forEach(item => {
      suggestions.push({
        type: 'history',
        text: item.title,
        description: item.url,
        icon: Clock,
        action: () => onSubmit(item.url),
        timestamp: item.lastVisited
      });
    });

    setSuggestions(suggestions.slice(0, 6));
    setAiSuggestions(aiSuggestions.slice(0, 3));
  }, [onSubmit]);

  const generateSearchSuggestions = (query) => {
    // Simulate smart search suggestions
    const baseSuggestions = [
      query,
      `${query} tutorial`,
      `${query} examples`,
      `what is ${query}`,
      `${query} vs`,
      `best ${query}`
    ];
    
    return baseSuggestions.slice(0, 3);
  };

  const generateAISuggestions = async (query) => {
    // Simulate AI-powered contextual suggestions
    const aiSuggestions = [
      {
        type: 'ai-explain',
        text: `Explain "${query}" with AI`,
        description: 'Get AI-powered explanation and analysis',
        icon: Brain,
        action: () => {
          // Trigger AI explanation
          console.log('AI Explain:', query);
        }
      },
      {
        type: 'ai-research',
        text: `Research "${query}" comprehensively`,
        description: 'AI will gather information from multiple sources',
        icon: Zap,
        action: () => {
          // Trigger AI research
          console.log('AI Research:', query);
        }
      }
    ];

    // Add contextual suggestions based on query type
    if (query.includes('buy') || query.includes('purchase') || query.includes('price')) {
      aiSuggestions.push({
        type: 'ai-shopping',
        text: `Find best deals for "${query}"`,
        description: 'AI will compare prices and find best options',
        icon: Star,
        action: () => console.log('AI Shopping:', query)
      });
    }

    return aiSuggestions;
  };

  const getPopularSites = (query) => {
    const sites = [
      { name: 'Google', url: 'https://www.google.com', description: 'Search engine' },
      { name: 'YouTube', url: 'https://www.youtube.com', description: 'Videos' },
      { name: 'GitHub', url: 'https://github.com', description: 'Code repository' },
      { name: 'Stack Overflow', url: 'https://stackoverflow.com', description: 'Programming Q&A' },
      { name: 'Reddit', url: 'https://www.reddit.com', description: 'Discussion platform' },
      { name: 'Twitter', url: 'https://twitter.com', description: 'Social media' },
      { name: 'LinkedIn', url: 'https://www.linkedin.com', description: 'Professional network' },
      { name: 'Wikipedia', url: 'https://wikipedia.org', description: 'Encyclopedia' }
    ];

    return sites.filter(site => 
      site.name.toLowerCase().includes(query.toLowerCase())
    ).slice(0, 2);
  };

  const getHistorySuggestions = (query) => {
    // Mock history data - in real implementation, this would come from backend
    const mockHistory = [
      {
        title: 'React Documentation - Getting Started',
        url: 'https://reactjs.org/docs/getting-started.html',
        lastVisited: new Date(Date.now() - 86400000) // 1 day ago
      },
      {
        title: 'JavaScript MDN Web Docs',
        url: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
        lastVisited: new Date(Date.now() - 172800000) // 2 days ago
      }
    ];

    return mockHistory.filter(item =>
      item.title.toLowerCase().includes(query.toLowerCase()) ||
      item.url.toLowerCase().includes(query.toLowerCase())
    );
  };

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    setSelectedIndex(-1);
    
    if (newValue.trim()) {
      generateSmartSuggestions(newValue);
      onShowSuggestions(true);
    } else {
      onShowSuggestions(false);
    }
  };

  const handleKeyDown = (e) => {
    const totalSuggestions = suggestions.length + aiSuggestions.length;
    
    if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && selectedIndex < totalSuggestions) {
        const allSuggestions = [...suggestions, ...aiSuggestions];
        allSuggestions[selectedIndex].action();
      } else {
        onSubmit(inputValue);
      }
      onShowSuggestions(false);
    } else if (e.key === 'Escape') {
      onShowSuggestions(false);
      setSelectedIndex(-1);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => 
        prev < totalSuggestions - 1 ? prev + 1 : -1
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => 
        prev > -1 ? prev - 1 : totalSuggestions - 1
      );
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(inputValue);
    onShowSuggestions(false);
  };

  const formatTimeAgo = (date) => {
    const diff = Date.now() - date.getTime();
    const days = Math.floor(diff / 86400000);
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    return `${days} days ago`;
  };

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              inputValue.startsWith('https://') ? 'bg-green-400' : 'bg-gray-400'
            }`} />
            <Search size={14} className="text-gray-400" />
          </div>
          
          <input
            ref={ref}
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => inputValue && onShowSuggestions(true)}
            onBlur={() => setTimeout(() => onShowSuggestions(false), 150)}
            placeholder="Search or enter URL - AI enhanced..."
            className="w-full h-11 pl-12 pr-16 bg-gray-800/70 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500/50 focus:bg-gray-800/90 text-sm transition-all duration-200"
          />
          
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
            {isLoading && (
              <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            )}
            <div className="w-5 h-5 flex items-center justify-center">
              <Brain size={12} className="text-purple-400" />
            </div>
          </div>
        </div>
      </form>

      {/* Smart Suggestions Dropdown */}
      <AnimatePresence>
        {showSuggestions && (suggestions.length > 0 || aiSuggestions.length > 0) && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute top-full left-0 right-0 mt-2 bg-gray-800/95 backdrop-blur-sm border border-gray-600/50 rounded-lg shadow-2xl z-50 max-h-96 overflow-y-auto"
          >
            {/* AI-Powered Suggestions */}
            {aiSuggestions.length > 0 && (
              <div className="border-b border-gray-700/50">
                <div className="px-4 py-2 text-xs text-purple-300 font-medium bg-purple-900/20">
                  <Brain size={12} className="inline mr-1" />
                  AI-Powered Suggestions
                </div>
                {aiSuggestions.map((suggestion, index) => (
                  <button
                    key={`ai-${index}`}
                    onClick={suggestion.action}
                    className={`w-full text-left px-4 py-3 text-sm hover:bg-gray-700/50 transition-colors flex items-center space-x-3 ${
                      selectedIndex === suggestions.length + index ? 'bg-blue-600/20 border-l-2 border-blue-500' : ''
                    }`}
                  >
                    <suggestion.icon size={16} className="text-purple-400 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-white truncate">{suggestion.text}</div>
                      <div className="text-gray-400 text-xs truncate">{suggestion.description}</div>
                    </div>
                    <ChevronRight size={12} className="text-gray-500" />
                  </button>
                ))}
              </div>
            )}

            {/* Regular Suggestions */}
            {suggestions.length > 0 && (
              <div>
                {suggestions.map((suggestion, index) => (
                  <button
                    key={`regular-${index}`}
                    onClick={suggestion.action}
                    className={`w-full text-left px-4 py-3 text-sm hover:bg-gray-700/50 transition-colors flex items-center space-x-3 ${
                      selectedIndex === index ? 'bg-blue-600/20 border-l-2 border-blue-500' : ''
                    }`}
                  >
                    <suggestion.icon size={16} className={`flex-shrink-0 ${
                      suggestion.type === 'history' ? 'text-blue-400' :
                      suggestion.type === 'popular' ? 'text-green-400' :
                      suggestion.type === 'search' ? 'text-yellow-400' : 'text-gray-400'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="text-white truncate">{suggestion.text}</div>
                      <div className="text-gray-400 text-xs truncate">
                        {suggestion.description}
                        {suggestion.timestamp && (
                          <span className="ml-2">• {formatTimeAgo(suggestion.timestamp)}</span>
                        )}
                      </div>
                    </div>
                    {suggestion.type === 'url' && (
                      <div className="text-xs text-gray-500 bg-gray-700/50 px-2 py-1 rounded">
                        Visit
                      </div>
                    )}
                  </button>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

SmartUrlBar.displayName = 'SmartUrlBar';

export default SmartUrlBar;