'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { useOnboarding } from '@/hooks';
import { Button, Input, Card } from '@/components/ui';
import { PeppiCharacter } from '@/components/peppi';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import api from '@/lib/api';

export default function OnboardingChildPage() {
  const router = useRouter();
  const { fetchChildren, setActiveChild } = useAuthStore();
  const { saveProgress } = useOnboarding();

  const [name, setName] = useState('');
  const [age, setAge] = useState<number>(6);
  const [gender, setGender] = useState<'male' | 'female' | ''>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!name.trim()) {
      setError("Please enter your child's name");
      return;
    }

    if (age < 4 || age > 14) {
      setError('Age must be between 4 and 14');
      return;
    }

    setIsLoading(true);

    try {
      // Calculate approximate date of birth from age
      const today = new Date();
      const birthYear = today.getFullYear() - age;
      const dateOfBirth = `${birthYear}-01-01`; // Use Jan 1 as approximate

      const childData = {
        name: name.trim(),
        date_of_birth: dateOfBirth,
        avatar: 'child_1',
        language: 'HINDI', // Default, will be updated in next step
      };

      const response = await api.createChild(childData);

      if (response.success && response.data) {
        // Set as active child
        setActiveChild(response.data);

        // Refresh children list
        await fetchChildren();

        // Save progress and move to next step
        saveProgress('hasAddedChild');
        router.push('/onboarding/language');
      } else {
        setError(response.error || 'Failed to create child profile');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('[OnboardingChild] Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    router.push('/onboarding');
  };

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
          className="w-full max-w-lg"
        >
          {/* Peppi Mascot */}
          <motion.div variants={fadeInUp} className="flex justify-center mb-6">
            <PeppiCharacter size="medium" expression="excited" />
          </motion.div>

          {/* Title */}
          <motion.h1
            variants={fadeInUp}
            className="text-2xl md:text-3xl font-bold text-center text-gray-900 mb-2"
          >
            Tell me about your child
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-600 mb-6"
          >
            I can&apos;t wait to meet them!
          </motion.p>

          {/* Form */}
          <motion.div variants={fadeInUp}>
            <Card>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Name Input */}
                <Input
                  label="Child's Name"
                  type="text"
                  placeholder="Enter name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />

                {/* Age Picker */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Age
                  </label>
                  <div className="flex gap-2 flex-wrap">
                    {Array.from({ length: 11 }, (_, i) => i + 4).map(
                      (ageOption) => (
                        <button
                          key={ageOption}
                          type="button"
                          onClick={() => setAge(ageOption)}
                          className={`px-4 py-2 rounded-xl font-semibold transition-colors ${
                            age === ageOption
                              ? 'bg-primary-500 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {ageOption}
                        </button>
                      )
                    )}
                  </div>
                </div>

                {/* Gender (Optional) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Gender (Optional)
                  </label>
                  <div className="flex gap-3">
                    <button
                      type="button"
                      onClick={() => setGender('male')}
                      className={`flex-1 px-4 py-3 rounded-xl font-semibold transition-colors ${
                        gender === 'male'
                          ? 'bg-primary-500 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Boy
                    </button>
                    <button
                      type="button"
                      onClick={() => setGender('female')}
                      className={`flex-1 px-4 py-3 rounded-xl font-semibold transition-colors ${
                        gender === 'female'
                          ? 'bg-primary-500 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Girl
                    </button>
                  </div>
                </div>

                {error && (
                  <p className="text-error-500 text-sm text-center">{error}</p>
                )}

                <Button
                  type="submit"
                  size="lg"
                  className="w-full"
                  isLoading={isLoading}
                >
                  Continue
                </Button>
              </form>
            </Card>
          </motion.div>

          {/* Progress Indicator */}
          <motion.div
            variants={fadeInUp}
            className="mt-6 text-center text-sm text-gray-500"
          >
            Step 2 of 4
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
