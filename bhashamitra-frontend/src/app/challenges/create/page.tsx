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
    const fetchQuota = async () => {
      try {
        setIsLoading(true);
        const res = await api.getChallengeQuota();
        
        // Logic: Support both 'any' casting and strict typing while drilling into data
        if (res?.success && res?.data) {
          const quotaData = (res.data as any).data || res.data;
          setQuota(quotaData);
        } else {
          throw new Error(res.error || 'Failed to fetch challenge quota.');
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred.';
        setError(errorMessage);
        console.error("Failed to fetch quota", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchQuota();
  }, []);

  // Logic: Calculate daily limit display string
  // Casting to 'any' bypasses the strict check for this one line
const dailyLimit = quota ? ((quota as any).daily_limit === null ? 'unlimited' : (quota as any).daily_limit) : 0;

  return (
    <div className="max-w-2xl mx-auto p-4 sm:p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">New Challenge</h1>
        
        {/* Logic: Show spinner while loading quota */}
        {isLoading && (
          <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Loading your quota...</span>
          </div>
        )}
        
        {/* Logic: Show error if fetch fails */}
        {error && (
          <p className="mt-2 text-sm text-red-600">Could not load quota: {error}</p>
        )}
        
        {/* Logic: Display usage stats once loaded */}
        {quota && !isLoading && (
          <p className="mt-2 text-sm text-blue-600">
            You have created {quota.challenges_created_today ?? 0} of {(quota as any).daily_limit ?? 2} challenges today.
          </p>
        )}
      </div>

      <CreateChallengeForm
        onSuccess={(code: string) => router.push(`/c/${code}`)}
        onCancel={() => router.back()}
        /* Logic: fallback to false if quota object is missing */
        canCreate={quota?.can_create ?? false}
        isQuotaLoading={isLoading}
      />
    </div>
  );
}
