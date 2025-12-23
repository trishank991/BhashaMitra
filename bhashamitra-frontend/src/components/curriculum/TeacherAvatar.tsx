'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { CurriculumTeacher, TeacherCharacterType, TEACHER_INFO } from '@/types/curriculum';

interface TeacherAvatarProps {
  teacher?: CurriculumTeacher;
  characterType?: TeacherCharacterType;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showName?: boolean;
  speaking?: boolean;
  className?: string;
}

const sizeClasses = {
  sm: 'w-10 h-10 text-2xl',
  md: 'w-16 h-16 text-4xl',
  lg: 'w-24 h-24 text-6xl',
  xl: 'w-32 h-32 text-7xl',
};

const nameSizeClasses = {
  sm: 'text-xs',
  md: 'text-sm',
  lg: 'text-base',
  xl: 'text-lg',
};

export function TeacherAvatar({
  teacher,
  characterType,
  size = 'md',
  showName = false,
  speaking = false,
  className,
}: TeacherAvatarProps) {
  // Determine character type from teacher or prop
  const charType = teacher?.character_type || characterType || 'CAT';
  const teacherInfo = TEACHER_INFO[charType];

  // Get emoji and colors based on character type
  const getTeacherEmoji = () => {
    if (charType === 'CAT') return '🐱';
    if (charType === 'OWL') return '🦉';
    return '🎓';
  };

  const getBackgroundGradient = () => {
    if (charType === 'CAT') {
      return 'bg-gradient-to-br from-orange-100 to-orange-200 border-orange-300';
    }
    if (charType === 'OWL') {
      return 'bg-gradient-to-br from-purple-100 to-purple-200 border-purple-300';
    }
    return 'bg-gradient-to-br from-gray-100 to-gray-200 border-gray-300';
  };

  const getSpeakingAnimation = () => {
    if (!speaking) return '';
    return 'animate-bounce';
  };

  const displayName = teacher?.name || teacherInfo?.name || 'Teacher';
  const displayNameHindi = teacher?.name_hindi || '';

  return (
    <div className={cn('flex flex-col items-center', className)}>
      {/* Avatar Circle */}
      <div
        className={cn(
          'rounded-full border-2 flex items-center justify-center shadow-md transition-all duration-300',
          sizeClasses[size],
          getBackgroundGradient(),
          speaking && 'ring-4 ring-yellow-400 ring-opacity-50',
        )}
      >
        {/* Use avatar URL if available, otherwise emoji */}
        {teacher?.avatar_url ? (
          <img
            src={teacher.avatar_url}
            alt={displayName}
            className="w-full h-full rounded-full object-cover"
          />
        ) : (
          <span className={cn('select-none', getSpeakingAnimation())}>
            {getTeacherEmoji()}
          </span>
        )}
      </div>

      {/* Name Label */}
      {showName && (
        <div className={cn('mt-2 text-center', nameSizeClasses[size])}>
          <p className="font-semibold text-gray-800">{displayName}</p>
          {displayNameHindi && (
            <p className="text-gray-500">{displayNameHindi}</p>
          )}
          <p className="text-xs text-gray-400">({teacherInfo?.levels})</p>
        </div>
      )}
    </div>
  );
}

// Simple variant for inline use
export function TeacherIcon({
  characterType = 'CAT',
  className,
}: {
  characterType?: TeacherCharacterType;
  className?: string;
}) {
  const emoji = characterType === 'CAT' ? '🐱' : '🦉';
  return <span className={cn('text-2xl', className)}>{emoji}</span>;
}

export default TeacherAvatar;
