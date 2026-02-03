'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface SpeakerButtonProps {
  isPlaying: boolean;
  isLoading: boolean;
  onClick?: (e?: React.MouseEvent) => void;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

/**
 * Kid-friendly speaker button with animations
 * Shows loading spinner when generating audio
 * Animates when playing
 */
export function SpeakerButton({
  isPlaying,
  isLoading,
  onClick,
  size = 'md',
  className,
}: SpeakerButtonProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    // Prevent event from reaching parent interactive elements
    const target = e.target as HTMLElement;
    const button = target.closest('button');
    if (button) {
      button.blur();
    }
    onClick?.(e);
  };

  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      onClick={handleClick}
      disabled={isLoading}
      className={cn(
        'rounded-full flex items-center justify-center transition-colors',
        'bg-gradient-to-br from-purple-400 to-pink-500',
        'hover:from-purple-500 hover:to-pink-600',
        'text-white shadow-lg',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        sizeClasses[size],
        className
      )}
      aria-label={isPlaying ? 'Stop speaking' : 'Listen to pronunciation'}
    >
      {isLoading ? (
        // Loading spinner
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className={cn('border-2 border-white border-t-transparent rounded-full', {
            'w-4 h-4': size === 'sm',
            'w-5 h-5': size === 'md',
            'w-6 h-6': size === 'lg',
          })}
        />
      ) : isPlaying ? (
        // Sound waves animation when playing
        <div className="flex items-center gap-0.5">
          {[1, 2, 3].map((bar) => (
            <motion.div
              key={bar}
              animate={{
                height: ['40%', '100%', '40%'],
              }}
              transition={{
                duration: 0.5,
                repeat: Infinity,
                delay: bar * 0.15,
              }}
              className={cn('bg-white rounded-full', {
                'w-0.5': size === 'sm',
                'w-1': size === 'md' || size === 'lg',
              })}
              style={{ minHeight: '4px' }}
            />
          ))}
        </div>
      ) : (
        // Speaker icon
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className={iconSizes[size]}
        >
          <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.318.664-2.66 1.905A9.76 9.76 0 0 0 1.5 12c0 .898.121 1.768.35 2.595.341 1.24 1.518 1.905 2.659 1.905h1.93l4.5 4.5c.945.945 2.561.276 2.561-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z" />
          <path d="M15.932 7.757a.75.75 0 0 1 1.061 0 6 6 0 0 1 0 8.486.75.75 0 0 1-1.06-1.061 4.5 4.5 0 0 0 0-6.364.75.75 0 0 1 0-1.06Z" />
        </svg>
      )}
    </motion.button>
  );
}

export default SpeakerButton;
