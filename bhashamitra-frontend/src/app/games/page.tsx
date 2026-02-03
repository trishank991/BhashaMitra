'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer } from '@/lib/constants';

const games = [
  {
    id: 'word-match',
    name: 'Word Match',
    description: 'Match words with their meanings',
    icon: '🎯',
    difficulty: 'easy',
    xpReward: 25,
    available: true,
  },
  {
    id: 'listen-speak',
    name: 'Listen & Speak',
    description: 'Practice pronunciation',
    icon: '🎤',
    difficulty: 'medium',
    xpReward: 30,
    available: true,
  },
  {
    id: 'fill-blanks',
    name: 'Fill the Blanks',
    description: 'Complete the sentences',
    icon: '✏️',
    difficulty: 'medium',
    xpReward: 30,
    available: false,
  },
  {
    id: 'picture-word',
    name: 'Picture Word',
    description: 'Match pictures to words',
    icon: '🖼️',
    difficulty: 'easy',
    xpReward: 20,
    available: false,
  },
  {
    id: 'spelling-bee',
    name: 'Spelling Bee',
    description: 'Spell words correctly',
    icon: '🐝',
    difficulty: 'hard',
    xpReward: 40,
    available: false,
  },
  {
    id: 'story-builder',
    name: 'Story Builder',
    description: 'Create your own stories',
    icon: '📝',
    difficulty: 'hard',
    xpReward: 50,
    available: false,
  },
];

export default function GamesPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated } = useAuthStore();

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

  return (
    <MainLayout headerTitle="Games" showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Intro */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-secondary-500 to-accent-500 text-white text-center py-6">
            <span className="text-5xl mb-3 block">🎮</span>
            <h2 className="text-xl font-bold">Learn While Playing!</h2>
            <p className="text-sm opacity-90 mt-1">
              Fun games to practice your language skills
            </p>
          </Card>
        </motion.div>

        {/* Available Games */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Available Now</h2>
          <div className="grid grid-cols-2 gap-3">
            {games
              .filter((g) => g.available)
              .map((game) => (
                <Link key={game.id} href={`/games/${game.id}`}>
                  <Card interactive className="text-center py-6 h-full">
                    <span className="text-4xl mb-3 block">{game.icon}</span>
                    <h3 className="font-bold text-gray-900">{game.name}</h3>
                    <p className="text-xs text-gray-500 mt-1">{game.description}</p>
                    <div className="mt-3 flex justify-center gap-2">
                      <Badge
                        variant={
                          game.difficulty === 'easy'
                            ? 'success'
                            : game.difficulty === 'medium'
                            ? 'warning'
                            : 'error'
                        }
                        size="sm"
                      >
                        {game.difficulty}
                      </Badge>
                      <Badge variant="primary" size="sm">
                        +{game.xpReward} XP
                      </Badge>
                    </div>
                  </Card>
                </Link>
              ))}
          </div>
        </motion.div>

        {/* Coming Soon */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Coming Soon</h2>
          <div className="grid grid-cols-2 gap-3">
            {games
              .filter((g) => !g.available)
              .map((game) => (
                <Card
                  key={game.id}
                  className="text-center py-6 h-full opacity-60"
                >
                  <span className="text-4xl mb-3 block">{game.icon}</span>
                  <h3 className="font-bold text-gray-900">{game.name}</h3>
                  <p className="text-xs text-gray-500 mt-1">{game.description}</p>
                  <div className="mt-3">
                    <Badge variant="neutral" size="sm">
                      Coming Soon
                    </Badge>
                  </div>
                </Card>
              ))}
          </div>
        </motion.div>

        {/* Daily Challenge */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-warning-50 border-2 border-warning-200">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-warning-100 rounded-full flex items-center justify-center">
                <span className="text-3xl">⚡</span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-warning-700">Daily Challenge</h3>
                <p className="text-sm text-warning-600">
                  Complete today&apos;s challenge for bonus XP!
                </p>
              </div>
              <Badge variant="warning">+100 XP</Badge>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
