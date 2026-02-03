'use client';

import { motion } from 'framer-motion';
import { Target, Clock, BookOpen, Star, TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { LearningGoal, GoalType } from '@/types/parent';

interface GoalCardProps {
  goal: LearningGoal;
  childName: string;
}

const goalConfig: Record<GoalType, { icon: typeof Target; label: string; unit: string; color: string }> = {
  DAILY_MINUTES: {
    icon: Clock,
    label: 'Daily Practice',
    unit: 'minutes',
    color: 'text-blue-600 bg-blue-100',
  },
  WEEKLY_STORIES: {
    icon: BookOpen,
    label: 'Weekly Stories',
    unit: 'stories',
    color: 'text-purple-600 bg-purple-100',
  },
  MONTHLY_POINTS: {
    icon: Star,
    label: 'Monthly Points',
    unit: 'points',
    color: 'text-yellow-600 bg-yellow-100',
  },
  LEVEL_TARGET: {
    icon: TrendingUp,
    label: 'Level Target',
    unit: 'level',
    color: 'text-green-600 bg-green-100',
  },
};

export function GoalCard({ goal, childName }: GoalCardProps) {
  const config = goalConfig[goal.goalType];
  const Icon = config.icon;

  const isCompleted = goal.progressPercentage >= 100;

  return (
    <div
      className={cn(
        'bg-white rounded-2xl p-5 shadow-sm border',
        isCompleted ? 'border-green-200 bg-green-50/50' : 'border-gray-100'
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={cn('w-10 h-10 rounded-full flex items-center justify-center', config.color)}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{config.label}</h3>
            <p className="text-sm text-gray-500">{childName}</p>
          </div>
        </div>
        {isCompleted && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full"
          >
            Done!
          </motion.div>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex items-baseline justify-between">
          <span className="text-3xl font-bold text-gray-900">{goal.currentValue}</span>
          <span className="text-gray-500">
            / {goal.targetValue} {config.unit}
          </span>
        </div>

        <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
          <motion.div
            className={cn(
              'h-full rounded-full',
              isCompleted
                ? 'bg-green-500'
                : 'bg-gradient-to-r from-primary-500 to-secondary-500'
            )}
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(100, goal.progressPercentage)}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>

        <p className="text-sm text-gray-500 text-right">
          {goal.progressPercentage.toFixed(0)}% complete
        </p>
      </div>

      {goal.endDate && (
        <p className="text-xs text-gray-400 mt-3">
          Ends {new Date(goal.endDate).toLocaleDateString()}
        </p>
      )}
    </div>
  );
}

export default GoalCard;
