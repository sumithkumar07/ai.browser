import React from 'react';
import { motion } from 'framer-motion';

export default function MinimalHeader({ children }) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="minimal-header bg-white border-b border-gray-200 px-4 py-3"
    >
      <div className="flex items-center justify-between space-x-4">
        {children}
      </div>
    </motion.header>
  );
}