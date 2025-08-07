import React, { createContext, useContext, useReducer } from 'react';

const BrowserContext = createContext();

const initialState = {
  sessions: [],
  currentSession: null,
  tabs: [],
  activeTab: null,
  splitMode: false,
  splitPanes: [],
  bubblePositions: {},
  windowLayout: {
    split_mode: 'single',
    splits: []
  }
};

function browserReducer(state, action) {
  switch (action.type) {
    case 'SET_SESSIONS':
      return {
        ...state,
        sessions: action.payload
      };
    case 'SET_CURRENT_SESSION':
      return {
        ...state,
        currentSession: action.payload,
        tabs: action.payload?.tabs || []
      };
    case 'ADD_TAB':
      return {
        ...state,
        tabs: [...state.tabs, action.payload]
      };
    case 'UPDATE_TAB':
      return {
        ...state,
        tabs: state.tabs.map(tab => 
          tab.id === action.payload.id ? { ...tab, ...action.payload } : tab
        )
      };
    case 'CLOSE_TAB':
      return {
        ...state,
        tabs: state.tabs.filter(tab => tab.id !== action.payload),
        activeTab: state.activeTab === action.payload ? null : state.activeTab
      };
    case 'SET_ACTIVE_TAB':
      return {
        ...state,
        activeTab: action.payload
      };
    case 'UPDATE_BUBBLE_POSITION':
      return {
        ...state,
        bubblePositions: {
          ...state.bubblePositions,
          [action.payload.tabId]: {
            x: action.payload.x,
            y: action.payload.y
          }
        }
      };
    case 'SET_SPLIT_MODE':
      return {
        ...state,
        splitMode: action.payload
      };
    case 'UPDATE_WINDOW_LAYOUT':
      return {
        ...state,
        windowLayout: action.payload
      };
    default:
      return state;
  }
}

export function useBrowser() {
  const context = useContext(BrowserContext);
  if (!context) {
    throw new Error('useBrowser must be used within a BrowserContextProvider');
  }
  return context;
}

export default function BrowserContextProvider({ children }) {
  const [state, dispatch] = useReducer(browserReducer, initialState);

  const contextValue = {
    ...state,
    dispatch,
    // Helper functions
    addTab: (tab) => dispatch({ type: 'ADD_TAB', payload: tab }),
    updateTab: (tab) => dispatch({ type: 'UPDATE_TAB', payload: tab }),
    closeTab: (tabId) => dispatch({ type: 'CLOSE_TAB', payload: tabId }),
    setActiveTab: (tabId) => dispatch({ type: 'SET_ACTIVE_TAB', payload: tabId }),
    updateBubblePosition: (tabId, x, y) => 
      dispatch({ type: 'UPDATE_BUBBLE_POSITION', payload: { tabId, x, y } }),
    setSplitMode: (enabled) => dispatch({ type: 'SET_SPLIT_MODE', payload: enabled }),
    setSessions: (sessions) => dispatch({ type: 'SET_SESSIONS', payload: sessions }),
    setCurrentSession: (session) => dispatch({ type: 'SET_CURRENT_SESSION', payload: session })
  };

  return (
    <BrowserContext.Provider value={contextValue}>
      {children}
    </BrowserContext.Provider>
  );
}