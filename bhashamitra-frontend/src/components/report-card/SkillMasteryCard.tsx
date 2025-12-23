'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { SkillMasteryItem } from '@/services/parentApi';

interface SkillMasteryCardProps {
  skills: SkillMasteryItem[];
  className?: string;
}

const masteryColors: Record<string, { bg: string; bar: string; text: string }> = {
  novice: { bg: 'bg-gray-100', bar: 'bg-gray-400', text: 'text-gray-600' },
  beginner: { bg: 'bg-blue-50', bar: 'bg-blue-400', text: 'text-blue-600' },
  intermediate: { bg: 'bg-green-50', bar: 'bg-green-500', text: 'text-green-600' },
  advanced: { bg: 'bg-purple-50', bar: 'bg-purple-500', text: 'text-purple-600' },
  expert: { bg: 'bg-yellow-50', bar: 'bg-yellow-500', text: 'text-yellow-700' },
};

const masteryLabels: Record<string, string> = {
  novice: 'Novice',
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
  expert: 'Expert',
};

export function SkillMasteryCard({ skills, className }: SkillMasteryCardProps) {
  return (
    <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Skill Mastery</h3>

      <div className="space-y-4">
        {skills.map((skill, index) => {
          const colors = masteryColors[skill.mastery_level] || masteryColors.novice;

          return (
            <motion.div
              key={skill.skill}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{skill.icon}</span>
                  <span className="font-medium text-gray-700">{skill.display_name}</span>
                </div>
                <span className={cn('text-sm font-medium', colors.text)}>
                  {masteryLabels[skill.mastery_level]}
                </span>
              </div>

              <div className={cn('h-3 rounded-full overflow-hidden', colors.bg)}>
                <motion.div
                  className={cn('h-full rounded-full', colors.bar)}
                  initial={{ width: 0 }}
                  animate={{ width: `${skill.percentage}%` }}
                  transition={{ duration: 0.8, delay: index * 0.1, ease: 'easeOut' }}
                />
              </div>

              <p className="text-xs text-gray-500 mt-1 text-right">
                {skill.percentage}% mastery
              </p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default SkillMasteryCard;
