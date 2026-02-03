'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading, Breadcrumb } from '@/components/ui';
import { ModuleCard, ProgressRing } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { CurriculumLevelWithProgress, CurriculumModuleWithProgress } from '@/types';

export default function LevelDetailPage() {
  const router = useRouter();
  const params = useParams();
  const levelId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [level, setLevel] = useState<CurriculumLevelWithProgress | null>(null);
  const [modules, setModules] = useState<CurriculumModuleWithProgress[]>([]);
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
    if (!levelId) {
      setError('Invalid level ID');
      setLoading(false);
      return;
    }

    const fetchLevelData = async () => {
      setLoading(true);
      try {
        const [levelRes, modulesRes] = await Promise.all([
          api.getCurriculumLevel(levelId, activeChild?.id),
          api.getLevelModules(levelId, activeChild?.id),
        ]);

        if (levelRes.success && levelRes.data) {
          setLevel(levelRes.data);
        } else {
          setError(levelRes.error || 'Failed to load level');
        }

        if (modulesRes.success && modulesRes.data) {
          setModules(modulesRes.data);
        }
      } catch {
        setError('Failed to load level data');
      } finally {
        setLoading(false);
      }
    };

    fetchLevelData();
  }, [isHydrated, isAuthenticated, levelId, activeChild?.id, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center py-16">
          <Loading size="lg" text="Loading level..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !level) {
    return (
      <MainLayout>
        <div className="text-center py-16">
          <p className="text-red-500 mb-4">{error || 'Level not found'}</p>
          <Link href="/languages/levels" className="text-indigo-600 hover:underline">
            Back to Levels
          </Link>
        </div>
      </MainLayout>
    );
  }

  const progressPercent = level.total_modules > 0
    ? Math.round((level.completed_modules / level.total_modules) * 100)
    : 0;

  // Determine which modules are locked
  const getModuleLockedStatus = (moduleIndex: number) => {
    if (moduleIndex === 0) return false; // First module always unlocked
    // Lock if previous module not complete
    const prevModule = modules[moduleIndex - 1];
    return prevModule && !prevModule.progress?.is_complete;
  };

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Breadcrumb Navigation */}
        <motion.div variants={fadeInUp}>
          <Breadcrumb
            items={[
              { label: 'Languages', href: '/languages', emoji: '\uD83D\uDCDA' },
              { label: 'Levels', href: '/languages/levels' },
              { label: level.name_english, emoji: level.emoji },
            ]}
          />
        </motion.div>

        {/* Level Header */}
        <motion.div
          variants={fadeInUp}
          className="rounded-2xl p-6 text-white"
          style={{ backgroundColor: level.theme_color }}
        >
          <div className="flex items-start gap-4">
            <ProgressRing
              progress={progressPercent}
              size={80}
              strokeWidth={6}
              color="#ffffff"
              bgColor="rgba(255,255,255,0.3)"
              showText={false}
            >
              <span className="text-3xl">{level.emoji}</span>
            </ProgressRing>

            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="bg-white/20 px-2 py-0.5 rounded-full text-sm font-bold">
                  {level.code}
                </span>
                <span className="text-sm opacity-80">
                  Ages {level.min_age}-{level.max_age}
                </span>
              </div>
              <h1 className="text-2xl font-bold mt-1">{level.name_english}</h1>
              <p className="text-lg opacity-90">
                {level.name_hindi} ({level.name_romanized})
              </p>
            </div>
          </div>

          <p className="mt-4 opacity-90">{level.description}</p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mt-4">
            <div className="bg-white/20 rounded-xl p-3 text-center">
              <p className="text-2xl font-bold">{level.completed_modules}/{level.total_modules}</p>
              <p className="text-xs opacity-80">Modules</p>
            </div>
            <div className="bg-white/20 rounded-xl p-3 text-center">
              <p className="text-2xl font-bold">{level.progress?.total_points || 0}</p>
              <p className="text-xs opacity-80">Points</p>
            </div>
            <div className="bg-white/20 rounded-xl p-3 text-center">
              <p className="text-2xl font-bold">{level.estimated_hours}h</p>
              <p className="text-xs opacity-80">Est. Time</p>
            </div>
          </div>
        </motion.div>

        {/* Peppi Message */}
        {level.peppi_welcome && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🐱</span>
              <div>
                <p className="font-medium text-amber-900">{level.peppi_welcome}</p>
                <p className="text-xs text-amber-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Learning Objectives */}
        {level.learning_objectives && level.learning_objectives.length > 0 && (
          <motion.div variants={fadeInUp}>
            <h2 className="text-lg font-bold text-gray-900 mb-3">Learning Objectives</h2>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
              <ul className="space-y-2">
                {level.learning_objectives.map((objective, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-green-500 mt-0.5">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </span>
                    <span className="text-sm text-gray-700">{objective}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {/* Modules */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Modules</h2>
          {modules.length === 0 ? (
            <div className="text-center py-8 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border-2 border-dashed border-purple-200">
              <span className="text-4xl mb-3 block">🚀</span>
              <p className="font-semibold text-purple-800">Coming Soon!</p>
              <p className="text-sm text-purple-600 mt-2 px-4">
                We&apos;re working hard to create amazing content for {level.name_english}.
                <br />Check back soon!
              </p>
              <Link
                href="/languages/levels"
                className="inline-block mt-4 px-4 py-2 bg-purple-600 text-white rounded-xl text-sm font-medium hover:bg-purple-700 transition-colors"
              >
                Explore Other Levels
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {modules.map((module, idx) => (
                <motion.div key={module.id} variants={fadeInUp}>
                  <ModuleCard
                    module={module}
                    levelColor={level.theme_color}
                    isLocked={getModuleLockedStatus(idx)}
                  />
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
