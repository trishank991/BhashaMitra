'use client';

import { HTMLAttributes, forwardRef } from 'react';
import { cn, getInitials } from '@/lib/utils';

interface AvatarProps extends HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  name?: string;
  emoji?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  ring?: boolean;
  ringColor?: string;
}

const sizeStyles = {
  xs: 'w-6 h-6 text-xs',
  sm: 'w-8 h-8 text-sm',
  md: 'w-10 h-10 text-base',
  lg: 'w-14 h-14 text-lg',
  xl: 'w-20 h-20 text-2xl',
};

export const Avatar = forwardRef<HTMLDivElement, AvatarProps>(
  (
    {
      className,
      src,
      alt,
      name,
      emoji,
      size = 'md',
      ring = false,
      ringColor = 'ring-primary-500',
      ...props
    },
    ref
  ) => {
    const initials = name ? getInitials(name) : '?';

    return (
      <div
        ref={ref}
        className={cn(
          'relative inline-flex items-center justify-center rounded-full overflow-hidden',
          'bg-gradient-to-br from-primary-400 to-accent-500',
          sizeStyles[size],
          ring && `ring-2 ring-offset-2 ${ringColor}`,
          className
        )}
        {...props}
      >
        {src ? (
          <img
            src={src}
            alt={alt || name || 'Avatar'}
            className="w-full h-full object-cover"
          />
        ) : emoji ? (
          <span className="flex items-center justify-center">{emoji}</span>
        ) : (
          <span className="font-semibold text-white">{initials}</span>
        )}
      </div>
    );
  }
);

Avatar.displayName = 'Avatar';

export function AvatarGroup({
  avatars,
  max = 4,
  size = 'md',
}: {
  avatars: Array<{ src?: string; name?: string; emoji?: string }>;
  max?: number;
  size?: 'xs' | 'sm' | 'md' | 'lg';
}) {
  const visibleAvatars = avatars.slice(0, max);
  const remainingCount = avatars.length - max;

  return (
    <div className="flex -space-x-2">
      {visibleAvatars.map((avatar, index) => (
        <Avatar
          key={index}
          {...avatar}
          size={size}
          ring
          ringColor="ring-white"
          className="relative"
          style={{ zIndex: visibleAvatars.length - index }}
        />
      ))}
      {remainingCount > 0 && (
        <div
          className={cn(
            'relative inline-flex items-center justify-center rounded-full',
            'bg-gray-200 text-gray-600 font-medium ring-2 ring-white',
            sizeStyles[size]
          )}
          style={{ zIndex: 0 }}
        >
          +{remainingCount}
        </div>
      )}
    </div>
  );
}

export default Avatar;
