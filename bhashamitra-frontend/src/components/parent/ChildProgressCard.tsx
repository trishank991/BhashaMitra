'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Flame, Star, Clock, FileText } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ChildSummary } from '@/types/parent';

interface ChildProgressCardProps {
  child: ChildSummary;
  onClick?: () => void;
  isSelected?: boolean;
}

export function ChildProgressCard({ child, onClick, isSelected }: ChildProgressCardProps) {
  const router = useRouter();

  const handleReportCard = (e: React.MouseEvent) => {
    e.stopPropagation();
    router.push(`/parent/report-card/${child.id}`);
  };

  const getLastActiveText = () => {
    const now = new Date();
    const lastActive = new Date(child.lastActiveAt);
    const diffMs = now.getTime() - lastActive.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays === 1) return 'Yesterday';
    return `${diffDays} days ago`;
  };

  return (
    <motion.div
      onClick={onClick}
      className={cn(
        'bg-white rounded-2xl p-5 cursor-pointer transition-all border-2',
        'hover:shadow-md',
        isSelected ? 'border-primary-500 shadow-md' : 'border-transparent shadow-sm'
      )}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="flex items-start gap-4">
        {/* Avatar */}
        <div className="relative">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
            {child.name[0]}
          </div>
          {child.currentStreak > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="absolute -bottom-1 -right-1 bg-orange-500 text-white text-xs font-bold px-2 py-0.5 rounded-full flex items-center gap-0.5"
            >
              <Flame size={12} />
              {child.currentStreak}
            </motion.div>
          )}
        </div>

        {/* Info */}
        <div className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-semibold text-gray-900 text-lg">{child.name}</h3>
              <div className="flex items-center gap-3 text-sm text-gray-500 mt-1">
                <span className="flex items-center gap-1">
                  <Star size={14} className="text-yellow-500" />
                  Level {child.level}
                </span>
                <span className="flex items-center gap-1">
                  <Clock size={14} />
                  {getLastActiveText()}
                </span>
              </div>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-primary-600">{child.points}</p>
              <p className="text-xs text-gray-400">points</p>
            </div>
          </div>

          {/* Weekly Progress Bar */}
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="text-gray-500">Weekly Progress</span>
              <span className="font-medium text-gray-700">{child.weeklyProgress}%</span>
            </div>
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${child.weeklyProgress}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
          </div>

          {/* Report Card Button */}
          <button
            onClick={handleReportCard}
            className="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 bg-primary-50 text-primary-600 rounded-lg hover:bg-primary-100 transition-colors text-sm font-medium"
          >
            <FileText size={16} />
            View Report Card
          </button>
        </div>
      </div>
    </motion.div>
  );
}

export default ChildProgressCard;
