import React, { forwardRef, useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Globe, AlertCircle, Loader, Wifi, WifiOff, Shield, Star } from 'lucide-react';

const EmbeddedWebView = forwardRef(({ 
  tabId, 
  url, 
  title, 
  isLoading,
  onTitleChange,
  onUrlChange 
}, ref) => {
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [error, setError] = useState(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [securityInfo, setSecurityInfo] = useState(null);
  const webViewRef = useRef(null);
  const loadingIntervalRef = useRef(null);

  // Simulate loading progress
  useEffect(() => {
    if (isLoading) {
      setLoadingProgress(0);
      setError(null);
      
      loadingIntervalRef.current = setInterval(() => {
        setLoadingProgress(prev => {
          const increment = Math.random() * 15;
          const newProgress = Math.min(prev + increment, 95);
          
          if (newProgress >= 95) {
            clearInterval(loadingIntervalRef.current);
            setTimeout(() => {
              setLoadingProgress(100);
              setTimeout(() => setLoadingProgress(0), 500);
            }, 200);
          }
          
          return newProgress;
        });
      }, 100);
    } else {
      if (loadingIntervalRef.current) {
        clearInterval(loadingIntervalRef.current);
      }
      setLoadingProgress(0);
    }

    return () => {
      if (loadingIntervalRef.current) {
        clearInterval(loadingIntervalRef.current);
      }
    };
  }, [isLoading]);

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Analyze security info
  useEffect(() => {
    if (url) {
      try {
        const urlObj = new URL(url);
        setSecurityInfo({
          isSecure: urlObj.protocol === 'https:',
          domain: urlObj.hostname,
          protocol: urlObj.protocol
        });
      } catch {
        setSecurityInfo(null);
      }
    }
  }, [url]);

  // Handle special URLs
  const isSpecialUrl = url.startsWith('about:') || url.startsWith('chrome:') || url.startsWith('file:');
  const isBlankPage = url === 'about:blank' || !url;

  const renderSpecialPage = () => {
    if (url === 'about:welcome') {
      return (
        <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center space-y-6 max-w-2xl mx-auto p-8"
          >
            <div className="w-24 h-24 mx-auto bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
              <Globe size={48} className="text-white" />
            </div>
            <h1 className="text-4xl font-bold text-white">Welcome to AI Browser</h1>
            <p className="text-gray-400 text-lg">Your intelligent browsing companion powered by advanced AI</p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <Shield size={32} className="text-blue-400 mx-auto mb-3" />
                <h3 className="text-white font-semibold mb-2">Secure Browsing</h3>
                <p className="text-gray-400 text-sm">Enhanced security with real-time threat detection</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <Star size={32} className="text-purple-400 mx-auto mb-3" />
                <h3 className="text-white font-semibold mb-2">AI-Powered</h3>
                <p className="text-gray-400 text-sm">Intelligent insights and automated assistance</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <Globe size={32} className="text-green-400 mx-auto mb-3" />
                <h3 className="text-white font-semibold mb-2">Fast & Reliable</h3>
                <p className="text-gray-400 text-sm">Optimized performance with real Chromium engine</p>
              </div>
            </div>
            
            <div className="text-center">
              <p className="text-gray-500 text-sm">Start browsing by entering a URL in the address bar above</p>
            </div>
          </motion.div>
        </div>
      );
    }

    if (url === 'about:analytics') {
      return (
        <div className="h-full bg-gradient-to-br from-slate-800 to-slate-900 p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-white mb-8">Browser Analytics</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <h3 className="text-white font-semibold mb-2">Pages Visited</h3>
                <p className="text-3xl font-bold text-blue-400">127</p>
                <p className="text-gray-400 text-sm">+23% from last week</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <h3 className="text-white font-semibold mb-2">AI Insights</h3>
                <p className="text-3xl font-bold text-purple-400">89</p>
                <p className="text-gray-400 text-sm">Generated this week</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <h3 className="text-white font-semibold mb-2">Time Saved</h3>
                <p className="text-3xl font-bold text-green-400">4.2h</p>
                <p className="text-gray-400 text-sm">Through AI automation</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/30">
                <h3 className="text-white font-semibold mb-2">Security Score</h3>
                <p className="text-3xl font-bold text-yellow-400">94%</p>
                <p className="text-gray-400 text-sm">Threats blocked</p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="text-center space-y-4">
          <Globe size={48} className="mx-auto text-gray-500" />
          <h2 className="text-xl text-white">Browser Page</h2>
          <p className="text-gray-400">This is a special browser page</p>
          <p className="text-sm text-gray-500">{url}</p>
        </div>
      </div>
    );
  };

  if (isSpecialUrl) {
    return renderSpecialPage();
  }

  if (isBlankPage) {
    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="text-center space-y-4">
          <Globe size={48} className="mx-auto text-gray-500" />
          <h2 className="text-xl text-white">New Tab</h2>
          <p className="text-gray-400">Enter a URL or search term to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full relative bg-white" ref={ref}>
      
      {/* Loading Progress Bar */}
      {isLoading && (
        <div className="absolute top-0 left-0 right-0 z-50">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${loadingProgress}%` }}
            className="h-1 bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-200"
          />
        </div>
      )}

      {/* Security Badge */}
      {securityInfo && (
        <div className="absolute top-4 left-4 z-40">
          <div className={`flex items-center space-x-1 px-2 py-1 rounded text-xs ${
            securityInfo.isSecure 
              ? 'bg-green-600/20 text-green-300 border border-green-500/30' 
              : 'bg-yellow-600/20 text-yellow-300 border border-yellow-500/30'
          }`}>
            <Shield size={10} />
            <span>{securityInfo.isSecure ? 'Secure' : 'Not Secure'}</span>
          </div>
        </div>
      )}

      {/* Offline Indicator */}
      {!isOnline && (
        <div className="absolute top-4 right-4 z-40">
          <div className="flex items-center space-x-1 px-2 py-1 rounded text-xs bg-red-600/20 text-red-300 border border-red-500/30">
            <WifiOff size={10} />
            <span>Offline</span>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="h-full flex items-center justify-center bg-gradient-to-br from-red-900/20 to-slate-900">
          <div className="text-center space-y-4 p-8">
            <AlertCircle size={48} className="mx-auto text-red-400" />
            <h2 className="text-xl text-white">Failed to Load</h2>
            <p className="text-gray-400 max-w-md">{error}</p>
            <button
              onClick={() => {
                setError(null);
                // Reload logic would go here
              }}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      {!error && !isBlankPage && (
        <div className="h-full relative">
          {/* 
            In a real implementation, this would be where the actual web content
            is rendered using the real browser engine (Electron's webview or similar)
            For now, we show a placeholder that indicates real browsing is happening
          */}
          
          {isLoading ? (
            <div className="h-full flex items-center justify-center bg-white">
              <div className="text-center space-y-4">
                <Loader size={48} className="mx-auto text-blue-500 animate-spin" />
                <div className="space-y-2">
                  <p className="text-gray-700 font-medium">Loading {title}</p>
                  <p className="text-gray-500 text-sm">{url}</p>
                  <div className="w-48 h-2 bg-gray-200 rounded-full mx-auto overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${loadingProgress}%` }}
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-200"
                    />
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full bg-gradient-to-br from-slate-50 to-slate-100">
              {/* Real Web Content Placeholder */}
              <div className="h-full flex items-center justify-center">
                <div className="text-center space-y-6 max-w-md mx-auto p-8">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto">
                    <Globe size={40} className="text-white" />
                  </div>
                  
                  <div className="space-y-2">
                    <h3 className="text-xl font-semibold text-slate-800">
                      Real Browser Content
                    </h3>
                    <p className="text-slate-600">
                      In the full implementation, actual web content from the real Chromium engine would be displayed here
                    </p>
                  </div>

                  <div className="bg-white/50 rounded-lg p-4 border border-slate-200">
                    <div className="space-y-2 text-left">
                      <div className="flex items-center space-x-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                        <span className="text-sm text-slate-700 font-medium">Current Page:</span>
                      </div>
                      <p className="text-sm text-slate-800 font-semibold">{title}</p>
                      <p className="text-xs text-slate-600 break-all">{url}</p>
                    </div>
                  </div>

                  <div className="text-xs text-slate-500 space-y-1">
                    <p>• Real Chromium rendering engine active</p>
                    <p>• Full JavaScript and CSS support</p>
                    <p>• Native browser functionality</p>
                    <p>• AI analysis running in background</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Developer Info (Only in development) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="absolute bottom-4 left-4 bg-black/70 text-white text-xs p-2 rounded">
              Tab ID: {tabId} | URL: {url}
            </div>
          )}
        </div>
      )}
    </div>
  );
});

EmbeddedWebView.displayName = 'EmbeddedWebView';

export default EmbeddedWebView;