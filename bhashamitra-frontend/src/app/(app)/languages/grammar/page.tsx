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
import api, { GrammarTopic } from '@/lib/api';

const TOPIC_ICONS: Record<string, string> = {
  'Sentence Structure': '📝',
  'Gender': '👫',
  'Pronouns': '👆',
  'Verbs': '🏃',
  'Numbers': '🔢',
};

// Language metadata for grammar page
const LANGUAGE_META = {
  HINDI: {
    title: 'Grammar',
    subtitle: 'व्याकरण - Learn sentence structure and rules',
  },
  TAMIL: {
    title: 'Grammar',
    subtitle: 'இலக்கணம் - Learn sentence structure and rules',
  },
};

// Sample grammar tips per language
const GRAMMAR_TIPS = {
  HINDI: {
    wordOrder: {
      title: 'Word Order (SOV)',
      description: 'Hindi follows Subject-Object-Verb order:',
      example: 'मैं सेब खाता हूँ।',
      translation: 'I apple eat = I eat an apple',
    },
    gender: {
      title: 'Gender (लिंग)',
      description: 'Nouns ending in आ are usually masculine, ई are usually feminine:',
      examples: [
        { word: 'लड़का', meaning: 'boy (M)' },
        { word: 'लड़की', meaning: 'girl (F)' },
      ],
    },
  },
  TAMIL: {
    wordOrder: {
      title: 'Word Order (SOV)',
      description: 'Tamil follows Subject-Object-Verb order:',
      example: 'நான் ஆப்பிள் சாப்பிடுகிறேன்.',
      translation: 'I apple eat = I eat an apple',
    },
    gender: {
      title: 'Gender (பால்)',
      description: 'Tamil has three genders: masculine, feminine, and neuter:',
      examples: [
        { word: 'மகன்', meaning: 'son (M)' },
        { word: 'மகள்', meaning: 'daughter (F)' },
      ],
    },
  },
};

export default function GrammarPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [topics, setTopics] = useState<GrammarTopic[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedTopic, setExpandedTopic] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();

  // Get current language from active child, default to Hindi
  // Handle both string and object formats from API
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';
  const metadata = LANGUAGE_META[currentLanguage as keyof typeof LANGUAGE_META] || LANGUAGE_META.HINDI;
  const grammarTips = GRAMMAR_TIPS[currentLanguage as keyof typeof GRAMMAR_TIPS] || GRAMMAR_TIPS.HINDI;

  // Audio playback hook - use current language
  const { isPlaying, isLoading: audioLoading, playAudio, stopAudio } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // State to track which text is currently playing
  const [playingText, setPlayingText] = useState<string | null>(null);

  // Handle playing text audio
  const handlePlayText = (text: string) => {
    if (playingText === text && isPlaying) {
      stopAudio();
      setPlayingText(null);
    } else {
      setPlayingText(text);
      playAudio(text);
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

    // Fetch grammar topics from API
    const fetchTopics = async () => {
      if (!activeChild?.id) {
        setLoading(false);
        return;
      }

      setLoading(true);

      try {
        console.log('[GrammarPage] Fetching topics for child:', activeChild.id, 'language:', currentLanguage);
        const response = await api.getGrammarTopics(activeChild.id, currentLanguage);
        console.log('[GrammarPage] API response:', response);

        if (response.success && response.data) {
          setTopics(response.data);
          console.log('[GrammarPage] Loaded', response.data.length, 'topics');
        } else {
          console.error('[GrammarPage] Failed to load topics:', response.error);
          setTopics([]);
        }
      } catch (err) {
        console.error('[GrammarPage] Error fetching topics:', err);
        setTopics([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
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
          <Card padding="sm" className="text-center bg-green-50">
            <p className="text-2xl font-bold text-green-600">{topics.length}</p>
            <p className="text-xs text-gray-500">Topics</p>
          </Card>
          <Card padding="sm" className="text-center bg-blue-50">
            <p className="text-2xl font-bold text-blue-600">
              {topics.reduce((sum, t) => sum + (t.rule_count || 0), 0)}
            </p>
            <p className="text-xs text-gray-500">Rules</p>
          </Card>
          <Card padding="sm" className="text-center bg-purple-50">
            <p className="text-2xl font-bold text-purple-600">0</p>
            <p className="text-xs text-gray-500">Mastered</p>
          </Card>
        </motion.div>

        {/* Topics List */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Grammar Topics</h2>

          {loading ? (
            <div className="flex justify-center py-12">
              <Loading size="lg" text="Loading topics..." />
            </div>
          ) : topics.length === 0 ? (
            <Card className="bg-gray-50 text-center py-8">
              <p className="text-gray-500">No grammar topics available yet.</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {topics.map((topic, index) => (
                <motion.div
                  key={topic.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card
                    interactive
                    className="hover:shadow-md transition-shadow"
                    onClick={() => setExpandedTopic(expandedTopic === topic.id ? null : topic.id)}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 bg-gradient-to-br from-green-100 to-teal-100 rounded-2xl flex items-center justify-center text-3xl">
                        {TOPIC_ICONS[topic.name] || '📚'}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-bold text-gray-900">{topic.name}</h3>
                          <Badge variant="secondary" size="sm">
                            Level {topic.level}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-500">{topic.name_native}</p>
                        <p className="text-xs text-gray-400 mt-1">{topic.description}</p>
                      </div>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className={`h-5 w-5 text-gray-400 transition-transform ${
                          expandedTopic === topic.id ? 'rotate-180' : ''
                        }`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>

                    {/* Expanded Content */}
                    {expandedTopic === topic.id && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-4 pt-4 border-t border-gray-100"
                      >
                        <p className="text-sm text-gray-600 mb-3">{topic.description}</p>
                        <Link href={`/languages/grammar/${topic.id}`}>
                          <button className="w-full py-2 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors">
                            Start Learning
                          </button>
                        </Link>
                      </motion.div>
                    )}
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Sample Grammar Rules */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Quick Grammar Tips</h2>
          <div className="space-y-3">
            <Card className="bg-gradient-to-br from-blue-50 to-indigo-50">
              <h3 className="font-bold text-gray-900">{grammarTips.wordOrder.title}</h3>
              <p className="text-sm text-gray-600 mt-1">
                {grammarTips.wordOrder.description}
              </p>
              <div className="mt-2 p-3 bg-white rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-lg">{grammarTips.wordOrder.example}</p>
                    <p className="text-sm text-gray-500">{grammarTips.wordOrder.translation}</p>
                  </div>
                  <SpeakerButton
                    isPlaying={playingText === grammarTips.wordOrder.example && isPlaying}
                    isLoading={playingText === grammarTips.wordOrder.example && audioLoading}
                    onClick={() => handlePlayText(grammarTips.wordOrder.example)}
                    size="sm"
                  />
                </div>
              </div>
            </Card>

            <Card className="bg-gradient-to-br from-pink-50 to-rose-50">
              <h3 className="font-bold text-gray-900">{grammarTips.gender.title}</h3>
              <p className="text-sm text-gray-600 mt-1">
                {grammarTips.gender.description}
              </p>
              <div className="mt-2 p-3 bg-white rounded-lg flex gap-4">
                <div className="flex-1 flex gap-4">
                  {grammarTips.gender.examples.map((ex, idx) => (
                    <div key={idx}>
                      <p className="text-lg">{ex.word}</p>
                      <p className="text-xs text-gray-500">{ex.meaning}</p>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2">
                  {grammarTips.gender.examples.map((ex, idx) => (
                    <SpeakerButton
                      key={idx}
                      isPlaying={playingText === ex.word && isPlaying}
                      isLoading={playingText === ex.word && audioLoading}
                      onClick={() => handlePlayText(ex.word)}
                      size="sm"
                    />
                  ))}
                </div>
              </div>
            </Card>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
