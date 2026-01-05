'use client';

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function MimicChallengePage() {
  const { challengeId } = useParams();
  const router = useRouter();
  const [isUploading, setIsUploading] = useState(false);

  const handleStopRecording = async (blob: Blob) => {
    setIsUploading(true);
    const uploadRes = await api.uploadMimicAudio(challengeId as string, blob);

    if (!uploadRes.success || !uploadRes.data) {
      alert(uploadRes.error || "Upload failed");
      setIsUploading(false);
      return;
    }

    const submitRes = await api.submitMimicAttempt({
      challenge_id: challengeId as string,
      child_id: localStorage.getItem('current_child_id') || 'default',
      audio_url: uploadRes.data.audio_url
    });

    if (submitRes.success) router.push(`/practice/mimic/results?id=${challengeId}`);
    else alert(submitRes.error || "Submission failed");
    setIsUploading(false);
  };

  return (
    <div className="p-10 text-center">
      <h1 className="text-2xl font-bold mb-4">Mimic Challenge</h1>
      {/* Visual audio feedback/recorder would trigger handleStopRecording(blob) */}
      {isUploading && <p className="text-blue-500 animate-pulse">Processing Audio...</p>}
    </div>
  );
}
