'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PublicChallengeResponse, ChallengeQuestion } from '@/lib/api';

interface ChallengeQuizProps {
  challenge: PublicChallengeResponse;
  onComplete: (answers: number[], timeTaken: number) => void;
}

export function ChallengeQuiz({ challenge, onComplete }: ChallengeQuizProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [timeLeft, setTimeLeft] = useState(challenge?.time_limit_seconds ?? 30);
  const [totalTime, setTotalTime] = useState(0);
  const [isAnswerLocked, setIsAnswerLocked] = useState(false);

  // Safe access to questions array with fallback
  const questions = challenge?.questions ?? [];
  const currentQuestion = (questions[currentIndex] ?? {}) as Omit<ChallengeQuestion, 'correct_index'>;
  const isLastQuestion = currentIndex === questions.length - 1;

  // Return early if no questions
  if (!questions.length) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-sm">
          <div className="text-6xl mb-4">📝</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">No Questions</h1>
          <p className="text-gray-500 mb-6">This challenge has no questions yet.</p>
          <a href="/" className="inline-block px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-full font-semibold">
            Go Home
          </a>
        </div>
      </div>
    );
  }

  const timeLimit = challenge?.time_limit_seconds ?? 30;

  // Move to next question with the given answer
  const moveToNext = useCallback((answerIndex: number) => {
    const newAnswers = [...answers, answerIndex];
    setAnswers(newAnswers);

    if (isLastQuestion) {
      onComplete(newAnswers, totalTime);
    } else {
      setCurrentIndex((prev) => prev + 1);
      setSelectedAnswer(null);
      setIsAnswerLocked(false);
      setTimeLeft(timeLimit);
    }
  }, [answers, isLastQuestion, totalTime, onComplete, timeLimit]);

  // Skip/timeout handler (uses -1 for unanswered)
  const handleSkip = useCallback(() => {
    moveToNext(selectedAnswer ?? -1);
  }, [selectedAnswer, moveToNext]);

  const handleSelectAnswer = (index: number) => {
    if (isAnswerLocked) return;
    setSelectedAnswer(index);
    setIsAnswerLocked(true);
    // Brief delay before moving to next - pass the index directly to avoid stale closure
    setTimeout(() => moveToNext(index), 500);
  };

  // Timer
  useEffect(() => {
    if (!questions.length) return; // Don't run timer if no questions

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          // Time's up - auto-submit current answer or -1 for no answer
          handleSkip();
          return timeLimit;
        }
        return prev - 1;
      });
      setTotalTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [currentIndex, timeLimit, questions.length, handleSkip]);

  const progressPercent = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;
  const timerPercent = timeLimit > 0 ? (timeLeft / timeLimit) * 100 : 0;

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 p-4">
      {/* Header */}
      <div className="max-w-lg mx-auto mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-600">
            Question {currentIndex + 1} of {questions.length}
          </span>
          <span className={`text-lg font-bold ${timeLeft <= 5 ? 'text-red-500 animate-pulse' : 'text-gray-700'}`}>
            {timeLeft}s
          </span>
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden mb-2">
          <motion.div
            className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercent}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>

        {/* Timer bar */}
        <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
          <motion.div
            className={`h-full ${timeLeft <= 5 ? 'bg-red-500' : 'bg-green-500'}`}
            animate={{ width: `${timerPercent}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Question Card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentIndex}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          className="max-w-lg mx-auto"
        >
          <div className="bg-white rounded-3xl shadow-xl p-6 mb-6">
            {/* Question type indicator */}
            <div className="text-sm text-gray-500 mb-2 text-center">
              {currentQuestion.type === 'alphabet_recognition' && 'Identify the letter'}
              {currentQuestion.type === 'vocabulary_to_english' && 'What does this mean?'}
              {currentQuestion.type === 'english_to_vocabulary' && 'Translate to the language'}
            </div>

            {/* Main prompt */}
            <div className="text-center mb-6">
              {currentQuestion.image_url && (
                <img
                  src={currentQuestion.image_url}
                  alt="Question"
                  className="w-32 h-32 mx-auto rounded-xl object-cover mb-4"
                />
              )}

              {/* Show native prompt if available, otherwise show question text */}
              {currentQuestion.prompt_native ? (
                <>
                  <h2 className="text-4xl font-bold text-gray-900 mb-2">
                    {currentQuestion.prompt_native}
                  </h2>
                  {currentQuestion.romanization && (
                    <p className="text-lg text-gray-500 italic">
                      {currentQuestion.romanization}
                    </p>
                  )}
                  <p className="text-gray-600 mt-2">{currentQuestion.question}</p>
                </>
              ) : (
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {currentQuestion.question}
                </h2>
              )}
            </div>

            {/* Answer choices - use 'options' from API, fallback to 'choices' */}
            <div className="grid grid-cols-2 gap-3">
              {(currentQuestion.options ?? currentQuestion.choices ?? []).map((choice, index) => (
                <motion.button
                  key={index}
                  whileHover={{ scale: isAnswerLocked ? 1 : 1.02 }}
                  whileTap={{ scale: isAnswerLocked ? 1 : 0.98 }}
                  onClick={() => handleSelectAnswer(index)}
                  disabled={isAnswerLocked}
                  className={`p-4 rounded-xl text-lg font-semibold transition-all ${
                    selectedAnswer === index
                      ? 'bg-purple-500 text-white ring-4 ring-purple-300'
                      : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                  } ${isAnswerLocked && selectedAnswer !== index ? 'opacity-50' : ''}`}
                >
                  {choice}
                </motion.button>
              ))}
            </div>

            {currentQuestion.hint && (
              <p className="text-sm text-gray-400 text-center mt-4">
                Hint: {currentQuestion.hint}
              </p>
            )}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Skip button */}
      <div className="max-w-lg mx-auto text-center">
        <button
          onClick={handleSkip}
          className="text-gray-400 hover:text-gray-600 text-sm underline"
        >
          Skip this question
        </button>
      </div>
    </div>
  );
}
