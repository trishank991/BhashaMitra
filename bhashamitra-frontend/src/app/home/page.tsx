'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore, useProgressStore, usePeppiStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';

export default function HomePage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated, activeChild } = useAuthStore();
  const { streak, storiesRead, wordsLearned } = useProgressStore();
  const { greet } = usePeppiStore();

  // Handle hydration
  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;

    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    // Greet user when page loads
    const timer = setTimeout(() => {
      greet();
    }, 500);
    return () => clearTimeout(timer);
  }, [isHydrated, isAuthenticated, router, greet]);

  // Show loading while hydrating
  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Redirecting..." />
      </div>
    );
  }

  const languageInfo = activeChild?.language
    ? SUPPORTED_LANGUAGES[activeChild.language.code]
    : SUPPORTED_LANGUAGES.HINDI;

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Quick Stats */}
        <motion.div variants={fadeInUp} className="grid grid-cols-3 gap-3">
          <Card padding="sm" className="text-center">
            <div className="text-2xl mb-1">🔥</div>
            <p className="text-2xl font-bold text-primary-600">{streak}</p>
            <p className="text-xs text-gray-500">Day Streak</p>
          </Card>
          <Card padding="sm" className="text-center">
            <div className="text-2xl mb-1">📖</div>
            <p className="text-2xl font-bold text-secondary-600">{storiesRead.length}</p>
            <p className="text-xs text-gray-500">Stories</p>
          </Card>
          <Card padding="sm" className="text-center">
            <div className="text-2xl mb-1">📝</div>
            <p className="text-2xl font-bold text-accent-600">{wordsLearned.length}</p>
            <p className="text-xs text-gray-500">Words</p>
          </Card>
        </motion.div>

        {/* Current Language */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-primary-500 to-accent-500 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-80">Learning</p>
                <h3 className="text-xl font-bold">{languageInfo?.name}</h3>
                <p className="text-2xl mt-1">{languageInfo?.nativeName}</p>
              </div>
              <span className="text-5xl">{languageInfo?.flag}</span>
            </div>
          </Card>
        </motion.div>

        {/* Continue Learning */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Continue Learning</h2>
          <Link href="/stories">
            <Card interactive className="flex items-center gap-4">
              <div className="w-16 h-16 bg-secondary-100 rounded-2xl flex items-center justify-center text-3xl">
                📚
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900">Story Time</h3>
                <p className="text-sm text-gray-500">Continue where you left off</p>
              </div>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 text-gray-400">
                <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </Card>
          </Link>
        </motion.div>

        {/* Quick Actions */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            <Link href="/stories">
              <Card interactive className="text-center py-6">
                <div className="text-4xl mb-2">📖</div>
                <h3 className="font-semibold text-gray-900">Read Stories</h3>
                <p className="text-xs text-gray-500 mt-1">Fun tales to explore</p>
              </Card>
            </Link>

            <Link href="/games">
              <Card interactive className="text-center py-6">
                <div className="text-4xl mb-2">🎮</div>
                <h3 className="font-semibold text-gray-900">Play Games</h3>
                <p className="text-xs text-gray-500 mt-1">Learn while playing</p>
              </Card>
            </Link>

            <Link href="/progress">
              <Card interactive className="text-center py-6">
                <div className="text-4xl mb-2">🏆</div>
                <h3 className="font-semibold text-gray-900">My Badges</h3>
                <p className="text-xs text-gray-500 mt-1">See your achievements</p>
              </Card>
            </Link>

            <Link href="/profile">
              <Card interactive className="text-center py-6">
                <div className="text-4xl mb-2">👤</div>
                <h3 className="font-semibold text-gray-900">Profile</h3>
                <p className="text-xs text-gray-500 mt-1">Settings & more</p>
              </Card>
            </Link>
          </div>
        </motion.div>

        {/* Daily Goal */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-success-50 border-2 border-success-200">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-success-700">Daily Goal</h3>
                <p className="text-sm text-success-600">
                  Read 1 story and learn 5 new words
                </p>
              </div>
              <Badge variant="success">In Progress</Badge>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
