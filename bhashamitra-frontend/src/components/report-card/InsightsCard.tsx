'use client';

import { motion } from 'framer-motion';
import {
  Lightbulb,
  TrendingUp,
  Target,
  Sparkles,
  AlertCircle,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { InsightItem } from '@/services/parentApi';

interface InsightsCardProps {
  insights: InsightItem[];
  className?: string;
}

const insightStyles: Record<string, { icon: React.ElementType; bg: string; border: string; iconColor: string }> = {
  strength: {
    icon: TrendingUp,
    bg: 'bg-green-50',
    border: 'border-green-200',
    iconColor: 'text-green-600'
  },
  improvement: {
    icon: Target,
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    iconColor: 'text-blue-600'
  },
  milestone: {
    icon: Sparkles,
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
    iconColor: 'text-yellow-600'
  },
  suggestion: {
    icon: Lightbulb,
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    iconColor: 'text-purple-600'
  },
};

export function InsightsCard({ insights, className }: InsightsCardProps) {
  if (insights.length === 0) {
    return (
      <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-purple-500" />
          Learning Insights
        </h3>
        <div className="text-center py-6">
          <AlertCircle className="w-10 h-10 text-gray-300 mx-auto mb-2" />
          <p className="text-gray-500">More learning data needed</p>
          <p className="text-sm text-gray-400">Keep practicing to see personalized insights!</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Lightbulb className="w-5 h-5 text-purple-500" />
        Learning Insights
      </h3>

      <div className="space-y-3">
        {insights.map((insight, index) => {
          const style = insightStyles[insight.type] || insightStyles.suggestion;
          const Icon = style.icon;

          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={cn(
                'rounded-xl p-4 border',
                style.bg,
                style.border
              )}
            >
              <div className="flex items-start gap-3">
                <div className={cn('mt-0.5', style.iconColor)}>
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-medium text-gray-800">{insight.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{insight.message}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default InsightsCard;
