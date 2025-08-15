import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  Search, 
  Bookmark, 
  Mic, 
  Sparkles, 
  ChevronUp, 
  ChevronDown 
} from 'lucide-react';

const FloatingActionBar = ({ onActionExecute, isVisible = true }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [quickActions, setQuickActions] = useState([]);

  // Initialize quick actions based on current context
  useEffect(() => {
    const actions = [
      {
        id: 'analyze_page',
        name: 'AI Analyze',
        icon: Brain,
        color: 'text-purple-400',
        description: 'Analyze current page with AI'
      },
      {
        id: 'voice_command',
        name: 'Hey ARIA',
        icon: Mic,
        color: 'text-green-400',
        description: 'Voice commands'
      },
      {
        id: 'smart_search',
        name: 'Smart Search',
        icon: Search,
        color: 'text-blue-400',
        description: 'AI-powered navigation'
      },
      {
        id: 'smart_bookmark',
        name: 'Smart Bookmark',
        icon: Bookmark,
        color: 'text-yellow-400',
        description: 'AI categorized bookmark'
      },
      {
        id: 'quick_summary',
        name: 'Summarize',
        icon: Sparkles,
        color: 'text-pink-400',
        description: 'Quick AI summary'
      },
      {
        id: 'optimize_performance',
        name: 'Optimize',
        icon: Zap,
        color: 'text-orange-400',
        description: 'Performance optimization'
      }
    ];
    
    setQuickActions(actions);
  }, []);

  const handleActionClick = async (action) => {
    try {
      // Execute action through callback
      if (onActionExecute) {
        await onActionExecute(action);
      }
      
      // Auto-collapse after action
      setTimeout(() => setIsExpanded(false), 1000);
    } catch (error) {
      console.error('Action execution failed:', error);
    }
  };

  if (!isVisible) return null;

  return (
    <motion.div
      className="fixed bottom-6 right-6 z-50"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Quick Actions Container */}
      <div className="relative">
        {/* Expanded Actions */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              className="absolute bottom-16 right-0 mb-2"
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.9 }}
              transition={{ duration: 0.2, staggerChildren: 0.05 }}
            >
              <div className="bg-slate-800/95 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-3 shadow-2xl min-w-[200px]">
                <div className="space-y-2">
                  {quickActions.map((action, index) => (
                    <motion.button
                      key={action.id}
                      className="flex items-center gap-3 w-full px-3 py-2 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 transition-all duration-200 group"
                      onClick={() => handleActionClick(action)}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <action.icon 
                        className={`w-4 h-4 ${action.color} group-hover:scale-110 transition-transform`} 
                      />
                      <div className="flex-1 text-left">
                        <div className="text-sm font-medium text-white">
                          {action.name}
                        </div>
                        <div className="text-xs text-slate-400">
                          {action.description}
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main Toggle Button */}
        <motion.button
          className="bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 hover:from-purple-500 hover:via-blue-500 hover:to-cyan-500 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 border border-white/10"
          onClick={() => setIsExpanded(!isExpanded)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.div
            animate={{ rotate: isExpanded ? 180 : 0 }}
            transition={{ duration: 0.3 }}
          >
            {isExpanded ? (
              <ChevronDown className="w-6 h-6" />
            ) : (
              <Sparkles className="w-6 h-6" />
            )}
          </motion.div>
        </motion.button>

        {/* Action Counter Badge */}
        <motion.div
          className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center border-2 border-slate-800"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring" }}
        >
          {quickActions.length}
        </motion.div>
      </div>
    </motion.div>
  );
};

export default FloatingActionBar;