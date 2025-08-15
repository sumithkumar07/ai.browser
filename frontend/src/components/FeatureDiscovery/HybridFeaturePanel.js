import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAI } from '../../contexts/AIContext';

const HybridFeaturePanel = ({ isVisible, onClose }) => {
  const { aiCapabilities, hybridFeatures } = useAI();
  const [activeTab, setActiveTab] = useState('neon');
  const [discoveredFeatures, setDiscoveredFeatures] = useState(0);

  useEffect(() => {
    // Count discovered features
    const totalFeatures = Object.keys(hybridFeatures).length;
    const activeFeatures = Object.values(hybridFeatures).filter(Boolean).length;
    setDiscoveredFeatures(activeFeatures);
  }, [hybridFeatures]);

  const neonFeatures = [
    {
      icon: "🧠",
      name: "Neon Chat Enhanced V2",
      description: "Advanced contextual understanding with 50-message memory and behavioral learning",
      status: aiCapabilities.neonAI?.neonChat ? "active" : "inactive",
      isNew: true
    },
    {
      icon: "🔍", 
      name: "Neon Focus Mode",
      description: "AI-powered distraction filtering and content optimization for enhanced reading",
      status: aiCapabilities.neonAI?.neonFocus ? "active" : "inactive",
      isNew: true
    },
    {
      icon: "📊",
      name: "Neon Intelligence",
      description: "Real-time page analysis with smart automation opportunity detection",
      status: aiCapabilities.neonAI?.neonIntelligence ? "active" : "inactive",
      isNew: true
    },
    {
      icon: "🛠️",
      name: "Neon Make Professional",  
      description: "Generate professional-grade applications with advanced templates and features",
      status: aiCapabilities.neonAI?.neonMake ? "active" : "inactive",
      isNew: false
    }
  ];

  const fellouFeatures = [
    {
      icon: "🔍",
      name: "Deep Search Professional",
      description: "Multi-source research with visual reports and professional export formats",
      status: aiCapabilities.fellouAI?.deepSearch ? "active" : "inactive",
      isNew: false
    },
    {
      icon: "🎭",
      name: "Deep Action Orchestration",
      description: "Multi-step workflow automation with intelligent error handling and recovery",
      status: aiCapabilities.fellouAI?.deepAction ? "active" : "inactive",
      isNew: false
    },
    {
      icon: "🧠",
      name: "Agentic Memory Enhanced", 
      description: "Advanced behavioral learning with 200-message history and predictive insights",
      status: aiCapabilities.fellouAI?.agenticMemory ? "active" : "inactive",
      isNew: true
    },
    {
      icon: "🎯",
      name: "Controllable Workflow Builder",
      description: "Visual drag-and-drop workflow designer with real-time collaboration features",
      status: aiCapabilities.fellouAI?.controllableWorkflow ? "active" : "inactive",
      isNew: true
    }
  ];

  const advancedFeatures = [
    {
      icon: "🔖",
      name: "Smart Bookmark Intelligence",
      description: "AI-powered bookmark organization with predictive categorization and insights",
      status: "active",
      isNew: true
    },
    {
      icon: "🎯",
      name: "Context-Aware Suggestions",
      description: "Proactive recommendations based on real-time context and behavioral patterns",
      status: "active", 
      isNew: true
    },
    {
      icon: "🔌",
      name: "AI Browser Plugins",
      description: "Generate custom browser plugins on-demand with complete functionality",
      status: "active",
      isNew: true
    },
    {
      icon: "🤝",
      name: "Real-Time Collaboration",
      description: "Multi-user AI-assisted collaboration with intelligent conflict resolution",
      status: "active",
      isNew: true
    },
    {
      icon: "🔮",
      name: "Predictive Content Caching",
      description: "AI pre-loads content based on behavioral prediction for enhanced performance",
      status: "active",
      isNew: true
    }
  ];

  const currentFeatures = activeTab === 'neon' ? neonFeatures : 
                         activeTab === 'fellou' ? fellouFeatures : advancedFeatures;

  if (!isVisible) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, x: 300 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 300 }}
        className="fixed right-4 top-20 w-96 max-h-[calc(100vh-6rem)] bg-gradient-to-b from-slate-900/95 to-purple-900/95 backdrop-blur-md rounded-xl border border-purple-500/30 shadow-2xl z-50 overflow-hidden"
      >
        {/* Header */}
        <div className="p-4 border-b border-purple-500/30">
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-xl font-bold text-white">🚀 Hybrid AI Features</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>
          
          <div className="text-sm text-purple-200 mb-3">
            {discoveredFeatures} active features • Next-generation AI capabilities
          </div>

          {/* Tabs */}
          <div className="flex space-x-1 bg-black/30 rounded-lg p-1">
            {[
              { id: 'neon', label: '🧠 Neon AI', count: neonFeatures.filter(f => f.status === 'active').length },
              { id: 'fellou', label: '🚀 Fellou.ai', count: fellouFeatures.filter(f => f.status === 'active').length },
              { id: 'advanced', label: '✨ Advanced', count: advancedFeatures.length }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-3 py-2 rounded-md text-xs font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-purple-600 text-white'
                    : 'text-gray-300 hover:text-white hover:bg-purple-600/50'
                }`}
              >
                {tab.label}
                <span className="ml-1 text-xs opacity-75">({tab.count})</span>
              </button>
            ))}
          </div>
        </div>

        {/* Features List */}
        <div className="p-4 overflow-y-auto max-h-96 custom-scrollbar">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-3"
            >
              {currentFeatures.map((feature, index) => (
                <motion.div
                  key={feature.name}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`relative p-3 rounded-lg border transition-all ${
                    feature.status === 'active'
                      ? 'bg-gradient-to-r from-purple-600/20 to-blue-600/20 border-purple-500/30'
                      : 'bg-gray-800/50 border-gray-600/30'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      <span className="text-2xl">{feature.icon}</span>
                      <div className="flex-1">
                        <h3 className={`font-semibold text-sm ${
                          feature.status === 'active' ? 'text-white' : 'text-gray-400'
                        }`}>
                          {feature.name}
                        </h3>
                        <p className={`text-xs mt-1 leading-relaxed ${
                          feature.status === 'active' ? 'text-gray-300' : 'text-gray-500'
                        }`}>
                          {feature.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {feature.isNew && (
                        <span className="bg-green-500 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                          NEW
                        </span>
                      )}
                      <div className={`w-2 h-2 rounded-full ${
                        feature.status === 'active' ? 'bg-green-400' : 'bg-gray-500'
                      }`} />
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-purple-500/30 bg-gradient-to-r from-purple-600/10 to-blue-600/10">
          <div className="text-xs text-purple-200 text-center">
            🌟 All features work seamlessly together for enhanced productivity
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default HybridFeaturePanel;