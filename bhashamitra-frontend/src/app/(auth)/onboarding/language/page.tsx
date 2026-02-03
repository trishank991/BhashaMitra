'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { useOnboarding } from '@/hooks';
import { Button, Card } from '@/components/ui';
import { PeppiCharacter } from '@/components/peppi';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { LanguageCode } from '@/types';
import api from '@/lib/api';

const PRIMARY_LANGUAGES: LanguageCode[] = ['HINDI', 'GUJARATI', 'TAMIL', 'PUNJABI'];

export default function OnboardingLanguagePage() {
  const router = useRouter();
  const { activeChild } = useAuthStore();
  const { saveProgress } = useOnboarding();

  const [selectedLanguage, setSelectedLanguage] = useState<LanguageCode | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!activeChild) {
      router.push('/onboarding/child');
    }
  }, [activeChild, router]);

  const handleContinue = async () => {
    if (!selectedLanguage) {
      setError('Please select a language');
      return;
    }

    if (!activeChild) {
      router.push('/onboarding/child');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Update child's language
      const response = await api.updateChild(activeChild.id, {
        language: selectedLanguage,
      });

      if (response.success) {
        saveProgress('hasSelectedLanguage');
        router.push('/onboarding/tour');
      } else {
        setError('Failed to update language preference');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('[OnboardingLanguage] Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    router.push('/onboarding/child');
  };

  if (!activeChild) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col">
      {/* Back button */}
      <header className="p-4">
        <Button variant="ghost" size="sm" onClick={handleBack}>
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
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8">
        <motion.div
          initial="initial"
          animate="animate"
          variants={staggerContainer}
          className="w-full max-w-2xl"
        >
          {/* Peppi Mascot */}
          <motion.div variants={fadeInUp} className="flex justify-center mb-6">
            <PeppiCharacter size="medium" expression="happy" />
          </motion.div>

          {/* Title */}
          <motion.h1
            variants={fadeInUp}
            className="text-2xl md:text-3xl font-bold text-center text-gray-900 mb-2"
          >
            Which language will {activeChild.name} learn?
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-600 mb-8"
          >
            Don&apos;t worry, you can always change this later!
          </motion.p>

          {/* Language Cards */}
          <motion.div variants={fadeInUp}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {PRIMARY_LANGUAGES.map((langCode) => {
                const lang = SUPPORTED_LANGUAGES[langCode];
                const isSelected = selectedLanguage === langCode;

                return (
                  <Card
                    key={langCode}
                    interactive
                    className={`cursor-pointer transition-all ${
                      isSelected
                        ? 'ring-4 ring-primary-500 bg-primary-50'
                        : 'hover:shadow-lg'
                    }`}
                    onClick={() => setSelectedLanguage(langCode)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">
                          {lang.name}
                        </h3>
                        <p className="text-2xl font-bold text-primary-600 mt-1">
                          {lang.nativeName}
                        </p>
                      </div>
                      <div className="text-3xl">{lang.flag}</div>
                    </div>

                    {isSelected && (
                      <div className="mt-4 flex items-center text-primary-600">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 24 24"
                          fill="currentColor"
                          className="w-5 h-5"
                        >
                          <path
                            fillRule="evenodd"
                            d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                            clipRule="evenodd"
                          />
                        </svg>
                        <span className="ml-2 font-semibold">Selected</span>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>

            {error && (
              <p className="text-error-500 text-sm text-center mb-4">{error}</p>
            )}

            <Button
              size="lg"
              className="w-full"
              onClick={handleContinue}
              isLoading={isLoading}
              disabled={!selectedLanguage}
            >
              Continue
            </Button>
          </motion.div>

          {/* Progress Indicator */}
          <motion.div
            variants={fadeInUp}
            className="mt-6 text-center text-sm text-gray-500"
          >
            Step 3 of 4
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
