'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading, Button, SpeakerButton } from '@/components/ui';
import { PeppiNarrator } from '@/components/peppi';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { useAudio } from '@/hooks/useAudio';
import api from '@/lib/api';
import type { SubscriptionTier, LanguageCode, Story } from '@/types';

export default function StoryDetailPage() {
  const router = useRouter();
  const params = useParams();
  const storyId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);
  const [showTranslation, setShowTranslation] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showPeppiNarrator, setShowPeppiNarrator] = useState(false);
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, user, activeChild } = useAuthStore();

  // Audio playback hook - use story language if available
  const { isPlaying, isLoading: audioLoading, playAudio, stopAudio } = useAudio({
    language: story?.language || 'HINDI',
    voiceStyle: 'kid_friendly',
  });

  // Handle playing page text
  const handlePlayPageText = () => {
    if (!story || !story.pages || !story.pages[currentPage]) return;
    const pageText = story.pages[currentPage].text;

    if (isPlaying) {
      stopAudio();
    } else {
      playAudio(pageText);
    }
  };

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  // Fetch story from API
  useEffect(() => {
    if (!isHydrated || !isAuthenticated || !storyId) return;

    const fetchStory = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.getStory(storyId);

        if (response.success && response.data) {
          setStory(response.data);
        } else {
          setError(response.error || 'Failed to load story');
        }
      } catch (err) {
        console.error('[StoryDetailPage] Error:', err);
        setError('Failed to load story');
      } finally {
        setLoading(false);
      }
    };

    fetchStory();
  }, [isHydrated, isAuthenticated, storyId]);

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

  if (loading) {
    return (
      <MainLayout headerTitle="Loading Story...">
        <div className="flex flex-col items-center justify-center py-12">
          <Loading size="lg" text="Loading story..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !story) {
    return (
      <MainLayout headerTitle="Story Not Found">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-6xl mb-4">📚</span>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Story Not Found</h1>
          <p className="text-gray-500 mb-6">{error || "This story doesn't exist or has been removed."}</p>
          <Link href="/stories">
            <Button>Back to Stories</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }

  // Get current page data from the story
  const currentStoryPage = story.pages && story.pages.length > 0 ? story.pages[currentPage] : null;
  const isLastPage = story.pages ? currentPage === story.pages.length - 1 : true;
  const isFirstPage = currentPage === 0;

  // Get subscription tier
  const subscriptionTier = (user?.subscription_tier as SubscriptionTier) || 'FREE';

  // Get child's Peppi preferences (default values if not set)
  const peppiGender = activeChild?.peppi_gender || 'female';
  const storyLanguage = (story?.language || 'HINDI') as LanguageCode;

  const handleNext = () => {
    stopAudio(); // Stop audio when changing pages
    setShowPeppiNarrator(false); // Hide Peppi narrator when changing pages
    if (isLastPage) {
      setIsCompleted(true);
    } else {
      setCurrentPage((prev) => prev + 1);
      setShowTranslation(false);
    }
  };

  const handlePrevious = () => {
    stopAudio(); // Stop audio when changing pages
    setShowPeppiNarrator(false); // Hide Peppi narrator when changing pages
    if (!isFirstPage) {
      setCurrentPage((prev) => prev - 1);
      setShowTranslation(false);
    }
  };

  const handleComplete = () => {
    router.push('/stories');
  };

  if (isCompleted) {
    return (
      <MainLayout headerTitle="Story Complete!">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-center justify-center py-12"
        >
          <div className="text-8xl mb-6">🎉</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Great Job!</h1>
          <p className="text-gray-500 mb-2">You finished &quot;{story.title}&quot;</p>
          <p className="text-lg font-medium text-primary-600 mb-8">+{story.xpReward} XP earned!</p>

          <Card className="w-full max-w-sm bg-gradient-to-br from-primary-50 to-secondary-50 mb-6">
            <div className="text-center">
              <h3 className="font-bold text-gray-900 mb-2">Story Summary</h3>
              <p className="text-sm text-gray-600">{story.description}</p>
            </div>
          </Card>

          <div className="flex gap-3">
            <Button variant="outline" onClick={() => { setIsCompleted(false); setCurrentPage(0); }}>
              Read Again
            </Button>
            <Button onClick={handleComplete}>
              Back to Stories
            </Button>
          </div>
        </motion.div>
      </MainLayout>
    );
  }

  return (
    <MainLayout headerTitle={story.title} showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Story Header */}
        <motion.div variants={fadeInUp} className="flex items-center justify-between">
          <Link href="/stories" className="flex items-center gap-2 text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>Back</span>
          </Link>
          <Badge variant={story.difficulty === 'beginner' ? 'success' : 'warning'}>
            {story.difficulty}
          </Badge>
        </motion.div>

        {/* Progress Bar */}
        <motion.div variants={fadeInUp} className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentPage + 1) / story.pages.length) * 100}%` }}
          />
        </motion.div>
        <p className="text-xs text-gray-400 text-center">
          Page {currentPage + 1} of {story.pages.length}
        </p>

        {/* Peppi Narrator Section - Listen to Full Story (Moved to TOP) */}
        <motion.div variants={fadeInUp}>
          {showPeppiNarrator && storyId ? (
            <PeppiNarrator
              storyId={storyId}
              storyTitle={story?.title}
              language={storyLanguage}
              defaultGender={peppiGender}
              subscriptionTier={subscriptionTier}
              onComplete={() => {
                // Story narration completed
                setIsCompleted(true);
              }}
            />
          ) : (
            <button
              onClick={() => setShowPeppiNarrator(true)}
              className="w-full py-4 px-6 bg-gradient-to-r from-purple-400 to-pink-400 hover:from-purple-500 hover:to-pink-500 text-white rounded-2xl font-semibold transition-all shadow-lg flex items-center justify-center gap-3"
            >
              <span className="text-2xl">🐱</span>
              <span>Listen with Peppi</span>
              <span className="text-xs opacity-75">(Full Story)</span>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
              </svg>
            </button>
          )}
        </motion.div>

        {/* Story Content Card */}
        <motion.div variants={fadeInUp}>
          <Card className="min-h-[300px] flex flex-col">
            {/* Image Placeholder */}
            <div className="w-full h-48 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-xl mb-6 flex items-center justify-center">
              <span className="text-6xl">
                {currentPage === 0 ? '📖' : currentPage === story.pages.length - 1 ? '🌟' : '📜'}
              </span>
            </div>

            {/* Hindi Text with Audio */}
            <div className="flex-1">
              {currentStoryPage ? (
                <>
                  <div className="mb-4">
                    <p className="text-2xl font-bold text-gray-900 leading-relaxed text-center mb-3">
                      {currentStoryPage.text}
                    </p>
                    {/* Listen Button */}
                    <div className="flex justify-center">
                      <button
                        onClick={handlePlayPageText}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-400 to-pink-500 text-white rounded-full font-medium hover:from-purple-500 hover:to-pink-600 transition-colors shadow-md"
                      >
                        <SpeakerButton
                          isPlaying={isPlaying}
                          isLoading={audioLoading}
                          onClick={() => {}}
                          size="sm"
                          className="!bg-transparent !shadow-none hover:!bg-white/20"
                        />
                        <span className="text-sm">
                          {audioLoading ? 'Loading...' : isPlaying ? 'Stop' : 'Listen'}
                        </span>
                      </button>
                    </div>
                  </div>

                  {/* Translation Toggle */}
                  <button
                    onClick={() => setShowTranslation(!showTranslation)}
                    className="w-full text-center text-sm text-primary-600 hover:text-primary-700 mb-2"
                  >
                    {showTranslation ? 'Hide translation' : 'Show translation'}
                  </button>

                  {/* English Translation */}
                  {showTranslation && currentStoryPage.translation && (
                    <motion.p
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-lg text-gray-500 text-center italic"
                    >
                      {currentStoryPage.translation}
                    </motion.p>
                  )}
                </>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-500">No content available for this page</p>
                </div>
              )}
            </div>
          </Card>
        </motion.div>

        {/* Navigation Buttons */}
        <motion.div variants={fadeInUp} className="flex gap-3">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={isFirstPage}
            className="flex-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </Button>
          <Button onClick={handleNext} className="flex-1">
            {isLastPage ? 'Finish' : 'Next'}
            {!isLastPage && (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </Button>
        </motion.div>

        {/* XP Reward Info */}
        <motion.div variants={fadeInUp} className="text-center">
          <p className="text-sm text-gray-400">
            Complete this story to earn <span className="text-primary-600 font-medium">+{story.xpReward} XP</span>
          </p>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
