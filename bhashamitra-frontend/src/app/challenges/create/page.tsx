'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import type { ChallengeQuotaResponse } from '@/lib/api';
import CreateChallengeForm from '@/components/challenges/CreateChallengeForm';
import { Loader2 } from 'lucide-react';

export default function CreateChallengePage() {
  const router = useRouter();
  const [quota, setQuota] = useState<ChallengeQuotaResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchQuota() {
      try {
        setIsLoading(true);
        const res = await api.getChallengeQuota();
        if (res.success && res.data?.data) {
          setQuota(res.data.data);
        } else {
          throw new Error(res.error || 'Failed to fetch challenge quota.');
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred.';
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    }
    fetchQuota();
  }, []);

  const dailyLimit = quota ? (quota.daily_limit === null ? 'unlimited' : quota.daily_limit) : 0;

  return (
    <div className="max-w-2xl mx-auto p-4 sm:p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">New Challenge</h1>
        {isLoading && (
          <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Loading your quota...</span>
          </div>
        )}
        {error && <p className="mt-2 text-sm text-red-600">Could not load quota: {error}</p>}
        {quota && (
          <p className="mt-2 text-sm text-blue-600">
            You have created {quota.challenges_created_today} of {dailyLimit} challenges today.
          </p>
        )}
      </div>
      <CreateChallengeForm 
        onSuccess={(code: string) => router.push(`/challenges/manage/${code}`)} 
        onCancel={() => router.back()} 
        canCreate={quota?.can_create ?? false}
        isQuotaLoading={isLoading}
      />
    </div>
  );
}
