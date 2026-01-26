'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { usePeppiStore } from '@/stores/peppiStore';
import { useProgressStore } from '@/stores/progressStore';
import { MainLayout } from '@/components/layout';
import { Card, Loading, Button, Breadcrumb } from '@/components/ui';
import { ProgressRing, LessonContentView } from '@/components/curriculum';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';
import { LessonWithProgress } from '@/types';
import { useSounds } from '@/hooks';

// Quiz Question Interface
interface QuizQuestion {
  question: string;
  options: string[];
  correctIndex: number;
}

export default function LessonDetailPage() {
  const router = useRouter();
  const params = useParams();
  const lessonId = params?.id as string | undefined;

  const [isHydrated, setIsHydrated] = useState(false);
  const [lesson, setLesson] = useState<LessonWithProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, activeChild } = useAuthStore();

  // Quiz state
  const [quizActive, setQuizActive] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [quizCompleted, setQuizCompleted] = useState(false);

  // Sound effects
  const { onCorrect, onWrong, onCelebration } = useSounds();
  const peppiStore = usePeppiStore();
  const progressStore = useProgressStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    if (!lessonId) {
      setError('Invalid lesson ID');
      setLoading(false);
      return;
    }

    const fetchLessonData = async () => {
      setLoading(true);
      try {
        const response = await api.getLesson(lessonId, activeChild?.id);
        if (response.success && response.data) {
          setLesson(response.data);
        } else {
          setError(response.error || 'Failed to load lesson');
        }
      } catch {
        setError('Failed to load lesson data');
      } finally {
        setLoading(false);
      }
    };

    fetchLessonData();
  }, [isHydrated, isAuthenticated, lessonId, activeChild?.id, router]);

  // Generate quiz questions from lesson content
  const generateQuizQuestions = (): QuizQuestion[] => {
    const questions: QuizQuestion[] = [];

    // Try to extract questions from lesson content exercises
    if (lesson?.content?.exercises && lesson.content.exercises.length > 0) {
      const exercises = lesson.content.exercises.filter(
        (ex) => ex.type === 'multiple_choice' && ex.options && ex.options.length > 1
      );

      exercises.slice(0, 5).forEach((exercise) => {
        if (exercise.options) {
          const correctIndex = typeof exercise.correct === 'number'
            ? exercise.correct
            : exercise.options.indexOf(exercise.correct as string);

          questions.push({
            question: exercise.question,
            options: exercise.options,
            correctIndex: correctIndex >= 0 ? correctIndex : 0,
          });
        }
      });
    }

    // Try to extract questions from sections if we don't have enough
    if (questions.length < 3 && lesson?.content?.sections && lesson.content.sections.length > 0) {
      lesson.content.sections.slice(0, 3).forEach((section) => {
        if (section.items && section.items.length >= 2) {
          // Create a "What did you learn?" question
          const correctAnswer = section.items[0];
          const wrongAnswers = section.items.slice(1, 3);

          questions.push({
            question: `What did you learn about "${section.title}"?`,
            options: [correctAnswer, ...wrongAnswers].sort(() => Math.random() - 0.5),
            correctIndex: [correctAnswer, ...wrongAnswers].sort(() => Math.random() - 0.5).indexOf(correctAnswer),
          });
        }
      });
    }

    // Fallback: Create generic questions if we still don't have enough
    const fallbackQuestions: QuizQuestion[] = [
      {
        question: 'Did you understand this lesson?',
        options: ['Yes, I understood everything!', 'I need more practice', 'No, it was too hard'],
        correctIndex: 0,
      },
      {
        question: 'Are you ready to use what you learned?',
        options: ['Yes, I am ready!', 'I need to review', 'Not sure yet'],
        correctIndex: 0,
      },
      {
        question: 'How do you feel about this lesson?',
        options: ['I loved it!', 'It was okay', 'I found it difficult'],
        correctIndex: 0,
      },
      {
        question: `What is the main topic of this lesson: "${lesson?.title_english}"?`,
        options: [
          lesson?.title_english || 'Learning new words',
          'Something completely different',
          'I do not remember',
        ],
        correctIndex: 0,
      },
      {
        question: 'Would you like to practice more?',
        options: ['Yes, practice makes perfect!', 'No, I am done', 'Maybe later'],
        correctIndex: 0,
      },
    ];

    // Add fallback questions if needed
    while (questions.length < 3 && fallbackQuestions.length > 0) {
      questions.push(fallbackQuestions.shift()!);
    }

    // Return 3-5 questions
    return questions.slice(0, Math.min(5, Math.max(3, questions.length)));
  };

  // Start the quiz
  const handleStartQuiz = () => {
    const questions = generateQuizQuestions();
    setQuizQuestions(questions);
    setQuizActive(true);
    setQuizScore(0);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setShowFeedback(false);
    setQuizCompleted(false);
  };

  // Handle quiz answer selection
  const handleQuizAnswer = (answerIndex: number) => {
    if (showFeedback) return; // Already answered this question

    setSelectedAnswer(answerIndex);
    setShowFeedback(true);

    const isCorrect = answerIndex === quizQuestions[currentQuestion]?.correctIndex;

    if (isCorrect) {
      setQuizScore(quizScore + 1);
      onCorrect();
    } else {
      onWrong();
    }
  };

  // Move to next quiz question
  const handleNextQuestion = () => {
    if (currentQuestion < quizQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setShowFeedback(false);
    } else {
      // Quiz completed
      setQuizCompleted(true);
      const finalScore = Math.round((quizScore / quizQuestions.length) * 100);

      if (finalScore >= 60) {
        onCelebration();
        // Trigger Peppi celebration for passing quiz
        peppiStore.celebrate();
      } else {
        // Trigger Peppi encouragement for retry
        peppiStore.encourage();
      }
    }
  };

  // Submit quiz and update lesson progress
  const handleSubmitQuiz = async () => {
    if (!activeChild || !lesson || !lessonId) return;

    const finalScore = Math.round((quizScore / quizQuestions.length) * 100);

    if (finalScore < 60) {
      // Failed - allow retry
      setQuizActive(false);
      setQuizCompleted(false);
      peppiStore.encourage();
      return;
    }

    setCompleting(true);
    try {
      // Update with REAL score (not fake 100%)
      const response = await api.updateLessonProgress(lessonId, activeChild.id, finalScore);
      if (response.success && response.data) {
        // Refresh lesson data
        const updated = await api.getLesson(lessonId, activeChild.id);
        if (updated.success && updated.data) {
          setLesson(updated.data);
        }
        
        // Update local progress store with XP from backend
        if (response.data.points_awarded) {
          progressStore.addXp(response.data.points_awarded);
        }
        
        // Update streak in progress store
        progressStore.updateStreak();
        
        // Trigger Peppi celebration
        peppiStore.celebrate();
      }
      setQuizActive(false);
      setQuizCompleted(false);
    } catch {
      setError('Failed to update progress');
    } finally {
      setCompleting(false);
    }
  };

  // Handle retry quiz
  const handleRetryQuiz = () => {
    handleStartQuiz();
  };

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center py-16">
          <Loading size="lg" text="Loading lesson..." />
        </div>
      </MainLayout>
    );
  }

  if (error || !lesson) {
    return (
      <MainLayout>
        <div className="text-center py-16">
          <p className="text-red-500 mb-4">{error || 'Lesson not found'}</p>
          <Link href="/languages/levels" className="text-indigo-600 hover:underline">
            Back to Levels
          </Link>
        </div>
      </MainLayout>
    );
  }

  const isCompleted = lesson.progress?.is_complete;
  const bestScore = lesson.progress?.best_score || 0;
  const attempts = lesson.progress?.attempts || 0;

  // Calculate stars (0-3)
  const getStars = (score: number) => {
    if (score >= lesson.mastery_threshold) return 3;
    if (score >= lesson.mastery_threshold * 0.75) return 2;
    if (score >= lesson.mastery_threshold * 0.5) return 1;
    return 0;
  };

  const stars = getStars(bestScore);

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Breadcrumb Navigation */}
        <motion.div variants={fadeInUp}>
          <Breadcrumb
            items={[
              { label: 'Languages', href: '/languages', emoji: '\uD83D\uDCDA' },
              { label: 'Levels', href: '/languages/levels' },
              { label: 'Module', href: `/languages/modules/${lesson.module}` },
              { label: lesson.title_english },
            ]}
          />
        </motion.div>

        {/* Lesson Header */}
        <motion.div variants={fadeInUp}>
          <Card className="overflow-hidden">
            <div className="p-6">
              <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold">
                  {lesson.order}
                </div>
                <div className="flex-1">
                  <h1 className="text-xl font-bold text-gray-900">{lesson.title_english}</h1>
                  <p className="text-gray-600">
                    {lesson.title_hindi} ({lesson.title_romanized})
                  </p>
                  {lesson.description && (
                    <p className="text-sm text-gray-500 mt-2">{lesson.description}</p>
                  )}
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-4 gap-3 mt-6">
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-indigo-600">{lesson.estimated_minutes}</p>
                  <p className="text-xs text-gray-500">Minutes</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-amber-600">{lesson.points_available}</p>
                  <p className="text-xs text-gray-500">Points</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-green-600">{lesson.mastery_threshold}%</p>
                  <p className="text-xs text-gray-500">To Master</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-purple-600">{attempts}</p>
                  <p className="text-xs text-gray-500">Attempts</p>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Peppi Introduction */}
        {lesson.peppi_intro && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🐱</span>
              <div>
                <p className="font-medium text-amber-900">{lesson.peppi_intro}</p>
                <p className="text-xs text-amber-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Progress Card */}
        {(isCompleted || attempts > 0) && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-gradient-to-br from-green-50 to-emerald-50">
              <div className="flex items-center gap-4">
                <ProgressRing
                  progress={bestScore}
                  size={80}
                  strokeWidth={6}
                  color={isCompleted ? '#22c55e' : '#f59e0b'}
                >
                  <span className="text-lg font-bold" style={{ color: isCompleted ? '#22c55e' : '#f59e0b' }}>
                    {bestScore}%
                  </span>
                </ProgressRing>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900">
                    {isCompleted ? 'Lesson Complete!' : 'In Progress'}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Best Score: {bestScore}% • {attempts} attempt{attempts !== 1 ? 's' : ''}
                  </p>
                  <div className="flex gap-1 mt-2">
                    {[1, 2, 3].map((star) => (
                      <svg
                        key={star}
                        className={`w-6 h-6 ${star <= stars ? 'text-amber-400' : 'text-gray-200'}`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Lesson Content */}
        <motion.div variants={fadeInUp}>
          {lesson.content && Object.keys(lesson.content).length > 0 ? (
            <LessonContentView
              content={lesson.content}
              lessonType={lesson.lesson_type || 'LEARNING'}
              language={activeChild?.language as string || 'HINDI'}
              onComplete={() => {
                // Content finished - user can now take quiz
              }}
            />
          ) : (
            <Card>
              <div className="text-center py-8">
                <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 text-lg">Lesson Content</h3>
                <p className="text-gray-500 mt-2">
                  Content for this lesson is being prepared.
                </p>
                <p className="text-sm text-gray-400 mt-1">
                  Check back soon for interactive learning activities!
                </p>
              </div>
            </Card>
          )}
        </motion.div>

        {/* Action Buttons */}
        <motion.div variants={fadeInUp} className="flex gap-3">
          <Button
            variant="outline"
            className="flex-1"
            onClick={() => router.push(`/languages/modules/${lesson.module}`)}
          >
            Back to Module
          </Button>
          <Button
            variant="primary"
            className="flex-1"
            disabled={completing}
            onClick={handleStartQuiz}
          >
            {completing ? 'Completing...' : isCompleted ? 'Practice Again' : 'Complete Lesson'}
          </Button>
        </motion.div>

        {/* Success Message */}
        {isCompleted && lesson.peppi_success && (
          <motion.div variants={fadeInUp}>
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 flex items-start gap-3">
              <span className="text-2xl">🎉</span>
              <div>
                <p className="font-medium text-green-900">{lesson.peppi_success}</p>
                <p className="text-xs text-green-700 mt-1">- Peppi</p>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Quiz Modal */}
      <AnimatePresence>
        {quizActive && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={(e) => {
              if (e.target === e.currentTarget && !quizCompleted) {
                // Allow closing if not completed yet
                setQuizActive(false);
              }
            }}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="bg-white rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              {!quizCompleted ? (
                <>
                  {/* Quiz Header */}
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                      Quick Quiz!
                      <span className="text-2xl">🎯</span>
                    </h3>
                    <button
                      onClick={() => setQuizActive(false)}
                      className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  {/* Progress */}
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-gray-500 mb-2">
                      <span>Question {currentQuestion + 1} of {quizQuestions.length}</span>
                      <span>Score: {quizScore}/{currentQuestion + (showFeedback ? 1 : 0)}</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-300"
                        style={{ width: `${((currentQuestion + 1) / quizQuestions.length) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Question */}
                  <div className="mb-6">
                    <p className="text-lg font-medium text-gray-900 mb-4">
                      {quizQuestions[currentQuestion]?.question}
                    </p>

                    {/* Options */}
                    <div className="space-y-2">
                      {quizQuestions[currentQuestion]?.options?.map((option, idx) => {
                        const isSelected = selectedAnswer === idx;
                        const isCorrect = idx === quizQuestions[currentQuestion]?.correctIndex;
                        const showCorrect = showFeedback && isCorrect;
                        const showWrong = showFeedback && isSelected && !isCorrect;

                        return (
                          <button
                            key={idx}
                            onClick={() => handleQuizAnswer(idx)}
                            disabled={showFeedback}
                            className={`w-full p-3 text-left rounded-lg border-2 transition-all ${
                              showCorrect
                                ? 'bg-green-100 border-green-500 text-green-800'
                                : showWrong
                                ? 'bg-red-100 border-red-500 text-red-800'
                                : isSelected
                                ? 'border-purple-500 bg-purple-50'
                                : 'border-gray-200 hover:border-purple-400 hover:bg-purple-50'
                            } ${showFeedback ? 'cursor-default' : 'cursor-pointer'}`}
                          >
                            <div className="flex items-center justify-between">
                              <span>{option}</span>
                              {showCorrect && <span className="text-green-600">✓</span>}
                              {showWrong && <span className="text-red-600">✗</span>}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Feedback */}
                  {showFeedback && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`mb-4 p-3 rounded-lg ${
                        selectedAnswer === quizQuestions[currentQuestion]?.correctIndex
                          ? 'bg-green-100 text-green-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}
                    >
                      <p className="font-medium">
                        {selectedAnswer === quizQuestions[currentQuestion]?.correctIndex
                          ? 'Correct! Well done!'
                          : 'Not quite! Keep learning!'}
                      </p>
                    </motion.div>
                  )}

                  {/* Next Button */}
                  {showFeedback && (
                    <Button
                      variant="primary"
                      className="w-full"
                      onClick={handleNextQuestion}
                    >
                      {currentQuestion < quizQuestions.length - 1 ? 'Next Question' : 'See Results'}
                    </Button>
                  )}
                </>
              ) : (
                <>
                  {/* Quiz Results */}
                  <div className="text-center">
                    <div className="text-6xl mb-4">
                      {Math.round((quizScore / quizQuestions.length) * 100) >= 60 ? '🎉' : '💪'}
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {Math.round((quizScore / quizQuestions.length) * 100) >= 60
                        ? 'Great Job!'
                        : 'Keep Practicing!'}
                    </h3>
                    <p className="text-lg text-gray-600 mb-4">
                      You scored{' '}
                      <span className="font-bold text-indigo-600">
                        {quizScore}/{quizQuestions.length}
                      </span>{' '}
                      ({Math.round((quizScore / quizQuestions.length) * 100)}%)
                    </p>

                    {Math.round((quizScore / quizQuestions.length) * 100) >= 60 ? (
                      <div className="space-y-3">
                        <p className="text-gray-600">
                          You passed! Your progress has been saved.
                        </p>
                        <Button
                          variant="primary"
                          className="w-full"
                          onClick={handleSubmitQuiz}
                          disabled={completing}
                        >
                          {completing ? 'Saving...' : 'Complete Lesson'}
                        </Button>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        <p className="text-gray-600">
                          You need at least 60% to pass. Try again!
                        </p>
                        <Button
                          variant="primary"
                          className="w-full"
                          onClick={handleRetryQuiz}
                        >
                          Try Again
                        </Button>
                        <Button
                          variant="outline"
                          className="w-full"
                          onClick={() => setQuizActive(false)}
                        >
                          Review Lesson
                        </Button>
                      </div>
                    )}
                  </div>
                </>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </MainLayout>
  );
}
