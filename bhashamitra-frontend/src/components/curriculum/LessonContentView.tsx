'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, Check, X, ChevronRight, BookOpen, Sparkles, HelpCircle, Award } from 'lucide-react';
import { cn } from '@/lib/utils';
import { api } from '@/lib/api';
import type { LessonContentJSON, LessonExercise, LessonContentSection, LessonType } from '@/types/curriculum';

interface LessonContentViewProps {
  content: LessonContentJSON;
  lessonType: LessonType;
  language?: string;
  onComplete?: (score: number) => void;
  className?: string;
}

type LessonStage = 'introduction' | 'learning' | 'practice' | 'summary' | 'complete';

export function LessonContentView({
  content,
  lessonType,
  language = 'HINDI',
  onComplete,
  className,
}: LessonContentViewProps) {
  const [stage, setStage] = useState<LessonStage>('introduction');
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | number | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [totalAnswered, setTotalAnswered] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const sections = content.sections || [];
  const exercises = content.exercises || [];
  const hasSections = sections.length > 0;
  const hasExercises = exercises.length > 0;

  // Play audio for text
  const playAudio = async (text: string) => {
    if (isPlaying) return;
    setIsPlaying(true);
    try {
      const response = await api.getAudio(text, language, 'kid_friendly');
      if (response.success && response.audioUrl) {
        const audio = new Audio(response.audioUrl);
        audio.onended = () => setIsPlaying(false);
        audio.onerror = () => setIsPlaying(false);
        await audio.play();
      } else {
        setIsPlaying(false);
      }
    } catch (error) {
      console.error('Audio playback error:', error);
      setIsPlaying(false);
    }
  };

  // Audio button component
  const AudioButton = ({ text, size = 'md' }: { text: string; size?: 'sm' | 'md' | 'lg' }) => {
    const sizeClasses = {
      sm: 'w-8 h-8',
      md: 'w-10 h-10',
      lg: 'w-12 h-12',
    };

    return (
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => playAudio(text)}
        disabled={isPlaying}
        className={cn(
          'rounded-full flex items-center justify-center shadow-md transition-all',
          sizeClasses[size],
          isPlaying ? 'bg-indigo-300 animate-pulse' : 'bg-indigo-500 hover:bg-indigo-600'
        )}
      >
        <Volume2 className="text-white" size={size === 'lg' ? 24 : size === 'md' ? 20 : 16} />
      </motion.button>
    );
  };

  // Handle moving to next stage
  const handleNextStage = () => {
    if (stage === 'introduction') {
      if (hasSections) {
        setStage('learning');
      } else if (hasExercises) {
        setStage('practice');
      } else if (content.summary) {
        setStage('summary');
      } else {
        setStage('complete');
        onComplete?.(100);
      }
    } else if (stage === 'learning') {
      if (currentSectionIndex < sections.length - 1) {
        setCurrentSectionIndex(currentSectionIndex + 1);
      } else if (hasExercises) {
        setStage('practice');
        setCurrentSectionIndex(0);
      } else if (content.summary) {
        setStage('summary');
      } else {
        setStage('complete');
        onComplete?.(100);
      }
    } else if (stage === 'practice') {
      // Move to next exercise or complete
      if (currentExerciseIndex < exercises.length - 1) {
        setCurrentExerciseIndex(currentExerciseIndex + 1);
        setSelectedAnswer(null);
        setIsCorrect(null);
      } else if (content.summary) {
        setStage('summary');
      } else {
        const finalScore = totalAnswered > 0 ? Math.round((score / totalAnswered) * 100) : 100;
        setStage('complete');
        onComplete?.(finalScore);
      }
    } else if (stage === 'summary') {
      const finalScore = totalAnswered > 0 ? Math.round((score / totalAnswered) * 100) : 100;
      setStage('complete');
      onComplete?.(finalScore);
    }
  };

  // Check answer for multiple choice
  const handleAnswer = (answer: string | number) => {
    if (isCorrect !== null) return; // Already answered

    setSelectedAnswer(answer);
    const currentExercise = exercises[currentExerciseIndex];
    const correct = answer === currentExercise.correct ||
      (typeof currentExercise.correct === 'number' && currentExercise.options &&
       currentExercise.options[currentExercise.correct] === answer);

    setIsCorrect(correct ? true : false);
    setTotalAnswered(totalAnswered + 1);
    if (correct) {
      setScore(score + 1);
    }
  };

  // Render introduction stage
  const renderIntroduction = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="text-center py-8"
    >
      <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
        <BookOpen className="text-white" size={40} />
      </div>

      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        {lessonType === 'INTRODUCTION' ? "Let's Begin!" : "Ready to Learn?"}
      </h2>

      {content.introduction && (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 mb-6 max-w-lg mx-auto">
          <p className="text-gray-700 text-lg leading-relaxed">{content.introduction}</p>
          {content.introduction_hindi && (
            <div className="mt-4 flex items-center justify-center gap-3">
              <p className="text-indigo-700 text-lg font-medium">{content.introduction_hindi}</p>
              <AudioButton text={content.introduction_hindi} size="sm" />
            </div>
          )}
        </div>
      )}

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleNextStage}
        className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-8 py-4 rounded-2xl font-bold text-lg shadow-lg flex items-center gap-2 mx-auto"
      >
        Start Learning
        <ChevronRight size={24} />
      </motion.button>
    </motion.div>
  );

  // Render learning section
  const renderSection = (section: LessonContentSection, index: number) => (
    <motion.div
      key={index}
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="bg-white rounded-2xl shadow-lg overflow-hidden"
    >
      {/* Section header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-4">
        <div className="flex items-center justify-between text-white">
          <h3 className="font-bold text-lg">{section.title}</h3>
          <span className="text-sm opacity-80">
            Section {index + 1} of {sections.length}
          </span>
        </div>
      </div>

      {/* Section content */}
      <div className="p-6">
        <ul className="space-y-4">
          {section.items.map((item, itemIndex) => (
            <motion.li
              key={itemIndex}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: itemIndex * 0.1 }}
              className="flex items-start gap-3 p-3 bg-gray-50 rounded-xl"
            >
              <span className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-sm flex-shrink-0">
                {itemIndex + 1}
              </span>
              <div className="flex-1">
                <p className="text-gray-700">{item}</p>
              </div>
              {/* Check if item has Hindi text */}
              {/[\u0900-\u097F]/.test(item) && (
                <AudioButton text={item} size="sm" />
              )}
            </motion.li>
          ))}
        </ul>
      </div>

      {/* Navigation */}
      <div className="p-4 bg-gray-50 flex justify-end">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleNextStage}
          className="bg-indigo-500 text-white px-6 py-3 rounded-xl font-medium flex items-center gap-2"
        >
          {currentSectionIndex < sections.length - 1 ? 'Next Section' : hasExercises ? 'Start Practice' : 'Complete'}
          <ChevronRight size={20} />
        </motion.button>
      </div>
    </motion.div>
  );

  // Render exercise
  const renderExercise = (exercise: LessonExercise, index: number) => (
    <motion.div
      key={index}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="bg-white rounded-2xl shadow-lg overflow-hidden"
    >
      {/* Exercise header */}
      <div className="bg-gradient-to-r from-amber-500 to-orange-600 p-4">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center gap-2">
            <HelpCircle size={24} />
            <span className="font-bold">Practice Time!</span>
          </div>
          <span className="text-sm opacity-80">
            Question {index + 1} of {exercises.length}
          </span>
        </div>
      </div>

      {/* Question */}
      <div className="p-6">
        <div className="mb-6">
          <p className="text-xl font-medium text-gray-900 mb-2">{exercise.question}</p>
          {exercise.question_hindi && (
            <div className="flex items-center gap-2">
              <p className="text-lg text-indigo-600">{exercise.question_hindi}</p>
              <AudioButton text={exercise.question_hindi} size="sm" />
            </div>
          )}
          {exercise.audio_text && (
            <div className="mt-4 flex justify-center">
              <AudioButton text={exercise.audio_text} size="lg" />
            </div>
          )}
        </div>

        {/* Multiple choice options */}
        {exercise.type === 'multiple_choice' && exercise.options && (
          <div className="grid grid-cols-1 gap-3">
            {exercise.options.map((option, optIndex) => {
              const isSelected = selectedAnswer === option || selectedAnswer === optIndex;
              const isCorrectOption = exercise.correct === option || exercise.correct === optIndex;

              return (
                <motion.button
                  key={optIndex}
                  whileHover={isCorrect === null ? { scale: 1.01 } : {}}
                  whileTap={isCorrect === null ? { scale: 0.99 } : {}}
                  onClick={() => handleAnswer(option)}
                  disabled={isCorrect !== null}
                  className={cn(
                    'p-4 rounded-xl text-left font-medium transition-all border-2',
                    isCorrect === null
                      ? 'bg-gray-50 border-gray-200 hover:border-indigo-400 hover:bg-indigo-50'
                      : isSelected && isCorrect
                        ? 'bg-green-100 border-green-500 text-green-800'
                        : isSelected && !isCorrect
                          ? 'bg-red-100 border-red-500 text-red-800'
                          : isCorrectOption
                            ? 'bg-green-50 border-green-300 text-green-700'
                            : 'bg-gray-50 border-gray-200 opacity-50'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-sm font-bold border-2 border-current">
                      {String.fromCharCode(65 + optIndex)}
                    </span>
                    <span className="flex-1">{option}</span>
                    {isCorrect !== null && isSelected && (
                      isCorrect ? <Check className="text-green-600" size={24} /> : <X className="text-red-600" size={24} />
                    )}
                    {isCorrect !== null && !isSelected && isCorrectOption && (
                      <Check className="text-green-600" size={24} />
                    )}
                  </div>
                </motion.button>
              );
            })}
          </div>
        )}

        {/* True/False */}
        {exercise.type === 'true_false' && (
          <div className="grid grid-cols-2 gap-4">
            {['True', 'False'].map((option) => {
              const isSelected = selectedAnswer === option;
              const isCorrectOption = exercise.correct === option;

              return (
                <motion.button
                  key={option}
                  whileHover={isCorrect === null ? { scale: 1.02 } : {}}
                  whileTap={isCorrect === null ? { scale: 0.98 } : {}}
                  onClick={() => handleAnswer(option)}
                  disabled={isCorrect !== null}
                  className={cn(
                    'p-6 rounded-2xl font-bold text-xl transition-all border-2',
                    isCorrect === null
                      ? option === 'True'
                        ? 'bg-green-50 border-green-200 hover:border-green-400'
                        : 'bg-red-50 border-red-200 hover:border-red-400'
                      : isSelected && isCorrect
                        ? 'bg-green-100 border-green-500'
                        : isSelected && !isCorrect
                          ? 'bg-red-100 border-red-500'
                          : isCorrectOption
                            ? 'bg-green-50 border-green-300'
                            : 'opacity-50'
                  )}
                >
                  {option}
                </motion.button>
              );
            })}
          </div>
        )}

        {/* Feedback */}
        {isCorrect !== null && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
              'mt-6 p-4 rounded-xl flex items-center gap-3',
              isCorrect ? 'bg-green-100' : 'bg-amber-100'
            )}
          >
            <span className="text-3xl">{isCorrect ? '🎉' : '💪'}</span>
            <div>
              <p className={cn('font-bold', isCorrect ? 'text-green-800' : 'text-amber-800')}>
                {isCorrect ? 'Great job!' : "Nice try! Keep learning!"}
              </p>
              <p className={cn('text-sm', isCorrect ? 'text-green-700' : 'text-amber-700')}>
                {isCorrect ? 'You got it right!' : `The correct answer was: ${exercise.options?.[exercise.correct as number] || exercise.correct}`}
              </p>
            </div>
          </motion.div>
        )}
      </div>

      {/* Navigation */}
      {isCorrect !== null && (
        <div className="p-4 bg-gray-50 flex justify-end">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleNextStage}
            className="bg-indigo-500 text-white px-6 py-3 rounded-xl font-medium flex items-center gap-2"
          >
            {currentExerciseIndex < exercises.length - 1 ? 'Next Question' : 'See Results'}
            <ChevronRight size={20} />
          </motion.button>
        </div>
      )}
    </motion.div>
  );

  // Render summary
  const renderSummary = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <Sparkles className="text-indigo-500" size={28} />
        <h3 className="text-xl font-bold text-gray-900">What You Learned</h3>
      </div>

      <ul className="space-y-3">
        {content.summary?.map((point, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-start gap-3 bg-white rounded-xl p-3"
          >
            <Check className="text-green-500 mt-0.5" size={20} />
            <span className="text-gray-700">{point}</span>
          </motion.li>
        ))}
      </ul>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleNextStage}
        className="w-full mt-6 bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2"
      >
        Complete Lesson
        <Award size={24} />
      </motion.button>
    </motion.div>
  );

  // Render complete stage
  const renderComplete = () => {
    const finalScore = totalAnswered > 0 ? Math.round((score / totalAnswered) * 100) : 100;
    const stars = finalScore >= 90 ? 3 : finalScore >= 70 ? 2 : finalScore >= 50 ? 1 : 0;

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center py-8"
      >
        <motion.div
          animate={{ rotate: [0, -10, 10, -10, 10, 0] }}
          transition={{ duration: 0.5 }}
          className="text-6xl mb-4"
        >
          🎉
        </motion.div>

        <h2 className="text-3xl font-bold text-gray-900 mb-2">Lesson Complete!</h2>

        {totalAnswered > 0 && (
          <>
            <p className="text-xl text-gray-600 mb-4">
              You scored <span className="font-bold text-indigo-600">{finalScore}%</span>
            </p>

            <div className="flex justify-center gap-2 mb-6">
              {[1, 2, 3].map((star) => (
                <motion.span
                  key={star}
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ delay: star * 0.2, type: 'spring' }}
                  className={cn(
                    'text-4xl',
                    star <= stars ? 'opacity-100' : 'opacity-30'
                  )}
                >
                  ⭐
                </motion.span>
              ))}
            </div>
          </>
        )}

        <p className="text-gray-500">
          Great work! You&apos;re making excellent progress.
        </p>
      </motion.div>
    );
  };

  return (
    <div className={cn('max-w-2xl mx-auto', className)}>
      {/* Progress indicator */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
          <span>Progress</span>
          <span>
            {stage === 'complete' ? 'Complete!' :
             stage === 'practice' ? `Exercise ${currentExerciseIndex + 1}/${exercises.length}` :
             stage === 'learning' ? `Section ${currentSectionIndex + 1}/${sections.length}` :
             stage}
          </span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-600"
            initial={{ width: 0 }}
            animate={{
              width: stage === 'complete' ? '100%' :
                     stage === 'summary' ? '90%' :
                     stage === 'practice' ? `${60 + (currentExerciseIndex / exercises.length) * 30}%` :
                     stage === 'learning' ? `${20 + (currentSectionIndex / sections.length) * 40}%` :
                     '10%'
            }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        {stage === 'introduction' && renderIntroduction()}
        {stage === 'learning' && sections[currentSectionIndex] && renderSection(sections[currentSectionIndex], currentSectionIndex)}
        {stage === 'practice' && exercises[currentExerciseIndex] && renderExercise(exercises[currentExerciseIndex], currentExerciseIndex)}
        {stage === 'summary' && renderSummary()}
        {stage === 'complete' && renderComplete()}
      </AnimatePresence>
    </div>
  );
}

export default LessonContentView;
