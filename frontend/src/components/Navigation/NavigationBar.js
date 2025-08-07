import React, { useState } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useUser } from '../../contexts/UserContext';
import { Search, ArrowLeft, ArrowRight, RotateCcw, Home, Settings } from 'lucide-react';

export default function NavigationBar() {
  const { activeTab, tabs, updateTab } = useBrowser();
  const { user } = useUser();
  const [urlInput, setUrlInput] = useState('');

  const activeTabData = tabs.find(tab => tab.id === activeTab);

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    if (activeTabData && urlInput.trim()) {
      let url = urlInput.trim();
      
      // Add protocol if missing
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        // Check if it's a search query or URL
        if (url.includes('.') && !url.includes(' ')) {
          url = 'https://' + url;
        } else {
          // Treat as search query
          url = `https://www.google.com/search?q=${encodeURIComponent(url)}`;
        }
      }
      
      updateTab({
        ...activeTabData,
        url: url,
        title: 'Loading...'
      });
    }
  };

  const handleBackButton = () => {
    // TODO: Implement back navigation
    console.log('Back navigation');
  };

  const handleForwardButton = () => {
    // TODO: Implement forward navigation
    console.log('Forward navigation');
  };

  const handleRefresh = () => {
    // TODO: Implement page refresh
    console.log('Refresh page');
  };

  const handleHome = () => {
    if (activeTabData) {
      updateTab({
        ...activeTabData,
        url: 'about:blank',
        title: 'New Tab'
      });
      setUrlInput('');
    }
  };

  return (
    <div className="nav-bar">
      {/* Navigation Controls */}
      <div className="flex items-center space-x-2">
        <button
          onClick={handleBackButton}
          className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
          disabled={!activeTabData}
        >
          <ArrowLeft size={16} className="text-white/80" />
        </button>
        
        <button
          onClick={handleForwardButton}
          className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
          disabled={!activeTabData}
        >
          <ArrowRight size={16} className="text-white/80" />
        </button>
        
        <button
          onClick={handleRefresh}
          className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
          disabled={!activeTabData}
        >
          <RotateCcw size={16} className="text-white/80" />
        </button>
        
        <button
          onClick={handleHome}
          className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
        >
          <Home size={16} className="text-white/80" />
        </button>
      </div>

      {/* URL Input */}
      <form onSubmit={handleUrlSubmit} className="flex-1 max-w-2xl mx-4">
        <div className="relative">
          <input
            type="text"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder={activeTabData?.url || "Search or enter URL..."}
            className="url-input w-full"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 w-6 h-6 rounded bg-ai-primary/20 hover:bg-ai-primary/40 flex items-center justify-center transition-colors"
          >
            <Search size={14} className="text-ai-primary" />
          </button>
        </div>
      </form>

      {/* User Controls */}
      <div className="flex items-center space-x-2">
        <div className="text-sm text-white/80">
          {user?.username}
        </div>
        
        <button className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors">
          <Settings size={16} className="text-white/80" />
        </button>
      </div>
    </div>
  );
}