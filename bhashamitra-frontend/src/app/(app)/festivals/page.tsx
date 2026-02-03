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

// Month names for display
const MONTH_NAMES = [
  '', 'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

// Festival icons based on name (inclusive, not religion-based)
const getFestivalIcon = (name: string): string => {
  const lowerName = name.toLowerCase();
  // Hindu festivals
  if (lowerName.includes('diwali') || lowerName.includes('deepavali')) return '🪔';
  if (lowerName.includes('holi')) return '🎨';
  if (lowerName.includes('navratri') || lowerName.includes('durga')) return '💃';
  if (lowerName.includes('dussehra') || lowerName.includes('vijayadashami')) return '🏹';
  if (lowerName.includes('ganesh')) return '🐘';
  if (lowerName.includes('raksha') || lowerName.includes('rakhi')) return '🧵';
  if (lowerName.includes('janmashtami') || lowerName.includes('krishna')) return '🎺';
  if (lowerName.includes('pongal') || lowerName.includes('makar') || lowerName.includes('sankranti')) return '🌾';
  if (lowerName.includes('ugadi') || lowerName.includes('gudi padwa')) return '📅';
  if (lowerName.includes('onam')) return '🚣';
  // Muslim festivals
  if (lowerName.includes('eid')) return '🌙';
  if (lowerName.includes('ramadan') || lowerName.includes('ramzan')) return '🕌';
  if (lowerName.includes('muharram')) return '🖤';
  if (lowerName.includes('milad')) return '📖';
  // Sikh festivals
  if (lowerName.includes('baisakhi') || lowerName.includes('vaisakhi')) return '🌻';
  if (lowerName.includes('lohri')) return '🔥';
  if (lowerName.includes('gobind')) return '⚔️';
  if (lowerName.includes('guru') || lowerName.includes('nanak')) return '📿';
  // Christian festivals
  if (lowerName.includes('christmas')) return '🎄';
  if (lowerName.includes('easter')) return '🐰';
  if (lowerName.includes('good friday')) return '✝️';
  // Jain festivals
  if (lowerName.includes('mahavir')) return '🙏';
  if (lowerName.includes('paryushana')) return '🧘';
  // Buddhist festivals
  if (lowerName.includes('buddha') || lowerName.includes('vesak')) return '🪷';
  return '🎉'; // Default celebration icon
};

export default function FestivalsPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();
  const { speakWithAnimation } = usePeppiStore();

  // Get current language from active child, default to Hindi
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

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
        // Fetch festivals for the current language
        console.log('[FestivalsPage] Fetching festivals for language:', currentLanguage);
        const response = await api.getFestivals({ language: currentLanguage as 'HINDI' | 'TAMIL' | 'PUNJABI' | 'GUJARATI' | 'TELUGU' | 'MALAYALAM' | 'BENGALI' });
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
  }, [isHydrated, isAuthenticated, router, currentLanguage]);

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
            <p className="text-gray-500">Celebrate together through stories</p>
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
                  Every festival has a beautiful story. Pick one and let us celebrate together!
                </p>
              </div>
            </div>
          </Card>
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
                <p className="text-sm text-gray-400 mt-2">Check back soon!</p>
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
                        {/* Festival Icon - based on festival name, not religion */}
                        <div className="w-14 h-14 bg-gradient-to-br from-warning-100 to-warning-200 rounded-xl flex items-center justify-center flex-shrink-0">
                          <span className="text-2xl">
                            {getFestivalIcon(festival.name)}
                          </span>
                        </div>

                        {/* Festival Info */}
                        <div className="flex-1 min-w-0">
                          <h3 className="font-bold text-gray-900 truncate mb-1">
                            {festival.name}
                          </h3>
                          <p className="text-sm text-primary-600 font-medium mb-1">
                            {festival.name_native}
                          </p>
                          <p className="text-xs text-gray-500 line-clamp-2">
                            {festival.description}
                          </p>
                          <div className="flex items-center gap-2 mt-2">
                            <Badge variant="secondary" size="sm">
                              {MONTH_NAMES[festival.typical_month]}
                            </Badge>
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
