'use client';

import { motion } from 'framer-motion';
import {
  Clock,
  Calendar,
  Star,
  BookOpen,
  Gamepad2,
  PenLine,
  Trophy,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ReportCardOverallStats } from '@/services/parentApi';

interface StatsOverviewProps {
  stats: ReportCardOverallStats;
  className?: string;
}

const statConfig = [
  {
    key: 'total_time_minutes',
    label: 'Learning Time',
    icon: Clock,
    color: 'bg-blue-100 text-blue-600',
    format: (v: number) => `${Math.floor(v / 60)}h ${v % 60}m`,
  },
  {
    key: 'days_active',
    label: 'Days Active',
    icon: Calendar,
    color: 'bg-green-100 text-green-600',
    format: (v: number) => `${v} days`,
  },
  {
    key: 'total_points',
    label: 'Points Earned',
    icon: Star,
    color: 'bg-yellow-100 text-yellow-600',
    format: (v: number) => v.toLocaleString(),
  },
  {
    key: 'lessons_completed',
    label: 'Lessons Done',
    icon: BookOpen,
    color: 'bg-purple-100 text-purple-600',
    format: (v: number) => v.toString(),
  },
  {
    key: 'stories_read',
    label: 'Stories Read',
    icon: BookOpen,
    color: 'bg-pink-100 text-pink-600',
    format: (v: number) => v.toString(),
  },
  {
    key: 'games_played',
    label: 'Games Played',
    icon: Gamepad2,
    color: 'bg-orange-100 text-orange-600',
    format: (v: number) => v.toString(),
  },
  {
    key: 'words_learned',
    label: 'Words Learned',
    icon: PenLine,
    color: 'bg-teal-100 text-teal-600',
    format: (v: number) => v.toString(),
  },
  {
    key: 'current_level',
    label: 'Current Level',
    icon: Trophy,
    color: 'bg-indigo-100 text-indigo-600',
    format: (v: number) => `Level ${v}`,
  },
];

export function StatsOverview({ stats, className }: StatsOverviewProps) {
  return (
    <div className={cn('grid grid-cols-2 md:grid-cols-4 gap-4', className)}>
      {statConfig.map((stat, index) => {
        const Icon = stat.icon;
        const value = stats[stat.key as keyof ReportCardOverallStats] as number;

        return (
          <motion.div
            key={stat.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100"
          >
            <div className="flex items-center gap-3">
              <div className={cn(
                'w-10 h-10 rounded-full flex items-center justify-center',
                stat.color.split(' ')[0]
              )}>
                <Icon className={cn('w-5 h-5', stat.color.split(' ')[1])} />
              </div>
              <div>
                <p className="text-sm text-gray-500">{stat.label}</p>
                <p className="text-xl font-bold text-gray-900">
                  {stat.format(value)}
                </p>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

export default StatsOverview;
