'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading, Button, Input } from '@/components/ui';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import { ChildProfile, LanguageCode } from '@/types';
import api from '@/lib/api';

const AVATARS = ['👦', '👧', '👶', '🧒', '👦🏽', '👧🏽', '👶🏽', '🧒🏽', '👦🏾', '👧🏾'];

export default function ChildDetailPage() {
  const router = useRouter();
  const params = useParams();
  const childId = params?.childId as string;

  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated, children, fetchChildren, setActiveChild, activeChild } = useAuthStore();

  const [child, setChild] = useState<ChildProfile | null>(null);
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [avatar, setAvatar] = useState('');
  const [language, setLanguage] = useState<LanguageCode>('HINDI');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const found = children.find(c => c.id === childId);
    if (found) {
      setChild(found);
      setName(found.name);
      setAge(String(found.age));
      setAvatar(found.avatar || '👦');
      const langCode = typeof found.language === 'string' ? found.language : found.language?.code || 'HINDI';
      setLanguage(langCode as LanguageCode);
    }
  }, [isHydrated, isAuthenticated, childId, children, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (!child) {
    return (
      <MainLayout headerTitle="Child Profile" showBack onBack={() => router.back()}>
        <div className="text-center py-12">
          <p className="text-gray-500">Child not found</p>
        </div>
      </MainLayout>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const res = await api.updateChild(childId, {
        name: name.trim(),
        age: parseInt(age),
        avatar,
        language,
      });

      if (res.success && res.data) {
        if (activeChild?.id === childId) {
          setActiveChild(res.data);
        }
        await fetchChildren();
        router.push('/children');
      } else {
        setError(res.error || 'Failed to update child');
      }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    setIsSubmitting(true);
    try {
      const res = await api.deleteChild(childId);
      if (res.success) {
        if (activeChild?.id === childId) {
          setActiveChild(null);
        }
        await fetchChildren();
        router.push('/children');
      } else {
        setError(res.error || 'Failed to delete child profile');
      }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
      setShowDeleteConfirm(false);
    }
  };

  return (
    <MainLayout headerTitle="Edit Profile" showBack onBack={() => router.back()} showNav={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6 max-w-md mx-auto"
      >
        <motion.div variants={fadeInUp} className="text-center">
          <span className="text-5xl block mb-2">{avatar}</span>
          <h1 className="text-2xl font-bold text-gray-900">Edit {child.name}&apos;s Profile</h1>
        </motion.div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <motion.div variants={fadeInUp} className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
              {error}
            </motion.div>
          )}

          <motion.div variants={fadeInUp}>
            <label className="block text-sm font-medium text-gray-700 mb-2">Avatar</label>
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
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
            <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
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

          <motion.div variants={fadeInUp} className="space-y-3">
            <Button type="submit" disabled={isSubmitting} className="w-full">
              {isSubmitting ? 'Saving...' : 'Save Changes'}
            </Button>
          </motion.div>
        </form>

        {/* Delete section */}
        <motion.div variants={fadeInUp} className="pt-4 border-t border-gray-200">
          {showDeleteConfirm ? (
            <div className="bg-red-50 p-4 rounded-xl space-y-3">
              <p className="text-sm text-red-700 font-medium">
                Are you sure you want to delete {child.name}&apos;s profile? This action cannot be undone.
              </p>
              <div className="flex gap-2">
                <button
                  onClick={handleDelete}
                  disabled={isSubmitting}
                  className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 disabled:opacity-50"
                >
                  {isSubmitting ? 'Deleting...' : 'Yes, Delete'}
                </button>
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="w-full text-center text-sm text-red-500 hover:text-red-600 py-2"
            >
              Delete this profile
            </button>
          )}
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
