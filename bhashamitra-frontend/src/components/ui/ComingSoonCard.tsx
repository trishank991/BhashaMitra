'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';
import { Lock, Sparkles, Bell } from 'lucide-react';

interface ComingSoonCardProps {
  title: string;
  titleHindi?: string;
  description: string;
  releaseHint?: string;
  peppiMessage?: string;
  type: 'level' | 'language' | 'feature';
  icon?: ReactNode;
  color?: string;
  showWaitlist?: boolean;
  onWaitlistClick?: () => void;
  className?: string;
}

export function ComingSoonCard({
  title,
  titleHindi,
  description,
  releaseHint,
  peppiMessage,
  type,
  icon,
  color = '#6366f1',
  showWaitlist = false,
  onWaitlistClick,
  className,
}: ComingSoonCardProps) {
  return (
    <Card
      className={cn(
        'relative overflow-hidden border-2 border-dashed border-gray-300 bg-gradient-to-br from-gray-50 to-gray-100',
        className
      )}
      variant="outlined"
      padding="lg"
    >
      {/* Coming Soon Badge */}
      <div className="absolute top-4 right-4 z-10">
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg">
          Coming Soon
        </div>
      </div>

      {/* Sparkle Decoration */}
      <motion.div
        className="absolute top-8 left-8"
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        <Sparkles className="w-6 h-6 text-yellow-400 opacity-50" />
      </motion.div>

      <CardContent className="pt-12">
        {/* Icon or Lock */}
        <div className="flex justify-center mb-4">
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center"
            style={{ backgroundColor: `${color}20` }}
          >
            {icon || <Lock className="w-10 h-10" style={{ color }} />}
          </div>
        </div>

        {/* Title */}
        <div className="text-center mb-4">
          <h3 className="text-2xl font-bold text-gray-800 mb-1">{title}</h3>
          {titleHindi && (
            <p className="text-xl font-semibold" style={{ color }}>
              {titleHindi}
            </p>
          )}
        </div>

        {/* Description */}
        <p className="text-gray-600 text-center mb-4">{description}</p>

        {/* Release Hint */}
        {releaseHint && (
          <div className="bg-white rounded-lg p-3 mb-4 border border-gray-200">
            <p className="text-sm font-semibold text-gray-700 text-center">
              {releaseHint}
            </p>
          </div>
        )}

        {/* Peppi Message */}
        {peppiMessage && (
          <motion.div
            className="bg-primary-50 border-2 border-primary-200 rounded-2xl p-4 mb-6"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-start gap-2">
              <span className="text-2xl">🐱</span>
              <p className="text-sm text-gray-700 italic">{peppiMessage}</p>
            </div>
          </motion.div>
        )}

        {/* Waitlist Button */}
        {showWaitlist && (
          <div className="text-center">
            <Button
              variant="outline"
              size="md"
              onClick={onWaitlistClick}
              leftIcon={<Bell className="w-4 h-4" />}
              className="border-2"
            >
              Notify Me
            </Button>
          </div>
        )}

        {/* Type Badge */}
        <div className="mt-6 text-center">
          <span className="inline-block px-3 py-1 bg-gray-200 text-gray-600 text-xs font-semibold rounded-full uppercase">
            {type === 'level' && 'New Level'}
            {type === 'language' && 'New Language'}
            {type === 'feature' && 'New Feature'}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

export default ComingSoonCard;
