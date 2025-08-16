import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import BrowserContextProvider from './contexts/BrowserContext';
import AIContextProvider from './contexts/AIContext';
import UserContextProvider from './contexts/UserContext';
import PerformanceContextProvider from './contexts/PerformanceContext';
import AccessibilityContextProvider from './contexts/AccessibilityContext';
import { ParallelFeaturesProvider } from './contexts/ParallelFeaturesContext';

// Import browser components
import UnifiedBrowser from './components/UnifiedBrowser/UnifiedBrowser';
import MainBrowser from './components/MainBrowser/MainBrowser';
import SimplifiedBrowser from './components/SimplifiedBrowser/SimplifiedBrowser';
import AuthWrapper from './components/Auth/AuthWrapper';
import './App.css';

function App() {
  // Browser mode selection - can be configured based on user preference
  const getBrowserMode = () => {
    // Check URL parameters for browser mode
    const params = new URLSearchParams(window.location.search);
    const mode = params.get('mode');
    
    // Check localStorage for saved preference
    const savedMode = localStorage.getItem('browserMode');
    
    return mode || savedMode || 'unified'; // Default to unified browser
  };

  const browserMode = getBrowserMode();

  const renderBrowserComponent = () => {
    switch (browserMode) {
      case 'advanced':
        return <MainBrowser />;
      case 'simplified':
        return <SimplifiedBrowser />;
      case 'unified':
      default:
        return <UnifiedBrowser />;
    }
  };

  return (
    <div className="App h-screen w-screen overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <DndProvider backend={HTML5Backend}>
        <UserContextProvider>
          <PerformanceContextProvider>
            <AccessibilityContextProvider>
              <ParallelFeaturesProvider>
                <AIContextProvider>
                  <BrowserContextProvider>
                    <Router>
                      <AuthWrapper>
                        <Routes>
                          {/* Main unified browser route */}
                          <Route path="/" element={<UnifiedBrowser />} />
                          
                          {/* Alternative browser modes */}
                          <Route path="/browser" element={<UnifiedBrowser />} />
                          <Route path="/browser/unified" element={<UnifiedBrowser />} />
                          <Route path="/browser/advanced" element={<MainBrowser />} />
                          <Route path="/browser/simplified" element={<SimplifiedBrowser />} />
                          
                          {/* Legacy routes for backward compatibility */}
                          <Route path="/advanced" element={<MainBrowser />} />
                          <Route path="/simple" element={<SimplifiedBrowser />} />
                        </Routes>
                      </AuthWrapper>
                    </Router>
                  </BrowserContextProvider>
                </AIContextProvider>
              </ParallelFeaturesProvider>
            </AccessibilityContextProvider>
          </PerformanceContextProvider>
        </UserContextProvider>
      </DndProvider>

      {/* Browser Mode Selector - Development Only */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed top-4 right-4 z-50">
          <div className="bg-black/80 text-white p-3 rounded-lg text-sm">
            <div className="mb-2 text-xs text-gray-300">Browser Mode:</div>
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  localStorage.setItem('browserMode', 'unified');
                  window.location.reload();
                }}
                className={`px-3 py-1 rounded text-xs transition-colors ${
                  browserMode === 'unified' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Unified
              </button>
              <button
                onClick={() => {
                  localStorage.setItem('browserMode', 'advanced');
                  window.location.reload();
                }}
                className={`px-3 py-1 rounded text-xs transition-colors ${
                  browserMode === 'advanced' 
                    ? 'bg-purple-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Advanced
              </button>
              <button
                onClick={() => {
                  localStorage.setItem('browserMode', 'simplified');
                  window.location.reload();
                }}
                className={`px-3 py-1 rounded text-xs transition-colors ${
                  browserMode === 'simplified' 
                    ? 'bg-green-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Simple
              </button>
            </div>
            <div className="text-xs text-gray-400 mt-2">
              Current: {browserMode}
            </div>
          </div>
        </div>
      )}

      {/* Global Loading Indicator */}
      <div id="global-loading" className="fixed inset-0 bg-slate-900 flex items-center justify-center z-50 opacity-0 pointer-events-none transition-opacity duration-300">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-white text-lg">Loading AI Browser...</p>
        </div>
      </div>

      {/* CSS Custom Properties */}
      <style jsx="true" global="true">{`
        :root {
          --browser-primary: #6366f1;
          --browser-secondary: #8b5cf6;
          --browser-accent: #06b6d4;
          --browser-bg: #0f172a;
          --browser-surface: #1e293b;
          --browser-border: #334155;
          --browser-text: #f8fafc;
          --browser-text-muted: #94a3b8;
        }

        .nav-btn {
          @apply p-2 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed;
        }

        .tab-item {
          transition: all 0.2s ease;
        }

        .tab-item:hover {
          transform: translateY(-1px);
        }

        .scrollbar-thin::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }

        .scrollbar-track-transparent::-webkit-scrollbar-track {
          background: transparent;
        }

        .scrollbar-thumb-gray-600::-webkit-scrollbar-thumb {
          background: rgba(75, 85, 99, 0.5);
          border-radius: 3px;
        }

        .scrollbar-thumb-gray-600::-webkit-scrollbar-thumb:hover {
          background: rgba(75, 85, 99, 0.8);
        }

        /* Enhanced focus styles for accessibility */
        *:focus-visible {
          outline: 2px solid var(--browser-primary);
          outline-offset: 2px;
        }

        /* Smooth transitions for all interactive elements */
        button, input, select, textarea {
          transition: all 0.2s ease;
        }

        /* Custom loading animation */
        @keyframes browser-pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }

        .browser-pulse {
          animation: browser-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
      `}</style>
    </div>
  );
}

export default App;