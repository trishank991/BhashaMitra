'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore, useProgressStore, usePeppiStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Badge, Loading, LanguageSelector } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { LanguageCode } from '@/types';
import api from '@/lib/api';

// Language-specific metadata for the home page
const LANGUAGE_METADATA: Record<string, { sampleLetter: string; scriptName: string }> = {
  HINDI: { sampleLetter: 'अ', scriptName: 'Devanagari' },
  TAMIL: { sampleLetter: 'அ', scriptName: 'Tamil Script' },
  TELUGU: { sampleLetter: 'అ', scriptName: 'Telugu Script' },
  GUJARATI: { sampleLetter: 'અ', scriptName: 'Gujarati Script' },
  PUNJABI: { sampleLetter: 'ਅ', scriptName: 'Gurmukhi' },
  BENGALI: { sampleLetter: 'অ', scriptName: 'Bengali Script' },
  MALAYALAM: { sampleLetter: 'അ', scriptName: 'Malayalam Script' },
};

interface CurriculumStats {
  letterCount: number;
  wordCount: number;
  topicCount: number;
  storyCount: number;
}

export default function HomePage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [isChangingLanguage, setIsChangingLanguage] = useState(false);
  const [curriculumStats, setCurriculumStats] = useState<CurriculumStats>({
    letterCount: 0,
    wordCount: 0,
    topicCount: 0,
    storyCount: 0,
  });
  const { isAuthenticated, activeChild, updateActiveChildLanguage } = useAuthStore();
  const { streak, storiesRead, wordsLearned } = useProgressStore();
  const { greet } = usePeppiStore();

  // Handle both string and object language formats from API
  const languageCode = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';
  const languageInfo = SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES] || SUPPORTED_LANGUAGES.HINDI;
  const languageMeta = LANGUAGE_METADATA[languageCode] || LANGUAGE_METADATA.HINDI;

  const handleLanguageChange = async (language: LanguageCode) => {
    console.log('[HomePage] Changing language to:', language);
    setIsChangingLanguage(true);
    try {
      const success = await updateActiveChildLanguage(language);
      if (!success) {
        console.error('[HomePage] Failed to update language');
      }
    } finally {
      setIsChangingLanguage(false);
    }
  };

  // Handle hydration
  useEffect(() => {
    setIsHydrated(true);
  }, []);

  // Fetch curriculum stats when language or child changes
  useEffect(() => {
    if (!isHydrated || !isAuthenticated || !activeChild?.id) return;

    const fetchCurriculumStats = async () => {
      try {
        // Fetch all curriculum data in parallel
        const [scriptsRes, vocabRes, grammarRes, storiesRes] = await Promise.all([
          api.getScripts(activeChild.id),
          api.getVocabularyThemes(activeChild.id),
          api.getGrammarTopics(activeChild.id),
          api.getStories(languageCode as LanguageCode),
        ]);

        // Count letters from all scripts
        let letterCount = 0;
        if (scriptsRes.success && scriptsRes.data) {
          letterCount = scriptsRes.data.reduce((sum, script) => sum + (script.total_letters || 0), 0);
        }

        // Count words from all themes
        let wordCount = 0;
        if (vocabRes.success && vocabRes.data) {
          wordCount = vocabRes.data.reduce((sum, theme) => sum + (theme.word_count || 0), 0);
        }

        // Count grammar topics
        let topicCount = 0;
        if (grammarRes.success && grammarRes.data) {
          topicCount = grammarRes.data.length;
        }

        // Count stories
        let storyCount = 0;
        if (storiesRes.success && storiesRes.data) {
          storyCount = storiesRes.data.results?.length || 0;
        }

        setCurriculumStats({
          letterCount,
          wordCount,
          topicCount,
          storyCount,
        });
      } catch (err) {
        console.error('[HomePage] Error fetching curriculum stats:', err);
      }
    };

    fetchCurriculumStats();
  }, [isHydrated, isAuthenticated, activeChild?.id, languageCode]);

  useEffect(() => {
    if (!isHydrated) return;

    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    // Greet user when page loads
    const timer = setTimeout(() => {
      greet();
    }, 500);
    return () => clearTimeout(timer);
  }, [isHydrated, isAuthenticated, router, greet]);

  // Show loading while hydrating
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

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Welcome Header */}
        <motion.div variants={fadeInUp} className="bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500 rounded-3xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm">Welcome back!</p>
              <h1 className="text-2xl font-bold">{activeChild?.name || 'Learner'}</h1>
              <p className="text-white/90 mt-1">Ready to learn {languageInfo?.name}?</p>
            </div>
            <div className="text-6xl">{languageInfo?.flag || '🇮🇳'}</div>
          </div>
        </motion.div>

        {/* Language Selector */}
        <motion.div variants={fadeInUp} className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-gray-900">Learning Language</h2>
            <p className="text-sm text-gray-500">Choose your language</p>
          </div>
          <LanguageSelector
            currentLanguage={languageCode as LanguageCode}
            onLanguageChange={handleLanguageChange}
            isLoading={isChangingLanguage}
          />
        </motion.div>

        {/* Quick Stats */}
        <motion.div variants={fadeInUp} className="grid grid-cols-3 gap-3">
          <Card padding="sm" className="text-center bg-orange-50">
            <div className="text-2xl mb-1">🔥</div>
            <p className="text-2xl font-bold text-orange-600">{streak}</p>
            <p className="text-xs text-gray-500">Day Streak</p>
          </Card>
          <Card padding="sm" className="text-center bg-blue-50">
            <div className="text-2xl mb-1">📖</div>
            <p className="text-2xl font-bold text-blue-600">{storiesRead.length}</p>
            <p className="text-xs text-gray-500">Stories</p>
          </Card>
          <Card padding="sm" className="text-center bg-green-50">
            <div className="text-2xl mb-1">📝</div>
            <p className="text-2xl font-bold text-green-600">{wordsLearned.length}</p>
            <p className="text-xs text-gray-500">Words</p>
          </Card>
        </motion.div>

        {/* Study Materials - Main Learning Section */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
            <span className="text-2xl">📚</span> Study Materials
          </h2>
          <div className="grid grid-cols-2 gap-3">
            <Link href="/learn/alphabet">
              <Card interactive className="bg-gradient-to-br from-red-100 to-orange-100 border-2 border-orange-200 hover:border-orange-400 transition-all">
                <div className="text-center py-4">
                  <div className="text-4xl mb-2">{languageMeta.sampleLetter}</div>
                  <h3 className="font-bold text-gray-900">Alphabet</h3>
                  <p className="text-xs text-gray-600 mt-1">Learn {languageMeta.scriptName}</p>
                  <p className="text-xs text-orange-600 font-medium mt-2">{curriculumStats.letterCount || 0} Letters</p>
                </div>
              </Card>
            </Link>

            <Link href="/learn/vocabulary">
              <Card interactive className="bg-gradient-to-br from-blue-100 to-indigo-100 border-2 border-blue-200 hover:border-blue-400 transition-all">
                <div className="text-center py-4">
                  <div className="text-4xl mb-2">📖</div>
                  <h3 className="font-bold text-gray-900">Vocabulary</h3>
                  <p className="text-xs text-gray-600 mt-1">Build word bank</p>
                  <p className="text-xs text-blue-600 font-medium mt-2">{curriculumStats.wordCount || 0} Words</p>
                </div>
              </Card>
            </Link>

            <Link href="/learn/grammar">
              <Card interactive className="bg-gradient-to-br from-green-100 to-teal-100 border-2 border-green-200 hover:border-green-400 transition-all">
                <div className="text-center py-4">
                  <div className="text-4xl mb-2">📝</div>
                  <h3 className="font-bold text-gray-900">Grammar</h3>
                  <p className="text-xs text-gray-600 mt-1">Learn rules</p>
                  <p className="text-xs text-green-600 font-medium mt-2">{curriculumStats.topicCount || 0} Topics</p>
                </div>
              </Card>
            </Link>

            <Link href="/stories">
              <Card interactive className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-200 hover:border-purple-400 transition-all">
                <div className="text-center py-4">
                  <div className="text-4xl mb-2">📚</div>
                  <h3 className="font-bold text-gray-900">Stories</h3>
                  <p className="text-xs text-gray-600 mt-1">Read & learn</p>
                  <p className="text-xs text-purple-600 font-medium mt-2">{curriculumStats.storyCount || 0} Stories</p>
                </div>
              </Card>
            </Link>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
            <span className="text-2xl">🎯</span> Quick Actions
          </h2>
          <div className="grid grid-cols-3 gap-3">
            <Link href="/games">
              <Card interactive className="text-center py-4 bg-yellow-50">
                <div className="text-3xl mb-1">🎮</div>
                <h3 className="font-semibold text-gray-900 text-sm">Games</h3>
              </Card>
            </Link>

            <Link href="/progress">
              <Card interactive className="text-center py-4 bg-amber-50">
                <div className="text-3xl mb-1">🏆</div>
                <h3 className="font-semibold text-gray-900 text-sm">Badges</h3>
              </Card>
            </Link>

            <Link href="/profile">
              <Card interactive className="text-center py-4 bg-gray-50">
                <div className="text-3xl mb-1">👤</div>
                <h3 className="font-semibold text-gray-900 text-sm">Profile</h3>
              </Card>
            </Link>
          </div>
        </motion.div>

        {/* Daily Goal */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-green-700">Daily Goal</h3>
                <p className="text-sm text-green-600">
                  Read 1 story and learn 5 new words
                </p>
              </div>
              <Badge variant="success">In Progress</Badge>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
