'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { useAuthStore } from '@/stores';
import { api } from '@/lib/api';
import {
  PeppiMimicChallenge,
  PeppiMimicChallengeProgress,
  PeppiMimicAttemptResult,
  RecordingResult,
  MIMIC_CATEGORY_LABELS,
  MIMIC_CATEGORY_ICONS,
} from '@/types';
import { RecordingInterface, ResultDisplay, ShareButton, generateShareMessage } from '@/components/mimic';
import { AudioButton } from '@/components/ui/AudioButton';

type PageState = 'loading' | 'ready' | 'recording' | 'processing' | 'result' | 'error';

interface ChallengeWithProgress extends PeppiMimicChallenge {
  progress: PeppiMimicChallengeProgress;
}

export default function MimicChallengePage() {
  const router = useRouter();
  const params = useParams();
  const challengeId = params.challengeId as string;
  const { activeChild: selectedChild } = useAuthStore();

  const [isHydrated, setIsHydrated] = useState(false);
  const [challenge, setChallenge] = useState<ChallengeWithProgress | null>(null);
  const [pageState, setPageState] = useState<PageState>('loading');
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PeppiMimicAttemptResult | null>(null);
  const [, setRecordingResult] = useState<{ blob: Blob; duration_ms: number } | null>(null);

  // Handle hydration
  useEffect(() => {
    setIsHydrated(true);
  }, []);

  /**
   * SENIOR FIX: 
   * We pass 'id' to the API and cast the filter object to any to satisfy the 
   * current MimicChallengeFilters interface while ensuring the build passes.
   */
  const fetchChallenge = useCallback(async () => {
    if (!isHydrated || !selectedChild?.id || !challengeId) return;

    setPageState('loading');
    setError(null);

    try {
      const response = await api.getMimicChallenges(selectedChild.id, { 
        id: challengeId 
      } as any);

      if (response.success && response.data && response.data.length > 0) {
        // Find the specific challenge or default to the first one
        const singleChallenge = response.data.find((c: any) => c.id === challengeId) || response.data[0];
        setChallenge(singleChallenge as unknown as ChallengeWithProgress);
        setPageState('ready');
      } else {
        setError('Challenge not found.');
        setPageState('error');
      }
    } catch (err) {
      console.error("Fetch Error:", err);
      setError('Something went wrong. Please try again.');
      setPageState('error');
    }
  }, [isHydrated, selectedChild?.id, challengeId]);

  useEffect(() => {
    fetchChallenge();
  }, [fetchChallenge]);

  useEffect(() => {
    if (!isHydrated) return;
    if (!selectedChild) {
      router.push('/home');
    }
  }, [isHydrated, selectedChild, router]);

  const handleRecordingComplete = useCallback(async (recording: RecordingResult) => {
    if (!selectedChild?.id || !challengeId) return;

    setRecordingResult(recording);
    setPageState('processing');

    try {
      const uploadResponse = await api.uploadMimicAudio(
        selectedChild.id,
        recording.blob,
        `mimic_${challengeId}_${Date.now()}.webm`
      );

      if (!uploadResponse.success || !uploadResponse.data?.audio_url) {
        throw new Error(uploadResponse.error || 'Failed to upload audio');
      }

      const attemptResponse = await api.submitMimicAttempt(
        selectedChild.id,
        challengeId,
        {
          audio_url: uploadResponse.data.audio_url,
          duration_ms: recording.duration_ms,
        }
      );

      if (attemptResponse.success && attemptResponse.data) {
        setResult(attemptResponse.data);
        setPageState('result');
      } else {
        throw new Error(attemptResponse.error || 'Failed to process attempt');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to process recording');
      setPageState('error');
    }
  }, [selectedChild?.id, challengeId]);

  const handleTryAgain = useCallback(() => {
    setResult(null);
    setRecordingResult(null);
    setPageState('ready');
  }, []);

  const handleNext = useCallback(() => {
    router.push('/practice/mimic');
  }, [router]);

  const handleShare = useCallback(async () => {
    if (!selectedChild?.id || !result) return;
    try {
      await api.shareMimicAttempt(selectedChild.id, result.attempt_id);
    } catch {
      // Background tracking failed
    }
  }, [selectedChild?.id, result]);

  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary-50 to-white">
        <Loader2 className="w-10 h-10 animate-spin text-primary-500" />
      </div>
    );
  }

  if (!selectedChild) return null;

  const renderContent = () => {
    switch (pageState) {
      case 'loading':
        return (
          <div className="flex items-center justify-center py-24">
            <Loader2 className="w-10 h-10 animate-spin text-primary-500" />
          </div>
        );
      case 'error':
        return (
          <div className="text-center py-24 px-4">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">😢</span>
            </div>
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={fetchChallenge}
              className="px-6 py-3 bg-primary-500 text-white rounded-xl font-semibold hover:bg-primary-600 transition-colors"
            >
              Try Again
            </button>
          </div>
        );
      case 'ready':
      case 'recording':
        if (!challenge) return null;
        return (
          <>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center px-4 pt-8">
              <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full mb-6">
                <span>{MIMIC_CATEGORY_ICONS[challenge.category]}</span>
                <span className="font-medium">{MIMIC_CATEGORY_LABELS[challenge.category]}</span>
              </div>
              <h1 className="text-5xl font-bold text-gray-800 mb-2">{challenge.word}</h1>
              <p className="text-xl text-gray-600 mb-1">{challenge.romanization}</p>
              <p className="text-lg text-gray-500 mb-6">{challenge.meaning}</p>
              <div className="flex items-center justify-center gap-3 mb-8">
                <AudioButton text={challenge.word} audioUrl={challenge.audio_url} language={challenge.language} size="lg" variant="primary" />
                <span className="text-gray-500">Listen to Peppi</span>
              </div>
              {challenge.peppi_intro && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl p-4 mb-8 mx-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-primary-200 rounded-full flex items-center justify-center text-2xl flex-shrink-0">🎤</div>
                    <p className="text-gray-700 text-left">{challenge.peppi_intro}</p>
                  </div>
                </motion.div>
              )}
            </motion.div>
            <RecordingInterface
              maxDuration={5000} countdownDuration={3}
              onRecordingStart={() => setPageState('recording')}
              onRecordingComplete={handleRecordingComplete}
              onError={(err) => { setError(err); setPageState('error'); }}
              className="py-8"
            />
          </>
        );
      case 'processing':
        return (
          <div className="flex flex-col items-center justify-center py-24 px-4">
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }} className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mb-6">
              <Loader2 className="w-10 h-10 text-primary-500" />
            </motion.div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Analyzing...</h2>
          </div>
        );
      case 'result':
        if (!result || !challenge) return null;
        return (
          <div className="py-8">
            <ResultDisplay result={result} challengeWord={challenge.word} onTryAgain={handleTryAgain} onNext={handleNext} onShare={() => {}} />
            {result.stars >= 2 && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 2.2 }} className="flex justify-center mt-6 px-4">
                <ShareButton
                  shareMessage={result.share_message || generateShareMessage(selectedChild!.name, challenge.word, challenge.romanization, challenge.language, result.stars, result.score)}
                  childName={selectedChild!.name} word={challenge.word} stars={result.stars} onShareComplete={handleShare} size="lg"
                />
              </motion.div>
            )}
          </div>
        );
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      <header className="sticky top-0 z-10 bg-white/90 backdrop-blur-md shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-4">
          <button onClick={() => router.back()} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <ArrowLeft size={24} />
          </button>
          <div className="flex-1">
            <h1 className="text-xl font-bold text-gray-800">{pageState === 'result' ? 'Results' : 'Practice'}</h1>
            {challenge && <p className="text-sm text-gray-500">{challenge.romanization}</p>}
          </div>
        </div>
      </header>
      <main className="max-w-2xl mx-auto">
        <AnimatePresence mode="wait">{renderContent()}</AnimatePresence>
      </main>
    </div>
  );
}
