import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Mic, MicOff, Volume2 } from 'lucide-react';

const VoiceCommandInterface = ({ isActive, onToggle, onVoiceCommand }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [confidence, setConfidence] = useState(0);

  const startListening = () => {
    if (!isActive) return;
    
    // Web Speech API integration would go here
    setIsListening(true);
    setTranscript('');
    
    // Simulate voice recognition (in production, use actual Web Speech API)
    setTimeout(() => {
      const mockTranscript = "Hey ARIA, analyze this page";
      setTranscript(mockTranscript);
      setConfidence(0.95);
      
      if (onVoiceCommand) {
        onVoiceCommand({
          transcription: mockTranscript,
          confidence: 0.95,
          wake_word: true
        });
      }
      
      setTimeout(() => {
        setIsListening(false);
        setTranscript('');
      }, 2000);
    }, 2000);
  };

  const stopListening = () => {
    setIsListening(false);
    setTranscript('');
  };

  if (!isActive) return null;

  return (
    <motion.div
      className="fixed top-4 right-4 z-50"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
    >
      <div className="bg-slate-800/95 backdrop-blur-xl border border-slate-700/50 rounded-lg p-4 shadow-xl min-w-[250px]">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Volume2 className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-medium text-white">Voice Commands</span>
          </div>
          <button
            onClick={onToggle}
            className="text-slate-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Voice Input */}
        <div className="space-y-3">
          {/* Microphone Button */}
          <motion.button
            className={`w-full flex items-center justify-center gap-2 p-3 rounded-lg border-2 transition-all duration-300 ${
              isListening
                ? 'bg-red-500/20 border-red-400 text-red-400'
                : 'bg-cyan-500/20 border-cyan-400 text-cyan-400 hover:bg-cyan-500/30'
            }`}
            onClick={isListening ? stopListening : startListening}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isListening ? (
              <>
                <MicOff className="w-5 h-5" />
                Listening...
              </>
            ) : (
              <>
                <Mic className="w-5 h-5" />
                Say "Hey ARIA"
              </>
            )}
          </motion.button>

          {/* Transcript Display */}
          {transcript && (
            <motion.div
              className="bg-slate-700/50 rounded-lg p-3"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="text-sm text-white mb-1">{transcript}</div>
              <div className="text-xs text-slate-400">
                Confidence: {Math.round(confidence * 100)}%
              </div>
            </motion.div>
          )}

          {/* Quick Commands */}
          <div className="space-y-1">
            <div className="text-xs text-slate-400 mb-2">Try saying:</div>
            <div className="grid grid-cols-1 gap-1">
              {[
                "Hey ARIA, analyze this page",
                "Hey ARIA, search for startups",
                "Hey ARIA, bookmark this page",
                "Hey ARIA, summarize content"
              ].map((command, index) => (
                <button
                  key={index}
                  className="text-xs text-left text-slate-300 hover:text-white p-2 rounded hover:bg-slate-700/50 transition-colors"
                  onClick={() => {
                    setTranscript(command);
                    if (onVoiceCommand) {
                      onVoiceCommand({
                        transcription: command,
                        confidence: 1.0,
                        wake_word: true
                      });
                    }
                  }}
                >
                  "{command}"
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default VoiceCommandInterface;