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
      // Use enhanced hybrid AI chat endpoint
      const response = await fetch(`${API_BASE}/ai/hybrid/neon-chat-enhanced`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          message: originalMessage,
          page_context: {
            url: window.location.href,
            content: document.body.innerText?.substring(0, 2000) // First 2000 chars for context
          },
          include_predictions: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response || 'I apologize, but I encountered an issue processing your request. Let me try to help you in a different way!',
        timestamp: new Date(),
        cached: data.cached,
        suggestions: data.enhanced_hybrid_features?.enhanced_suggestions || [],
        intelligence_level: data.hybrid_intelligence_level || 'enhanced',
        user_intent: data.enhanced_hybrid_features?.user_intent || 'conversational',
        hybrid_features: data.enhanced_hybrid_features || {},
        neon_ai_enhanced: data.neon_ai_enhanced || false,
        fellou_ai_enhanced: data.fellou_ai_enhanced || false
      };

      addChatMessage(aiMessage);
      
      // Set enhanced suggestions from hybrid AI
      if (data.enhanced_hybrid_features?.enhanced_suggestions && Array.isArray(data.enhanced_hybrid_features.enhanced_suggestions)) {
        setSuggestions(data.enhanced_hybrid_features.enhanced_suggestions);
      }

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: '🤖 I apologize for the interruption! It seems there was a connection issue. I\'m still here to help with my enhanced hybrid AI capabilities - please try asking your question again!',
        timestamp: new Date(),
        error: true,
        suggestions: ['Try hybrid AI chat again', 'Enable Neon Focus mode', 'Create professional workflow', 'Generate research report', 'Build custom app']
      };
      addChatMessage(errorMessage);
      setSuggestions(errorMessage.suggestions);
    } finally {
      setIsProcessing(false);
      setAIStatus('idle');
    }
  };

  const handleSuggestionClick = (suggestion) => {
    // Handle hybrid AI suggestions intelligently
    const suggestionLower = suggestion.toLowerCase();
    
    if (suggestionLower.includes('focus') || suggestionLower.includes('distraction')) {
      handleNeonFocusMode();
    } else if (suggestionLower.includes('research') || suggestionLower.includes('report')) {
      handleProfessionalResearch(suggestion);
    } else if (suggestionLower.includes('workflow') || suggestionLower.includes('automat')) {
      handleWorkflowBuilder(suggestion);
    } else if (suggestionLower.includes('app') || suggestionLower.includes('create') || suggestionLower.includes('build')) {
      handleProfessionalAppGeneration(suggestion);
    } else if (suggestionLower.includes('analy') || suggestionLower.includes('intelligen')) {
      handleSmartContentAnalysis(window.location.href);
    } else if (suggestionLower.includes('slack') || suggestionLower.includes('notion') || suggestionLower.includes('google') || suggestionLower.includes('microsoft')) {
      // Handle cross-platform integration suggestions
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: `🌐 **Cross-Platform Integration Ready**\n\nI can help you connect with external platforms:\n\n✅ **Available Integrations:**\n- 📱 Slack (messages, channels, files)\n- 📝 Notion (pages, databases, updates)\n- 📊 Google Workspace (docs, sheets, email)\n- 💼 Microsoft 365 (docs, email, meetings)\n\nLet me know which platform you'd like to integrate with!`,
        timestamp: new Date(),
        special_type: 'integration_ready',
        suggestions: ['Set up Slack integration', 'Connect to Notion', 'Link Google Workspace', 'Integrate Microsoft 365']
      });
      setSuggestions(['Set up Slack integration', 'Connect to Notion', 'Link Google Workspace', 'Integrate Microsoft 365']);
    } else {
      // Default behavior for regular suggestions
      setInputMessage(suggestion);
      setSuggestions([]);
      document.querySelector('input[type="text"]')?.focus();
    }
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
      
      // Use enhanced Neon Intelligence for real-time analysis
      const response = await fetch(`${API_BASE}/ai/hybrid/neon-intelligence`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          url: url || window.location.href,
          analysis_depth: 'comprehensive'
        })
      });

      const data = await response.json();
      
      const analysisMessage = {
        id: Date.now(),
        type: 'ai',
        content: `🧠 **Enhanced Neon Intelligence Analysis Complete**\n\n🔗 **URL**: ${url || window.location.href}\n\n${typeof data.intelligence_data === 'object' ? JSON.stringify(data.intelligence_data, null, 2) : data.intelligence_data || 'Advanced real-time analysis completed successfully!'}`,
        timestamp: new Date(),
        special_type: 'neon_intelligence',
        analysis_data: data,
        neon_ai_enhanced: true
      };

      addChatMessage(analysisMessage);
      
    } catch (error) {
      console.error('Neon Intelligence analysis failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🧠 I encountered an issue with the enhanced analysis. Let me help you with a different approach or try the basic content analysis!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNeonFocusMode = async () => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${API_BASE}/ai/hybrid/neon-focus-mode`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          url: window.location.href,
          focus_type: 'reading'
        })
      });

      const data = await response.json();
      
      const focusMessage = {
        id: Date.now(),
        type: 'ai',
        content: `🔍 **Neon Focus Mode Activated**\n\nI've analyzed the current page for distraction-free reading. Focus session is ready with AI-powered content optimization!\n\n✨ **Focus Features:**\n- Distraction filtering active\n- Content optimization applied\n- Reading flow enhanced\n- Smart highlights enabled`,
        timestamp: new Date(),
        special_type: 'neon_focus',
        focus_data: data,
        neon_ai_enhanced: true,
        suggestions: ['Apply focus optimizations', 'Adjust reading settings', 'Generate content summary', 'Create reading outline']
      };

      addChatMessage(focusMessage);
      setSuggestions(focusMessage.suggestions);
      
    } catch (error) {
      console.error('Neon Focus mode failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🔍 Focus mode setup encountered an issue. I can still help you organize your reading experience in other ways!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleProfessionalResearch = async (query) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${API_BASE}/ai/hybrid/deep-search-professional`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          research_query: query || 'Current page topic analysis',
          report_format: 'comprehensive',
          export_format: 'html'
        })
      });

      const data = await response.json();
      
      const researchMessage = {
        id: Date.now(),
        type: 'ai',
        content: `📊 **Professional Deep Search Report Generated**\n\n🔍 **Research Query**: ${query || 'Current page analysis'}\n\n✅ **Professional Report Ready:**\n- Multi-source research compilation\n- Visual charts and infographics\n- Executive summary with insights\n- Export formats: HTML, PDF, PowerPoint, Excel\n\n📈 The comprehensive report includes market analysis, competitive insights, and actionable recommendations!`,
        timestamp: new Date(),
        special_type: 'deep_research',
        research_data: data,
        fellou_ai_enhanced: true,
        suggestions: ['View full report', 'Export to PDF', 'Create follow-up research', 'Share insights', 'Generate presentation']
      };

      addChatMessage(researchMessage);
      setSuggestions(researchMessage.suggestions);
      
    } catch (error) {
      console.error('Professional research failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '📊 Professional research encountered an issue. I can help you with basic research and analysis instead!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleWorkflowBuilder = async (description) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${API_BASE}/ai/hybrid/controllable-workflow-builder`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          workflow_description: description || 'Create a productivity workflow for current task',
          visual_mode: true
        })
      });

      const data = await response.json();
      
      const workflowMessage = {
        id: Date.now(),
        type: 'ai',
        content: `🎯 **Visual Workflow Builder Ready**\n\n🛠️ **Workflow**: ${description || 'Productivity workflow'}\n\n✨ **Features Available:**\n- Drag-and-drop visual interface\n- Node-based workflow design\n- Conditional logic and branches\n- Real-time execution monitoring\n- Cross-platform integrations\n\n🚀 Your visual workflow is designed and ready for execution!`,
        timestamp: new Date(),
        special_type: 'workflow_builder',
        workflow_data: data,
        fellou_ai_enhanced: true,
        suggestions: ['Open workflow builder', 'Execute workflow', 'Edit workflow steps', 'Share workflow', 'Create workflow template']
      };

      addChatMessage(workflowMessage);
      setSuggestions(workflowMessage.suggestions);
      
    } catch (error) {
      console.error('Workflow builder failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🎯 Workflow builder setup encountered an issue. I can help you create simpler automation sequences!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleProfessionalAppGeneration = async (appRequest) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch(`${API_BASE}/ai/hybrid/neon-make-professional`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          app_request: appRequest || 'Create a productivity dashboard app',
          template_type: 'auto_detect',
          advanced_features: true
        })
      });

      const data = await response.json();
      
      const appMessage = {
        id: Date.now(),
        type: 'ai',
        content: `🛠️ **Professional App Generated**\n\n📱 **App**: ${appRequest || 'Productivity dashboard'}\n\n✨ **Professional Features:**\n- Modern responsive design with PWA capabilities\n- Advanced JavaScript with ES6+ features\n- Dark/light theme support\n- Data persistence and offline mode\n- Professional UI/UX with accessibility\n- Analytics and performance monitoring\n\n🚀 Your professional-grade app is ready for deployment!`,
        timestamp: new Date(),
        special_type: 'professional_app',
        app_data: data,
        neon_ai_enhanced: true,
        suggestions: ['Open app in new tab', 'Download app code', 'Customize app features', 'Deploy app', 'Create another app']
      };

      addChatMessage(appMessage);
      setSuggestions(appMessage.suggestions);
      
    } catch (error) {
      console.error('Professional app generation failed:', error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: '🛠️ Professional app generation encountered an issue. I can help you create simpler apps or tools!',
        timestamp: new Date(),
        error: true
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const quickActions = [
    {
      icon: Brain, 
      label: 'Neon Intelligence', 
      description: 'Real-time page analysis',
      action: () => handleSmartContentAnalysis(window.location.href),
      color: 'from-blue-500 to-purple-600'
    },
    {
      icon: Sparkles, 
      label: 'Focus Mode', 
      description: 'Distraction-free reading',
      action: () => handleNeonFocusMode(),
      color: 'from-purple-500 to-pink-600'
    },
    {
      icon: FileText, 
      label: 'Research Report', 
      description: 'Professional Deep Search',
      action: () => handleProfessionalResearch(),
      color: 'from-green-500 to-blue-600'
    },
    {
      icon: Zap, 
      label: 'Workflow Builder', 
      description: 'Visual automation',
      action: () => handleWorkflowBuilder(),
      color: 'from-orange-500 to-red-600'
    },
    {
      icon: Settings, 
      label: 'Create Pro App', 
      description: 'Neon Make generator',
      action: () => handleProfessionalAppGeneration(),
      color: 'from-indigo-500 to-purple-600'
    },
    {
      icon: TrendingUp, 
      label: 'Cross-Platform', 
      description: 'Connect external tools',
      action: () => setSuggestions(['Connect to Slack', 'Integrate with Notion', 'Sync with Google Workspace', 'Link Microsoft 365']),
      color: 'from-teal-500 to-green-600'
    }
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
              
              {/* 🚀 HYBRID AI CAPABILITIES SHOWCASE */}
              <div className="text-sm space-y-2 bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-lg p-4 border border-purple-500/20">
                <p className="text-purple-300 font-medium mb-3">✨ Hybrid AI Capabilities (Neon + Fellou.ai)</p>
                <p>🧠 <strong>Neon Chat</strong> - Contextual webpage understanding</p>
                <p>🔍 <strong>Neon Focus</strong> - Distraction-free reading mode</p>
                <p>🛠️ <strong>Neon Make</strong> - Professional app generation</p>
                <p>🎭 <strong>Deep Action</strong> - Multi-step workflow orchestration</p>
                <p>📊 <strong>Deep Search</strong> - Professional research reports</p>
                <p>🧠 <strong>Agentic Memory</strong> - Behavioral learning</p>
                <p>🌐 <strong>Cross-Platform</strong> - Slack, Notion, Google integration</p>
                <p>⚡ <strong>Enhanced Performance</strong> - Caching, memory optimization</p>
                <p>🎤 <strong>Voice Input</strong> - Talk to me naturally</p>
              </div>
              
              {/* 🎯 ENHANCED HYBRID SUGGESTIONS */}
              <div className="mt-4 space-y-2">
                <p className="text-xs text-gray-400 font-medium mb-2">🚀 Try these hybrid AI features:</p>
                {[
                  'Activate Neon Focus mode for this page',
                  'Create professional research report',
                  'Generate a workflow for my tasks',
                  'Build a custom app for my needs',
                  'Analyze this webpage with AI intelligence',
                  'Connect to Slack or Notion'
                ].map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="block w-full text-left text-xs bg-gradient-to-r from-purple-500/20 to-blue-500/20 hover:from-purple-500/30 hover:to-blue-500/30 text-purple-300 px-3 py-2 rounded-lg transition-all duration-200 border border-purple-500/10 hover:border-purple-500/30"
                  >
                    ✨ {suggestion}
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