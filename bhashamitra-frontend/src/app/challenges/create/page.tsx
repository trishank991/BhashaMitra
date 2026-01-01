'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import api, { ChallengeQuotaResponse } from '@/lib/api';
import { MainLayout } from '@/components/layout';
import { CreateChallengeForm } from '@/components/challenges/CreateChallengeForm';
import { ShareButton } from '@/components/challenges/ShareButton';
import { Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';

export default function CreateChallengePage() {
  const router = useRouter();
  const { isAuthenticated, user, activeChild } = useAuthStore();
  const [isHydrated, setIsHydrated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [quota, setQuota] = useState<ChallengeQuotaResponse | null>(null);
  const [createdCode, setCreatedCode] = useState<string | null>(null);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login?redirect=/challenges/create');
    }
  }, [isHydrated, isAuthenticated, router]);

  useEffect(() => {
    if (!isHydrated || !isAuthenticated) return;

    const fetchQuota = async () => {
      setLoading(true);
      try {
        const response = await api.getChallengeQuota();
        if (response.success && response.data) {
          setQuota(response.data.data);
        }
      } catch (err) {
        console.error('Error fetching quota:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuota();
  }, [isHydrated, isAuthenticated]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const isPaidUser = user?.subscription_tier === 'STANDARD' || user?.subscription_tier === 'PREMIUM';
  const shareUrl = createdCode ? `${typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'}/c/${createdCode}` : '';

  // Success state after creating challenge
  if (createdCode) {
    return (
      <MainLayout headerTitle="Challenge Created!">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-lg mx-auto text-center py-8"
        >
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <div className="text-6xl mb-4">🎉</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Challenge Created!</h1>
            <p className="text-gray-500 mb-6">Share this link with friends and family</p>

            {/* Share Code */}
            <div className="bg-purple-50 rounded-2xl p-6 mb-6">
              <div className="text-4xl font-mono font-bold text-purple-600 mb-2">{createdCode}</div>
              <div className="text-sm text-gray-500">bhashamitra.app/c/{createdCode}</div>
            </div>

            {/* Share Buttons */}
            <div className="space-y-3 mb-6">
              <ShareButton
                url={shareUrl}
                title="Play my BhashaMitra challenge!"
                className="w-full justify-center"
              />

              <button
                onClick={() => navigator.clipboard.writeText(shareUrl)}
                className="w-full py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full font-semibold transition-colors"
              >
                Copy Link
              </button>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => router.push(`/c/${createdCode}`)}
                className="flex-1 py-3 px-4 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-xl font-semibold transition-colors"
              >
                Preview
              </button>
              <button
                onClick={() => router.push('/challenges')}
                className="flex-1 py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition-colors"
              >
                My Challenges
              </button>
            </div>
          </div>
        </motion.div>
      </MainLayout>
    );
  }

  // Loading quota
  if (loading) {
    return (
      <MainLayout headerTitle="Create Challenge">
        <div className="py-12">
          <Loading size="lg" text="Loading..." />
        </div>
      </MainLayout>
    );
  }

  // Quota exceeded
  if (quota && !quota.can_create) {
    return (
      <MainLayout headerTitle="Create Challenge">
        <div className="max-w-lg mx-auto text-center py-8">
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <div className="text-6xl mb-4">⏰</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Daily Limit Reached</h1>
            <p className="text-gray-500 mb-6">
              Free users can create 2 challenges per day. Upgrade for unlimited challenges!
            </p>

            <button
              onClick={() => router.push('/subscription')}
              className="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-xl font-semibold transition-all mb-4"
            >
              Upgrade Now
            </button>

            <button
              onClick={() => router.push('/challenges')}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              Back to My Challenges
            </button>
          </div>
        </div>
      </MainLayout>
    );
  }

  // Create form
  return (
    <MainLayout headerTitle="Create Challenge">
      <div className="py-4">
        {/* Quota reminder */}
        {quota && !isPaidUser && (
          <div className="max-w-lg mx-auto mb-4 px-4 py-3 bg-blue-50 rounded-xl">
            <p className="text-sm text-blue-700">
              {quota.challenges_created_today}/2 daily challenges used. {quota.message}
            </p>
          </div>
        )}

        <CreateChallengeForm
          onSuccess={(code) => setCreatedCode(code)}
          onCancel={() => router.push('/challenges')}
          defaultLanguage={(activeChild?.language as string) || 'HINDI'}
        />
      </div>
    </MainLayout>
  );
}
