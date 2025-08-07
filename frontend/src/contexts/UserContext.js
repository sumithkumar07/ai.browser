import React, { createContext, useContext, useReducer, useEffect } from 'react';

const UserContext = createContext();

const initialState = {
  user: {
    id: 'demo-user-123',
    name: 'Demo User',
    email: 'demo@aibrowser.com',
    user_mode: 'power',
    created_at: new Date().toISOString()
  }, // Mock user for demo
  isAuthenticated: true, // Set to true for demo
  isLoading: false,
  userMode: 'power', // consumer, power, enterprise
  preferences: {
    theme: 'dark',
    bubbleTabStyle: 'modern',
    aiAssistantAlwaysVisible: false,
    autoExecuteSimpleTasks: true,
    privacyMode: false
  },
  authToken: 'demo-token-123' // Mock token
};

function userReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload,
        isLoading: false
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload
      };
    case 'SET_USER_MODE':
      return {
        ...state,
        userMode: action.payload
      };
    case 'UPDATE_PREFERENCES':
      return {
        ...state,
        preferences: {
          ...state.preferences,
          ...action.payload
        }
      };
    case 'SET_AUTH_TOKEN':
      if (action.payload) {
        localStorage.setItem('authToken', action.payload);
      } else {
        localStorage.removeItem('authToken');
      }
      return {
        ...state,
        authToken: action.payload
      };
    case 'LOGOUT':
      localStorage.removeItem('authToken');
      return {
        ...initialState,
        isLoading: false,
        authToken: null
      };
    default:
      return state;
  }
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserContextProvider');
  }
  return context;
}

export default function UserContextProvider({ children }) {
  const [state, dispatch] = useReducer(userReducer, initialState);

  useEffect(() => {
    // Check for existing auth token on mount
    const token = localStorage.getItem('authToken');
    if (token) {
      // TODO: Validate token with backend
      dispatch({ type: 'SET_LOADING', payload: false });
    } else {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, []);

  const contextValue = {
    ...state,
    dispatch,
    // Helper functions
    setUser: (user) => dispatch({ type: 'SET_USER', payload: user }),
    setUserMode: (mode) => dispatch({ type: 'SET_USER_MODE', payload: mode }),
    updatePreferences: (preferences) => dispatch({ type: 'UPDATE_PREFERENCES', payload: preferences }),
    setAuthToken: (token) => dispatch({ type: 'SET_AUTH_TOKEN', payload: token }),
    logout: () => dispatch({ type: 'LOGOUT' }),
    setLoading: (loading) => dispatch({ type: 'SET_LOADING', payload: loading })
  };

  return (
    <UserContext.Provider value={contextValue}>
      {children}
    </UserContext.Provider>
  );
}