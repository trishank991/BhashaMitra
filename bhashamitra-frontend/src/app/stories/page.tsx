'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import type { LanguageCode } from '@/types';

// Mock stories data
const mockStories = [
  {
    id: '1',
    title: 'The Clever Crow',
    titleNative: 'चालाक कौआ',
    description: 'A thirsty crow finds a clever way to drink water from a pot.',
    language: 'HINDI' as LanguageCode,
    difficulty: 'beginner' as const,
    duration: 5,
    thumbnail: '',
    isLocked: false,
    requiredLevel: 1,
    xpReward: 50,
  },
  {
    id: '2',
    title: 'The Lion and the Mouse',
    titleNative: 'शेर और चूहा',
    description: 'A small mouse helps a mighty lion, teaching us about kindness.',
    language: 'HINDI' as LanguageCode,
    difficulty: 'beginner' as const,
    duration: 7,
    thumbnail: '',
    isLocked: false,
    requiredLevel: 1,
    xpReward: 60,
  },
  {
    id: '3',
    title: 'The Thirsty Elephant',
    titleNative: 'प्यासा हाथी',
    description: 'An elephant learns the importance of sharing water.',
    language: 'HINDI' as LanguageCode,
    difficulty: 'intermediate' as const,
    duration: 10,
    thumbnail: '',
    isLocked: true,
    requiredLevel: 3,
    xpReward: 80,
  },
];

export default function StoriesPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated } = useAuthStore();
  const [selectedLanguage, setSelectedLanguage] = useState<LanguageCode>('HINDI');

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

  const filteredStories = mockStories.filter(
    (story) => story.language === selectedLanguage
  );

  return (
    <MainLayout headerTitle="Stories" showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Language Filter */}
        <motion.div variants={fadeInUp} className="flex gap-2 overflow-x-auto pb-2 -mx-4 px-4">
          {Object.values(SUPPORTED_LANGUAGES).slice(0, 6).map((lang) => (
            <button
              key={lang.code}
              onClick={() => setSelectedLanguage(lang.code)}
              className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedLanguage === lang.code
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {lang.flag} {lang.name}
            </button>
          ))}
        </motion.div>

        {/* Stories Grid */}
        <motion.div variants={fadeInUp} className="space-y-4">
          <h2 className="text-lg font-bold text-gray-900">
            {SUPPORTED_LANGUAGES[selectedLanguage].name} Stories
          </h2>

          {filteredStories.length === 0 ? (
            <Card className="text-center py-8">
              <p className="text-4xl mb-4">📚</p>
              <p className="text-gray-500">No stories available yet for this language.</p>
              <p className="text-sm text-gray-400 mt-2">Check back soon!</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {filteredStories.map((story) => (
                <Link
                  key={story.id}
                  href={story.isLocked ? '#' : `/stories/${story.id}`}
                  className={story.isLocked ? 'cursor-not-allowed' : ''}
                >
                  <Card
                    interactive={!story.isLocked}
                    className={`flex items-center gap-4 ${
                      story.isLocked ? 'opacity-60' : ''
                    }`}
                  >
                    {/* Thumbnail */}
                    <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-xl flex items-center justify-center">
                      {story.isLocked ? (
                        <span className="text-2xl">🔒</span>
                      ) : (
                        <span className="text-2xl">📖</span>
                      )}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-bold text-gray-900 truncate">
                          {story.title}
                        </h3>
                        <Badge
                          variant={
                            story.difficulty === 'beginner'
                              ? 'success'
                              : story.difficulty === 'intermediate'
                              ? 'warning'
                              : 'error'
                          }
                          size="sm"
                        >
                          {story.difficulty}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600">{story.titleNative}</p>
                      <div className="flex items-center gap-3 mt-1">
                        <span className="text-xs text-gray-400">
                          {story.duration} min
                        </span>
                        <span className="text-xs text-primary-500 font-medium">
                          +{story.xpReward} XP
                        </span>
                      </div>
                    </div>

                    {/* Arrow */}
                    {!story.isLocked && (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={2}
                        stroke="currentColor"
                        className="w-5 h-5 text-gray-400"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="m8.25 4.5 7.5 7.5-7.5 7.5"
                        />
                      </svg>
                    )}
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </motion.div>

        {/* Coming Soon */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-accent-50 border-2 border-accent-200 text-center py-6">
            <span className="text-4xl">✨</span>
            <h3 className="font-bold text-accent-700 mt-2">More Stories Coming Soon!</h3>
            <p className="text-sm text-accent-600 mt-1">
              We&apos;re adding new stories every week
            </p>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
