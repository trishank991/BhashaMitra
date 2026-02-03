'use client';

import React from 'react';
import Link from 'next/link';
import { LessonWithProgress } from '@/types';

interface LessonCardProps {
  lesson: LessonWithProgress;
  moduleColor?: string;
  index: number;
  isLocked?: boolean;
}

export function LessonCard({
  lesson,
  moduleColor = '#6366f1',
  index,
  isLocked = false,
}: LessonCardProps) {
  const isCompleted = lesson.progress?.is_complete;
  const hasStarted = lesson.progress && lesson.progress.attempts > 0;
  const bestScore = lesson.progress?.best_score || 0;

  // Calculate stars (0-3)
  const getStars = (score: number) => {
    if (score >= lesson.mastery_threshold) return 3;
    if (score >= lesson.mastery_threshold * 0.75) return 2;
    if (score >= lesson.mastery_threshold * 0.5) return 1;
    return 0;
  };

  const stars = hasStarted ? getStars(bestScore) : 0;

  return (
    <Link
      href={isLocked ? '#' : `/languages/lessons/${lesson.id}`}
      className={`
        flex items-center gap-3 p-3 rounded-xl transition-all duration-200
        ${isLocked
          ? 'opacity-50 cursor-not-allowed bg-gray-50'
          : isCompleted
            ? 'bg-green-50 hover:bg-green-100'
            : hasStarted
              ? 'bg-amber-50 hover:bg-amber-100'
              : 'bg-white border border-gray-200 hover:border-gray-300 hover:shadow-sm'
        }
      `}
      onClick={(e) => isLocked && e.preventDefault()}
    >
      {/* Lesson Number */}
      <div
        className={`
          w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold
          ${isCompleted
            ? 'bg-green-500 text-white'
            : hasStarted
              ? 'bg-amber-500 text-white'
              : 'text-white'
          }
        `}
        style={!isCompleted && !hasStarted ? { backgroundColor: moduleColor } : {}}
      >
        {isCompleted ? (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ) : isLocked ? (
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        ) : (
          index + 1
        )}
      </div>

      {/* Lesson Info */}
      <div className="flex-1 min-w-0">
        <h4 className="font-medium text-gray-900 text-sm truncate">
          {lesson.title_english}
        </h4>
        <p className="text-xs text-gray-500 truncate">
          {lesson.title_hindi}
        </p>
        <div className="flex items-center gap-2 mt-1">
          <span className="text-xs text-gray-400">
            {lesson.estimated_minutes} min
          </span>
          <span className="text-xs text-gray-400">
            {lesson.points_available} pts
          </span>
        </div>
      </div>

      {/* Stars / Score */}
      <div className="flex-shrink-0 text-right">
        {hasStarted ? (
          <>
            <div className="flex gap-0.5">
              {[1, 2, 3].map((star) => (
                <svg
                  key={star}
                  className={`w-4 h-4 ${star <= stars ? 'text-amber-400' : 'text-gray-200'}`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-0.5">
              Best: {bestScore}%
            </p>
          </>
        ) : (
          <span className="text-xs text-gray-400">Not started</span>
        )}
      </div>
    </Link>
  );
}

export default LessonCard;
