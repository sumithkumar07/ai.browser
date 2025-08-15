import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Enhanced Accessibility Context for better user experience
const AccessibilityContext = createContext();

const initialState = {
  isHighContrast: false,
  fontSize: 'normal', // small, normal, large, x-large
  reduceMotion: false,
  screenReaderMode: false,
  keyboardNavigationEnabled: true,
  focusVisible: true,
  announcements: [],
  preferences: {
    colorBlindFriendly: false,
    largeClickTargets: false,
    simplifiedInterface: false,
    voiceCommands: false
  },
  ariaLive: 'polite', // off, polite, assertive
  focusHistory: [],
  currentFocusId: null
};

function accessibilityReducer(state, action) {
  switch (action.type) {
    case 'TOGGLE_HIGH_CONTRAST':
      return {
        ...state,
        isHighContrast: !state.isHighContrast
      };
    case 'SET_FONT_SIZE':
      return {
        ...state,
        fontSize: action.payload
      };
    case 'TOGGLE_REDUCE_MOTION':
      return {
        ...state,
        reduceMotion: !state.reduceMotion
      };
    case 'TOGGLE_SCREEN_READER_MODE':
      return {
        ...state,
        screenReaderMode: !state.screenReaderMode
      };
    case 'ADD_ANNOUNCEMENT':
      return {
        ...state,
        announcements: [
          ...state.announcements,
          {
            id: Date.now(),
            message: action.payload.message,
            priority: action.payload.priority || 'polite',
            timestamp: new Date().toISOString()
          }
        ]
      };
    case 'CLEAR_ANNOUNCEMENTS':
      return {
        ...state,
        announcements: []
      };
    case 'UPDATE_PREFERENCES':
      return {
        ...state,
        preferences: {
          ...state.preferences,
          ...action.payload
        }
      };
    case 'SET_ARIA_LIVE':
      return {
        ...state,
        ariaLive: action.payload
      };
    case 'UPDATE_FOCUS':
      return {
        ...state,
        focusHistory: [
          ...state.focusHistory.slice(-9), // Keep last 10 focus events
          {
            id: action.payload,
            timestamp: Date.now()
          }
        ],
        currentFocusId: action.payload
      };
    case 'TOGGLE_KEYBOARD_NAVIGATION':
      return {
        ...state,
        keyboardNavigationEnabled: !state.keyboardNavigationEnabled
      };
    default:
      return state;
  }
}

export function useAccessibility() {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityContextProvider');
  }
  return context;
}

export default function AccessibilityContextProvider({ children }) {
  const [state, dispatch] = useReducer(accessibilityReducer, initialState);

  // Detect user preferences from system
  useEffect(() => {
    // Check for prefers-reduced-motion
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mediaQuery.matches) {
      dispatch({ type: 'TOGGLE_REDUCE_MOTION' });
    }

    // Check for high contrast preference
    const highContrastQuery = window.matchMedia('(prefers-contrast: high)');
    if (highContrastQuery.matches) {
      dispatch({ type: 'TOGGLE_HIGH_CONTRAST' });
    }

    // Listen for preference changes
    const handleMotionChange = (e) => {
      if (e.matches !== state.reduceMotion) {
        dispatch({ type: 'TOGGLE_REDUCE_MOTION' });
      }
    };

    const handleContrastChange = (e) => {
      if (e.matches !== state.isHighContrast) {
        dispatch({ type: 'TOGGLE_HIGH_CONTRAST' });
      }
    };

    mediaQuery.addEventListener('change', handleMotionChange);
    highContrastQuery.addEventListener('change', handleContrastChange);

    return () => {
      mediaQuery.removeEventListener('change', handleMotionChange);
      highContrastQuery.removeEventListener('change', handleContrastChange);
    };
  }, [state.reduceMotion, state.isHighContrast]);

  // Enhanced keyboard navigation
  useEffect(() => {
    if (!state.keyboardNavigationEnabled) return;

    const handleKeyDown = (e) => {
      // Enhanced Tab navigation
      if (e.key === 'Tab') {
        const focusableElements = document.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
          dispatch({
            type: 'UPDATE_FOCUS',
            payload: document.activeElement?.id || 'unknown'
          });
        }
      }

      // Enhanced keyboard shortcuts
      if (e.key === 'Escape') {
        // Close any open modals or menus
        const escapeEvent = new CustomEvent('accessibility-escape', {
          detail: { currentFocus: document.activeElement }
        });
        window.dispatchEvent(escapeEvent);
        
        announce('Closed current dialog or menu', 'polite');
      }

      // Skip links navigation
      if (e.key === 'Enter' && e.ctrlKey) {
        const skipLinks = document.querySelectorAll('[data-skip-link]');
        if (skipLinks.length > 0) {
          skipLinks[0].focus();
          announce('Skip link navigation activated', 'polite');
        }
      }

      // Quick help
      if (e.key === 'F1') {
        e.preventDefault();
        const helpEvent = new CustomEvent('accessibility-help-requested');
        window.dispatchEvent(helpEvent);
        announce('Help requested', 'polite');
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [state.keyboardNavigationEnabled]);

  // Screen reader announcements
  useEffect(() => {
    const announcer = document.getElementById('aria-live-announcer');
    if (announcer && state.announcements.length > 0) {
      const latest = state.announcements[state.announcements.length - 1];
      announcer.textContent = latest.message;
      announcer.setAttribute('aria-live', latest.priority);
    }
  }, [state.announcements]);

  // Focus management
  useEffect(() => {
    const handleFocusIn = (e) => {
      if (e.target.id) {
        dispatch({
          type: 'UPDATE_FOCUS',
          payload: e.target.id
        });
      }
    };

    document.addEventListener('focusin', handleFocusIn);
    return () => document.removeEventListener('focusin', handleFocusIn);
  }, []);

  const announce = (message, priority = 'polite') => {
    dispatch({
      type: 'ADD_ANNOUNCEMENT',
      payload: { message, priority }
    });
  };

  const contextValue = {
    ...state,
    dispatch,
    
    // Helper functions
    toggleHighContrast: () => dispatch({ type: 'TOGGLE_HIGH_CONTRAST' }),
    setFontSize: (size) => dispatch({ type: 'SET_FONT_SIZE', payload: size }),
    toggleReduceMotion: () => dispatch({ type: 'TOGGLE_REDUCE_MOTION' }),
    toggleScreenReaderMode: () => dispatch({ type: 'TOGGLE_SCREEN_READER_MODE' }),
    toggleKeyboardNavigation: () => dispatch({ type: 'TOGGLE_KEYBOARD_NAVIGATION' }),
    
    updatePreferences: (prefs) => dispatch({ 
      type: 'UPDATE_PREFERENCES', 
      payload: prefs 
    }),
    
    announce,
    
    clearAnnouncements: () => dispatch({ type: 'CLEAR_ANNOUNCEMENTS' }),
    
    setAriaLive: (level) => dispatch({ type: 'SET_ARIA_LIVE', payload: level }),
    
    // Accessibility helper functions
    getTabIndex: (isDisabled = false) => {
      return isDisabled ? -1 : 0;
    },
    
    getFocusableElements: (container = document) => {
      return container.querySelectorAll(
        'button:not(:disabled), [href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"]):not(:disabled)'
      );
    },
    
    trapFocus: (container) => {
      const focusableElements = contextValue.getFocusableElements(container);
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      const handleTabKey = (e) => {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              e.preventDefault();
              lastElement.focus();
            }
          } else {
            if (document.activeElement === lastElement) {
              e.preventDefault();
              firstElement.focus();
            }
          }
        }
      };
      
      container.addEventListener('keydown', handleTabKey);
      return () => container.removeEventListener('keydown', handleTabKey);
    },
    
    // Get CSS classes for accessibility
    getAccessibilityClasses: () => {
      let classes = [];
      
      if (state.isHighContrast) classes.push('high-contrast');
      if (state.reduceMotion) classes.push('reduce-motion');
      if (state.fontSize !== 'normal') classes.push(`font-size-${state.fontSize}`);
      if (state.preferences.largeClickTargets) classes.push('large-targets');
      if (state.preferences.simplifiedInterface) classes.push('simplified');
      
      return classes.join(' ');
    },
    
    // Check if element should be announced
    shouldAnnounce: (element) => {
      if (!element || typeof element.hasAttribute !== 'function') return false;
      return state.screenReaderMode || element.hasAttribute('data-announce-always');
    },
    
    // Generate ARIA labels dynamically
    generateAriaLabel: (element, context) => {
      const base = element.getAttribute('aria-label') || element.textContent || '';
      
      if (context && context.position) {
        return `${base}, item ${context.position.current} of ${context.position.total}`;
      }
      
      if (context && context.state) {
        return `${base}, ${context.state}`;
      }
      
      return base;
    }
  };

  return (
    <AccessibilityContext.Provider value={contextValue}>
      {children}
      
      {/* ARIA Live Region for announcements */}
      <div
        id="aria-live-announcer"
        aria-live={state.ariaLive}
        aria-atomic="true"
        className="sr-only"
        role="status"
      />
      
      {/* Screen reader only skip links */}
      <div className="sr-only">
        <a href="#main-content" data-skip-link className="skip-link">
          Skip to main content
        </a>
        <a href="#navigation" data-skip-link className="skip-link">
          Skip to navigation
        </a>
        <a href="#ai-assistant" data-skip-link className="skip-link">
          Skip to AI assistant
        </a>
      </div>
    </AccessibilityContext.Provider>
  );
}

// Hook to use the accessibility context
export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (context === undefined) {
    throw new Error('useAccessibility must be used within an AccessibilityContextProvider');
  }
  return context;
};

export default AccessibilityContextProvider;