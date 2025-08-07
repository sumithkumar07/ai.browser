import React, { useEffect, useState } from 'react';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { useUser } from '../../contexts/UserContext';
import BubbleTabWorkspace from '../BubbleTab/BubbleTabWorkspace';
import AIAssistant from '../AIAssistant/AIAssistant';
import NavigationBar from '../Navigation/NavigationBar';
import { Plus } from 'lucide-react';

export default function MainBrowser() {
  const { currentSession, tabs, addTab } = useBrowser();
  const { isAssistantVisible, toggleAssistant } = useAI();
  const { user } = useUser();
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    // Initialize browser session
    const initializeBrowser = async () => {
      try {
        // Create initial session if none exists
        if (!currentSession) {
          // For now, create a mock session
          const mockSession = {
            id: 'session-1',
            user_id: user.id,
            name: 'Default Session',
            tabs: [
              {
                id: 'tab-1',
                url: 'https://example.com',
                title: 'Welcome to AI Browser',
                position_x: 200,
                position_y: 150,
                is_active: true
              }
            ],
            created_at: new Date().toISOString()
          };
          
          // Add initial tab
          addTab(mockSession.tabs[0]);
        }
      } catch (error) {
        console.error('Error initializing browser:', error);
      } finally {
        setIsInitializing(false);
      }
    };

    if (user) {
      initializeBrowser();
    }
  }, [user, currentSession, addTab]);

  const handleNewTab = () => {
    const newTab = {
      id: `tab-${Date.now()}`,
      url: 'about:blank',
      title: 'New Tab',
      position_x: Math.random() * 400 + 200,
      position_y: Math.random() * 300 + 150,
      is_active: false
    };
    addTab(newTab);
  };

  if (isInitializing) {
    return (
      <div className="flex items-center justify-center h-screen bg-ai-dark">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-primary mx-auto"></div>
          <p className="text-white mt-4">Initializing AI Browser...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="browser-container relative">
      {/* Navigation Bar */}
      <NavigationBar />
      
      {/* Bubble Tab Workspace */}
      <BubbleTabWorkspace />
      
      {/* AI Assistant */}
      {isAssistantVisible && <AIAssistant />}
      
      {/* Floating Action Button - New Tab */}
      <button
        onClick={handleNewTab}
        className="fab"
        title="New Tab"
      >
        <Plus size={28} />
      </button>
      
      {/* AI Assistant Toggle */}
      <button
        onClick={toggleAssistant}
        className="fixed bottom-30 right-100 w-16 h-16 rounded-full bg-gradient-to-r from-ai-secondary to-purple-600 border-none cursor-pointer flex items-center justify-center text-white text-2xl ai-pulse transition-all duration-300 hover:scale-110 z-150"
        title="Toggle AI Assistant"
      >
        🤖
      </button>

      {/* Welcome Message for First Time Users */}
      {tabs.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center max-w-2xl mx-auto px-6">
            <h1 className="text-6xl font-bold text-white mb-6">
              Welcome to the Future
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Your AI-powered browser with bubble tabs, intelligent automation, and advanced capabilities
            </p>
            <button
              onClick={handleNewTab}
              className="bg-gradient-to-r from-ai-primary to-ai-secondary text-white py-4 px-8 rounded-2xl font-semibold text-lg hover:opacity-90 transition-opacity"
            >
              Create Your First Tab
            </button>
          </div>
        </div>
      )}

      {/* User Mode Indicator */}
      <div className="fixed top-6 right-6 bg-gray-900/50 backdrop-blur-xl border border-gray-700 rounded-lg px-3 py-2 text-sm text-white">
        {user?.user_mode} mode
      </div>
    </div>
  );
}