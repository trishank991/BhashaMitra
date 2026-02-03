'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading } from '@/components/ui';
import { XPProgressBar } from '@/components/ui/ProgressBar';
import { useProgressStore, useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, LEVEL_TITLES, XP_PER_LEVEL } from '@/lib/constants';

export default function ProgressPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated } = useAuthStore();
  const { xp, level, streak, badges, storiesRead, wordsLearned, gameSessions } =
    useProgressStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

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

  const levelTitle = LEVEL_TITLES[level] || `Level ${level}`;

  // Mock achievements for display
  const allBadges = [
    {
      id: 'first-story',
      name: 'Story Starter',
      description: 'Read your first story!',
      icon: '📖',
      earned: badges.some((b) => b.id === 'first-story'),
    },
    {
      id: 'streak-7',
      name: 'Week Warrior',
      description: 'Practice for 7 days in a row',
      icon: '🔥',
      earned: badges.some((b) => b.id === 'streak-7'),
    },
    {
      id: 'words-10',
      name: 'Word Collector',
      description: 'Learn 10 new words',
      icon: '📝',
      earned: badges.some((b) => b.id === 'words-10'),
    },
    {
      id: 'game-master',
      name: 'Game Master',
      description: 'Win 5 games in a row',
      icon: '🎮',
      earned: false,
    },
    {
      id: 'story-10',
      name: 'Bookworm',
      description: 'Read 10 stories',
      icon: '📚',
      earned: badges.some((b) => b.id === 'story-10'),
    },
    {
      id: 'streak-30',
      name: 'Monthly Master',
      description: 'Practice for 30 days',
      icon: '⭐',
      earned: badges.some((b) => b.id === 'streak-30'),
    },
  ];

  return (
    <MainLayout headerTitle="My Progress" showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Level Card */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-primary-500 to-accent-500 text-white">
            <div className="text-center mb-4">
              <span className="text-6xl">🏆</span>
              <h2 className="text-2xl font-bold mt-2">Level {level}</h2>
              <p className="text-lg opacity-90">{levelTitle}</p>
            </div>
            <div className="bg-white/20 rounded-xl p-4">
              <XPProgressBar
                currentXP={xp}
                xpForNextLevel={XP_PER_LEVEL * level}
                level={level}
                className="[&_*]:text-white [&_.text-primary-600]:text-white [&_.text-gray-500]:text-white/80"
              />
            </div>
          </Card>
        </motion.div>

        {/* Stats Grid */}
        <motion.div variants={fadeInUp} className="grid grid-cols-2 gap-3">
          <Card className="text-center">
            <span className="text-3xl mb-2 block">🔥</span>
            <p className="text-3xl font-bold text-primary-600">{streak}</p>
            <p className="text-sm text-gray-500">Day Streak</p>
          </Card>
          <Card className="text-center">
            <span className="text-3xl mb-2 block">⭐</span>
            <p className="text-3xl font-bold text-warning-500">{xp + level * XP_PER_LEVEL}</p>
            <p className="text-sm text-gray-500">Total XP</p>
          </Card>
          <Card className="text-center">
            <span className="text-3xl mb-2 block">📖</span>
            <p className="text-3xl font-bold text-secondary-600">{storiesRead.length}</p>
            <p className="text-sm text-gray-500">Stories Read</p>
          </Card>
          <Card className="text-center">
            <span className="text-3xl mb-2 block">📝</span>
            <p className="text-3xl font-bold text-accent-600">{wordsLearned.length}</p>
            <p className="text-sm text-gray-500">Words Learned</p>
          </Card>
        </motion.div>

        {/* Badges Section */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Badges</h2>
          <div className="grid grid-cols-3 gap-3">
            {allBadges.map((badge) => (
              <Card
                key={badge.id}
                className={`text-center py-4 ${
                  badge.earned ? '' : 'opacity-40 grayscale'
                }`}
              >
                <span className="text-3xl block mb-2">{badge.icon}</span>
                <p className="text-xs font-semibold text-gray-900">{badge.name}</p>
                {badge.earned && (
                  <Badge variant="success" size="sm" className="mt-2">
                    Earned!
                  </Badge>
                )}
              </Card>
            ))}
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Recent Activity</h2>
          <Card>
            {gameSessions.length === 0 && storiesRead.length === 0 ? (
              <div className="text-center py-6">
                <span className="text-4xl block mb-2">📊</span>
                <p className="text-gray-500">No activity yet</p>
                <p className="text-sm text-gray-400 mt-1">
                  Start reading stories and playing games!
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
                  <span className="text-2xl">📖</span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">Story completed</p>
                    <p className="text-xs text-gray-500">Today</p>
                  </div>
                  <Badge variant="primary" size="sm">
                    +50 XP
                  </Badge>
                </div>
              </div>
            )}
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
