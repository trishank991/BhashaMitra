'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Badge, SpeakerButton } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { useAudio } from '@/hooks/useAudio';
import api, { VocabularyTheme } from '@/lib/api';

const THEME_ICONS: Record<string, string> = {
  'Family': '👨‍👩‍👧‍👦',
  'Colors': '🎨',
  'Numbers': '🔢',
  'Animals': '🐾',
  'Food': '🍎',
  'Body Parts': '🖐️',
  'Greetings': '👋',
  'Actions': '🏃',
};

// Sample words per language (for preview section)
const SAMPLE_WORDS = {
  HINDI: [
    { word: 'माँ', roman: 'maa', meaning: 'mother' },
    { word: 'पिता', roman: 'pita', meaning: 'father' },
    { word: 'लाल', roman: 'laal', meaning: 'red' },
    { word: 'नीला', roman: 'neela', meaning: 'blue' },
  ],
  TAMIL: [
    { word: 'அம்மா', roman: 'ammaa', meaning: 'mother' },
    { word: 'அப்பா', roman: 'appaa', meaning: 'father' },
    { word: 'சிவப்பு', roman: 'sivappu', meaning: 'red' },
    { word: 'நீலம்', roman: 'neelam', meaning: 'blue' },
  ],
};

// Language metadata
const LANGUAGE_META: Record<string, { title: string; subtitle: string }> = {
  HINDI: {
    title: 'Vocabulary',
    subtitle: 'शब्दावली - Build your word bank',
  },
  TAMIL: {
    title: 'Vocabulary',
    subtitle: 'சொற்களஞ்சியம் - Build your word bank',
  },
};

export default function VocabularyPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [themes, setThemes] = useState<VocabularyTheme[]>([]);
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [error, setError] = useState<string | null>(null);
  const [playingWord, setPlayingWord] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();

  // Get current language from active child, default to Hindi
  // Handle both string and object formats from API
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';
  const metadata = LANGUAGE_META[currentLanguage] || LANGUAGE_META.HINDI;
  const sampleWords = SAMPLE_WORDS[currentLanguage as keyof typeof SAMPLE_WORDS] || SAMPLE_WORDS.HINDI;

  // Audio playback hook - use current language
  const { isPlaying, isLoading: audioLoading, playAudio, stopAudio } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // Handle playing word audio
  const handlePlayWord = (word: string) => {
    if (playingWord === word && isPlaying) {
      stopAudio();
      setPlayingWord(null);
    } else {
      setPlayingWord(word);
      playAudio(word);
    }
  };

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    // Fetch vocabulary themes from API
    const fetchThemes = async () => {
      if (!activeChild?.id) {
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        console.log('[VocabularyPage] Fetching themes for child:', activeChild.id, 'language:', currentLanguage);
        const response = await api.getVocabularyThemes(activeChild.id, currentLanguage);
        console.log('[VocabularyPage] API response:', response);

        if (response.success && response.data) {
          setThemes(response.data);
          console.log('[VocabularyPage] Loaded', response.data.length, 'themes');
        } else {
          setError(response.error || 'Failed to load vocabulary themes');
          setThemes([]);
        }
      } catch (err) {
        console.error('[VocabularyPage] Error fetching themes:', err);
        setError('Failed to load vocabulary themes');
        setThemes([]);
      } finally {
        setLoading(false);
      }
    };

    fetchThemes();
  }, [isHydrated, isAuthenticated, router, activeChild?.id, currentLanguage]);

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
        <motion.div variants={fadeInUp} className="flex items-center gap-3">
          <Link href="anguages" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{metadata.title}</h1>
            <p className="text-gray-500">{metadata.subtitle}</p>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div variants={fadeInUp} className="grid grid-cols-3 gap-3">
          <Card padding="sm" className="text-center bg-blue-50">
            <p className="text-2xl font-bold text-blue-600">
              {themes.reduce((sum, t) => sum + (t.word_count || 0), 0)}
            </p>
            <p className="text-xs text-gray-500">Total Words</p>
          </Card>
          <Card padding="sm" className="text-center bg-green-50">
            <p className="text-2xl font-bold text-green-600">{themes.length}</p>
            <p className="text-xs text-gray-500">Themes</p>
          </Card>
          <Card padding="sm" className="text-center bg-orange-50">
            <p className="text-2xl font-bold text-orange-600">
              {themes.reduce((sum, t) => sum + (t.progress?.words_mastered || 0), 0)}
            </p>
            <p className="text-xs text-gray-500">Mastered</p>
          </Card>
        </motion.div>

        {/* Themes List */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Word Themes</h2>

          {loading ? (
            <div className="flex justify-center py-12">
              <Loading size="lg" text="Loading themes..." />
            </div>
          ) : themes.length === 0 ? (
            <Card className="bg-gray-50 text-center py-8">
              <p className="text-gray-500">No vocabulary themes available yet.</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {themes.map((theme, index) => (
                <motion.div
                  key={theme.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Link href={`/languages/vocabulary/${theme.id}`}>
                    <Card interactive className="hover:shadow-md transition-shadow">
                      <div className="flex items-center gap-4">
                        <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl flex items-center justify-center text-3xl">
                          {THEME_ICONS[theme.name] || '📖'}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-gray-900">{theme.name}</h3>
                            <Badge variant="secondary" size="sm">
                              Level {theme.level}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-500">{theme.name_native}</p>
                          <p className="text-xs text-gray-400 mt-1">{theme.word_count} words</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center">
                            <span className="text-sm font-bold text-gray-600">
                              {theme.progress?.progress_percentage || 0}%
                            </span>
                          </div>
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </div>
                      </div>
                    </Card>
                  </Link>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Sample Words Preview */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Sample Words</h2>
          <p className="text-sm text-gray-500 mb-3">Tap the speaker to hear pronunciation</p>
          <div className="grid grid-cols-2 gap-3">
            {sampleWords.map((item, i) => (
              <Card key={i} className="bg-gradient-to-br from-purple-50 to-pink-50 relative">
                <div className="text-center">
                  <p className="text-3xl font-bold text-gray-900">{item.word}</p>
                  <p className="text-sm text-purple-600">{item.roman}</p>
                  <p className="text-xs text-gray-500 mt-1">{item.meaning}</p>
                  <div className="mt-2 flex justify-center">
                    <SpeakerButton
                      isPlaying={playingWord === item.word && isPlaying}
                      isLoading={playingWord === item.word && audioLoading}
                      onClick={() => handlePlayWord(item.word)}
                      size="sm"
                    />
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
