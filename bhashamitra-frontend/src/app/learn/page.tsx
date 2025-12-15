'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';

const CURRICULUM_MODULES = [
  {
    id: 'alphabet',
    title: 'Alphabet',
    titleNative: 'वर्णमाला',
    description: 'Learn letters, sounds, and writing',
    icon: 'अ',
    color: 'from-orange-400 to-red-500',
    href: '/learn/alphabet',
  },
  {
    id: 'vocabulary',
    title: 'Vocabulary',
    titleNative: 'शब्दावली',
    description: 'Build your word bank with flashcards',
    icon: '📚',
    color: 'from-blue-400 to-purple-500',
    href: '/learn/vocabulary',
  },
  {
    id: 'grammar',
    title: 'Grammar',
    titleNative: 'व्याकरण',
    description: 'Learn sentence structure and rules',
    icon: '📝',
    color: 'from-green-400 to-teal-500',
    href: '/learn/grammar',
  },
  {
    id: 'stories',
    title: 'Stories',
    titleNative: 'कहानियाँ',
    description: 'Read fun stories in your language',
    icon: '📖',
    color: 'from-pink-400 to-rose-500',
    href: '/stories',
  },
];

export default function LearnPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated, activeChild } = useAuthStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

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
          <h1 className="text-2xl font-bold text-gray-900">Learn</h1>
          <p className="text-gray-500 mt-1">
            Choose what you want to learn today, {activeChild?.name || 'there'}!
          </p>
        </motion.div>

        {/* Quick Stats */}
        <motion.div variants={fadeInUp} className="grid grid-cols-3 gap-3">
          <Card padding="sm" className="text-center bg-gradient-to-br from-orange-50 to-orange-100">
            <div className="text-2xl mb-1">📝</div>
            <p className="text-xl font-bold text-orange-600">49</p>
            <p className="text-xs text-gray-500">Letters</p>
          </Card>
          <Card padding="sm" className="text-center bg-gradient-to-br from-blue-50 to-blue-100">
            <div className="text-2xl mb-1">📚</div>
            <p className="text-xl font-bold text-blue-600">80</p>
            <p className="text-xs text-gray-500">Words</p>
          </Card>
          <Card padding="sm" className="text-center bg-gradient-to-br from-green-50 to-green-100">
            <div className="text-2xl mb-1">📖</div>
            <p className="text-xl font-bold text-green-600">5</p>
            <p className="text-xs text-gray-500">Grammar</p>
          </Card>
        </motion.div>

        {/* Curriculum Modules */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Study Materials</h2>
          <div className="grid grid-cols-2 gap-4">
            {CURRICULUM_MODULES.map((module) => (
              <Link key={module.id} href={module.href}>
                <Card
                  interactive
                  className={`h-full bg-gradient-to-br ${module.color} text-white overflow-hidden`}
                >
                  <div className="p-4">
                    <div className="text-4xl mb-3">{module.icon}</div>
                    <h3 className="font-bold text-lg">{module.title}</h3>
                    <p className="text-sm opacity-90">{module.titleNative}</p>
                    <p className="text-xs mt-2 opacity-80">{module.description}</p>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </motion.div>

        {/* Daily Challenge */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center">
                <span className="text-3xl">🎯</span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-lg">Daily Challenge</h3>
                <p className="text-sm opacity-90">
                  Learn 5 new words and practice 10 flashcards
                </p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold">0/15</p>
                <p className="text-xs opacity-80">Complete</p>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Recent Activity */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Continue Learning</h2>
          <Card className="bg-gray-50">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">अ</span>
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">Hindi Alphabet</h3>
                <p className="text-sm text-gray-500">Continue from where you left off</p>
              </div>
              <Link href="/learn/alphabet">
                <button className="px-4 py-2 bg-orange-500 text-white rounded-xl text-sm font-medium hover:bg-orange-600 transition-colors">
                  Continue
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
