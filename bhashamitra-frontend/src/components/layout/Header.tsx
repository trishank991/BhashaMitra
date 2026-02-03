'use client';

import { useAuthStore } from '@/stores';
import { Avatar } from '@/components/ui';
import { XPProgressBar } from '@/components/ui/ProgressBar';
import { useProgressStore } from '@/stores';
import { getGreeting } from '@/lib/utils';
import { LEVEL_TITLES, XP_PER_LEVEL } from '@/lib/constants';
import Link from 'next/link';

interface HeaderProps {
  showProgress?: boolean;
  title?: string;
  showBack?: boolean;
  onBack?: () => void;
}

export function Header({ showProgress = true, title, showBack = false, onBack }: HeaderProps) {
  const { activeChild } = useAuthStore();
  const { xp, level, streak } = useProgressStore();

  const greeting = getGreeting();
  const levelTitle = LEVEL_TITLES[level] || `Level ${level}`;

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-lg border-b border-gray-100">
      <div className="px-4 py-3">
        {/* Top row - greeting and avatar */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            {showBack && (
              <button
                onClick={onBack || (() => window.history.back())}
                className="p-2 -ml-2 rounded-full hover:bg-gray-100 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                </svg>
              </button>
            )}

            {title ? (
              <h1 className="text-xl font-bold text-gray-900">{title}</h1>
            ) : (
              <div>
                <p className="text-sm text-gray-500">{greeting}</p>
                <h1 className="text-lg font-bold text-gray-900">
                  {activeChild?.name || 'Explorer'}!
                </h1>
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            {/* Streak indicator */}
            {streak > 0 && (
              <div className="flex items-center gap-1 bg-primary-50 px-2 py-1 rounded-full">
                <span className="text-lg">🔥</span>
                <span className="text-sm font-bold text-primary-600">{streak}</span>
              </div>
            )}

            {/* Profile link */}
            <Link href="/profile">
              <Avatar
                emoji={activeChild?.avatar || '🐯'}
                size="md"
                ring
                ringColor="ring-primary-400"
              />
            </Link>
          </div>
        </div>

        {/* Progress bar */}
        {showProgress && (
          <div className="mt-2">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-accent-600">{levelTitle}</span>
            </div>
            <XPProgressBar
              currentXP={xp}
              xpForNextLevel={XP_PER_LEVEL * level}
              level={level}
            />
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
