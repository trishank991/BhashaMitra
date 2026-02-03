'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, useProgressStore, usePeppiStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading, LanguageSelector } from '@/components/ui';
import { SUPPORTED_LANGUAGES } from '@/lib/constants';
import { LanguageCode } from '@/types';
import api from '@/lib/api';
import { useSubscription, useChildHomepageProgress } from '@/hooks/useSubscription';
import { FreeHomepage, PaidHomepage } from '@/components/home';
import { EmailVerificationBanner } from '@/components/auth';
import { motion } from 'framer-motion';
import { fadeInUp } from '@/lib/constants';

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

  // Subscription and progress hooks
  const subscription = useSubscription();
  const childProgress = useChildHomepageProgress(activeChild?.id || null);

  // Handle both string and object language formats from API
  const languageCode = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';
  const languageInfo = SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES] || SUPPORTED_LANGUAGES.HINDI;

  const handleLanguageChange = async (language: LanguageCode) => {
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
        const [scriptsRes, vocabRes, grammarRes, storiesRes] = await Promise.all([
          api.getScripts(activeChild.id),
          api.getVocabularyThemes(activeChild.id),
          api.getGrammarTopics(activeChild.id),
          api.getStories(languageCode as LanguageCode),
        ]);

        let letterCount = 0;
        if (scriptsRes.success && scriptsRes.data) {
          letterCount = scriptsRes.data.reduce((sum, script) => sum + (script.total_letters || 0), 0);
        }

        let wordCount = 0;
        if (vocabRes.success && vocabRes.data) {
          wordCount = vocabRes.data.reduce((sum, theme) => sum + (theme.word_count || 0), 0);
        }

        let topicCount = 0;
        if (grammarRes.success && grammarRes.data) {
          topicCount = grammarRes.data.length;
        }

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

  // Show loading while subscription data is loading
  if (subscription.loading) {
    return (
      <MainLayout>
        <div className="min-h-[60vh] flex items-center justify-center">
          <Loading size="lg" text="Loading your dashboard..." />
        </div>
      </MainLayout>
    );
  }

  // Always show Peppi - MainLayout decides what to show based on subscription tier:
  // - Paid users: PeppiChatButton + PeppiChatPanel (3 modes)
  // - Free users: PeppiAlphabetHelper (preset prompts only)

  return (
    <MainLayout showPeppi={true}>
      {/* Email Verification Banner */}
      <EmailVerificationBanner className="mb-4 -mx-4 sm:-mx-6 rounded-none sm:rounded-lg sm:mx-0" />

      {/* Language Selector at the top */}
      <motion.div
        variants={fadeInUp}
        initial="initial"
        animate="animate"
        className="flex items-center justify-between mb-6"
      >
        <div>
          <h2 className="text-lg font-bold text-gray-900">Learning {languageInfo?.name}</h2>
          <p className="text-sm text-gray-500">{languageInfo?.flag} {languageInfo?.nativeName}</p>
        </div>
        <LanguageSelector
          currentLanguage={languageCode as LanguageCode}
          onLanguageChange={handleLanguageChange}
          isLoading={isChangingLanguage}
        />
      </motion.div>

      {/* Render appropriate homepage based on subscription tier */}
      {subscription.isPaidTier ? (
        <PaidHomepage
          child={activeChild}
          tier={subscription.tier as 'STANDARD' | 'PREMIUM'}
          streak={streak}
          storiesRead={storiesRead}
          wordsLearned={wordsLearned}
          features={subscription.features}
          limits={subscription.limits}
          childProgress={childProgress}
          curriculumStats={curriculumStats}
        />
      ) : (
        <FreeHomepage
          child={activeChild}
          streak={streak}
          storiesRead={storiesRead}
          wordsLearned={wordsLearned}
          limits={subscription.limits}
          upgradeCta={subscription.upgradeCta}
          curriculumStats={curriculumStats}
          childProgress={childProgress}
        />
      )}

    </MainLayout>
  );
}
