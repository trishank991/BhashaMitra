'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api, { ChallengeQuotaResponse } from '@/lib/api';
import CreateChallengeForm from '@/components/challenges/CreateChallengeForm';

export default function CreateChallengePage() {
  const router = useRouter();
  const [quota, setQuota] = useState<ChallengeQuotaResponse | null>(null);

  useEffect(() => {
    async function fetchQuota() {
      const res = await api.getChallengeQuota();
      if (res.success && res.data) setQuota(res.data);
    }
    fetchQuota();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">New Challenge</h1>
      {quota && <p className="mb-4 text-sm text-blue-600">Created {quota.challenges_created_today} of {quota.daily_limit} today.</p>}
      <CreateChallengeForm 
        onSuccess={(code: string) => router.push(`/challenges/manage/${code}`)} 
        onCancel={() => router.back()} 
      />
    </div>
  );
}
