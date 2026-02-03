'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Badge, Button, SpeakerButton } from '@/components/ui';
import { VisualFlashcard } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api, { VocabularyWord, VocabularyTheme } from '@/lib/api';
import { useAudio } from '@/hooks/useAudio';
import { useSounds } from '@/hooks';

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

const THEME_EMOJIS: Record<string, string> = {
  'Family': '👨‍👩‍👧',
  'Colors': '🎨',
  'Numbers': '🔢',
  'Animals': '🐾',
  'Food': '🍎',
  'Body Parts': '🖐️',
  'Greetings': '👋',
  'Actions': '🏃',
};

const getThemeEmoji = (themeName?: string): string => {
  return THEME_EMOJIS[themeName || ''] || '📚';
};

export default function VocabularyThemeDetailPage() {
  const router = useRouter();
  const params = useParams();
  const themeId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [theme, setTheme] = useState<VocabularyTheme | null>(null);
  const [words, setWords] = useState<VocabularyWord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [showMeaning, setShowMeaning] = useState(false);
  const [mode, setMode] = useState<'list' | 'flashcard'>('list');
  const [playingWord, setPlayingWord] = useState<string | null>(null);
  const [reviewedWords, setReviewedWords] = useState<Set<string>>(new Set());
  const [completionXP, setCompletionXP] = useState<number>(0);
  const [showCompletion, setShowCompletion] = useState(false);
  const { isAuthenticated, activeChild } = useAuthStore();

  // Get current language from active child
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  // Audio playback hook - use current language
  const { isPlaying, isLoading: audioLoading, playAudio, stopAudio } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // Sound effects hook
  const { onClick, onCorrect, onPageTurn, onCelebration } = useSounds();

  // Handle playing word audio
  const handlePlayWord = (word: string, e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation(); // Prevent card click events
    }
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

    // Fetch theme and words from API
    const fetchThemeAndWords = async () => {
      if (!themeId) {
        setLoading(false);
        setError('Invalid theme ID');
        return;
      }
      if (!activeChild?.id) {
        setLoading(false);
        setError('No active child profile');
        return;
      }

      setLoading(true);
      setError(null);

      try {
        console.log('[VocabularyDetail] Fetching theme', themeId, 'for child:', activeChild.id);

        // First, fetch themes to get theme info
        const themesResponse = await api.getVocabularyThemes(activeChild.id);
        console.log('[VocabularyDetail] Themes response:', themesResponse);

        if (themesResponse.success && themesResponse.data) {
          const foundTheme = themesResponse.data.find(t => t.id === themeId);
          if (foundTheme) {
            setTheme(foundTheme);
            console.log('[VocabularyDetail] Found theme:', foundTheme.name);
          } else {
            console.log('[VocabularyDetail] Theme not found in list');
          }
        }

        // Fetch words for this theme
        const wordsResponse = await api.getThemeWords(activeChild.id, themeId);
        console.log('[VocabularyDetail] Words response:', wordsResponse);

        if (wordsResponse.success && wordsResponse.data && wordsResponse.data.length > 0) {
          setWords(wordsResponse.data);
          console.log('[VocabularyDetail] Loaded', wordsResponse.data.length, 'words');
        } else {
          setError('No words found for this theme');
          setWords([]);
        }
      } catch (err) {
        console.error('[VocabularyDetail] Error fetching data:', err);
        setError('Failed to load vocabulary words');
        setWords([]);
      } finally {
        setLoading(false);
      }
    };

    fetchThemeAndWords();
  }, [isHydrated, isAuthenticated, activeChild?.id, themeId, router]);

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
        <div className="flex justify-center py-12">
          <Loading size="lg" text="Loading vocabulary..." />
        </div>
      </MainLayout>
    );
  }

  if (error || words.length === 0) {
    return (
      <MainLayout headerTitle="Theme Not Found">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-6xl mb-4">📚</span>
          <h1 className="text-xl font-bold text-gray-900 mb-2">
            {error || 'No Words Found'}
          </h1>
          <p className="text-gray-500 mb-6">
            {error ? 'Please try again later.' : 'This vocabulary theme has no words yet.'}
          </p>
          <Link href="/languages/vocabulary">
            <Button>Back to Vocabulary</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }

  const currentWord = words[currentWordIndex];
  const themeName = theme?.name || 'Vocabulary';
  const themeNameNative = theme?.name_native || '';
  const themeIcon = theme?.name ? THEME_ICONS[theme.name] || '📖' : '📖';

  // Track word review and update SRS
  const handleWordReviewed = async (wordId: string, quality: number = 4) => {
    if (!activeChild?.id || reviewedWords.has(wordId)) return;

    try {
      // Call flashcard review API (quality 4 = good recall)
      const response = await api.reviewFlashcard(activeChild.id, wordId, quality);
      if (response.success) {
        onCorrect(); // Play correct sound when word is reviewed
        setReviewedWords(prev => new Set(prev).add(wordId));
        // Award 5 XP per word reviewed
        setCompletionXP(prev => prev + 5);
      }
    } catch (err) {
      console.error('[VocabularyDetail] Failed to record review:', err);
    }
  };

  const handleNextWord = () => {
    // Mark current word as reviewed when moving to next
    if (currentWord && showMeaning) {
      handleWordReviewed(currentWord.id);
    }

    if (currentWordIndex < words.length - 1) {
      onClick(); // Play click sound when navigating
      setCurrentWordIndex((prev) => prev + 1);
      setShowMeaning(false);
    } else if (currentWordIndex === words.length - 1 && showMeaning) {
      // Last word reviewed - mark as complete
      handleWordReviewed(currentWord.id);
      onCelebration(); // Play celebration sound on completion
      setShowCompletion(true);
    }
  };

  const handlePrevWord = () => {
    if (currentWordIndex > 0) {
      onClick(); // Play click sound when navigating
      setCurrentWordIndex((prev) => prev - 1);
      setShowMeaning(false);
    }
  };

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
          <Link href="/languages/vocabulary" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{themeIcon}</span>
              <h1 className="text-2xl font-bold text-gray-900">{themeName}</h1>
            </div>
            {themeNameNative && (
              <p className="text-gray-500">{themeNameNative}</p>
            )}
          </div>
        </motion.div>

        {/* Mode Toggle */}
        <motion.div variants={fadeInUp} className="flex gap-2">
          <button
            onClick={() => { onClick(); setMode('list'); }}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
              mode === 'list'
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Word List
          </button>
          <button
            onClick={() => { onClick(); setMode('flashcard'); setCurrentWordIndex(0); setShowMeaning(false); }}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
              mode === 'flashcard'
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Flashcards
          </button>
        </motion.div>

        {mode === 'list' ? (
          /* Word List Mode */
          <motion.div variants={fadeInUp} className="space-y-3">
            {words.map((word) => (
              <Card key={word.id} className="hover:shadow-md transition-shadow overflow-hidden">
                <div className="flex items-center gap-4">
                  {/* Add image */}
                  {word.image_url ? (
                    <div className="w-16 h-16 rounded-xl overflow-hidden flex-shrink-0">
                      <img
                        src={word.image_url}
                        alt={word.translation}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          // Fallback to placeholder on error
                          e.currentTarget.src = '';
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  ) : (
                    <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl flex items-center justify-center flex-shrink-0">
                      <span className="text-2xl">{getThemeEmoji(theme?.name)}</span>
                    </div>
                  )}
                  <div className="flex-1">
                    <p className="text-2xl font-bold text-gray-900">{word.word}</p>
                    <p className="text-sm text-purple-600">{word.romanization}</p>
                    <p className="text-sm text-gray-500">{word.translation}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <SpeakerButton
                      isPlaying={playingWord === word.word && isPlaying}
                      isLoading={playingWord === word.word && audioLoading}
                      onClick={() => handlePlayWord(word.word)}
                      size="sm"
                    />
                    <div className="text-right">
                      {word.gender && (
                        <Badge variant={word.gender === 'masculine' ? 'primary' : 'secondary'} size="sm">
                          {word.gender === 'masculine' ? 'M' : 'F'}
                        </Badge>
                      )}
                      <p className="text-xs text-gray-400 mt-1">{word.part_of_speech}</p>
                    </div>
                  </div>
                </div>
                {word.example_sentence && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Example: </span>
                      {word.example_sentence}
                    </p>
                  </div>
                )}
              </Card>
            ))}
          </motion.div>
        ) : (
          /* Flashcard Mode */
          <motion.div variants={fadeInUp} className="space-y-6">
            {/* Progress */}
            <div className="text-center">
              <p className="text-sm text-gray-500">
                Card {currentWordIndex + 1} of {words.length}
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div
                  className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentWordIndex + 1) / words.length) * 100}%` }}
                />
              </div>
            </div>

            {/* Flashcard */}
            <AnimatePresence mode="wait">
              <motion.div
                key={currentWordIndex}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.2 }}
              >
                <VisualFlashcard
                  word={currentWord.word}
                  romanization={currentWord.romanization}
                  translation={currentWord.translation}
                  imageUrl={currentWord.image_url}
                  gender={currentWord.gender}
                  partOfSpeech={currentWord.part_of_speech}
                  exampleSentence={currentWord.example_sentence}
                  category={theme?.name}
                  isFlipped={showMeaning}
                  onFlip={() => { onPageTurn(); setShowMeaning(!showMeaning); }}
                  onAudioPlay={(word) => handlePlayWord(word)}
                />
              </motion.div>
            </AnimatePresence>

            {/* Navigation */}
            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={handlePrevWord}
                disabled={currentWordIndex === 0}
                className="flex-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Previous
              </Button>
              <Button
                onClick={handleNextWord}
                disabled={currentWordIndex === words.length - 1}
                className="flex-1"
              >
                Next
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Button>
            </div>

            {(showCompletion || (currentWordIndex === words.length - 1 && showMeaning)) && (
              <Card className="bg-gradient-to-br from-green-50 to-teal-50 text-center py-6">
                <span className="text-5xl mb-3 block">🎉</span>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Excellent Work!</h3>
                <p className="text-sm text-gray-600 mb-2">
                  You reviewed all {words.length} words in {themeName}!
                </p>
                {completionXP > 0 && (
                  <div className="bg-yellow-100 rounded-xl py-2 px-4 inline-block mb-4">
                    <span className="text-2xl mr-2">⭐</span>
                    <span className="text-lg font-bold text-yellow-700">+{completionXP} XP</span>
                  </div>
                )}
                <div className="flex gap-3 justify-center">
                  <Button
                    variant="outline"
                    onClick={() => {
                      onClick();
                      setCurrentWordIndex(0);
                      setShowMeaning(false);
                      setShowCompletion(false);
                      setReviewedWords(new Set());
                      setCompletionXP(0);
                    }}
                  >
                    Practice Again
                  </Button>
                  <Link href="/languages/vocabulary">
                    <Button onClick={onClick}>Back to Vocabulary</Button>
                  </Link>
                </div>
              </Card>
            )}
          </motion.div>
        )}
      </motion.div>
    </MainLayout>
  );
}
