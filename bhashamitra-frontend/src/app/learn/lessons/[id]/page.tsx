'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button } from '@/components/ui';
import { ProgressRing, LessonContentView } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { LessonWithProgress } from '@/types';

export default function LessonDetailPage() {
  const router = useRouter();
  const params = useParams();
  const lessonId = params.id as string;

  const [isHydrated, setIsHydrated] = useState(false);
  const [lesson, setLesson] = useState<LessonWithProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
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

    const fetchLessonData = async () => {
      setLoading(true);
      try {
        const response = await api.getLesson(lessonId, activeChild?.id);
        if (response.success && response.data) {
          setLesson(response.data);
        } else {
          setError(response.error || 'Failed to load lesson');
        }
      } catch (err) {
        setError('Failed to load lesson data');
      } finally {
        setLoading(false);
      }
    };

    fetchLessonData();
  }, [isHydrated, isAuthenticated, lessonId, activeChild?.id, router]);

  const handleCompleteLesson = async () => {
    if (!activeChild || !lesson) return;

    setCompleting(true);
    try {
      // Simulate completing with a high score (in real app, this would be based on actual performance)
      const response = await api.updateLessonProgress(lessonId, activeChild.id, 100);
      if (response.success && response.data) {
        // Refresh lesson data
        const updated = await api.getLesson(lessonId, activeChild.id);
        if (updated.success && updated.data) {
          setLesson(updated.data);
        }
      }
    } catch (err) {
      setError('Failed to update progress');
    } finally {
      setCompleting(false);
    }
  };

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
          <Loading size="lg" text="Loading lesson..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !lesson) {
    return (
      <MainLayout>
        <div className="text-center py-16">
          <p className="text-red-500 mb-4">{error || 'Lesson not found'}</p>
          <Link href="/learn/levels" className="text-indigo-600 hover:underline">
            Back to Levels
          </Link>
        </div>
      </MainLayout>
    );
  }

  const isCompleted = lesson.progress?.is_complete;
  const bestScore = lesson.progress?.best_score || 0;
  const attempts = lesson.progress?.attempts || 0;

  // Calculate stars (0-3)
  const getStars = (score: number) => {
    if (score >= lesson.mastery_threshold) return 3;
    if (score >= lesson.mastery_threshold * 0.75) return 2;
    if (score >= lesson.mastery_threshold * 0.5) return 1;
    return 0;
  };

  const stars = getStars(bestScore);

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Back Button */}
        <motion.div variants={fadeInUp}>
          <Link
            href={`/learn/modules/${lesson.module}`}
            className="inline-flex items-center text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Module
          </Link>
        </motion.div>

        {/* Lesson Header */}
        <motion.div variants={fadeInUp}>
          <Card className="overflow-hidden">
            <div className="p-6">
              <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold">
                  {lesson.order}
                </div>
                <div className="flex-1">
                  <h1 className="text-xl font-bold text-gray-900">{lesson.title_english}</h1>
                  <p className="text-gray-600">
                    {lesson.title_hindi} ({lesson.title_romanized})
                  </p>
                  {lesson.description && (
                    <p className="text-sm text-gray-500 mt-2">{lesson.description}</p>
                  )}
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-4 gap-3 mt-6">
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-indigo-600">{lesson.estimated_minutes}</p>
                  <p className="text-xs text-gray-500">Minutes</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-amber-600">{lesson.points_available}</p>
                  <p className="text-xs text-gray-500">Points</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-green-600">{lesson.mastery_threshold}%</p>
                  <p className="text-xs text-gray-500">To Master</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-purple-600">{attempts}</p>
                  <p className="text-xs text-gray-500">Attempts</p>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Peppi Introduction */}
        {lesson.peppi_intro && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🦜</span>
              <div>
                <p className="font-medium text-amber-900">{lesson.peppi_intro}</p>
                <p className="text-xs text-amber-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Progress Card */}
        {(isCompleted || attempts > 0) && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-gradient-to-br from-green-50 to-emerald-50">
              <div className="flex items-center gap-4">
                <ProgressRing
                  progress={bestScore}
                  size={80}
                  strokeWidth={6}
                  color={isCompleted ? '#22c55e' : '#f59e0b'}
                >
                  <span className="text-lg font-bold" style={{ color: isCompleted ? '#22c55e' : '#f59e0b' }}>
                    {bestScore}%
                  </span>
                </ProgressRing>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900">
                    {isCompleted ? 'Lesson Complete!' : 'In Progress'}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Best Score: {bestScore}% • {attempts} attempt{attempts !== 1 ? 's' : ''}
                  </p>
                  <div className="flex gap-1 mt-2">
                    {[1, 2, 3].map((star) => (
                      <svg
                        key={star}
                        className={`w-6 h-6 ${star <= stars ? 'text-amber-400' : 'text-gray-200'}`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Lesson Content */}
        <motion.div variants={fadeInUp}>
          {lesson.content && Object.keys(lesson.content).length > 0 ? (
            <LessonContentView
              content={lesson.content}
              lessonType={lesson.lesson_type || 'LEARNING'}
              language={activeChild?.language as string || 'HINDI'}
              onComplete={() => {
                // Auto-complete lesson when content is finished
                handleCompleteLesson();
              }}
            />
          ) : (
            <Card>
              <div className="text-center py-8">
                <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 text-lg">Lesson Content</h3>
                <p className="text-gray-500 mt-2">
                  Content for this lesson is being prepared.
                </p>
                <p className="text-sm text-gray-400 mt-1">
                  Check back soon for interactive learning activities!
                </p>
              </div>
            </Card>
          )}
        </motion.div>

        {/* Action Buttons */}
        <motion.div variants={fadeInUp} className="flex gap-3">
          <Button
            variant="outline"
            className="flex-1"
            onClick={() => router.push(`/learn/modules/${lesson.module}`)}
          >
            Back to Module
          </Button>
          <Button
            variant="primary"
            className="flex-1"
            disabled={completing}
            onClick={handleCompleteLesson}
          >
            {completing ? 'Completing...' : isCompleted ? 'Practice Again' : 'Complete Lesson'}
          </Button>
        </motion.div>

        {/* Success Message */}
        {isCompleted && lesson.peppi_success && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🎉</span>
              <div>
                <p className="font-medium text-green-900">{lesson.peppi_success}</p>
                <p className="text-xs text-green-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>
    </MainLayout>
  );
}
