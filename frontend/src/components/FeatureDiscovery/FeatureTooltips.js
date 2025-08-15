import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const FeatureTooltips = ({ isVisible, onClose, feature }) => {
  const [currentTip, setCurrentTip] = useState(0);

  const featureTips = {
    "advanced_ai": [
      {
        title: "🧠 Smart Bookmark Intelligence",
        description: "AI automatically categorizes and organizes your bookmarks with predictive insights",
        action: "Try saving any webpage to see AI organization in action"
      },
      {
        title: "🎯 Context-Aware Suggestions", 
        description: "Get proactive AI recommendations based on your current activity and browsing patterns",
        action: "AI learns your patterns and suggests next steps automatically"
      },
      {
        title: "🔌 AI Browser Plugins",
        description: "Generate custom browser plugins with AI - just describe what you need",
        action: "Ask ARIA to create a custom plugin for any task"
      }
    ],
    "hybrid_intelligence": [
      {
        title: "🌉 Seamless Neon + Fellou Integration",
        description: "Perfect harmony between contextual AI and workflow orchestration",
        action: "All features work together automatically for enhanced results"
      },
      {
        title: "🤝 Real-Time Collaboration",
        description: "AI-assisted multi-user collaboration with smart conflict resolution",
        action: "Share sessions with team members for enhanced productivity"
      },
      {
        title: "🔮 Predictive Caching",
        description: "AI pre-loads content you'll likely need based on your behavior patterns",
        action: "Experience faster browsing with intelligent predictions"
      }
    ],
    "professional_reports": [
      {
        title: "📊 Enhanced Visual Reports",
        description: "Professional reports with charts, infographics, and multiple export formats",
        action: "Generate comprehensive research reports with visual elements"
      },
      {
        title: "🔍 Deep Search Professional",
        description: "Multi-source research compilation with competitive analysis",
        action: "Create professional research reports with citations and visuals"
      }
    ]
  };

  const tips = featureTips[feature] || [];

  useEffect(() => {
    if (isVisible && tips.length > 1) {
      const timer = setInterval(() => {
        setCurrentTip((prev) => (prev + 1) % tips.length);
      }, 4000);
      return () => clearInterval(timer);
    }
  }, [isVisible, tips.length]);

  if (!isVisible || tips.length === 0) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, scale: 0.8, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.8, y: 20 }}
        className="absolute top-full left-0 mt-2 z-50 w-80 p-4 bg-gradient-to-r from-purple-900/95 to-blue-900/95 backdrop-blur-md rounded-xl border border-purple-500/30 shadow-2xl"
      >
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-lg font-semibold text-white">{tips[currentTip]?.title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>
        
        <p className="text-gray-200 text-sm mb-3 leading-relaxed">
          {tips[currentTip]?.description}
        </p>
        
        <div className="bg-gradient-to-r from-purple-600/30 to-blue-600/30 rounded-lg p-2 mb-3">
          <p className="text-purple-200 text-xs font-medium">
            💡 {tips[currentTip]?.action}
          </p>
        </div>

        {tips.length > 1 && (
          <div className="flex justify-center space-x-1">
            {tips.map((_, index) => (
              <div
                key={index}
                className={`h-1.5 w-1.5 rounded-full transition-all ${
                  index === currentTip ? 'bg-purple-400 w-4' : 'bg-gray-500'
                }`}
              />
            ))}
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  );
};

export default FeatureTooltips;