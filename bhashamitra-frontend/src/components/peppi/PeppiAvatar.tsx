'use client';

import { motion, AnimatePresence, Variants } from 'framer-motion';
import { usePeppiStore } from '@/stores';
import { cn } from '@/lib/utils';

interface PeppiAvatarProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showBubble?: boolean;
  onClick?: () => void;
  className?: string;
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

export function PeppiAvatar({ size = 'md', showBubble = true, onClick, className }: PeppiAvatarProps) {
  const { mood, currentMessage, isTyping } = usePeppiStore();
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
        <svg
          viewBox="0 0 200 200"
          width={svg}
          height={svg}
          className="w-full h-full"
        >
          {/* Body - Cream colored fluffy body */}
          <ellipse
            cx="100"
            cy="130"
            rx="60"
            ry="50"
            fill="#F5E6D3"
            stroke="#E8D5C4"
            strokeWidth="2"
          />

          {/* Head - Ragdoll characteristic round face */}
          <circle
            cx="100"
            cy="80"
            r="55"
            fill="#F5E6D3"
            stroke="#E8D5C4"
            strokeWidth="2"
          />

          {/* Ears - Pointed with orange tips */}
          <g>
            {/* Left ear */}
            <path
              d="M55 45 L45 15 L75 35 Z"
              fill="#F5E6D3"
              stroke="#E8D5C4"
              strokeWidth="2"
            />
            <path
              d="M52 38 L48 20 L68 34 Z"
              fill="#E8A87C"
            />
            {/* Right ear */}
            <path
              d="M145 45 L155 15 L125 35 Z"
              fill="#F5E6D3"
              stroke="#E8D5C4"
              strokeWidth="2"
            />
            <path
              d="M148 38 L152 20 L132 34 Z"
              fill="#E8A87C"
            />
          </g>

          {/* Face markings - Orange/saffron color points (Ragdoll pattern) */}
          <ellipse
            cx="100"
            cy="95"
            rx="35"
            ry="25"
            fill="#E8A87C"
            opacity="0.6"
          />

          {/* Eyes - Big expressive blue eyes */}
          <g>
            {/* Left eye white */}
            <ellipse cx="75" cy="75" rx="18" ry="20" fill="white" />
            {/* Left eye iris */}
            <motion.ellipse
              cx="75"
              cy="75"
              rx="12"
              ry="14"
              fill="#4A90D9"
              animate={
                mood === 'sleepy'
                  ? { ry: [14, 3, 14] }
                  : mood === 'excited'
                  ? { ry: [14, 16, 14] }
                  : {}
              }
              transition={{ duration: 3, repeat: Infinity }}
            />
            {/* Left eye pupil */}
            <motion.ellipse
              cx="75"
              cy="75"
              rx="6"
              ry="8"
              fill="#1A1A2E"
              animate={
                mood === 'sleepy'
                  ? { ry: [8, 2, 8] }
                  : mood === 'excited'
                  ? { ry: [8, 10, 8] }
                  : {}
              }
              transition={{ duration: 3, repeat: Infinity }}
            />
            {/* Left eye shine */}
            <circle cx="70" cy="70" r="4" fill="white" opacity="0.8" />

            {/* Right eye white */}
            <ellipse cx="125" cy="75" rx="18" ry="20" fill="white" />
            {/* Right eye iris */}
            <motion.ellipse
              cx="125"
              cy="75"
              rx="12"
              ry="14"
              fill="#4A90D9"
              animate={
                mood === 'sleepy'
                  ? { ry: [14, 3, 14] }
                  : mood === 'excited'
                  ? { ry: [14, 16, 14] }
                  : {}
              }
              transition={{ duration: 3, repeat: Infinity }}
            />
            {/* Right eye pupil */}
            <motion.ellipse
              cx="125"
              cy="75"
              rx="6"
              ry="8"
              fill="#1A1A2E"
              animate={
                mood === 'sleepy'
                  ? { ry: [8, 2, 8] }
                  : mood === 'excited'
                  ? { ry: [8, 10, 8] }
                  : {}
              }
              transition={{ duration: 3, repeat: Infinity }}
            />
            {/* Right eye shine */}
            <circle cx="120" cy="70" r="4" fill="white" opacity="0.8" />
          </g>

          {/* Nose - Pink triangular nose */}
          <path
            d="M100 95 L94 103 L106 103 Z"
            fill="#FFB6C1"
            stroke="#E8A0A8"
            strokeWidth="1"
          />

          {/* Mouth - Cute cat smile */}
          <motion.path
            d="M94 108 Q100 115 106 108"
            fill="none"
            stroke="#8B7355"
            strokeWidth="2"
            strokeLinecap="round"
            animate={
              mood === 'celebrating'
                ? { d: ['M94 108 Q100 120 106 108', 'M94 108 Q100 115 106 108'] }
                : mood === 'sleepy'
                ? { d: 'M94 108 Q100 110 106 108' }
                : {}
            }
            transition={{ duration: 0.5, repeat: mood === 'celebrating' ? Infinity : 0 }}
          />
          {/* Mouth line down */}
          <path
            d="M100 103 L100 108"
            fill="none"
            stroke="#8B7355"
            strokeWidth="2"
            strokeLinecap="round"
          />

          {/* Whiskers */}
          <g stroke="#8B7355" strokeWidth="1.5" strokeLinecap="round">
            {/* Left whiskers */}
            <motion.line
              x1="60" y1="95" x2="35" y2="90"
              animate={{ x2: [35, 30, 35] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <motion.line
              x1="60" y1="100" x2="35" y2="100"
              animate={{ x2: [35, 28, 35] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.1 }}
            />
            <motion.line
              x1="60" y1="105" x2="35" y2="110"
              animate={{ x2: [35, 30, 35] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.2 }}
            />
            {/* Right whiskers */}
            <motion.line
              x1="140" y1="95" x2="165" y2="90"
              animate={{ x2: [165, 170, 165] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <motion.line
              x1="140" y1="100" x2="165" y2="100"
              animate={{ x2: [165, 172, 165] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.1 }}
            />
            <motion.line
              x1="140" y1="105" x2="165" y2="110"
              animate={{ x2: [165, 170, 165] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.2 }}
            />
          </g>

          {/* Front paws */}
          <g>
            <ellipse cx="65" cy="165" rx="15" ry="12" fill="#F5E6D3" stroke="#E8D5C4" strokeWidth="2" />
            <ellipse cx="135" cy="165" rx="15" ry="12" fill="#F5E6D3" stroke="#E8D5C4" strokeWidth="2" />
            {/* Paw pads */}
            <circle cx="60" cy="168" r="3" fill="#FFB6C1" />
            <circle cx="65" cy="170" r="3" fill="#FFB6C1" />
            <circle cx="70" cy="168" r="3" fill="#FFB6C1" />
            <circle cx="130" cy="168" r="3" fill="#FFB6C1" />
            <circle cx="135" cy="170" r="3" fill="#FFB6C1" />
            <circle cx="140" cy="168" r="3" fill="#FFB6C1" />
          </g>

          {/* Tail - Fluffy curved tail */}
          <motion.path
            d="M155 140 Q180 130 175 100 Q170 80 160 85"
            fill="none"
            stroke="#E8A87C"
            strokeWidth="12"
            strokeLinecap="round"
            animate={
              mood === 'happy' || mood === 'excited'
                ? { d: ['M155 140 Q180 130 175 100 Q170 80 160 85', 'M155 140 Q185 125 180 95 Q175 75 165 80'] }
                : {}
            }
            transition={{ duration: 1, repeat: Infinity, repeatType: 'reverse' }}
          />

          {/* Collar with bell (optional cute accessory) */}
          <path
            d="M60 115 Q100 125 140 115"
            fill="none"
            stroke="#F97316"
            strokeWidth="6"
            strokeLinecap="round"
          />
          <circle cx="100" cy="122" r="6" fill="#FFD700" stroke="#DAA520" strokeWidth="1" />
          <circle cx="100" cy="122" r="2" fill="#DAA520" />
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
