import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, X, Sparkles, MessageSquare, Lightbulb, TrendingUp,
  FileText, Eye, Zap, BarChart3, Globe, Clock, Star, ChevronRight,
  Copy, ExternalLink, Bookmark, Share2, Download, RefreshCw,
  ChevronDown, Search, Filter, Settings
} from 'lucide-react';

export default function AIInsightsPanel({ 
  pageAnalysis, 
  insights, 
  contextualActions,
  currentUrl,
  currentTab,
  onActionExecute,
  onClose 
}) {
  const [activeSection, setActiveSection] = useState('summary');
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showInsightFilters, setShowInsightFilters] = useState(false);
  const [selectedInsightTypes, setSelectedInsightTypes] = useState(['all']);

  const chatInputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Initialize chat with page context
  useEffect(() => {
    if (pageAnalysis && chatMessages.length === 0) {
      setChatMessages([
        {
          id: 'welcome',
          type: 'ai',
          content: `I've analyzed "${currentTab?.title || 'this page'}" and I'm ready to help. You can ask me about the content, get summaries, or explore related topics.`,
          timestamp: new Date(),
          context: { url: currentUrl, title: currentTab?.title }
        }
      ]);
    }
  }, [pageAnalysis, currentUrl, currentTab?.title]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatMessages]);

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: chatInput,
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setIsAnalyzing(true);

    try {
      // Simulate AI response with context about current page
      setTimeout(() => {
        const aiResponse = {
          id: (Date.now() + 1).toString(),
          type: 'ai',
          content: generateContextualResponse(chatInput, pageAnalysis),
          timestamp: new Date(),
          context: { 
            url: currentUrl, 
            title: currentTab?.title,
            analysis: pageAnalysis 
          }
        };
        
        setChatMessages(prev => [...prev, aiResponse]);
        setIsAnalyzing(false);
      }, 1000);
    } catch (error) {
      console.error('Chat error:', error);
      setIsAnalyzing(false);
    }
  };

  const generateContextualResponse = (query, analysis) => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('summar')) {
      return analysis?.summary || "This page discusses various topics. I can provide more specific information if you ask about particular sections.";
    }
    
    if (lowerQuery.includes('key point') || lowerQuery.includes('main point')) {
      return analysis?.keyPoints?.join('\n• ') || "The main points include several important aspects of the topic discussed.";
    }
    
    if (lowerQuery.includes('question') || lowerQuery.includes('what')) {
      return "Based on my analysis, this content covers important information. What specific aspect would you like to know more about?";
    }
    
    return `I understand you're asking about "${query}". Based on the current page content, I can help you explore this topic further. What specific information are you looking for?`;
  };

  const executeContextualAction = async (action) => {
    setIsAnalyzing(true);
    
    try {
      await onActionExecute(action);
      
      // Add confirmation message to chat
      const confirmMessage = {
        id: Date.now().toString(),
        type: 'ai',
        content: `I've executed: ${action.title}. ${action.description}`,
        timestamp: new Date(),
        action: action
      };
      
      setChatMessages(prev => [...prev, confirmMessage]);
    } catch (error) {
      console.error('Action execution failed:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderInsights = () => {
    if (!insights || insights.length === 0) {
      return (
        <div className="text-center py-8 text-gray-400">
          <Eye size={32} className="mx-auto mb-3 opacity-50" />
          <p>No insights available for current page</p>
        </div>
      );
    }

    const filteredInsights = selectedInsightTypes.includes('all') 
      ? insights 
      : insights.filter(insight => selectedInsightTypes.includes(insight.type));

    return (
      <div className="space-y-3">
        {filteredInsights.map((insight, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-gray-800/50 rounded-lg p-4 border border-gray-700/30"
          >
            <div className="flex items-start space-x-3">
              <div className={`p-2 rounded-lg ${getInsightColorClass(insight.type)}`}>
                {getInsightIcon(insight.type)}
              </div>
              <div className="flex-1">
                <h4 className="text-white font-medium mb-1">{insight.title}</h4>
                <p className="text-gray-300 text-sm mb-2">{insight.content}</p>
                {insight.confidence && (
                  <div className="flex items-center space-x-2 text-xs text-gray-400">
                    <span>Confidence:</span>
                    <div className="w-16 h-1 bg-gray-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-blue-500 transition-all duration-300"
                        style={{ width: `${insight.confidence}%` }}
                      />
                    </div>
                    <span>{insight.confidence}%</span>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  const getInsightIcon = (type) => {
    const icons = {
      summary: <FileText size={16} />,
      trend: <TrendingUp size={16} />,
      fact: <Lightbulb size={16} />,
      statistic: <BarChart3 size={16} />,
      recommendation: <Star size={16} />
    };
    return icons[type] || <Brain size={16} />;
  };

  const getInsightColorClass = (type) => {
    const classes = {
      summary: 'bg-blue-600/20 text-blue-300',
      trend: 'bg-green-600/20 text-green-300',
      fact: 'bg-yellow-600/20 text-yellow-300',
      statistic: 'bg-purple-600/20 text-purple-300',
      recommendation: 'bg-red-600/20 text-red-300'
    };
    return classes[type] || 'bg-gray-600/20 text-gray-300';
  };

  const renderContextualActions = () => {
    if (!contextualActions || contextualActions.length === 0) return null;

    return (
      <div className="space-y-2">
        {contextualActions.map((action, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => executeContextualAction(action)}
            className="w-full text-left p-3 bg-gradient-to-r from-purple-600/10 to-blue-600/10 border border-purple-500/20 rounded-lg hover:from-purple-600/20 hover:to-blue-600/20 transition-all duration-200 group"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-600/20 rounded-lg">
                  <Zap size={14} className="text-purple-300" />
                </div>
                <div>
                  <div className="text-white font-medium text-sm">{action.title}</div>
                  <div className="text-gray-400 text-xs">{action.description}</div>
                </div>
              </div>
              <ChevronRight size={14} className="text-gray-400 group-hover:text-white transition-colors" />
            </div>
          </motion.button>
        ))}
      </div>
    );
  };

  const sections = [
    { id: 'summary', label: 'Summary', icon: FileText },
    { id: 'insights', label: 'Insights', icon: Lightbulb },
    { id: 'actions', label: 'Actions', icon: Zap },
    { id: 'chat', label: 'Chat', icon: MessageSquare }
  ];

  return (
    <div className="ai-insights-panel h-full bg-gray-900/95 backdrop-blur-sm flex flex-col">
      
      {/* Header */}
      <div className="border-b border-gray-700/50 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <Brain size={16} className="text-white" />
            </div>
            <h3 className="text-white font-semibold">AI Insights</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white transition-colors"
          >
            <X size={16} />
          </button>
        </div>

        {/* Current Page Info */}
        {currentTab && (
          <div className="bg-gray-800/50 rounded-lg p-3 mb-3">
            <div className="flex items-center space-x-2 mb-1">
              <Globe size={12} className="text-blue-400" />
              <span className="text-xs text-gray-400">Analyzing</span>
            </div>
            <div className="text-white text-sm font-medium truncate" title={currentTab.title}>
              {currentTab.title}
            </div>
            <div className="text-xs text-gray-500 truncate" title={currentUrl}>
              {currentUrl}
            </div>
          </div>
        )}

        {/* Section Tabs */}
        <div className="flex space-x-1 bg-gray-800/30 rounded-lg p-1">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs transition-colors ${
                activeSection === section.id
                  ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                  : 'text-gray-400 hover:text-gray-300 hover:bg-gray-700/30'
              }`}
            >
              <section.icon size={12} />
              <span>{section.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full p-4 overflow-y-auto">
          
          {/* Summary Section */}
          {activeSection === 'summary' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-medium">Page Summary</h4>
                <button className="p-1 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white">
                  <RefreshCw size={14} />
                </button>
              </div>
              
              {pageAnalysis?.summary ? (
                <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700/30">
                  <p className="text-gray-300 leading-relaxed">{pageAnalysis.summary}</p>
                  
                  {pageAnalysis.keyPoints && (
                    <div className="mt-4 pt-4 border-t border-gray-700/30">
                      <h5 className="text-white font-medium mb-2">Key Points</h5>
                      <ul className="space-y-1">
                        {pageAnalysis.keyPoints.map((point, index) => (
                          <li key={index} className="text-gray-300 text-sm flex items-start space-x-2">
                            <span className="w-1 h-1 bg-blue-400 rounded-full mt-2 flex-shrink-0"></span>
                            <span>{point}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  <FileText size={32} className="mx-auto mb-3 opacity-50" />
                  <p>Analyzing page content...</p>
                  <div className="w-16 h-1 bg-gray-700 rounded-full mx-auto mt-2 overflow-hidden">
                    <div className="h-full bg-blue-500 animate-pulse"></div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Insights Section */}
          {activeSection === 'insights' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-medium">AI Insights</h4>
                <button
                  onClick={() => setShowInsightFilters(!showInsightFilters)}
                  className="p-1 hover:bg-gray-700/50 rounded text-gray-400 hover:text-white"
                >
                  <Filter size={14} />
                </button>
              </div>

              {/* Insight Filters */}
              <AnimatePresence>
                {showInsightFilters && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="bg-gray-800/30 rounded-lg p-3"
                  >
                    <div className="flex flex-wrap gap-2">
                      {['all', 'summary', 'trend', 'fact', 'statistic'].map((type) => (
                        <button
                          key={type}
                          onClick={() => {
                            setSelectedInsightTypes(prev =>
                              type === 'all' ? ['all'] :
                              prev.includes('all') ? [type] :
                              prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
                            );
                          }}
                          className={`px-2 py-1 rounded text-xs transition-colors ${
                            selectedInsightTypes.includes(type)
                              ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                              : 'bg-gray-700/50 text-gray-400 hover:text-gray-300'
                          }`}
                        >
                          {type.charAt(0).toUpperCase() + type.slice(1)}
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {renderInsights()}
            </div>
          )}

          {/* Actions Section */}
          {activeSection === 'actions' && (
            <div className="space-y-4">
              <h4 className="text-white font-medium">Smart Actions</h4>
              {renderContextualActions()}
              
              {/* Quick Actions */}
              <div className="pt-4 border-t border-gray-700/30">
                <h5 className="text-gray-400 text-sm mb-3">Quick Actions</h5>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { icon: Bookmark, label: 'Bookmark', action: 'bookmark' },
                    { icon: Share2, label: 'Share', action: 'share' },
                    { icon: Copy, label: 'Copy URL', action: 'copy' },
                    { icon: ExternalLink, label: 'Open External', action: 'external' }
                  ].map((action) => (
                    <button
                      key={action.action}
                      className="flex items-center space-x-2 p-2 bg-gray-800/30 rounded-lg hover:bg-gray-700/50 transition-colors text-sm text-gray-300 hover:text-white"
                    >
                      <action.icon size={14} />
                      <span>{action.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Chat Section */}
          {activeSection === 'chat' && (
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-white font-medium">AI Chat</h4>
                <span className="text-xs text-gray-400">Context-aware</span>
              </div>
              
              {/* Chat Messages */}
              <div 
                ref={chatContainerRef}
                className="flex-1 space-y-3 overflow-y-auto mb-4 max-h-64"
              >
                {chatMessages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[85%] p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-blue-600/20 text-blue-100 border border-blue-500/30'
                        : 'bg-gray-800/50 text-gray-300 border border-gray-700/30'
                    }`}>
                      <p className="text-sm whitespace-pre-line">{message.content}</p>
                      <div className="text-xs text-gray-400 mt-1">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                ))}
                
                {isAnalyzing && (
                  <div className="flex justify-start">
                    <div className="bg-gray-800/50 p-3 rounded-lg border border-gray-700/30">
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-1 h-1 bg-purple-400 rounded-full animate-bounce"></div>
                          <div className="w-1 h-1 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-1 h-1 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span className="text-sm text-gray-400">AI is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Chat Input */}
              <form onSubmit={handleChatSubmit} className="flex space-x-2">
                <input
                  ref={chatInputRef}
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask about this page..."
                  className="flex-1 px-3 py-2 bg-gray-800/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 text-sm focus:outline-none focus:border-blue-500/50"
                  disabled={isAnalyzing}
                />
                <button
                  type="submit"
                  disabled={!chatInput.trim() || isAnalyzing}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600/50 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                >
                  <MessageSquare size={14} />
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}