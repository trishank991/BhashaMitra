'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Button, Loading, SubscriptionBadge } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import api from '@/lib/api';
import type { LanguageCode, SubscriptionTier, Story } from '@/types';

export default function StoriesPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [stories, setStories] = useState<Story[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, user, activeChild } = useAuthStore();

  // Get current language from active child, default to Hindi
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code) as LanguageCode
    : 'HINDI';
  const [selectedLanguage, setSelectedLanguage] = useState<LanguageCode>(currentLanguage);

  // Get subscription tier info
  const subscriptionTier = (user?.subscription_tier as SubscriptionTier) || 'FREE';
  const storyLimit = subscriptionTier === 'PREMIUM' ? 9999 : subscriptionTier === 'STANDARD' ? 8 : 4;

  // Update selected language when activeChild changes
  useEffect(() => {
    if (currentLanguage) {
      setSelectedLanguage(currentLanguage);
    }
  }, [currentLanguage]);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    // Fetch stories from API
    const fetchStories = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getStories(selectedLanguage);

        if (response.success && response.data) {
          // Handle paginated response - results array contains the stories
          const storiesData = response.data.results || [];
          setStories(storiesData);
        } else {
          setError(response.error || 'Failed to load stories');
          setStories([]);
        }
      } catch (err) {
        console.error('[StoriesPage] Error fetching stories:', err);
        setError('Failed to load stories');
        setStories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchStories();
  }, [isHydrated, isAuthenticated, router, selectedLanguage]);

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

  // Apply story limit based on subscription tier
  const filteredStories = stories.slice(0, storyLimit);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const hasMoreStories = stories.length > storyLimit;

  return (
    <MainLayout headerTitle="Stories" showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Header with Back Button */}
        <motion.div variants={fadeInUp} className="flex items-center gap-3">
          <Link href="/home" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900">Stories</h1>
            <p className="text-gray-500">Read and learn with fun stories</p>
          </div>
          <SubscriptionBadge tier={subscriptionTier} />
        </motion.div>

        {/* Story Limit Info */}
        {subscriptionTier !== 'PREMIUM' && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-primary-50 border border-primary-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📚</span>
                  <div>
                    <p className="font-medium text-gray-900">
                      {filteredStories.length} of {storyLimit} stories available
                    </p>
                    <p className="text-sm text-gray-500">
                      {subscriptionTier === 'FREE'
                        ? 'Upgrade to Standard for 8 stories, or Premium for unlimited!'
                        : 'Upgrade to Premium for unlimited stories!'}
                    </p>
                  </div>
                </div>
                <Link href="/profile">
                  <Button variant="primary" size="sm">
                    Upgrade
                  </Button>
                </Link>
              </div>
            </Card>
          </motion.div>
        )}

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
