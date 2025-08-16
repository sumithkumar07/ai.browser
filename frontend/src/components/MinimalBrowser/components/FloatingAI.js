import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, X, Sparkles, Lightbulb, BarChart3, 
  BookOpen, Zap, Star, MessageSquare, Eye
} from 'lucide-react';

export default function FloatingAI({ 
  isVisible, 
  onToggle, 
  context, 
  currentUrl, 
  onFeatureActivate 
}) {
  const [activeTab, setActiveTab] = useState('insights');

  // Only show AI when there's meaningful context or user explicitly requests it
  const shouldShowAI = isVisible || (context && context.confidence > 0.7);

  const contextualInsights = context ? [
    {
      icon: Eye,
      title: 'Page Analysis',
      description: 'I can analyze this content for key insights',
      action: () => onFeatureActivate('content_analysis')
    },
    {
      icon: Star,
      title: 'Smart Bookmark',
      description: 'This looks important - bookmark it intelligently?',
      action: () => onFeatureActivate('smart_bookmark')
    },
    {
      icon: Zap,
      title: 'Performance',
      description: 'I can optimize your browser performance',
      action: () => onFeatureActivate('performance_boost')
    }
  ] : [];

  return (
    <>
      {/* Floating AI Button - Bottom Right */}
      <AnimatePresence>
        {shouldShowAI && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => onToggle(!isVisible)}
            className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white shadow-lg hover:shadow-xl transition-shadow z-50"
          >
            <Brain size={24} />
            
            {/* Context Indicator */}
            {context && context.confidence > 0.8 && (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center"
              >
                <Sparkles size={8} className="text-white" />
              </motion.div>
            )}
          </motion.button>
        )}
      </AnimatePresence>

      {/* AI Assistant Panel */}
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed bottom-24 right-6 w-80 bg-white rounded-xl border border-gray-200 shadow-2xl z-50"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-100">
              <div className="flex items-center space-x-2">
                <Brain size={20} className="text-purple-500" />
                <span className="font-medium text-gray-900">AI Assistant</span>
              </div>
              <button
                onClick={() => onToggle(false)}
                className="p-1 hover:bg-gray-100 rounded"
              >
                <X size={16} className="text-gray-500" />
              </button>
            </div>

            {/* Content */}
            <div className="p-4">
              {context ? (
                <div className="space-y-4">
                  <div className="text-sm text-gray-600">
                    I noticed you're on: <span className="font-medium">{currentUrl}</span>
                  </div>
                  
                  <div className="space-y-2">
                    {contextualInsights.map((insight, index) => (
                      <motion.button
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={insight.action}
                        className="w-full text-left p-3 hover:bg-gray-50 rounded-lg flex items-start space-x-3 transition-colors"
                      >
                        <insight.icon size={16} className="text-purple-500 mt-0.5 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-gray-900">
                            {insight.title}
                          </div>
                          <div className="text-xs text-gray-600 mt-1">
                            {insight.description}
                          </div>
                        </div>
                      </motion.button>
                    ))}
                  </div>

                  {/* Quick Actions */}
                  <div className="pt-3 border-t border-gray-100">
                    <div className="text-xs text-gray-500 mb-2">Quick Actions</div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => onFeatureActivate('voice_command')}
                        className="flex-1 px-3 py-2 bg-purple-50 text-purple-600 rounded-lg text-xs font-medium hover:bg-purple-100 transition-colors"
                      >
                        Voice Commands
                      </button>
                      <button
                        onClick={() => onFeatureActivate('tab_organization')}
                        className="flex-1 px-3 py-2 bg-blue-50 text-blue-600 rounded-lg text-xs font-medium hover:bg-blue-100 transition-colors"
                      >
                        Organize Tabs
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-6">
                  <Brain size={32} className="mx-auto text-gray-400 mb-3" />
                  <div className="text-sm text-gray-600 mb-4">
                    I'm ready to help! Browse to a page and I'll provide contextual assistance.
                  </div>
                  <button
                    onClick={() => onFeatureActivate('ai_assistance')}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors"
                  >
                    Show Available Features
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}