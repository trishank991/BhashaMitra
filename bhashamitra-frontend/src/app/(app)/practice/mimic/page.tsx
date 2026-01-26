'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Mic, Star, Filter, Trophy, Loader2, CheckCircle } from 'lucide-react';
import { useAuthStore } from '@/stores';
import api from '@/lib/api'; // Changed to default import to match refined api.ts
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
  const { activeChild: selectedChild } = useAuthStore();

  const [isHydrated, setIsHydrated] = useState(false);
  const [challenges, setChallenges] = useState<PeppiMimicChallengeWithProgress[]>([]);
  const [progressSummary, setProgressSummary] = useState<PeppiMimicProgressSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<MimicChallengeFilters>({});
  const [showFilters, setShowFilters] = useState(false);

  // Handle hydration
  useEffect(() => {
    setIsHydrated(true);
  }, []);

  // Fetch challenges and progress
  const fetchData = useCallback(async () => {
    // Only fetch if hydrated and we have a selected child
    if (!isHydrated || !selectedChild?.id) return;

    setIsLoading(true);
    setError(null);

    try {
      // Adjusted to match the api.ts signature: (childId, filters)
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
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [isHydrated, selectedChild?.id, filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Redirect if no child selected
  useEffect(() => {
    if (isHydrated && !selectedChild) {
      router.push('/home');
    }
  }, [isHydrated, selectedChild, router]);

  const handleChallengeClick = (challengeId: string) => {
    router.push(`/practice/mimic/${challengeId}`);
  };

  const handleFilterChange = (newFilters: Partial<MimicChallengeFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const clearFilters = () => setFilters({});

  const availableCategories = Array.from(
    new Set(challenges.map(c => c.category))
  ) as MimicCategory[];

  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary-50 to-white">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    );
  }

  if (!selectedChild) return null;

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white pb-10">
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

      {/* Progress Summary Card */}
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

      {/* Filter Section (Animated) */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden bg-white border-b"
          >
            <div className="max-w-2xl mx-auto px-4 py-3 space-y-4">
              {/* Category buttons... [Logic remains as you had it] */}
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase mb-2 block">Category</label>
                <div className="flex flex-wrap gap-2">
                  <button onClick={() => handleFilterChange({ category: undefined })} className={cn("px-4 py-1.5 rounded-full text-sm font-medium", !filters.category ? "bg-primary-500 text-white" : "bg-gray-100 text-gray-600")}>All</button>
                  {availableCategories.map(cat => (
                    <button key={cat} onClick={() => handleFilterChange({ category: cat })} className={cn("px-4 py-1.5 rounded-full text-sm font-medium flex items-center gap-2", filters.category === cat ? "bg-primary-500 text-white" : "bg-gray-100 text-gray-600")}>
                      <span>{MIMIC_CATEGORY_ICONS[cat]}</span> {MIMIC_CATEGORY_LABELS[cat]}
                    </button>
                  ))}
                </div>
              </div>
              {/* Other filters... */}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Challenge List */}
      <main className="max-w-2xl mx-auto px-4 py-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12"><Loader2 className="w-8 h-8 animate-spin text-primary-500" /></div>
        ) : challenges.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
            <Mic className="w-16 h-16 text-gray-200 mx-auto mb-4" />
            <p className="text-gray-500">No challenges found matching your filters.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {challenges.map((challenge, index) => (
              <motion.div
                key={challenge.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => handleChallengeClick(challenge.id)}
                className="bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer border border-gray-100 flex items-center gap-4 group"
              >
                <div className="w-14 h-14 bg-primary-50 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
                  {MIMIC_CATEGORY_ICONS[challenge.category]}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-gray-800">{challenge.word}</h3>
                    {challenge.mastered && <CheckCircle className="w-5 h-5 text-green-500" />}
                  </div>
                  <p className="text-sm text-gray-400">{challenge.meaning}</p>
                  {challenge.attempts > 0 && (
                    <div className="flex gap-1 mt-1">
                      {[1, 2, 3].map(i => (
                        <Star key={i} size={12} className={i <= challenge.best_stars ? "fill-yellow-400 text-yellow-400" : "text-gray-200"} />
                      ))}
                    </div>
                  )}
                </div>
                <div onClick={e => e.stopPropagation()}>
                  <AudioButton text={challenge.word} audioUrl={challenge.audio_url} language={challenge.language} size="sm" variant="secondary" />
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
