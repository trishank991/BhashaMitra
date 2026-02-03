'use client';

import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCw, Trophy, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import PeppiSpeech from '@/components/peppi/PeppiSpeech';
import { shuffleArray } from '@/lib/utils';

interface Letter {
  id: string;
  letter: string;
  transliteration: string;
  audioUrl?: string;
}

interface LetterMatchGameProps {
  letters: Letter[];
  language?: string;
  onGameComplete: (score: number, totalPairs: number) => void;
  onBack?: () => void;
  className?: string;
}

type CardType = 'letter' | 'transliteration';

interface GameCard {
  id: string;
  letterId: string;
  content: string;
  type: CardType;
  isFlipped: boolean;
  isMatched: boolean;
}

export function LetterMatchGame({
  letters,
  onGameComplete,
  onBack,
  className,
}: LetterMatchGameProps) {
  const ageConfig = useAgeConfig();
  const [cards, setCards] = useState<GameCard[]>([]);
  const [flippedCards, setFlippedCards] = useState<string[]>([]);
  const [matchedPairs, setMatchedPairs] = useState<number>(0);
  const [moves, setMoves] = useState<number>(0);
  const [isChecking, setIsChecking] = useState(false);
  const [gameComplete, setGameComplete] = useState(false);
  const [streak, setStreak] = useState(0);
  const [peppiTrigger, setPeppiTrigger] = useState<'welcome' | 'correct' | 'incorrect' | 'lessonComplete' | 'encouragement'>('welcome');

  // Adjust number of pairs based on age
  const pairsToUse = ageConfig.variant === 'junior' ? 4 : ageConfig.variant === 'standard' ? 6 : 8;

  // Initialize game
  useEffect(() => {
    initializeGame();
  }, [letters]);

  const initializeGame = useCallback(() => {
    const selectedLetters = shuffleArray(letters).slice(0, pairsToUse);

    const gameCards: GameCard[] = [];

    selectedLetters.forEach((letter) => {
      // Card with Hindi letter
      gameCards.push({
        id: `${letter.id}-letter`,
        letterId: letter.id,
        content: letter.letter,
        type: 'letter',
        isFlipped: false,
        isMatched: false,
      });

      // Card with transliteration
      gameCards.push({
        id: `${letter.id}-trans`,
        letterId: letter.id,
        content: letter.transliteration,
        type: 'transliteration',
        isFlipped: false,
        isMatched: false,
      });
    });

    setCards(shuffleArray(gameCards));
    setFlippedCards([]);
    setMatchedPairs(0);
    setMoves(0);
    setGameComplete(false);
    setStreak(0);
    setPeppiTrigger('welcome');
  }, [letters, pairsToUse]);

  const handleCardClick = useCallback((cardId: string) => {
    if (isChecking) return;
    if (flippedCards.length >= 2) return;

    const card = cards.find((c) => c.id === cardId);
    if (!card || card.isFlipped || card.isMatched) return;

    // Flip the card
    setCards((prev) =>
      prev.map((c) => (c.id === cardId ? { ...c, isFlipped: true } : c))
    );

    const newFlippedCards = [...flippedCards, cardId];
    setFlippedCards(newFlippedCards);

    // Check for match when two cards are flipped
    if (newFlippedCards.length === 2) {
      setIsChecking(true);
      setMoves((prev) => prev + 1);

      const [firstId, secondId] = newFlippedCards;
      const firstCard = cards.find((c) => c.id === firstId);
      const secondCard = cards.find((c) => c.id === secondId);

      if (firstCard && secondCard && firstCard.letterId === secondCard.letterId) {
        // Match found!
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              c.letterId === firstCard.letterId ? { ...c, isMatched: true } : c
            )
          );
          setMatchedPairs((prev) => prev + 1);
          setFlippedCards([]);
          setIsChecking(false);
          setStreak((prev) => prev + 1);
          setPeppiTrigger('correct');

          // Check for game complete
          if (matchedPairs + 1 === pairsToUse) {
            setGameComplete(true);
            setPeppiTrigger('lessonComplete');
            onGameComplete(calculateScore(), pairsToUse);
          }
        }, 500);
      } else {
        // No match - flip back
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              newFlippedCards.includes(c.id) ? { ...c, isFlipped: false } : c
            )
          );
          setFlippedCards([]);
          setIsChecking(false);
          setStreak(0);
          setPeppiTrigger('incorrect');
        }, 1000);
      }
    }
  }, [cards, flippedCards, isChecking, matchedPairs, pairsToUse, onGameComplete]);

  const calculateScore = () => {
    // Score based on efficiency (fewer moves = higher score)
    const perfectMoves = pairsToUse;
    const efficiency = Math.max(0, 100 - (moves - perfectMoves) * 5);
    return Math.round(efficiency);
  };

  const gridCols = ageConfig.variant === 'junior' ? 'grid-cols-2 sm:grid-cols-4' : 'grid-cols-3 sm:grid-cols-4';

  return (
    <div className={cn('min-h-screen bg-gradient-to-b from-primary-50 to-white p-4', className)}>
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
            Letter Match
          </h1>

          <button
            onClick={initializeGame}
            className="flex items-center gap-2 text-primary-600 hover:text-primary-700"
          >
            <RefreshCw size={20} />
            <span className="hidden sm:inline">Restart</span>
          </button>
        </div>

        {/* Stats */}
        <div className="flex justify-center gap-6 mt-4">
          <div className="text-center">
            <p className="text-sm text-gray-500">Pairs</p>
            <p className={cn('font-bold text-primary-600', ageConfig.fontSize.body)}>
              {matchedPairs}/{pairsToUse}
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-500">Moves</p>
            <p className={cn('font-bold text-gray-700', ageConfig.fontSize.body)}>
              {moves}
            </p>
          </div>
          {streak > 1 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="text-center"
            >
              <p className="text-sm text-gray-500">Streak</p>
              <p className={cn('font-bold text-orange-500', ageConfig.fontSize.body)}>
                🔥 {streak}
              </p>
            </motion.div>
          )}
        </div>
      </div>

      {/* Game Grid */}
      <div className="max-w-3xl mx-auto">
        <div className={cn('grid gap-3', gridCols)}>
          {cards.map((card) => (
            <motion.div
              key={card.id}
              className="aspect-square"
              whileHover={{ scale: card.isMatched ? 1 : 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div
                onClick={() => handleCardClick(card.id)}
                className={cn(
                  'w-full h-full rounded-2xl cursor-pointer transition-all duration-300',
                  'flex items-center justify-center shadow-md',
                  card.isMatched
                    ? 'bg-green-100 border-2 border-green-400'
                    : card.isFlipped
                    ? 'bg-white border-2 border-primary-400'
                    : 'bg-gradient-to-br from-primary-400 to-primary-600',
                )}
              >
                <AnimatePresence mode="wait">
                  {card.isFlipped || card.isMatched ? (
                    <motion.div
                      key="front"
                      initial={{ rotateY: -90, opacity: 0 }}
                      animate={{ rotateY: 0, opacity: 1 }}
                      exit={{ rotateY: 90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="text-center"
                    >
                      <p
                        className={cn(
                          'font-bold',
                          card.type === 'letter' ? ageConfig.fontSize.heading : ageConfig.fontSize.body,
                          card.isMatched ? 'text-green-700' : 'text-gray-900'
                        )}
                      >
                        {card.content}
                      </p>
                      {card.isMatched && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="mt-1"
                        >
                          <Star className="w-5 h-5 text-yellow-500 mx-auto fill-yellow-400" />
                        </motion.div>
                      )}
                    </motion.div>
                  ) : (
                    <motion.div
                      key="back"
                      initial={{ rotateY: 90, opacity: 0 }}
                      animate={{ rotateY: 0, opacity: 1 }}
                      exit={{ rotateY: -90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <span className="text-4xl text-white/80">?</span>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          ))}
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
                {ageConfig.variant === 'junior' ? 'Yay! You Did It!' : 'Great Job!'}
              </h2>

              <p className={cn('text-gray-600 mb-4', ageConfig.fontSize.body)}>
                You matched all {pairsToUse} pairs in {moves} moves!
              </p>

              <div className="flex items-center justify-center gap-1 mb-6">
                {[...Array(Math.min(5, Math.ceil(calculateScore() / 20)))].map((_, i) => (
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

export default LetterMatchGame;
