'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import { Card, Button } from '@/components/ui';
import { useSounds } from '@/hooks';
import { useAgeConfig } from '@/hooks/useAgeConfig';

interface FillBlanksGameProps {
  onComplete?: (score: number, passed: boolean) => void;
  onBack?: () => void;
}

// Sample fill-in-the-blank sentences for Hindi learning
const FILL_IN_THE_BLANK_SENTENCES = [
  {
    id: '1',
    sentence: 'माँ ___ खाती है।',
    options: ['सेब', 'दूध', 'पानी'],
    correctAnswer: 'सेब',
    hint: 'एक लाल फल',
    translation: 'Mother eats ___',
  },
  {
    id: '2',
    sentence: 'पिताजी ___ पढ़ते हैं।',
    options: ['किताब', 'खेल', 'नाटक'],
    correctAnswer: 'किताब',
    hint: 'जिसमें लिखा हो',
    translation: 'Father reads ___',
  },
  {
    id: '3',
    sentence: 'कुत्ता ___ करता है।',
    options: ['भौंक', 'गाता', 'बोल'],
    correctAnswer: 'भौंक',
    hint: 'जानवर की आवाज़',
    translation: 'Dog ___',
  },
  {
    id: '4',
    sentence: 'सूरज ___ में निकलता है।',
    options: ['पूरब', 'नीचे', 'ज़मीन'],
    correctAnswer: 'पूरब',
    hint: 'जहाँ से सूरज आता है',
    translation: 'Sun rises in the ___',
  },
  {
    id: '5',
    sentence: 'बच्चे ___ में खेलते हैं।',
    options: ['पार्क', 'घर', 'स्कूल'],
    correctAnswer: 'पार्क',
    hint: 'बाहर का खेलने का जगह',
    translation: 'Children play in the ___',
  },
];

export default function FillBlanksGame({ onComplete, onBack }: FillBlanksGameProps) {
  const [questions] = useState(FILL_IN_THE_BLANK_SENTENCES);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [score, setScore] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [shuffledOptions, setShuffledOptions] = useState<string[]>([]);

  useAgeConfig();
  const { onCorrect, onWrong, onLevelUp, onClick } = useSounds();

  // Shuffle options for each question
  useEffect(() => {
    if (questions[currentIndex]) {
      const currentQuestion = questions[currentIndex];
      const shuffled = [...currentQuestion.options].sort(() => Math.random() - 0.5);
      setShuffledOptions(shuffled);
      setSelectedAnswer(null);
      setShowHint(false);
    }
  }, [currentIndex, questions]);

  const handleAnswerSelect = useCallback((answer: string) => {
    if (selectedAnswer) return; // Already answered
    
    onClick();
    setSelectedAnswer(answer);
    
    const currentQuestion = questions[currentIndex];
    if (answer === currentQuestion.correctAnswer) {
      setScore(s => s + 20);
      onCorrect();
      
      // Trigger confetti for correct answer
      confetti({
        particleCount: 50,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#22c55e', '#3b82f6', '#f59e0b'],
      });
    } else {
      onWrong();
    }
  }, [selectedAnswer, currentIndex, questions, onCorrect, onWrong, onClick]);

  const handleNext = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(i => i + 1);
    } else {
      // Game complete
      setIsComplete(true);
      const finalScore = score;
      const passed = finalScore >= 60;
      
      if (passed) {
        onLevelUp();
        confetti({
          particleCount: 150,
          spread: 100,
          origin: { y: 0.5 },
        });
      }
      
      onComplete?.(finalScore, passed);
    }
  }, [currentIndex, questions.length, score, onComplete, onLevelUp]);

  const currentQuestion = questions[currentIndex];
  const isCorrect = selectedAnswer === currentQuestion?.correctAnswer;

  if (isComplete) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center p-4">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="max-w-md w-full"
        >
          <Card className="text-center p-8 bg-white shadow-xl">
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">मुबारक!</h2>
            <p className="text-gray-600 mb-6">आपने खेल पूरा कर लिया!</p>
            
            <div className="text-5xl font-bold text-primary-600 mb-2">
              {score} / {questions.length * 20}
            </div>
            <p className="text-sm text-gray-500 mb-6">अंक</p>

            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={onBack}>
                वापस जाएं
              </Button>
              <Button 
                variant="primary" 
                onClick={() => {
                  setCurrentIndex(0);
                  setScore(0);
                  setSelectedAnswer(null);
                  setIsComplete(false);
                }}
              >
                फिर से खेलें
              </Button>
            </div>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <Button variant="ghost" size="sm" onClick={onBack}>
            ← वापस
          </Button>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {currentIndex + 1} / {questions.length}
            </span>
            <div className="w-32 h-3 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-primary-500"
                initial={{ width: 0 }}
                animate={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>
          <span className="text-lg font-bold text-primary-600">
            {score} XP
          </span>
        </div>
      </div>

      {/* Game Content */}
      <div className="max-w-2xl mx-auto p-6">
        <motion.div
          key={currentIndex}
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -50, opacity: 0 }}
        >
          {/* Question Card */}
          <Card className="p-8 mb-6 bg-white shadow-lg">
            <p className="text-lg text-gray-500 mb-2">{currentQuestion?.translation}</p>
            <p className="text-3xl font-bold text-gray-900 mb-8">
              {currentQuestion?.sentence.split('___').map((part, i, arr) => (
                <span key={i}>
                  {part}
                  {i < arr.length - 1 && (
                    <span className="inline-block min-w-[80px] border-b-4 border-primary-400 mx-1 text-center align-middle">
                      <AnimatePresence mode="wait">
                        {selectedAnswer ? (
                          <motion.span
                            key="answer"
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={isCorrect ? 'text-green-600' : 'text-red-600'}
                          >
                            {selectedAnswer}
                          </motion.span>
                        ) : (
                          <motion.span
                            key="blank"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-primary-300"
                          >
                            ?
                          </motion.span>
                        )}
                      </AnimatePresence>
                    </span>
                  )}
                </span>
              ))}
            </p>

            {/* Hint Toggle */}
            {!selectedAnswer && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowHint(!showHint)}
                className="mb-4"
              >
                💡 सुराग {showHint ? 'छुपाएं' : 'दिखाएं'}
              </Button>
            )}

            {/* Hint */}
            {showHint && !isCorrect && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4"
              >
                <p className="text-sm text-yellow-700">
                  <strong>सुराग:</strong> {currentQuestion?.hint}
                </p>
              </motion.div>
            )}

            {/* Feedback */}
            {selectedAnswer && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`p-4 rounded-lg mb-4 ${
                  isCorrect 
                    ? 'bg-green-100 border-2 border-green-300' 
                    : 'bg-red-100 border-2 border-red-300'
                }`}
              >
                <p className={`font-bold ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                  {isCorrect ? '✅ सही उत्तर!' : `❌ सही उत्तर: ${currentQuestion?.correctAnswer}`}
                </p>
              </motion.div>
            )}
          </Card>

          {/* Options */}
          <div className="grid grid-cols-1 gap-3">
            {shuffledOptions.map((option, index) => (
              <motion.div
                key={option}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <button
                  onClick={() => handleAnswerSelect(option)}
                  disabled={!!selectedAnswer}
                  className={`w-full p-4 rounded-xl font-bold text-lg transition-all ${
                    selectedAnswer === option
                      ? isCorrect
                        ? 'bg-green-500 text-white shadow-lg transform scale-105'
                        : 'bg-red-500 text-white shadow-lg'
                      : selectedAnswer
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-white hover:bg-primary-50 hover:shadow-md text-gray-900'
                  }`}
                >
                  {option}
                </button>
              </motion.div>
            ))}
          </div>

          {/* Next Button */}
          {selectedAnswer && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6"
            >
              <Button
                variant="primary"
                size="lg"
                className="w-full"
                onClick={handleNext}
              >
                {currentIndex < questions.length - 1 ? 'अगला प्रश्न →' : 'खेल समाप्त ✓'}
              </Button>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
