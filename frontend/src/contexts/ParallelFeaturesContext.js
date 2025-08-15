import React, { createContext, useContext, useReducer, useEffect } from 'react';
import ParallelFeaturesService from '../services/parallelFeaturesService';

const ParallelFeaturesContext = createContext();

// Action types
const ACTIONS = {
  SET_CAPABILITIES: 'SET_CAPABILITIES',
  SET_VOICE_ACTIVE: 'SET_VOICE_ACTIVE',
  SET_QUICK_ACTIONS: 'SET_QUICK_ACTIONS',
  SET_NAVIGATION_RESULTS: 'SET_NAVIGATION_RESULTS',
  SET_BOOKMARKS_INTELLIGENCE: 'SET_BOOKMARKS_INTELLIGENCE',
  SET_PERFORMANCE_OPTIMIZATION: 'SET_PERFORMANCE_OPTIMIZATION',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR'
};

// Initial state
const initialState = {
  capabilities: null,
  voiceActive: false,
  quickActions: [],
  navigationResults: null,
  bookmarksIntelligence: null,
  performanceOptimization: null,
  loading: false,
  error: null
};

// Reducer
function parallelFeaturesReducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_CAPABILITIES:
      return { ...state, capabilities: action.payload, loading: false };
    case ACTIONS.SET_VOICE_ACTIVE:
      return { ...state, voiceActive: action.payload };
    case ACTIONS.SET_QUICK_ACTIONS:
      return { ...state, quickActions: action.payload };
    case ACTIONS.SET_NAVIGATION_RESULTS:
      return { ...state, navigationResults: action.payload };
    case ACTIONS.SET_BOOKMARKS_INTELLIGENCE:
      return { ...state, bookmarksIntelligence: action.payload };
    case ACTIONS.SET_PERFORMANCE_OPTIMIZATION:
      return { ...state, performanceOptimization: action.payload };
    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };
    case ACTIONS.SET_ERROR:
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}

export function ParallelFeaturesProvider({ children }) {
  const [state, dispatch] = useReducer(parallelFeaturesReducer, initialState);

  // Load capabilities on mount
  useEffect(() => {
    loadCapabilities();
  }, []);

  const loadCapabilities = async () => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const capabilities = await ParallelFeaturesService.getAllCapabilities();
      dispatch({ type: ACTIONS.SET_CAPABILITIES, payload: capabilities });
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
    }
  };

  // Natural Language Navigation
  const navigateWithNaturalLanguage = async (query, userContext = null) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.naturalLanguageNavigation(query, userContext);
      dispatch({ type: ACTIONS.SET_NAVIGATION_RESULTS, payload: result });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // AI-Powered URL Parsing
  const parseUrlWithAI = async (inputText) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.aiPoweredUrlParsing(inputText);
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // Smart Bookmark Categorization
  const categorizeBooksmarkWithAI = async (bookmarkData) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.smartBookmarkCategorization(bookmarkData);
      dispatch({ type: ACTIONS.SET_BOOKMARKS_INTELLIGENCE, payload: result });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // Predictive Content Caching
  const enablePredictiveCaching = async (userId, browsingContext) => {
    try {
      const result = await ParallelFeaturesService.predictiveContentCaching(userId, browsingContext);
      dispatch({ type: ACTIONS.SET_PERFORMANCE_OPTIMIZATION, payload: result });
      return result;
    } catch (error) {
      console.error('Predictive caching failed:', error);
      return null;
    }
  };

  // Voice Command Processing
  const processVoiceCommand = async (audioInput, userContext = null) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.processVoiceCommand(audioInput, userContext);
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // Quick Actions Management
  const loadQuickActions = async (userContext) => {
    try {
      const result = await ParallelFeaturesService.getQuickActionsBar(userContext);
      if (result.success) {
        dispatch({ type: ACTIONS.SET_QUICK_ACTIONS, payload: result.quick_actions });
      }
      return result;
    } catch (error) {
      console.error('Quick actions loading failed:', error);
      return null;
    }
  };

  const executeQuickAction = async (actionId, context, parameters = null) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.executeQuickAction(actionId, context, parameters);
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // Template & Automation
  const getTemplateLibrary = async (category = null, userId = null) => {
    try {
      const result = await ParallelFeaturesService.getTemplateLibrary(category, userId);
      return result;
    } catch (error) {
      console.error('Template library access failed:', error);
      return null;
    }
  };

  const generateWorkflowFromDescription = async (description, userContext = null) => {
    try {
      dispatch({ type: ACTIONS.SET_LOADING, payload: true });
      const result = await ParallelFeaturesService.generateWorkflowFromDescription(description, userContext);
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      return result;
    } catch (error) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error.message });
      throw error;
    }
  };

  // Voice Control
  const toggleVoiceCommands = () => {
    dispatch({ type: ACTIONS.SET_VOICE_ACTIVE, payload: !state.voiceActive });
  };

  const value = {
    ...state,
    
    // Navigation
    navigateWithNaturalLanguage,
    parseUrlWithAI,
    
    // Intelligence
    categorizeBooksmarkWithAI,
    
    // Performance
    enablePredictiveCaching,
    
    // Voice & Actions
    processVoiceCommand,
    loadQuickActions,
    executeQuickAction,
    toggleVoiceCommands,
    
    // Templates & Automation
    getTemplateLibrary,
    generateWorkflowFromDescription,
    
    // Utility
    loadCapabilities
  };

  return (
    <ParallelFeaturesContext.Provider value={value}>
      {children}
    </ParallelFeaturesContext.Provider>
  );
}

export function useParallelFeatures() {
  const context = useContext(ParallelFeaturesContext);
  if (context === undefined) {
    throw new Error('useParallelFeatures must be used within a ParallelFeaturesProvider');
  }
  return context;
}

export default ParallelFeaturesContext;