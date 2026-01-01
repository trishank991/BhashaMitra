'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { soundService } from '@/lib/soundService';

interface SuccessCheckProps {
  /** Whether to show the animation */
  show: boolean;
  /** Callback when animation completes */
  onComplete?: () => void;
  /** Size of the checkmark */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Whether to play sound */
  playSound?: boolean;
  /** Custom class name */
  className?: string;
}

const SIZES = {
  sm: 48,
  md: 64,
  lg: 96,
  xl: 128,
};

/**
 * Animated success checkmark for correct answers.
 *
 * Shows a satisfying checkmark animation with optional sound.
 * Great for quiz answers, completed tasks, etc.
 *
 * @example
 * ```tsx
 * <SuccessCheck
 *   show={isCorrect}
 *   onComplete={() => moveToNextQuestion()}
 * />
 * ```
 */
export function SuccessCheck({
  show,
  onComplete,
  size = 'md',
  playSound = true,
  className = '',
}: SuccessCheckProps) {
  const dimension = SIZES[size];

  useEffect(() => {
    if (show && playSound) {
      soundService.onCorrect();
    }
  }, [show, playSound]);

  useEffect(() => {
    if (show && onComplete) {
      const timer = setTimeout(onComplete, 1200);
      return () => clearTimeout(timer);
    }
  }, [show, onComplete]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className={`flex items-center justify-center ${className}`}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
        >
          <svg
            width={dimension}
            height={dimension}
            viewBox="0 0 100 100"
            className="drop-shadow-lg"
          >
            {/* Background circle */}
            <motion.circle
              cx="50"
              cy="50"
              r="45"
              fill="#10B981"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15 }}
            />

            {/* Outer ring pulse */}
            <motion.circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="#10B981"
              strokeWidth="3"
              initial={{ scale: 1, opacity: 1 }}
              animate={{ scale: 1.5, opacity: 0 }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
            />

            {/* Checkmark path */}
            <motion.path
              d="M30 50 L45 65 L70 35"
              fill="none"
              stroke="white"
              strokeWidth="8"
              strokeLinecap="round"
              strokeLinejoin="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ delay: 0.2, duration: 0.4, ease: 'easeOut' }}
            />
          </svg>

          {/* Sparkles */}
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-yellow-400 rounded-full"
              initial={{
                x: 0,
                y: 0,
                scale: 0,
                opacity: 1,
              }}
              animate={{
                x: Math.cos((i * Math.PI * 2) / 6) * dimension * 0.8,
                y: Math.sin((i * Math.PI * 2) / 6) * dimension * 0.8,
                scale: [0, 1.5, 0],
                opacity: [1, 1, 0],
              }}
              transition={{
                delay: 0.3,
                duration: 0.6,
                ease: 'easeOut',
              }}
            />
          ))}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default SuccessCheck;
