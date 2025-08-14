import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Enhanced Performance Context for optimization and monitoring
const PerformanceContext = createContext();

const initialState = {
  performanceMetrics: {
    renderTime: 0,
    memoryUsage: 0,
    animationFPS: 60,
    apiResponseTime: 0,
    cacheHitRate: 0,
    userInteractionLatency: 0
  },
  optimizationSettings: {
    lazyLoadingEnabled: true,
    animationOptimizationEnabled: true,
    prefetchingEnabled: true,
    memoryOptimizationEnabled: true,
    compressionEnabled: true
  },
  resourceUsage: {
    componentsLoaded: 0,
    assetsLoaded: 0,
    memoryFootprint: 0,
    networkRequests: 0
  },
  debugMode: false,
  performanceHistory: []
};

function performanceReducer(state, action) {
  switch (action.type) {
    case 'UPDATE_METRICS':
      return {
        ...state,
        performanceMetrics: {
          ...state.performanceMetrics,
          ...action.payload
        }
      };
    case 'UPDATE_RESOURCE_USAGE':
      return {
        ...state,
        resourceUsage: {
          ...state.resourceUsage,
          ...action.payload
        }
      };
    case 'TOGGLE_DEBUG_MODE':
      return {
        ...state,
        debugMode: !state.debugMode
      };
    case 'UPDATE_OPTIMIZATION_SETTINGS':
      return {
        ...state,
        optimizationSettings: {
          ...state.optimizationSettings,
          ...action.payload
        }
      };
    case 'ADD_PERFORMANCE_ENTRY':
      return {
        ...state,
        performanceHistory: [
          ...state.performanceHistory.slice(-49), // Keep last 50 entries
          {
            ...action.payload,
            timestamp: Date.now()
          }
        ]
      };
    default:
      return state;
  }
}

export function usePerformance() {
  const context = useContext(PerformanceContext);
  if (!context) {
    throw new Error('usePerformance must be used within a PerformanceContextProvider');
  }
  return context;
}

export default function PerformanceContextProvider({ children }) {
  const [state, dispatch] = useReducer(performanceReducer, initialState);

  // Performance monitoring hooks
  useEffect(() => {
    // Monitor render performance
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.entryType === 'paint') {
          dispatch({
            type: 'UPDATE_METRICS',
            payload: { renderTime: entry.startTime }
          });
        }
      });
    });

    observer.observe({ entryTypes: ['paint', 'measure'] });

    // Monitor memory usage (if supported)
    if (window.performance && window.performance.memory) {
      const checkMemory = () => {
        const memInfo = window.performance.memory;
        dispatch({
          type: 'UPDATE_METRICS',
          payload: {
            memoryUsage: Math.round(memInfo.usedJSHeapSize / 1024 / 1024)
          }
        });
      };

      const memoryInterval = setInterval(checkMemory, 5000);
      return () => {
        clearInterval(memoryInterval);
        observer.disconnect();
      };
    }

    return () => observer.disconnect();
  }, []);

  // FPS monitoring for animations
  useEffect(() => {
    let frameCount = 0;
    let lastTime = performance.now();
    
    const measureFPS = () => {
      frameCount++;
      const currentTime = performance.now();
      
      if (currentTime >= lastTime + 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        dispatch({
          type: 'UPDATE_METRICS',
          payload: { animationFPS: fps }
        });
        
        frameCount = 0;
        lastTime = currentTime;
      }
      
      requestAnimationFrame(measureFPS);
    };

    const rafId = requestAnimationFrame(measureFPS);
    return () => cancelAnimationFrame(rafId);
  }, []);

  // Network performance monitoring
  useEffect(() => {
    const originalFetch = window.fetch;
    let requestCount = 0;
    
    window.fetch = async (...args) => {
      const startTime = performance.now();
      requestCount++;
      
      try {
        const response = await originalFetch(...args);
        const endTime = performance.now();
        const responseTime = endTime - startTime;
        
        dispatch({
          type: 'UPDATE_METRICS',
          payload: { apiResponseTime: Math.round(responseTime) }
        });
        
        dispatch({
          type: 'UPDATE_RESOURCE_USAGE',
          payload: { networkRequests: requestCount }
        });
        
        return response;
      } catch (error) {
        const endTime = performance.now();
        const responseTime = endTime - startTime;
        
        dispatch({
          type: 'ADD_PERFORMANCE_ENTRY',
          payload: {
            type: 'network_error',
            duration: responseTime,
            url: args[0]
          }
        });
        
        throw error;
      }
    };

    return () => {
      window.fetch = originalFetch;
    };
  }, []);

  const contextValue = {
    ...state,
    dispatch,
    // Helper functions
    updateMetrics: (metrics) => dispatch({ type: 'UPDATE_METRICS', payload: metrics }),
    updateResourceUsage: (usage) => dispatch({ type: 'UPDATE_RESOURCE_USAGE', payload: usage }),
    toggleDebugMode: () => dispatch({ type: 'TOGGLE_DEBUG_MODE' }),
    updateOptimizationSettings: (settings) => dispatch({ 
      type: 'UPDATE_OPTIMIZATION_SETTINGS', 
      payload: settings 
    }),
    addPerformanceEntry: (entry) => dispatch({ 
      type: 'ADD_PERFORMANCE_ENTRY', 
      payload: entry 
    }),
    
    // Performance optimization helpers
    isHighPerformanceMode: () => {
      return state.performanceMetrics.animationFPS >= 50 && 
             state.performanceMetrics.memoryUsage < 100;
    },
    
    shouldOptimizeAnimations: () => {
      return state.performanceMetrics.animationFPS < 30 || 
             state.performanceMetrics.memoryUsage > 150;
    },
    
    getPerformanceScore: () => {
      const { animationFPS, memoryUsage, apiResponseTime } = state.performanceMetrics;
      
      let score = 100;
      
      // FPS impact (30% weight)
      if (animationFPS < 30) score -= 30;
      else if (animationFPS < 50) score -= 15;
      
      // Memory impact (25% weight)  
      if (memoryUsage > 200) score -= 25;
      else if (memoryUsage > 100) score -= 10;
      
      // API response impact (25% weight)
      if (apiResponseTime > 2000) score -= 25;
      else if (apiResponseTime > 1000) score -= 10;
      
      // Network requests impact (20% weight)
      if (state.resourceUsage.networkRequests > 50) score -= 20;
      else if (state.resourceUsage.networkRequests > 25) score -= 10;
      
      return Math.max(0, Math.min(100, score));
    }
  };

  return (
    <PerformanceContext.Provider value={contextValue}>
      {children}
    </PerformanceContext.Provider>
  );
}