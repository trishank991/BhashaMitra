'use client';

import { motion } from 'framer-motion';
import { Clock, CheckCircle, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ParentChildActivity } from '@/types/parent';

interface ActivitySuggestionProps {
  activity: ParentChildActivity;
  onStart?: () => void;
}

export function ActivitySuggestion({ activity, onStart }: ActivitySuggestionProps) {
  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-900">{activity.title}</h3>
            {activity.isFeatured && (
              <Star className="w-4 h-4 text-yellow-500 fill-yellow-400" />
            )}
          </div>
          <p className="text-sm text-gray-500 mt-1">{activity.description}</p>
        </div>
      </div>

      <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
        <span className="flex items-center gap-1">
          <Clock size={14} />
          {activity.durationMinutes} min
        </span>
        <span className="text-gray-300">|</span>
        <span>Ages {activity.minAge}-{activity.maxAge}</span>
      </div>

      {/* Materials Needed */}
      {activity.materialsNeeded.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Materials</p>
          <div className="flex flex-wrap gap-2">
            {activity.materialsNeeded.map((material, index) => (
              <span
                key={index}
                className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
              >
                {material}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Learning Outcomes */}
      <div className="mb-4">
        <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Learning Outcomes</p>
        <div className="space-y-1">
          {activity.learningOutcomes.slice(0, 3).map((outcome, index) => (
            <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
              <CheckCircle size={14} className="text-green-500" />
              {outcome}
            </div>
          ))}
        </div>
      </div>

      <motion.button
        onClick={onStart}
        className={cn(
          'w-full py-3 rounded-xl font-semibold transition-all',
          'bg-primary-500 hover:bg-primary-600 text-white'
        )}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        Start Activity
      </motion.button>
    </div>
  );
}

export default ActivitySuggestion;
