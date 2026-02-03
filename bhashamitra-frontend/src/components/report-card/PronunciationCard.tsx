'use client';

import { motion } from 'framer-motion';
import { Mic, Star, Trophy } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { PronunciationStats } from '@/services/parentApi';

interface PronunciationCardProps {
  pronunciation: PronunciationStats;
  className?: string;
}

export function PronunciationCard({ pronunciation, className }: PronunciationCardProps) {
  const hasData = pronunciation.challenges_attempted > 0;
  const masteryPercent = pronunciation.total_challenges > 0
    ? Math.round((pronunciation.challenges_mastered / pronunciation.total_challenges) * 100)
    : 0;

  return (
    <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Mic className="w-5 h-5 text-primary-500" />
        Pronunciation Practice
      </h3>

      {!hasData ? (
        <div className="text-center py-6">
          <Mic className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">No pronunciation practice yet!</p>
          <p className="text-sm text-gray-400">Try the Peppi Mimic feature to practice speaking</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-primary-50 rounded-xl p-4 text-center"
            >
              <div className="text-3xl font-bold text-primary-600">
                {Math.round(pronunciation.average_score)}%
              </div>
              <div className="text-sm text-primary-700">Average Score</div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="bg-yellow-50 rounded-xl p-4 text-center"
            >
              <div className="flex items-center justify-center gap-1">
                {[...Array(3)].map((_, i) => (
                  <Star
                    key={i}
                    className={cn(
                      'w-6 h-6',
                      i < Math.round(pronunciation.total_stars / Math.max(pronunciation.challenges_attempted, 1))
                        ? 'text-yellow-400 fill-yellow-400'
                        : 'text-gray-300'
                    )}
                  />
                ))}
              </div>
              <div className="text-sm text-yellow-700 mt-1">
                {pronunciation.total_stars} Total Stars
              </div>
            </motion.div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Challenges Attempted</span>
              <span className="font-medium">
                {pronunciation.challenges_attempted} / {pronunciation.total_challenges}
              </span>
            </div>

            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Mastered</span>
              <span className="font-medium text-green-600">
                {pronunciation.challenges_mastered} ({masteryPercent}%)
              </span>
            </div>

            {pronunciation.best_category && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Best Category</span>
                <span className="font-medium flex items-center gap-1">
                  <Trophy className="w-4 h-4 text-yellow-500" />
                  {pronunciation.best_category}
                </span>
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Overall Mastery</span>
              <span className="text-sm font-medium">{masteryPercent}%</span>
            </div>
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary-400 to-primary-600 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${masteryPercent}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default PronunciationCard;
