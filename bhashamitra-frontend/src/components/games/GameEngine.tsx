'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { PeppiAvatar } from '@/components/peppi/PeppiAvatar';
import { usePeppiStore } from '@/stores';
import { Flame, Volume2, CheckCircle2, XCircle, Star } from 'lucide-react';

interface GameQuestion {
  id: string;
  question: string;
  questionHindi: string;
  correctAnswer: string;
  options: Array<{
    id: string;
    text: string;
    textHindi: string;
    image?: string;
  }>;
  audioUrl?: string;
  imageUrl?: string;
}

interface GameEngineProps {
  gameCode: string;
  childAge: number;
  onComplete: (score: number, accuracy: number) => void;
  onExit?: () => void;
}

interface GameState {
  currentQuestion: number;
  totalQuestions: number;
  score: number;
  streak: number;
  correctCount: number;
  isComplete: boolean;
}

// Peppi Hinglish feedback messages
const correctMessages = [
  'बहुत अच्छे! 🌟',
  'वाह! Perfect! ⭐',
  'हाँ! That\'s right!',
  'शाबाश! Champion!',
  'Excellent! तुम तो genius हो!',
];

const encouragementMessages = [
  'ओह! कोई बात नहीं, try again!',
  'Almost! एक बार और!',
  'Hmm, ज़रा सोचो...',
  'Not quite! Listen again!',
];

const streakMessages: Record<number, string> = {
  3: 'Wow! तुम on fire हो! 🔥',
  5: 'पाँच correct! Unstoppable! 🚀',
  7: 'सात in a row! Superstar! ⭐',
  10: 'दस! Perfect score! 🏆👑',
};

function getRandomItem<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

export function GameEngine({ gameCode, childAge, onComplete, onExit }: GameEngineProps) {
  const { setMood, setCurrentMessage } = usePeppiStore();

  const [gameState, setGameState] = useState<GameState>({
    currentQuestion: 0,
    totalQuestions: 10,
    score: 0,
    streak: 0,
    correctCount: 0,
    isComplete: false,
  });

  const [questions, setQuestions] = useState<GameQuestion[]>([]);
  const [displayOptions, setDisplayOptions] = useState<GameQuestion['options']>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Calculate number of options based on age (research-backed)
  const getOptionsCount = useCallback(() => {
    if (childAge <= 3) return 2;  // Binary choice for youngest
    if (childAge === 4) return 3;  // Slight challenge
    return 4;  // Standard quiz format for age 5+
  }, [childAge]);

  // Load game data
  useEffect(() => {
    const loadGame = async () => {
      setIsLoading(true);
      try {
        // In production, fetch from API
        // const response = await fetch(`/api/v1/games/${gameCode}?age=${childAge}`);
        // const data = await response.json();

        // Mock data for now
        const mockQuestions: GameQuestion[] = Array.from({ length: 10 }, (_, i) => ({
          id: `q${i + 1}`,
          question: `Question ${i + 1}`,
          questionHindi: `सवाल ${i + 1}`,
          correctAnswer: 'opt1',
          options: shuffleArray([
            { id: 'opt1', text: 'Correct Answer', textHindi: 'सही जवाब', image: '/images/option1.png' },
            { id: 'opt2', text: 'Wrong 1', textHindi: 'गलत 1', image: '/images/option2.png' },
            { id: 'opt3', text: 'Wrong 2', textHindi: 'गलत 2', image: '/images/option3.png' },
            { id: 'opt4', text: 'Wrong 3', textHindi: 'गलत 3', image: '/images/option4.png' },
          ]),
        }));

        setQuestions(mockQuestions);
        setGameState(prev => ({ ...prev, totalQuestions: mockQuestions.length }));
        setMood('happy');
        setCurrentMessage('चलो खेलते हैं! Let\'s play!');
      } catch (error) {
        console.error('Failed to load game:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadGame();
  }, [gameCode, childAge, setMood, setCurrentMessage]);

  // Update display options when question changes
  useEffect(() => {
    if (questions.length > 0 && gameState.currentQuestion < questions.length) {
      const currentQ = questions[gameState.currentQuestion];
      const optionsCount = getOptionsCount();
      // Ensure correct answer is included, then fill with wrong answers
      const correctOpt = currentQ.options.find(o => o.id === currentQ.correctAnswer);
      const wrongOpts = currentQ.options.filter(o => o.id !== currentQ.correctAnswer);
      const selectedOpts = correctOpt
        ? [correctOpt, ...wrongOpts.slice(0, optionsCount - 1)]
        : currentQ.options.slice(0, optionsCount);
      setDisplayOptions(shuffleArray(selectedOpts));
    }
  }, [questions, gameState.currentQuestion, getOptionsCount]);

  const currentQ = questions[gameState.currentQuestion];

  // Play sound effect
  const playSound = (type: 'correct' | 'incorrect') => {
    try {
      const audio = new Audio(`/sounds/${type}.mp3`);
      audio.volume = 0.5;
      audio.play().catch(() => {});
    } catch {
      // Ignore audio errors
    }
  };

  // Handle answer selection
  const handleAnswerSelect = (answerId: string) => {
    if (selectedAnswer || !currentQ) return;

    setSelectedAnswer(answerId);
    const correct = answerId === currentQ.correctAnswer;
    setIsCorrect(correct);
    setShowFeedback(true);

    if (correct) {
      playSound('correct');
      const newStreak = gameState.streak + 1;
      const newScore = gameState.score + 10 + (newStreak >= 3 ? 5 : 0); // Streak bonus

      setMood('celebrating');

      // Check for streak milestone
      if (streakMessages[newStreak]) {
        setCurrentMessage(streakMessages[newStreak]);
      } else {
        setCurrentMessage(getRandomItem(correctMessages));
      }

      setGameState(prev => ({
        ...prev,
        score: newScore,
        streak: newStreak,
        correctCount: prev.correctCount + 1,
      }));

      // Auto-advance after feedback
      setTimeout(() => {
        handleNextQuestion();
      }, 1500);
    } else {
      playSound('incorrect');
      setMood('encouraging');
      setCurrentMessage(getRandomItem(encouragementMessages));

      setGameState(prev => ({
        ...prev,
        streak: 0, // Reset streak on wrong answer
      }));
      // Don't auto-advance - allow retry
    }
  };

  // Handle retry (for wrong answers)
  const handleRetry = () => {
    setSelectedAnswer(null);
    setIsCorrect(null);
    setShowFeedback(false);
    setMood('happy');
    setCurrentMessage('फिर से try करो! You can do it!');
  };

  // Handle next question
  const handleNextQuestion = () => {
    setSelectedAnswer(null);
    setIsCorrect(null);
    setShowFeedback(false);

    if (gameState.currentQuestion + 1 >= gameState.totalQuestions) {
      // Game complete
      setGameState(prev => ({ ...prev, isComplete: true }));
      setMood('celebrating');
      setCurrentMessage('बहुत बढ़िया! You completed the game! 🎉');

      const accuracy = ((gameState.correctCount + 1) / gameState.totalQuestions) * 100;
      setTimeout(() => {
        onComplete(gameState.score + 10, accuracy);
      }, 2000);
    } else {
      setGameState(prev => ({
        ...prev,
        currentQuestion: prev.currentQuestion + 1,
      }));
      setMood('happy');
      setCurrentMessage('अगला सवाल! Next question!');
    }
  };

  // Play question audio
  const playQuestionAudio = () => {
    if (currentQ?.audioUrl) {
      const audio = new Audio(currentQ.audioUrl);
      audio.play().catch(() => {});
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <PeppiAvatar size="lg" />
        <p className="text-lg text-gray-600">Game लोड हो रहा है...</p>
      </div>
    );
  }

  if (gameState.isComplete) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center p-8"
      >
        <PeppiAvatar size="xl" className="mx-auto mb-6" />
        <h2 className="text-3xl font-bold text-gray-800 mb-4">🎉 बधाई हो!</h2>
        <p className="text-xl text-gray-600 mb-2">
          {gameState.correctCount} / {gameState.totalQuestions} सही!
        </p>
        <div className="flex items-center justify-center gap-2 text-4xl font-bold text-primary-600 mb-8">
          <Star className="w-10 h-10 text-yellow-500 fill-yellow-500" />
          {gameState.score} points
        </div>
        <Button variant="primary" size="lg" onClick={onExit}>
          Continue
        </Button>
      </motion.div>
    );
  }

  if (!currentQ) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      {/* Header with Progress */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-gray-700">
            {gameState.currentQuestion + 1} / {gameState.totalQuestions}
          </span>
          {gameState.streak >= 2 && (
            <motion.div
              className="flex items-center gap-1 bg-orange-100 px-2 py-1 rounded-full"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            >
              <Flame className="w-4 h-4 text-orange-500" />
              <span className="text-xs font-bold text-orange-600">{gameState.streak}</span>
            </motion.div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Star className="w-5 h-5 text-yellow-500" />
          <span className="font-bold text-gray-800">{gameState.score}</span>
        </div>
      </div>

      <ProgressBar
        value={gameState.currentQuestion}
        max={gameState.totalQuestions}
        variant="primary"
        size="md"
        animated
      />

      {/* Peppi Section */}
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50">
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <PeppiAvatar size="md" />
          </div>
        </CardContent>
      </Card>

      {/* Question Card */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-1">{currentQ.questionHindi}</h2>
              <p className="text-gray-500">{currentQ.question}</p>
            </div>
            {currentQ.audioUrl && (
              <Button variant="ghost" size="sm" onClick={playQuestionAudio}>
                <Volume2 className="w-6 h-6" />
              </Button>
            )}
          </div>

          {/* Question Image */}
          {currentQ.imageUrl && (
            <div className="mb-6 flex justify-center">
              <img
                src={currentQ.imageUrl}
                alt="Question"
                className="max-h-40 rounded-xl"
              />
            </div>
          )}

          {/* Answer Options */}
          <div className={cn(
            'grid gap-4',
            displayOptions.length <= 2 ? 'grid-cols-2' : 'grid-cols-2'
          )}>
            {displayOptions.map((option) => {
              const isSelected = selectedAnswer === option.id;
              const isCorrectAnswer = option.id === currentQ.correctAnswer;
              const showCorrect = showFeedback && isCorrectAnswer;
              const showIncorrect = showFeedback && isSelected && !isCorrect;

              return (
                <motion.button
                  key={option.id}
                  onClick={() => handleAnswerSelect(option.id)}
                  disabled={!!selectedAnswer}
                  className={cn(
                    'relative p-4 rounded-2xl border-3 text-left transition-all',
                    'disabled:cursor-not-allowed',
                    !selectedAnswer && 'border-gray-200 bg-white hover:border-primary-300 hover:bg-primary-50 hover:shadow-lg',
                    showCorrect && 'border-green-500 bg-green-50',
                    showIncorrect && 'border-red-400 bg-red-50',
                    isSelected && !showFeedback && 'border-primary-500 bg-primary-50'
                  )}
                  whileHover={!selectedAnswer ? { scale: 1.02, y: -2 } : {}}
                  whileTap={!selectedAnswer ? { scale: 0.98 } : {}}
                >
                  {option.image && (
                    <div className="mb-3 flex justify-center">
                      <div className="w-20 h-20 bg-gray-100 rounded-xl flex items-center justify-center">
                        <img
                          src={option.image}
                          alt={option.text}
                          className="max-w-full max-h-full object-contain"
                          onError={(e) => {
                            (e.target as HTMLImageElement).style.display = 'none';
                          }}
                        />
                      </div>
                    </div>
                  )}
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-bold text-gray-800">{option.textHindi}</p>
                      <p className="text-sm text-gray-500">{option.text}</p>
                    </div>
                    {showCorrect && <CheckCircle2 className="w-6 h-6 text-green-500" />}
                    {showIncorrect && <XCircle className="w-6 h-6 text-red-500" />}
                  </div>
                </motion.button>
              );
            })}
          </div>

          {/* Retry Button (only shows on incorrect answer) */}
          <AnimatePresence>
            {isCorrect === false && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mt-6 text-center"
              >
                <Button variant="primary" size="lg" onClick={handleRetry}>
                  फिर से Try करें
                </Button>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </div>
  );
}

export default GameEngine;
