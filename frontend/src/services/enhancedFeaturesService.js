/**
 * Enhanced Features Service - API integration for all new parallel features
 * Minimal integration with existing frontend - works through API calls only
 */

import axios from 'axios';

const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class EnhancedFeaturesService {
  constructor() {
    this.apiClient = axios.create({
      baseURL: `${API_BASE}/api/enhanced-features`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Add request interceptor for authentication
    this.apiClient.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // ===== NAVIGATION FEATURES =====
  
  async aiPoweredNavigation(query, userId = 'anonymous', context = {}) {
    try {
      const response = await this.apiClient.post('/navigation/ai-powered', {
        query,
        user_id: userId,
        context
      });
      return response.data;
    } catch (error) {
      console.error('AI Navigation error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async crossSiteIntelligence(currentUrl, userContext = {}) {
    try {
      const response = await this.apiClient.post('/navigation/cross-site-intelligence', {
        current_url: currentUrl,
        user_context: userContext
      });
      return response.data;
    } catch (error) {
      console.error('Cross-site intelligence error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async smartBookmarking(url, pageContent, userId = 'anonymous') {
    try {
      const response = await this.apiClient.post('/navigation/smart-bookmarking', {
        url,
        page_content: pageContent,
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Smart bookmarking error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async contextualActions(url, selectedText, pageContext = {}) {
    try {
      const response = await this.apiClient.post('/navigation/contextual-actions', {
        url,
        selected_text: selectedText,
        page_context: pageContext
      });
      return response.data;
    } catch (error) {
      console.error('Contextual actions error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== PRODUCTIVITY FEATURES =====

  async oneClickActions(pageUrl, pageContent, userContext = {}) {
    try {
      const response = await this.apiClient.post('/productivity/one-click-actions', {
        page_url: pageUrl,
        page_content: pageContent,
        user_context: userContext
      });
      return response.data;
    } catch (error) {
      console.error('One-click actions error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async smartSuggestions(pageUrl, pageContent, userBehavior = {}) {
    try {
      const response = await this.apiClient.post('/productivity/smart-suggestions', {
        page_url: pageUrl,
        page_content: pageContent,
        user_behavior: userBehavior
      });
      return response.data;
    } catch (error) {
      console.error('Smart suggestions error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getTemplateLibrary(category = null, userId = null) {
    try {
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      if (userId) params.append('user_id', userId);
      
      const response = await this.apiClient.get(`/productivity/template-library?${params}`);
      return response.data;
    } catch (error) {
      console.error('Template library error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getQuickActionsBar(pageContext = {}, userPreferences = {}) {
    try {
      const response = await this.apiClient.post('/productivity/quick-actions-bar', {
        page_context: pageContext,
        user_preferences: userPreferences
      });
      return response.data;
    } catch (error) {
      console.error('Quick actions bar error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== PERFORMANCE FEATURES =====

  async predictiveCaching(userId, currentUrl, userBehavior = {}) {
    try {
      const response = await this.apiClient.post('/performance/predictive-caching', {
        user_id: userId,
        current_url: currentUrl,
        user_behavior: userBehavior
      });
      return response.data;
    } catch (error) {
      console.error('Predictive caching error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async bandwidthOptimization(pageContent, userPreferences = {}) {
    try {
      const response = await this.apiClient.post('/performance/bandwidth-optimization', {
        page_content: pageContent,
        user_preferences: userPreferences
      });
      return response.data;
    } catch (error) {
      console.error('Bandwidth optimization error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async backgroundProcessing(taskType, taskData, userId) {
    try {
      const response = await this.apiClient.post('/performance/background-processing', {
        task_type: taskType,
        task_data: taskData,
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Background processing error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async memoryManagement(tabData, systemResources = {}) {
    try {
      const response = await this.apiClient.post('/performance/memory-management', {
        tab_data: tabData,
        system_resources: systemResources
      });
      return response.data;
    } catch (error) {
      console.error('Memory management error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async performanceMonitoring(userId) {
    try {
      const response = await this.apiClient.get(`/performance/monitoring/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Performance monitoring error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== AI INTERFACE FEATURES =====

  async naturalLanguageInterface(userInput, userId, context = {}) {
    try {
      const response = await this.apiClient.post('/ai-interface/natural-language', {
        user_input: userInput,
        user_id: userId,
        context: context
      });
      return response.data;
    } catch (error) {
      console.error('Natural language interface error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async voiceCommands(commandText, userId, audioData = null) {
    try {
      const response = await this.apiClient.post('/ai-interface/voice-commands', {
        command_text: commandText,
        user_id: userId,
        audio_data: audioData
      });
      return response.data;
    } catch (error) {
      console.error('Voice commands error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async multiAgentWorkflows(taskDescription, userId, complexity = 'medium') {
    try {
      const response = await this.apiClient.post('/ai-interface/multi-agent-workflows', {
        task_description: taskDescription,
        user_id: userId,
        complexity: complexity
      });
      return response.data;
    } catch (error) {
      console.error('Multi-agent workflows error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async crossPlatformIntelligence(userId, platformData, learningContext = {}) {
    try {
      const response = await this.apiClient.post('/ai-interface/cross-platform-intelligence', {
        user_id: userId,
        platform_data: platformData,
        learning_context: learningContext
      });
      return response.data;
    } catch (error) {
      console.error('Cross-platform intelligence error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getConversationMemory(userId) {
    try {
      const response = await this.apiClient.get(`/ai-interface/conversation-memory/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Get conversation memory error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async updateConversationMemory(userId, conversationData) {
    try {
      const response = await this.apiClient.post(`/ai-interface/conversation-memory/${userId}`, conversationData);
      return response.data;
    } catch (error) {
      console.error('Update conversation memory error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== FEATURE DISCOVERY & MANAGEMENT =====

  async getAvailableFeatures() {
    try {
      const response = await this.apiClient.get('/features/available');
      return response.data;
    } catch (error) {
      console.error('Get available features error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getQuickAccessFeatures() {
    try {
      const response = await this.apiClient.get('/features/quick-access');
      return response.data;
    } catch (error) {
      console.error('Get quick access features error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async executeFeature(featureId, parameters, userId) {
    try {
      const response = await this.apiClient.post('/features/execute', {
        feature_id: featureId,
        parameters: parameters,
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Execute feature error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getFeaturesStatus() {
    try {
      const response = await this.apiClient.get('/features/status');
      return response.data;
    } catch (error) {
      console.error('Get features status error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== BROWSER ENGINE SIMULATION =====

  async nativeBrowserControls(action, parameters = {}) {
    try {
      const response = await this.apiClient.post('/browser-engine/native-controls', {
        action: action,
        parameters: parameters
      });
      return response.data;
    } catch (error) {
      console.error('Native browser controls error:', error);
      return { status: 'error', error: error.message };
    }
  }

  async getBrowserEngineCapabilities() {
    try {
      const response = await this.apiClient.get('/browser-engine/capabilities');
      return response.data;
    } catch (error) {
      console.error('Get browser engine capabilities error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // ===== UTILITY METHODS =====

  async executeContextualAction(action, context) {
    switch (action) {
      case 'ai_analyze':
        return await this.oneClickActions(context.url, context.content, context.userContext);
      case 'smart_bookmark':
        return await this.smartBookmarking(context.url, context.content, context.userId);
      case 'voice_command':
        return await this.voiceCommands(context.command, context.userId);
      case 'natural_language':
        return await this.naturalLanguageInterface(context.input, context.userId, context.context);
      default:
        return { status: 'error', error: 'Unknown contextual action' };
    }
  }

  // Background feature initialization (runs automatically)
  async initializeBackgroundFeatures(userId) {
    try {
      // Initialize predictive caching
      await this.predictiveCaching(userId, window.location.href, {
        session_duration: Date.now() - (window.sessionStart || Date.now()),
        pages_visited: 1
      });

      // Start performance monitoring
      await this.performanceMonitoring(userId);

      // Initialize cross-platform intelligence
      await this.crossPlatformIntelligence(userId, {
        browser: {
          user_agent: navigator.userAgent,
          viewport: { width: window.innerWidth, height: window.innerHeight }
        }
      });

      console.log('✅ Enhanced features initialized in background');
      return { status: 'success', message: 'Background features initialized' };
    } catch (error) {
      console.error('Background initialization error:', error);
      return { status: 'error', error: error.message };
    }
  }

  // Check if features are working
  async healthCheck() {
    try {
      const status = await this.getFeaturesStatus();
      console.log('🚀 Enhanced Features Status:', status);
      return status;
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error', error: error.message };
    }
  }
}

// Create singleton instance
export const enhancedFeaturesService = new EnhancedFeaturesService();

// Auto-initialize when service is imported (minimal impact)
if (typeof window !== 'undefined') {
  // Initialize in background without disrupting UI
  setTimeout(() => {
    const userId = localStorage.getItem('userId') || 'anonymous';
    enhancedFeaturesService.initializeBackgroundFeatures(userId).catch(console.warn);
  }, 2000); // Wait 2 seconds after page load
}

export default enhancedFeaturesService;