'use client';

import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCw, Trophy, Star, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import PeppiSpeech from '@/components/peppi/PeppiSpeech';
import { shuffleArray } from '@/lib/utils';

interface Word {
  id: string;
  word: string;
  transliteration: string;
  meaning: string;
  audioUrl?: string;
  imageUrl?: string;
}

interface MatchPairsGameProps {
  words: Word[];
  matchType: 'word-meaning' | 'word-image' | 'word-transliteration';
  language?: string;
  timeLimit?: number; // in seconds, 0 for no limit
  onGameComplete: (score: number, totalPairs: number, timeSpent: number) => void;
  onBack?: () => void;
  className?: string;
}

interface MatchItem {
  id: string;
  wordId: string;
  content: string;
  type: 'left' | 'right';
  imageUrl?: string;
}

export function MatchPairsGame({
  words,
  matchType = 'word-meaning',
  timeLimit = 0,
  onGameComplete,
  onBack,
  className,
}: MatchPairsGameProps) {
  const ageConfig = useAgeConfig();
  const [leftItems, setLeftItems] = useState<MatchItem[]>([]);
  const [rightItems, setRightItems] = useState<MatchItem[]>([]);
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const [selectedRight, setSelectedRight] = useState<string | null>(null);
  const [matchedPairs, setMatchedPairs] = useState<Set<string>>(new Set());
  const [incorrectPair, setIncorrectPair] = useState<{ left: string; right: string } | null>(null);
  const [score, setScore] = useState(0);
  const [timeSpent, setTimeSpent] = useState(0);
  const [gameComplete, setGameComplete] = useState(false);
  const [peppiTrigger, setPeppiTrigger] = useState<'welcome' | 'correct' | 'incorrect' | 'lessonComplete' | 'encouragement'>('welcome');

  // Adjust pairs based on age
  const pairsToUse = ageConfig.variant === 'junior' ? 4 : ageConfig.variant === 'standard' ? 6 : 8;

  // Timer
  useEffect(() => {
    if (gameComplete) return;

    const timer = setInterval(() => {
      setTimeSpent((prev) => {
        if (timeLimit > 0 && prev >= timeLimit) {
          setGameComplete(true);
          onGameComplete(score, pairsToUse, prev);
          return prev;
        }
        return prev + 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [gameComplete, timeLimit, score, pairsToUse, onGameComplete]);

  // Initialize game
  useEffect(() => {
    initializeGame();
  }, [words, matchType]);

  const initializeGame = useCallback(() => {
    const selectedWords = shuffleArray(words).slice(0, pairsToUse);

    // Create left items (always the word in Hindi)
    const left: MatchItem[] = selectedWords.map((word) => ({
      id: `${word.id}-left`,
      wordId: word.id,
      content: ageConfig.showHindiScript ? word.word : word.transliteration,
      type: 'left',
    }));

    // Create right items based on match type
    const right: MatchItem[] = selectedWords.map((word) => {
      let content = '';
      let imageUrl: string | undefined;

      switch (matchType) {
        case 'word-meaning':
          content = word.meaning;
          break;
        case 'word-image':
          content = '';
          imageUrl = word.imageUrl;
          break;
        case 'word-transliteration':
          content = word.transliteration;
          break;
      }

      return {
        id: `${word.id}-right`,
        wordId: word.id,
        content,
        type: 'right',
        imageUrl,
      };
    });

    setLeftItems(shuffleArray(left));
    setRightItems(shuffleArray(right));
    setSelectedLeft(null);
    setSelectedRight(null);
    setMatchedPairs(new Set());
    setIncorrectPair(null);
    setScore(0);
    setTimeSpent(0);
    setGameComplete(false);
    setPeppiTrigger('welcome');
  }, [words, matchType, pairsToUse, ageConfig.showHindiScript]);

  const handleLeftSelect = useCallback((id: string) => {
    if (matchedPairs.has(leftItems.find((i) => i.id === id)?.wordId || '')) return;
    setSelectedLeft(id);

    // Check for match if right is already selected
    if (selectedRight) {
      checkMatch(id, selectedRight);
    }
  }, [matchedPairs, leftItems, selectedRight]);

  const handleRightSelect = useCallback((id: string) => {
    if (matchedPairs.has(rightItems.find((i) => i.id === id)?.wordId || '')) return;
    setSelectedRight(id);

    // Check for match if left is already selected
    if (selectedLeft) {
      checkMatch(selectedLeft, id);
    }
  }, [matchedPairs, rightItems, selectedLeft]);

  const checkMatch = useCallback((leftId: string, rightId: string) => {
    const leftItem = leftItems.find((i) => i.id === leftId);
    const rightItem = rightItems.find((i) => i.id === rightId);

    if (!leftItem || !rightItem) return;

    if (leftItem.wordId === rightItem.wordId) {
      // Correct match!
      setMatchedPairs((prev) => new Set(Array.from(prev).concat(leftItem.wordId)));
      setScore((prev) => prev + 10);
      setSelectedLeft(null);
      setSelectedRight(null);
      setPeppiTrigger('correct');

      // Check for game complete
      if (matchedPairs.size + 1 === pairsToUse) {
        setTimeout(() => {
          setGameComplete(true);
          setPeppiTrigger('lessonComplete');
          onGameComplete(score + 10, pairsToUse, timeSpent);
        }, 500);
      }
    } else {
      // Incorrect match
      setIncorrectPair({ left: leftId, right: rightId });
      setScore((prev) => Math.max(0, prev - 2));
      setPeppiTrigger('incorrect');

      setTimeout(() => {
        setIncorrectPair(null);
        setSelectedLeft(null);
        setSelectedRight(null);
      }, 800);
    }
  }, [leftItems, rightItems, matchedPairs, pairsToUse, score, timeSpent, onGameComplete]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getItemStyle = (item: MatchItem, isSelected: boolean, side: 'left' | 'right') => {
    const isMatched = matchedPairs.has(item.wordId);
    const isIncorrect = incorrectPair?.[side] === item.id;

    if (isMatched) return 'bg-green-100 border-green-400 opacity-60';
    if (isIncorrect) return 'bg-red-100 border-red-400 animate-shake';
    if (isSelected) return 'bg-primary-100 border-primary-500 ring-2 ring-primary-300';
    return 'bg-white border-gray-200 hover:border-primary-300';
  };

  return (
    <div className={cn('min-h-screen bg-gradient-to-b from-secondary-50 to-white p-4', className)}>
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-6">
        <div className="flex items-center justify-between">
          {onBack && (
            <button
              onClick={onBack}
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              ← Back
            </button>
          )}

          <h1 className={cn('text-center font-bold text-gray-900', ageConfig.fontSize.heading)}>
            Match Pairs
          </h1>

          <button
            onClick={initializeGame}
            className="flex items-center gap-2 text-primary-600 hover:text-primary-700"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        {/* Stats */}
        <div className="flex justify-center gap-6 mt-4">
          <div className="text-center">
            <p className="text-sm text-gray-500">Score</p>
            <p className={cn('font-bold text-primary-600', ageConfig.fontSize.body)}>
              {score}
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-500">Matched</p>
            <p className={cn('font-bold text-green-600', ageConfig.fontSize.body)}>
              {matchedPairs.size}/{pairsToUse}
            </p>
          </div>
          <div className="text-center flex items-center gap-1">
            <Clock size={16} className="text-gray-400" />
            <p className={cn('font-bold text-gray-700', ageConfig.fontSize.body)}>
              {formatTime(timeSpent)}
            </p>
          </div>
        </div>
      </div>

      {/* Game Area */}
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-2 gap-4 md:gap-8">
          {/* Left Column */}
          <div className="space-y-3">
            <p className={cn('text-center text-gray-500 mb-2', ageConfig.fontSize.small)}>
              {ageConfig.showHindiScript ? 'Hindi' : 'Word'}
            </p>
            {leftItems.map((item) => (
              <motion.button
                key={item.id}
                onClick={() => handleLeftSelect(item.id)}
                disabled={matchedPairs.has(item.wordId)}
                className={cn(
                  'w-full p-4 rounded-xl border-2 transition-all',
                  getItemStyle(item, selectedLeft === item.id, 'left'),
                  ageConfig.fontSize.body
                )}
                whileHover={{ scale: matchedPairs.has(item.wordId) ? 1 : 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <span className="font-semibold">{item.content}</span>
                {matchedPairs.has(item.wordId) && (
                  <Star className="inline-block w-4 h-4 ml-2 text-yellow-500 fill-yellow-400" />
                )}
              </motion.button>
            ))}
          </div>

          {/* Right Column */}
          <div className="space-y-3">
            <p className={cn('text-center text-gray-500 mb-2', ageConfig.fontSize.small)}>
              {matchType === 'word-meaning' ? 'Meaning' : matchType === 'word-image' ? 'Image' : 'Sound'}
            </p>
            {rightItems.map((item) => (
              <motion.button
                key={item.id}
                onClick={() => handleRightSelect(item.id)}
                disabled={matchedPairs.has(item.wordId)}
                className={cn(
                  'w-full p-4 rounded-xl border-2 transition-all',
                  getItemStyle(item, selectedRight === item.id, 'right'),
                  ageConfig.fontSize.body
                )}
                whileHover={{ scale: matchedPairs.has(item.wordId) ? 1 : 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {item.imageUrl ? (
                  <img
                    src={item.imageUrl}
                    alt="Match item"
                    className="w-12 h-12 object-cover rounded-lg mx-auto"
                  />
                ) : (
                  <span className="font-semibold">{item.content}</span>
                )}
                {matchedPairs.has(item.wordId) && (
                  <Star className="inline-block w-4 h-4 ml-2 text-yellow-500 fill-yellow-400" />
                )}
              </motion.button>
            ))}
          </div>
        </div>
      </div>

      {/* Game Complete Overlay */}
      <AnimatePresence>
        {gameComplete && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-3xl p-8 max-w-md mx-4 text-center shadow-2xl"
            >
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 0.5, repeat: 3 }}
              >
                <Trophy className="w-20 h-20 text-yellow-500 mx-auto mb-4" />
              </motion.div>

              <h2 className={cn('font-bold text-gray-900 mb-2', ageConfig.fontSize.heading)}>
                {ageConfig.variant === 'junior' ? 'Amazing!' : 'Well Done!'}
              </h2>

              <div className="space-y-2 mb-6">
                <p className={cn('text-gray-600', ageConfig.fontSize.body)}>
                  Score: <span className="font-bold text-primary-600">{score}</span>
                </p>
                <p className={cn('text-gray-600', ageConfig.fontSize.small)}>
                  Time: {formatTime(timeSpent)}
                </p>
              </div>

              <div className="flex items-center justify-center gap-1 mb-6">
                {[...Array(Math.min(5, Math.ceil(score / 20)))].map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: i * 0.1 }}
                  >
                    <Star className="w-8 h-8 text-yellow-400 fill-yellow-400" />
                  </motion.div>
                ))}
              </div>

              <div className="flex gap-3 justify-center">
                <button
                  onClick={initializeGame}
                  className={cn(
                    'flex items-center gap-2 bg-primary-500 hover:bg-primary-600',
                    'text-white font-semibold rounded-full px-6 py-3 transition-all',
                    ageConfig.fontSize.body
                  )}
                >
                  <RefreshCw size={20} />
                  Play Again
                </button>
                {onBack && (
                  <button
                    onClick={onBack}
                    className={cn(
                      'bg-gray-100 hover:bg-gray-200 text-gray-700',
                      'font-semibold rounded-full px-6 py-3 transition-all',
                      ageConfig.fontSize.body
                    )}
                  >
                    Done
                  </button>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Peppi */}
      <div className="fixed bottom-4 left-4 z-40">
        <PeppiSpeech
          trigger={peppiTrigger}
          size={ageConfig.variant === 'junior' ? 'lg' : 'md'}
        />
      </div>
    </div>
  );
}

export default MatchPairsGame;
