'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Badge } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { Song, SongCategory, SONG_CATEGORY_INFO } from '@/types';

export default function SongsPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [songs, setSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<SongCategory | 'ALL'>('ALL');
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

    const fetchSongs = async () => {
      setLoading(true);
      try {
        // Get L1 songs for young children, filtered by child's language
        const childLanguage = typeof activeChild?.language === 'string'
          ? activeChild.language
          : (activeChild?.language as { code?: string })?.code || 'HINDI';
        const response = await api.getSongsByLevel('L1', childLanguage);
        if (response.success && response.data) {
          setSongs(response.data);
        } else {
          setError(response.error || 'Failed to load songs');
        }
      } catch {
        setError('Failed to load songs');
      } finally {
        setLoading(false);
      }
    };

    fetchSongs();
  }, [isHydrated, isAuthenticated, router, activeChild?.language]);

  const categories: (SongCategory | 'ALL')[] = ['ALL', 'RHYME', 'FOLK', 'EDUCATIONAL', 'FESTIVAL'];

  const filteredSongs = selectedCategory === 'ALL'
    ? songs
    : songs.filter(song => song.category === selectedCategory);

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
          <Link
            href="anguages"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Learn
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">Songs</h1>
          <p className="text-gray-500 mt-1">
            Sing along with fun Hindi songs, {activeChild?.name || 'there'}!
          </p>
        </motion.div>

        {/* Category Filters */}
        <motion.div variants={fadeInUp} className="flex gap-2 overflow-x-auto pb-2">
          {categories.map((category) => {
            const isAll = category === 'ALL';
            const categoryInfo = isAll ? null : SONG_CATEGORY_INFO[category];
            const isSelected = selectedCategory === category;

            return (
              <motion.button
                key={category}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  isSelected
                    ? 'bg-pink-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {isAll ? 'All Songs' : `${categoryInfo?.emoji} ${categoryInfo?.label}`}
              </motion.button>
            );
          })}
        </motion.div>

        {/* Song Count */}
        <motion.div variants={fadeInUp} className="text-sm text-gray-500">
          {filteredSongs.length} {filteredSongs.length === 1 ? 'song' : 'songs'}
        </motion.div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center py-16">
            <Loading size="lg" text="Loading songs..." />
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="text-center py-16">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="text-indigo-600 hover:underline"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Songs Grid */}
        {!loading && !error && (
          <motion.div variants={fadeInUp} className="grid grid-cols-1 gap-4">
            {filteredSongs.map((song, index) => {
              const categoryInfo = SONG_CATEGORY_INFO[song.category];
              const durationMinutes = Math.ceil(song.duration_seconds / 60);

              return (
                <motion.div
                  key={song.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Link href={`/languages/songs/${song.id}`}>
                    <Card interactive className="overflow-hidden" padding="none">
                      <div className="p-4">
                        {/* Header */}
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h3 className="text-lg font-bold text-gray-900 mb-1">
                              {song.title_english}
                            </h3>
                            <p className="text-2xl font-bold text-pink-600 mb-1">
                              {song.title_hindi}
                            </p>
                            <p className="text-sm text-gray-500 italic">
                              {song.title_romanized}
                            </p>
                          </div>
                          <div className="text-4xl ml-2">{categoryInfo.emoji}</div>
                        </div>

                        {/* Category Badge */}
                        <div className="flex items-center gap-2 mb-3">
                          <Badge className={`text-xs ${categoryInfo.color}`}>
                            {categoryInfo.label}
                          </Badge>
                          <span className="text-xs text-gray-500">{durationMinutes} min</span>
                        </div>

                        {/* Play Button */}
                        <motion.div
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          className="w-full py-3 bg-gradient-to-r from-pink-400 to-rose-500 text-white rounded-2xl font-bold text-sm flex items-center justify-center gap-2"
                        >
                          <span className="text-xl">▶️</span>
                          Play Song
                        </motion.div>
                      </div>
                    </Card>
                  </Link>
                </motion.div>
              );
            })}
          </motion.div>
        )}

        {/* Empty State */}
        {!loading && !error && filteredSongs.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🎵</div>
            <p className="text-gray-500">No songs found in this category</p>
          </div>
        )}
      </motion.div>
    </MainLayout>
  );
}
