'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useOnboarding } from '@/hooks';
import { Button } from '@/components/ui';

interface TourScreen {
  id: number;
  title: string;
  description: string;
  emoji: string;
  color: string;
}

const TOUR_SCREENS: TourScreen[] = [
  {
    id: 1,
    title: 'Learn Languages',
    description:
      'Discover Indian languages through fun alphabet and vocabulary lessons designed for kids',
    emoji: '📚',
    color: 'from-orange-400 to-orange-600',
  },
  {
    id: 2,
    title: 'Play Games',
    description:
      'Make learning exciting with interactive games and challenges that help you practice',
    emoji: '🎮',
    color: 'from-green-400 to-green-600',
  },
  {
    id: 3,
    title: 'Practice Speaking',
    description:
      'Use our Mimic feature to practice pronunciation and improve your speaking skills',
    emoji: '🎤',
    color: 'from-purple-400 to-purple-600',
  },
  {
    id: 4,
    title: 'Track Progress',
    description:
      'Earn XP, maintain streaks, level up, and watch your language skills grow every day',
    emoji: '🏆',
    color: 'from-yellow-400 to-yellow-600',
  },
  {
    id: 5,
    title: 'Parent Dashboard',
    description:
      'Parents can monitor learning progress, view insights, and celebrate achievements together',
    emoji: '👨‍👩‍👧‍👦',
    color: 'from-pink-400 to-pink-600',
  },
];

export default function OnboardingTourPage() {
  const router = useRouter();
  const { completeOnboarding, saveProgress } = useOnboarding();
  const [currentScreen, setCurrentScreen] = useState(0);
  const [direction, setDirection] = useState(1);
  const [isCompleting, setIsCompleting] = useState(false);

  const screen = TOUR_SCREENS[currentScreen];
  const isFirstScreen = currentScreen === 0;
  const isLastScreen = currentScreen === TOUR_SCREENS.length - 1;

  const handleNext = () => {
    if (isLastScreen) {
      handleFinish();
    } else {
      setDirection(1);
      setCurrentScreen((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    if (!isFirstScreen) {
      setDirection(-1);
      setCurrentScreen((prev) => prev - 1);
    }
  };

  const handleSkip = async () => {
    await handleFinish();
  };

  const handleFinish = async () => {
    setIsCompleting(true);

    try {
      // Save tour progress
      saveProgress('hasCompletedTour');

      // Complete onboarding via API
      await completeOnboarding();

      // Redirect to home
      router.push('/home');
    } catch (error) {
      console.error('[OnboardingTour] Error:', error);
      // Still redirect even if API fails
      router.push('/home');
    } finally {
      setIsCompleting(false);
    }
  };

  const slideVariants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 300 : -300,
      opacity: 0,
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1,
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 300 : -300,
      opacity: 0,
    }),
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col">
      {/* Header with Skip button */}
      <header className="p-4 flex justify-between items-center">
        <div className="text-xl font-bold text-primary-600">PeppiAcademy</div>
        {!isLastScreen && (
          <Button variant="ghost" size="sm" onClick={handleSkip}>
            Skip Tour
          </Button>
        )}
      </header>

      {/* Progress Dots */}
      <div className="px-6 py-4">
        <div className="flex items-center justify-center gap-2">
          {TOUR_SCREENS.map((_, index) => (
            <button
              key={index}
              onClick={() => {
                setDirection(index > currentScreen ? 1 : -1);
                setCurrentScreen(index);
              }}
              className={`h-2 rounded-full transition-all duration-300 ${
                index === currentScreen
                  ? 'w-8 bg-primary-500'
                  : index < currentScreen
                  ? 'w-2 bg-primary-300'
                  : 'w-2 bg-gray-300'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8 overflow-hidden">
        <div
          className="w-full max-w-md relative"
          style={{ minHeight: '400px' }}
        >
          <AnimatePresence initial={false} custom={direction} mode="wait">
            <motion.div
              key={currentScreen}
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{
                x: { type: 'spring', stiffness: 300, damping: 30 },
                opacity: { duration: 0.2 },
              }}
              className="absolute inset-0 flex flex-col items-center justify-center"
            >
              {/* Emoji Icon */}
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
                className={`w-32 h-32 sm:w-40 sm:h-40 rounded-full bg-gradient-to-br ${screen.color} flex items-center justify-center mb-8 shadow-2xl`}
              >
                <span className="text-6xl sm:text-7xl">{screen.emoji}</span>
              </motion.div>

              {/* Content */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.5 }}
                className="text-center px-4"
              >
                <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
                  {screen.title}
                </h2>
                <p className="text-gray-600 text-lg leading-relaxed">
                  {screen.description}
                </p>
              </motion.div>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Navigation Buttons */}
      <footer className="p-6 pb-8">
        <div className="w-full max-w-md mx-auto flex gap-3">
          <Button
            variant="outline"
            size="lg"
            onClick={handleBack}
            className={`flex-1 ${isFirstScreen ? 'invisible' : ''}`}
            disabled={isCompleting}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-5 h-5 mr-2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15.75 19.5 8.25 12l7.5-7.5"
              />
            </svg>
            Back
          </Button>
          <Button
            size="lg"
            onClick={handleNext}
            className="flex-1"
            isLoading={isCompleting}
          >
            {isLastScreen ? (
              "Get Started!"
            ) : (
              <>
                Next
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                  className="w-5 h-5 ml-2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="m8.25 4.5 7.5 7.5-7.5 7.5"
                  />
                </svg>
              </>
            )}
          </Button>
        </div>

        {/* Step indicator */}
        <p className="text-center text-sm text-gray-500 mt-4">
          Step 4 of 4 • Screen {currentScreen + 1} of {TOUR_SCREENS.length}
        </p>
      </footer>
    </div>
  );
}
