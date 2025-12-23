'use client';

import { motion } from 'framer-motion';
import { Calendar, BookOpen, Gamepad2, ChevronRight } from 'lucide-react';
import { Festival, FestivalReligion } from '@/types';

interface FestivalCardProps {
  festival: Festival;
  onClick?: () => void;
  compact?: boolean;
}

const RELIGION_STYLES: Record<FestivalReligion, { gradient: string; icon: string }> = {
  HINDU: { gradient: 'from-orange-100 to-red-100 border-orange-300', icon: 'bg-orange-500' },
  MUSLIM: { gradient: 'from-green-100 to-emerald-100 border-green-300', icon: 'bg-green-600' },
  SIKH: { gradient: 'from-amber-100 to-orange-100 border-amber-300', icon: 'bg-amber-500' },
  CHRISTIAN: { gradient: 'from-blue-100 to-indigo-100 border-blue-300', icon: 'bg-blue-500' },
  JAIN: { gradient: 'from-purple-100 to-pink-100 border-purple-300', icon: 'bg-purple-500' },
  BUDDHIST: { gradient: 'from-yellow-100 to-amber-100 border-yellow-300', icon: 'bg-yellow-600' },
};

const MONTH_NAMES = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

export function FestivalCard({ festival, onClick, compact = false }: FestivalCardProps) {
  const style = RELIGION_STYLES[festival.religion] || RELIGION_STYLES.HINDU;

  if (compact) {
    return (
      <motion.div
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onClick}
        className={`bg-gradient-to-br ${style.gradient} border rounded-xl p-3 cursor-pointer`}
      >
        <div className="flex items-center gap-3">
          <div className={`${style.icon} w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm`}>
            {MONTH_NAMES[festival.typical_month - 1]}
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-semibold text-gray-800 truncate">
              {festival.localized_name || festival.name}
            </h4>
            {festival.name_native && (
              <p className="text-sm text-gray-600 truncate">{festival.name_native}</p>
            )}
          </div>
          <ChevronRight className="w-5 h-5 text-gray-400" />
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`bg-gradient-to-br ${style.gradient} border rounded-2xl p-5 cursor-pointer shadow-sm hover:shadow-md transition-shadow`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className={`${style.icon} px-3 py-1 rounded-full text-white text-xs font-medium`}>
          {festival.religion}
        </div>
        <div className="flex items-center gap-1 text-gray-500 text-sm">
          <Calendar className="w-4 h-4" />
          <span>{MONTH_NAMES[festival.typical_month - 1]}</span>
        </div>
      </div>

      {/* Title */}
      <h3 className="text-xl font-bold text-gray-800 mb-1">
        {festival.localized_name || festival.name}
      </h3>
      {festival.name_native && (
        <p className="text-lg text-gray-600 mb-2">{festival.name_native}</p>
      )}

      {/* Description */}
      <p className="text-sm text-gray-600 line-clamp-2 mb-4">
        {festival.description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4">
        {festival.story_count !== undefined && festival.story_count > 0 && (
          <div className="flex items-center gap-1.5 text-gray-500">
            <BookOpen className="w-4 h-4" />
            <span className="text-sm">{festival.story_count} Stories</span>
          </div>
        )}
        {festival.activity_count !== undefined && festival.activity_count > 0 && (
          <div className="flex items-center gap-1.5 text-gray-500">
            <Gamepad2 className="w-4 h-4" />
            <span className="text-sm">{festival.activity_count} Activities</span>
          </div>
        )}
      </div>

      {/* Explore button */}
      <motion.div
        whileHover={{ x: 4 }}
        className="flex items-center gap-1 mt-4 text-gray-700 font-medium"
      >
        <span>Explore</span>
        <ChevronRight className="w-5 h-5" />
      </motion.div>
    </motion.div>
  );
}

export default FestivalCard;
