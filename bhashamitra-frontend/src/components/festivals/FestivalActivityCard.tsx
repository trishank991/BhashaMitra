'use client';

import { motion } from 'framer-motion';
import {
  BookOpen,
  Scissors,
  ChefHat,
  Music,
  Gamepad2,
  GraduationCap,
  HelpCircle,
  Video,
  Clock,
  Star,
  Award,
} from 'lucide-react';
import { FestivalActivity, FestivalActivityType } from '@/types';

interface FestivalActivityCardProps {
  activity: FestivalActivity;
  onClick?: () => void;
  childAge?: number;
}

const ACTIVITY_ICONS: Record<FestivalActivityType, React.ComponentType<{ className?: string }>> = {
  STORY: BookOpen,
  CRAFT: Scissors,
  COOKING: ChefHat,
  SONG: Music,
  GAME: Gamepad2,
  VOCABULARY: GraduationCap,
  QUIZ: HelpCircle,
  VIDEO: Video,
};

const ACTIVITY_COLORS: Record<FestivalActivityType, { bg: string; text: string; icon: string }> = {
  STORY: { bg: 'bg-blue-50', text: 'text-blue-700', icon: 'bg-blue-500' },
  CRAFT: { bg: 'bg-pink-50', text: 'text-pink-700', icon: 'bg-pink-500' },
  COOKING: { bg: 'bg-orange-50', text: 'text-orange-700', icon: 'bg-orange-500' },
  SONG: { bg: 'bg-purple-50', text: 'text-purple-700', icon: 'bg-purple-500' },
  GAME: { bg: 'bg-green-50', text: 'text-green-700', icon: 'bg-green-500' },
  VOCABULARY: { bg: 'bg-indigo-50', text: 'text-indigo-700', icon: 'bg-indigo-500' },
  QUIZ: { bg: 'bg-yellow-50', text: 'text-yellow-700', icon: 'bg-yellow-500' },
  VIDEO: { bg: 'bg-red-50', text: 'text-red-700', icon: 'bg-red-500' },
};

const DIFFICULTY_LABELS = ['Easy', 'Medium', 'Hard'];

export function FestivalActivityCard({ activity, onClick, childAge }: FestivalActivityCardProps) {
  const Icon = ACTIVITY_ICONS[activity.activity_type] || HelpCircle;
  const colors = ACTIVITY_COLORS[activity.activity_type] || ACTIVITY_COLORS.STORY;

  const isAgeAppropriate = childAge
    ? childAge >= activity.min_age && childAge <= activity.max_age
    : true;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`${colors.bg} rounded-xl p-4 cursor-pointer border border-transparent hover:border-gray-200 transition-all ${
        !isAgeAppropriate ? 'opacity-60' : ''
      }`}
    >
      {/* Header */}
      <div className="flex items-start gap-3 mb-3">
        <div className={`${colors.icon} p-2 rounded-lg text-white`}>
          <Icon className="w-5 h-5" />
        </div>
        <div className="flex-1">
          <h4 className={`font-semibold ${colors.text}`}>{activity.title}</h4>
          <span className={`text-xs ${colors.text} opacity-70 uppercase`}>
            {activity.activity_type}
          </span>
        </div>
        <div className="flex items-center gap-1 text-amber-500">
          <Award className="w-4 h-4" />
          <span className="text-sm font-medium">{activity.points_reward}</span>
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 line-clamp-2 mb-3">
        {activity.description}
      </p>

      {/* Meta info */}
      <div className="flex items-center flex-wrap gap-3 text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <Clock className="w-3.5 h-3.5" />
          <span>{activity.duration_minutes} min</span>
        </div>

        <div className="flex items-center gap-1">
          <span>Ages {activity.min_age}-{activity.max_age}</span>
        </div>

        <div className="flex items-center gap-0.5">
          {[...Array(3)].map((_, i) => (
            <Star
              key={i}
              className={`w-3 h-3 ${
                i < activity.difficulty_level
                  ? 'text-amber-400 fill-amber-400'
                  : 'text-gray-300'
              }`}
            />
          ))}
          <span className="ml-1">{DIFFICULTY_LABELS[activity.difficulty_level - 1]}</span>
        </div>
      </div>

      {/* Age warning */}
      {!isAgeAppropriate && childAge && (
        <div className="mt-2 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded">
          Recommended for ages {activity.min_age}-{activity.max_age}
        </div>
      )}
    </motion.div>
  );
}

export default FestivalActivityCard;
