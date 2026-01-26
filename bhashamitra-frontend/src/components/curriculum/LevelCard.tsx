'use client';

import React from 'react';
import Link from 'next/link';
import { CurriculumLevelWithProgress } from '@/types';
import { ProgressRing } from './ProgressRing';

interface LevelCardProps {
  level: CurriculumLevelWithProgress;
  isLocked?: boolean;
  isCurrent?: boolean;
}

export function LevelCard({ level, isLocked = false, isCurrent = false }: LevelCardProps) {
  const progressPercent = level.total_modules > 0
    ? Math.round((level.completed_modules / level.total_modules) * 100)
    : 0;

  const isCompleted = level.progress?.is_complete || progressPercent === 100;

  // Check if level has no content (Coming Soon)
  const isComingSoon = level.total_modules === 0;
  const isDisabled = isLocked || isComingSoon;

  return (
    <Link
      href={isDisabled ? '#' : `/languages/levels/${level.id}`}
      className={`
        block rounded-2xl p-4 transition-all duration-300
        ${isDisabled
          ? 'opacity-60 cursor-not-allowed bg-gray-50'
          : 'hover:shadow-lg hover:-translate-y-1 bg-white shadow-md'
        }
        ${isCurrent && !isComingSoon ? 'ring-2 ring-offset-2' : ''}
      `}
      style={{
        borderLeft: `4px solid ${isComingSoon ? '#9CA3AF' : level.theme_color}`,
        ...(isCurrent && !isComingSoon ? { ringColor: level.theme_color } : {}),
      }}
      onClick={(e) => isDisabled && e.preventDefault()}
    >
      <div className="flex items-start gap-4">
        {/* Emoji and Progress */}
        <div className="relative">
          <ProgressRing
            progress={progressPercent}
            size={64}
            strokeWidth={5}
            color={level.theme_color}
            showText={false}
          >
            <span className="text-2xl">{level.emoji}</span>
          </ProgressRing>
          {isCompleted && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          )}
          {isLocked && !isComingSoon && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-gray-400 rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
          )}
          {isComingSoon && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-purple-400 rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          )}
        </div>

        {/* Level Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span
              className="text-xs font-bold px-2 py-0.5 rounded-full text-white"
              style={{ backgroundColor: level.theme_color }}
            >
              {level.code}
            </span>
            {isCurrent && !isComingSoon && (
              <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-amber-100 text-amber-700">
                Current
              </span>
            )}
            {isComingSoon && (
              <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-purple-100 text-purple-700">
                Coming Soon
              </span>
            )}
          </div>
          <h3 className="font-bold text-gray-900 mt-1 truncate">
            {level.name_english}
          </h3>
          <p className="text-sm text-gray-600 truncate">
            {level.name_hindi} ({level.name_romanized})
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Ages {level.min_age}-{level.max_age}
          </p>
        </div>

        {/* Stats */}
        <div className="text-right">
          {isComingSoon ? (
            <p className="text-xs text-purple-500 font-medium">
              Content being<br />prepared
            </p>
          ) : (
            <>
              <p className="text-xs text-gray-500">Modules</p>
              <p className="font-bold text-gray-900">
                {level.completed_modules}/{level.total_modules}
              </p>
              {level.progress?.total_points ? (
                <>
                  <p className="text-xs text-gray-500 mt-1">Points</p>
                  <p className="font-bold text-amber-600">
                    {level.progress.total_points}
                  </p>
                </>
              ) : null}
            </>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div className="mt-3 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{
            width: `${progressPercent}%`,
            backgroundColor: level.theme_color,
          }}
        />
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 mt-3 line-clamp-2">
        {isComingSoon
          ? `${level.description} This level's content is being prepared and will be available soon!`
          : level.description}
      </p>
    </Link>
  );
}

export default LevelCard;
