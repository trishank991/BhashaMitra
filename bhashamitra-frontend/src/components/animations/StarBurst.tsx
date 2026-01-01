'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { soundService } from '@/lib/soundService';

interface StarBurstProps {
  /** Whether to show the animation */
  show: boolean;
  /** Callback when animation completes */
  onComplete?: () => void;
  /** Number of stars to show */
  starCount?: number;
  /** Size of the burst */
  size?: 'sm' | 'md' | 'lg';
  /** Custom message to display */
  message?: string;
  /** Whether to play sound */
  playSound?: boolean;
  /** Custom class name */
  className?: string;
}

const STAR_COLORS = ['#FFD700', '#FFA500', '#FF6347', '#FFE066', '#FFEC8B'];

/**
 * Animated star burst for streaks, achievements, and special moments.
 *
 * Perfect for celebrating streak milestones, earned badges, or level ups.
 *
 * @example
 * ```tsx
 * <StarBurst
 *   show={streakMilestone}
 *   message="5 in a row!"
 *   onComplete={() => setShowStreak(false)}
 * />
 * ```
 */
export function StarBurst({
  show,
  onComplete,
  starCount = 8,
  size = 'md',
  message,
  playSound = true,
  className = '',
}: StarBurstProps) {
  const sizeMultiplier = size === 'sm' ? 0.6 : size === 'lg' ? 1.4 : 1;
  const baseRadius = 80 * sizeMultiplier;

  useEffect(() => {
    if (show && playSound) {
      soundService.onStreak();
    }
  }, [show, playSound]);

  useEffect(() => {
    if (show && onComplete) {
      const timer = setTimeout(onComplete, 2000);
      return () => clearTimeout(timer);
    }
  }, [show, onComplete]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className={`flex flex-col items-center justify-center ${className}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Stars orbiting outward */}
          <div className="relative" style={{ width: baseRadius * 3, height: baseRadius * 3 }}>
            {/* Center glow */}
            <motion.div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
              style={{
                width: 40 * sizeMultiplier,
                height: 40 * sizeMultiplier,
                background: 'radial-gradient(circle, #FFD700 0%, transparent 70%)',
              }}
              initial={{ scale: 0, opacity: 0 }}
              animate={{
                scale: [0, 2, 1.5],
                opacity: [0, 1, 0.5],
              }}
              transition={{ duration: 0.6 }}
            />

            {/* Stars bursting out */}
            {[...Array(starCount)].map((_, i) => {
              const angle = (i * 360) / starCount;
              const delay = i * 0.05;
              const color = STAR_COLORS[i % STAR_COLORS.length];

              return (
                <motion.div
                  key={i}
                  className="absolute top-1/2 left-1/2"
                  initial={{
                    x: '-50%',
                    y: '-50%',
                    rotate: 0,
                    scale: 0,
                  }}
                  animate={{
                    x: `calc(-50% + ${Math.cos((angle * Math.PI) / 180) * baseRadius}px)`,
                    y: `calc(-50% + ${Math.sin((angle * Math.PI) / 180) * baseRadius}px)`,
                    rotate: 360,
                    scale: [0, 1.2, 1],
                  }}
                  transition={{
                    delay,
                    duration: 0.8,
                    ease: 'easeOut',
                  }}
                >
                  <motion.svg
                    width={24 * sizeMultiplier}
                    height={24 * sizeMultiplier}
                    viewBox="0 0 24 24"
                    animate={{
                      rotate: [0, 20, -20, 0],
                      scale: [1, 1.1, 1],
                    }}
                    transition={{
                      delay: delay + 0.5,
                      duration: 1,
                      repeat: 1,
                      ease: 'easeInOut',
                    }}
                  >
                    <path
                      fill={color}
                      d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                      filter="drop-shadow(0 0 4px rgba(255, 215, 0, 0.5))"
                    />
                  </motion.svg>
                </motion.div>
              );
            })}

            {/* Secondary smaller stars */}
            {[...Array(Math.floor(starCount / 2))].map((_, i) => {
              const angle = (i * 360) / (starCount / 2) + 22.5;
              const delay = 0.3 + i * 0.05;

              return (
                <motion.div
                  key={`small-${i}`}
                  className="absolute top-1/2 left-1/2"
                  initial={{
                    x: '-50%',
                    y: '-50%',
                    scale: 0,
                    opacity: 0,
                  }}
                  animate={{
                    x: `calc(-50% + ${Math.cos((angle * Math.PI) / 180) * baseRadius * 1.3}px)`,
                    y: `calc(-50% + ${Math.sin((angle * Math.PI) / 180) * baseRadius * 1.3}px)`,
                    scale: [0, 0.6, 0.4],
                    opacity: [0, 1, 0],
                  }}
                  transition={{
                    delay,
                    duration: 1,
                    ease: 'easeOut',
                  }}
                >
                  <div
                    className="rounded-full"
                    style={{
                      width: 8 * sizeMultiplier,
                      height: 8 * sizeMultiplier,
                      backgroundColor: '#FFE066',
                    }}
                  />
                </motion.div>
              );
            })}
          </div>

          {/* Message */}
          {message && (
            <motion.div
              className="mt-4 text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.4 }}
            >
              <span
                className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500"
                style={{ fontSize: 20 * sizeMultiplier }}
              >
                {message}
              </span>
            </motion.div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default StarBurst;
