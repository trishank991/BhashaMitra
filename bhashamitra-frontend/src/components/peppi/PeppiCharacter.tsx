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

      {/* Peppi character - ragdoll cat SVG */}
      <motion.div
        className={cn(sizeClass, 'relative')}
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        animate={animate && animation ? (animation as any) : false}
      >
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-lg">
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
          <ellipse fill="#4A90D9" cx="35" cy="50" rx="9" ry="11"/>
          <ellipse fill="#4A90D9" cx="65" cy="50" rx="9" ry="11"/>
          <ellipse fill="#1a1a1a" cx="35" cy="51" rx="4" ry="5"/>
          <ellipse fill="#1a1a1a" cx="65" cy="51" rx="4" ry="5"/>
          <circle fill="white" cx="38" cy="45" r="3"/>
          <circle fill="white" cx="68" cy="45" r="3"/>
          {/* Nose */}
          <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>
          {/* Whiskers */}
          <line stroke="#999" strokeWidth="1" x1="8" y1="52" x2="28" y2="56"/>
          <line stroke="#999" strokeWidth="1" x1="8" y1="60" x2="28" y2="60"/>
          <line stroke="#999" strokeWidth="1" x1="92" y1="52" x2="72" y2="56"/>
          <line stroke="#999" strokeWidth="1" x1="92" y1="60" x2="72" y2="60"/>
          {/* Collar */}
          <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>
          {/* Bell */}
          <circle fill="#FFD700" cx="50" cy="83" r="5"/>
          <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
        </svg>
      </motion.div>
    </div>
  );
}

export default PeppiCharacter;
