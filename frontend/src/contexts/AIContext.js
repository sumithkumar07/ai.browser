import React, { createContext, useContext, useReducer } from 'react';

const AIContext = createContext();

const initialState = {
  isAssistantVisible: false,
  isAssistantCollapsed: false,
  chatMessages: [],
  currentTasks: [],
  aiCapabilities: {
    automation: true,
    contentAnalysis: true,
    personalAssistant: true,
    codeExecution: false,
    // 🚀 HYBRID AI CAPABILITIES - FULLY ACTIVE
    neonAI: {
      neonChat: true,          // Contextual webpage understanding
      neonDo: true,            // Enhanced browser automation  
      neonMake: true,          // Professional app generation
      neonFocus: true,         // Distraction-free reading mode
      neonIntelligence: true   // Real-time page analysis
    },
    fellouAI: {
      deepAction: true,           // Multi-step workflow orchestration
      deepSearch: true,           // Professional research reports
      agenticMemory: true,        // Behavioral learning & prediction
      controllableWorkflow: true  // Visual workflow builder
    },
    hybridIntelligence: true,     // Combined Neon + Fellou.ai intelligence
    crossPlatformIntegration: true // Slack, Notion, Google, Microsoft
  },
  aiStatus: 'idle', // idle, processing, error
  currentAnalysis: null,
  automationQueue: [],
  // 🧠 ENHANCED HYBRID AI STATE
  hybridFeatures: {
    contextualAwareness: true,        // Neon AI active
    behavioralLearning: true,         // Agentic Memory active
    predictiveAssistance: true,       // Predictive insights active
    workflowOrchestration: true,      // Deep Action active
    professionalResearch: true,       // Deep Search active
    appGeneration: true,              // Neon Make active
    crossPlatformSync: true,          // External integrations active
    realTimeIntelligence: true,       // Live analysis active
    // 🚀 NEW ADVANCED FEATURES
    smartBookmarkIntelligence: true,  // AI bookmark management
    contextAwareSuggestions: true,    // Proactive AI assistance
    aiBrowserPlugins: true,           // Dynamic plugin generation
    realTimeCollaboration: true,      // Multi-user AI collaboration
    predictiveContentCaching: true,   // AI-powered pre-loading
    seamlessIntegration: true         // Perfect Neon+Fellou harmony
  },
  agenticMemory: {
    learningScore: 0,
    behaviorPatterns: [],
    preferences: {},
    interactionHistory: []
  },
  activeWorkflows: [],
  generatedApps: [],
  researchReports: []
};

function aiReducer(state, action) {
  switch (action.type) {
    case 'TOGGLE_ASSISTANT':
      return {
        ...state,
        isAssistantVisible: !state.isAssistantVisible
      };
    case 'COLLAPSE_ASSISTANT':
      return {
        ...state,
        isAssistantCollapsed: action.payload
      };
    case 'ADD_CHAT_MESSAGE':
      return {
        ...state,
        chatMessages: [...state.chatMessages, action.payload]
      };
    case 'SET_AI_STATUS':
      return {
        ...state,
        aiStatus: action.payload
      };
    case 'ADD_TASK':
      return {
        ...state,
        currentTasks: [...state.currentTasks, action.payload]
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        currentTasks: state.currentTasks.map(task => 
          task.id === action.payload.id ? { ...task, ...action.payload } : task
        )
      };
    case 'REMOVE_TASK':
      return {
        ...state,
        currentTasks: state.currentTasks.filter(task => task.id !== action.payload)
      };
    case 'SET_CURRENT_ANALYSIS':
      return {
        ...state,
        currentAnalysis: action.payload
      };
    case 'ADD_TO_AUTOMATION_QUEUE':
      return {
        ...state,
        automationQueue: [...state.automationQueue, action.payload]
      };
    case 'CLEAR_CHAT':
      return {
        ...state,
        chatMessages: []
      };
    // 🚀 NEW HYBRID AI ACTIONS
    case 'UPDATE_HYBRID_FEATURES':
      return {
        ...state,
        hybridFeatures: { ...state.hybridFeatures, ...action.payload }
      };
    case 'UPDATE_AGENTIC_MEMORY':
      return {
        ...state,
        agenticMemory: { ...state.agenticMemory, ...action.payload }
      };
    case 'ADD_WORKFLOW':
      return {
        ...state,
        activeWorkflows: [...state.activeWorkflows, action.payload]
      };
    case 'UPDATE_WORKFLOW':
      return {
        ...state,
        activeWorkflows: state.activeWorkflows.map(workflow =>
          workflow.id === action.payload.id ? { ...workflow, ...action.payload } : workflow
        )
      };
    case 'ADD_GENERATED_APP':
      return {
        ...state,
        generatedApps: [...state.generatedApps, action.payload]
      };
    case 'ADD_RESEARCH_REPORT':
      return {
        ...state,
        researchReports: [...state.researchReports, action.payload]
      };
    case 'SET_HYBRID_STATUS':
      return {
        ...state,
        aiCapabilities: { ...state.aiCapabilities, ...action.payload }
      };
    default:
      return state;
  }
}

export function useAI() {
  const context = useContext(AIContext);
  if (!context) {
    throw new Error('useAI must be used within an AIContextProvider');
  }
  return context;
}

export default function AIContextProvider({ children }) {
  const [state, dispatch] = useReducer(aiReducer, initialState);

  const contextValue = {
    ...state,
    dispatch,
    // Helper functions
    toggleAssistant: () => dispatch({ type: 'TOGGLE_ASSISTANT' }),
    collapseAssistant: (collapsed) => dispatch({ type: 'COLLAPSE_ASSISTANT', payload: collapsed }),
    addChatMessage: (message) => dispatch({ type: 'ADD_CHAT_MESSAGE', payload: message }),
    setAIStatus: (status) => dispatch({ type: 'SET_AI_STATUS', payload: status }),
    addTask: (task) => dispatch({ type: 'ADD_TASK', payload: task }),
    updateTask: (task) => dispatch({ type: 'UPDATE_TASK', payload: task }),
    removeTask: (taskId) => dispatch({ type: 'REMOVE_TASK', payload: taskId }),
    setCurrentAnalysis: (analysis) => dispatch({ type: 'SET_CURRENT_ANALYSIS', payload: analysis }),
    addToAutomationQueue: (automation) => dispatch({ type: 'ADD_TO_AUTOMATION_QUEUE', payload: automation }),
    clearChat: () => dispatch({ type: 'CLEAR_CHAT' }),
    // 🚀 NEW HYBRID AI HELPER FUNCTIONS
    updateHybridFeatures: (features) => dispatch({ type: 'UPDATE_HYBRID_FEATURES', payload: features }),
    updateAgenticMemory: (memory) => dispatch({ type: 'UPDATE_AGENTIC_MEMORY', payload: memory }),
    addWorkflow: (workflow) => dispatch({ type: 'ADD_WORKFLOW', payload: workflow }),
    updateWorkflow: (workflow) => dispatch({ type: 'UPDATE_WORKFLOW', payload: workflow }),
    addGeneratedApp: (app) => dispatch({ type: 'ADD_GENERATED_APP', payload: app }),
    addResearchReport: (report) => dispatch({ type: 'ADD_RESEARCH_REPORT', payload: report }),
    setHybridStatus: (status) => dispatch({ type: 'SET_HYBRID_STATUS', payload: status })
  };

  return (
    <AIContext.Provider value={contextValue}>
      {children}
    </AIContext.Provider>
  );
}