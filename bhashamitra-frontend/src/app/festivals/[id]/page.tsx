'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { MainLayout } from '@/components/layout';
import { Card, Button, Loading } from '@/components/ui';
import { PeppiAvatar } from '@/components/peppi';
import { useAuthStore, usePeppiStore } from '@/stores';
import { fadeInUp } from '@/lib/constants';
import api from '@/lib/api';
import type { Festival, Story } from '@/types';

// Backend returns story pages with this structure
interface BackendStoryPage {
  id?: string;
  page_number?: number;
  text_content?: string;
  text?: string;
  image_url?: string;
}

interface LocalStoryPage {
  id: string;
  page_number: number;
  text_content: string;
  image_url?: string;
}

export default function FestivalStoryPage() {
  const router = useRouter();
  const params = useParams();
  const festivalId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [festival, setFestival] = useState<Festival | null>(null);
  const [stories, setStories] = useState<Story[]>([]);
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);
  const [storyPages, setStoryPages] = useState<LocalStoryPage[]>([]);
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isNarrating, setIsNarrating] = useState(false);
  const [audioPlaying, setAudioPlaying] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();
  const { speakWithAnimation, stopNarration } = usePeppiStore();

  // Get child's Peppi preferences
  const peppiGender = activeChild?.peppi_gender || 'female';
  const childLanguage = typeof activeChild?.language === 'string'
    ? activeChild.language
    : activeChild?.language?.code || 'HINDI';

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchFestivalData = async () => {
      if (!festivalId) {
        setError('Invalid festival ID');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        // Fetch festival details
        const festivalResponse = await api.getFestival(festivalId);
        if (festivalResponse.success && festivalResponse.data) {
          setFestival(festivalResponse.data);
        } else {
          setError(festivalResponse.error || 'Failed to load festival');
          return;
        }

        // Fetch festival stories
        const storiesResponse = await api.getFestivalStories(festivalId);
        if (storiesResponse.success && storiesResponse.data) {
          setStories(storiesResponse.data);
          // Auto-select the first story if available
          if (storiesResponse.data.length > 0) {
            const firstStory = storiesResponse.data[0];
            setSelectedStory(firstStory);
            // Fetch story pages from the story detail
            await fetchStoryPages(firstStory.id);
          }
        }
      } catch (err) {
        console.error('[FestivalStoryPage] Error:', err);
        setError('Failed to load festival data');
      } finally {
        setLoading(false);
      }
    };

    fetchFestivalData();
  }, [isHydrated, isAuthenticated, router, festivalId]);

  const fetchStoryPages = async (storyId: string) => {
    try {
      const response = await api.getStory(storyId);
      if (response.success && response.data) {
        // Transform pages to our format
        const pages = response.data.pages?.map((p: BackendStoryPage, index: number) => ({
          id: p.id || `page-${index}`,
          page_number: p.page_number || index + 1,
          text_content: p.text_content || (p as unknown as { text?: string }).text || '',
          image_url: p.image_url,
        })) || [];
        setStoryPages(pages);
        setCurrentPageIndex(0);
      }
    } catch (err) {
      console.error('[FestivalStoryPage] Error fetching story pages:', err);
    }
  };

  // Peppi greeting when story loads
  useEffect(() => {
    if (isHydrated && !loading && selectedStory && storyPages.length > 0) {
      const greeting = peppiGender === 'male'
        ? `Let me tell you the story of ${festival?.name}!`
        : `Let me tell you the story of ${festival?.name}!`;
      speakWithAnimation(greeting, 'greeting');
    }
  }, [isHydrated, loading, selectedStory, storyPages.length, festival?.name, peppiGender, speakWithAnimation]);

  // Stop audio on unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
      stopNarration();
    };
  }, [stopNarration]);

  const currentPage = storyPages[currentPageIndex];
  const totalPages = storyPages.length;
  const isFirstPage = currentPageIndex === 0;
  const isLastPage = currentPageIndex === totalPages - 1;

  const handlePreviousPage = useCallback(() => {
    if (!isFirstPage) {
      stopAudio();
      setCurrentPageIndex((prev) => prev - 1);
    }
  }, [isFirstPage]);

  const handleNextPage = useCallback(() => {
    if (!isLastPage) {
      stopAudio();
      setCurrentPageIndex((prev) => prev + 1);
    }
  }, [isLastPage]);

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setAudioPlaying(false);
    setIsNarrating(false);
  };

  const handleNarrate = async () => {
    if (!currentPage) return;

    if (audioPlaying) {
      stopAudio();
      return;
    }

    setIsNarrating(true);
    setAudioPlaying(true);

    try {
      // Use the TTS API to generate narration
      const result = await api.getAudio(
        currentPage.text_content,
        childLanguage,
        'kid_friendly'
      );

      if (result.success && result.audioUrl) {
        // Create and play audio
        const audio = new Audio(result.audioUrl);
        audioRef.current = audio;

        audio.onended = () => {
          setAudioPlaying(false);
          setIsNarrating(false);
          // Auto-advance to next page after narration
          if (!isLastPage) {
            setTimeout(() => handleNextPage(), 1000);
          }
        };

        audio.onerror = () => {
          setAudioPlaying(false);
          setIsNarrating(false);
          console.error('[FestivalStoryPage] Audio playback error');
        };

        await audio.play();
      } else {
        console.error('[FestivalStoryPage] Failed to get audio:', result.error);
        setAudioPlaying(false);
        setIsNarrating(false);
      }
    } catch (err) {
      console.error('[FestivalStoryPage] Narration error:', err);
      setAudioPlaying(false);
      setIsNarrating(false);
    }
  };

  const handleNarrateAll = async () => {
    if (audioPlaying) {
      stopAudio();
      return;
    }
    // Start from current page and narrate
    handleNarrate();
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
      <MainLayout headerTitle="Festival Story" showProgress={false}>
        <div className="flex justify-center py-12">
          <Loading size="lg" text="Loading story..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !festival) {
    return (
      <MainLayout headerTitle="Festival Story" showProgress={false}>
        <Card className="bg-red-50 border border-red-200 text-center py-8">
          <p className="text-4xl mb-4">😿</p>
          <p className="text-red-600">{error || 'Festival not found'}</p>
          <Link href="/festivals">
            <Button variant="primary" className="mt-4">
              Back to Festivals
            </Button>
          </Link>
        </Card>
      </MainLayout>
    );
  }

  return (
    <MainLayout headerTitle={festival.name} showProgress={false} showPeppi={false}>
      <motion.div
        initial="initial"
        animate="animate"
        className="space-y-4"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="flex items-center gap-3">
          <Link href="/festivals" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div className="flex-1">
            <h1 className="text-xl font-bold text-gray-900">{festival.name}</h1>
            <p className="text-sm text-primary-600">{festival.name_native}</p>
          </div>
        </motion.div>

        {/* No stories message */}
        {stories.length === 0 && (
          <Card className="text-center py-8">
            <p className="text-4xl mb-4">📚</p>
            <p className="text-gray-500">No stories available for this festival yet.</p>
            <Link href="/festivals">
              <Button variant="secondary" className="mt-4">
                Browse Other Festivals
              </Button>
            </Link>
          </Card>
        )}

        {/* Story Reader */}
        {selectedStory && storyPages.length > 0 && currentPage && (
          <div className="space-y-4">
            {/* Story Title */}
            <motion.div variants={fadeInUp}>
              <Card className="bg-gradient-to-r from-warning-50 to-warning-100 border-warning-200">
                <h2 className="text-lg font-bold text-gray-900">{selectedStory.title}</h2>
                {selectedStory.titleNative && (
                  <p className="text-sm text-warning-700">{selectedStory.titleNative}</p>
                )}
              </Card>
            </motion.div>

            {/* Peppi Narrator */}
            <motion.div variants={fadeInUp} className="flex items-center gap-4">
              <div className="relative">
                <PeppiAvatar
                  size="md"
                  showBubble={false}
                />
                {isNarrating && (
                  <motion.div
                    className="absolute -top-1 -right-1 w-4 h-4 bg-primary-500 rounded-full"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.5, repeat: Infinity }}
                  />
                )}
              </div>
              <div className="flex-1">
                <p className="text-sm text-gray-600">
                  {isNarrating
                    ? 'Peppi is reading...'
                    : 'Tap the play button to hear Peppi read the story!'}
                </p>
              </div>
              <Button
                variant={audioPlaying ? 'secondary' : 'primary'}
                size="sm"
                onClick={handleNarrateAll}
                className="flex items-center gap-2"
              >
                {audioPlaying ? (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Stop
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                    Read
                  </>
                )}
              </Button>
            </motion.div>

            {/* Story Content */}
            <AnimatePresence mode="wait">
              <motion.div
                key={currentPageIndex}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="min-h-[300px] flex flex-col">
                  {/* Page indicator */}
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-gray-400">
                      Page {currentPageIndex + 1} of {totalPages}
                    </span>
                    <div className="flex gap-1">
                      {storyPages.map((_, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            stopAudio();
                            setCurrentPageIndex(idx);
                          }}
                          className={`w-2 h-2 rounded-full transition-colors ${
                            idx === currentPageIndex
                              ? 'bg-primary-500'
                              : idx < currentPageIndex
                              ? 'bg-primary-200'
                              : 'bg-gray-200'
                          }`}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Page image (if available) */}
                  {currentPage.image_url && (
                    <div className="mb-4 rounded-lg overflow-hidden">
                      <img
                        src={currentPage.image_url}
                        alt={`Page ${currentPageIndex + 1}`}
                        className="w-full h-48 object-cover"
                      />
                    </div>
                  )}

                  {/* Story text */}
                  <div className="flex-1 flex items-center justify-center">
                    <p className="text-xl leading-relaxed text-gray-800 text-center px-4">
                      {currentPage.text_content}
                    </p>
                  </div>
                </Card>
              </motion.div>
            </AnimatePresence>

            {/* Navigation Controls */}
            <div className="flex items-center justify-between">
              <Button
                variant="secondary"
                onClick={handlePreviousPage}
                disabled={isFirstPage}
                className="flex items-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Previous
              </Button>

              <Button
                variant="primary"
                onClick={handleNextPage}
                disabled={isLastPage}
                className="flex items-center gap-2"
              >
                {isLastPage ? 'The End!' : 'Next'}
                {!isLastPage && (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </Button>
            </div>

            {/* End of story celebration */}
            {isLastPage && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <Card className="bg-gradient-to-r from-primary-50 to-secondary-50 border-2 border-primary-200">
                  <div className="space-y-3">
                    <span className="text-5xl">🎉</span>
                    <h3 className="text-xl font-bold text-gray-900">Great job!</h3>
                    <p className="text-gray-600">
                      You finished the {festival.name} story!
                    </p>
                    <div className="flex gap-3 justify-center pt-2">
                      <Button
                        variant="secondary"
                        onClick={() => {
                          setCurrentPageIndex(0);
                          stopAudio();
                        }}
                      >
                        Read Again
                      </Button>
                      <Link href="/festivals">
                        <Button variant="primary">
                          More Stories
                        </Button>
                      </Link>
                    </div>
                  </div>
                </Card>
              </motion.div>
            )}
          </div>
        )}
      </motion.div>
    </MainLayout>
  );
}
