'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  value: number; // 0-100
  max?: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'accent' | 'success';
  animated?: boolean;
  className?: string;
}

const sizeStyles = {
  sm: 'h-2',
  md: 'h-3',
  lg: 'h-4',
};

const variantStyles = {
  primary: 'bg-primary-500',
  secondary: 'bg-secondary-500',
  accent: 'bg-accent-500',
  success: 'bg-success-500',
};

export function ProgressBar({
  value,
  max = 100,
  showLabel = false,
  size = 'md',
  variant = 'primary',
  animated = true,
  className,
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div className={cn('w-full', className)}>
      {showLabel && (
        <div className="flex justify-between mb-1">
          <span className="text-sm font-medium text-gray-700">
            Progress
          </span>
          <span className="text-sm font-medium text-gray-700">
            {Math.round(percentage)}%
          </span>
        </div>
      )}

      <div
        className={cn(
          'w-full bg-gray-200 rounded-full overflow-hidden',
          sizeStyles[size]
        )}
      >
        <motion.div
          className={cn(
            'h-full rounded-full',
            variantStyles[variant],
            animated && 'relative overflow-hidden'
          )}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          {animated && (
            <motion.div
              className="absolute inset-0 w-full h-full"
              style={{
                background:
                  'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
              }}
              animate={{ x: ['-100%', '100%'] }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: 'linear',
              }}
            />
          )}
        </motion.div>
      </div>
    </div>
  );
}

export function XPProgressBar({
  currentXP,
  xpForNextLevel,
  level,
  className,
}: {
  currentXP: number;
  xpForNextLevel: number;
  level: number;
  className?: string;
}) {
  return (
    <div className={cn('w-full', className)}>
      <div className="flex justify-between mb-1">
        <span className="text-sm font-bold text-primary-600">
          Level {level}
        </span>
        <span className="text-xs text-gray-500">
          {currentXP} / {xpForNextLevel} XP
        </span>
      </div>
      <ProgressBar
        value={currentXP}
        max={xpForNextLevel}
        size="md"
        variant="primary"
        animated
      />
    </div>
  );
}

export default ProgressBar;
