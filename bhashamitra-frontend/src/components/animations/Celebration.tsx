'use client';

import { useEffect, useState, useCallback, memo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { soundService } from '@/lib/soundService';

interface CelebrationProps {
  /** Whether to show the celebration */
  show: boolean;
  /** Callback when animation completes */
  onComplete?: () => void;
  /** Type of celebration */
  type?: 'confetti' | 'stars' | 'fireworks';
  /** Duration in milliseconds */
  duration?: number;
  /** Whether to play sound */
  playSound?: boolean;
}

interface Particle {
  id: number;
  x: number;
  y: number;
  rotation: number;
  scale: number;
  color: string;
  delay: number;
  type: 'circle' | 'square' | 'star';
}

const COLORS = [
  '#FF6B6B', // Red
  '#4ECDC4', // Teal
  '#FFE66D', // Yellow
  '#95E1D3', // Mint
  '#F38181', // Coral
  '#AA96DA', // Purple
  '#FCBAD3', // Pink
  '#A8D8EA', // Sky Blue
  '#FF9F43', // Orange
  '#6C5CE7', // Indigo
];

const generateParticles = (count: number, type: CelebrationProps['type']): Particle[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: -20 - Math.random() * 20,
    rotation: Math.random() * 360,
    scale: 0.5 + Math.random() * 0.5,
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
    delay: Math.random() * 0.5,
    type: type === 'stars'
      ? 'star'
      : (['circle', 'square', 'star'] as const)[Math.floor(Math.random() * 3)],
  }));
};

const ParticleComponent = memo(function ParticleComponent({
  particle,
  type
}: {
  particle: Particle;
  type: CelebrationProps['type'];
}) {
  const getShape = () => {
    switch (particle.type) {
      case 'star':
        return (
          <svg viewBox="0 0 24 24" className="w-full h-full">
            <path
              fill={particle.color}
              d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
            />
          </svg>
        );
      case 'square':
        return (
          <div
            className="w-full h-full rounded-sm"
            style={{ backgroundColor: particle.color }}
          />
        );
      default:
        return (
          <div
            className="w-full h-full rounded-full"
            style={{ backgroundColor: particle.color }}
          />
        );
    }
  };

  return (
    <motion.div
      className="absolute"
      style={{
        left: `${particle.x}%`,
        width: type === 'stars' ? 24 : 12,
        height: type === 'stars' ? 24 : 12,
      }}
      initial={{
        y: particle.y,
        rotate: 0,
        scale: 0,
        opacity: 0,
      }}
      animate={{
        y: ['0%', '120vh'],
        rotate: [0, particle.rotation * 2],
        scale: [0, particle.scale, particle.scale, 0],
        opacity: [0, 1, 1, 0],
      }}
      transition={{
        duration: 2.5,
        delay: particle.delay,
        ease: [0.25, 0.46, 0.45, 0.94],
        times: [0, 0.1, 0.8, 1],
      }}
    >
      {getShape()}
    </motion.div>
  );
});

/**
 * Celebration animation component for achievements, level ups, etc.
 *
 * Uses framer-motion for smooth, performant animations.
 * Automatically plays celebration sound when shown.
 *
 * @example
 * ```tsx
 * <Celebration
 *   show={showCelebration}
 *   onComplete={() => setShowCelebration(false)}
 *   type="confetti"
 * />
 * ```
 */
export function Celebration({
  show,
  onComplete,
  type = 'confetti',
  duration = 3000,
  playSound = true,
}: CelebrationProps) {
  const [particles, setParticles] = useState<Particle[]>([]);

  const handleAnimationComplete = useCallback(() => {
    // Call onComplete after animation duration
    const timer = setTimeout(() => {
      onComplete?.();
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onComplete]);

  useEffect(() => {
    if (show) {
      // Generate particles
      const particleCount = type === 'fireworks' ? 60 : 40;
      setParticles(generateParticles(particleCount, type));

      // Play sound
      if (playSound) {
        soundService.onCelebration();
      }

      // Cleanup
      const cleanup = handleAnimationComplete();
      return cleanup;
    } else {
      setParticles([]);
    }
  }, [show, type, playSound, handleAnimationComplete]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="fixed inset-0 pointer-events-none z-50 overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Particles */}
          {particles.map((particle) => (
            <ParticleComponent key={particle.id} particle={particle} type={type} />
          ))}

          {/* Center burst effect for fireworks */}
          {type === 'fireworks' && (
            <motion.div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
              initial={{ scale: 0, opacity: 1 }}
              animate={{ scale: [0, 2, 3], opacity: [1, 0.5, 0] }}
              transition={{ duration: 0.8 }}
            >
              <div className="w-32 h-32 bg-gradient-radial from-yellow-300 via-orange-400 to-transparent rounded-full" />
            </motion.div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default Celebration;
