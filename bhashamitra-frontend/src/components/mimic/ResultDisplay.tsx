'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, Trophy, Share2, RotateCcw, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { soundService } from '@/lib/soundService';
import { PeppiMimicAttemptResult, getStarRating } from '@/types';

interface ResultDisplayProps {
  result: PeppiMimicAttemptResult;
  challengeWord: string;
  onShare?: () => void;
  onTryAgain?: () => void;
  onNext?: () => void;
  className?: string;
}

export function ResultDisplay({
  result,
  challengeWord,
  onShare,
  onTryAgain,
  onNext,
  className,
}: ResultDisplayProps) {
  const [showStars, setShowStars] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [showButtons, setShowButtons] = useState(false);
  const soundsPlayedRef = useRef(false);

  const starRating = getStarRating(result.stars);

  // Staggered animation sequence with sound effects
  useEffect(() => {
    const timers: NodeJS.Timeout[] = [];

    // Show stars after initial delay and play star sounds
    timers.push(setTimeout(() => {
      setShowStars(true);

      // Play sounds only once
      if (!soundsPlayedRef.current) {
        soundsPlayedRef.current = true;

        // Play star earned sounds for each star (staggered)
        for (let i = 0; i < result.stars; i++) {
          timers.push(setTimeout(() => {
            soundService.playStarEarned(i);
          }, i * 200 + 100));
        }

        // Play the result sound after stars animate
        timers.push(setTimeout(() => {
          soundService.playMimicResult(result.stars);
        }, result.stars * 200 + 300));
      }
    }, 500));

    // Show details after stars
    timers.push(setTimeout(() => setShowDetails(true), 1500));

    // Show buttons last
    timers.push(setTimeout(() => setShowButtons(true), 2000));

    return () => timers.forEach(clearTimeout);
  }, [result.stars]);

  const renderStars = () => {
    return (
      <div className="flex justify-center gap-2 mb-6">
        {[0, 1, 2].map((index) => (
          <motion.div
            key={index}
            initial={{ scale: 0, rotate: -180, opacity: 0 }}
            animate={showStars ? {
              scale: 1,
              rotate: 0,
              opacity: 1,
            } : {}}
            transition={{
              delay: index * 0.2,
              type: "spring",
              stiffness: 200,
              damping: 10,
            }}
          >
            <Star
              size={56}
              className={cn(
                "transition-colors duration-300",
                index < result.stars
                  ? "fill-yellow-400 text-yellow-400 drop-shadow-lg"
                  : "fill-gray-200 text-gray-300"
              )}
            />
          </motion.div>
        ))}
      </div>
    );
  };

  return (
    <div className={cn("text-center", className)}>
      {/* Stars */}
      {renderStars()}

      {/* Score and Label */}
      <AnimatePresence>
        {showStars && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h2 className={cn(
              "text-3xl font-bold mb-2",
              result.stars === 3 ? "text-yellow-500" :
              result.stars === 2 ? "text-green-500" :
              result.stars === 1 ? "text-blue-500" :
              "text-gray-500"
            )}>
              {starRating.label}
            </h2>

            {/* Score percentage */}
            <div className="text-5xl font-extrabold text-gray-800 mb-1">
              {Math.round(result.score)}%
            </div>

            {/* Points earned */}
            <div className="flex items-center justify-center gap-2 mb-6">
              <Trophy className="text-amber-500" size={20} />
              <span className="text-lg font-semibold text-amber-600">
                +{result.points_earned} points
              </span>
              {result.is_personal_best && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="bg-purple-100 text-purple-700 text-xs font-bold px-2 py-1 rounded-full"
                >
                  NEW BEST!
                </motion.span>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Peppi Feedback */}
      <AnimatePresence>
        {showDetails && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl p-6 mb-6 mx-4"
          >
            {/* Peppi avatar placeholder */}
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 bg-primary-200 rounded-full flex items-center justify-center text-3xl flex-shrink-0">
                {result.stars === 3 ? '🎉' :
                 result.stars === 2 ? '😊' :
                 result.stars === 1 ? '💪' : '🤗'}
              </div>
              <div className="text-left flex-1">
                <p className="font-semibold text-primary-800 mb-1">Peppi says:</p>
                <p className="text-gray-700">{result.peppi_feedback}</p>
              </div>
            </div>

            {/* Transcription feedback */}
            {result.transcription && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-500 mb-1">You said:</p>
                <p className="text-lg font-medium text-gray-800">
                  &ldquo;{result.transcription}&rdquo;
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Target: <span className="font-medium">{challengeWord}</span>
                </p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Mastery badge */}
      <AnimatePresence>
        {showDetails && result.mastered && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
            className="mb-6"
          >
            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-yellow-400 to-amber-500 text-white px-6 py-3 rounded-full shadow-lg">
              <Trophy size={24} />
              <span className="font-bold">Word Mastered!</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Action Buttons */}
      <AnimatePresence>
        {showButtons && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col sm:flex-row gap-3 justify-center px-4"
          >
            {/* Try Again */}
            <motion.button
              onClick={() => {
                soundService.onClick();
                onTryAgain?.();
              }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition-colors"
            >
              <RotateCcw size={20} />
              Try Again
            </motion.button>

            {/* Share Button */}
            {onShare && result.stars >= 2 && (
              <motion.button
                onClick={() => {
                  soundService.onClick();
                  onShare?.();
                }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-xl font-semibold transition-colors"
              >
                <Share2 size={20} />
                Share with Family
              </motion.button>
            )}

            {/* Next Challenge */}
            {onNext && (
              <motion.button
                onClick={() => {
                  soundService.onClick();
                  onNext?.();
                }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-semibold transition-colors"
              >
                Next Word
                <ChevronRight size={20} />
              </motion.button>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Progress summary */}
      <AnimatePresence>
        {showButtons && result.progress && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-8 text-sm text-gray-500"
          >
            <p>
              Best score: <span className="font-semibold">{Math.round(result.progress.best_score)}%</span>
              {' | '}
              Total attempts: <span className="font-semibold">{result.progress.total_attempts}</span>
              {' | '}
              Points: <span className="font-semibold">{result.progress.total_points}</span>
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default ResultDisplay;
