import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, Brain, Search, Layers, Globe, X, CheckCircle, 
  Settings, Play, Pause, Activity, Cpu, Memory
} from 'lucide-react';
import HybridBrowserService from '../../services/HybridBrowserService';

export default function HybridBrowserPanel({ isVisible, onClose }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [capabilities, setCapabilities] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hybridStatus, setHybridStatus] = useState(null);

  useEffect(() => {
    if (isVisible) {
      loadHybridCapabilities();
    }
  }, [isVisible]);

  const loadHybridCapabilities = async () => {
    setIsLoading(true);
    try {
      const [capabilitiesResult, statusResult] = await Promise.all([
        HybridBrowserService.getAllCapabilities(),
        HybridBrowserService.getHybridBrowserStatus()
      ]);

      if (capabilitiesResult.success) {
        setCapabilities(capabilitiesResult.capabilities);
      }

      if (statusResult.success) {
        setHybridStatus(statusResult);
      }
    } catch (error) {
      console.error('Failed to load hybrid capabilities:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'deep-action', label: 'Deep Actions', icon: Zap },
    { id: 'agentic-memory', label: 'AI Memory', icon: Brain },
    { id: 'deep-search', label: 'Deep Search', icon: Search },
    { id: 'virtual-workspace', label: 'Virtual Workspace', icon: Layers },
    { id: 'browser-engine', label: 'Native Browser', icon: Globe }
  ];

  const OverviewContent = () => (
    <div className="space-y-6">
      <div className="text-center space-y-4">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto"
        >
          <Activity size={32} className="text-white" />
        </motion.div>
        
        <h2 className="text-2xl font-bold text-white">
          🚀 Hybrid AI Browser
        </h2>
        <p className="text-gray-300">
          Neon AI + Fellou.ai capabilities with advanced enhancements
        </p>
      </div>

      {hybridStatus && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-green-600/20 border border-green-500/30 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <CheckCircle size={16} className="text-green-400" />
              <span className="text-green-300 text-sm font-medium">Phase 1</span>
            </div>
            <div className="text-white text-lg font-semibold">Complete</div>
            <div className="text-gray-400 text-xs">Enhanced Web-Based Hybrid</div>
          </div>

          <div className="bg-blue-600/20 border border-blue-500/30 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <CheckCircle size={16} className="text-blue-400" />
              <span className="text-blue-300 text-sm font-medium">Phase 2</span>
            </div>
            <div className="text-white text-lg font-semibold">Complete</div>
            <div className="text-gray-400 text-xs">Browser Engine Foundation</div>
          </div>

          <div className="bg-purple-600/20 border border-purple-500/30 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <CheckCircle size={16} className="text-purple-400" />
              <span className="text-purple-300 text-sm font-medium">Phase 3</span>
            </div>
            <div className="text-white text-lg font-semibold">Ready</div>
            <div className="text-gray-400 text-xs">Native Browser Engine</div>
          </div>
        </div>
      )}

      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-white">🌟 Hybrid Advantages</h3>
        <div className="space-y-2">
          {[
            "All Neon AI capabilities: Contextual understanding + real-time intelligence",
            "All Fellou.ai capabilities: Deep actions + agentic memory + controllable workflows",
            "Advanced AI analysis with multi-model collaboration",
            "Virtual workspace with shadow window operations",
            "Native browser engine with full OS integration"
          ].map((advantage, index) => (
            <div key={index} className="flex items-start space-x-2 text-gray-300 text-sm">
              <CheckCircle size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
              <span>{advantage}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const FeatureContent = ({ feature, data }) => {
    if (!data || !data.success) {
      return (
        <div className="text-center py-8">
          <div className="text-gray-400">Feature data unavailable</div>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="text-center">
          <h3 className="text-xl font-bold text-white mb-2">
            {feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </h3>
          <p className="text-gray-300 text-sm">
            {data.implementation_status || 'Fully Operational'}
          </p>
        </div>

        {data.capabilities && (
          <div className="space-y-4">
            {Object.entries(data.capabilities).map(([key, value]) => (
              <div key={key} className="bg-gray-800/50 rounded-lg p-4">
                <h4 className="text-white font-medium mb-2 capitalize">
                  {key.replace(/_/g, ' ')}
                </h4>
                {Array.isArray(value) ? (
                  <div className="space-y-1">
                    {value.map((item, index) => (
                      <div key={index} className="text-gray-300 text-sm flex items-center space-x-2">
                        <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                        <span>{item}</span>
                      </div>
                    ))}
                  </div>
                ) : typeof value === 'object' ? (
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    {Object.entries(value).map(([subKey, subValue]) => (
                      <div key={subKey} className="text-gray-300">
                        <span className="capitalize">{subKey.replace(/_/g, ' ')}: </span>
                        <span className="text-blue-300">{String(subValue)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-300 text-sm">{String(value)}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-gray-900/95 backdrop-blur-lg border border-gray-700/50 rounded-2xl w-full max-w-6xl h-[80vh] overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700/50">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
              <Activity size={20} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Hybrid Browser Control Center</h1>
              <p className="text-gray-400 text-sm">All 3 phases implemented • Neon AI + Fellou.ai + Advanced AI</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X size={20} className="text-gray-400" />
          </button>
        </div>

        <div className="flex h-full">
          {/* Sidebar */}
          <div className="w-64 border-r border-gray-700/50 p-4 space-y-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors text-left ${
                  activeTab === tab.id
                    ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30'
                    : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
                }`}
              >
                <tab.icon size={18} />
                <span className="text-sm font-medium">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Main Content */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-6">
              {isLoading ? (
                <div className="flex items-center justify-center h-64">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                </div>
              ) : (
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.2 }}
                  >
                    {activeTab === 'overview' && <OverviewContent />}
                    {activeTab === 'deep-action' && capabilities && (
                      <FeatureContent 
                        feature="deep_action_technology" 
                        data={capabilities.deep_action_technology} 
                      />
                    )}
                    {activeTab === 'agentic-memory' && capabilities && (
                      <FeatureContent 
                        feature="agentic_memory_system" 
                        data={capabilities.agentic_memory_system} 
                      />
                    )}
                    {activeTab === 'deep-search' && capabilities && (
                      <FeatureContent 
                        feature="deep_search_integration" 
                        data={capabilities.deep_search_integration} 
                      />
                    )}
                    {activeTab === 'virtual-workspace' && capabilities && (
                      <FeatureContent 
                        feature="virtual_workspace" 
                        data={capabilities.virtual_workspace} 
                      />
                    )}
                    {activeTab === 'browser-engine' && capabilities && (
                      <FeatureContent 
                        feature="browser_engine_foundation" 
                        data={capabilities.browser_engine_foundation} 
                      />
                    )}
                  </motion.div>
                </AnimatePresence>
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}