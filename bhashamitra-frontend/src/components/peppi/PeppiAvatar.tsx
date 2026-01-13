'use client';

import { motion, AnimatePresence, Variants } from 'framer-motion';
import { usePeppiStore } from '@/stores';
import { cn } from '@/lib/utils';

interface PeppiAvatarProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showBubble?: boolean;
  onClick?: () => void;
  className?: string;
  mood?: 'happy' | 'excited' | 'thinking' | 'encouraging' | 'celebrating' | 'sleepy';
}

const sizeStyles = {
  sm: { container: 'w-16 h-16', svg: 64 },
  md: { container: 'w-24 h-24', svg: 96 },
  lg: { container: 'w-32 h-32', svg: 128 },
  xl: { container: 'w-48 h-48', svg: 192 },
};

const moodAnimations: Record<string, Variants> = {
  happy: {
    idle: { rotate: 0, scale: 1 },
    animate: {
      rotate: [-2, 2, -2],
      scale: [1, 1.02, 1],
      transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
    },
  },
  excited: {
    idle: { rotate: 0, scale: 1, y: 0 },
    animate: {
      y: [-4, 0, -4],
      scale: [1, 1.05, 1],
      transition: { duration: 0.5, repeat: Infinity, ease: 'easeInOut' },
    },
  },
  thinking: {
    idle: { rotate: 0 },
    animate: {
      rotate: [0, -5, 0, 5, 0],
      transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
    },
  },
  encouraging: {
    idle: { scale: 1 },
    animate: {
      scale: [1, 1.1, 1],
      transition: { duration: 1, repeat: Infinity, ease: 'easeInOut' },
    },
  },
  celebrating: {
    idle: { rotate: 0, y: 0 },
    animate: {
      rotate: [-10, 10, -10, 10, 0],
      y: [0, -10, 0, -10, 0],
      transition: { duration: 0.8, repeat: Infinity, ease: 'easeInOut' },
    },
  },
  sleepy: {
    idle: { rotate: 0 },
    animate: {
      rotate: [-3, 3],
      transition: { duration: 3, repeat: Infinity, ease: 'easeInOut', repeatType: 'reverse' as const },
    },
  },
};

export function PeppiAvatar({ size = 'md', showBubble = true, onClick, className, mood: propMood }: PeppiAvatarProps) {
  const store = usePeppiStore();
  // Use prop mood if provided, otherwise fall back to store mood
  const mood = propMood || store.mood;
  const { currentMessage, isTyping } = store;
  const { container, svg } = sizeStyles[size];
  const animation = moodAnimations[mood] || moodAnimations.happy;

  return (
    <div className={cn('relative', className)}>
      {/* Speech Bubble */}
      <AnimatePresence>
        {showBubble && (currentMessage || isTyping) && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.9 }}
            className="absolute -top-2 left-1/2 -translate-x-1/2 -translate-y-full z-10"
          >
            <div className="relative bg-white rounded-2xl shadow-card px-4 py-3 max-w-xs">
              {isTyping ? (
                <div className="flex gap-1">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-primary-400 rounded-full"
                      animate={{ y: [-2, 2, -2] }}
                      transition={{ duration: 0.5, repeat: Infinity, delay: i * 0.15 }}
                    />
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-700 font-medium">{currentMessage}</p>
              )}
              {/* Speech bubble tail */}
              <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white transform rotate-45" />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Peppi Cat SVG */}
      <motion.div
        className={cn(
          container,
          'cursor-pointer transition-shadow hover:drop-shadow-lg'
        )}
        variants={animation}
        initial="idle"
        animate="animate"
        onClick={onClick}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        {/* Peppi SVG - matches landing page design */}
        <svg
          viewBox="0 0 100 100"
          width={svg}
          height={svg}
          className="w-full h-full"
        >
          {/* Ears */}
          <path fill="#F5E6D3" d="M20 40 L10 10 L35 30 Z"/>
          <path fill="#F5E6D3" d="M80 40 L90 10 L65 30 Z"/>
          <path fill="#E8D4C4" d="M18 32 L12 14 L30 28 Z"/>
          <path fill="#E8D4C4" d="M82 32 L88 14 L70 28 Z"/>
          <path fill="#FFCDB8" d="M22 30 L16 18 L32 28 Z"/>
          <path fill="#FFCDB8" d="M78 30 L84 18 L68 28 Z"/>

          {/* Head */}
          <ellipse fill="#F5E6D3" cx="50" cy="50" rx="38" ry="35"/>

          {/* Eyes */}
          <ellipse fill="white" cx="35" cy="48" rx="12" ry="14"/>
          <ellipse fill="white" cx="65" cy="48" rx="12" ry="14"/>
          <motion.ellipse
            fill="#4A90D9"
            cx="35"
            cy="50"
            rx="9"
            ry="11"
            animate={
              mood === 'sleepy'
                ? { ry: [11, 3, 11] as const }
                : mood === 'excited'
                ? { ry: [11, 13, 11] as const }
                : { ry: 11 }
            }
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.ellipse
            fill="#4A90D9"
            cx="65"
            cy="50"
            rx="9"
            ry="11"
            animate={
              mood === 'sleepy'
                ? { ry: [11, 3, 11] as const }
                : mood === 'excited'
                ? { ry: [11, 13, 11] as const }
                : { ry: 11 }
            }
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.ellipse
            fill="#1a1a1a"
            cx="35"
            cy="51"
            rx="4"
            ry="5"
            animate={
              mood === 'sleepy'
                ? { ry: [5, 1, 5] as const }
                : mood === 'excited'
                ? { ry: [5, 6, 5] as const }
                : { ry: 5 }
            }
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.ellipse
            fill="#1a1a1a"
            cx="65"
            cy="51"
            rx="4"
            ry="5"
            animate={
              mood === 'sleepy'
                ? { ry: [5, 1, 5] as const }
                : mood === 'excited'
                ? { ry: [5, 6, 5] as const }
                : { ry: 5 }
            }
            transition={{ duration: 3, repeat: Infinity }}
          />
          {/* Eye shine */}
          <circle fill="white" cx="38" cy="45" r="3"/>
          <circle fill="white" cx="68" cy="45" r="3"/>

          {/* Nose */}
          <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>

          {/* Whiskers */}
          <motion.line
            stroke="#999"
            strokeWidth="1"
            x1="8" y1="52" x2="28" y2="56"
            animate={{ x1: [8, 5, 8] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
          <motion.line
            stroke="#999"
            strokeWidth="1"
            x1="8" y1="60" x2="28" y2="60"
            animate={{ x1: [8, 4, 8] }}
            transition={{ duration: 2, repeat: Infinity, delay: 0.1 }}
          />
          <motion.line
            stroke="#999"
            strokeWidth="1"
            x1="92" y1="52" x2="72" y2="56"
            animate={{ x1: [92, 95, 92] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
          <motion.line
            stroke="#999"
            strokeWidth="1"
            x1="92" y1="60" x2="72" y2="60"
            animate={{ x1: [92, 96, 92] }}
            transition={{ duration: 2, repeat: Infinity, delay: 0.1 }}
          />

          {/* Collar */}
          <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>

          {/* Bell */}
          <circle fill="#FFD700" cx="50" cy="83" r="5"/>
          <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
        </svg>
      </motion.div>

      {/* Mood indicator (small icon) */}
      {mood === 'celebrating' && (
        <motion.div
          className="absolute -top-1 -right-1"
          animate={{ rotate: [0, 15, -15, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 0.5, repeat: Infinity }}
        >
          <span className="text-2xl">⭐</span>
        </motion.div>
      )}
    </div>
  );
}

export default PeppiAvatar;