'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Sparkles } from 'lucide-react';

export type PeppiExpression = 'happy' | 'excited' | 'thinking' | 'celebrating' | 'waving' | 'encouraging';
export type PeppiSize = 'small' | 'medium' | 'large';

interface PeppiCharacterProps {
  expression: PeppiExpression;
  size: PeppiSize;
  animate?: boolean;
  className?: string;
}

const sizeMap: Record<PeppiSize, string> = {
  small: 'w-16 h-16',
  medium: 'w-24 h-24',
  large: 'w-32 h-32',
};

const expressionAnimations: Record<PeppiExpression, object> = {
  happy: {
    y: [0, -8, 0],
    rotate: [0, -5, 5, 0],
    transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
  },
  excited: {
    y: [0, -12, 0],
    scale: [1, 1.1, 1],
    transition: { duration: 0.6, repeat: Infinity, ease: 'easeInOut' },
  },
  thinking: {
    rotate: [-5, 5, -5],
    transition: { duration: 3, repeat: Infinity, ease: 'easeInOut' },
  },
  celebrating: {
    rotate: [-15, 15, -15],
    y: [0, -20, 0],
    transition: { duration: 0.8, repeat: Infinity, ease: 'easeInOut' },
  },
  waving: {
    rotate: [0, 10, -10, 10, -10, 0],
    transition: { duration: 1.5, repeat: Infinity, ease: 'easeInOut' },
  },
  encouraging: {
    scale: [1, 1.08, 1],
    transition: { duration: 1.2, repeat: Infinity, ease: 'easeInOut' },
  },
};

export function PeppiCharacter({
  expression = 'happy',
  size = 'medium',
  animate = true,
  className,
}: PeppiCharacterProps) {
  const animation = expressionAnimations[expression];
  const sizeClass = sizeMap[size];

  return (
    <div className={cn('relative inline-block', className)}>
      {/* Celebration sparkles */}
      {expression === 'celebrating' && (
        <>
          <motion.div
            className="absolute -top-2 -left-2"
            animate={{
              scale: [0, 1, 0],
              rotate: [0, 180, 360],
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              repeatDelay: 0.5,
            }}
          >
            <Sparkles className="w-5 h-5 text-yellow-400 fill-yellow-400" />
          </motion.div>
          <motion.div
            className="absolute -top-2 -right-2"
            animate={{
              scale: [0, 1, 0],
              rotate: [0, -180, -360],
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              repeatDelay: 0.5,
              delay: 0.3,
            }}
          >
            <Sparkles className="w-5 h-5 text-yellow-400 fill-yellow-400" />
          </motion.div>
        </>
      )}

      {/* Peppi image */}
      <motion.div
        className={cn(sizeClass, 'relative')}
        animate={animate ? animation : {}}
      >
        <img
          src={`/images/peppi/peppi_${expression}.png`}
          alt={`Peppi ${expression}`}
          className="w-full h-full object-contain"
          onError={(e) => {
            // Fallback to happy expression if specific image not found
            const target = e.target as HTMLImageElement;
            if (!target.src.includes('peppi_happy.png')) {
              target.src = '/images/peppi/peppi_happy.png';
            }
          }}
        />
      </motion.div>
    </div>
  );
}

export default PeppiCharacter;
