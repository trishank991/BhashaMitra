'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button, Badge, SpeakerButton } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { useAudio } from '@/hooks/useAudio';
import api, { GameWord } from '@/lib/api';

// Game data - descriptions update based on language
const getGamesData = (languageName: string) => ({
  'word-match': {
    name: 'Word Match',
    icon: '🎯',
    description: `Match ${languageName} words with their English meanings`,
    xpReward: 25,
  },
  'listen-speak': {
    name: 'Listen & Speak',
    icon: '🎤',
    description: `Practice ${languageName} pronunciation by listening and speaking`,
    xpReward: 30,
  },
});

// Fallback words for each language (used when API fails)
const FALLBACK_WORDS: Record<string, GameWord[]> = {
  HINDI: [
    { word: 'माँ', english: 'mother', romanized: 'maa' },
    { word: 'पिता', english: 'father', romanized: 'pita' },
    { word: 'लाल', english: 'red', romanized: 'laal' },
    { word: 'नीला', english: 'blue', romanized: 'neela' },
    { word: 'पानी', english: 'water', romanized: 'paani' },
    { word: 'खाना', english: 'food', romanized: 'khaana' },
  ],
  TAMIL: [
    { word: 'அம்மா', english: 'mother', romanized: 'amma' },
    { word: 'அப்பா', english: 'father', romanized: 'appa' },
    { word: 'சிவப்பு', english: 'red', romanized: 'sivappu' },
    { word: 'நீலம்', english: 'blue', romanized: 'neelam' },
    { word: 'தண்ணீர்', english: 'water', romanized: 'thanneer' },
    { word: 'உணவு', english: 'food', romanized: 'unavu' },
  ],
  TELUGU: [
    { word: 'అమ్మ', english: 'mother', romanized: 'amma' },
    { word: 'నాన్న', english: 'father', romanized: 'naanna' },
    { word: 'ఎరుపు', english: 'red', romanized: 'erupu' },
    { word: 'నీలం', english: 'blue', romanized: 'neelam' },
    { word: 'నీళ్ళు', english: 'water', romanized: 'neellu' },
    { word: 'ఆహారం', english: 'food', romanized: 'aaharam' },
  ],
  GUJARATI: [
    { word: 'મા', english: 'mother', romanized: 'maa' },
    { word: 'પિતા', english: 'father', romanized: 'pita' },
    { word: 'લાલ', english: 'red', romanized: 'laal' },
    { word: 'વાદળી', english: 'blue', romanized: 'vaadli' },
    { word: 'પાણી', english: 'water', romanized: 'paani' },
    { word: 'ખોરાક', english: 'food', romanized: 'khoraak' },
  ],
};

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Word Match Game Component
function WordMatchGame({
  onComplete,
  gameWords,
  language,
  languageName
}: {
  onComplete: (score: number) => void;
  gameWords: GameWord[];
  language: string;
  languageName: string;
}) {
  const [words] = useState(() => shuffleArray(gameWords).slice(0, 4));
  const [shuffledEnglish] = useState(() => shuffleArray(words.map(w => w.english)));
  const [selectedWord, setSelectedWord] = useState<number | null>(null);
  const [matches, setMatches] = useState<Record<number, number>>({});
  const [score, setScore] = useState(0);
  const [wrongMatch, setWrongMatch] = useState<number | null>(null);

  // Audio hook for kid-friendly voice - uses the child's language
  const { isPlaying, isLoading, playAudio } = useAudio({
    language: language,
    voiceStyle: 'enthusiastic', // Use enthusiastic voice for games
  });

  const handleWordClick = (index: number) => {
    if (matches[index] !== undefined) return;
    setSelectedWord(index);
    setWrongMatch(null);
  };

  const handleEnglishClick = (englishIndex: number) => {
    if (selectedWord === null) return;

    const correctEnglish = words[selectedWord].english;
    const selectedEnglishWord = shuffledEnglish[englishIndex];

    if (correctEnglish === selectedEnglishWord) {
      setMatches(prev => ({ ...prev, [selectedWord]: englishIndex }));
      setScore(prev => prev + 1);
      setSelectedWord(null);

      if (Object.keys(matches).length + 1 === words.length) {
        setTimeout(() => onComplete(score + 1), 500);
      }
    } else {
      setWrongMatch(englishIndex);
      setTimeout(() => {
        setWrongMatch(null);
        setSelectedWord(null);
      }, 500);
    }
  };

  const matchedEnglishIndices = Object.values(matches);

  return (
    <div className="space-y-6">
      <div className="text-center mb-4">
        <Badge variant="primary" size="lg">Score: {score}/{words.length}</Badge>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Language words */}
        <div className="space-y-3">
          <p className="text-sm font-medium text-gray-500 text-center">{languageName}</p>
          {words.map((word, index) => (
            <motion.div
              key={index}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleWordClick(index)}
            >
              <Card
                className={`text-center h-20 flex flex-col items-center justify-center cursor-pointer transition-all relative ${
                  matches[index] !== undefined
                    ? 'bg-green-100 border-green-500'
                    : selectedWord === index
                    ? 'bg-blue-100 border-blue-500 ring-2 ring-blue-300'
                    : 'hover:bg-gray-50'
                }`}
              >
                {/* Speaker button */}
                <div className="absolute top-1 right-1">
                  <SpeakerButton
                    size="sm"
                    isPlaying={isPlaying}
                    isLoading={isLoading}
                    onClick={() => playAudio(word.word)}
                  />
                </div>
                <p className="text-2xl font-bold">{word.word}</p>
                <p className="text-xs text-gray-400 mt-1">{word.romanized}</p>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* English words */}
        <div className="space-y-3">
          <p className="text-sm font-medium text-gray-500 text-center">English</p>
          {shuffledEnglish.map((english, index) => (
            <motion.div
              key={index}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleEnglishClick(index)}
            >
              <Card
                className={`text-center h-20 flex flex-col items-center justify-center cursor-pointer transition-all ${
                  matchedEnglishIndices.includes(index)
                    ? 'bg-green-100 border-green-500'
                    : wrongMatch === index
                    ? 'bg-red-100 border-red-500'
                    : 'hover:bg-gray-50'
                }`}
              >
                <p className="text-lg font-medium">{english}</p>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      <p className="text-center text-sm text-gray-500">
        Tap a {languageName} word, then tap its English meaning
      </p>
    </div>
  );
}

// Listen & Speak Game Component
function ListenSpeakGame({
  onComplete,
  gameWords,
  language,
  languageName
}: {
  onComplete: (score: number) => void;
  gameWords: GameWord[];
  language: string;
  languageName: string;
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [score, setScore] = useState(0);
  const [words] = useState(() => shuffleArray(gameWords).slice(0, 4));

  // Audio hook for kid-friendly voice - uses the child's language
  const { isPlaying, isLoading, playAudio } = useAudio({
    language: language,
    voiceStyle: 'kid_friendly', // Use kid_friendly voice for pronunciation
  });

  const currentWord = words[currentIndex];

  // Play pronunciation when the card loads
  const handlePlayPronunciation = () => {
    playAudio(currentWord.word);
  };

  const handleCorrect = () => {
    setScore(prev => prev + 1);
    handleNext();
  };

  const handleNext = () => {
    if (currentIndex + 1 >= words.length) {
      onComplete(score + 1);
    } else {
      setCurrentIndex(prev => prev + 1);
      setShowAnswer(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-4">
        <Badge variant="primary" size="lg">
          Word {currentIndex + 1}/{words.length} | Score: {score}
        </Badge>
      </div>

      <Card className="text-center py-8 bg-gradient-to-br from-purple-50 to-pink-50">
        {/* Large speaker button for pronunciation */}
        <div className="flex justify-center mb-4">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handlePlayPronunciation}
            disabled={isLoading}
            className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 text-white shadow-lg flex items-center justify-center"
          >
            {isLoading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="w-8 h-8 border-3 border-white border-t-transparent rounded-full"
              />
            ) : isPlaying ? (
              <div className="flex items-center gap-1">
                {[1, 2, 3, 4].map((bar) => (
                  <motion.div
                    key={bar}
                    animate={{ height: ['30%', '100%', '30%'] }}
                    transition={{ duration: 0.4, repeat: Infinity, delay: bar * 0.1 }}
                    className="w-1.5 bg-white rounded-full"
                    style={{ minHeight: '6px' }}
                  />
                ))}
              </div>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-10 h-10">
                <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.318.664-2.66 1.905A9.76 9.76 0 0 0 1.5 12c0 .898.121 1.768.35 2.595.341 1.24 1.518 1.905 2.659 1.905h1.93l4.5 4.5c.945.945 2.561.276 2.561-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 0 1-1.06-1.06 8.25 8.25 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z" />
                <path d="M15.932 7.757a.75.75 0 0 1 1.061 0 6 6 0 0 1 0 8.486.75.75 0 0 1-1.06-1.061 4.5 4.5 0 0 0 0-6.364.75.75 0 0 1 0-1.06Z" />
              </svg>
            )}
          </motion.button>
        </div>
        <p className="text-xs text-purple-500 mb-3">Tap to listen!</p>

        <p className="text-5xl font-bold text-gray-900 mb-2">{currentWord.word}</p>
        <p className="text-lg text-purple-600">{currentWord.romanized}</p>

        {showAnswer && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-white rounded-xl"
          >
            <p className="text-gray-600">Meaning:</p>
            <p className="text-xl font-bold text-gray-900">{currentWord.english}</p>
          </motion.div>
        )}
      </Card>

      <div className="space-y-3">
        <p className="text-center text-sm text-gray-500">
          Try to pronounce the word, then check if you were right!
        </p>

        {!showAnswer ? (
          <Button
            onClick={() => setShowAnswer(true)}
            className="w-full bg-purple-500 hover:bg-purple-600"
          >
            Show Answer
          </Button>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            <Button
              onClick={handleCorrect}
              className="bg-green-500 hover:bg-green-600"
            >
              I Got It Right!
            </Button>
            <Button
              onClick={handleNext}
              variant="outline"
            >
              Try Again Later
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GameDetailPage() {
  const router = useRouter();
  const params = useParams();
  const gameId = params.id as string;

  const [isHydrated, setIsHydrated] = useState(false);
  const [gameState, setGameState] = useState<'intro' | 'playing' | 'complete'>('intro');
  const [finalScore, setFinalScore] = useState(0);
  const [gameWords, setGameWords] = useState<GameWord[]>([]);
  const [isLoadingWords, setIsLoadingWords] = useState(true);
  const { isAuthenticated, activeChild } = useAuthStore();

  // Get language code - handle both string and object formats
  const languageCode = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  const languageInfo = SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES] || SUPPORTED_LANGUAGES.HINDI;
  const languageName = languageInfo?.name || 'Hindi';

  // Get game data with language-specific description
  const gamesData = getGamesData(languageName);
  const game = gamesData[gameId as keyof typeof gamesData];

  // Fetch vocabulary words for the game
  const fetchGameWords = useCallback(async () => {
    if (!activeChild?.id) {
      // Use fallback words if no child
      setGameWords(FALLBACK_WORDS[languageCode] || FALLBACK_WORDS.HINDI);
      setIsLoadingWords(false);
      return;
    }

    setIsLoadingWords(true);
    try {
      const response = await api.getGameVocabulary(activeChild.id, 10);
      if (response.success && response.data && response.data.length > 0) {
        setGameWords(response.data);
      } else {
        // Use fallback words for the language
        setGameWords(FALLBACK_WORDS[languageCode] || FALLBACK_WORDS.HINDI);
      }
    } catch (error) {
      console.error('Error fetching game vocabulary:', error);
      // Use fallback words for the language
      setGameWords(FALLBACK_WORDS[languageCode] || FALLBACK_WORDS.HINDI);
    } finally {
      setIsLoadingWords(false);
    }
  }, [activeChild?.id, languageCode]);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  useEffect(() => {
    if (isHydrated && isAuthenticated) {
      fetchGameWords();
    }
  }, [isHydrated, isAuthenticated, fetchGameWords]);

  const handleGameComplete = (score: number) => {
    setFinalScore(score);
    setGameState('complete');
  };

  const handlePlayAgain = () => {
    setGameState('intro');
    setFinalScore(0);
  };

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

  if (!game) {
    return (
      <MainLayout headerTitle="Game Not Found">
        <div className="flex flex-col items-center justify-center py-12">
          <span className="text-6xl mb-4">🎮</span>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Game Not Found</h1>
          <p className="text-gray-500 mb-6">This game doesn&apos;t exist.</p>
          <Link href="/games">
            <Button>Back to Games</Button>
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
          <Link href="/games" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{game.name}</h1>
            <p className="text-gray-500">{game.description}</p>
          </div>
        </motion.div>

        {/* Game Content */}
        <motion.div variants={fadeInUp}>
          {gameState === 'intro' && (
            <Card className="text-center py-12">
              <span className="text-6xl mb-4 block">{game.icon}</span>
              <h2 className="text-xl font-bold text-gray-900 mb-2">{game.name}</h2>
              <p className="text-gray-500 mb-6">{game.description}</p>
              <Badge variant="success" className="mb-6">+{game.xpReward} XP</Badge>
              <div>
                <Button
                  onClick={() => setGameState('playing')}
                  className="px-8"
                  disabled={isLoadingWords || gameWords.length === 0}
                >
                  {isLoadingWords ? 'Loading...' : 'Start Game'}
                </Button>
              </div>
            </Card>
          )}

          {gameState === 'playing' && (
            <>
              {gameId === 'word-match' && (
                <WordMatchGame
                  onComplete={handleGameComplete}
                  gameWords={gameWords}
                  language={languageCode}
                  languageName={languageName}
                />
              )}
              {gameId === 'listen-speak' && (
                <ListenSpeakGame
                  onComplete={handleGameComplete}
                  gameWords={gameWords}
                  language={languageCode}
                  languageName={languageName}
                />
              )}
            </>
          )}

          {gameState === 'complete' && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <Card className="text-center py-12 bg-gradient-to-br from-green-50 to-teal-50">
                <span className="text-6xl mb-4 block">🎉</span>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Great Job!</h2>
                <p className="text-lg text-gray-600 mb-4">
                  You scored {finalScore} points!
                </p>
                <Badge variant="success" size="lg" className="mb-6">
                  +{game.xpReward} XP Earned!
                </Badge>
                <div className="flex gap-3 justify-center">
                  <Button onClick={handlePlayAgain} variant="outline">
                    Play Again
                  </Button>
                  <Link href="/games">
                    <Button>Back to Games</Button>
                  </Link>
                </div>
              </Card>
            </motion.div>
          )}
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
