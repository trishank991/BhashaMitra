'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Mic, Star, Filter, Trophy, Loader2, CheckCircle } from 'lucide-react';
import { useAuthStore } from '@/stores';
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';
import {
  PeppiMimicChallengeWithProgress,
  PeppiMimicProgressSummary,
  MimicCategory,
  MimicChallengeFilters,
  MIMIC_CATEGORY_LABELS,
  MIMIC_CATEGORY_ICONS,
  MIMIC_DIFFICULTY_LABELS,
  MimicDifficulty,
} from '@/types';
import { AudioButton } from '@/components/ui/AudioButton';

export default function MimicPracticePage() {
  const router = useRouter();
  const { selectedChild } = useAuthStore();

  const [challenges, setChallenges] = useState<PeppiMimicChallengeWithProgress[]>([]);
  const [progressSummary, setProgressSummary] = useState<PeppiMimicProgressSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<MimicChallengeFilters>({});
  const [showFilters, setShowFilters] = useState(false);

  // Fetch challenges and progress
  const fetchData = useCallback(async () => {
    if (!selectedChild?.id) return;

    setIsLoading(true);
    setError(null);

    try {
      const [challengesRes, progressRes] = await Promise.all([
        api.getMimicChallenges(selectedChild.id, filters),
        api.getMimicProgress(selectedChild.id),
      ]);

      if (challengesRes.success && challengesRes.data) {
        setChallenges(challengesRes.data);
      } else {
        setError(challengesRes.error || 'Failed to load challenges');
      }

      if (progressRes.success && progressRes.data) {
        setProgressSummary(progressRes.data);
      }
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [selectedChild?.id, filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Redirect if no child selected
  useEffect(() => {
    if (!selectedChild) {
      router.push('/home');
    }
  }, [selectedChild, router]);

  const handleChallengeClick = (challengeId: string) => {
    router.push(`/practice/mimic/${challengeId}`);
  };

  const handleFilterChange = (newFilters: Partial<MimicChallengeFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  // Get available categories from challenges
  const availableCategories = Array.from(
    new Set(challenges.map(c => c.category))
  ) as MimicCategory[];

  if (!selectedChild) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white/90 backdrop-blur-md shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-4">
          <button
            onClick={() => router.back()}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div className="flex-1">
            <h1 className="text-xl font-bold text-gray-800">Peppi Mimic</h1>
            <p className="text-sm text-gray-500">Practice pronunciation</p>
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={cn(
              "p-2 rounded-full transition-colors",
              showFilters ? "bg-primary-100 text-primary-600" : "hover:bg-gray-100"
            )}
          >
            <Filter size={24} />
          </button>
        </div>
      </header>

      {/* Progress Summary */}
      {progressSummary && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl mx-auto px-4 py-4"
        >
          <div className="bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl p-4 text-white shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Trophy size={24} />
                <span className="font-semibold">Your Progress</span>
              </div>
              <span className="text-2xl font-bold">{progressSummary.total_points} pts</span>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold">{progressSummary.challenges_attempted}</div>
                <div className="text-xs opacity-80">Attempted</div>
              </div>
              <div>
                <div className="text-2xl font-bold">{progressSummary.challenges_mastered}</div>
                <div className="text-xs opacity-80">Mastered</div>
              </div>
              <div>
                <div className="text-2xl font-bold">{Math.round(progressSummary.average_score)}%</div>
                <div className="text-xs opacity-80">Avg Score</div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Filters */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="max-w-2xl mx-auto px-4 py-3 space-y-3">
              {/* Category Filter */}
              <div>
                <label className="text-sm font-medium text-gray-600 block mb-2">Category</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => handleFilterChange({ category: undefined })}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                      !filters.category
                        ? "bg-primary-500 text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    All
                  </button>
                  {availableCategories.map(category => (
                    <button
                      key={category}
                      onClick={() => handleFilterChange({ category })}
                      className={cn(
                        "px-3 py-1.5 rounded-full text-sm font-medium transition-colors flex items-center gap-1",
                        filters.category === category
                          ? "bg-primary-500 text-white"
                          : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                      )}
                    >
                      <span>{MIMIC_CATEGORY_ICONS[category]}</span>
                      {MIMIC_CATEGORY_LABELS[category]}
                    </button>
                  ))}
                </div>
              </div>

              {/* Difficulty Filter */}
              <div>
                <label className="text-sm font-medium text-gray-600 block mb-2">Difficulty</label>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleFilterChange({ difficulty: undefined })}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                      !filters.difficulty
                        ? "bg-primary-500 text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    All
                  </button>
                  {([1, 2, 3] as MimicDifficulty[]).map(difficulty => (
                    <button
                      key={difficulty}
                      onClick={() => handleFilterChange({ difficulty })}
                      className={cn(
                        "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                        filters.difficulty === difficulty
                          ? "bg-primary-500 text-white"
                          : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                      )}
                    >
                      {MIMIC_DIFFICULTY_LABELS[difficulty]}
                    </button>
                  ))}
                </div>
              </div>

              {/* Status Filter */}
              <div>
                <label className="text-sm font-medium text-gray-600 block mb-2">Status</label>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleFilterChange({ mastered: undefined })}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                      filters.mastered === undefined
                        ? "bg-primary-500 text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    All
                  </button>
                  <button
                    onClick={() => handleFilterChange({ mastered: false })}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                      filters.mastered === false
                        ? "bg-primary-500 text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    To Practice
                  </button>
                  <button
                    onClick={() => handleFilterChange({ mastered: true })}
                    className={cn(
                      "px-3 py-1.5 rounded-full text-sm font-medium transition-colors",
                      filters.mastered === true
                        ? "bg-primary-500 text-white"
                        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    Mastered
                  </button>
                </div>
              </div>

              {/* Clear Filters */}
              {(filters.category || filters.difficulty || filters.mastered !== undefined) && (
                <button
                  onClick={clearFilters}
                  className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  Clear all filters
                </button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Content */}
      <main className="max-w-2xl mx-auto px-4 py-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={fetchData}
              className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
            >
              Try Again
            </button>
          </div>
        ) : challenges.length === 0 ? (
          <div className="text-center py-12">
            <Mic className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No challenges found</p>
            {(filters.category || filters.difficulty || filters.mastered !== undefined) && (
              <button
                onClick={clearFilters}
                className="mt-4 text-primary-600 hover:text-primary-700 font-medium"
              >
                Clear filters
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {challenges.map((challenge, index) => (
              <motion.div
                key={challenge.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => handleChallengeClick(challenge.id)}
                className="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer border border-gray-100"
              >
                <div className="flex items-center gap-4">
                  {/* Category Icon */}
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-2xl flex-shrink-0">
                    {MIMIC_CATEGORY_ICONS[challenge.category]}
                  </div>

                  {/* Word Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl font-bold text-gray-800">{challenge.word}</h3>
                      {challenge.mastered && (
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                      )}
                    </div>
                    <p className="text-sm text-gray-500">
                      {challenge.romanization} • {challenge.meaning}
                    </p>
                    {/* Stars */}
                    {challenge.attempts > 0 && (
                      <div className="flex items-center gap-1 mt-1">
                        {[0, 1, 2].map(i => (
                          <Star
                            key={i}
                            size={14}
                            className={cn(
                              i < challenge.best_stars
                                ? "fill-yellow-400 text-yellow-400"
                                : "text-gray-200"
                            )}
                          />
                        ))}
                        <span className="text-xs text-gray-400 ml-1">
                          {challenge.attempts} attempts
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Play Audio Button */}
                  <div onClick={e => e.stopPropagation()}>
                    <AudioButton
                      text={challenge.word}
                      audioUrl={challenge.audio_url}
                      language={challenge.language}
                      size="sm"
                      variant="secondary"
                    />
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
