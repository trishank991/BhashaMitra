'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Card, Badge } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES, LEVEL_TITLES, XP_PER_LEVEL } from '@/lib/constants';
import { ChildProfile } from '@/types';
import { SubscriptionFeatures, SubscriptionLimits } from '@/lib/api';
import { ChildProgress } from '@/hooks/useSubscription';

interface PaidHomepageProps {
  child: ChildProfile | null;
  tier: 'STANDARD' | 'PREMIUM';
  streak: number;
  storiesRead: string[];
  wordsLearned: string[];
  features: SubscriptionFeatures;
  limits: SubscriptionLimits;
  childProgress: ChildProgress | null;
  curriculumStats: {
    letterCount: number;
    wordCount: number;
    topicCount: number;
    storyCount: number;
  };
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

export function PaidHomepage({
  child,
  tier,
  streak,
  storiesRead,
  wordsLearned,
  features,
  limits,
  childProgress,
  curriculumStats,
}: PaidHomepageProps) {
  const languageCode = child?.language
    ? (typeof child.language === 'string' ? child.language : child.language.code)
    : 'HINDI';
  const languageInfo = SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES] || SUPPORTED_LANGUAGES.HINDI;
  const languageMeta = LANGUAGE_METADATA[languageCode] || LANGUAGE_METADATA.HINDI;

  const isPremium = tier === 'PREMIUM';

  // Get level from child profile or use default
  const currentLevel = child?.level || 1;
  const levelTitle = LEVEL_TITLES[currentLevel] || `Level ${currentLevel}`;
  const xpForNextLevel = XP_PER_LEVEL * currentLevel;
  const currentXp = childProgress?.summary.total_points || 0;
  const xpProgress = Math.min((currentXp / xpForNextLevel) * 100, 100);

  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="space-y-6"
    >
      {/* Peppi's Classroom Header */}
      <motion.div
        variants={fadeInUp}
        className={`rounded-3xl p-6 text-white relative overflow-hidden ${
          isPremium
            ? 'bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500'
            : 'bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500'
        }`}
      >
        {/* Floating decorations */}
        <div className="absolute top-2 right-4 text-3xl opacity-40 animate-pulse">
          <span role="img" aria-label="star">{isPremium ? '\u{1F451}' : '\u2B50'}</span>
        </div>
        <div className="absolute bottom-2 left-4 text-2xl opacity-40">
          <span role="img" aria-label="book">&#x1F4DA;</span>
        </div>

        <div className="flex items-center justify-between relative z-10">
          <div>
            <div className="flex items-center gap-2">
              <p className="text-white/80 text-sm">Welcome to</p>
              {isPremium && (
                <Badge className="bg-yellow-400/20 text-yellow-200 text-xs">
                  <span role="img" aria-label="crown">&#x1F451;</span> Premium
                </Badge>
              )}
            </div>
            <h1 className="text-2xl font-bold">Peppi&apos;s Classroom</h1>
            <p className="text-white/90 mt-1">
              Ready for today&apos;s lesson, {child?.name || 'friend'}?
            </p>

            {/* Level Display with Progress */}
            <div className="mt-3 flex items-center gap-3">
              <div className="bg-white/20 rounded-full px-3 py-1">
                <span className="text-sm font-medium">Level {currentLevel}</span>
              </div>
              <div className="flex-1">
                <div className="flex justify-between text-xs text-white/80 mb-1">
                  <span>{levelTitle}</span>
                  <span>{currentXp} / {xpForNextLevel} XP</span>
                </div>
                <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-yellow-400 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${xpProgress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="text-5xl">
            <span role="img" aria-label="school">&#x1F3EB;</span>
          </div>
        </div>
      </motion.div>

      {/* Current Progress Card - Curriculum Journey */}
      {childProgress?.currentProgress && (
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-200">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-indigo-100 rounded-2xl flex items-center justify-center">
                <span className="text-3xl">
                  <span role="img" aria-label="journey">&#x1F6E4;&#xFE0F;</span>
                </span>
              </div>
              <div className="flex-1">
                <p className="text-xs text-indigo-500 font-medium uppercase tracking-wide">
                  Your Learning Journey
                </p>
                <h3 className="font-bold text-indigo-700 text-lg">
                  {childProgress.currentProgress.level.name}
                </h3>
                {childProgress.currentProgress.module && (
                  <p className="text-sm text-indigo-600">
                    {childProgress.currentProgress.module.name}
                    {childProgress.currentProgress.lesson && (
                      <span className="text-indigo-400"> &rarr; {childProgress.currentProgress.lesson.title}</span>
                    )}
                  </p>
                )}
              </div>
              <Link href={childProgress.currentProgress.continue_url}>
                <button className="bg-indigo-600 text-white px-5 py-2.5 rounded-full font-bold hover:bg-indigo-700 transition-all flex items-center gap-2">
                  Continue
                  <span>&rarr;</span>
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Quick Stats */}
      <motion.div variants={fadeInUp} className="grid grid-cols-4 gap-3">
        <Card padding="sm" className="text-center bg-orange-50">
          <div className="text-xl mb-1">
            <span role="img" aria-label="fire">&#x1F525;</span>
          </div>
          <p className="text-xl font-bold text-orange-600">{streak}</p>
          <p className="text-xs text-gray-500">Streak</p>
        </Card>
        <Card padding="sm" className="text-center bg-purple-50">
          <div className="text-xl mb-1">
            <span role="img" aria-label="trophy">&#x1F3C6;</span>
          </div>
          <p className="text-xl font-bold text-purple-600">
            {childProgress?.summary.levels_completed || 0}
          </p>
          <p className="text-xs text-gray-500">Levels</p>
        </Card>
        <Card padding="sm" className="text-center bg-blue-50">
          <div className="text-xl mb-1">
            <span role="img" aria-label="star">&#x2B50;</span>
          </div>
          <p className="text-xl font-bold text-blue-600">
            {childProgress?.summary.total_points || 0}
          </p>
          <p className="text-xs text-gray-500">Points</p>
        </Card>
        <Card padding="sm" className="text-center bg-green-50">
          <div className="text-xl mb-1">
            <span role="img" aria-label="book">&#x1F4D6;</span>
          </div>
          <p className="text-xl font-bold text-green-600">{storiesRead.length}</p>
          <p className="text-xs text-gray-500">Stories</p>
        </Card>
      </motion.div>

      {/* Curriculum Journey */}
      <motion.div variants={fadeInUp}>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span className="text-2xl">
              <span role="img" aria-label="books">&#x1F4DA;</span>
            </span>
            Learning Path
          </h2>
          <Link href="/languages/levels" className="text-sm text-indigo-600 font-medium">
            View All Levels &rarr;
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <Link href="/languages/levels">
            <Card interactive className="bg-gradient-to-br from-indigo-100 to-purple-100 border-2 border-indigo-200 hover:border-indigo-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="journey">&#x1F6E4;&#xFE0F;</span>
                </div>
                <h3 className="font-bold text-gray-900">L1-L10 Journey</h3>
                <p className="text-xs text-gray-600 mt-1">Structured curriculum</p>
                <p className="text-xs text-indigo-600 font-medium mt-2">
                  Level {childProgress?.summary.levels_completed || 0 + 1}
                </p>
              </div>
            </Card>
          </Link>

          <Link href="/languages/songs">
            <Card interactive className="bg-gradient-to-br from-pink-100 to-rose-100 border-2 border-pink-200 hover:border-pink-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="music">&#x1F3B5;</span>
                </div>
                <h3 className="font-bold text-gray-900">Songs</h3>
                <p className="text-xs text-gray-600 mt-1">Learn with music</p>
                <p className="text-xs text-pink-600 font-medium mt-2">
                  Hindi rhymes
                </p>
              </div>
            </Card>
          </Link>
        </div>
      </motion.div>

      {/* Study Materials */}
      <motion.div variants={fadeInUp}>
        <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
          <span className="text-2xl">
            <span role="img" aria-label="pencil">&#x270F;&#xFE0F;</span>
          </span>
          Study Materials
        </h2>
        <div className="grid grid-cols-2 gap-3">
          <Link href="/languages/alphabet">
            <Card interactive className="bg-gradient-to-br from-red-100 to-orange-100 border-2 border-orange-200 hover:border-orange-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">{languageMeta.sampleLetter}</div>
                <h3 className="font-bold text-gray-900">Alphabet</h3>
                <p className="text-xs text-gray-600 mt-1">{languageMeta.scriptName}</p>
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
                  <span role="img" aria-label="word">&#x1F4D6;</span>
                </div>
                <h3 className="font-bold text-gray-900">Vocabulary</h3>
                <p className="text-xs text-gray-600 mt-1">Build word bank</p>
                <p className="text-xs text-blue-600 font-medium mt-2">
                  {curriculumStats.wordCount || 0} Words
                </p>
              </div>
            </Card>
          </Link>

          <Link href="/languages/grammar">
            <Card interactive className="bg-gradient-to-br from-green-100 to-teal-100 border-2 border-green-200 hover:border-green-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="pencil">&#x1F4DD;</span>
                </div>
                <h3 className="font-bold text-gray-900">Grammar</h3>
                <p className="text-xs text-gray-600 mt-1">Learn rules</p>
                <p className="text-xs text-green-600 font-medium mt-2">
                  {curriculumStats.topicCount || 0} Topics
                </p>
              </div>
            </Card>
          </Link>

          <Link href="/stories">
            <Card interactive className="bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-200 hover:border-purple-400 transition-all">
              <div className="text-center py-4">
                <div className="text-4xl mb-2">
                  <span role="img" aria-label="books">&#x1F4DA;</span>
                </div>
                <h3 className="font-bold text-gray-900">Stories</h3>
                <p className="text-xs text-gray-600 mt-1">With Peppi narration</p>
                <p className="text-xs text-purple-600 font-medium mt-2">
                  Unlimited access
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
          Quick Actions
        </h2>
        <div className="grid grid-cols-5 gap-3">
          <Link href="/practice/mimic">
            <Card interactive className="text-center py-4 bg-cyan-50">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="microphone">&#x1F3A4;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Mimic</h3>
            </Card>
          </Link>

          <Link href="/games">
            <Card interactive className="text-center py-4 bg-yellow-50">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="games">&#x1F3AE;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Games</h3>
            </Card>
          </Link>

          <Link href="/festivals">
            <Card interactive className="text-center py-4 bg-red-50">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="diya">&#x1FA94;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Festivals</h3>
            </Card>
          </Link>

          <Link href="/progress">
            <Card interactive className="text-center py-4 bg-amber-50">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="trophy">&#x1F3C6;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Badges</h3>
            </Card>
          </Link>

          <Link href="/challenges">
            <Card interactive className="text-center py-4 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="competition">&#x1F465;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Challenge Friends</h3>
            </Card>
          </Link>

          <Link href="/profile">
            <Card interactive className="text-center py-4 bg-gray-50">
              <div className="text-2xl mb-1">
                <span role="img" aria-label="person">&#x1F464;</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-xs">Profile</h3>
            </Card>
          </Link>
        </div>
      </motion.div>

      {/* Live Classes Banner (Premium Only) */}
      {isPremium && features.has_live_classes && (
        <motion.div variants={fadeInUp}>
          <Card className="bg-gradient-to-r from-purple-600 to-pink-600 text-white">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center">
                <span className="text-3xl">
                  <span role="img" aria-label="video">&#x1F4F9;</span>
                </span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-lg">Live Classes</h3>
                <p className="text-white/90 text-sm">
                  {limits.free_live_classes} free classes this month
                </p>
              </div>
              <Link href="/live-classes">
                <button className="bg-white text-purple-600 px-4 py-2 rounded-full font-bold hover:shadow-lg transition-all">
                  Book Now
                </button>
              </Link>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Daily Goal */}
      <motion.div variants={fadeInUp}>
        <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-2xl">
                <span role="img" aria-label="target">&#x1F3AF;</span>
              </span>
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-green-700">Daily Goal</h3>
              <p className="text-sm text-green-600">
                Complete 1 lesson and read 1 story
              </p>
            </div>
            <Badge variant="success">In Progress</Badge>
          </div>
        </Card>
      </motion.div>
    </motion.div>
  );
}
