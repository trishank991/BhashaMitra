'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, Button, Badge, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { api } from '@/lib/api';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { GAME_WIN_XP } from '@/lib/constants';

// Sample word pairs for the game
const wordPairs = [
  { id: '1', hindi: 'किताब', english: 'Book', hint: '📚' },
  { id: '2', hindi: 'पानी', english: 'Water', hint: '💧' },
  { id: '3', hindi: 'खाना', english: 'Food', hint: '🍽️' },
  { id: '4', hindi: 'घर', english: 'Home', hint: '🏠' },
  { id: '5', hindi: 'स्कूल', english: 'School', hint: '🏫' },
  { id: '6', hindi: 'पेड़', english: 'Tree', hint: '🌳' },
];

interface CardData {
  id: string;
  word: string;
  type: 'hindi' | 'english';
  pairId: string;
  isFlipped: boolean;
  isMatched: boolean;
}

type GameState = 'start' | 'playing' | 'completed';

// Card flip animation variants
const cardFlipVariants = {
  initial: { rotateY: 0 },
  flipped: { rotateY: 180, transition: { duration: 0.3 } },
  matched: { 
    rotateY: 180, 
    scale: 1.05,
    transition: { duration: 0.2 }
  },
};

export default function WordMatchPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [isHydrated, setIsHydrated] = useState(false);
  const [gameState, setGameState] = useState<GameState>('start');
  const [cards, setCards] = useState<CardData[]>([]);
  const [selectedCards, setSelectedCards] = useState<string[]>([]);
  const [attempts, setAttempts] = useState(0);
  const [matches, setMatches] = useState(0);
  const [isChecking, setIsChecking] = useState(false);
  const [xpEarned, setXpEarned] = useState(0);
  const [isAwardingXP, setIsAwardingXP] = useState(false);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  const shuffleArray = useCallback(<T,>(array: T[]): T[] => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }, []);

  const initializeGame = useCallback(() => {
    const cardPairs: CardData[] = [];

    wordPairs.forEach((pair) => {
      cardPairs.push({
        id: `hindi-${pair.id}`,
        word: pair.hindi,
        type: 'hindi',
        pairId: pair.id,
        isFlipped: false,
        isMatched: false,
      });
      cardPairs.push({
        id: `english-${pair.id}`,
        word: pair.english,
        type: 'english',
        pairId: pair.id,
        isFlipped: false,
        isMatched: false,
      });
    });

    setCards(shuffleArray(cardPairs));
    setSelectedCards([]);
    setAttempts(0);
    setMatches(0);
    setXpEarned(0);
    setGameState('playing');
  }, [shuffleArray]);

  const handleCardClick = (cardId: string) => {
    if (isChecking) return;

    const card = cards.find((c) => c.id === cardId);
    if (!card || card.isFlipped || card.isMatched) return;

    // Flip the card
    setCards((prev) =>
      prev.map((c) => (c.id === cardId ? { ...c, isFlipped: true } : c))
    );
    setSelectedCards((prev) => [...prev, cardId]);

    // If two cards are selected, check for match
    if (selectedCards.length === 1) {
      setIsChecking(true);
      setAttempts((prev) => prev + 1);

      const firstCard = cards.find((c) => c.id === selectedCards[0]);
      const secondCard = cards.find((c) => c.id === cardId);

      if (firstCard && secondCard && firstCard.pairId === secondCard.pairId) {
        // Match found
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              c.id === selectedCards[0] || c.id === cardId
                ? { ...c, isMatched: true }
                : c
            )
          );
          setMatches((prev) => prev + 1);
          setSelectedCards([]);
          setIsChecking(false);
        }, 500);
      } else {
        // No match - flip back after delay
        setTimeout(() => {
          setCards((prev) =>
            prev.map((c) =>
              c.id === selectedCards[0] || c.id === cardId
                ? { ...c, isFlipped: false }
                : c
            )
          );
          setSelectedCards([]);
          setIsChecking(false);
        }, 1000);
      }
    }
  };

  useEffect(() => {
    if (matches === wordPairs.length && gameState === 'playing') {
      // Game completed
      const xp = GAME_WIN_XP;
      setXpEarned(xp);
      setGameState('completed');

      // Award XP via API
      const awardXP = async () => {
        setIsAwardingXP(true);
        try {
          await api.awardXP(xp, 'word_match_game');
        } catch (error) {
          console.error('Failed to award XP:', error);
        } finally {
          setIsAwardingXP(false);
        }
      };

      awardXP();
    }
  }, [matches, gameState]);

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
    <MainLayout headerTitle="Word Match" showBack={true} showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Start Screen */}
        {gameState === 'start' && (
          <motion.div variants={fadeInUp} className="text-center space-y-6">
            <Card className="bg-gradient-to-r from-secondary-500 to-accent-500 text-white py-8">
              <span className="text-6xl mb-4 block">🎯</span>
              <h2 className="text-2xl font-bold">Word Match</h2>
              <p className="text-sm opacity-90 mt-2">
                Match Hindi words with their English meanings!
              </p>
            </Card>

            <Card className="text-center py-6">
              <h3 className="font-bold text-gray-900 mb-2">How to Play</h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>1. Click on a card to flip it</li>
                <li>2. Find the matching word pair</li>
                <li>3. Match all pairs to win!</li>
              </ul>
              <Badge variant="success" className="mt-4">
                +{GAME_WIN_XP} XP on completion
              </Badge>
            </Card>

            <Button onClick={initializeGame} size="lg" className="w-full">
              Start Playing 🎮
            </Button>
          </motion.div>
        )}

        {/* Game Screen */}
        {gameState === 'playing' && (
          <motion.div variants={fadeInUp} className="space-y-4">
            {/* Stats */}
            <div className="flex justify-between items-center">
              <Badge variant="primary">
                Matches: {matches}/{wordPairs.length}
              </Badge>
              <Badge variant="neutral">Attempts: {attempts}</Badge>
            </div>

            {/* Cards Grid */}
            <div className="grid grid-cols-3 gap-3">
              {cards.map((card) => (
                <motion.div
                  key={card.id}
                  initial="initial"
                  animate={
                    card.isFlipped || card.isMatched
                      ? 'flipped'
                      : 'initial'
                  }
                  variants={cardFlipVariants}
                  onClick={() => handleCardClick(card.id)}
                  className="aspect-square cursor-pointer"
                  style={{ perspective: '1000px' }}
                >
                  <div
                    className={`w-full h-full relative preserve-3d transition-all duration-500 ${
                      card.isFlipped || card.isMatched ? 'rotate-y-180' : ''
                    }`}
                  >
                    {/* Card Back */}
                    <div
                      className={`absolute inset-0 backface-hidden rounded-2xl flex items-center justify-center shadow-soft ${
                        card.isMatched
                          ? 'bg-success-100'
                          : 'bg-gradient-to-br from-primary-400 to-primary-600'
                      }`}
                    >
                      <span className="text-3xl">❓</span>
                    </div>

                    {/* Card Front */}
                    <div
                      className={`absolute inset-0 backface-hidden rotate-y-180 rounded-2xl flex flex-col items-center justify-center shadow-card ${
                        card.isMatched
                          ? 'bg-success-50 border-2 border-success-200'
                          : 'bg-white'
                      }`}
                    >
                      <span className="text-2xl">{wordPairs.find(p => p.id === card.pairId)?.hint}</span>
                      <span
                        className={`text-lg font-bold mt-1 ${
                          card.type === 'hindi'
                            ? 'text-primary-700'
                            : 'text-gray-800'
                        }`}
                      >
                        {card.word}
                      </span>
                      {card.isMatched && (
                        <span className="text-success-600 text-sm">✓</span>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Completion Screen */}
        {gameState === 'completed' && (
          <motion.div variants={fadeInUp} className="text-center space-y-6">
            <Card className="bg-gradient-to-r from-success-400 to-success-600 text-white py-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                className="text-6xl mb-4"
              >
                🎉
              </motion.div>
              <h2 className="text-2xl font-bold">Congratulations!</h2>
              <p className="text-sm opacity-90 mt-2">
                You matched all the words!
              </p>
            </Card>

            <Card className="text-center py-6">
              <h3 className="font-bold text-gray-900 mb-4">Your Results</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Total Attempts</span>
                  <span className="font-bold">{attempts}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Pairs Matched</span>
                  <span className="font-bold">{wordPairs.length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Accuracy</span>
                  <span className="font-bold text-success-600">
                    {attempts > 0 ? Math.round((wordPairs.length / attempts) * 100) : 100}%
                  </span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-100">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3, type: 'spring' }}
                  className="inline-flex items-center gap-2 bg-warning-50 px-4 py-2 rounded-full"
                >
                  <span className="text-2xl">⭐</span>
                  <span className="font-bold text-warning-600">
                    {isAwardingXP ? 'Awarding...' : `+${xpEarned} XP Earned!`}
                  </span>
                </motion.div>
              </div>
            </Card>

            <div className="space-y-3">
              <Button onClick={initializeGame} size="lg" className="w-full">
                Play Again 🔄
              </Button>
              <Button
                onClick={() => router.push('/games')}
                variant="outline"
                size="lg"
                className="w-full"
              >
                Back to Games
              </Button>
            </div>
          </motion.div>
        )}
      </motion.div>
    </MainLayout>
  );
}
