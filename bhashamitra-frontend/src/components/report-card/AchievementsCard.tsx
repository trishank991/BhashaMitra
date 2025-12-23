'use client';

import { motion } from 'framer-motion';
import { Trophy, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { AchievementItem } from '@/services/parentApi';

interface AchievementsCardProps {
  achievements: AchievementItem[];
  className?: string;
}

export function AchievementsCard({ achievements, className }: AchievementsCardProps) {
  if (achievements.length === 0) {
    return (
      <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Trophy className="w-5 h-5 text-yellow-500" />
          Achievements
        </h3>
        <div className="text-center py-8">
          <Star className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">No achievements yet!</p>
          <p className="text-sm text-gray-400">Keep learning to earn your first badge</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Trophy className="w-5 h-5 text-yellow-500" />
        Achievements ({achievements.length})
      </h3>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {achievements.slice(0, 6).map((achievement, index) => (
          <motion.div
            key={achievement.id}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-4 text-center border border-yellow-100"
          >
            <div className="text-3xl mb-2">{achievement.icon}</div>
            <h4 className="font-medium text-gray-800 text-sm">{achievement.name}</h4>
            <p className="text-xs text-gray-500 mt-1 line-clamp-2">{achievement.description}</p>
            <div className="mt-2 flex items-center justify-center gap-1">
              <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />
              <span className="text-xs font-medium text-yellow-600">+{achievement.xp_reward} XP</span>
            </div>
          </motion.div>
        ))}
      </div>

      {achievements.length > 6 && (
        <button className="w-full mt-4 text-sm text-primary-600 hover:text-primary-700 font-medium">
          View all {achievements.length} achievements
        </button>
      )}
    </div>
  );
}

export default AchievementsCard;
