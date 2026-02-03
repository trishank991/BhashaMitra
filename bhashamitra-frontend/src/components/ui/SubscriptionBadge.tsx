'use client';

import { SubscriptionTier } from '@/types';
import { cn } from '@/lib/utils';

interface SubscriptionBadgeProps {
  tier: SubscriptionTier;
  showDescription?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const tierConfig: Record<SubscriptionTier, {
  label: string;
  icon: string;
  bgColor: string;
  textColor: string;
  description: string;
}> = {
  FREE: {
    label: 'Free',
    icon: '🌱',
    bgColor: 'bg-gray-100',
    textColor: 'text-gray-700',
    description: '4 stories with voice',
  },
  STANDARD: {
    label: 'Standard',
    icon: '⭐',
    bgColor: 'bg-blue-100',
    textColor: 'text-blue-700',
    description: '8 stories, games & quizzes',
  },
  PREMIUM: {
    label: 'Premium',
    icon: '👑',
    bgColor: 'bg-gradient-to-r from-amber-100 to-yellow-100',
    textColor: 'text-amber-700',
    description: 'Unlimited stories, premium voices',
  },
};

const sizeStyles = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
  lg: 'px-4 py-1.5 text-base',
};

export function SubscriptionBadge({
  tier,
  showDescription = false,
  size = 'md',
  className,
}: SubscriptionBadgeProps) {
  const config = tierConfig[tier] || tierConfig.FREE;

  return (
    <div className={cn('inline-flex flex-col', className)}>
      <span
        className={cn(
          'inline-flex items-center font-medium rounded-full',
          config.bgColor,
          config.textColor,
          sizeStyles[size]
        )}
      >
        <span className="mr-1">{config.icon}</span>
        {config.label}
      </span>
      {showDescription && (
        <span className="text-xs text-gray-500 mt-1">{config.description}</span>
      )}
    </div>
  );
}

export default SubscriptionBadge;
