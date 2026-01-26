'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading, Button, Input } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { LanguageCode } from '@/types';
import api from '@/lib/api';

const AVATARS = ['👦', '👧', '👶', '🧒', '👦🏽', '👧🏽', '👶🏽', '🧒🏽', '👦🏾', '👧🏾'];

export default function AddChildPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated, fetchChildren, setActiveChild } = useAuthStore();

  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [avatar, setAvatar] = useState('👦');
  const [language, setLanguage] = useState<LanguageCode>('HINDI');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name.trim()) {
      setError('Please enter a name');
      return;
    }
    if (!age || parseInt(age) < 3 || parseInt(age) > 15) {
      setError('Please enter a valid age (3-15)');
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await api.createChild({
        name: name.trim(),
        age: parseInt(age),
        avatar,
        language,
      });

      if (res.success && res.data) {
        setActiveChild(res.data);
        await fetchChildren();
        router.push('/home');
      } else {
        setError(res.error || 'Failed to add child');
      }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <MainLayout headerTitle="Add Child" showBack onBack={() => router.back()} showNav={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6 max-w-md mx-auto"
      >
        <motion.div variants={fadeInUp} className="text-center">
          <span className="text-5xl block mb-2">🎉</span>
          <h1 className="text-2xl font-bold text-gray-900">Add a Child</h1>
          <p className="text-sm text-gray-500 mt-1">Set up their learning profile</p>
        </motion.div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <motion.div variants={fadeInUp} className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
              {error}
            </motion.div>
          )}

          <motion.div variants={fadeInUp}>
            <label className="block text-sm font-medium text-gray-700 mb-2">Choose an Avatar</label>
            <div className="flex flex-wrap gap-2">
              {AVATARS.map((a) => (
                <button
                  key={a}
                  type="button"
                  onClick={() => setAvatar(a)}
                  className={`text-3xl p-2 rounded-xl transition-all ${
                    avatar === a ? 'bg-primary-100 ring-2 ring-primary-500 scale-110' : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  {a}
                </button>
              ))}
            </div>
          </motion.div>

          <motion.div variants={fadeInUp}>
            <label className="block text-sm font-medium text-gray-700 mb-1">Child&apos;s Name</label>
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter name"
              required
            />
          </motion.div>

          <motion.div variants={fadeInUp}>
            <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
            <Input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="3-15"
              min={3}
              max={15}
              required
            />
          </motion.div>

          <motion.div variants={fadeInUp}>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language to Learn</label>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(SUPPORTED_LANGUAGES).map(([code, lang]) => (
                <button
                  key={code}
                  type="button"
                  onClick={() => setLanguage(code as LanguageCode)}
                  className={`p-3 rounded-xl text-left transition-all ${
                    language === code
                      ? 'bg-primary-50 border-2 border-primary-500'
                      : 'bg-gray-50 border-2 border-transparent hover:border-gray-200'
                  }`}
                >
                  <span className="text-lg">{lang.flag}</span>
                  <p className="text-sm font-medium mt-1">{lang.name}</p>
                </button>
              ))}
            </div>
          </motion.div>

          <motion.div variants={fadeInUp}>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="w-full"
            >
              {isSubmitting ? 'Adding...' : 'Add Child'}
            </Button>
          </motion.div>
        </form>
      </motion.div>
    </MainLayout>
  );
}
