import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { usePerformance } from '../../contexts/PerformanceContext';
import { Activity, Zap, Monitor, Clock, Cpu, MemoryStick } from 'lucide-react';

export default function PerformanceMonitor() {
  const { performanceScore, metrics, isOptimizationActive } = usePerformance();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Show performance monitor for power users or when optimization is active
    setIsVisible(isOptimizationActive || performanceScore < 70);
  }, [isOptimizationActive, performanceScore]);

  if (!isVisible) return null;

  return (
    <motion.div
      className="fixed bottom-4 right-4 glass-strong border border-gray-700/50 rounded-xl p-4 z-30 w-64"
      initial={{ opacity: 0, y: 20, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.9 }}
    >
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-white font-medium text-sm flex items-center">
          <Activity className="mr-2 text-green-400" size={16} />
          Performance
        </h4>
        <div className={`w-2 h-2 rounded-full ${
          performanceScore >= 90 ? 'bg-green-400' : 
          performanceScore >= 70 ? 'bg-yellow-400' : 'bg-red-400'
        } animate-pulse`} />
      </div>

      <div className="space-y-3">
        {/* Performance Score */}
        <div className="flex items-center justify-between">
          <span className="text-gray-300 text-sm">Score</span>
          <span className={`font-medium ${
            performanceScore >= 90 ? 'text-green-400' : 
            performanceScore >= 70 ? 'text-yellow-400' : 'text-red-400'
          }`}>
            {performanceScore}/100
          </span>
        </div>

        {/* Metrics */}
        {metrics && (
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-gray-800/30 rounded-lg p-2">
              <div className="flex items-center text-gray-400 mb-1">
                <Cpu size={10} className="mr-1" />
                CPU
              </div>
              <div className="text-white font-medium">
                {metrics.cpu || 'N/A'}
              </div>
            </div>
            
            <div className="bg-gray-800/30 rounded-lg p-2">
              <div className="flex items-center text-gray-400 mb-1">
                <MemoryStick size={10} className="mr-1" />
                Memory
              </div>
              <div className="text-white font-medium">
                {metrics.memory || 'N/A'}
              </div>
            </div>
          </div>
        )}

        {/* Optimization Status */}
        {isOptimizationActive && (
          <motion.div
            className="flex items-center justify-center p-2 bg-blue-600/20 rounded-lg"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ repeat: Infinity, duration: 2 }}
          >
            <Zap size={12} className="mr-2 text-blue-400" />
            <span className="text-blue-400 text-xs">Optimizing...</span>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}