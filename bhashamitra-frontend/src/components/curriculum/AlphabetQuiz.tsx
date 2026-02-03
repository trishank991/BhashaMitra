'use client';

import { useState, useCallback, useEffect, useMemo, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Volume2, RefreshCw, CheckCircle2, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import { useSounds } from '@/hooks/useSounds';
import { useAudio } from '@/hooks/useAudio';
import LetterCard from './LetterCard';
import PeppiSpeech from '@/components/peppi/PeppiSpeech';

interface Letter {
  char: string;
  roman: string;
  sound: string;
  exampleWord?: string;
}

interface AlphabetQuizProps {
  letters: Letter[];
  quizType: 'sound-to-letter' | 'letter-to-sound';
  language?: string;
  passingScore?: number;
  onComplete: (score: number, passed: boolean) => void;
  onBack?: () => void;
  className?: string;
}

interface Question {
  correctLetter: Letter;
  options: Letter[];
}

// Utility to shuffle array
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Generate a quiz question
function generateQuestion(letters: Letter[], correctLetter: Letter, optionCount: number): Question {
  const incorrectOptions = letters
    .filter(l => l.char !== correctLetter.char)
    .sort(() => Math.random() - 0.5)
    .slice(0, optionCount - 1);

  const options = shuffleArray([correctLetter, ...incorrectOptions]);

  return {
    correctLetter,
    options,
  };
}

// Generate TTS text for a letter with context for clearer pronunciation
// Single characters are hard for TTS to pronounce clearly, so we add the example word
function getLetterAudioText(letter: Letter, language: string = 'HINDI'): string {
  // If we have an example word, use "letter से word" pattern for clearer pronunciation
  if (letter.exampleWord) {
    if (language === 'TAMIL') {
      // Tamil pattern: "க, உதாரணமாக கல்" (letter, for example, word)
      return `${letter.char}, உதாரணமாக ${letter.exampleWord}`;
    } else {
      // Hindi, Punjabi, etc: "letter से word" (letter from word)
      return `${letter.char} से ${letter.exampleWord}`;
    }
  }
  // Fallback: just the letter (may not be clear)
  return letter.char;
}

export function AlphabetQuiz({
  letters,
  quizType,
  language = 'HINDI',
  passingScore = 60,
  onComplete,
  onBack,
  className,
}: AlphabetQuizProps) {
  const ageConfig = useAgeConfig();
  const { onCorrect, onWrong, onCelebration } = useSounds();
  const { playAudio } = useAudio({ language });

  // Age-adapted settings
  const questionCount = useMemo(() => {
    switch (ageConfig.variant) {
      case 'junior':
        return Math.min(5, letters.length);
      case 'standard':
        return Math.min(8, letters.length);
      case 'teen':
        return Math.min(10, letters.length);
      default:
        return 8;
    }
  }, [ageConfig.variant, letters.length]);

  const optionCount = useMemo(() => {
    return ageConfig.variant === 'junior' ? 3 : 4;
  }, [ageConfig.variant]);

  // Quiz state
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isCorrectAnswer, setIsCorrectAnswer] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [quizComplete, setQuizComplete] = useState(false);

  // Use ref for audio play guard to avoid double-play in React 18 Strict Mode
  const hasPlayedQuestionRef = useRef(false);

  // Generate questions on mount
  useEffect(() => {
    const selectedLetters = shuffleArray(letters).slice(0, questionCount);
    const generatedQuestions = selectedLetters.map(letter =>
      generateQuestion(letters, letter, optionCount)
    );
    setQuestions(generatedQuestions);
  }, [letters, questionCount, optionCount]);

  // Current question
  const currentQuestion = questions[currentQuestionIndex];

  // Reset the play guard when moving to a new question
  useEffect(() => {
    hasPlayedQuestionRef.current = false;
  }, [currentQuestionIndex]);

  // Auto-play question audio for sound-to-letter quiz
  // Play the letter with example word for clearer pronunciation
  // Uses ref to prevent double-play in React 18 Strict Mode
  useEffect(() => {
    if (quizType === 'sound-to-letter' && currentQuestion && !hasPlayedQuestionRef.current) {
      hasPlayedQuestionRef.current = true;
      // Use letter + example word for clearer TTS pronunciation
      const audioText = getLetterAudioText(currentQuestion.correctLetter, language);
      playAudio(audioText);
    }
  }, [currentQuestion, quizType, playAudio, language]);

  // Handle answer selection
  const handleAnswerSelect = useCallback(
    (letter: Letter) => {
      if (isCorrectAnswer !== null) return; // Already answered

      setSelectedAnswer(letter.char);
      const correct = letter.char === currentQuestion.correctLetter.char;
      setIsCorrectAnswer(correct);

      if (correct) {
        onCorrect();
        setCorrectAnswers(prev => prev + 1);
        setScore(prev => prev + Math.round(100 / questionCount));

        // Move to next question or complete quiz
        setTimeout(() => {
          if (currentQuestionIndex + 1 >= questions.length) {
            // Quiz complete
            setQuizComplete(true);
            const finalScore = Math.round(((correctAnswers + 1) / questionCount) * 100);
            const passed = finalScore >= passingScore;
            if (passed) {
              onCelebration();
            }
          } else {
            // Next question (ref is reset by useEffect when currentQuestionIndex changes)
            setCurrentQuestionIndex(prev => prev + 1);
            setSelectedAnswer(null);
            setIsCorrectAnswer(null);
          }
        }, 1500);
      } else {
        onWrong();
        // Allow retry after animation
        setTimeout(() => {
          setSelectedAnswer(null);
          setIsCorrectAnswer(null);
        }, 1000);
      }
    },
    [
      currentQuestion,
      isCorrectAnswer,
      currentQuestionIndex,
      questions.length,
      questionCount,
      correctAnswers,
      passingScore,
      onCorrect,
      onWrong,
      onCelebration,
    ]
  );

  // Replay question audio
  const handleReplayAudio = useCallback(() => {
    if (quizType === 'sound-to-letter' && currentQuestion) {
      // Use letter + example word for clearer TTS pronunciation
      const audioText = getLetterAudioText(currentQuestion.correctLetter, language);
      playAudio(audioText);
    }
  }, [quizType, currentQuestion, playAudio, language]);

  // Retry quiz
  const handleRetry = useCallback(() => {
    setCurrentQuestionIndex(0);
    setSelectedAnswer(null);
    setIsCorrectAnswer(null);
    setScore(0);
    setCorrectAnswers(0);
    setQuizComplete(false);
    hasPlayedQuestionRef.current = false;

    // Regenerate questions
    const selectedLetters = shuffleArray(letters).slice(0, questionCount);
    const generatedQuestions = selectedLetters.map(letter =>
      generateQuestion(letters, letter, optionCount)
    );
    setQuestions(generatedQuestions);
  }, [letters, questionCount, optionCount]);

  // Complete and return score
  const handleComplete = useCallback(() => {
    const finalScore = Math.round((correctAnswers / questionCount) * 100);
    const passed = finalScore >= passingScore;
    onComplete(finalScore, passed);
  }, [correctAnswers, questionCount, passingScore, onComplete]);

  if (questions.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className={cn('text-gray-600', ageConfig.fontSize.body)}>
          Loading quiz...
        </p>
      </div>
    );
  }

  if (quizComplete) {
    const finalScore = Math.round((correctAnswers / questionCount) * 100);
    const passed = finalScore >= passingScore;

    return (
      <div className={cn('min-h-screen flex flex-col items-center justify-center', ageConfig.spacing.padding, className)}>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center max-w-2xl"
        >
          {/* Score Display */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
            className={cn(
              'w-48 h-48 mx-auto mb-8 rounded-full flex items-center justify-center',
              passed ? 'bg-green-100 border-8 border-green-500' : 'bg-orange-100 border-8 border-orange-500'
            )}
          >
            <div>
              <p className={cn('font-bold', passed ? 'text-green-700' : 'text-orange-700', ageConfig.fontSize.heading)}>
                {finalScore}%
              </p>
              <p className={cn('text-sm', passed ? 'text-green-600' : 'text-orange-600')}>
                {correctAnswers}/{questionCount} correct
              </p>
            </div>
          </motion.div>

          {/* Status Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.4 }}
            className="mb-6"
          >
            {passed ? (
              <CheckCircle2 className="w-20 h-20 mx-auto text-green-500" />
            ) : (
              <XCircle className="w-20 h-20 mx-auto text-orange-500" />
            )}
          </motion.div>

          {/* Peppi Encouragement - disabled autoSpeak as English text with Hindi TTS causes issues */}
          <div className="mb-8">
            <PeppiSpeech
              trigger={passed ? 'lessonComplete' : 'encouragement'}
              autoSpeak={false}
              size="lg"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 justify-center">
            {!passed && (
              <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                onClick={handleRetry}
                className={cn(
                  'flex items-center gap-2 px-8 py-4 rounded-full',
                  'bg-primary-500 hover:bg-primary-600 text-white font-semibold',
                  'transition-colors shadow-lg',
                  ageConfig.fontSize.body
                )}
              >
                <RefreshCw className="w-5 h-5" />
                Try Again
              </motion.button>
            )}
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              onClick={handleComplete}
              className={cn(
                'px-8 py-4 rounded-full font-semibold transition-colors shadow-lg',
                passed
                  ? 'bg-green-500 hover:bg-green-600 text-white'
                  : 'bg-gray-500 hover:bg-gray-600 text-white',
                ageConfig.fontSize.body
              )}
            >
              {passed ? 'Continue' : 'Finish'}
            </motion.button>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className={cn('min-h-screen flex flex-col', ageConfig.spacing.padding, className)}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        {onBack && (
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className={ageConfig.fontSize.small}>Back</span>
          </button>
        )}

        {/* Progress */}
        <div className="flex-1 mx-8">
          <div className="flex items-center gap-2 mb-2">
            <span className={cn('text-gray-600', ageConfig.fontSize.small)}>
              Question {currentQuestionIndex + 1} of {questionCount}
            </span>
          </div>
          <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-primary-500"
              initial={{ width: 0 }}
              animate={{ width: `${((currentQuestionIndex + 1) / questionCount) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Score */}
        <div className="text-right">
          <p className={cn('font-bold text-primary-600', ageConfig.fontSize.body)}>
            Score: {score}%
          </p>
        </div>
      </div>

      {/* Question Area */}
      <div className="flex-1 flex flex-col items-center justify-center">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentQuestionIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="w-full max-w-4xl"
          >
            {/* Prompt */}
            <div className="text-center mb-12">
              {quizType === 'sound-to-letter' ? (
                <>
                  <p className={cn('text-gray-700 mb-6', ageConfig.fontSize.body)}>
                    Which letter makes this sound?
                  </p>
                  <button
                    onClick={handleReplayAudio}
                    className={cn(
                      'flex items-center gap-3 px-8 py-4 rounded-full mx-auto',
                      'bg-primary-500 hover:bg-primary-600 text-white font-semibold',
                      'transition-colors shadow-lg',
                      ageConfig.fontSize.body
                    )}
                  >
                    <Volume2 className="w-6 h-6" />
                    Play Sound
                  </button>
                </>
              ) : (
                <>
                  <p className={cn('text-gray-700 mb-6', ageConfig.fontSize.body)}>
                    What sound does this letter make?
                  </p>
                  <div className={cn('text-8xl font-bold text-primary-600 mb-4')}>
                    {currentQuestion.correctLetter.char}
                  </div>
                </>
              )}
            </div>

            {/* Options */}
            {quizType === 'sound-to-letter' ? (
              <div
                className={cn(
                  'grid gap-6 w-full',
                  optionCount <= 2 ? 'grid-cols-2 max-w-xl mx-auto' : 'grid-cols-2 md:grid-cols-4'
                )}
              >
                {currentQuestion.options.map((option, index) => (
                  <motion.div
                    key={option.char}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <LetterCard
                      letter={option.char}
                      transliteration={option.roman}
                      isSelected={selectedAnswer === option.char && isCorrectAnswer === null}
                      isCorrect={selectedAnswer === option.char && isCorrectAnswer === true}
                      isIncorrect={selectedAnswer === option.char && isCorrectAnswer === false}
                      onClick={() => handleAnswerSelect(option)}
                      showAudio={false}
                    />
                  </motion.div>
                ))}
              </div>
            ) : (
              <div
                className={cn(
                  'grid gap-6 w-full max-w-2xl mx-auto',
                  optionCount <= 2 ? 'grid-cols-1' : 'grid-cols-2'
                )}
              >
                {currentQuestion.options.map((option, index) => (
                  <motion.div
                    key={option.char}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <button
                      onClick={() => handleAnswerSelect(option)}
                      className={cn(
                        'w-full px-8 py-6 rounded-2xl border-2 font-semibold transition-all',
                        ageConfig.fontSize.body,
                        selectedAnswer === option.char && isCorrectAnswer === null &&
                          'border-primary-500 bg-primary-50 ring-2 ring-primary-300',
                        selectedAnswer === option.char && isCorrectAnswer === true &&
                          'border-green-500 bg-green-50 ring-2 ring-green-300',
                        selectedAnswer === option.char && isCorrectAnswer === false &&
                          'border-red-500 bg-red-50 ring-2 ring-red-300 animate-shake',
                        selectedAnswer !== option.char &&
                          'border-gray-200 bg-white hover:border-primary-300 hover:bg-gray-50'
                      )}
                    >
                      {option.roman} ({option.sound})
                    </button>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        {/* Peppi Feedback */}
        {isCorrectAnswer !== null && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-12"
          >
            <PeppiSpeech
              trigger={isCorrectAnswer ? 'correct' : 'incorrect'}
              size="md"
              autoSpeak={false}
            />
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default AlphabetQuiz;
