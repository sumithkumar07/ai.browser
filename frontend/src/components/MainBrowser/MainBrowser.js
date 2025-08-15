import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { useUser } from '../../contexts/UserContext';
import { usePerformance } from '../../contexts/PerformanceContext';
import { useAccessibility } from '../../contexts/AccessibilityContext';

// Import components
import Navigation from '../Navigation/Navigation';
import BubbleTab from '../BubbleTab/BubbleTab';
import EnhancedAIAssistant from '../AIAssistant/EnhancedAIAssistant';
import PerformanceMonitor from '../Performance/PerformanceMonitor';
import InteractiveTutorial from '../Tutorial/InteractiveTutorial';

// Import new feature discovery components
import SmartFeatureHighlight from '../FeatureDiscovery/SmartFeatureHighlight';
import HybridFeaturePanel from '../FeatureDiscovery/HybridFeaturePanel';
import FeatureTooltips from '../FeatureDiscovery/FeatureTooltips';

// Import minimal enhanced features integration
import FloatingActionButton from '../EnhancedFeatures/FloatingActionButton';
// Import comprehensive features panel
import ComprehensiveFeaturesPanel from '../ComprehensiveFeatures/ComprehensiveFeaturesPanel';

// Icons
import { 
  Brain, 
  Sparkles, 
  Zap, 
  Shield, 
  Globe,
  BarChart3,
  Users,
  Lightbulb,
  BookOpen,
  Layers
} from 'lucide-react';

export default function MainBrowser() {
  const { tabs, currentView, addTab, setCurrentView } = useBrowser();
  const { isAssistantVisible, toggleAssistant, hybridFeatures, aiCapabilities } = useAI();
  const { user } = useUser();
  const { performanceScore } = usePerformance();
  const { preferences } = useAccessibility();
  const containerRef = useRef(null);

  // 🚀 Enhanced UI Discovery State
  const [showFeaturePanel, setShowFeaturePanel] = useState(false);
  const [activeTooltip, setActiveTooltip] = useState(null);
  const [discoveryMode, setDiscoveryMode] = useState(false);
  
  // 🚀 Comprehensive Features Panel State
  const [showComprehensiveFeatures, setShowComprehensiveFeatures] = useState(false);

  useEffect(() => {
    // Initialize hybrid AI features on component mount
    if (user && !hybridFeatures?.hybridIntelligence) {
      // Initialize hybrid features
      console.log('Initializing hybrid AI capabilities...');
    }

    // Show discovery mode for new users
    const hasSeenFeatures = localStorage.getItem('hasSeenHybridFeatures');
    if (!hasSeenFeatures) {
      const timer = setTimeout(() => {
        setDiscoveryMode(true);
        localStorage.setItem('hasSeenHybridFeatures', 'true');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [user, hybridFeatures]);

  const handleCreateFirstTab = () => {
    const welcomeTab = {
      id: 'welcome-' + Date.now(),
      title: 'Welcome to Enhanced AI Browser',
      url: 'about:welcome',
      isActive: true,
      content: {
        type: 'welcome',
        data: {
          title: 'AI Agentic Browser - Enhanced Edition',
          subtitle: 'Now with Advanced Hybrid AI Intelligence',
          features: [
            {
              icon: Brain,
              title: 'Advanced AI Analysis',
              description: 'Real-time collaborative analysis, industry-specific intelligence, and visual content understanding'
            },
            {
              icon: Sparkles,
              title: 'Hybrid AI Intelligence',
              description: 'Neon AI + Fellou.ai integration for contextual understanding and workflow automation'
            },
            {
              icon: Zap,
              title: 'Enhanced Automation',
              description: 'Deep Action workflows with intelligent multi-step task execution'
            },
            {
              icon: BarChart3,
              title: 'Professional Reports',
              description: 'Advanced research capabilities with visual report generation and export'
            },
            {
              icon: Users,
              title: 'Collaborative AI',
              description: 'Multiple AI models working together for complex analysis and insights'
            },
            {
              icon: Lightbulb,
              title: 'Predictive Assistance',
              description: 'Behavioral learning with proactive suggestions and workflow optimization'
            }
          ]
        }
      }
    };
    addTab(welcomeTab);
  };

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className={`bg-gradient-to-br ${color} p-4 rounded-xl backdrop-blur-lg border border-white/10`}
    >
      <div className="flex items-center space-x-3">
        <Icon size={24} className="text-white" />
        <div>
          <p className="text-white/80 text-sm">{title}</p>
          <p className="text-white font-semibold text-lg">{value}</p>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div 
      ref={containerRef}
      className={`main-browser h-screen w-screen flex flex-col relative overflow-hidden
        ${preferences.highContrast ? 'high-contrast' : ''}
        ${preferences.reducedMotion ? 'reduced-motion' : ''}
      `}
      style={{ fontSize: preferences.fontSize }}
    >
      {/* Enhanced Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/5 to-transparent" />
      </div>

      {/* Navigation */}
      <Navigation />

      {/* Main Content Area */}
      <div className="flex-1 flex relative">
        {/* Browser Content */}
        <div className="flex-1 flex flex-col">
          {tabs.length === 0 ? (
            /* Enhanced Welcome Screen */
            <motion.div 
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex-1 flex items-center justify-center p-8"
            >
              <div className="max-w-6xl mx-auto text-center space-y-12">
                {/* Hero Section */}
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="space-y-6"
                >
                  <div className="relative">
                    <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white via-purple-200 to-blue-200 mb-4">
                      Welcome to the Enhanced Future
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                      Experience the next generation of AI-powered browsing with advanced hybrid intelligence, 
                      professional-grade automation, and world-class analysis capabilities.
                    </p>
                  </div>

                  {/* Status Cards */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                    <StatCard 
                      icon={Brain} 
                      title="AI Intelligence" 
                      value="Enhanced" 
                      color="from-purple-600/30 to-blue-600/30" 
                    />
                    <StatCard 
                      icon={Sparkles} 
                      title="Hybrid AI" 
                      value={hybridFeatures?.hybridIntelligence ? "Active" : "Ready"} 
                      color="from-blue-600/30 to-cyan-600/30" 
                    />
                    <StatCard 
                      icon={Shield} 
                      title="Performance" 
                      value={`${performanceScore}%`} 
                      color="from-green-600/30 to-emerald-600/30" 
                    />
                    <StatCard 
                      icon={Globe} 
                      title="Mode" 
                      value={user?.subscription || "Power"} 
                      color="from-amber-600/30 to-orange-600/30" 
                    />
                  </div>
                </motion.div>

                {/* Feature Cards */}
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto"
                >
                  {[
                    {
                      icon: Brain,
                      title: "Advanced AI Analysis",
                      description: "Real-time collaboration, industry intelligence, visual & audio analysis",
                      gradient: "from-purple-500/20 to-blue-500/20",
                      border: "border-purple-500/30",
                      features: ["Collaborative Analysis", "Industry-Specific", "Visual Intelligence", "Audio Processing"],
                      featureId: "advanced_ai",
                      isEnhanced: true
                    },
                    {
                      icon: Sparkles,
                      title: "Hybrid AI Intelligence",
                      description: "Neon AI + Fellou.ai integration with behavioral learning",
                      gradient: "from-blue-500/20 to-cyan-500/20",
                      border: "border-blue-500/30",
                      features: ["Neon Chat Enhanced", "Deep Search Pro", "Agentic Memory", "Workflow Builder"],
                      featureId: "hybrid_intelligence",
                      isEnhanced: true,
                      hasNewFeatures: true
                    },
                    {
                      icon: BarChart3,
                      title: "Professional Reports",
                      description: "Research, trends, and visual reports with export capabilities",
                      gradient: "from-green-500/20 to-teal-500/20",
                      border: "border-green-500/30",
                      features: ["Academic Research", "Trend Detection", "Knowledge Graphs", "Visual Reports"],
                      featureId: "professional_reports",
                      isEnhanced: true
                    },
                    {
                      icon: Zap,
                      title: "Creative & Automation",
                      description: "Content generation, code creation, and workflow automation",
                      gradient: "from-amber-500/20 to-orange-500/20",
                      border: "border-amber-500/30",
                      features: ["Content Generation", "Code Creation", "Data Visualization", "Smart Automation"],
                      featureId: "creative_automation",
                      isEnhanced: true
                    }
                  ].map((feature, index) => (
                    <SmartFeatureHighlight
                      key={feature.title}
                      featureId={feature.featureId}
                      title={feature.title}
                      description={feature.description}
                      isNew={feature.hasNewFeatures}
                    >
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 + index * 0.1 }}
                        whileHover={{ scale: 1.02, y: -5 }}
                        className={`relative bg-gradient-to-br ${feature.gradient} backdrop-blur-lg border ${feature.border} rounded-2xl p-6 space-y-4 hover:shadow-2xl transition-all duration-300 cursor-pointer`}
                        onClick={() => setActiveTooltip(activeTooltip === feature.featureId ? null : feature.featureId)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <feature.icon size={28} className="text-white" />
                            <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
                          </div>
                          {feature.isEnhanced && (
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              className="text-xs bg-gradient-to-r from-purple-500/30 to-blue-500/30 text-purple-200 px-2 py-1 rounded-full font-medium"
                            >
                              Enhanced ✨
                            </motion.div>
                          )}
                        </div>
                        <p className="text-gray-300 text-sm leading-relaxed">{feature.description}</p>
                        <div className="space-y-1">
                          {feature.features.map((item, i) => (
                            <div key={i} className="text-xs text-gray-400 flex items-center">
                              <span className="w-1 h-1 bg-gray-400 rounded-full mr-2"></span>
                              {item}
                            </div>
                          ))}
                        </div>
                        
                        <FeatureTooltips
                          isVisible={activeTooltip === feature.featureId}
                          onClose={() => setActiveTooltip(null)}
                          feature={feature.featureId}
                        />
                      </motion.div>
                    </SmartFeatureHighlight>
                  ))}
                </motion.div>

                {/* Action Buttons */}
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                  className="flex flex-wrap justify-center gap-4"
                >
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleCreateFirstTab}
                    className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 transition-all duration-300"
                  >
                    Create Your First Enhanced Tab
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setCurrentView('zen')}
                    className="px-8 py-4 bg-gradient-to-r from-slate-700 to-slate-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-slate-500/25 transition-all duration-300"
                  >
                    Start with Smart Search
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowComprehensiveFeatures(true)}
                    className="px-8 py-4 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 border border-emerald-500/30"
                  >
                    🚀 All 17 Features Ready
                  </motion.button>
                </motion.div>

                {/* Capabilities Preview */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1.0 }}
                  className="text-center space-y-4"
                >
                  <p className="text-gray-400 text-sm">Available AI Capabilities:</p>
                  <div className="flex flex-wrap justify-center gap-2 max-w-4xl mx-auto">
                    {[
                      "Real-time Collaborative Analysis", "Industry-Specific Intelligence", "Visual Content Analysis",
                      "Audio Intelligence", "Creative Content Generation", "Academic Research", "Trend Detection",
                      "Knowledge Graph Building", "Neon Chat Enhanced", "Deep Search Professional", 
                      "Controllable Workflows", "Agentic Memory", "Cross-Platform Integration"
                    ].map((capability, index) => (
                      <motion.span
                        key={capability}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 1.1 + index * 0.05 }}
                        className="px-3 py-1 bg-gray-800/50 text-gray-300 text-xs rounded-full border border-gray-700/50"
                      >
                        {capability}
                      </motion.span>
                    ))}
                  </div>
                </motion.div>
              </div>
            </motion.div>
          ) : (
            /* Browser Tabs Content */
            <div className="flex-1 relative">
              {/* Tabs Header */}
              <div className="flex bg-gray-900/50 border-b border-gray-700/50 px-4 py-2">
                {tabs.map((tab) => (
                  <div
                    key={tab.id}
                    className={`px-4 py-2 mr-2 rounded-t-lg cursor-pointer transition-colors ${
                      tab.isActive 
                        ? 'bg-gray-800 text-white border-t-2 border-purple-500' 
                        : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <span className="text-sm">{tab.title}</span>
                  </div>
                ))}
              </div>

              {/* Tab Content */}
              <div className="flex-1 relative">
                {currentView === 'bubble' && (
                  <div className="absolute inset-0">
                    <BubbleTab />
                  </div>
                )}
                
                {currentView === 'grid' && (
                  <div className="absolute inset-0 p-4">
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 h-full">
                      {tabs.map((tab) => (
                        <motion.div
                          key={tab.id}
                          whileHover={{ scale: 1.02 }}
                          className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-gray-700/50"
                        >
                          <h3 className="text-white font-medium text-sm mb-2">{tab.title}</h3>
                          <p className="text-gray-400 text-xs">{tab.url}</p>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
                
                {currentView === 'list' && (
                  <div className="absolute inset-0 p-4">
                    <div className="space-y-2">
                      {tabs.map((tab) => (
                        <motion.div
                          key={tab.id}
                          whileHover={{ x: 5 }}
                          className="bg-gray-800/50 backdrop-blur-lg rounded-lg p-4 border border-gray-700/50 flex items-center justify-between"
                        >
                          <div>
                            <h3 className="text-white font-medium">{tab.title}</h3>
                            <p className="text-gray-400 text-sm">{tab.url}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
                
                {currentView === 'zen' && (
                  <div className="absolute inset-0 flex items-center justify-center p-8">
                    <div className="max-w-2xl w-full space-y-8">
                      <div className="text-center">
                        <h2 className="text-3xl font-bold text-white mb-4">Zen Mode</h2>
                        <p className="text-gray-400">Focus on what matters with distraction-free browsing</p>
                      </div>
                      
                      <div className="bg-gray-800/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-700/50">
                        <input
                          type="text"
                          placeholder="Enter URL or search with enhanced AI..."
                          className="w-full bg-transparent text-white text-xl placeholder-gray-400 focus:outline-none"
                        />
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                        {["Enhanced Analysis", "Smart Automation", "AI Research", "Creative Tools"].map((feature) => (
                          <div key={feature} className="p-4 bg-gray-800/30 rounded-xl">
                            <p className="text-gray-300 text-sm">{feature}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Enhanced AI Assistant */}
        <AnimatePresence>
          {isAssistantVisible && (
            <motion.div
              key="ai-assistant"
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className="w-96 h-full border-l border-gray-700/50"
            >
              <EnhancedAIAssistant />
            </motion.div>
          )}
        </AnimatePresence>

        {/* AI Assistant Toggle Button */}
        {!isAssistantVisible && (
          <motion.button
            initial={{ x: 100 }}
            animate={{ x: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => toggleAssistant()}
            className="fixed right-6 top-1/2 transform -translate-y-1/2 w-14 h-14 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl shadow-lg hover:shadow-purple-500/25 transition-all duration-300 z-50"
          >
            <Brain size={24} />
          </motion.button>
        )}
      </div>

      {/* Performance Monitor */}
      <PerformanceMonitor />
      
      {/* Interactive Tutorial */}
      <InteractiveTutorial />

      {/* 🚀 ENHANCED FEATURE DISCOVERY PANEL */}
      <HybridFeaturePanel 
        isVisible={showFeaturePanel}
        onClose={() => setShowFeaturePanel(false)}
      />

      {/* Feature Discovery Button */}
      {!showFeaturePanel && (
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowFeaturePanel(true)}
          className="fixed right-6 bottom-6 w-14 h-14 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-white shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 z-50"
          title="Discover Hybrid AI Features"
        >
          <Layers size={24} />
          {/* New Features Indicator */}
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ repeat: Infinity, duration: 2 }}
            className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-xs font-bold"
          >
            6
          </motion.div>
        </motion.button>
      )}

      {/* 🚀 MINIMAL ENHANCED FEATURES INTEGRATION */}
      <FloatingActionButton userId={user?.id || 'anonymous'} />
    </div>
  );
}