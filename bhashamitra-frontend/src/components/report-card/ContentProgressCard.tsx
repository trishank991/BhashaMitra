'use client';

import { motion } from 'framer-motion';
import { BookOpen, Gamepad2, PenLine, FileText, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ContentCompletionItem } from '@/services/parentApi';

interface ContentProgressCardProps {
  content: ContentCompletionItem[];
  className?: string;
}

const contentIcons: Record<string, { icon: React.ElementType; color: string }> = {
  lessons: { icon: BookOpen, color: 'text-purple-500' },
  stories: { icon: FileText, color: 'text-pink-500' },
  games: { icon: Gamepad2, color: 'text-orange-500' },
  exercises: { icon: PenLine, color: 'text-blue-500' },
};

export function ContentProgressCard({ content, className }: ContentProgressCardProps) {
  return (
    <div className={cn('bg-white rounded-2xl p-6 shadow-sm border border-gray-100', className)}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <CheckCircle2 className="w-5 h-5 text-green-500" />
        Content Completion
      </h3>

      <div className="space-y-4">
        {content.map((item, index) => {
          const config = contentIcons[item.content_type.toLowerCase()] || {
            icon: BookOpen,
            color: 'text-gray-500'
          };
          const Icon = config.icon;

          return (
            <motion.div
              key={item.content_type}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <Icon className={cn('w-5 h-5', config.color)} />
                  <span className="font-medium text-gray-700 capitalize">
                    {item.content_type}
                  </span>
                </div>
                <span className="text-sm text-gray-500">
                  {item.completed} / {item.total}
                </span>
              </div>

              <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${item.percentage}%` }}
                  transition={{ duration: 0.8, delay: index * 0.1, ease: 'easeOut' }}
                />
              </div>

              <p className="text-xs text-gray-500 mt-1 text-right">
                {item.percentage}% complete
              </p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default ContentProgressCard;
