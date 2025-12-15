'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading } from '@/components/ui';
import { useAuthStore, usePeppiStore } from '@/stores';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import type { Festival } from '@/types';

// Religion filter options with icons
const RELIGION_FILTERS = [
  { value: '', label: 'All Festivals', icon: '🎉' },
  { value: 'HINDU', label: 'Hindu', icon: '🕉️' },
  { value: 'MUSLIM', label: 'Muslim', icon: '☪️' },
  { value: 'SIKH', label: 'Sikh', icon: '🙏' },
  { value: 'CHRISTIAN', label: 'Christian', icon: '✝️' },
  { value: 'JAIN', label: 'Jain', icon: '☸️' },
  { value: 'BUDDHIST', label: 'Buddhist', icon: '☸️' },
];

// Month names for display
const MONTH_NAMES = [
  '', 'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

export default function FestivalsPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedReligion, setSelectedReligion] = useState('');
  const { isAuthenticated } = useAuthStore();
  const { speakWithAnimation } = usePeppiStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchFestivals = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getFestivals(selectedReligion || undefined);
        if (response.success && response.data) {
          setFestivals(response.data);
        } else {
          setError(response.error || 'Failed to load festivals');
          setFestivals([]);
        }
      } catch (err) {
        console.error('[FestivalsPage] Error fetching festivals:', err);
        setError('Failed to load festivals');
        setFestivals([]);
      } finally {
        setLoading(false);
      }
    };

    fetchFestivals();
  }, [isHydrated, isAuthenticated, router, selectedReligion]);

  // Peppi greeting on page load
  useEffect(() => {
    if (isHydrated && isAuthenticated && !loading && festivals.length > 0) {
      speakWithAnimation('Choose a festival to hear its story!', 'greeting');
    }
  }, [isHydrated, isAuthenticated, loading, festivals.length, speakWithAnimation]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  return (
    <MainLayout headerTitle="Festival Stories" showProgress={false}>
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
            <h1 className="text-2xl font-bold text-gray-900">Festival Stories</h1>
            <p className="text-gray-500">Learn about Indian festivals through stories</p>
          </div>
        </motion.div>

        {/* Peppi Introduction Card */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-primary-50 to-secondary-50 border-2 border-primary-200">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-md">
                <span className="text-3xl">🐱</span>
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Story Time with Peppi!</h3>
                <p className="text-sm text-gray-600">
                  Pick a festival and I will tell you its story!
                </p>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Religion Filter */}
        <motion.div variants={fadeInUp} className="flex gap-2 overflow-x-auto pb-2 -mx-4 px-4">
          {RELIGION_FILTERS.map((filter) => (
            <button
              key={filter.value}
              onClick={() => setSelectedReligion(filter.value)}
              className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors flex items-center gap-2 ${
                selectedReligion === filter.value
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <span>{filter.icon}</span>
              <span>{filter.label}</span>
            </button>
          ))}
        </motion.div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center py-12">
            <Loading size="lg" text="Loading festivals..." />
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="bg-red-50 border border-red-200 text-center py-8">
            <p className="text-4xl mb-4">😿</p>
            <p className="text-red-600">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              Try Again
            </button>
          </Card>
        )}

        {/* Festivals Grid */}
        {!loading && !error && (
          <motion.div variants={fadeInUp} className="space-y-4">
            {festivals.length === 0 ? (
              <Card className="text-center py-8">
                <p className="text-4xl mb-4">📚</p>
                <p className="text-gray-500">No festivals found.</p>
                <p className="text-sm text-gray-400 mt-2">
                  {selectedReligion ? 'Try selecting a different filter.' : 'Check back soon!'}
                </p>
              </Card>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {festivals.map((festival) => (
                  <Link key={festival.id} href={`/festivals/${festival.id}`}>
                    <Card
                      interactive
                      className="h-full hover:shadow-lg transition-shadow"
                    >
                      <div className="flex items-start gap-4">
                        {/* Festival Icon */}
                        <div className="w-14 h-14 bg-gradient-to-br from-warning-100 to-warning-200 rounded-xl flex items-center justify-center flex-shrink-0">
                          <span className="text-2xl">
                            {festival.religion === 'HINDU' && '🪔'}
                            {festival.religion === 'MUSLIM' && '🌙'}
                            {festival.religion === 'SIKH' && '🙏'}
                            {festival.religion === 'CHRISTIAN' && '⭐'}
                            {festival.religion === 'JAIN' && '🪷'}
                            {festival.religion === 'BUDDHIST' && '🪷'}
                          </span>
                        </div>

                        {/* Festival Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="font-bold text-gray-900 truncate">
                              {festival.name}
                            </h3>
                            <Badge variant="secondary" size="sm">
                              {festival.religion.charAt(0) + festival.religion.slice(1).toLowerCase()}
                            </Badge>
                          </div>
                          <p className="text-sm text-primary-600 font-medium mb-1">
                            {festival.name_native}
                          </p>
                          <p className="text-xs text-gray-500 line-clamp-2">
                            {festival.description}
                          </p>
                          <div className="flex items-center gap-2 mt-2">
                            <span className="text-xs text-gray-400">
                              {MONTH_NAMES[festival.typical_month]}
                            </span>
                            {festival.stories && festival.stories.length > 0 && (
                              <span className="text-xs text-primary-500 font-medium">
                                {festival.stories.length} {festival.stories.length === 1 ? 'story' : 'stories'}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Arrow */}
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth={2}
                          stroke="currentColor"
                          className="w-5 h-5 text-gray-400 flex-shrink-0"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m8.25 4.5 7.5 7.5-7.5 7.5"
                          />
                        </svg>
                      </div>
                    </Card>
                  </Link>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {/* Coming Soon Card */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-accent-50 border-2 border-accent-200 text-center py-6">
            <span className="text-4xl">✨</span>
            <h3 className="font-bold text-accent-700 mt-2">More Festival Stories Coming!</h3>
            <p className="text-sm text-accent-600 mt-1">
              We are adding stories for more festivals every week
            </p>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
