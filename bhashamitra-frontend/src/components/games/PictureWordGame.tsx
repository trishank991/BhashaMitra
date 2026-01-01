'use client';

import { useState, useCallback, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCw, Trophy, Star, ArrowLeft } from 'lucide-react';
import { cn, shuffleArray } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import { useSounds } from '@/hooks/useSounds';
import AudioButton from '@/components/ui/AudioButton';
import PeppiSpeech from '@/components/peppi/PeppiSpeech';
import Celebration from '@/components/animations/Celebration';

interface Word {
  id: string;
  word: string;
  transliteration: string;
  meaning: string;
  imageUrl: string;
  audioUrl?: string;
}

interface PictureWordGameProps {
  words: Word[];
  language?: string;
  onGameComplete: (score: number, totalQuestions: number) => void;
  onBack?: () => void;
  className?: string;
}

interface Question {
  correctWord: Word;
  options: Word[];
}

type PeppiTriggerType = 'welcome' | 'correct' | 'incorrect' | 'encouragement' | 'lessonComplete';

export function PictureWordGame({
  words,
  language = 'HINDI',
  onGameComplete,
  onBack,
  className,
}: PictureWordGameProps) {
  const ageConfig = useAgeConfig();
  const { onCorrect, onWrong, onCelebration } = useSounds();

  // Age-based number of options
  const optionsCount = useMemo(() => {
    switch (ageConfig.variant) {
      case 'junior':
        return 3;
      case 'standard':
        return 4;
      case 'teen':
        return 4;
      default:
        return 4;
    }
  }, [ageConfig.variant]);

  // Game state
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [gameComplete, setGameComplete] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [peppiTrigger, setPeppiTrigger] = useState<PeppiTriggerType>('welcome');

  // Initialize game
  const initializeGame = useCallback(() => {
    if (words.length < optionsCount) {
      console.warn('Not enough words to create questions');
      return;
    }

    // Create questions
    const shuffledWords = shuffleArray([...words]);
    const newQuestions: Question[] = [];

    for (let i = 0; i < Math.min(shuffledWords.length, 10); i++) {
      const correctWord = shuffledWords[i];

      // Get wrong options
      const wrongOptions = shuffledWords
        .filter((w) => w.id !== correctWord.id)
        .slice(0, optionsCount - 1);

      // Shuffle options
      const options = shuffleArray([correctWord, ...wrongOptions]);

      newQuestions.push({
        correctWord,
        options,
      });
    }

    setQuestions(newQuestions);
    setCurrentQuestionIndex(0);
    setScore(0);
    setSelectedOption(null);
    setIsCorrect(null);
    setAttempts(0);
    setGameComplete(false);
    setShowCelebration(false);
    setPeppiTrigger('welcome');
  }, [words, optionsCount]);

  // Initialize on mount
  useEffect(() => {
    initializeGame();
  }, [initializeGame]);

  const currentQuestion = questions[currentQuestionIndex];

  // Handle option selection
  const handleOptionSelect = useCallback(
    (wordId: string) => {
      if (selectedOption || !currentQuestion) return;

      setSelectedOption(wordId);
      const correct = wordId === currentQuestion.correctWord.id;
      setIsCorrect(correct);

      if (correct) {
        // Correct answer
        onCorrect();
        const points = attempts === 0 ? 10 : attempts === 1 ? 5 : 3;
        setScore((prev) => prev + points);
        setPeppiTrigger('correct');

        // Move to next question after delay
        setTimeout(() => {
          if (currentQuestionIndex + 1 >= questions.length) {
            // Game complete
            setGameComplete(true);
            setShowCelebration(true);
            setPeppiTrigger('lessonComplete');
            onCelebration();
            onGameComplete(score + points, questions.length);
          } else {
            // Next question
            setCurrentQuestionIndex((prev) => prev + 1);
            setSelectedOption(null);
            setIsCorrect(null);
            setAttempts(0);
            setPeppiTrigger('encouragement');
          }
        }, 1500);
      } else {
        // Wrong answer
        onWrong();
        setAttempts((prev) => prev + 1);
        setPeppiTrigger('incorrect');

        // Allow retry after brief delay (max 2 attempts)
        setTimeout(() => {
          if (attempts >= 1) {
            // Max attempts reached, move to next question
            setTimeout(() => {
              if (currentQuestionIndex + 1 >= questions.length) {
                setGameComplete(true);
                setPeppiTrigger('lessonComplete');
                onGameComplete(score, questions.length);
              } else {
                setCurrentQuestionIndex((prev) => prev + 1);
                setSelectedOption(null);
                setIsCorrect(null);
                setAttempts(0);
                setPeppiTrigger('encouragement');
              }
            }, 1000);
          } else {
            setSelectedOption(null);
            setIsCorrect(null);
          }
        }, 800);
      }
    },
    [
      selectedOption,
      currentQuestion,
      currentQuestionIndex,
      questions.length,
      attempts,
      score,
      onCorrect,
      onWrong,
      onCelebration,
      onGameComplete,
    ]
  );

  // Get option button style
  const getOptionStyle = (wordId: string) => {
    if (!selectedOption) {
      return 'bg-white border-gray-200 hover:border-primary-300 hover:shadow-md';
    }

    if (wordId === selectedOption) {
      if (isCorrect) {
        return 'bg-green-100 border-green-500 ring-2 ring-green-300';
      } else {
        return 'bg-red-100 border-red-500 ring-2 ring-red-300 animate-shake';
      }
    }

    // Show correct answer after wrong attempt
    if (isCorrect === false && wordId === currentQuestion?.correctWord.id) {
      return 'bg-green-50 border-green-300';
    }

    return 'bg-white border-gray-200 opacity-60';
  };

  // Calculate stars based on score
  const getStarCount = (finalScore: number, total: number) => {
    const percentage = (finalScore / (total * 10)) * 100;
    if (percentage >= 90) return 5;
    if (percentage >= 75) return 4;
    if (percentage >= 60) return 3;
    if (percentage >= 40) return 2;
    return 1;
  };

  if (!currentQuestion && !gameComplete) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-secondary-50 to-white flex items-center justify-center">
        <div className="text-center">
          <p className={cn('text-gray-600', ageConfig.fontSize.body)}>
            Loading game...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('min-h-screen bg-gradient-to-b from-secondary-50 to-white p-4', className)}>
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-6">
        <div className="flex items-center justify-between">
          {onBack && (
            <button
              onClick={onBack}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft size={20} />
              <span className={cn('hidden sm:inline', ageConfig.fontSize.small)}>Back</span>
            </button>
          )}

          <h1 className={cn('text-center font-bold text-gray-900', ageConfig.fontSize.heading)}>
            Picture Word Match
          </h1>

          <button
            onClick={initializeGame}
            className="flex items-center gap-2 text-primary-600 hover:text-primary-700 transition-colors"
            title="Restart Game"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        {/* Progress */}
        <div className="flex justify-center gap-6 mt-4">
          <div className="text-center">
            <p className={cn('text-gray-500', ageConfig.fontSize.small)}>Question</p>
            <p className={cn('font-bold text-primary-600', ageConfig.fontSize.body)}>
              {currentQuestionIndex + 1}/{questions.length}
            </p>
          </div>
          <div className="text-center">
            <p className={cn('text-gray-500', ageConfig.fontSize.small)}>Score</p>
            <p className={cn('font-bold text-green-600', ageConfig.fontSize.body)}>
              {score}
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2 mt-4 overflow-hidden">
          <motion.div
            className="bg-gradient-to-r from-primary-400 to-primary-600 h-full rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Game Area */}
      {currentQuestion && !gameComplete && (
        <div className="max-w-4xl mx-auto">
          <motion.div
            key={currentQuestionIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* Image Display */}
            <div className="bg-white rounded-3xl shadow-lg p-6 md:p-8 mb-6">
              <div className="flex flex-col items-center gap-4">
                <motion.div
                  className="relative w-full max-w-md aspect-square rounded-2xl overflow-hidden shadow-md"
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <img
                    src={currentQuestion.correctWord.imageUrl}
                    alt="What is this?"
                    className="w-full h-full object-cover"
                  />
                </motion.div>

                {/* Audio Button */}
                <div className="flex items-center gap-3">
                  <p className={cn('text-gray-600', ageConfig.fontSize.body)}>
                    {ageConfig.variant === 'junior' ? 'Tap to hear:' : 'Listen:'}
                  </p>
                  <AudioButton
                    text={currentQuestion.correctWord.word}
                    audioUrl={currentQuestion.correctWord.audioUrl}
                    language={language}
                    size="lg"
                    variant="primary"
                  />
                </div>

                <p className={cn('text-center text-gray-700 font-semibold', ageConfig.fontSize.body)}>
                  {ageConfig.variant === 'junior'
                    ? 'Which word matches the picture?'
                    : 'Select the correct word for this picture'}
                </p>
              </div>
            </div>

            {/* Word Options */}
            <div className={cn('grid gap-4', {
              'grid-cols-1 sm:grid-cols-3': optionsCount === 3,
              'grid-cols-2 sm:grid-cols-4': optionsCount === 4,
            })}>
              {currentQuestion.options.map((word, index) => (
                <motion.button
                  key={word.id}
                  onClick={() => handleOptionSelect(word.id)}
                  disabled={!!selectedOption}
                  className={cn(
                    'p-6 rounded-2xl border-2 transition-all shadow-sm',
                    getOptionStyle(word.id),
                    ageConfig.fontSize.body,
                    'font-semibold'
                  )}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={!selectedOption ? { scale: 1.05, y: -5 } : {}}
                  whileTap={!selectedOption ? { scale: 0.98 } : {}}
                >
                  <div className="flex flex-col items-center gap-2">
                    {ageConfig.showHindiScript ? (
                      <>
                        <span className="text-2xl">{word.word}</span>
                        <span className={cn('text-gray-500', ageConfig.fontSize.small)}>
                          {word.transliteration}
                        </span>
                      </>
                    ) : (
                      <span>{word.transliteration}</span>
                    )}

                    {/* Show meaning for teens */}
                    {ageConfig.variant === 'teen' && (
                      <span className={cn('text-gray-600 mt-1', ageConfig.fontSize.small)}>
                        ({word.meaning})
                      </span>
                    )}

                    {/* Checkmark for correct answer */}
                    {selectedOption === word.id && isCorrect && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                      >
                        <Star className="w-6 h-6 text-yellow-500 fill-yellow-400" />
                      </motion.div>
                    )}
                  </div>
                </motion.button>
              ))}
            </div>

            {/* Attempt Counter */}
            {attempts > 0 && !isCorrect && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mt-4"
              >
                <p className={cn('text-orange-600', ageConfig.fontSize.small)}>
                  {attempts === 1 ? 'Try again! One more chance.' : 'Moving to next question...'}
                </p>
              </motion.div>
            )}
          </motion.div>
        </div>
      )}

      {/* Game Complete Overlay */}
      <AnimatePresence>
        {gameComplete && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-3xl p-8 max-w-md w-full text-center shadow-2xl"
            >
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 0.5, repeat: 3 }}
              >
                <Trophy className="w-20 h-20 text-yellow-500 mx-auto mb-4" />
              </motion.div>

              <h2 className={cn('font-bold text-gray-900 mb-4', ageConfig.fontSize.heading)}>
                {ageConfig.variant === 'junior' ? 'Amazing!' : 'Excellent Work!'}
              </h2>

              <div className="space-y-2 mb-6">
                <p className={cn('text-gray-600', ageConfig.fontSize.body)}>
                  Final Score: <span className="font-bold text-primary-600">{score}</span>
                </p>
                <p className={cn('text-gray-600', ageConfig.fontSize.small)}>
                  Questions: {currentQuestionIndex}/{questions.length}
                </p>
              </div>

              {/* Stars */}
              <div className="flex items-center justify-center gap-1 mb-6">
                {[...Array(5)].map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0 }}
                    animate={{ scale: i < getStarCount(score, questions.length) ? 1 : 0.5 }}
                    transition={{ delay: i * 0.1, type: 'spring' }}
                  >
                    <Star
                      className={cn(
                        'w-8 h-8',
                        i < getStarCount(score, questions.length)
                          ? 'text-yellow-400 fill-yellow-400'
                          : 'text-gray-300'
                      )}
                    />
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

      {/* Celebration Animation */}
      <Celebration
        show={showCelebration}
        onComplete={() => setShowCelebration(false)}
        type="confetti"
      />

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

export default PictureWordGame;
