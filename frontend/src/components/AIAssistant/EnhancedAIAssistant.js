import React, { useState, useRef, useEffect } from 'react';
import { useAI } from '../../contexts/AIContext';
import { 
  Send, Minimize2, Maximize2, Bot, Zap, FileText, Settings, 
  Brain, Eye, Mic, PenTool, BarChart3, BookOpen, TrendingUp, 
  Network, Lightbulb, Palette, Code, Globe, Users, Target,
  Cpu, Factory, Briefcase, GraduationCap, Heart, Scale,
  Search, Workflow, Memory, ArrowRight, Sparkles, Layers,
  MessageCircle, PlayCircle, PauseCircle
} from 'lucide-react';

export default function EnhancedAIAssistant() {
  const { 
    isAssistantCollapsed, 
    collapseAssistant, 
    chatMessages, 
    addChatMessage, 
    aiStatus,
    setAIStatus,
    clearChat,
    hybridFeatures,
    aiCapabilities
  } = useAI();
  
  const [inputMessage, setInputMessage] = useState('');
  const [activeTab, setActiveTab] = useState('chat');
  const [selectedIndustry, setSelectedIndustry] = useState('technology');
  const [analysisType, setAnalysisType] = useState('comprehensive');
  const [contentInput, setContentInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const callAPI = async (endpoint, data) => {
    try {
      setIsProcessing(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai/enhanced/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      setLastResult(result);
      
      // Add result to chat
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: JSON.stringify(result, null, 2),
        timestamp: new Date(),
        feature: endpoint
      });
      
      return result;
    } catch (error) {
      console.error(`API call failed for ${endpoint}:`, error);
      addChatMessage({
        id: Date.now(),
        type: 'ai',
        content: `Error calling ${endpoint}: ${error.message}`,
        timestamp: new Date(),
        feature: endpoint
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleEnhancedChat = async (e) => {
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
      const result = await callAPI('enhanced-chat', {
        message: inputMessage,
        context: { activeFeature: activeTab }
      });
    } catch (error) {
      console.error('Enhanced chat failed:', error);
    } finally {
      setAIStatus('idle');
    }
  };

  const handleAdvancedFeature = async (endpoint, data) => {
    await callAPI(endpoint, data);
  };

  if (isAssistantCollapsed) {
    return (
      <div className="ai-assistant collapsed">
        <button
          onClick={() => collapseAssistant(false)}
          className="w-full h-full bg-gradient-to-r from-ai-secondary to-purple-600 rounded-full flex items-center justify-center text-white text-2xl hover:scale-110 transition-transform ai-pulse"
        >
          🧠
        </button>
      </div>
    );
  }

  return (
    <div className="ai-assistant bg-gray-900/95 backdrop-blur-lg border border-gray-700/50 rounded-2xl shadow-2xl">
      {/* Enhanced Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700/50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
            <Brain className="text-white" size={20} />
          </div>
          <div>
            <h3 className="text-white font-semibold">ARIA Enhanced AI</h3>
            <p className="text-gray-400 text-sm">
              {hybridFeatures?.hybridIntelligence ? 'Hybrid Intelligence Active' : 'Enhanced Assistant'}
            </p>
          </div>
        </div>
        
        <button
          onClick={() => collapseAssistant(true)}
          className="w-8 h-8 rounded bg-gray-700 hover:bg-gray-600 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
        >
          <Minimize2 size={16} />
        </button>
      </div>

      {/* Enhanced Feature Tabs */}
      <div className="flex flex-wrap border-b border-gray-700/50">
        {[
          { id: 'chat', icon: MessageCircle, label: 'Chat' },
          { id: 'analysis', icon: Brain, label: 'Analysis' },
          { id: 'creative', icon: Palette, label: 'Creative' },
          { id: 'research', icon: BookOpen, label: 'Research' },
          { id: 'hybrid', icon: Sparkles, label: 'Hybrid AI' },
          { id: 'industry', icon: Factory, label: 'Industry' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 min-w-16 px-2 py-2 text-xs font-medium transition-colors ${
              activeTab === tab.id 
                ? 'text-purple-400 border-b-2 border-purple-400 bg-gray-800/50' 
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <tab.icon size={14} className="inline mr-1" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Dynamic Content Based on Active Tab */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96">
        {activeTab === 'chat' && (
          <div className="space-y-4">
            {chatMessages.length === 0 ? (
              <div className="text-center text-gray-400">
                <Bot size={48} className="mx-auto mb-4 text-gray-600" />
                <p className="mb-2">Hi! I'm your Enhanced ARIA AI.</p>
                <p className="text-sm">Now with {aiCapabilities?.neonAI ? 'Neon AI' : ''} {aiCapabilities?.fellouAI ? '+ Fellou.ai' : ''} hybrid intelligence!</p>
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-gray-800/50 p-2 rounded">🧠 Advanced Analysis</div>
                  <div className="bg-gray-800/50 p-2 rounded">🎨 Creative Generation</div>
                  <div className="bg-gray-800/50 p-2 rounded">📊 Industry Intelligence</div>
                  <div className="bg-gray-800/50 p-2 rounded">🔍 Research & Trends</div>
                </div>
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
                        ? 'bg-purple-500 text-white ml-4'
                        : 'bg-gray-700 text-gray-100 mr-4'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                      {message.feature && <span className="ml-2 text-purple-300">({message.feature})</span>}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-4">
            <h4 className="text-white font-medium flex items-center">
              <Brain className="mr-2" size={16} />
              Advanced AI Analysis
            </h4>
            
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => handleAdvancedFeature('real-time-collaborative-analysis', {
                  content: contentInput || 'Analyze current webpage',
                  analysis_goals: ['comprehensive', 'actionable']
                })}
                disabled={isProcessing}
                className="bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 p-3 rounded-lg text-sm text-blue-300"
              >
                <Users size={16} className="mb-1" />
                Collaborative Analysis
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('visual-content-analysis', {
                  image_description: contentInput || 'Current webpage visuals',
                  ocr_text: 'Extract text from images'
                })}
                disabled={isProcessing}
                className="bg-green-600/20 hover:bg-green-600/30 border border-green-500/30 p-3 rounded-lg text-sm text-green-300"
              >
                <Eye size={16} className="mb-1" />
                Visual Analysis
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('audio-intelligence-analysis', {
                  transcript: contentInput || 'Analyze audio content',
                  audio_metadata: { type: 'speech', duration: 60 }
                })}
                disabled={isProcessing}
                className="bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 p-3 rounded-lg text-sm text-purple-300"
              >
                <Mic size={16} className="mb-1" />
                Audio Intelligence
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('design-intelligence-analysis', {
                  design_description: contentInput || 'Current page design',
                  design_type: 'web'
                })}
                disabled={isProcessing}
                className="bg-pink-600/20 hover:bg-pink-600/30 border border-pink-500/30 p-3 rounded-lg text-sm text-pink-300"
              >
                <PenTool size={16} className="mb-1" />
                Design Intelligence
              </button>
            </div>
            
            <textarea
              value={contentInput}
              onChange={(e) => setContentInput(e.target.value)}
              placeholder="Enter content to analyze..."
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
            />
          </div>
        )}

        {activeTab === 'creative' && (
          <div className="space-y-4">
            <h4 className="text-white font-medium flex items-center">
              <Palette className="mr-2" size={16} />
              Creative AI Generation
            </h4>
            
            <div className="grid grid-cols-1 gap-2">
              <button
                onClick={() => handleAdvancedFeature('creative-content-generation', {
                  content_type: 'blog_post',
                  brief: contentInput || 'Create engaging content',
                  brand_context: { tone: 'professional', style: 'modern' }
                })}
                disabled={isProcessing}
                className="bg-gradient-to-r from-purple-600/20 to-pink-600/20 hover:from-purple-600/30 hover:to-pink-600/30 border border-purple-500/30 p-3 rounded-lg text-sm text-purple-300"
              >
                <PenTool size={16} className="mb-1" />
                Creative Content Generation
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('data-visualization-generation', {
                  data_description: contentInput || 'Create charts from data',
                  visualization_goals: ['clarity', 'engagement']
                })}
                disabled={isProcessing}
                className="bg-gradient-to-r from-green-600/20 to-blue-600/20 hover:from-green-600/30 hover:to-blue-600/30 border border-green-500/30 p-3 rounded-lg text-sm text-green-300"
              >
                <BarChart3 size={16} className="mb-1" />
                Data Visualization
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('code-generation', {
                  task_description: contentInput || 'Generate useful code',
                  language: 'javascript',
                  context: { framework: 'react' }
                })}
                disabled={isProcessing}
                className="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 hover:from-blue-600/30 hover:to-cyan-600/30 border border-blue-500/30 p-3 rounded-lg text-sm text-blue-300"
              >
                <Code size={16} className="mb-1" />
                Intelligent Code Generation
              </button>
            </div>
            
            <textarea
              value={contentInput}
              onChange={(e) => setContentInput(e.target.value)}
              placeholder="Describe what you want to create..."
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
            />
          </div>
        )}

        {activeTab === 'research' && (
          <div className="space-y-4">
            <h4 className="text-white font-medium flex items-center">
              <BookOpen className="mr-2" size={16} />
              Research & Intelligence
            </h4>
            
            <div className="grid grid-cols-1 gap-2">
              <button
                onClick={() => handleAdvancedFeature('academic-research-assistance', {
                  research_topic: contentInput || 'AI and automation trends',
                  research_goals: ['comprehensive_analysis', 'citations']
                })}
                disabled={isProcessing}
                className="bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 p-3 rounded-lg text-sm text-blue-300"
              >
                <GraduationCap size={16} className="mb-1" />
                Academic Research
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('trend-detection-analysis', {
                  data_sources: [contentInput || 'Current webpage'],
                  analysis_period: '2024-2025'
                })}
                disabled={isProcessing}
                className="bg-green-600/20 hover:bg-green-600/30 border border-green-500/30 p-3 rounded-lg text-sm text-green-300"
              >
                <TrendingUp size={16} className="mb-1" />
                Trend Detection
              </button>
              
              <button
                onClick={() => handleAdvancedFeature('knowledge-graph-building', {
                  content: contentInput || 'Build knowledge connections',
                  domain: 'technology'
                })}
                disabled={isProcessing}
                className="bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 p-3 rounded-lg text-sm text-purple-300"
              >
                <Network size={16} className="mb-1" />
                Knowledge Graph
              </button>
            </div>
            
            <input
              value={contentInput}
              onChange={(e) => setContentInput(e.target.value)}
              placeholder="Enter research topic..."
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
            />
          </div>
        )}

        {activeTab === 'hybrid' && (
          <div className="space-y-4">
            <h4 className="text-white font-medium flex items-center">
              <Sparkles className="mr-2" size={16} />
              Hybrid AI (Neon + Fellou.ai)
            </h4>
            
            {hybridFeatures?.hybridIntelligence ? (
              <div className="grid grid-cols-1 gap-2">
                <button
                  onClick={() => callAPI('../../hybrid/neon-chat-enhanced', {
                    message: contentInput || 'Analyze current context',
                    page_context: { url: window.location.href }
                  })}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 hover:from-blue-500/30 hover:to-purple-500/30 border border-blue-400/30 p-3 rounded-lg text-sm text-blue-300"
                >
                  <Brain size={16} className="mb-1" />
                  Neon Chat Enhanced
                </button>
                
                <button
                  onClick={() => callAPI('../../hybrid/deep-search-professional', {
                    research_query: contentInput || 'Professional research',
                    report_format: 'comprehensive'
                  })}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-green-500/20 to-teal-500/20 hover:from-green-500/30 hover:to-teal-500/30 border border-green-400/30 p-3 rounded-lg text-sm text-green-300"
                >
                  <Search size={16} className="mb-1" />
                  Deep Search Pro
                </button>
                
                <button
                  onClick={() => callAPI('../../hybrid/controllable-workflow-builder', {
                    workflow_description: contentInput || 'Build visual workflow',
                    visual_mode: true
                  })}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 hover:from-purple-500/30 hover:to-pink-500/30 border border-purple-400/30 p-3 rounded-lg text-sm text-purple-300"
                >
                  <Workflow size={16} className="mb-1" />
                  Workflow Builder
                </button>
                
                <button
                  onClick={() => callAPI('../../hybrid/agentic-memory-learning', {
                    interaction_data: { content: contentInput, action: 'analyze' },
                    learning_mode: 'adaptive'
                  })}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 border border-cyan-400/30 p-3 rounded-lg text-sm text-cyan-300"
                >
                  <Memory size={16} className="mb-1" />
                  Agentic Memory
                </button>
              </div>
            ) : (
              <div className="text-center text-gray-400 p-4">
                <Sparkles size={32} className="mx-auto mb-2 text-gray-600" />
                <p className="text-sm">Hybrid AI features initializing...</p>
              </div>
            )}
            
            <input
              value={contentInput}
              onChange={(e) => setContentInput(e.target.value)}
              placeholder="Enter task or query..."
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
            />
          </div>
        )}

        {activeTab === 'industry' && (
          <div className="space-y-4">
            <h4 className="text-white font-medium flex items-center">
              <Factory className="mr-2" size={16} />
              Industry-Specific AI
            </h4>
            
            <select
              value={selectedIndustry}
              onChange={(e) => setSelectedIndustry(e.target.value)}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-purple-400 text-sm"
            >
              <option value="finance">💰 Finance</option>
              <option value="healthcare">🏥 Healthcare</option>
              <option value="legal">⚖️ Legal</option>
              <option value="education">🎓 Education</option>
              <option value="technology">💻 Technology</option>
              <option value="retail">🛍️ Retail</option>
            </select>
            
            <button
              onClick={() => handleAdvancedFeature('industry-specific-analysis', {
                content: contentInput || 'Analyze from industry perspective',
                industry: selectedIndustry
              })}
              disabled={isProcessing}
              className="w-full bg-gradient-to-r from-amber-600/20 to-orange-600/20 hover:from-amber-600/30 hover:to-orange-600/30 border border-amber-500/30 p-3 rounded-lg text-sm text-amber-300"
            >
              <Target size={16} className="mb-1" />
              Industry Analysis ({selectedIndustry})
            </button>
            
            <textarea
              value={contentInput}
              onChange={(e) => setContentInput(e.target.value)}
              placeholder={`Enter content to analyze from ${selectedIndustry} perspective...`}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
            />
          </div>
        )}
        
        {aiStatus === 'processing' && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-100 max-w-xs p-3 rounded-lg mr-4">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-400"></div>
                <span className="text-sm">Advanced AI processing...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Input Area */}
      <div className="p-4 border-t border-gray-700/50">
        {activeTab === 'chat' && (
          <form onSubmit={handleEnhancedChat} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask me anything with enhanced AI..."
              className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 text-sm"
              disabled={aiStatus === 'processing'}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || aiStatus === 'processing'}
              className="w-10 h-10 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg flex items-center justify-center text-white transition-colors"
            >
              <Send size={16} />
            </button>
          </form>
        )}
        
        {isProcessing && (
          <div className="flex items-center justify-center mt-2">
            <div className="animate-pulse text-purple-400 text-sm">
              Processing with advanced AI capabilities...
            </div>
          </div>
        )}
        
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