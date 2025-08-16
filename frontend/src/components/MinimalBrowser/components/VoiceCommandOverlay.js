import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Volume2, X } from 'lucide-react';

export default function VoiceCommandOverlay({ 
  isVisible, 
  onClose, 
  onCommand 
}) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [confidence, setConfidence] = useState(0);

  const voiceCommands = [
    { trigger: 'Hey Browser, analyze this page', description: 'Analyze current page content' },
    { trigger: 'Hey Browser, bookmark this', description: 'Smart bookmark current page' },
    { trigger: 'Hey Browser, organize tabs', description: 'Organize tabs intelligently' },
    { trigger: 'Hey Browser, optimize performance', description: 'Boost browser performance' },
    { trigger: 'Hey Browser, search for [query]', description: 'Perform smart search' },
    { trigger: 'Hey Browser, go to [website]', description: 'Navigate to website' }
  ];

  const startListening = () => {
    setIsListening(true);
    setTranscript('');
    
    // Simulate voice recognition (in real app, use Web Speech API)
    setTimeout(() => {
      setTranscript('Listening for "Hey Browser" commands...');
      setConfidence(0.8);
    }, 500);
  };

  const stopListening = () => {
    setIsListening(false);
    if (transcript.includes('Hey Browser')) {
      onCommand(transcript);
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                  <Mic size={20} className="text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Voice Commands</h3>
                  <p className="text-gray-600 text-sm">Say "Hey Browser" to start</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-lg text-gray-500"
              >
                <X size={20} />
              </button>
            </div>

            {/* Voice Visualization */}
            <div className="text-center mb-6">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={isListening ? stopListening : startListening}
                className={`w-20 h-20 rounded-full flex items-center justify-center transition-all ${
                  isListening 
                    ? 'bg-red-500 hover:bg-red-600' 
                    : 'bg-blue-500 hover:bg-blue-600'
                }`}
              >
                {isListening ? (
                  <MicOff size={32} className="text-white" />
                ) : (
                  <Mic size={32} className="text-white" />
                )}
              </motion.button>
              
              <div className="mt-4">
                <div className={`text-sm font-medium ${isListening ? 'text-red-600' : 'text-gray-600'}`}>
                  {isListening ? 'Listening...' : 'Tap to start listening'}
                </div>
                
                {transcript && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-2 p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="text-sm text-gray-700">{transcript}</div>
                    {confidence > 0 && (
                      <div className="text-xs text-gray-500 mt-1">
                        Confidence: {Math.round(confidence * 100)}%
                      </div>
                    )}
                  </motion.div>
                )}
              </div>
            </div>

            {/* Available Commands */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-gray-900 mb-3">Available Commands</h4>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {voiceCommands.map((command, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
                    onClick={() => {
                      onCommand(command.trigger);
                      onClose();
                    }}
                  >
                    <div className="text-sm font-medium text-purple-700 mb-1">
                      {command.trigger}
                    </div>
                    <div className="text-xs text-gray-600">
                      {command.description}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Status */}
            <div className="mt-6 p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-2 text-blue-700">
                <Volume2 size={16} />
                <span className="text-sm font-medium">Voice Recognition Active</span>
              </div>
              <p className="text-xs text-blue-600 mt-1">
                All commands are processed locally for privacy
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}