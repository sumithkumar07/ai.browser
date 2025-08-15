import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const SmartFeatureHighlight = ({ children, featureId, title, description, isNew = false }) => {
  const [isHighlighted, setIsHighlighted] = useState(false);
  const [hasBeenSeen, setHasBeenSeen] = useState(false);

  useEffect(() => {
    // Check if user has seen this feature before
    const seenFeatures = JSON.parse(localStorage.getItem('seenFeatures') || '[]');
    setHasBeenSeen(seenFeatures.includes(featureId));

    // Auto-highlight new features for first-time users
    if (isNew && !seenFeatures.includes(featureId)) {
      const timer = setTimeout(() => {
        setIsHighlighted(true);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [featureId, isNew]);

  const handleInteraction = () => {
    if (!hasBeenSeen) {
      const seenFeatures = JSON.parse(localStorage.getItem('seenFeatures') || '[]');
      seenFeatures.push(featureId);
      localStorage.setItem('seenFeatures', JSON.stringify(seenFeatures));
      setHasBeenSeen(true);
    }
    setIsHighlighted(false);
  };

  return (
    <div 
      className="relative"
      onMouseEnter={() => setIsHighlighted(true)}
      onMouseLeave={() => setIsHighlighted(false)}
      onClick={handleInteraction}
    >
      {children}
      
      {/* New Feature Badge */}
      {isNew && !hasBeenSeen && (
        <motion.div
          initial={{ scale: 0, rotate: -45 }}
          animate={{ scale: 1, rotate: 0 }}
          className="absolute -top-2 -right-2 bg-gradient-to-r from-green-400 to-emerald-500 text-white text-xs px-2 py-1 rounded-full font-bold shadow-lg z-10"
        >
          NEW
        </motion.div>
      )}

      {/* Enhanced Feature Badge */}
      {!isNew && featureId.includes('enhanced') && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute -top-1 -right-1 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-xs px-1.5 py-0.5 rounded-full font-bold shadow-lg z-10"
        >
          ✨
        </motion.div>
      )}

      {/* Highlight Glow Effect */}
      {isHighlighted && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-xl blur-sm -z-10"
          style={{
            filter: 'blur(8px)',
            transform: 'scale(1.05)'
          }}
        />
      )}

      {/* Feature Description Tooltip */}
      {isHighlighted && description && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-64 p-3 bg-black/90 backdrop-blur-md rounded-lg border border-purple-500/30 shadow-xl z-20"
        >
          <h4 className="text-white font-semibold text-sm mb-1">{title}</h4>
          <p className="text-gray-300 text-xs leading-relaxed">{description}</p>
          
          {/* Arrow */}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-black/90" />
        </motion.div>
      )}
    </div>
  );
};

export default SmartFeatureHighlight;