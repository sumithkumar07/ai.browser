import React, { useState, useRef, useEffect } from 'react';
import { useAI } from '../../contexts/AIContext';
import { Send, Minimize2, Maximize2, Bot, Zap, FileText, Settings, TrendingUp, Brain, Sparkles, MessageSquare, X, Mic, MicOff, Copy, ThumbsUp, ThumbsDown, RotateCcw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api`;

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
  const [isListening, setIsListening] = useState(false);
  const [responseRatings, setResponseRatings] = useState({});
  const [assistantPersonality, setAssistantPersonality] = useState('friendly');
  const [showQuickActions, setShowQuickActions] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Load performance metrics with enhanced error handling
  useEffect(() => {
    loadPerformanceMetrics();
    const interval = setInterval(loadPerformanceMetrics, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadPerformanceMetrics = async () => {
    try {
      const response = await fetch(`${API_BASE}/ai/enhanced/performance-metrics`, {
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
    const originalMessage = inputMessage;
    setInputMessage('');
    setIsProcessing(true);
    setAIStatus('processing');

    try {
      const response = await fetch(`${API_BASE}/ai/enhanced/enhanced-chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          message: originalMessage,
          context: { 
            activeFeature,
            assistantPersonality,
            timestamp: new Date().toISOString()
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response?.response || data.response || 'I apologize, but I encountered an issue processing your request. Let me try to help you in a different way!',
        timestamp: new Date(),
        cached: data.cached,
        suggestions: data.response?.suggestions || [],
        intelligence_level: data.response?.intelligence_level || 'enhanced',
        user_intent: data.response?.user_intent || 'conversational',
        model_used: data.response?.model_used || 'llama3-70b-8192'
      };

      addChatMessage(aiMessage);
      
      // Set enhanced suggestions
      if (data.response?.suggestions && Array.isArray(data.response.suggestions)) {
        setSuggestions(data.response.suggestions);
      }

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: '🤖 I apologize for the interruption! It seems there was a connection issue. I\'m still here to help - please try asking your question again, or let me know if you\'d like to explore different features while we reconnect!',
        timestamp: new Date(),
        error: true,
        suggestions: ['Try your question again', 'Explore automation features', 'Check content analysis', 'Browse browser settings']
      };
      addChatMessage(errorMessage);
      setSuggestions(errorMessage.suggestions);
    } finally {
      setIsProcessing(false);
      setAIStatus('idle');
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
    setSuggestions([]);
    document.querySelector('input[type="text"]')?.focus();
  };

  const handleVoiceInput = async () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🎤 Voice input is not supported in your browser. Please try typing your message instead!',
        timestamp: new Date()
      });
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInputMessage(transcript);
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🎤 I had trouble hearing you. Please try speaking clearly or use the text input!',
        timestamp: new Date()
      });
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const handleCopyMessage = (content) => {
    navigator.clipboard.writeText(content).then(() => {
      // Could add a toast notification here
    });
  };

  const handleRateResponse = (messageId, rating) => {
    setResponseRatings(prev => ({
      ...prev,
      [messageId]: rating
    }));
  };

  const handleRetryLastMessage = () => {
    const lastUserMessage = [...chatMessages].reverse().find(msg => msg.type === 'user');
    if (lastUserMessage) {
      setInputMessage(lastUserMessage.content);
    }
  };

  const handleSmartContentAnalysis = async (url) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${API_BASE}/ai/enhanced/smart-content-analysis`, {
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
        content: `📊 **Enhanced Content Analysis Complete**\n\n🔗 **URL**: ${url}\n\n${typeof data.enhanced_analysis === 'object' ? JSON.stringify(data.enhanced_analysis, null, 2) : data.enhanced_analysis || 'Analysis completed successfully!'}`,
        timestamp: new Date(),
        special_type: 'analysis',
        analysis_data: data
      };

      addChatMessage(analysisMessage);
      
    } catch (error) {
      console.error('Content analysis failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '📊 I encountered an issue analyzing that content. Please check the URL and try again, or let me help you with a different task!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const quickActions = [
    { icon: Zap, label: 'Automate Task', action: () => setActiveFeature('automation') },
    { icon: FileText, label: 'Analyze Content', action: () => setActiveFeature('analysis') },
    { icon: Brain, label: 'AI Suggestions', action: () => setSuggestions(['Analyze current tab', 'Organize my tabs', 'Set up automation', 'Help me be productive']) },
    { icon: Settings, label: 'Customize AI', action: () => setActiveFeature('settings') }
  ];

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
          className="w-16 h-16 bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center text-white text-2xl shadow-2xl transition-all duration-300 hover:shadow-purple-500/25 animate-ai-pulse"
          aria-label="Expand AI Assistant"
        >
          <Brain className="animate-pulse" size={24} />
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className="enhanced-ai-assistant fixed bottom-6 right-6 w-96 h-[600px] glass-strong rounded-2xl shadow-2xl flex flex-col z-50 md:w-80 sm:w-full sm:bottom-0 sm:right-0 sm:rounded-none sm:h-screen"
      initial={{ opacity: 0, y: 100, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 100, scale: 0.9 }}
      transition={{ duration: 0.4, type: "spring", stiffness: 120 }}
    >
      {/* Enhanced Header with Status */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700/50 bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-t-2xl">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center relative">
            <Brain className="text-white" size={20} />
            <motion.div
              className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full"
              animate={{ scale: [1, 1.3, 1] }}
              transition={{ repeat: Infinity, duration: 2 }}
            />
          </div>
          <div>
            <h3 className="text-white font-semibold flex items-center">
              ARIA <Sparkles className="ml-1 text-yellow-400" size={14} />
            </h3>
            <p className="text-gray-400 text-xs">
              {isProcessing ? 'Processing...' : 'Enhanced AI Assistant'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {performanceMetrics && (
            <div className="text-xs text-green-400 flex items-center" title="Cache Performance">
              <TrendingUp size={12} className="mr-1" />
              {performanceMetrics.cache_status?.entries || 0}
            </div>
          )}
          
          <button
            onClick={() => setShowQuickActions(!showQuickActions)}
            className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-purple-600/50 flex items-center justify-center text-gray-300 hover:text-white transition-all duration-200"
            title="Quick Actions"
          >
            <Zap size={16} />
          </button>
          
          <button
            onClick={() => collapseAssistant(true)}
            className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
            title="Minimize"
          >
            <Minimize2 size={16} />
          </button>
          
          <button
            onClick={toggleAssistant}
            className="w-8 h-8 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 flex items-center justify-center text-gray-300 hover:text-white transition-colors sm:block"
            title="Close"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Quick Actions Panel */}
      <AnimatePresence>
        {showQuickActions && (
          <motion.div
            className="absolute top-16 left-4 right-4 bg-gray-900/95 backdrop-blur-xl border border-gray-700/50 rounded-xl p-4 z-10"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <h4 className="text-white font-medium mb-3 text-sm">Quick Actions</h4>
            <div className="grid grid-cols-2 gap-2">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  onClick={() => {
                    action.action();
                    setShowQuickActions(false);
                  }}
                  className="flex items-center p-2 bg-gray-800/50 hover:bg-gray-700/50 rounded-lg text-white text-xs transition-colors"
                >
                  <action.icon size={14} className="mr-2" />
                  {action.label}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

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
        <AnimatePresence mode="popLayout">
          {chatMessages.length === 0 ? (
            <motion.div 
              className="text-center text-gray-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <Brain size={48} className="mx-auto mb-4 text-purple-400" />
              <p className="mb-3 font-medium text-white">Hi! I'm ARIA, your enhanced AI assistant! 🚀</p>
              <div className="text-sm space-y-2 bg-gray-800/30 rounded-lg p-4">
                <p>🤖 <strong>Smart Automation</strong> - Form filling, e-commerce, booking</p>
                <p>📊 <strong>Content Analysis</strong> - Research, summarization, insights</p>
                <p>🎯 <strong>Tab Management</strong> - Organization, productivity</p>
                <p>⚡ <strong>Enhanced Performance</strong> - Caching, memory optimization</p>
                <p>🎤 <strong>Voice Input</strong> - Talk to me naturally</p>
              </div>
              
              <div className="mt-4 space-y-2">
                {['Analyze current webpage', 'Help me automate a task', 'Organize my browser tabs', 'What can you do?'].map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => setInputMessage(suggestion)}
                    className="block w-full text-left text-xs bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 px-3 py-2 rounded-lg transition-colors"
                  >
                    💡 {suggestion}
                  </button>
                ))}
              </div>
            </motion.div>
          ) : (
            chatMessages.map((message) => (
              <motion.div
                key={message.id}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-2xl relative group ${
                    message.type === 'user'
                      ? 'bg-gradient-to-r from-ai-primary to-purple-600 text-white ml-4'
                      : 'glass text-gray-100 mr-4'
                  }`}
                >
                  {message.type === 'ai' && (
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <span className="text-xs text-purple-400 font-medium">ARIA</span>
                        {message.intelligence_level === 'enhanced' && (
                          <Sparkles className="ml-1 text-yellow-400" size={12} />
                        )}
                        {message.model_used && (
                          <span className="ml-2 text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-full">
                            {message.model_used.includes('70b') ? 'Pro' : 'Fast'}
                          </span>
                        )}
                      </div>
                      {message.cached && (
                        <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
                          Cached
                        </span>
                      )}
                    </div>
                  )}
                  
                  <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                  
                  <div className="flex items-center justify-between mt-2">
                    <p className="text-xs opacity-70">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                    
                    {/* Message Actions */}
                    <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => handleCopyMessage(message.content)}
                        className="text-xs text-gray-400 hover:text-white p-1 rounded"
                        title="Copy message"
                      >
                        <Copy size={12} />
                      </button>
                      
                      {message.type === 'ai' && (
                        <>
                          <button
                            onClick={() => handleRateResponse(message.id, 'up')}
                            className={`text-xs p-1 rounded ${
                              responseRatings[message.id] === 'up' 
                                ? 'text-green-400' 
                                : 'text-gray-400 hover:text-green-400'
                            }`}
                            title="Good response"
                          >
                            <ThumbsUp size={12} />
                          </button>
                          
                          <button
                            onClick={() => handleRateResponse(message.id, 'down')}
                            className={`text-xs p-1 rounded ${
                              responseRatings[message.id] === 'down' 
                                ? 'text-red-400' 
                                : 'text-gray-400 hover:text-red-400'
                            }`}
                            title="Needs improvement"
                          >
                            <ThumbsDown size={12} />
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                  
                  {/* Message suggestions */}
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-3 space-y-1">
                      <p className="text-xs text-gray-400 font-medium">Follow up:</p>
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
        
        {/* Enhanced Processing indicator */}
        {isProcessing && (
          <motion.div 
            className="flex justify-start"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="glass text-gray-100 max-w-xs p-3 rounded-2xl mr-4">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  {[0, 0.2, 0.4].map((delay, index) => (
                    <motion.div
                      key={index}
                      className="w-2 h-2 bg-ai-primary rounded-full"
                      animate={{ scale: [1, 1.5, 1] }}
                      transition={{ repeat: Infinity, duration: 1, delay }}
                    />
                  ))}
                </div>
                <span className="text-sm">ARIA is thinking...</span>
              </div>
            </div>
          </motion.div>
        )}
        
        {/* Enhanced suggestions */}
        {suggestions.length > 0 && !isProcessing && (
          <motion.div 
            className="space-y-2"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-xs text-gray-400 font-medium">💡 Suggestions for you:</p>
            {suggestions.map((suggestion, index) => (
              <motion.button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="block w-full text-left text-sm glass hover:bg-gray-700/50 text-gray-300 px-3 py-2 rounded-lg transition-all duration-200 hover:scale-102"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                ✨ {suggestion}
              </motion.button>
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
              placeholder="Enter URL for enhanced analysis..."
              className="w-full input-primary text-sm mb-2"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.target.value.trim()) {
                  handleSmartContentAnalysis(e.target.value.trim());
                  e.target.value = '';
                }
              }}
            />
            <p className="text-xs text-gray-400">Press Enter to analyze any webpage instantly</p>
          </div>
        )}
        
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={
                activeFeature === 'automation' ? 'Describe what you want to automate...' :
                activeFeature === 'analysis' ? 'Ask about content analysis...' :
                'Ask ARIA anything...'
              }
              className="w-full input-primary text-sm pr-10"
              disabled={isProcessing}
            />
            
            {/* Voice Input Button */}
            <button
              type="button"
              onClick={handleVoiceInput}
              className={`absolute right-2 top-1/2 transform -translate-y-1/2 w-6 h-6 rounded-full flex items-center justify-center transition-all duration-200 ${
                isListening 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : 'bg-gray-600 text-gray-300 hover:bg-purple-600 hover:text-white'
              }`}
              title={isListening ? 'Stop listening' : 'Voice input'}
            >
              {isListening ? <MicOff size={12} /> : <Mic size={12} />}
            </button>
          </div>
          
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
        
        {/* Enhanced Footer Actions */}
        <div className="flex justify-between items-center mt-3">
          <div className="flex items-center space-x-2">
            {chatMessages.length > 0 && (
              <button
                onClick={clearChat}
                className="text-xs text-gray-400 hover:text-gray-300 transition-colors flex items-center"
              >
                <RotateCcw size={12} className="mr-1" />
                Clear
              </button>
            )}
            
            <button
              onClick={handleRetryLastMessage}
              className="text-xs text-gray-400 hover:text-gray-300 transition-colors flex items-center"
              title="Retry last message"
            >
              <RotateCcw size={12} className="mr-1" />
              Retry
            </button>
          </div>
          
          {performanceMetrics && (
            <div className="text-xs text-gray-500 flex items-center">
              <TrendingUp size={10} className="mr-1" />
              Enhanced Mode: {performanceMetrics.cache_status?.entries || 0} cached
            </div>
          )}
        </div>
      </div>

      {/* Enhanced Settings Panel */}
      {activeFeature === 'settings' && (
        <motion.div
          className="absolute inset-0 glass-strong rounded-2xl p-4 z-10"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-white font-semibold">🤖 AI Settings</h3>
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
                Assistant Personality
              </label>
              <select 
                className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                value={assistantPersonality}
                onChange={(e) => setAssistantPersonality(e.target.value)}
              >
                <option value="friendly">Friendly & Conversational</option>
                <option value="professional">Professional & Direct</option>
                <option value="creative">Creative & Innovative</option>
                <option value="technical">Technical & Detailed</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Response Style
              </label>
              <select className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white">
                <option>Balanced & Helpful</option>
                <option>Detailed & Comprehensive</option>
                <option>Concise & Efficient</option>
                <option>Step-by-step Guidance</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Enhanced Features
              </label>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Voice Input</span>
                  <input type="checkbox" defaultChecked className="rounded" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Smart Suggestions</span>
                  <input type="checkbox" defaultChecked className="rounded" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Performance Caching</span>
                  <input type="checkbox" defaultChecked className="rounded" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Context Memory</span>
                  <input type="checkbox" defaultChecked className="rounded" />
                </div>
              </div>
            </div>
            
            {performanceMetrics && (
              <div className="mt-4 p-3 glass rounded-lg">
                <h4 className="text-sm font-medium text-white mb-2 flex items-center">
                  <TrendingUp className="mr-2" size={16} />
                  Performance Metrics
                </h4>
                <div className="text-xs text-gray-400 space-y-1">
                  <p>💾 Cache Entries: {performanceMetrics.cache_status?.entries || 0}</p>
                  <p>⚡ Cache Status: {performanceMetrics.cache_status?.enabled ? '✅ Enabled' : '❌ Disabled'}</p>
                  <p>🧠 Intelligence: Enhanced Mode Active</p>
                  <p>🚀 Model: Llama3-70B (Primary)</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}