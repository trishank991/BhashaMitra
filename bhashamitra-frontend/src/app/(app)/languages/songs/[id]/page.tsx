'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button, Badge } from '@/components/ui';
import { PeppiSongNarrator } from '@/components/peppi';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { Song, SONG_CATEGORY_INFO, SubscriptionTier, PeppiGender } from '@/types';

export default function SongDetailPage() {
  const router = useRouter();
  const params = useParams();
  const songId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [song, setSong] = useState<Song | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showLyrics, setShowLyrics] = useState(true);
  const [showPeppiNarrator, setShowPeppiNarrator] = useState(false);
  const { isAuthenticated, activeChild, user } = useAuthStore();

  // Get subscription tier
  const subscriptionTier = (user?.subscription_tier as SubscriptionTier) || 'FREE';

  // Get child's Peppi preferences
  const peppiGender = activeChild?.peppi_gender || 'female';

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    if (!songId) {
      setError('Invalid song ID');
      setLoading(false);
      return;
    }

    const fetchSong = async () => {
      setLoading(true);
      try {
        const response = await api.getSong(songId);
        if (response.success && response.data) {
          setSong(response.data);
        } else {
          setError(response.error || 'Failed to load song');
        }
      } catch {
        setError('Failed to load song');
      } finally {
        setLoading(false);
      }
    };

    fetchSong();
  }, [isHydrated, isAuthenticated, songId, router]);

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
          <Loading size="lg" text="Loading song..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !song) {
    return (
      <MainLayout>
        <div className="text-center py-16">
          <p className="text-red-500 mb-4">{error || 'Song not found'}</p>
          <Link href="/languages/songs" className="text-indigo-600 hover:underline">
            Back to Songs
          </Link>
        </div>
      </MainLayout>
    );
  }

  const categoryInfo = SONG_CATEGORY_INFO[song.category];
  const durationMinutes = Math.ceil(song.duration_seconds / 60);

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
            href="/languages/songs"
            className="inline-flex items-center text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Songs
          </Link>
        </motion.div>

        {/* Song Header */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-br from-pink-400 to-rose-500 text-white overflow-hidden">
            <div className="text-center py-4">
              <div className="text-5xl mb-4">{categoryInfo.emoji}</div>
              <h1 className="text-2xl font-bold mb-2">{song.title_english}</h1>
              <p className="text-3xl font-bold mb-2">{song.title_hindi}</p>
              <p className="text-lg opacity-90 italic">{song.title_romanized}</p>
              <div className="flex items-center justify-center gap-3 mt-4">
                <Badge className="bg-white/20 text-white">
                  {categoryInfo.label}
                </Badge>
                <span className="text-sm opacity-80">{durationMinutes} min</span>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Play Button */}
        <motion.div variants={fadeInUp}>
          <Card>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-full py-6 bg-gradient-to-r from-pink-400 to-rose-500 text-white rounded-3xl font-bold text-xl flex items-center justify-center gap-3"
            >
              <span className="text-4xl">{isPlaying ? '⏸️' : '▶️'}</span>
              {isPlaying ? 'Pause' : 'Play Song'}
            </motion.button>
            {!song.audio_url && (
              <p className="text-center text-gray-500 text-sm mt-3">
                Audio coming soon! Read along with the lyrics below.
              </p>
            )}
          </Card>
        </motion.div>

        {/* Peppi Narrator Section - Listen with Peppi (Above Lyrics/Actions) */}
        <motion.div variants={fadeInUp}>
          {showPeppiNarrator && songId ? (
            <PeppiSongNarrator
              songId={songId}
              songTitle={song?.title_english}
              language="HINDI"
              defaultGender={peppiGender as PeppiGender}
              subscriptionTier={subscriptionTier}
              onComplete={() => {
                // Song narration completed
              }}
            />
          ) : (
            <button
              onClick={() => setShowPeppiNarrator(true)}
              className="w-full py-4 px-6 bg-gradient-to-r from-pink-400 to-rose-400 hover:from-pink-500 hover:to-rose-500 text-white rounded-2xl font-semibold transition-all shadow-lg flex items-center justify-center gap-3"
            >
              <span className="text-2xl">🐱</span>
              <span>Listen with Peppi</span>
              <span className="text-xs opacity-75">(Full Song)</span>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
              </svg>
            </button>
          )}
        </motion.div>

        {/* Lyrics Toggle */}
        <motion.div variants={fadeInUp} className="flex gap-2">
          <Button
            variant={showLyrics ? 'primary' : 'outline'}
            onClick={() => setShowLyrics(true)}
            className="flex-1"
          >
            Show Lyrics
          </Button>
          <Button
            variant={!showLyrics ? 'primary' : 'outline'}
            onClick={() => setShowLyrics(false)}
            className="flex-1"
          >
            Show Actions
          </Button>
        </motion.div>

        {/* Lyrics or Actions */}
        <AnimatePresence mode="wait">
          {showLyrics ? (
            <motion.div
              key="lyrics"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Card>
                <h3 className="text-lg font-bold text-gray-900 mb-4">Lyrics</h3>

                {/* Hindi Lyrics */}
                <div className="mb-4 p-4 bg-pink-50 rounded-2xl">
                  <p className="text-sm text-gray-500 mb-2">Hindi</p>
                  <p className="text-2xl text-pink-900 leading-relaxed whitespace-pre-line">
                    {song.lyrics_hindi}
                  </p>
                </div>

                {/* Romanized Lyrics */}
                <div className="mb-4 p-4 bg-purple-50 rounded-2xl">
                  <p className="text-sm text-gray-500 mb-2">Romanized</p>
                  <p className="text-lg text-purple-900 leading-relaxed whitespace-pre-line italic">
                    {song.lyrics_romanized}
                  </p>
                </div>

                {/* English Translation */}
                <div className="p-4 bg-blue-50 rounded-2xl">
                  <p className="text-sm text-gray-500 mb-2">English</p>
                  <p className="text-base text-blue-900 leading-relaxed whitespace-pre-line">
                    {song.lyrics_english}
                  </p>
                </div>
              </Card>
            </motion.div>
          ) : (
            <motion.div
              key="actions"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Card>
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Actions & Movements
                </h3>
                <div className="space-y-3">
                  {song.actions && song.actions.length > 0 ? (
                    song.actions.map((action, index) => (
                      <div
                        key={index}
                        className="flex items-center gap-3 p-3 bg-yellow-50 rounded-2xl"
                      >
                        <div className="w-10 h-10 bg-yellow-200 rounded-full flex items-center justify-center font-bold text-yellow-700">
                          {index + 1}
                        </div>
                        <p className="text-base text-gray-900">{action}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-center py-4">
                      No actions for this song. Just sing along!
                    </p>
                  )}
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Peppi Encouragement */}
        <motion.div variants={fadeInUp}>
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 flex items-start gap-3">
            <span className="text-2xl">🐱</span>
            <div>
              <p className="font-medium text-amber-900">
                Great job learning this song, {activeChild?.name || 'there'}!
                Singing is a wonderful way to learn Hindi!
              </p>
              <p className="text-xs text-amber-700 mt-1">- Peppi</p>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
