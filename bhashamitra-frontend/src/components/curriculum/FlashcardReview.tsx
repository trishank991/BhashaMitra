'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, RotateCcw, TrendingUp, Award, Calendar, Flame } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/stores';
import { api, Flashcard } from '@/lib/api';

interface FlashcardReviewProps {
  onComplete?: (score: number) => void;
  maxCards?: number;
  className?: string;
}

type DifficultyRating = 1 | 2 | 3 | 4;

interface ReviewStats {
  total: number;
  reviewed: number;
  correct: number;
  sessionScore: number;
}

const DIFFICULTY_CONFIG = {
  1: {
    label: 'Again',
    color: 'bg-red-500 hover:bg-red-600',
    emoji: '😰',
    description: "I don't remember",
  },
  2: {
    label: 'Hard',
    color: 'bg-orange-500 hover:bg-orange-600',
    emoji: '🤔',
    description: 'Hard to recall',
  },
  3: {
    label: 'Good',
    color: 'bg-blue-500 hover:bg-blue-600',
    emoji: '😊',
    description: 'Got it right',
  },
  4: {
    label: 'Easy',
    color: 'bg-green-500 hover:bg-green-600',
    emoji: '😄',
    description: 'Very easy!',
  },
} as const;

export function FlashcardReview({ onComplete, maxCards = 20, className }: FlashcardReviewProps) {
  const { activeChild } = useAuthStore();

  const [isLoading, setIsLoading] = useState(true);
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isReviewing, setIsReviewing] = useState(false);
  const [stats, setStats] = useState<ReviewStats>({
    total: 0,
    reviewed: 0,
    correct: 0,
    sessionScore: 0,
  });
  const [streak, setStreak] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const currentCard = cards[currentIndex];

  // Fetch flashcards on mount
  useEffect(() => {
    fetchFlashcards();
  }, [activeChild?.id]);

  const fetchFlashcards = async () => {
    if (!activeChild?.id) {
      setError('Please select a child profile');
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await api.getFlashcardsDue(activeChild.id, maxCards);
      if (response.success && response.data) {
        setCards(response.data);
        setStats({
          total: response.data.length,
          reviewed: 0,
          correct: 0,
          sessionScore: 0,
        });
      } else {
        setError(response.error || 'Failed to fetch flashcards');
      }
    } catch {
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const playAudio = async (text: string, audioUrl?: string) => {
    setIsPlaying(true);
    try {
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.onended = () => setIsPlaying(false);
        audio.onerror = () => setIsPlaying(false);
        await audio.play();
      } else {
        const response = await api.getAudio(text, 'HINDI', 'kid_friendly');
        if (response.success && response.audioUrl) {
          const audio = new Audio(response.audioUrl);
          audio.onended = () => setIsPlaying(false);
          audio.onerror = () => setIsPlaying(false);
          await audio.play();
        } else {
          setIsPlaying(false);
        }
      }
    } catch (error) {
      console.error('Audio playback error:', error);
      setIsPlaying(false);
    }
  };

  const handleFlip = useCallback(() => {
    if (!isReviewing) {
      setIsFlipped(!isFlipped);
    }
  }, [isFlipped, isReviewing]);

  const handleReview = async (rating: DifficultyRating) => {
    if (!currentCard || !activeChild?.id || isReviewing) return;

    setIsReviewing(true);

    try {
      const response = await api.reviewFlashcard(activeChild.id, currentCard.word_id, rating);

      if (response.success) {
        const wasCorrect = rating >= 3;
        const newReviewed = stats.reviewed + 1;
        const newCorrect = stats.correct + (wasCorrect ? 1 : 0);
        const newScore = Math.round((newCorrect / newReviewed) * 100);

        setStats({
          total: stats.total,
          reviewed: newReviewed,
          correct: newCorrect,
          sessionScore: newScore,
        });

        if (wasCorrect) {
          setStreak(streak + 1);
          if ((streak + 1) % 5 === 0) {
            setShowCelebration(true);
            setTimeout(() => setShowCelebration(false), 2000);
          }
        } else {
          setStreak(0);
        }

        setTimeout(() => {
          if (currentIndex < cards.length - 1) {
            setCurrentIndex(currentIndex + 1);
            setIsFlipped(false);
          } else {
            onComplete?.(newScore);
          }
          setIsReviewing(false);
        }, 600);
      } else {
        setError(response.error || 'Failed to submit review');
        setIsReviewing(false);
      }
    } catch {
      setError('Network error. Please try again.');
      setIsReviewing(false);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setIsFlipped(false);
    setStats({
      total: cards.length,
      reviewed: 0,
      correct: 0,
      sessionScore: 0,
    });
    setStreak(0);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className={cn('flex items-center justify-center min-h-[400px]', className)}>
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-600">Loading flashcards...</p>
        </div>
      </div>
    );
  }

  // Empty state
  if (cards.length === 0 && !error) {
    return (
      <div className={cn('flex flex-col items-center justify-center min-h-[400px] text-center', className)}>
        <div className="text-6xl mb-4">🎉</div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          All Caught Up!
        </h3>
        <p className="text-gray-600 max-w-md">
          You&apos;ve reviewed all due flashcards for today. Great job! Come back tomorrow for more practice.
        </p>
        <div className="mt-6 flex items-center gap-2 text-green-600">
          <Award size={24} />
          <span className="font-semibold">Daily Goal Complete!</span>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className={cn('flex flex-col items-center justify-center min-h-[400px] text-center', className)}>
        <div className="text-6xl mb-4">😕</div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Oops!
        </h3>
        <p className="text-gray-600 max-w-md mb-6">{error}</p>
        <button
          onClick={fetchFlashcards}
          className="flex items-center gap-2 bg-primary-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-primary-600 transition-colors"
        >
          <RotateCcw size={20} />
          Try Again
        </button>
      </div>
    );
  }

  // Session complete
  if (stats.reviewed >= stats.total && stats.total > 0) {
    return (
      <div className={cn('flex flex-col items-center justify-center min-h-[400px] text-center', className)}>
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', duration: 0.5 }}
          className="text-8xl mb-6"
        >
          🎉
        </motion.div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Session Complete!
        </h2>

        {/* Stats Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 max-w-2xl w-full">
          <div className="bg-blue-50 rounded-2xl p-6 border-2 border-blue-200">
            <div className="text-3xl font-bold text-blue-600 mb-1">{stats.reviewed}</div>
            <div className="text-sm text-gray-600">Cards Reviewed</div>
          </div>
          <div className="bg-green-50 rounded-2xl p-6 border-2 border-green-200">
            <div className="text-3xl font-bold text-green-600 mb-1">{stats.correct}</div>
            <div className="text-sm text-gray-600">Remembered</div>
          </div>
          <div className="bg-purple-50 rounded-2xl p-6 border-2 border-purple-200">
            <div className="text-3xl font-bold text-purple-600 mb-1">{stats.sessionScore}%</div>
            <div className="text-sm text-gray-600">Score</div>
          </div>
        </div>

        <p className="text-gray-700 max-w-md mb-6">
          {stats.sessionScore >= 90
            ? "Outstanding! You're a vocabulary champion! 🏆"
            : stats.sessionScore >= 70
            ? "Great work! Keep practicing to master these words! 🌟"
            : "Good effort! Review these cards again tomorrow to improve! 💪"}
        </p>

        <div className="flex gap-4">
          <button
            onClick={handleRestart}
            className="flex items-center gap-2 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-medium hover:bg-gray-50 transition-colors"
          >
            <RotateCcw size={20} />
            Review Again
          </button>
          <button
            onClick={() => onComplete?.(stats.sessionScore)}
            className="flex items-center gap-2 bg-primary-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-primary-600 transition-colors"
          >
            <Award size={20} />
            Done
          </button>
        </div>
      </div>
    );
  }

  // Main flashcard interface
  return (
    <div className={cn('max-w-4xl mx-auto', className)}>
      {/* Progress Header */}
      <div className="mb-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Calendar className="text-primary-500" size={24} />
            <div>
              <div className="text-sm text-gray-500">Progress</div>
              <div className="font-bold text-gray-900">
                {stats.reviewed} / {stats.total} cards
              </div>
            </div>
          </div>

          {streak > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-2 bg-orange-100 px-4 py-2 rounded-full border-2 border-orange-300"
            >
              <Flame className="text-orange-500" size={20} />
              <div className="font-bold text-orange-700">{streak} streak</div>
            </motion.div>
          )}

          {stats.reviewed > 0 && (
            <div className="flex items-center gap-2">
              <TrendingUp className="text-green-500" size={20} />
              <div className="font-bold text-gray-900">{stats.sessionScore}%</div>
            </div>
          )}
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <motion.div
            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-full rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(stats.reviewed / stats.total) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Celebration */}
      <AnimatePresence>
        {showCelebration && (
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="fixed top-20 left-1/2 -translate-x-1/2 text-6xl z-50"
          >
            🎉
          </motion.div>
        )}
      </AnimatePresence>

      {/* Flashcard */}
      <div className="relative mb-8">
        <div
          className="relative h-[400px] cursor-pointer"
          onClick={handleFlip}
          style={{ perspective: '1000px' }}
        >
          <motion.div
            className="relative w-full h-full"
            animate={{ rotateY: isFlipped ? 180 : 0 }}
            transition={{ duration: 0.6, type: 'spring' }}
            style={{ transformStyle: 'preserve-3d' }}
          >
            {/* Front of card */}
            <div
              className="absolute inset-0 rounded-3xl border-4 border-primary-300 bg-gradient-to-br from-primary-50 to-white shadow-2xl p-8 flex flex-col items-center justify-center"
              style={{ backfaceVisibility: 'hidden' }}
            >
              {/* New badge */}
              {currentCard?.is_new && (
                <div className="absolute top-4 left-4 bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-sm font-bold">
                  NEW
                </div>
              )}

              {/* Audio button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  playAudio(currentCard?.word || '', currentCard?.pronunciation_audio_url);
                }}
                disabled={isPlaying}
                className={cn(
                  'absolute top-4 right-4 w-14 h-14 rounded-full flex items-center justify-center shadow-lg transition-all',
                  isPlaying
                    ? 'bg-primary-300 animate-pulse'
                    : 'bg-primary-500 hover:bg-primary-600'
                )}
              >
                <Volume2 className="text-white" size={24} />
              </button>

              <div className="text-center">
                <p className="text-7xl md:text-8xl font-bold text-gray-900 mb-4">
                  {currentCard?.word}
                </p>
                <p className="text-2xl text-primary-600 font-semibold mb-2">
                  {currentCard?.romanization}
                </p>
                {(currentCard?.part_of_speech || currentCard?.gender) && (
                  <span className="inline-block bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium">
                    {currentCard?.part_of_speech}
                    {currentCard?.gender && ` • ${currentCard.gender}`}
                  </span>
                )}
              </div>

              <p className="absolute bottom-8 text-gray-400 text-sm">
                Tap card to reveal meaning
              </p>
            </div>

            {/* Back of card */}
            <div
              className="absolute inset-0 rounded-3xl border-4 border-green-300 bg-gradient-to-br from-green-50 to-white shadow-2xl p-8 flex flex-col items-center justify-center"
              style={{
                backfaceVisibility: 'hidden',
                transform: 'rotateY(180deg)',
              }}
            >
              <div className="text-center">
                <div className="text-6xl mb-6">✅</div>
                <p className="text-3xl font-bold text-gray-900 mb-2">
                  {currentCard?.translation}
                </p>
                <p className="text-xl text-gray-600">
                  ({currentCard?.romanization})
                </p>
              </div>

              <p className="absolute bottom-8 text-gray-400 text-sm">
                How well did you remember?
              </p>
            </div>
          </motion.div>
        </div>

        {/* Helper text */}
        {!isFlipped && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center text-gray-500 mt-4 text-sm"
          >
            Try to remember the meaning, then tap to reveal
          </motion.p>
        )}
      </div>

      {/* Difficulty Buttons */}
      <AnimatePresence>
        {isFlipped && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4"
          >
            {(Object.entries(DIFFICULTY_CONFIG) as [string, typeof DIFFICULTY_CONFIG[DifficultyRating]][]).map(
              ([rating, config]) => (
                <motion.button
                  key={rating}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleReview(Number(rating) as DifficultyRating)}
                  disabled={isReviewing}
                  className={cn(
                    'flex flex-col items-center justify-center py-6 text-white rounded-2xl font-medium transition-all shadow-lg',
                    config.color,
                    isReviewing && 'opacity-50 cursor-not-allowed'
                  )}
                >
                  <span className="text-3xl mb-2">{config.emoji}</span>
                  <span className="font-bold text-lg">{config.label}</span>
                  <span className="text-xs opacity-90 mt-1">{config.description}</span>
                </motion.button>
              )
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* SM-2 Info */}
      {isFlipped && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-xl p-4 text-sm text-gray-600">
          <p className="flex items-center gap-2">
            <span>💡</span>
            <span>
              <strong>Spaced Repetition:</strong> Cards you find easy will appear less often, while
              harder cards will be shown more frequently to help you learn.
            </span>
          </p>
        </div>
      )}
    </div>
  );
}

export default FlashcardReview;
