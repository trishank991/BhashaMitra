'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore, usePeppiStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button, SpeakerButton } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api, { GrammarRule, GrammarTopic, GrammarExample } from '@/lib/api';
import { useAudio } from '@/hooks/useAudio';

export default function GrammarTopicDetailPage() {
  const router = useRouter();
  const params = useParams();
  const topicId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [topic, setTopic] = useState<GrammarTopic | null>(null);
  const [rules, setRules] = useState<GrammarRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedRule, setExpandedRule] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();
  const { speakWithAnimation } = usePeppiStore();

  // Get current language from active child
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  // Audio playback hook - use current language
  const { isPlaying, isLoading: audioLoading, error: audioError, playAudio, stopAudio } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // State to track which example is currently playing - use unique ID for stability
  const [playingId, setPlayingId] = useState<string | null>(null);

  // Track audio error for display
  const [displayError, setDisplayError] = useState<string | null>(null);

  // Log audio errors for debugging and display
  useEffect(() => {
    if (audioError) {
      console.error('[Grammar] Audio error:', audioError);
      setDisplayError(audioError);
      // Clear error after 3 seconds
      const timer = setTimeout(() => {
        setDisplayError(null);
        setPlayingId(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [audioError]);

  // Handle playing text audio - use unique ID for tracking
  const handlePlayExample = useCallback(async (example: string | GrammarExample, ruleId: string, exampleIndex: number) => {
    // Create a unique ID for this example
    const exampleId = `${ruleId}-${exampleIndex}`;
    
    // Handle both string and object example formats
    let textToPlay: string;
    if (typeof example === 'string') {
      // Extract text before any parentheses or equals sign
      const match = example.match(/^([^(=]+)/);
      textToPlay = match ? match[1].trim() : example;
    } else {
      // Object format: { hindi: '...', romanized: '...', english: '...' }
      textToPlay = example.hindi || example.romanized || '';
    }

    console.log('[Grammar] handlePlayExample called:', {
      exampleId,
      textToPlay,
      language: currentLanguage,
      isPlaying,
      playingId
    });

    if (playingId === exampleId && isPlaying) {
      console.log('[Grammar] Stopping audio');
      stopAudio();
      setPlayingId(null);
    } else {
      console.log('[Grammar] Starting audio playback for:', textToPlay);
      setPlayingId(exampleId);
      try {
        await playAudio(textToPlay);
        console.log('[Grammar] playAudio called successfully');
      } catch (err) {
        console.error('[Grammar] playAudio error:', err);
        setPlayingId(null);
      }
    }
  }, [playingId, isPlaying, stopAudio, playAudio, currentLanguage]);

  // Format example for display
  const formatExample = (example: string | GrammarExample): string => {
    if (typeof example === 'string') {
      return example;
    }
    // Object format: { hindi: '...', romanized: '...', english: '...' }
    const parts: string[] = [];
    if (example.hindi) parts.push(example.hindi);
    if (example.romanized) parts.push(`(${example.romanized})`);
    if (example.english) parts.push(`= ${example.english}`);
    return parts.join(' ');
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

    const fetchTopicAndRules = async () => {
      if (!topicId) {
        setError('Invalid topic ID');
        setLoading(false);
        return;
      }
      if (!activeChild?.id) {
        setError('Please select a child profile first');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        // Fetch topic details to get the name
        const topicsResponse = await api.getGrammarTopics(activeChild.id, currentLanguage);
        if (topicsResponse.success && topicsResponse.data) {
          const foundTopic = topicsResponse.data.find(t => t.id === topicId);
          if (foundTopic) {
            setTopic(foundTopic);
          }
        }

        // Fetch rules for this topic
        const rulesResponse = await api.getTopicRules(activeChild.id, topicId);
        if (rulesResponse.success && rulesResponse.data) {
          setRules(rulesResponse.data);
          console.log('[GrammarTopicDetail] Loaded', rulesResponse.data.length, 'rules');
        } else {
          console.log('[GrammarTopicDetail] No rules returned:', rulesResponse.error);
          setRules([]);
        }
      } catch (err) {
        console.error('[GrammarTopicDetail] Error:', err);
        setError('Failed to load grammar rules');
      } finally {
        setLoading(false);
      }
    };

    fetchTopicAndRules();
  }, [isHydrated, isAuthenticated, activeChild?.id, topicId, router, currentLanguage]);

  // Peppi greeting when rules load
  useEffect(() => {
    if (isHydrated && !loading && topic && rules.length > 0) {
      speakWithAnimation(`Let's learn about ${topic.name}!`, 'explanation');
    }
  }, [isHydrated, loading, topic, rules.length, speakWithAnimation]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (!loading && !topic && error) {
    return (
      <MainLayout headerTitle="Topic Not Found">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-6xl mb-4">📚</span>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Topic Not Found</h1>
          <p className="text-gray-500 mb-6">This grammar topic doesn't exist.</p>
          <Link href="/languages/grammar">
            <Button>Back to Grammar</Button>
          </Link>
        </div>
      </MainLayout>
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
          <Link href="/languages/grammar" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{topic?.name || 'Grammar Topic'}</h1>
            <p className="text-gray-500">{topic?.name_native || ''}</p>
          </div>
        </motion.div>

        {/* Audio Error Toast */}
        {displayError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm"
          >
            🔊 Audio error: {displayError}
          </motion.div>
        )}

        {/* Stats */}
        <motion.div variants={fadeInUp} className="grid grid-cols-2 gap-3">
          <Card padding="sm" className="text-center bg-green-50">
            <p className="text-2xl font-bold text-green-600">{rules.length}</p>
            <p className="text-xs text-gray-500">Rules</p>
          </Card>
          <Card padding="sm" className="text-center bg-blue-50">
            <p className="text-2xl font-bold text-blue-600">0</p>
            <p className="text-xs text-gray-500">Practiced</p>
          </Card>
        </motion.div>

        {/* Rules List */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Grammar Rules</h2>

          {loading ? (
            <div className="flex justify-center py-12">
              <Loading size="lg" text="Loading rules..." />
            </div>
          ) : rules.length === 0 ? (
            <Card className="bg-gray-50 text-center py-8">
              <p className="text-gray-500">No rules available for this topic yet.</p>
            </Card>
          ) : (
            <div className="space-y-4">
              {rules.map((rule, index) => (
                <motion.div
                  key={rule.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card
                    interactive
                    className="hover:shadow-md transition-shadow"
                    onClick={() => setExpandedRule(expandedRule === rule.id ? null : rule.id)}
                  >
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-gradient-to-br from-green-100 to-teal-100 rounded-xl flex items-center justify-center text-lg font-bold text-green-600">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-bold text-gray-900">{rule.title}</h3>
                        </div>
                        <p className="text-sm text-gray-500 mt-1 line-clamp-2">{rule.explanation}</p>
                      </div>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className={`h-5 w-5 text-gray-400 transition-transform ${
                          expandedRule === rule.id ? 'rotate-180' : ''
                        }`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>

                    {/* Expanded Content - using regular div to avoid motion animation conflicts */}
                    {expandedRule === rule.id && (
                      <div className="mt-4 pt-4 border-t border-gray-100 space-y-4">
                        {/* Explanation */}
                        <div>
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Explanation</h4>
                          <p className="text-sm text-gray-600">{rule.explanation}</p>
                        </div>

                        {/* Formula */}
                        {rule.formula && (
                          <div className="p-3 bg-blue-50 rounded-lg">
                            <h4 className="text-sm font-semibold text-blue-700 mb-1">Formula</h4>
                            <p className="text-sm text-blue-600 font-mono">{rule.formula}</p>
                          </div>
                        )}

                        {/* Examples */}
                        <div onClick={(e: React.MouseEvent) => e.stopPropagation()}>
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Examples</h4>
                          <div className="space-y-2">
                            {rule.examples.map((example, i) => {
                              // Extract text for audio playback - handle both string and object formats
                              let textToPlay: string;
                              if (typeof example === 'string') {
                                const match = example.match(/^([^(=]+)/);
                                textToPlay = match ? match[1].trim() : example;
                              } else {
                                textToPlay = example.hindi || example.romanized || '';
                              }
                              // Create unique ID for this example
                              const exampleId = `${rule.id}-${i}`;
                              // Check if this example is currently playing or loading
                              const isThisPlaying = playingId === exampleId && isPlaying;
                              const isThisLoading = playingId === exampleId && audioLoading;
                              
                              return (
                                <div
                                  key={i}
                                  className="p-3 bg-gray-50 rounded-lg text-sm text-gray-700 flex items-center justify-between gap-3 pointer-events-none"
                                  onClick={(e: React.MouseEvent) => e.stopPropagation()}
                                >
                                  <span className="flex-1 pointer-events-auto">{formatExample(example)}</span>
                                  <div className="pointer-events-auto" onClick={(e: React.MouseEvent) => e.stopPropagation()}>
                                    <SpeakerButton
                                      isPlaying={isThisPlaying}
                                      isLoading={isThisLoading}
                                      onClick={() => {
                                        console.log('[Grammar] Playing audio for:', textToPlay);
                                        handlePlayExample(example, rule.id, i);
                                      }}
                                      size="sm"
                                    />
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>

                        {/* Tips */}
                        {rule.tips && (
                          <div className="p-3 bg-yellow-50 rounded-lg">
                            <h4 className="text-sm font-semibold text-yellow-700 mb-1">💡 Tip</h4>
                            <p className="text-sm text-yellow-600">{rule.tips}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Practice Button */}
        <motion.div variants={fadeInUp} className="pt-4">
          <Card className="bg-gradient-to-br from-green-50 to-teal-50 text-center py-6">
            <span className="text-4xl mb-2 block">📝</span>
            <h3 className="font-bold text-gray-900 mb-2">Ready to Practice?</h3>
            <p className="text-sm text-gray-600 mb-4">
              Test your understanding with interactive exercises
            </p>
            <Button className="bg-green-500 hover:bg-green-600">
              Start Practice (Coming Soon)
            </Button>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
