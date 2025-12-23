'use client';

import { motion } from 'framer-motion';
import { Flame, Trophy, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { StreakInfo } from '@/services/parentApi';

interface StreakCardProps {
  streak: StreakInfo;
  className?: string;
}

export function StreakCard({ streak, className }: StreakCardProps) {
  const isActive = streak.streak_status === 'active';
  const isNew = streak.streak_status === 'new';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        'rounded-2xl p-6 shadow-sm border',
        isActive
          ? 'bg-gradient-to-br from-orange-500 to-red-500 text-white border-orange-400'
          : 'bg-white border-gray-100',
        className
      )}
    >
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Flame className={cn('w-6 h-6', isActive ? 'text-white' : 'text-orange-500')} />
            <span className={cn('font-semibold', isActive ? 'text-white' : 'text-gray-900')}>
              Learning Streak
            </span>
          </div>

          <div className="flex items-baseline gap-2">
            <span className={cn(
              'text-4xl font-bold',
              isActive ? 'text-white' : 'text-gray-900'
            )}>
              {streak.current_streak}
            </span>
            <span className={cn(
              'text-lg',
              isActive ? 'text-white/80' : 'text-gray-500'
            )}>
              days
            </span>
          </div>

          <p className={cn(
            'text-sm mt-2',
            isActive ? 'text-white/90' : 'text-gray-600'
          )}>
            {streak.streak_message}
          </p>
        </div>

        <div className={cn(
          'text-right',
          isActive ? 'text-white/80' : 'text-gray-500'
        )}>
          <div className="flex items-center gap-1 justify-end">
            <Trophy className="w-4 h-4" />
            <span className="text-sm">Best</span>
          </div>
          <p className={cn(
            'text-2xl font-bold',
            isActive ? 'text-white' : 'text-gray-700'
          )}>
            {streak.longest_streak}
          </p>
          <span className="text-xs">days</span>
        </div>
      </div>

      {isActive && streak.current_streak >= 7 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-4 pt-4 border-t border-white/20"
        >
          <div className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-300" />
            <span className="text-sm font-medium">
              Amazing! You're on fire!
            </span>
          </div>
        </motion.div>
      )}

      {isNew && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-4 pt-4 border-t border-gray-100"
        >
          <p className="text-sm text-gray-500">
            Start learning today to begin your streak!
          </p>
        </motion.div>
      )}
    </motion.div>
  );
}

export default StreakCard;
