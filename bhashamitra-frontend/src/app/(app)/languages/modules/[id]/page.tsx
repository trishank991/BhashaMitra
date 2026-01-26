'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading, Breadcrumb } from '@/components/ui';
import { LessonCard, ProgressRing } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { CurriculumModuleWithProgress, LessonWithProgress, MODULE_TYPE_INFO } from '@/types';

export default function ModuleDetailPage() {
  const router = useRouter();
  const params = useParams();
  const moduleId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [module, setModule] = useState<CurriculumModuleWithProgress | null>(null);
  const [lessons, setLessons] = useState<LessonWithProgress[]>([]);
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
    if (!moduleId) {
      setError('Invalid module ID');
      setLoading(false);
      return;
    }

    const fetchModuleData = async () => {
      setLoading(true);
      try {
        const [moduleRes, lessonsRes] = await Promise.all([
          api.getCurriculumModule(moduleId, activeChild?.id),
          api.getModuleLessons(moduleId, activeChild?.id),
        ]);

        if (moduleRes.success && moduleRes.data) {
          setModule(moduleRes.data);
        } else {
          setError(moduleRes.error || 'Failed to load module');
        }

        if (lessonsRes.success && lessonsRes.data) {
          setLessons(lessonsRes.data);
        }
      } catch {
        setError('Failed to load module data');
      } finally {
        setLoading(false);
      }
    };

    fetchModuleData();
  }, [isHydrated, isAuthenticated, moduleId, activeChild?.id, router]);

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
          <Loading size="lg" text="Loading module..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !module) {
    return (
      <MainLayout>
        <div className="text-center py-16">
          <p className="text-red-500 mb-4">{error || 'Module not found'}</p>
          <Link href="/languages/levels" className="text-indigo-600 hover:underline">
            Back to Levels
          </Link>
        </div>
      </MainLayout>
    );
  }

  const typeInfo = MODULE_TYPE_INFO[module.module_type] || {
    label: module.module_type,
    emoji: module.emoji,
    color: '#6366f1',
  };

  const progressPercent = module.total_lessons > 0
    ? Math.round((module.completed_lessons / module.total_lessons) * 100)
    : 0;

  // Determine which lessons are locked
  const getLessonLockedStatus = (lessonIndex: number) => {
    if (lessonIndex === 0) return false; // First lesson always unlocked
    // Lock if previous lesson not complete
    const prevLesson = lessons[lessonIndex - 1];
    return prevLesson && !prevLesson.progress?.is_complete;
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
              { label: 'Level', href: module.level ? `/languages/levels/${module.level}` : '/languages/levels' },
              { label: module.name_english },
            ]}
          />
        </motion.div>

        {/* Module Header */}
        <motion.div
          variants={fadeInUp}
          className="rounded-2xl p-6 text-white"
          style={{ backgroundColor: typeInfo.color }}
        >
          <div className="flex items-start gap-4">
            <ProgressRing
              progress={progressPercent}
              size={72}
              strokeWidth={5}
              color="#ffffff"
              bgColor="rgba(255,255,255,0.3)"
              showText={false}
            >
              <span className="text-2xl">{module.emoji}</span>
            </ProgressRing>

            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="bg-white/20 px-2 py-0.5 rounded-full text-xs font-medium">
                  {typeInfo.label}
                </span>
              </div>
              <h1 className="text-xl font-bold mt-1">{module.name_english}</h1>
              <p className="opacity-90">
                {module.name_hindi} ({module.name_romanized})
              </p>
            </div>
          </div>

          <p className="mt-4 opacity-90 text-sm">{module.description}</p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-white/20 rounded-xl p-2 text-center">
              <p className="text-xl font-bold">{module.completed_lessons}/{module.total_lessons}</p>
              <p className="text-xs opacity-80">Lessons</p>
            </div>
            <div className="bg-white/20 rounded-xl p-2 text-center">
              <p className="text-xl font-bold">{module.progress?.total_points || 0}</p>
              <p className="text-xs opacity-80">Points</p>
            </div>
            <div className="bg-white/20 rounded-xl p-2 text-center">
              <p className="text-xl font-bold">{module.estimated_minutes}m</p>
              <p className="text-xs opacity-80">Est. Time</p>
            </div>
          </div>
        </motion.div>

        {/* Peppi Introduction */}
        {module.peppi_intro && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🐱</span>
              <div>
                <p className="font-medium text-amber-900">{module.peppi_intro}</p>
                <p className="text-xs text-amber-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Lessons */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Lessons</h2>
          {lessons.length === 0 ? (
            <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-xl">
              <p>No lessons available yet.</p>
              <p className="text-sm mt-1">Content coming soon!</p>
            </div>
          ) : (
            <div className="space-y-2">
              {lessons.map((lesson, idx) => (
                <motion.div key={lesson.id} variants={fadeInUp}>
                  <LessonCard
                    lesson={lesson}
                    moduleColor={typeInfo.color}
                    index={idx}
                    isLocked={getLessonLockedStatus(idx)}
                  />
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Module Completion Message */}
        {module.progress?.is_complete && module.peppi_completion && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🎉</span>
              <div>
                <p className="font-bold text-green-900">Module Complete!</p>
                <p className="text-sm text-green-700 mt-1">{module.peppi_completion}</p>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>
    </MainLayout>
  );
}
