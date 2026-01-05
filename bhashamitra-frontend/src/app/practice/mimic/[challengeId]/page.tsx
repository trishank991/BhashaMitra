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
    try {
      // 1. Upload the audio file
      const uploadRes = await api.uploadMimicAudio(challengeId as string, blob) as any;

      if (!uploadRes?.success || !uploadRes?.data?.audio_url) {
        alert(uploadRes?.error || "Upload failed");
        setIsUploading(false);
        return;
      }

      // 2. Submit the attempt
      // FIXED: Changed from passing an object to passing 3 positional arguments 
      // as required by your api.ts definition.
      const submitRes = await api.submitMimicAttempt(
        challengeId as string,                                      // Arg 1: challenge_id
        localStorage.getItem('current_child_id') || 'default',      // Arg 2: child_id
        uploadRes.data.audio_url                                    // Arg 3: audio_url
      ) as any;

      if (submitRes?.success) {
        router.push(`/practice/mimic/results?id=${challengeId}`);
      } else {
        alert(submitRes?.error || "Submission failed");
      }
    } catch (error) {
      console.error("Mimic error:", error);
      alert("An unexpected error occurred.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-10 text-center">
      <h1 className="text-2xl font-bold mb-4">Mimic Challenge</h1>
      {/* Visual audio feedback/recorder would trigger handleStopRecording(blob) 
          Ensure your recorder component calls handleStopRecording with the generated blob.
      */}
      {isUploading && (
        <div className="mt-4">
          <p className="text-blue-500 animate-pulse font-medium">Processing Audio...</p>
          <p className="text-xs text-gray-500">Evaluating pronunciation and fluency...</p>
        </div>
      )}
    </div>
  );
}
