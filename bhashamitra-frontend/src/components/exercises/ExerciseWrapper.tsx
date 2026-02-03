'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import PeppiSpeech from '@/components/peppi/PeppiSpeech';

interface ExerciseWrapperProps {
  title: string;
  currentQuestion: number;
  totalQuestions: number;
  streak: number;
  onBack?: () => void;
  onNext?: () => void;
  showNext?: boolean;
  children: React.ReactNode;
  peppiTrigger?: 'welcome' | 'correct' | 'incorrect' | 'encouragement' | 'lessonComplete' | 'streak' | 'hint' | 'idle';
  className?: string;
}

export function ExerciseWrapper({
  title,
  currentQuestion,
  totalQuestions,
  streak,
  onBack,
  onNext,
  showNext = false,
  children,
  peppiTrigger = 'idle',
  className,
}: ExerciseWrapperProps) {
  const ageConfig = useAgeConfig();
  const [showPeppi, setShowPeppi] = useState(true);
  const [currentPeppiTrigger, setCurrentPeppiTrigger] = useState(peppiTrigger);

  // Update Peppi trigger when prop changes
  useEffect(() => {
    setCurrentPeppiTrigger(peppiTrigger);
    setShowPeppi(true);

    // Auto-hide Peppi after message (except for certain states)
    if (!['idle', 'welcome', 'lessonComplete'].includes(peppiTrigger)) {
      const timer = setTimeout(() => setShowPeppi(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [peppiTrigger]);

  // Show streak celebration
  useEffect(() => {
    if (streak > 0 && streak % 3 === 0) {
      setCurrentPeppiTrigger('streak');
      setShowPeppi(true);
    }
  }, [streak]);

  const progress = (currentQuestion / totalQuestions) * 100;

  return (
    <div className={cn('min-h-screen bg-gradient-to-b from-primary-50 to-white', className)}>
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Back button */}
            {onBack && (
              <button
                onClick={onBack}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowLeft size={20} />
                <span className={cn('hidden sm:inline', ageConfig.fontSize.small)}>Back</span>
              </button>
            )}

            {/* Title and progress */}
            <div className="flex-1 mx-4">
              <h1 className={cn('text-center font-semibold text-gray-900', ageConfig.fontSize.body)}>
                {title}
              </h1>
              <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.5, ease: 'easeOut' }}
                />
              </div>
              <p className="text-center text-xs text-gray-500 mt-1">
                {currentQuestion} / {totalQuestions}
              </p>
            </div>

            {/* Streak indicator */}
            {streak > 0 && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="flex items-center gap-1 bg-orange-100 text-orange-700 px-3 py-1 rounded-full"
              >
                <span>🔥</span>
                <span className="font-bold">{streak}</span>
              </motion.div>
            )}
          </div>
        </div>
      </header>

      {/* Main content area */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="relative">
          {/* Exercise content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentQuestion}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: ageConfig.animations.duration }}
            >
              {children}
            </motion.div>
          </AnimatePresence>

          {/* Next button (when available) */}
          {showNext && onNext && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8 flex justify-center"
            >
              <button
                onClick={onNext}
                className={cn(
                  'flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white',
                  'font-semibold rounded-full px-8 py-3 transition-all shadow-lg hover:shadow-xl',
                  ageConfig.fontSize.body
                )}
              >
                Next
                <ArrowRight size={20} />
              </button>
            </motion.div>
          )}
        </div>
      </main>

      {/* Peppi companion */}
      <AnimatePresence>
        {showPeppi && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            className="fixed bottom-4 left-4 z-40"
          >
            <PeppiSpeech
              trigger={currentPeppiTrigger}
              size={ageConfig.variant === 'junior' ? 'lg' : 'md'}
              position="left"
              autoSpeak={currentPeppiTrigger !== 'idle'}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default ExerciseWrapper;
