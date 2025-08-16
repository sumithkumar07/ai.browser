import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://ai-completion-plan.preview.emergentagent.com';

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('auth_token') || '';
};

// Helper function to create auth headers
const getAuthHeaders = () => {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

class ParallelFeaturesService {
  // Advanced Navigation Services
  static async naturalLanguageNavigation(query, userContext = null) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/advanced-navigation/natural-language-navigation`,
        { query, user_context: userContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Natural language navigation failed:', error);
      throw error;
    }
  }

  static async aiPoweredUrlParsing(inputText) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/advanced-navigation/ai-powered-url-parsing`,
        { input_text: inputText },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('AI URL parsing failed:', error);
      throw error;
    }
  }

  // Cross-Site Intelligence Services
  static async analyzeWebsiteRelationships(urls, depth = 2) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/cross-site-intelligence/website-relationship-mapping`,
        { urls, depth },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Website relationship analysis failed:', error);
      throw error;
    }
  }

  static async smartBookmarkCategorization(bookmarkData) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/cross-site-intelligence/smart-bookmark-categorization`,
        { bookmark_data: bookmarkData },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Smart bookmark categorization failed:', error);
      throw error;
    }
  }

  // Enhanced Performance Services
  static async predictiveContentCaching(userId, browsingContext) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/enhanced-performance/predictive-content-caching`,
        { user_id: userId, browsing_context: browsingContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Predictive caching failed:', error);
      throw error;
    }
  }

  static async intelligentTabSuspension(tabContext) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/enhanced-performance/intelligent-tab-suspension`,
        { tab_context: tabContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Tab suspension failed:', error);
      throw error;
    }
  }

  // Template & Automation Services
  static async getTemplateLibrary(category = null, userId = null) {
    try {
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      if (userId) params.append('user_id', userId);

      const response = await axios.get(
        `${API_BASE_URL}/api/template-automation/template-library?${params.toString()}`,
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Template library access failed:', error);
      throw error;
    }
  }

  static async createAutomationWorkflow(workflowConfig) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/template-automation/create-automation-workflow`,
        { workflow_config: workflowConfig },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Workflow creation failed:', error);
      throw error;
    }
  }

  static async generateWorkflowFromDescription(description, userContext = null) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/template-automation/generate-workflow-from-description`,
        { description, user_context: userContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Workflow generation failed:', error);
      throw error;
    }
  }

  // Voice & Actions Services
  static async processVoiceCommand(audioInput, userContext = null) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/voice-actions/process-voice-command`,
        { audio_input: audioInput, user_context: userContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Voice command processing failed:', error);
      throw error;
    }
  }

  static async getOneClickActions(pageContext, userPreferences = null) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/voice-actions/one-click-actions`,
        { page_context: pageContext, user_preferences: userPreferences },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('One-click actions failed:', error);
      throw error;
    }
  }

  static async getQuickActionsBar(userContext) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/voice-actions/quick-actions-bar`,
        { user_context: userContext },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Quick actions bar failed:', error);
      throw error;
    }
  }

  static async executeQuickAction(actionId, context, parameters = null) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/voice-actions/execute-quick-action`,
        { action_id: actionId, context, parameters },
        { headers: getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Quick action execution failed:', error);
      throw error;
    }
  }

  // Capability Services
  static async getAllCapabilities() {
    try {
      const [navCaps, intelligenceCaps, perfCaps, automationCaps, voiceCaps] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/advanced-navigation/navigation-capabilities`, { headers: getAuthHeaders() }),
        axios.get(`${API_BASE_URL}/api/cross-site-intelligence/intelligence-capabilities`, { headers: getAuthHeaders() }),
        axios.get(`${API_BASE_URL}/api/enhanced-performance/performance-capabilities`, { headers: getAuthHeaders() }),
        axios.get(`${API_BASE_URL}/api/template-automation/automation-capabilities`, { headers: getAuthHeaders() }),
        axios.get(`${API_BASE_URL}/api/voice-actions/voice-actions-capabilities`, { headers: getAuthHeaders() })
      ]);

      return {
        navigation: navCaps.data,
        intelligence: intelligenceCaps.data,
        performance: perfCaps.data,
        automation: automationCaps.data,
        voice_actions: voiceCaps.data
      };
    } catch (error) {
      console.error('Capabilities fetch failed:', error);
      return null;
    }
  }
}

export default ParallelFeaturesService;