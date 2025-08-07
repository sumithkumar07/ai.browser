import React, { useState, useRef, useEffect } from 'react';
import { useAI } from '../../contexts/AIContext';
import { Send, Minimize2, Maximize2, Bot, Zap, FileText, Settings } from 'lucide-react';

export default function AIAssistant() {
  const { 
    isAssistantCollapsed, 
    collapseAssistant, 
    chatMessages, 
    addChatMessage, 
    aiStatus,
    setAIStatus,
    clearChat 
  } = useAI();
  
  const [inputMessage, setInputMessage] = useState('');
  const [activeFeature, setActiveFeature] = useState('chat'); // chat, automation, analysis
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || aiStatus === 'processing') return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    addChatMessage(userMessage);
    setInputMessage('');
    setAIStatus('processing');

    try {
      // Send to backend API
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/ai/chat`, {
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

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response || 'Sorry, I encountered an error processing your request.',
        timestamp: new Date()
      };

      addChatMessage(aiMessage);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Sorry, I\'m having trouble connecting right now. Please try again later.',
        timestamp: new Date()
      };
      addChatMessage(errorMessage);
    } finally {
      setAIStatus('idle');
    }
  };

  if (isAssistantCollapsed) {
    return (
      <div className="ai-assistant collapsed">
        <button
          onClick={() => collapseAssistant(false)}
          className="w-full h-full bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center text-white text-2xl hover:scale-110 transition-transform ai-pulse"
        >
          🤖
        </button>
      </div>
    );
  }

  return (
    <div className="ai-assistant">
      {/* Assistant Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center">
            <Bot className="text-white" size={20} />
          </div>
          <div>
            <h3 className="text-white font-semibold">AI Assistant</h3>
            <p className="text-gray-400 text-sm">Ready to help</p>
          </div>
        </div>
        
        <button
          onClick={() => collapseAssistant(true)}
          className="w-8 h-8 rounded bg-gray-700 hover:bg-gray-600 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
        >
          <Minimize2 size={16} />
        </button>
      </div>

      {/* Feature Tabs */}
      <div className="flex border-b border-gray-700">
        <button
          onClick={() => setActiveFeature('chat')}
          className={`flex-1 px-3 py-2 text-sm font-medium transition-colors ${
            activeFeature === 'chat' 
              ? 'text-ai-primary border-b-2 border-ai-primary bg-gray-800/50' 
              : 'text-gray-400 hover:text-white'
          }`}
        >
          <Bot size={16} className="inline mr-2" />
          Chat
        </button>
        
        <button
          onClick={() => setActiveFeature('automation')}
          className={`flex-1 px-3 py-2 text-sm font-medium transition-colors ${
            activeFeature === 'automation' 
              ? 'text-ai-primary border-b-2 border-ai-primary bg-gray-800/50' 
              : 'text-gray-400 hover:text-white'
          }`}
        >
          <Zap size={16} className="inline mr-2" />
          Automate
        </button>
        
        <button
          onClick={() => setActiveFeature('analysis')}
          className={`flex-1 px-3 py-2 text-sm font-medium transition-colors ${
            activeFeature === 'analysis' 
              ? 'text-ai-primary border-b-2 border-ai-primary bg-gray-800/50' 
              : 'text-gray-400 hover:text-white'
          }`}
        >
          <FileText size={16} className="inline mr-2" />
          Analyze
        </button>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatMessages.length === 0 ? (
          <div className="text-center text-gray-400">
            <Bot size={48} className="mx-auto mb-4 text-gray-600" />
            <p className="mb-2">Hi! I'm your AI assistant.</p>
            <p className="text-sm">I can help with:</p>
            <ul className="text-sm mt-2 space-y-1">
              <li>• Web automation tasks</li>
              <li>• Content analysis</li>
              <li>• Tab management</li>
              <li>• Productivity tips</li>
            </ul>
          </div>
        ) : (
          chatMessages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-ai-primary text-white ml-4'
                    : 'bg-gray-700 text-gray-100 mr-4'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}
        
        {aiStatus === 'processing' && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-100 max-w-xs p-3 rounded-lg mr-4">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-ai-primary"></div>
                <span className="text-sm">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700">
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder={`Ask me anything about ${activeFeature}...`}
            className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-ai-primary text-sm"
            disabled={aiStatus === 'processing'}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || aiStatus === 'processing'}
            className="w-10 h-10 bg-ai-primary hover:bg-ai-primary/80 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg flex items-center justify-center text-white transition-colors"
          >
            <Send size={16} />
          </button>
        </form>
        
        {chatMessages.length > 0 && (
          <button
            onClick={clearChat}
            className="mt-2 text-xs text-gray-400 hover:text-gray-300 transition-colors"
          >
            Clear conversation
          </button>
        )}
      </div>
    </div>
  );
}