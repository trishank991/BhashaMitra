'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { soundService } from '@/lib/soundService';

interface LevelUpProps {
  /** Whether to show the animation */
  show: boolean;
  /** The new level number */
  level: number;
  /** Callback when animation completes */
  onComplete?: () => void;
  /** Whether to play sound */
  playSound?: boolean;
  /** Custom class name */
  className?: string;
}

/**
 * Level up celebration animation.
 *
 * Shows a dramatic level up animation with the new level number.
 * Perfect for when users advance to a new learning level.
 *
 * @example
 * ```tsx
 * <LevelUp
 *   show={justLeveledUp}
 *   level={5}
 *   onComplete={() => setJustLeveledUp(false)}
 * />
 * ```
 */
export function LevelUp({
  show,
  level,
  onComplete,
  playSound = true,
  className = '',
}: LevelUpProps) {
  useEffect(() => {
    if (show && playSound) {
      soundService.onLevelUp();
    }
  }, [show, playSound]);

  useEffect(() => {
    if (show && onComplete) {
      const timer = setTimeout(onComplete, 3000);
      return () => clearTimeout(timer);
    }
  }, [show, onComplete]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className={`fixed inset-0 flex items-center justify-center z-50 pointer-events-none ${className}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Dark overlay */}
          <motion.div
            className="absolute inset-0 bg-black/40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />

          {/* Main content */}
          <div className="relative flex flex-col items-center">
            {/* Rays of light */}
            {[...Array(12)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-1 bg-gradient-to-t from-yellow-400 to-transparent"
                style={{
                  height: 200,
                  transformOrigin: 'bottom center',
                  rotate: `${i * 30}deg`,
                }}
                initial={{ scaleY: 0, opacity: 0 }}
                animate={{
                  scaleY: [0, 1, 0.8],
                  opacity: [0, 0.6, 0.3],
                }}
                transition={{
                  delay: 0.3 + i * 0.02,
                  duration: 1.5,
                  ease: 'easeOut',
                }}
              />
            ))}

            {/* "LEVEL UP" text */}
            <motion.div
              className="relative z-10 mb-4"
              initial={{ y: 50, opacity: 0, scale: 0.5 }}
              animate={{ y: 0, opacity: 1, scale: 1 }}
              transition={{
                type: 'spring',
                stiffness: 200,
                damping: 15,
                delay: 0.2,
              }}
            >
              <motion.span
                className="text-4xl md:text-5xl font-black tracking-wider"
                style={{
                  background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6347 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  textShadow: '0 0 40px rgba(255, 215, 0, 0.5)',
                }}
                animate={{
                  scale: [1, 1.05, 1],
                }}
                transition={{
                  duration: 0.5,
                  repeat: 2,
                  ease: 'easeInOut',
                }}
              >
                LEVEL UP!
              </motion.span>
            </motion.div>

            {/* Level number */}
            <motion.div
              className="relative z-10"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{
                type: 'spring',
                stiffness: 200,
                damping: 12,
                delay: 0.5,
              }}
            >
              <div className="relative">
                {/* Glowing background */}
                <motion.div
                  className="absolute inset-0 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 blur-xl"
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 0.8, 0.5],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: 'easeInOut',
                  }}
                />

                {/* Level circle */}
                <div className="relative w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center shadow-2xl border-4 border-white/30">
                  <motion.span
                    className="text-5xl md:text-6xl font-black text-white"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{
                      type: 'spring',
                      stiffness: 300,
                      damping: 15,
                      delay: 0.8,
                    }}
                  >
                    {level}
                  </motion.span>
                </div>

                {/* Orbiting stars */}
                {[...Array(5)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute"
                    style={{
                      top: '50%',
                      left: '50%',
                    }}
                    animate={{
                      rotate: 360,
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: 'linear',
                      delay: i * 0.2,
                    }}
                  >
                    <motion.div
                      style={{
                        x: `${90 + i * 10}px`,
                        y: '-50%',
                      }}
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24">
                        <path
                          fill="#FFD700"
                          d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                        />
                      </svg>
                    </motion.div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Sparkle particles */}
            {[...Array(20)].map((_, i) => (
              <motion.div
                key={`sparkle-${i}`}
                className="absolute w-2 h-2 rounded-full"
                style={{
                  backgroundColor: ['#FFD700', '#FF6347', '#4ECDC4', '#AA96DA'][i % 4],
                }}
                initial={{
                  x: 0,
                  y: 0,
                  scale: 0,
                  opacity: 1,
                }}
                animate={{
                  x: (Math.random() - 0.5) * 300,
                  y: (Math.random() - 0.5) * 300,
                  scale: [0, 1, 0],
                  opacity: [1, 1, 0],
                }}
                transition={{
                  delay: 0.5 + Math.random() * 0.5,
                  duration: 1.5,
                  ease: 'easeOut',
                }}
              />
            ))}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default LevelUp;
