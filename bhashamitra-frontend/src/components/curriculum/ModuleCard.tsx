'use client';

import React from 'react';
import Link from 'next/link';
import { CurriculumModuleWithProgress, MODULE_TYPE_INFO } from '@/types';
import { ProgressRing } from './ProgressRing';

interface ModuleCardProps {
  module: CurriculumModuleWithProgress;
  levelColor?: string;
  isLocked?: boolean;
}

export function ModuleCard({ module, levelColor = '#6366f1', isLocked = false }: ModuleCardProps) {
  const progressPercent = module.total_lessons > 0
    ? Math.round((module.completed_lessons / module.total_lessons) * 100)
    : 0;

  const isCompleted = module.progress?.is_complete || progressPercent === 100;
  const typeInfo = MODULE_TYPE_INFO[module.module_type] || {
    label: module.module_type,
    emoji: module.emoji,
    color: levelColor,
  };

  return (
    <Link
      href={isLocked ? '#' : `/languages/modules/${module.id}`}
      className={`
        block rounded-xl p-4 transition-all duration-300
        ${isLocked
          ? 'opacity-50 cursor-not-allowed bg-gray-50'
          : 'hover:shadow-md hover:-translate-y-0.5 bg-white border border-gray-200'
        }
      `}
      onClick={(e) => isLocked && e.preventDefault()}
    >
      <div className="flex items-center gap-3">
        {/* Module Icon with Progress */}
        <div className="relative flex-shrink-0">
          <ProgressRing
            progress={progressPercent}
            size={52}
            strokeWidth={4}
            color={typeInfo.color}
            showText={false}
          >
            <span className="text-xl">{module.emoji}</span>
          </ProgressRing>
          {isCompleted && (
            <div className="absolute -top-0.5 -right-0.5 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          )}
          {isLocked && (
            <div className="absolute -top-0.5 -right-0.5 w-5 h-5 bg-gray-400 rounded-full flex items-center justify-center">
              <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
          )}
        </div>

        {/* Module Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span
              className="text-[10px] font-medium px-1.5 py-0.5 rounded text-white"
              style={{ backgroundColor: typeInfo.color }}
            >
              {typeInfo.label}
            </span>
          </div>
          <h3 className="font-semibold text-gray-900 text-sm mt-0.5 truncate">
            {module.name_english}
          </h3>
          <p className="text-xs text-gray-500 truncate">
            {module.name_hindi}
          </p>
        </div>

        {/* Lessons Count */}
        <div className="text-right flex-shrink-0">
          <p className="text-xs text-gray-500">Lessons</p>
          <p className="font-bold text-sm text-gray-900">
            {module.completed_lessons}/{module.total_lessons}
          </p>
        </div>
      </div>

      {/* Progress bar */}
      <div className="mt-3 h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{
            width: `${progressPercent}%`,
            backgroundColor: typeInfo.color,
          }}
        />
      </div>

      {/* Duration */}
      <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
        <span>{module.estimated_minutes} min</span>
        {module.progress?.total_points ? (
          <span className="text-amber-600 font-medium">
            {module.progress.total_points} pts
          </span>
        ) : null}
      </div>
    </Link>
  );
}

export default ModuleCard;
