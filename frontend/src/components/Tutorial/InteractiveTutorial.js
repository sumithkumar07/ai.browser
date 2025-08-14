import React, { useState, useCallback, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  HelpCircle, 
  ArrowRight, 
  ArrowLeft, 
  X, 
  CheckCircle, 
  Play, 
  Pause,
  SkipForward,
  RotateCcw,
  Book,
  Lightbulb,
  Target,
  Zap,
  Brain,
  Globe,
  MousePointer,
  Keyboard,
  Eye
} from 'lucide-react';
import { useAccessibility } from '../contexts/AccessibilityContext';

// Enhanced Interactive Tutorial Component
export default function InteractiveTutorial({ 
  isOpen, 
  onClose, 
  tutorialType = 'welcome', 
  autoStart = false,
  userExpertiseLevel = 'general' 
}) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(autoStart);
  const [completedSteps, setCompletedSteps] = useState(new Set());
  const [showHints, setShowHints] = useState(true);
  const [progress, setProgress] = useState(0);
  const { announce, shouldAnnounce } = useAccessibility();
  const tutorialRef = useRef(null);
  const stepTimer = useRef(null);

  // Comprehensive tutorial content based on expertise level
  const tutorialContent = {
    welcome: {
      title: "🌟 Welcome to Your Enhanced AI Browser!",
      description: "Let's explore the powerful features that will transform your browsing experience.",
      steps: [
        {
          id: 'bubble-workspace',
          title: "3D Bubble Workspace",
          description: "Your tabs float as interactive 3D bubbles. Drag them around, organize by categories, and enjoy physics-based interactions!",
          target: '.enhanced-bubble-workspace',
          action: "Look around the workspace",
          tip: "Try dragging a bubble tab with your mouse",
          icon: Globe,
          duration: 8000
        },
        {
          id: 'ai-assistant',
          title: "Meet Your AI Assistant",
          description: "ARIA is powered by advanced AI. She learns from your conversations and provides intelligent, context-aware assistance.",
          target: '[data-testid="ai-assistant-toggle"]',
          action: "Click to open AI assistant",
          tip: "Use ⌘K (Ctrl+K) as a quick shortcut",
          icon: Brain,
          duration: 10000
        },
        {
          id: 'view-modes',
          title: "Multiple View Modes",
          description: "Switch between Bubble, Grid, List, and Zen modes. Each optimized for different workflows and preferences.",
          target: '[data-view-mode-toggle]',
          action: "Try different view modes",
          tip: "Press G for Grid, L for List, Space for Zen mode",
          icon: Eye,
          duration: 8000
        },
        {
          id: 'smart-url-bar',
          title: "Smart URL & Search",
          description: "Our enhanced URL bar provides intelligent suggestions from your history, bookmarks, and smart predictions.",
          target: 'input[type="text"]',
          action: "Type something to see suggestions",
          tip: "It learns from your browsing patterns",
          icon: Lightbulb,
          duration: 6000
        },
        {
          id: 'automation-features',
          title: "Powerful Automation",
          description: "Let AI handle repetitive tasks like form filling, booking appointments, and online shopping for you.",
          target: '[data-automation-button]',
          action: "Explore automation features",
          tip: "Perfect for recurring tasks",
          icon: Zap,
          duration: 8000
        }
      ]
    },
    advanced: {
      title: "🚀 Advanced Features Mastery",
      description: "Unlock the full potential of your AI browser with these advanced capabilities.",
      steps: [
        {
          id: 'performance-optimization',
          title: "Performance Optimization",
          description: "Monitor real-time performance metrics, optimize memory usage, and fine-tune your experience.",
          target: '[data-performance-panel]',
          action: "Open performance panel",
          tip: "Check FPS, memory usage, and response times",
          icon: Target,
          duration: 10000
        },
        {
          id: 'batch-automation',
          title: "Batch Content Analysis",
          description: "Analyze multiple websites simultaneously with AI-powered insights and competitive intelligence.",
          target: '[data-batch-analysis]',
          action: "Try batch analysis feature",
          tip: "Process up to 10 URLs at once",
          icon: Brain,
          duration: 12000
        },
        {
          id: 'workflow-optimization',
          title: "Workflow Customization",
          description: "Create custom workflows, set up keyboard shortcuts, and automate your most common tasks.",
          target: '[data-workflow-settings]',
          action: "Access workflow settings",
          tip: "Save 80% of your time with smart workflows",
          icon: Zap,
          duration: 10000
        }
      ]
    },
    accessibility: {
      title: "♿ Accessibility Features",
      description: "Make your browsing experience comfortable and accessible for everyone.",
      steps: [
        {
          id: 'keyboard-navigation',
          title: "Enhanced Keyboard Navigation",
          description: "Navigate the entire interface using just your keyboard with improved focus indicators and shortcuts.",
          target: 'body',
          action: "Press Tab to navigate",
          tip: "Use Arrow keys in bubble workspace",
          icon: Keyboard,
          duration: 8000
        },
        {
          id: 'screen-reader',
          title: "Screen Reader Support",
          description: "Full ARIA compliance with intelligent announcements and structured content for screen readers.",
          target: '#aria-live-announcer',
          action: "Enable screen reader mode",
          tip: "All interactions are announced clearly",
          icon: Eye,
          duration: 10000
        },
        {
          id: 'high-contrast',
          title: "Visual Accessibility",
          description: "High contrast mode, customizable font sizes, and reduced motion options for better visibility.",
          target: '[data-accessibility-settings]',
          action: "Try high contrast mode",
          tip: "Adapts to your system preferences automatically",
          icon: Eye,
          duration: 8000
        }
      ]
    }
  };

  const currentTutorial = tutorialContent[tutorialType] || tutorialContent.welcome;
  const currentStepData = currentTutorial.steps[currentStep];

  // Auto-advance tutorial when playing
  useEffect(() => {
    if (isPlaying && currentStepData && isOpen) {
      stepTimer.current = setTimeout(() => {
        handleNextStep();
      }, currentStepData.duration);
    }

    return () => {
      if (stepTimer.current) {
        clearTimeout(stepTimer.current);
      }
    };
  }, [isPlaying, currentStep, isOpen]);

  // Update progress
  useEffect(() => {
    const newProgress = ((currentStep + 1) / currentTutorial.steps.length) * 100;
    setProgress(newProgress);
  }, [currentStep, currentTutorial.steps.length]);

  // Announce step changes for accessibility
  useEffect(() => {
    if (currentStepData && shouldAnnounce()) {
      announce(
        `Tutorial step ${currentStep + 1} of ${currentTutorial.steps.length}: ${currentStepData.title}. ${currentStepData.description}`,
        'polite'
      );
    }
  }, [currentStep, currentStepData, announce, shouldAnnounce]);

  const handleNextStep = useCallback(() => {
    if (currentStep < currentTutorial.steps.length - 1) {
      setCompletedSteps(prev => new Set([...prev, currentStepData.id]));
      setCurrentStep(currentStep + 1);
    } else {
      handleTutorialComplete();
    }
  }, [currentStep, currentTutorial.steps.length, currentStepData]);

  const handlePreviousStep = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  }, [currentStep]);

  const handleTutorialComplete = useCallback(() => {
    setCompletedSteps(prev => new Set([...prev, currentStepData.id]));
    announce('Tutorial completed! You can now start exploring your enhanced AI browser.', 'assertive');
    
    // Store completion in localStorage
    const completedTutorials = JSON.parse(localStorage.getItem('completedTutorials') || '[]');
    completedTutorials.push({
      type: tutorialType,
      completedAt: new Date().toISOString(),
      userLevel: userExpertiseLevel
    });
    localStorage.setItem('completedTutorials', JSON.stringify(completedTutorials));
    
    setTimeout(() => {
      onClose();
    }, 2000);
  }, [currentStepData, tutorialType, userExpertiseLevel, announce, onClose]);

  const handleSkipTutorial = useCallback(() => {
    announce('Tutorial skipped', 'polite');
    onClose();
  }, [announce, onClose]);

  const highlightTarget = useCallback((selector) => {
    // Remove previous highlights
    document.querySelectorAll('.tutorial-highlight').forEach(el => {
      el.classList.remove('tutorial-highlight');
    });

    // Add highlight to current target
    if (selector && selector !== 'body') {
      const target = document.querySelector(selector);
      if (target) {
        target.classList.add('tutorial-highlight');
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, []);

  useEffect(() => {
    if (currentStepData && isOpen) {
      highlightTarget(currentStepData.target);
    }

    return () => {
      // Cleanup highlights when component unmounts
      document.querySelectorAll('.tutorial-highlight').forEach(el => {
        el.classList.remove('tutorial-highlight');
      });
    };
  }, [currentStepData, isOpen, highlightTarget]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          ref={tutorialRef}
          className="relative bg-gradient-to-br from-gray-900/95 via-purple-900/10 to-blue-900/10 backdrop-blur-xl border border-gray-700/50 rounded-3xl shadow-2xl max-w-2xl w-full mx-4 overflow-hidden"
          initial={{ scale: 0.8, y: 50 }}
          animate={{ scale: 1, y: 0 }}
          exit={{ scale: 0.8, y: 50 }}
          transition={{ type: "spring", stiffness: 300, damping: 25 }}
        >
          {/* Header */}
          <div className="p-6 border-b border-gray-700/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                  <Book size={24} className="text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">{currentTutorial.title}</h2>
                  <p className="text-gray-400">{currentTutorial.description}</p>
                </div>
              </div>
              <button
                onClick={handleSkipTutorial}
                className="w-10 h-10 rounded-full glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                aria-label="Close tutorial"
              >
                <X size={20} />
              </button>
            </div>

            {/* Progress Bar */}
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                <span>Step {currentStep + 1} of {currentTutorial.steps.length}</span>
                <span>{Math.round(progress)}% Complete</span>
              </div>
              <div className="w-full bg-gray-700/50 rounded-full h-2">
                <motion.div
                  className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex items-start space-x-4 mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-600/20 to-blue-600/20 rounded-2xl flex items-center justify-center border border-purple-500/30">
                    <currentStepData.icon size={28} className="text-purple-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-white mb-2">
                      {currentStepData.title}
                    </h3>
                    <p className="text-gray-300 leading-relaxed mb-4">
                      {currentStepData.description}
                    </p>
                    
                    {showHints && currentStepData.tip && (
                      <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
                        <div className="flex items-start space-x-2">
                          <Lightbulb size={16} className="text-yellow-400 mt-0.5" />
                          <div>
                            <p className="text-sm text-yellow-200 font-medium">Quick Tip:</p>
                            <p className="text-sm text-yellow-100">{currentStepData.tip}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Action Button */}
                <div className="bg-gray-800/30 rounded-xl p-4 mb-6">
                  <div className="flex items-center space-x-3">
                    <MousePointer size={16} className="text-blue-400" />
                    <span className="text-blue-200 font-medium">Try it:</span>
                    <span className="text-white">{currentStepData.action}</span>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Controls */}
          <div className="p-6 border-t border-gray-700/30 bg-gray-900/20">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <button
                  onClick={handlePreviousStep}
                  disabled={currentStep === 0}
                  className="w-10 h-10 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                  aria-label="Previous step"
                >
                  <ArrowLeft size={18} />
                </button>

                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="w-10 h-10 rounded-lg glass hover:bg-gray-600/50 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                  aria-label={isPlaying ? "Pause tutorial" : "Play tutorial"}
                >
                  {isPlaying ? <Pause size={18} /> : <Play size={18} />}
                </button>

                <button
                  onClick={() => setShowHints(!showHints)}
                  className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
                    showHints 
                      ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' 
                      : 'glass hover:bg-gray-600/50 text-gray-400 hover:text-white'
                  }`}
                  aria-label="Toggle hints"
                >
                  <Lightbulb size={18} />
                </button>
              </div>

              <div className="flex items-center space-x-3">
                <button
                  onClick={handleSkipTutorial}
                  className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
                >
                  Skip Tutorial
                </button>

                <button
                  onClick={handleNextStep}
                  className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-medium transition-all flex items-center space-x-2 shadow-lg"
                >
                  {currentStep === currentTutorial.steps.length - 1 ? (
                    <>
                      <CheckCircle size={18} />
                      <span>Complete</span>
                    </>
                  ) : (
                    <>
                      <span>Next</span>
                      <ArrowRight size={18} />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Step Indicators */}
          <div className="px-6 pb-4">
            <div className="flex items-center justify-center space-x-2">
              {currentTutorial.steps.map((step, index) => (
                <button
                  key={step.id}
                  onClick={() => setCurrentStep(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentStep
                      ? 'bg-gradient-to-r from-purple-600 to-blue-600 scale-125'
                      : completedSteps.has(step.id)
                      ? 'bg-green-500'
                      : 'bg-gray-600 hover:bg-gray-500'
                  }`}
                  aria-label={`Go to step ${index + 1}: ${step.title}`}
                />
              ))}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}