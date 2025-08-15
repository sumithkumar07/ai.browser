/**
 * Real Browser Service - Frontend Integration
 * Handles communication with the real Chromium browser engine
 */

import axios from 'axios';

class RealBrowserService {
  constructor() {
    this.baseURL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
    this.apiClient = axios.create({
      baseURL: `${this.baseURL}/api/real-browser`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth
    this.apiClient.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor for error handling
    this.apiClient.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Real Browser API Error:', error);
        return Promise.reject(error);
      }
    );

    this.activeTabs = new Map();
    this.currentSession = null;
  }

  // Session Management
  async createSession(sessionId = null) {
    try {
      const response = await this.apiClient.post('/sessions/create', {
        session_id: sessionId
      });
      
      if (response.data.success) {
        this.currentSession = response.data.session_id;
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to create browser session:', error);
      throw error;
    }
  }

  async getSessions() {
    try {
      const response = await this.apiClient.get('/sessions');
      return response.data;
    } catch (error) {
      console.error('Failed to get sessions:', error);
      throw error;
    }
  }

  async cleanupSession(sessionId) {
    try {
      const response = await this.apiClient.delete(`/sessions/${sessionId}`);
      
      if (response.data.success && sessionId === this.currentSession) {
        this.currentSession = null;
        this.activeTabs.clear();
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to cleanup session:', error);
      throw error;
    }
  }

  // Tab Management
  async createNewTab(url = 'about:blank') {
    try {
      // Ensure we have a session
      if (!this.currentSession) {
        await this.createSession();
      }

      const response = await this.apiClient.post('/tabs/create', {
        url,
        session_id: this.currentSession
      });

      if (response.data.success) {
        this.activeTabs.set(response.data.tab_id, {
          id: response.data.tab_id,
          url: response.data.url,
          title: response.data.title,
          sessionId: response.data.session_id,
          createdAt: new Date()
        });
      }

      return response.data;
    } catch (error) {
      console.error('Failed to create new tab:', error);
      throw error;
    }
  }

  async getTabInfo(tabId) {
    try {
      const response = await this.apiClient.get(`/tabs/${tabId}`);
      
      if (response.data.success) {
        // Update local tab info
        if (this.activeTabs.has(tabId)) {
          const tabInfo = this.activeTabs.get(tabId);
          this.activeTabs.set(tabId, {
            ...tabInfo,
            ...response.data,
            lastUpdated: new Date()
          });
        }
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to get tab info:', error);
      throw error;
    }
  }

  async closeTab(tabId) {
    try {
      const response = await this.apiClient.delete(`/tabs/${tabId}`);
      
      if (response.data.success) {
        this.activeTabs.delete(tabId);
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to close tab:', error);
      throw error;
    }
  }

  // Navigation
  async navigateToUrl(url, tabId = null) {
    try {
      const response = await this.apiClient.post('/navigate', {
        url,
        tab_id: tabId,
        session_id: this.currentSession
      });

      if (response.data.success) {
        // Update tab info if we have the tab
        const finalTabId = response.data.tab_id;
        if (this.activeTabs.has(finalTabId)) {
          const tabInfo = this.activeTabs.get(finalTabId);
          this.activeTabs.set(finalTabId, {
            ...tabInfo,
            url: response.data.url,
            title: response.data.title,
            lastNavigated: new Date()
          });
        } else {
          // Add new tab to tracking
          this.activeTabs.set(finalTabId, {
            id: finalTabId,
            url: response.data.url,
            title: response.data.title,
            sessionId: this.currentSession,
            lastNavigated: new Date()
          });
        }
      }

      return response.data;
    } catch (error) {
      console.error('Failed to navigate to URL:', error);
      throw error;
    }
  }

  async goBack(tabId) {
    try {
      const response = await this.apiClient.post(`/tabs/${tabId}/back`);
      
      if (response.data.success && this.activeTabs.has(tabId)) {
        const tabInfo = this.activeTabs.get(tabId);
        this.activeTabs.set(tabId, {
          ...tabInfo,
          url: response.data.url,
          title: response.data.title,
          lastUpdated: new Date()
        });
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to go back:', error);
      throw error;
    }
  }

  async goForward(tabId) {
    try {
      const response = await this.apiClient.post(`/tabs/${tabId}/forward`);
      
      if (response.data.success && this.activeTabs.has(tabId)) {
        const tabInfo = this.activeTabs.get(tabId);
        this.activeTabs.set(tabId, {
          ...tabInfo,
          url: response.data.url,
          title: response.data.title,
          lastUpdated: new Date()
        });
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to go forward:', error);
      throw error;
    }
  }

  async reload(tabId) {
    try {
      const response = await this.apiClient.post(`/tabs/${tabId}/reload`);
      
      if (response.data.success && this.activeTabs.has(tabId)) {
        const tabInfo = this.activeTabs.get(tabId);
        this.activeTabs.set(tabId, {
          ...tabInfo,
          url: response.data.url,
          title: response.data.title,
          lastUpdated: new Date()
        });
      }
      
      return response.data;
    } catch (error) {
      console.error('Failed to reload:', error);
      throw error;
    }
  }

  // Content and Analysis
  async getPageContent(tabId) {
    try {
      const response = await this.apiClient.get(`/tabs/${tabId}/content`);
      return response.data;
    } catch (error) {
      console.error('Failed to get page content:', error);
      throw error;
    }
  }

  async takeScreenshot(tabId) {
    try {
      const response = await this.apiClient.post(`/tabs/${tabId}/screenshot`);
      return response.data;
    } catch (error) {
      console.error('Failed to take screenshot:', error);
      throw error;
    }
  }

  async evaluateJavaScript(tabId, script) {
    try {
      const response = await this.apiClient.post(`/tabs/${tabId}/evaluate`, {
        script
      });
      return response.data;
    } catch (error) {
      console.error('Failed to evaluate JavaScript:', error);
      throw error;
    }
  }

  // Health and Capabilities
  async getBrowserHealth() {
    try {
      const response = await this.apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Failed to get browser health:', error);
      throw error;
    }
  }

  async getBrowserCapabilities() {
    try {
      const response = await this.apiClient.get('/capabilities');
      return response.data;
    } catch (error) {
      console.error('Failed to get browser capabilities:', error);
      throw error;
    }
  }

  // Utility Methods
  getActiveTabs() {
    return Array.from(this.activeTabs.values());
  }

  getCurrentSession() {
    return this.currentSession;
  }

  isTabActive(tabId) {
    return this.activeTabs.has(tabId);
  }

  // Smart URL processing
  processUrl(input) {
    const trimmed = input.trim();
    
    // Check if it's already a complete URL
    if (trimmed.match(/^https?:\/\//)) {
      return trimmed;
    }
    
    // Check if it looks like a domain
    if (trimmed.includes('.') && !trimmed.includes(' ')) {
      return `https://${trimmed}`;
    }
    
    // Treat as search query
    return `https://www.google.com/search?q=${encodeURIComponent(trimmed)}`;
  }

  // Event handlers for Electron integration
  setupElectronIntegration() {
    if (window.electronAPI) {
      console.log('🔌 Electron API detected - Real browser capabilities enabled');
      
      // You can add electron-specific integrations here
      return true;
    }
    
    console.log('🌐 Running in web mode - Using backend browser engine');
    return false;
  }

  // Quick actions for common browsing tasks
  async quickSearch(query) {
    const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
    return await this.navigateToUrl(searchUrl);
  }

  async openPopularSite(site) {
    const urls = {
      'google': 'https://www.google.com',
      'youtube': 'https://www.youtube.com',
      'github': 'https://github.com',
      'stackoverflow': 'https://stackoverflow.com',
      'reddit': 'https://www.reddit.com',
      'twitter': 'https://twitter.com',
      'facebook': 'https://www.facebook.com',
      'linkedin': 'https://www.linkedin.com',
      'news': 'https://news.google.com',
      'wiki': 'https://wikipedia.org'
    };
    
    const url = urls[site.toLowerCase()] || `https://www.${site.toLowerCase()}.com`;
    return await this.navigateToUrl(url);
  }

  // Cleanup
  async cleanup() {
    try {
      if (this.currentSession) {
        await this.cleanupSession(this.currentSession);
      }
    } catch (error) {
      console.error('Cleanup failed:', error);
    }
  }
}

// Export singleton instance
const realBrowserService = new RealBrowserService();
export default realBrowserService;