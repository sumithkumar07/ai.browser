/**
 * 🚀 Hybrid Browser Service - Minimal Frontend Integration
 * Provides access to all Phase 1-3 hybrid browser capabilities
 */

import axios from 'axios';

class HybridBrowserService {
  constructor() {
    this.baseURL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
    this.apiClient = axios.create({
      baseURL: `${this.baseURL}/api/hybrid-browser`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      }
    });
  }

  // === PHASE 1: DEEP ACTION TECHNOLOGY ===
  
  async createWorkflow(command, context = null, userId = null) {
    try {
      const response = await this.apiClient.post('/deep-action/create-workflow', {
        command,
        context,
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Workflow creation failed:', error);
      return { success: false, error: error.message };
    }
  }

  async executeWorkflow(workflowId, approveAll = false) {
    try {
      const response = await this.apiClient.post(`/deep-action/execute-workflow/${workflowId}`, null, {
        params: { approve_all: approveAll }
      });
      return response.data;
    } catch (error) {
      console.error('Workflow execution failed:', error);
      return { success: false, error: error.message };
    }
  }

  async getWorkflowStatus(workflowId) {
    try {
      const response = await this.apiClient.get(`/deep-action/workflow-status/${workflowId}`);
      return response.data;
    } catch (error) {
      console.error('Workflow status check failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === PHASE 1: AGENTIC MEMORY SYSTEM ===

  async trackUserBehavior(userId, actionType, actionData, context = null, success = true) {
    try {
      const response = await this.apiClient.post('/agentic-memory/track-behavior', {
        user_id: userId,
        action_type: actionType,
        action_data: actionData,
        context,
        success
      });
      return response.data;
    } catch (error) {
      console.error('Behavior tracking failed:', error);
      return { success: false, error: error.message };
    }
  }

  async getPersonalizedSuggestions(userId, context = null) {
    try {
      const params = context ? { context: JSON.stringify(context) } : {};
      const response = await this.apiClient.get(`/agentic-memory/personalized-suggestions/${userId}`, { params });
      return response.data;
    } catch (error) {
      console.error('Personalized suggestions failed:', error);
      return { success: false, error: error.message };
    }
  }

  async adaptToUserContext(userId, currentTask, historicalContext = null) {
    try {
      const response = await this.apiClient.post(`/agentic-memory/adapt-context/${userId}`, {
        current_task: currentTask,
        historical_context: historicalContext
      });
      return response.data;
    } catch (error) {
      console.error('Context adaptation failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === PHASE 1: DEEP SEARCH INTEGRATION ===

  async parallelDeepSearch(query, platforms = null, userId = null, searchOptions = null) {
    try {
      const response = await this.apiClient.post('/deep-search/parallel-search', {
        query,
        platforms,
        user_id: userId,
        search_options: searchOptions
      });
      return response.data;
    } catch (error) {
      console.error('Deep search failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === PHASE 2: VIRTUAL WORKSPACE ===

  async createVirtualWorkspace(userId, workspaceConfig = null) {
    try {
      const response = await this.apiClient.post('/virtual-workspace/create', {
        user_id: userId,
        workspace_config: workspaceConfig
      });
      return response.data;
    } catch (error) {
      console.error('Virtual workspace creation failed:', error);
      return { success: false, error: error.message };
    }
  }

  async createShadowWindow(workspaceId, windowConfig) {
    try {
      const response = await this.apiClient.post(`/virtual-workspace/shadow-window/${workspaceId}`, windowConfig);
      return response.data;
    } catch (error) {
      console.error('Shadow window creation failed:', error);
      return { success: false, error: error.message };
    }
  }

  async executeBackgroundOperation(workspaceId, operationConfig) {
    try {
      const response = await this.apiClient.post(`/virtual-workspace/background-operation/${workspaceId}`, {
        operation_config: operationConfig
      });
      return response.data;
    } catch (error) {
      console.error('Background operation failed:', error);
      return { success: false, error: error.message };
    }
  }

  async getWorkspaceStatus(workspaceId) {
    try {
      const response = await this.apiClient.get(`/virtual-workspace/status/${workspaceId}`);
      return response.data;
    } catch (error) {
      console.error('Workspace status check failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === PHASE 2: BROWSER ENGINE FOUNDATION ===

  async createNativeBrowserInstance(userId, config = null) {
    try {
      const response = await this.apiClient.post('/browser-engine/create-instance', {
        user_id: userId,
        config
      });
      return response.data;
    } catch (error) {
      console.error('Native browser instance creation failed:', error);
      return { success: false, error: error.message };
    }
  }

  async integrateWithOS(integrationType, config = null) {
    try {
      const response = await this.apiClient.post(`/browser-engine/os-integration/${integrationType}`, {
        integration_type: integrationType,
        config
      });
      return response.data;
    } catch (error) {
      console.error('OS integration failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === COMPREHENSIVE STATUS ===

  async getHybridBrowserStatus() {
    try {
      const response = await this.apiClient.get('/comprehensive-status');
      return response.data;
    } catch (error) {
      console.error('Hybrid browser status check failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === CAPABILITIES ===

  async getAllCapabilities() {
    try {
      const [deepActionCaps, agenticMemoryCaps, deepSearchCaps, virtualWorkspaceCaps, browserEngineCaps] = await Promise.all([
        this.apiClient.get('/deep-action/capabilities'),
        this.apiClient.get('/agentic-memory/capabilities'),
        this.apiClient.get('/deep-search/capabilities'),
        this.apiClient.get('/virtual-workspace/capabilities'),
        this.apiClient.get('/browser-engine/capabilities')
      ]);

      return {
        success: true,
        capabilities: {
          deep_action_technology: deepActionCaps.data,
          agentic_memory_system: agenticMemoryCaps.data,
          deep_search_integration: deepSearchCaps.data,
          virtual_workspace: virtualWorkspaceCaps.data,
          browser_engine_foundation: browserEngineCaps.data
        }
      };
    } catch (error) {
      console.error('Capabilities check failed:', error);
      return { success: false, error: error.message };
    }
  }

  // === UTILITY METHODS ===

  isFeatureAvailable(feature) {
    const availableFeatures = [
      'deep_action_technology',
      'agentic_memory_system', 
      'deep_search_integration',
      'virtual_workspace',
      'browser_engine_foundation'
    ];
    return availableFeatures.includes(feature);
  }

  async testConnection() {
    try {
      const response = await this.apiClient.get('/comprehensive-status');
      return response.data.success || false;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }
}

export default new HybridBrowserService();