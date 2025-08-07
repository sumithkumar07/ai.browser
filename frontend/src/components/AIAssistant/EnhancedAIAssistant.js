import React, { useState, useRef, useEffect } from 'react';
import { useAI } from '../../contexts/AIContext';
import { Send, Minimize2, Maximize2, Bot, Zap, FileText, Settings, TrendingUp, Brain, Sparkles, MessageSquare, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function EnhancedAIAssistant() {
  const { 
    isAssistantVisible,
    toggleAssistant,
    isAssistantCollapsed, 
    collapseAssistant, 
    chatMessages, 
    addChatMessage, 
    aiStatus,
    setAIStatus,
    clearChat 
  } = useAI();
  
  const [inputMessage, setInputMessage] = useState('');
  const [activeFeature, setActiveFeature] = useState('chat');
  const [isProcessing, setIsProcessing] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Load performance metrics
  useEffect(() => {
    loadPerformanceMetrics();
  }, []);

  const loadPerformanceMetrics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/performance-metrics`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
      
      if (response.ok) {
        const metrics = await response.json();
        setPerformanceMetrics(metrics);
      }
    } catch (error) {
      console.error('Could not load performance metrics:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isProcessing) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    addChatMessage(userMessage);
    setInputMessage('');
    setIsProcessing(true);
    setAIStatus('processing');

    try {
      // Use enhanced AI chat endpoint
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/enhanced-chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          message: inputMessage,
          context: { activeFeature }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response?.response || data.response || 'Sorry, I encountered an error processing your request.',
        timestamp: new Date(),
        cached: data.cached,
        suggestions: data.response?.suggestions || []
      };

      addChatMessage(aiMessage);
      
      // Set suggestions for quick actions
      if (data.response?.suggestions) {
        setSuggestions(data.response.suggestions);
      }

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Sorry, I\'m having trouble connecting right now. Please try again later.',
        timestamp: new Date(),
        error: true
      };
      addChatMessage(errorMessage);
    } finally {
      setIsProcessing(false);
      setAIStatus('idle');
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
    setSuggestions([]);
  };

  const handleSmartContentAnalysis = async (url) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/enhanced/smart-content-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          url: url,
          analysis_type: 'comprehensive'
        })
      });

      const data = await response.json();
      
      const analysisMessage = {
        id: Date.now(),
        type: 'ai',
        content: `📊 **Content Analysis Complete**\n\nURL: ${url}\n\n${JSON.stringify(data, null, 2)}`,
        timestamp: new Date(),
        special_type: 'analysis'
      };

      addChatMessage(analysisMessage);
      
    } catch (error) {
      console.error('Content analysis failed:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  if (!isAssistantVisible) return null;

  if (isAssistantCollapsed) {
    return (
      <motion.div 
        className="fixed bottom-6 right-6 z-50"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        <button
          onClick={() => collapseAssistant(false)}
          className="w-16 h-16 bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center text-white text-2xl shadow-2xl transition-all duration-300 hover:shadow-purple-500/25"
        >
          <Brain className="animate-pulse" size={24} />
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className="enhanced-ai-assistant fixed bottom-6 right-6 w-96 h-[600px] bg-gray-900/95 backdrop-blur-xl border border-gray-700/50 rounded-2xl shadow-2xl flex flex-col z-50 md:w-80 sm:w-full sm:bottom-0 sm:right-0 sm:rounded-none sm:h-screen"
      initial={{ opacity: 0, y: 100 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 100 }}
      transition={{ duration: 0.3 }}
    >
      {/* Enhanced Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700/50 bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-t-2xl">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center relative">
            <Brain className="text-white" size={20} />
            <motion.div
              className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 2 }}
            />
          </div>
          <div>
            <h3 className="text-white font-semibold flex items-center">
              ARIA <Sparkles className="ml-1 text-yellow-400" size={14} />
            </h3>
            <p className="text-gray-400 text-xs">
              {isProcessing ? 'Thinking...' : 'Enhanced AI Assistant'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {performanceMetrics && (
            <div className="text-xs text-green-400 flex items-center">
              <TrendingUp size={12} className="mr-1" />
              {performanceMetrics.cache_status?.entries || 0}
            </div>
          )}
          <button
            onClick={() => collapseAssistant(true)}
            className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
          >
            <Minimize2 size={16} />
          </button>
          <button
            onClick={toggleAssistant}
            className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-300 hover:text-white transition-colors sm:block"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Enhanced Feature Tabs */}
      <div className="flex border-b border-gray-700/50 bg-gray-800/30">
        {[
          { id: 'chat', icon: MessageSquare, label: 'Chat' },
          { id: 'automation', icon: Zap, label: 'Automate' },
          { id: 'analysis', icon: FileText, label: 'Analyze' },
          { id: 'settings', icon: Settings, label: 'Settings' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveFeature(tab.id)}
            className={`flex-1 px-2 py-3 text-xs font-medium transition-all duration-200 ${
              activeFeature === tab.id 
                ? 'text-ai-primary border-b-2 border-ai-primary bg-gray-800/50' 
                : 'text-gray-400 hover:text-white hover:bg-gray-800/30'
            }`}
          >
            <tab.icon size={14} className="inline mr-1" />
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Enhanced Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        <AnimatePresence>
          {chatMessages.length === 0 ? (
            <motion.div 
              className="text-center text-gray-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <Brain size={48} className="mx-auto mb-4 text-purple-400" />
              <p className="mb-2 font-medium">Hi! I'm ARIA, your enhanced AI assistant.</p>
              <div className="text-sm space-y-1">
                <p>🤖 <strong>Smart Automation</strong> - Form filling, e-commerce, booking</p>
                <p>📊 <strong>Content Analysis</strong> - Research, summarization, insights</p>
                <p>🎯 <strong>Tab Management</strong> - Organization, productivity</p>
                <p>⚡ <strong>Enhanced Performance</strong> - Caching, memory optimization</p>
              </div>
            </motion.div>
          ) : (
            chatMessages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-2xl relative ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-ai-primary to-purple-600 text-white ml-4'
                      : 'bg-gray-800/80 text-gray-100 mr-4 border border-gray-700/30'
                  }`}
                >
                  {message.type === 'ai' && (
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-purple-400 font-medium">ARIA</span>
                      {message.cached && (
                        <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
                          Cached
                        </span>
                      )}
                    </div>
                  )}
                  
                  <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                  
                  <p className="text-xs opacity-70 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                  
                  {/* Message suggestions */}
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {message.suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="block w-full text-left text-xs bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 px-2 py-1 rounded-lg transition-colors"
                        >
                          💡 {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
        
        {/* Processing indicator */}
        {isProcessing && (
          <motion.div 
            className="flex justify-start"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="bg-gray-800/80 text-gray-100 max-w-xs p-3 rounded-2xl mr-4 border border-gray-700/30">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <motion.div
                    className="w-2 h-2 bg-ai-primary rounded-full"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 0.8, delay: 0 }}
                  />
                  <motion.div
                    className="w-2 h-2 bg-ai-primary rounded-full"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 0.8, delay: 0.2 }}
                  />
                  <motion.div
                    className="w-2 h-2 bg-ai-primary rounded-full"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 0.8, delay: 0.4 }}
                  />
                </div>
                <span className="text-sm">ARIA is processing...</span>
              </div>
            </div>
          </motion.div>
        )}
        
        {/* Quick suggestions */}
        {suggestions.length > 0 && (
          <motion.div 
            className="space-y-2"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-xs text-gray-400 font-medium">Quick suggestions:</p>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="block w-full text-left text-sm bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 px-3 py-2 rounded-lg transition-colors border border-gray-700/30"
              >
                ✨ {suggestion}
              </button>
            ))}
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Input Area */}
      <div className="p-4 border-t border-gray-700/50 bg-gray-800/30">
        {activeFeature === 'analysis' && (
          <div className="mb-3">
            <input
              type="url"
              placeholder="Enter URL for smart analysis..."
              className="w-full bg-gray-800/50 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-ai-primary text-sm mb-2"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.target.value.trim()) {
                  handleSmartContentAnalysis(e.target.value.trim());
                  e.target.value = '';
                }
              }}
            />
          </div>
        )}
        
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder={
              activeFeature === 'automation' ? 'Describe automation task...' :
              activeFeature === 'analysis' ? 'Ask about content analysis...' :
              'Ask ARIA anything...'
            }
            className="flex-1 bg-gray-800/50 border border-gray-600 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-ai-primary text-sm transition-colors"
            disabled={isProcessing}
          />
          
          <motion.button
            type="submit"
            disabled={!inputMessage.trim() || isProcessing}
            className="w-12 h-12 bg-gradient-to-r from-ai-primary to-purple-600 hover:from-ai-primary/80 hover:to-purple-600/80 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed rounded-xl flex items-center justify-center text-white transition-all duration-200"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Send size={16} />
          </motion.button>
        </form>
        
        {chatMessages.length > 0 && (
          <div className="flex justify-between items-center mt-2">
            <button
              onClick={clearChat}
              className="text-xs text-gray-400 hover:text-gray-300 transition-colors"
            >
              Clear conversation
            </button>
            
            {performanceMetrics && (
              <div className="text-xs text-gray-500">
                Cache: {performanceMetrics.cache_status?.entries || 0} entries
              </div>
            )}
          </div>
        )}
      </div>

      {/* Feature-specific panels */}
      {activeFeature === 'settings' && (
        <motion.div
          className="absolute inset-0 bg-gray-900/95 backdrop-blur-xl rounded-2xl p-4 z-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-white font-semibold">AI Settings</h3>
            <button
              onClick={() => setActiveFeature('chat')}
              className="text-gray-400 hover:text-white"
            >
              <X size={20} />
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Response Style
              </label>
              <select className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white">
                <option>Balanced</option>
                <option>Detailed</option>
                <option>Concise</option>
                <option>Technical</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Auto-Analysis
              </label>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Enable smart content analysis</span>
                <input type="checkbox" className="rounded" />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Performance Mode
              </label>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Enable caching & optimization</span>
                <input type="checkbox" defaultChecked className="rounded" />
              </div>
            </div>
            
            {performanceMetrics && (
              <div className="mt-4 p-3 bg-gray-800/50 rounded-lg">
                <h4 className="text-sm font-medium text-white mb-2">Performance Metrics</h4>
                <div className="text-xs text-gray-400 space-y-1">
                  <p>Cache Entries: {performanceMetrics.cache_status?.entries || 0}</p>
                  <p>Cache Status: {performanceMetrics.cache_status?.enabled ? 'Enabled' : 'Disabled'}</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}