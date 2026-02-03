'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { useOnboarding } from '@/hooks';
import { Button, Card } from '@/components/ui';
import { PeppiCharacter } from '@/components/peppi';
import { fadeInUp, staggerContainer } from '@/lib/constants';

export default function OnboardingWelcomePage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuthStore();
  const { saveProgress, skipOnboarding } = useOnboarding();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleGetStarted = () => {
    saveProgress('hasSeenWelcome');
    router.push('/onboarding/child');
  };

  const handleSkip = () => {
    skipOnboarding();
    router.push('/home');
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col">
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8">
        <motion.div
          initial="initial"
          animate="animate"
          variants={staggerContainer}
          className="w-full max-w-2xl"
        >
          {/* Peppi Mascot */}
          <motion.div variants={fadeInUp} className="flex justify-center mb-8">
            <PeppiCharacter size="large" expression="happy" />
          </motion.div>

          {/* Welcome Message */}
          <motion.h1
            variants={fadeInUp}
            className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-3"
          >
            Welcome to PeppiAcademy, {user.name}!
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-600 text-lg mb-8"
          >
            I&apos;m Peppi, and I&apos;ll be your guide on this wonderful
            language learning journey!
          </motion.p>

          {/* What We'll Do Card */}
          <motion.div variants={fadeInUp}>
            <Card>
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                What we&apos;ll do together:
              </h2>

              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold mr-4">
                    1
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      Add your child
                    </h3>
                    <p className="text-sm text-gray-600">
                      Tell us about your little learner
                    </p>
                  </div>
                </div>

                <div className="flex items-start">
                  <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold mr-4">
                    2
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      Choose a language
                    </h3>
                    <p className="text-sm text-gray-600">
                      Pick which language to learn first
                    </p>
                  </div>
                </div>

                <div className="flex items-start">
                  <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold mr-4">
                    3
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Quick tour</h3>
                    <p className="text-sm text-gray-600">
                      See all the fun features available
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-8 space-y-3">
                <Button size="lg" className="w-full" onClick={handleGetStarted}>
                  Get Started
                </Button>

                <Button
                  variant="ghost"
                  size="lg"
                  className="w-full"
                  onClick={handleSkip}
                >
                  Skip for now
                </Button>
              </div>
            </Card>
          </motion.div>

          {/* Progress Indicator */}
          <motion.div
            variants={fadeInUp}
            className="mt-8 text-center text-sm text-gray-500"
          >
            Step 1 of 4
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
