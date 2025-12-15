'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button, SpeakerButton } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api, { GrammarRule } from '@/lib/api';
import { useAudio } from '@/hooks/useAudio';

// Mock grammar rules data
const mockGrammarRules: Record<string, { topic: string; topicNative: string; rules: GrammarRule[] }> = {
  '1': {
    topic: 'Sentence Structure',
    topicNative: 'वाक्य रचना',
    rules: [
      {
        id: '1',
        title: 'Subject-Object-Verb (SOV) Order',
        explanation: 'Hindi follows SOV word order, unlike English which uses SVO. The verb comes at the end of the sentence.',
        formula: 'Subject + Object + Verb',
        examples: [
          'मैं सेब खाता हूँ। (I apple eat = I eat an apple)',
          'राम किताब पढ़ता है। (Ram book reads = Ram reads a book)',
        ],
        tips: 'Remember: The verb always comes at the end!',
      },
      {
        id: '2',
        title: 'Postpositions',
        explanation: 'Hindi uses postpositions instead of prepositions. They come after the noun.',
        formula: 'Noun + Postposition',
        examples: [
          'मेज पर (table on = on the table)',
          'घर में (house in = in the house)',
        ],
        tips: 'Think of it as the opposite of English prepositions.',
      },
    ],
  },
  '2': {
    topic: 'Gender',
    topicNative: 'लिंग',
    rules: [
      {
        id: '1',
        title: 'Masculine Nouns',
        explanation: 'Most nouns ending in आ (aa) are masculine. Verbs and adjectives must agree with the gender.',
        examples: [
          'लड़का (boy) - masculine',
          'कमरा (room) - masculine',
          'बड़ा लड़का (big boy)',
        ],
      },
      {
        id: '2',
        title: 'Feminine Nouns',
        explanation: 'Most nouns ending in ई (ee) or इ (i) are feminine.',
        examples: [
          'लड़की (girl) - feminine',
          'किताब (book) - feminine',
          'बड़ी लड़की (big girl)',
        ],
      },
    ],
  },
  '3': {
    topic: 'Pronouns',
    topicNative: 'सर्वनाम',
    rules: [
      {
        id: '1',
        title: 'Personal Pronouns',
        explanation: 'Hindi has different pronouns for formal and informal situations.',
        examples: [
          'मैं (I)',
          'तू (you - very informal)',
          'तुम (you - informal)',
          'आप (you - formal)',
          'वह (he/she - informal)',
          'वे (they/he/she - formal)',
        ],
        tips: 'Use आप with elders and strangers to show respect.',
      },
    ],
  },
  '4': {
    topic: 'Verbs',
    topicNative: 'क्रिया',
    rules: [
      {
        id: '1',
        title: 'Verb Root + Ending',
        explanation: 'Hindi verbs change based on gender, number, and tense. Start with the verb root and add appropriate endings.',
        formula: 'Verb Root + Gender/Number Ending + Tense Marker',
        examples: [
          'खा (eat root) → खाता (eats - masculine) → खाती (eats - feminine)',
          'जा (go root) → जाता है (goes) → गया (went)',
        ],
      },
      {
        id: '2',
        title: 'Present Tense',
        explanation: 'Add ता/ती/ते to the verb root, then add auxiliary verb.',
        examples: [
          'मैं खाता हूँ (I eat - male speaker)',
          'मैं खाती हूँ (I eat - female speaker)',
          'वह खाता है (He eats)',
        ],
      },
    ],
  },
  '5': {
    topic: 'Numbers',
    topicNative: 'संख्या',
    rules: [
      {
        id: '1',
        title: 'Cardinal Numbers 1-10',
        explanation: 'Learn the basic Hindi numbers from 1 to 10.',
        examples: [
          '१ - एक (ek) - one',
          '२ - दो (do) - two',
          '३ - तीन (teen) - three',
          '४ - चार (chaar) - four',
          '५ - पाँच (paanch) - five',
          '६ - छह (chhah) - six',
          '७ - सात (saat) - seven',
          '८ - आठ (aath) - eight',
          '९ - नौ (nau) - nine',
          '१० - दस (das) - ten',
        ],
      },
    ],
  },
};

export default function GrammarTopicDetailPage() {
  const router = useRouter();
  const params = useParams();
  const topicId = params.id as string;

  const [isHydrated, setIsHydrated] = useState(false);
  const [rules, setRules] = useState<GrammarRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedRule, setExpandedRule] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();

  const topicData = mockGrammarRules[topicId];

  // Audio playback hook
  const { isPlaying, isLoading: audioLoading, playAudio, stopAudio } = useAudio({
    language: 'HINDI',
    voiceStyle: 'kid_friendly',
  });

  // State to track which text is currently playing
  const [playingText, setPlayingText] = useState<string | null>(null);

  // Handle playing text audio - extract Hindi text from examples
  const handlePlayExample = (example: string) => {
    // Extract Hindi text before any parentheses or equals sign
    const hindiMatch = example.match(/^([^(=]+)/);
    const hindiText = hindiMatch ? hindiMatch[1].trim() : example;

    if (playingText === hindiText && isPlaying) {
      stopAudio();
      setPlayingText(null);
    } else {
      setPlayingText(hindiText);
      playAudio(hindiText);
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

    // Try to fetch from API, fall back to mock data
    const fetchRules = async () => {
      if (!activeChild?.id) {
        // Use mock data
        if (topicData) {
          setRules(topicData.rules);
        }
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        const response = await api.getTopicRules(activeChild.id, topicId);
        if (response.success && response.data && response.data.length > 0) {
          setRules(response.data);
        } else if (topicData) {
          // Fall back to mock data
          setRules(topicData.rules);
        }
      } catch {
        // Fall back to mock data
        if (topicData) {
          setRules(topicData.rules);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchRules();
  }, [isHydrated, isAuthenticated, activeChild, topicId, router, topicData]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (!topicData) {
    return (
      <MainLayout headerTitle="Topic Not Found">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-6xl mb-4">📚</span>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Topic Not Found</h1>
          <p className="text-gray-500 mb-6">This grammar topic doesn&apos;t exist.</p>
          <Link href="/learn/grammar">
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
          <Link href="/learn/grammar" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{topicData.topic}</h1>
            <p className="text-gray-500">{topicData.topicNative}</p>
          </div>
        </motion.div>

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

                    {/* Expanded Content */}
                    {expandedRule === rule.id && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-4 pt-4 border-t border-gray-100 space-y-4"
                      >
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
                        <div>
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Examples</h4>
                          <div className="space-y-2">
                            {rule.examples.map((example, i) => {
                              const hindiMatch = example.match(/^([^(=]+)/);
                              const hindiText = hindiMatch ? hindiMatch[1].trim() : example;
                              return (
                                <div
                                  key={i}
                                  className="p-3 bg-gray-50 rounded-lg text-sm text-gray-700 flex items-center justify-between gap-3"
                                >
                                  <span className="flex-1">{example}</span>
                                  <SpeakerButton
                                    isPlaying={playingText === hindiText && isPlaying}
                                    isLoading={playingText === hindiText && audioLoading}
                                    onClick={() => handlePlayExample(example)}
                                    size="sm"
                                  />
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
                      </motion.div>
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
