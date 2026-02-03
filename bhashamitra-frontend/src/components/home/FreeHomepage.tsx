'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { ChildProfile, LanguageCode } from '@/types';
import { UpgradeCTA, SubscriptionLimits } from '@/lib/api';
import { ChildProgress } from '@/hooks/useSubscription';

interface FreeHomepageProps {
  child: ChildProfile | null;
  streak: number;
  storiesRead: string[];
  wordsLearned: string[];
  limits: SubscriptionLimits;
  upgradeCta: UpgradeCTA | null;
  curriculumStats: {
    letterCount: number;
    wordCount: number;
    topicCount: number;
    storyCount: number;
  };
  childProgress: ChildProgress | null;
}

// Language-specific metadata
const LANGUAGE_METADATA: Record<string, { sampleLetter: string; scriptName: string }> = {
  HINDI: { sampleLetter: '\u0905', scriptName: 'Devanagari' },
  TAMIL: { sampleLetter: '\u0B85', scriptName: 'Tamil Script' },
  TELUGU: { sampleLetter: '\u0C05', scriptName: 'Telugu Script' },
  GUJARATI: { sampleLetter: '\u0A85', scriptName: 'Gujarati Script' },
  PUNJABI: { sampleLetter: '\u0A05', scriptName: 'Gurmukhi' },
  BENGALI: { sampleLetter: '\u0985', scriptName: 'Bengali Script' },
  MALAYALAM: { sampleLetter: '\u0D05', scriptName: 'Malayalam Script' },
};

export function FreeHomepage({
  child,
  streak,
  storiesRead,
  wordsLearned,
  limits,
  upgradeCta,
  curriculumStats,
  childProgress,
}: FreeHomepageProps) {
  const languageCode = child?.language
    ? (typeof child.language === 'string' ? child.language : child.language.code)
    : 'HINDI';
  const languageInfo = SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES] || SUPPORTED_LANGUAGES.HINDI;
  const languageMeta = LANGUAGE_METADATA[languageCode] || LANGUAGE_METADATA.HINDI;

  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="space-y-6"
    >
      {/* Peppi's Playground Header */}
      <motion.div
        variants={fadeInUp}
        className="bg-gradient-to-r from-green-400 via-teal-400 to-cyan-400 rounded-3xl p-6 text-white relative overflow-hidden"
      >
        {/* Floating decorations */}
        <div className="absolute top-2 right-4 text-4xl opacity-40 animate-bounce">
          <span role="img" aria-label="sparkles">&#x2728;</span>
        </div>
        <div className="absolute bottom-2 left-4 text-3xl opacity-40 animate-pulse">
          <span role="img" aria-label="rainbow">&#x1F308;</span>
        </div>

        <div className="flex items-center justify-between relative z-10">
          <div>
            <p className="text-white/80 text-sm">Welcome to</p>
            <h1 className="text-2xl font-bold">Peppi&apos;s Playground</h1>
            <p className="text-white/90 mt-1">
              Hi {child?.name || 'friend'}! Let&apos;s explore {languageInfo?.name}!
            </p>
          </div>
          <div className="text-5xl">
            <span role="img" aria-label="playground">&#x1F3A0;</span>
          </div>
        </div>
      </motion.div>

      {/* Continue Learning Card */}
      {childProgress?.currentProgress && (
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-green-50 to-teal-50 border-2 border-green-200">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center">
                <span className="text-3xl">
                  <span role="img" aria-label="rocket">&#x1F680;</span>
                </span>
              </div>
              <div className="flex-1">
                <p className="text-xs text-green-500 font-medium uppercase tracking-wide">
                  Continue Learning
                </p>
                <h3 className="font-bold text-green-700 text-lg">
                  {childProgress.currentProgress.module?.name || 'Start Your Journey'}
                </h3>
                <p className="text-sm text-green-600">
                  {childProgress.currentProgress.level.name}
                </p>
              </div>
              <Link href={childProgress.currentProgress.continue_url}>
                <button className="bg-green-600 text-white px-5 py-2.5 rounded-full font-bold hover:bg-green-700 transition-all flex items-center gap-2">
                  Start
                  <span>&rarr;</span>
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Upgrade Banner */}
      {upgradeCta && (
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-purple-100 to-pink-100 border-2 border-purple-300">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                <span className="text-2xl">
                  <span role="img" aria-label="star">&#x2B50;</span>
                </span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-purple-700">{upgradeCta.message}</h3>
                <p className="text-sm text-purple-600">
                  Get unlimited content for just {upgradeCta.price}
                </p>
              </div>
              <Link href="/#pricing">
                <button className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-bold hover:shadow-lg transition-all">
                  {upgradeCta.button_text}
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Quick Stats with Limits */}
      <motion.div variants={fadeInUp} className="grid grid-cols-3 gap-3">
        <Card padding="sm" className="text-center bg-orange-50">
          <div className="text-2xl mb-1">
            <span role="img" aria-label="fire">&#x1F525;</span>
          </div>
          <p className="text-2xl font-bold text-orange-600">{streak}</p>
          <p className="text-xs text-gray-500">Day Streak</p>
        </Card>
        <Card padding="sm" className="text-center bg-blue-50">
          <div className="text-2xl mb-1">
            <span role="img" aria-label="book">&#x1F4D6;</span>
          </div>
          <p className="text-2xl font-bold text-blue-600">
            {storiesRead.length}/{limits.story_limit === -1 ? '\u221e' : limits.story_limit}
          </p>
          <p className="text-xs text-gray-500">Stories</p>
        </Card>
        <Card padding="sm" className="text-center bg-green-50">
          <div className="text-2xl mb-1">
            <span role="img" aria-label="games">&#x1F3AE;</span>
          </div>
          <p className="text-2xl font-bold text-green-600">
            0/{limits.games_per_day === -1 ? '\u221e' : limits.games_per_day}
          </p>
          <p className="text-xs text-gray-500">Games Today</p>
        </Card>
      </motion.div>

      {/* Fun Activities - Playground Section */}
      <motion.div variants={fadeInUp}>
        <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
          <span className="text-2xl">
            <span role="img" aria-label="playground">&#x1F3A1;</span>
          </span>
          Fun Activities
        </h2>
        <div className="grid grid-cols-2 gap-3">
          <Link href="/languages/alphabet">
            <Card interactive className="bg-gradient-to-br from-red-100 to-orange-100 border-2 border-orange-200 hover:border-orange-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">{languageMeta.sampleLetter}</div>
                <h3 className="font-bold text-gray-900">Letters</h3>
                <p className="text-xs text-gray-600 mt-1">Learn {languageMeta.scriptName}</p>
                <p className="text-xs text-orange-600 font-medium mt-2">
                  {curriculumStats.letterCount || 0} Letters
                </p>
              </div>
            </Card>
          </Link>

          <Link href="/languages/vocabulary">
            <Card interactive className="bg-gradient-to-br from-blue-100 to-indigo-100 border-2 border-blue-200 hover:border-blue-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="abc">&#x1F524;</span>
                </div>
                <h3 className="font-bold text-gray-900">Words</h3>
                <p className="text-xs text-gray-600 mt-1">Build word bank</p>
                <p className="text-xs text-blue-600 font-medium mt-2">
                  {curriculumStats.wordCount || 0} Words
                </p>
              </div>
            </Card>
          </Link>

          <Link href="/stories">
            <Card interactive className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-200 hover:border-purple-400 transition-all relative">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="books">&#x1F4DA;</span>
                </div>
                <h3 className="font-bold text-gray-900">Stories</h3>
                <p className="text-xs text-gray-600 mt-1">Read & enjoy</p>
                <p className="text-xs text-purple-600 font-medium mt-2">
                  {storiesRead.length}/{limits.story_limit} read
                </p>
              </div>
              {storiesRead.length >= limits.story_limit && (
                <div className="absolute top-2 right-2 bg-orange-500 text-white text-[10px] px-2 py-0.5 rounded-full">
                  Limit reached
                </div>
              )}
            </Card>
          </Link>

          <Link href="/games">
            <Card interactive className="bg-gradient-to-br from-yellow-100 to-amber-100 border-2 border-yellow-200 hover:border-yellow-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="games">&#x1F3AE;</span>
                </div>
                <h3 className="font-bold text-gray-900">Games</h3>
                <p className="text-xs text-gray-600 mt-1">Play & learn</p>
                <p className="text-xs text-yellow-600 font-medium mt-2">
                  {limits.games_per_day}/day limit
                </p>
              </div>
            </Card>
          </Link>
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div variants={fadeInUp}>
        <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
          <span className="text-2xl">
            <span role="img" aria-label="target">&#x1F3AF;</span>
          </span>
          Explore More
        </h2>
        <div className="grid grid-cols-4 gap-3">
          <Link href="/practice/mimic">
            <Card interactive className="text-center py-4 bg-cyan-50">
              <div className="text-3xl mb-1">
                <span role="img" aria-label="microphone">&#x1F3A4;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Mimic</h3>
            </Card>
          </Link>

          <Link href="/festivals">
            <Card interactive className="text-center py-4 bg-red-50">
              <div className="text-3xl mb-1">
                <span role="img" aria-label="diya">&#x1FA94;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Festivals</h3>
            </Card>
          </Link>

          <Link href="/progress">
            <Card interactive className="text-center py-4 bg-amber-50">
              <div className="text-3xl mb-1">
                <span role="img" aria-label="trophy">&#x1F3C6;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Badges</h3>
            </Card>
          </Link>

          <Link href="/challenges">
            <Card interactive className="text-center py-4 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200">
              <div className="text-3xl mb-1">
                <span role="img" aria-label="competition">&#x1F465;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Challenge Friends</h3>
            </Card>
          </Link>

          <Link href="/profile">
            <Card interactive className="text-center py-4 bg-gray-50">
              <div className="text-3xl mb-1">
                <span role="img" aria-label="person">&#x1F464;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Profile</h3>
            </Card>
          </Link>
        </div>
      </motion.div>

      {/* Upgrade CTA at bottom */}
      {upgradeCta && (
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-teal-600 to-cyan-600 text-white">
            <div className="text-center py-4">
              <h3 className="text-xl font-bold mb-2">
                <span role="img" aria-label="rocket">&#x1F680;</span>
                Ready for the full journey?
              </h3>
              <p className="text-white/90 mb-4">
                Unlock all 10 levels, Peppi AI chat, unlimited games & more!
              </p>
              <Link href="/#pricing">
                <button className="bg-white text-teal-600 px-6 py-3 rounded-full font-bold hover:shadow-lg transition-all">
                  Explore Standard Plan - {upgradeCta.price}
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      )}
    </motion.div>
  );
}
