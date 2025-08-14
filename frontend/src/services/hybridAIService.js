/**
 * 🚀 HYBRID AI SERVICE - Frontend API Client
 * Provides seamless integration with Neon AI + Fellou.ai hybrid capabilities
 * Preserves existing UI while adding advanced intelligence
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class HybridAIService {
  constructor() {
    this.axiosInstance = axios.create({
      baseURL: `${API_BASE_URL}/api/ai/hybrid`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth interceptor
    this.axiosInstance.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // =============================================================================
  // 🧠 NEON AI METHODS - CONTEXTUAL INTELLIGENCE
  // =============================================================================

  /**
   * 🧠 Enhanced chat with Neon AI contextual understanding
   */
  async neonChatEnhanced(message, pageContext = null, includePredictions = true) {
    try {
      const response = await this.axiosInstance.post('/neon-chat-enhanced', {
        message,
        page_context: pageContext,
        include_predictions: includePredictions
      });

      return {
        success: true,
        data: response.data,
        hybridFeatures: {
          neonAI: true,
          contextualAwareness: response.data.hybrid_features?.contextual_awareness || false,
          behavioralLearning: response.data.hybrid_features?.behavioral_learning || false,
          predictiveAssistance: response.data.hybrid_features?.predictive_suggestions?.length > 0 || false
        }
      };
    } catch (error) {
      console.error('Neon Chat Enhanced error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Neon Chat enhancement failed',
        fallbackToStandard: true
      };
    }
  }

  /**
   * 🛠️ Generate mini-apps with Neon Make
   */
  async generateApp(appRequest, appType = 'auto_detect', context = null) {
    try {
      const response = await this.axiosInstance.post('/neon-make-app-generator', {
        app_request: appRequest,
        app_type: appType,
        context,
        generate_code: true
      });

      return {
        success: true,
        data: response.data,
        appGenerated: true,
        neonMakeActive: true
      };
    } catch (error) {
      console.error('Neon Make app generation error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'App generation failed'
      };
    }
  }

  // =============================================================================
  // 🚀 FELLOU.AI METHODS - ADVANCED WORKFLOWS
  // =============================================================================

  /**
   * 🎭 Create multi-step workflow with Deep Action
   */
  async createDeepActionWorkflow(taskDescription, context = null, executionMode = 'plan_only') {
    try {
      const response = await this.axiosInstance.post('/deep-action-orchestrator', {
        task_description: taskDescription,
        context,
        execution_mode: executionMode
      });

      return {
        success: true,
        data: response.data,
        workflowCreated: true,
        fellouAIActive: true
      };
    } catch (error) {
      console.error('Deep Action workflow error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Workflow creation failed'
      };
    }
  }

  /**
   * ⚡ Execute Deep Action workflow step-by-step
   */
  async executeWorkflowStep(workflowId, stepIndex = 0, executionParams = null) {
    try {
      const response = await this.axiosInstance.post('/deep-action-execute', {
        workflow_id: workflowId,
        step_index: stepIndex,
        execution_params: executionParams
      });

      return {
        success: true,
        data: response.data,
        stepExecuted: true
      };
    } catch (error) {
      console.error('Workflow execution error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Workflow execution failed'
      };
    }
  }

  /**
   * 🔍 Conduct automated research with Deep Search
   */
  async deepSearchResearch(researchQuery, searchDepth = 'comprehensive', includeVisualReport = true) {
    try {
      const response = await this.axiosInstance.post('/deep-search-intelligence', {
        research_query: researchQuery,
        search_depth: searchDepth,
        include_visual_report: includeVisualReport
      });

      return {
        success: true,
        data: response.data,
        researchCompleted: true,
        fellouAIActive: true
      };
    } catch (error) {
      console.error('Deep Search research error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Research failed'
      };
    }
  }

  // =============================================================================
  // 🧠 AGENTIC MEMORY METHODS - BEHAVIORAL LEARNING
  // =============================================================================

  /**
   * 🧠 Update Agentic Memory with user interaction
   */
  async updateAgenticMemory(interactionData, learningMode = 'adaptive') {
    try {
      const response = await this.axiosInstance.post('/agentic-memory-learning', {
        interaction_data: interactionData,
        learning_mode: learningMode
      });

      return {
        success: true,
        data: response.data,
        learningUpdated: true,
        agenticMemoryActive: true
      };
    } catch (error) {
      console.error('Agentic Memory update error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Learning update failed'
      };
    }
  }

  /**
   * 💡 Get personalized insights from behavioral learning
   */
  async getPersonalizedInsights(userId) {
    try {
      const response = await this.axiosInstance.get(`/agentic-memory-insights/${userId}`);

      return {
        success: true,
        data: response.data,
        insightsAvailable: true
      };
    } catch (error) {
      console.error('Personalized insights error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Insights retrieval failed'
      };
    }
  }

  // =============================================================================
  // 🎯 HYBRID SYSTEM MANAGEMENT
  // =============================================================================

  /**
   * 📊 Get comprehensive hybrid system status
   */
  async getHybridSystemStatus() {
    try {
      const response = await this.axiosInstance.get('/hybrid-system-status');

      return {
        success: true,
        data: response.data,
        systemStatus: 'operational'
      };
    } catch (error) {
      console.error('Hybrid system status error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Status check failed'
      };
    }
  }

  /**
   * 🚀 Get hybrid AI capabilities and features
   */
  async getHybridCapabilities() {
    try {
      const response = await this.axiosInstance.get('/hybrid-capabilities');

      return {
        success: true,
        data: response.data,
        capabilitiesLoaded: true
      };
    } catch (error) {
      console.error('Hybrid capabilities error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Capabilities check failed'
      };
    }
  }

  /**
   * 🎯 Comprehensive hybrid content analysis
   */
  async hybridContentAnalysis(content, analysisTypes = ['contextual', 'predictive', 'behavioral'], includeRecommendations = true) {
    try {
      const response = await this.axiosInstance.post('/hybrid-analysis', {
        content,
        analysis_types: analysisTypes,
        include_recommendations: includeRecommendations
      });

      return {
        success: true,
        data: response.data,
        analysisCompleted: true,
        hybridActive: true
      };
    } catch (error) {
      console.error('Hybrid analysis error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Hybrid analysis failed'
      };
    }
  }

  /**
   * 📊 Get hybrid performance metrics
   */
  async getHybridMetrics() {
    try {
      const response = await this.axiosInstance.get('/hybrid-metrics');

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Hybrid metrics error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Metrics retrieval failed'
      };
    }
  }

  // =============================================================================
  // 🔧 UTILITY METHODS
  // =============================================================================

  /**
   * 📱 Get current page context for Neon Chat
   */
  getCurrentPageContext() {
    if (typeof window === 'undefined') return null;

    return {
      url: window.location.href,
      title: document.title,
      content: document.body.innerText?.slice(0, 5000) || '',
      metadata: {
        timestamp: new Date().toISOString(),
        viewport: {
          width: window.innerWidth,
          height: window.innerHeight
        }
      }
    };
  }

  /**
   * 🎯 Auto-detect interaction type for Agentic Memory
   */
  createInteractionData(type, content, outcome = 'completed', context = null) {
    return {
      type,
      content,
      outcome,
      context: context || this.getCurrentPageContext(),
      timestamp: new Date().toISOString(),
      session_id: this.getSessionId()
    };
  }

  /**
   * 🔐 Get current session ID
   */
  getSessionId() {
    let sessionId = localStorage.getItem('hybridAISessionId');
    if (!sessionId) {
      sessionId = `hybrid_session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('hybridAISessionId', sessionId);
    }
    return sessionId;
  }

  /**
   * 🧠 Enhanced chat method that integrates with existing ARIA AI
   */
  async enhancedChat(message, options = {}) {
    const {
      includeContext = true,
      includePredictions = true,
      learningMode = 'adaptive'
    } = options;

    try {
      // Get page context for Neon AI
      const pageContext = includeContext ? this.getCurrentPageContext() : null;

      // Enhanced chat with Neon AI
      const chatResult = await this.neonChatEnhanced(message, pageContext, includePredictions);

      // Update Agentic Memory for learning
      if (chatResult.success) {
        const interactionData = this.createInteractionData('hybrid_chat', message, 'completed', pageContext);
        await this.updateAgenticMemory(interactionData, learningMode);
      }

      return chatResult;

    } catch (error) {
      console.error('Enhanced chat error:', error);
      return {
        success: false,
        error: 'Enhanced chat failed',
        fallbackToStandard: true
      };
    }
  }

  /**
   * 🎨 Auto-detect and suggest app generation opportunities
   */
  detectAppOpportunities(message) {
    const opportunities = [];
    const messageLower = message.toLowerCase();

    // Calculator opportunity
    if (/calculate|math|compute|formula/i.test(message)) {
      opportunities.push({
        type: 'calculator',
        confidence: 0.8,
        suggestion: 'Generate a calculator app for your computation needs'
      });
    }

    // Todo/Task manager opportunity
    if (/todo|task|list|organize|plan/i.test(message)) {
      opportunities.push({
        type: 'todo_manager',
        confidence: 0.75,
        suggestion: 'Create a task management app to organize your plans'
      });
    }

    // Data visualization opportunity
    if (/chart|graph|visualize|data|plot/i.test(message)) {
      opportunities.push({
        type: 'data_visualizer',
        confidence: 0.85,
        suggestion: 'Build a data visualization app for your analysis'
      });
    }

    // Note-taking opportunity
    if (/note|write|document|memo/i.test(message)) {
      opportunities.push({
        type: 'note_taker',
        confidence: 0.7,
        suggestion: 'Generate a note-taking app for documentation'
      });
    }

    // Timer/productivity opportunity
    if (/time|timer|track|pomodoro|productivity/i.test(message)) {
      opportunities.push({
        type: 'timer_tracker',
        confidence: 0.8,
        suggestion: 'Create a time tracking app for productivity'
      });
    }

    return opportunities;
  }

  /**
   * 🔍 Auto-detect research opportunities
   */
  detectResearchOpportunities(message) {
    const opportunities = [];
    const messageLower = message.toLowerCase();

    if (/research|analyze|study|investigate|explore|compare/i.test(message)) {
      opportunities.push({
        type: 'deep_search',
        confidence: 0.9,
        suggestion: 'Run Deep Search automated research on this topic'
      });
    }

    if (/competitor|market|industry|trends/i.test(message)) {
      opportunities.push({
        type: 'competitive_analysis',
        confidence: 0.85,
        suggestion: 'Conduct competitive analysis and market research'
      });
    }

    return opportunities;
  }

  /**
   * ⚡ Auto-detect workflow opportunities
   */
  detectWorkflowOpportunities(message) {
    const opportunities = [];
    const messageLower = message.toLowerCase();

    if (/automate|workflow|process|steps|sequence/i.test(message)) {
      opportunities.push({
        type: 'deep_action',
        confidence: 0.8,
        suggestion: 'Create automated workflow with Deep Action orchestration'
      });
    }

    if (/schedule|book|fill.*form|submit|apply/i.test(message)) {
      opportunities.push({
        type: 'task_automation',
        confidence: 0.75,
        suggestion: 'Set up task automation for repetitive actions'
      });
    }

    return opportunities;
  }

  /**
   * 🎯 Comprehensive opportunity detection
   */
  detectAllOpportunities(message) {
    return {
      apps: this.detectAppOpportunities(message),
      research: this.detectResearchOpportunities(message),
      workflows: this.detectWorkflowOpportunities(message)
    };
  }
}

// Export singleton instance
export default new HybridAIService();