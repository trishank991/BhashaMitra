'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import api, { ChallengeResponse, ChallengeQuotaResponse } from '@/lib/api';
import { MainLayout } from '@/components/layout';
import { ChallengeCard } from '@/components/challenges/ChallengeCard';
import { Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';

export default function ChallengesPage() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const [isHydrated, setIsHydrated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [challenges, setChallenges] = useState<ChallengeResponse[]>([]);
  const [quota, setQuota] = useState<ChallengeQuotaResponse | null>(null);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login?redirect=/challenges');
    }
  }, [isHydrated, isAuthenticated, router]);

  useEffect(() => {
    if (!isHydrated || !isAuthenticated) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        const [challengesRes, quotaRes] = await Promise.all([
          api.getMyChallenges(),
          api.getChallengeQuota(),
        ]);

        if (challengesRes.success && challengesRes.data) {
          setChallenges(challengesRes.data.data || []);
        }
        if (quotaRes.success && quotaRes.data) {
          setQuota(quotaRes.data.data);
        }
      } catch (err) {
        console.error('Error fetching challenges:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isHydrated, isAuthenticated]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const isPaidUser = user?.subscription_tier === 'STANDARD' || user?.subscription_tier === 'PREMIUM';

  return (
    <MainLayout headerTitle="My Challenges">
      <div className="space-y-6">
        {/* Header with Create Button */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Challenges</h1>
            <p className="text-gray-500">Create quizzes and share with friends</p>
          </div>
          <button
            onClick={() => router.push('/challenges/create')}
            disabled={quota ? !quota.can_create : false}
            className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-300 disabled:to-gray-400 text-white rounded-xl font-semibold transition-all shadow-lg"
          >
            + Create
          </button>
        </div>

        {/* Quota Info */}
        {quota && (
          <div className={`p-4 rounded-xl ${quota.can_create ? 'bg-green-50' : 'bg-amber-50'}`}>
            <div className="flex items-center justify-between">
              <div>
                <p className={`font-medium ${quota.can_create ? 'text-green-700' : 'text-amber-700'}`}>
                  {quota.message}
                </p>
                {!isPaidUser && (
                  <p className="text-sm text-gray-500 mt-1">
                    {quota.challenges_created_today}/2 daily challenges used
                  </p>
                )}
              </div>
              {!isPaidUser && !quota.can_create && (
                <button
                  onClick={() => router.push('/pricing')}
                  className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-sm font-medium"
                >
                  Upgrade
                </button>
              )}
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="py-12">
            <Loading size="lg" text="Loading challenges..." />
          </div>
        )}

        {/* Empty State */}
        {!loading && challenges.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="text-6xl mb-4">🎯</div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">No Challenges Yet</h2>
            <p className="text-gray-500 mb-6">
              Create your first challenge and share it with friends!
            </p>
            <button
              onClick={() => router.push('/challenges/create')}
              className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-xl font-semibold"
            >
              Create Your First Challenge
            </button>
          </motion.div>
        )}

        {/* Challenge Grid */}
        {!loading && challenges.length > 0 && (
          <div className="grid gap-4 md:grid-cols-2">
            {challenges.map((challenge, index) => (
              <motion.div
                key={challenge.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <ChallengeCard
                  challenge={challenge}
                  onView={(code) => router.push(`/c/${code}`)}
                />
              </motion.div>
            ))}
          </div>
        )}

        {/* Stats Summary */}
        {!loading && challenges.length > 0 && (
          <div className="bg-gradient-to-r from-purple-100 to-pink-100 rounded-2xl p-6">
            <h3 className="font-bold text-gray-900 mb-4">Your Stats</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{challenges.length}</div>
                <div className="text-sm text-gray-500">Challenges</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-pink-600">
                  {challenges.reduce((sum, c) => sum + c.total_completions, 0)}
                </div>
                <div className="text-sm text-gray-500">Total Plays</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {challenges.reduce((sum, c) => sum + c.participant_count, 0)}
                </div>
                <div className="text-sm text-gray-500">Players</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
