import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, Bookmark, Zap, Eye, BarChart3, 
  Sparkles, MessageSquare, Star, Layers
} from 'lucide-react';

export default function ContextualMenu({ 
  isVisible, 
  position, 
  context, 
  onClose, 
  onFeatureSelect 
}) {
  const contextualFeatures = [
    {
      id: 'content_analysis',
      icon: Eye,
      title: 'Analyze Content',
      description: 'AI analysis of current page',
      condition: () => context && context.page_content
    },
    {
      id: 'smart_bookmark',
      icon: Bookmark,
      title: 'Smart Bookmark',
      description: 'Intelligently categorize and save',
      condition: () => context && context.current_url !== 'about:blank'
    },
    {
      id: 'performance_boost',
      icon: Zap,
      title: 'Performance Boost',
      description: 'Optimize browser performance',
      condition: () => true
    },
    {
      id: 'tab_organization',
      icon: Layers,
      title: 'Organize Tabs',
      description: 'Smart tab grouping',
      condition: () => context && context.recent_actions?.length > 3
    },
    {
      id: 'ai_assistance',
      icon: Brain,
      title: 'AI Help',
      description: 'Get contextual assistance',
      condition: () => true
    }
  ];

  const availableFeatures = contextualFeatures.filter(feature => feature.condition());

  return (
    <AnimatePresence>
      {isVisible && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40"
          />
          
          {/* Context Menu */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            style={{
              left: position.x,
              top: position.y,
              transform: 'translateY(-10px)'
            }}
            className="fixed bg-white rounded-lg border border-gray-200 shadow-xl z-50 min-w-[200px] overflow-hidden"
          >
            <div className="py-2">
              {availableFeatures.map((feature, index) => (
                <motion.button
                  key={feature.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => {
                    onFeatureSelect(feature.id);
                    onClose();
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-gray-50 flex items-center space-x-3 transition-colors"
                >
                  <feature.icon size={16} className="text-gray-600 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900">
                      {feature.title}
                    </div>
                    <div className="text-xs text-gray-500">
                      {feature.description}
                    </div>
                  </div>
                </motion.button>
              ))}
              
              {availableFeatures.length === 0 && (
                <div className="px-4 py-3 text-sm text-gray-500 text-center">
                  No contextual features available
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}