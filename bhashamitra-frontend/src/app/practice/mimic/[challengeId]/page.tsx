'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';

export default function MimicChallengePage() {
  const { challengeId } = useParams();
  const router = useRouter();
  const [isUploading, setIsUploading] = useState(false);

  // Get child_id from auth store or localStorage
  const activeChild = useAuthStore((state) => state.activeChild);
  const [childId, setChildId] = useState<string | null>(null);

  useEffect(() => {
    // Get child ID from store or localStorage
    const storedChildId = activeChild?.id || localStorage.getItem('current_child_id');
    if (storedChildId) {
      setChildId(storedChildId);
    }
  }, [activeChild]);

  const handleStopRecording = async (blob: Blob, durationMs: number = 3000) => {
    if (!childId) {
      alert("Please select a child profile first");
      return;
    }

    setIsUploading(true);
    try {
      // 1. Upload the audio file - FIXED: pass childId instead of challengeId
      const uploadRes = await api.uploadMimicAudio(childId, blob) as any;

      if (!uploadRes?.success || !uploadRes?.data?.audio_url) {
        alert(uploadRes?.error || "Upload failed");
        setIsUploading(false);
        return;
      }

      // 2. Submit the attempt
      const submitRes = await api.submitMimicAttempt(
        childId,                                                     // Arg 1: child_id
        challengeId as string,                                       // Arg 2: challenge_id
        {
          audio_url: uploadRes.data.audio_url,
          duration_ms: durationMs
        }                                                            // Arg 3: data object
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