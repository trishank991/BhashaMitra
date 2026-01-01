'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading } from '@/components/ui';
import { LevelCard } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { CurriculumLevelWithProgress } from '@/types';

export default function LevelsPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [levels, setLevels] = useState<CurriculumLevelWithProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchLevels = async () => {
      setLoading(true);
      try {
        const response = await api.getCurriculumLevels(activeChild?.id);
        if (response.success && response.data) {
          setLevels(response.data);
        } else {
          setError(response.error || 'Failed to load levels');
        }
      } catch {
        setError('Failed to load curriculum levels');
      } finally {
        setLoading(false);
      }
    };

    fetchLevels();
  }, [isHydrated, isAuthenticated, activeChild?.id, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  // Find current level based on child's level or first incomplete
  const currentLevelOrder = activeChild?.level || 1;
  const currentLevel = levels.find(l => l.order === currentLevelOrder);

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Header */}
        <motion.div variants={fadeInUp}>
          <h1 className="text-2xl font-bold text-gray-900">Your Learning Journey</h1>
          <p className="text-gray-500 mt-1">
            {activeChild?.name ? `${activeChild.name}'s` : 'Your'} path to Hindi mastery
          </p>
        </motion.div>

        {/* Current Level Highlight */}
        {currentLevel && (
          <motion.div variants={fadeInUp}>
            <div
              className="p-4 rounded-2xl text-white"
              style={{ backgroundColor: currentLevel.theme_color }}
            >
              <div className="flex items-center gap-3">
                <span className="text-4xl">{currentLevel.emoji}</span>
                <div>
                  <p className="text-sm opacity-90">Currently at</p>
                  <h2 className="text-xl font-bold">
                    {currentLevel.code}: {currentLevel.name_english}
                  </h2>
                  <p className="text-sm opacity-90">{currentLevel.name_hindi}</p>
                </div>
              </div>
              {currentLevel.peppi_welcome && (
                <div className="mt-3 p-3 bg-white/20 rounded-xl">
                  <p className="text-sm italic">&ldquo;{currentLevel.peppi_welcome}&rdquo;</p>
                  <p className="text-xs mt-1 opacity-80">- Peppi</p>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* Levels List */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">All Levels</h2>
          {loading ? (
            <div className="flex justify-center py-8">
              <Loading size="md" text="Loading levels..." />
            </div>
          ) : error ? (
            <div className="text-center py-8 text-red-500">{error}</div>
          ) : levels.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No curriculum levels available yet.
            </div>
          ) : (
            <div className="space-y-4">
              {levels.map((level) => {
                // Determine if level is locked (must complete previous level first)
                const isLocked = level.order > currentLevelOrder + 1;
                const isCurrent = level.order === currentLevelOrder;

                return (
                  <motion.div
                    key={level.id}
                    variants={fadeInUp}
                  >
                    <LevelCard
                      level={level}
                      isLocked={isLocked}
                      isCurrent={isCurrent}
                    />
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>

        {/* Learning Tips */}
        <motion.div variants={fadeInUp}>
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-4">
            <h3 className="font-bold text-indigo-900 mb-2">Learning Tips</h3>
            <ul className="text-sm text-indigo-700 space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-indigo-500">1.</span>
                Complete modules in order for best results
              </li>
              <li className="flex items-start gap-2">
                <span className="text-indigo-500">2.</span>
                Practice daily to maintain your streak
              </li>
              <li className="flex items-start gap-2">
                <span className="text-indigo-500">3.</span>
                Earn 3 stars on lessons to unlock achievements
              </li>
            </ul>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
