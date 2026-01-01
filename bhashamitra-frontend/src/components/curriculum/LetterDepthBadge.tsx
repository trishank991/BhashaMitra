'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { LetterDepth, LETTER_DEPTH_INFO } from '@/types/curriculum';

interface LetterDepthBadgeProps {
  depth: LetterDepth;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  showDescription?: boolean;
  className?: string;
}

const sizeClasses = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-3 py-1',
  lg: 'text-base px-4 py-1.5',
};

const iconSizeClasses = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
};

export function LetterDepthBadge({
  depth,
  size = 'md',
  showLabel = true,
  showDescription = false,
  className,
}: LetterDepthBadgeProps) {
  const info = LETTER_DEPTH_INFO[depth];

  const getDepthIcon = () => {
    if (depth === 'DEEP') return '📘';
    if (depth === 'EXPOSURE') return '👁️';
    return '📖';
  };

  const getDepthColor = () => {
    if (depth === 'DEEP') {
      return 'bg-green-100 text-green-800 border-green-300';
    }
    if (depth === 'EXPOSURE') {
      return 'bg-blue-100 text-blue-800 border-blue-300';
    }
    return 'bg-gray-100 text-gray-800 border-gray-300';
  };

  return (
    <div className={cn('inline-flex flex-col items-start', className)}>
      <span
        className={cn(
          'inline-flex items-center gap-1.5 rounded-full border font-medium',
          sizeClasses[size],
          getDepthColor()
        )}
      >
        <span className={iconSizeClasses[size]}>{getDepthIcon()}</span>
        {showLabel && <span>{info?.label || depth}</span>}
      </span>
      {showDescription && info?.description && (
        <p className="mt-1 text-xs text-gray-500 max-w-xs">{info.description}</p>
      )}
    </div>
  );
}

// Progress indicator for letter mastery
interface LetterMasteryIndicatorProps {
  depth: LetterDepth;
  progress: number; // 0-100
  className?: string;
}

export function LetterMasteryIndicator({
  depth,
  progress,
  className,
}: LetterMasteryIndicatorProps) {
  const getProgressColor = () => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-yellow-500';
    return 'bg-blue-500';
  };

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <LetterDepthBadge depth={depth} size="sm" showLabel={false} />
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={cn('h-full transition-all duration-500', getProgressColor())}
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className="text-xs font-medium text-gray-600">{progress}%</span>
    </div>
  );
}

// Compact depth indicator for lists
export function DepthIcon({
  depth,
  className,
}: {
  depth: LetterDepth;
  className?: string;
}) {
  const icon = depth === 'DEEP' ? '📘' : '👁️';
  const title = LETTER_DEPTH_INFO[depth]?.label || depth;

  return (
    <span className={cn('cursor-help', className)} title={title}>
      {icon}
    </span>
  );
}

export default LetterDepthBadge;
