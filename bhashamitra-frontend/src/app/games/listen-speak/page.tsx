'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, Button, Badge, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { api } from '@/lib/api';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { GAME_WIN_XP } from '@/lib/constants';

// Sample Hindi words for pronunciation practice
const hindiWords = [
  { id: '1', word: 'नमस्ते', transliteration: 'Namaste', meaning: 'Hello', hint: '🙏' },
  { id: '2', word: 'धन्यवाद', transliteration: 'Dhanyavaad', meaning: 'Thank you', hint: '🙏' },
  { id: '3', word: 'किताब', transliteration: 'Kitaab', meaning: 'Book', hint: '📚' },
  { id: '4', word: 'पानी', transliteration: 'Paani', meaning: 'Water', hint: '💧' },
  { id: '5', word: 'खाना', transliteration: 'Khaana', meaning: 'Food', hint: '🍽️' },
  { id: '6', word: 'घर', transliteration: 'Ghar', meaning: 'Home', hint: '🏠' },
  { id: '7', word: 'स्कूल', transliteration: 'School', meaning: 'School', hint: '🏫' },
  { id: '8', word: 'पेड़', transliteration: 'Ped', meaning: 'Tree', hint: '🌳' },
  { id: '9', word: 'सूरज', transliteration: 'Sooraj', meaning: 'Sun', hint: '☀️' },
  { id: '10', word: 'चाँद', transliteration: 'Chaand', meaning: 'Moon', hint: '🌙' },
];

type GameState = 'start' | 'playing' | 'completed';

interface WordAttempt {
  wordId: string;
  word: string;
  transliteration: string;
  attempts: number;
  success: boolean;
}

export default function ListenSpeakPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [isHydrated, setIsHydrated] = useState(false);
  const [gameState, setGameState] = useState<GameState>('start');
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [wordAttempts, setWordAttempts] = useState<WordAttempt[]>([]);
  const [attempts, setAttempts] = useState(0);
  const [xpEarned, setXpEarned] = useState(0);
  const [isAwardingXP, setIsAwardingXP] = useState(false);
  
  // Audio states
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechResult, setSpeechResult] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [lastAttemptCorrect, setLastAttemptCorrect] = useState<boolean | null>(null);
  
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  const currentWord = hindiWords[currentWordIndex];

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  // Initialize speech recognition and synthesis
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = 'hi-IN';
        
        recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
          const result = event.results[0][0].transcript;
          setSpeechResult(result);
          checkPronunciation(result);
        };
        
        recognitionRef.current.onerror = () => {
          setIsListening(false);
          setLastAttemptCorrect(false);
          setShowResult(true);
        };
        
        recognitionRef.current.onend = () => {
          setIsListening(false);
        };
      }
      
      synthRef.current = window.speechSynthesis;
    }
  }, []);

  const initializeGame = useCallback(() => {
    setCurrentWordIndex(0);
    setWordAttempts([]);
    setAttempts(0);
    setXpEarned(0);
    setShowResult(false);
    setSpeechResult('');
    setLastAttemptCorrect(null);
    setGameState('playing');
  }, []);

  const speakWord = useCallback(() => {
    if (!synthRef.current || !currentWord) return;
    
    setIsSpeaking(true);
    const utterance = new SpeechSynthesisUtterance(currentWord.word);
    utterance.lang = 'hi-IN';
    utterance.rate = 0.7;
    
    utterance.onend = () => {
      setIsSpeaking(false);
    };
    
    synthRef.current.speak(utterance);
  }, [currentWord]);

  const startListening = useCallback(() => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser');
      return;
    }
    
    setIsListening(true);
    setSpeechResult('');
    setShowResult(false);
    setLastAttemptCorrect(null);
    recognitionRef.current.start();
  }, []);

  const checkPronunciation = useCallback((spoken: string) => {
    if (!currentWord) return;
    
    // Simple matching - normalize both strings
    const spokenNormalized = spoken.toLowerCase().trim();
    const targetNormalized = currentWord.word.toLowerCase().trim();
    
    // Allow some flexibility for recognition errors
    const isCorrect = spokenNormalized.includes(targetNormalized) || 
                      targetNormalized.includes(spokenNormalized) ||
                      levenshteinDistance(spokenNormalized, targetNormalized) <= 2;
    
    setLastAttemptCorrect(isCorrect);
    setShowResult(true);
    setAttempts(prev => prev + 1);
    
    // Track attempt for this word
    setWordAttempts(prev => {
      const existing = prev.find(a => a.wordId === currentWord.id);
      if (existing) {
        return prev.map(a => 
          a.wordId === currentWord.id 
            ? { ...a, attempts: a.attempts + 1, success: isCorrect }
            : a
        );
      }
      return [...prev, {
        wordId: currentWord.id,
        word: currentWord.word,
        transliteration: currentWord.transliteration,
        attempts: 1,
        success: isCorrect,
      }];
    });
  }, [currentWord]);

  const nextWord = useCallback(() => {
    if (currentWordIndex < hindiWords.length - 1) {
      setCurrentWordIndex(prev => prev + 1);
      setShowResult(false);
      setSpeechResult('');
      setLastAttemptCorrect(null);
    } else {
      // Game completed
      const xp = GAME_WIN_XP;
      setXpEarned(xp);
      setGameState('completed');
      
      // Award XP via API
      const awardXP = async () => {
        setIsAwardingXP(true);
        try {
          await api.awardXP(xp, 'listen_speak_game');
        } catch (error) {
          console.error('Failed to award XP:', error);
        } finally {
          setIsAwardingXP(false);
        }
      };
      
      awardXP();
    }
  }, [currentWordIndex]);

  const getTotalCorrect = () => {
    return wordAttempts.filter(a => a.success).length;
  };

  // Levenshtein distance for fuzzy matching
  const levenshteinDistance = (a: string, b: string): number => {
    const matrix: number[][] = [];
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[b.length][a.length];
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

  return (
    <MainLayout headerTitle="Listen & Speak" showBack={true} showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Start Screen */}
        {gameState === 'start' && (
          <motion.div variants={fadeInUp} className="text-center space-y-6">
            <Card className="bg-gradient-to-r from-accent-500 to-primary-500 text-white py-8">
              <span className="text-6xl mb-4 block">🎤</span>
              <h2 className="text-2xl font-bold">Listen & Speak</h2>
              <p className="text-sm opacity-90 mt-2">
                Practice your Hindi pronunciation!
              </p>
            </Card>

            <Card className="text-center py-6">
              <h3 className="font-bold text-gray-900 mb-2">How to Play</h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>1. Click "Listen" to hear the word</li>
                <li>2. Click "Speak" and say the word</li>
                <li>3. Get feedback and move to the next word</li>
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
        {gameState === 'playing' && currentWord && (
          <motion.div variants={fadeInUp} className="space-y-4">
            {/* Progress */}
            <div className="flex justify-between items-center">
              <Badge variant="primary">
                Word: {currentWordIndex + 1}/{hindiWords.length}
              </Badge>
              <Badge variant="neutral">
                Attempts: {attempts}
              </Badge>
            </div>

            {/* Word Card */}
            <Card className="text-center py-8">
              <motion.div
                key={currentWord.id}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <span className="text-4xl mb-4 block">{currentWord.hint}</span>
                <h2 className="text-5xl font-bold text-primary-700 mb-2" style={{ fontFamily: 'Noto Sans Devanagari, sans-serif' }}>
                  {currentWord.word}
                </h2>
                <p className="text-lg text-gray-600">
                  {currentWord.transliteration}
                </p>
                <p className="text-sm text-gray-500">
                  {currentWord.meaning}
                </p>
              </motion.div>
            </Card>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <Button
                onClick={speakWord}
                disabled={isSpeaking}
                variant="secondary"
                size="lg"
                className="flex-1"
                leftIcon={isSpeaking ? <span className="animate-pulse">🔊</span> : '🔊'}
              >
                {isSpeaking ? 'Speaking...' : 'Listen'}
              </Button>
              
              <Button
                onClick={startListening}
                disabled={isListening}
                variant="accent"
                size="lg"
                className="flex-1"
                leftIcon={isListening ? '🎙️' : '🎙️'}
              >
                {isListening ? 'Listening...' : 'Speak'}
              </Button>
            </div>

            {/* Recording Visual Feedback */}
            <AnimatePresence>
              {isListening && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="text-center"
                >
                  <div className="inline-flex items-center gap-2 bg-accent-100 px-4 py-2 rounded-full">
                    <motion.span
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ repeat: Infinity, duration: 0.5 }}
                      className="text-2xl"
                    >
                      🎙️
                    </motion.span>
                    <span className="text-accent-700 font-medium">Listening... Say the word!</span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Result Feedback */}
            <AnimatePresence>
              {showResult && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  <Card className={`text-center py-4 ${lastAttemptCorrect ? 'bg-success-50 border-2 border-success-200' : 'bg-error-50 border-2 border-error-200'}`}>
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                      className="text-3xl mb-2"
                    >
                      {lastAttemptCorrect ? '🎉' : '😅'}
                    </motion.div>
                    <p className={`font-bold ${lastAttemptCorrect ? 'text-success-700' : 'text-error-700'}`}>
                      {lastAttemptCorrect ? 'Great pronunciation!' : 'Keep trying!'}
                    </p>
                    {!lastAttemptCorrect && speechResult && (
                      <p className="text-sm text-gray-600 mt-1">
                        You said: "{speechResult}"
                      </p>
                    )}
                    <Button
                      onClick={nextWord}
                      size="md"
                      className="mt-4"
                      rightIcon="➡️"
                    >
                      {currentWordIndex < hindiWords.length - 1 ? 'Next Word' : 'See Results'}
                    </Button>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
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
              <h2 className="text-2xl font-bold">Excellent Work!</h2>
              <p className="text-sm opacity-90 mt-2">
                You completed all the words!
              </p>
            </Card>

            <Card className="text-center py-6">
              <h3 className="font-bold text-gray-900 mb-4">Your Results</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Words Practiced</span>
                  <span className="font-bold">{hindiWords.length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Total Attempts</span>
                  <span className="font-bold">{attempts}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Perfect Pronunciations</span>
                  <span className="font-bold text-success-600">
                    {getTotalCorrect()}
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
                Practice Again 🔄
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

// Type declarations for Web Speech API
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  length: number;
  isFinal: boolean;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: Event) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

export {};
