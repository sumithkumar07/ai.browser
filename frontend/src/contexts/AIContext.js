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
    codeExecution: false
  },
  aiStatus: 'idle', // idle, processing, error
  currentAnalysis: null,
  automationQueue: []
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
    clearChat: () => dispatch({ type: 'CLEAR_CHAT' })
  };

  return (
    <AIContext.Provider value={contextValue}>
      {children}
    </AIContext.Provider>
  );
}