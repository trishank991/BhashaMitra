'use client';

import { motion } from 'framer-motion';
import { Clock, BookOpen, Star, MessageCircle, TrendingUp, ChevronRight } from 'lucide-react';
import type { WeeklyReport } from '@/types/parent';

interface WeeklyReportCardProps {
  report: WeeklyReport;
  childName: string;
  onViewDetails?: () => void;
}

export function WeeklyReportCard({ report, childName, onViewDetails }: WeeklyReportCardProps) {
  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  const weekRange = `${new Date(report.weekStart).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })} - ${new Date(report.weekEnd).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })}`;

  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-semibold text-gray-900">{childName}&apos;s Weekly Report</h3>
          <p className="text-sm text-gray-500">{weekRange}</p>
        </div>
        <button
          onClick={onViewDetails}
          className="text-primary-600 hover:text-primary-700 flex items-center gap-1 text-sm font-medium"
        >
          Details <ChevronRight size={16} />
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        <div className="text-center p-3 bg-gray-50 rounded-xl">
          <Clock className="w-5 h-5 text-blue-500 mx-auto mb-1" />
          <p className="text-lg font-bold text-gray-900">
            {formatDuration(report.totalTimeMinutes)}
          </p>
          <p className="text-xs text-gray-500">Time</p>
        </div>

        <div className="text-center p-3 bg-gray-50 rounded-xl">
          <BookOpen className="w-5 h-5 text-purple-500 mx-auto mb-1" />
          <p className="text-lg font-bold text-gray-900">{report.storiesCompleted}</p>
          <p className="text-xs text-gray-500">Stories</p>
        </div>

        <div className="text-center p-3 bg-gray-50 rounded-xl">
          <Star className="w-5 h-5 text-yellow-500 mx-auto mb-1" />
          <p className="text-lg font-bold text-gray-900">{report.pointsEarned}</p>
          <p className="text-xs text-gray-500">Points</p>
        </div>

        <div className="text-center p-3 bg-gray-50 rounded-xl">
          <MessageCircle className="w-5 h-5 text-primary-500 mx-auto mb-1" />
          <p className="text-lg font-bold text-gray-900">{report.newWordsLearned}</p>
          <p className="text-xs text-gray-500">Words</p>
        </div>
      </div>

      {/* Achievements */}
      {report.achievementsUnlocked.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-gray-500 mb-2">Achievements Unlocked</p>
          <div className="flex flex-wrap gap-2">
            {report.achievementsUnlocked.map((achievement) => (
              <motion.div
                key={achievement.id}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="flex items-center gap-2 bg-yellow-50 text-yellow-700 px-3 py-1.5 rounded-full text-sm"
              >
                <span>{achievement.icon}</span>
                <span className="font-medium">{achievement.name}</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Strengths & Improvements */}
      <div className="grid md:grid-cols-2 gap-4">
        {report.areasOfStrength.length > 0 && (
          <div>
            <p className="text-sm text-gray-500 mb-2 flex items-center gap-1">
              <TrendingUp size={14} className="text-green-500" />
              Strengths
            </p>
            <ul className="space-y-1">
              {report.areasOfStrength.slice(0, 3).map((area, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                  {area}
                </li>
              ))}
            </ul>
          </div>
        )}

        {report.areasForImprovement.length > 0 && (
          <div>
            <p className="text-sm text-gray-500 mb-2">Focus Areas</p>
            <ul className="space-y-1">
              {report.areasForImprovement.slice(0, 3).map((area, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-orange-400 rounded-full" />
                  {area}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default WeeklyReportCard;
