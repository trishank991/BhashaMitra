'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';
import { PeppiMimicChallengeWithProgress } from '@/types/mimic';

type PageState = 'loading' | 'no-child' | 'ready' | 'listening' | 'recording' | 'processing' | 'results' | 'error';

// Word comparison from pronunciation evaluation
interface WordComparison {
  expected: string;
  expected_roman: string;
  heard: string;
  heard_roman: string;
  is_correct: boolean;
  similarity: number;
  hint?: string | null;
}

// Result from the mimic attempt submission
interface MimicResult {
  attempt_id: string;
  transcription: string;
  score: number;
  stars: number;
  coach_tip?: string;
  points_earned: number;
  is_personal_best: boolean;
  mastered: boolean;
  peppi_feedback: string;
  share_message?: string;
  progress: {
    best_score: number;
    best_stars: number;
    total_attempts: number;
    mastered: boolean;
  };
  score_breakdown?: {
    stt_confidence: { raw: number; weighted: number; weight: number };
    text_match: { raw: number; weighted: number; weight: number };
    energy: { raw: number; weighted: number; weight: number };
    duration: { raw: number; weighted: number; weight: number };
  };
  // Enhanced evaluation fields (from transliteration service)
  evaluation?: {
    score: number;
    stars: number;
    is_correct: boolean;
    expected: { native: string; roman: string };
    heard: { native: string; roman: string };
    feedback: {
      level: string;
      emoji: string;
      message_hindi: string;
      message_english: string;
      encouragement: string;
    };
    word_comparison: WordComparison[];
    hints: string[];
  };
}

export default function MimicChallengePage() {
  const { challengeId } = useParams();
  const router = useRouter();

  // State
  const [pageState, setPageState] = useState<PageState>('loading');
  const [challenge, setChallenge] = useState<PeppiMimicChallengeWithProgress | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  // Result state - show inline instead of redirecting
  const [result, setResult] = useState<MimicResult | null>(null);
  const [attemptNumber, setAttemptNumber] = useState(1);

  // Recording
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Get child_id from auth store
  const activeChild = useAuthStore((state) => state.activeChild);
  const [childId, setChildId] = useState<string | null>(null);

  // Initialize childId
  useEffect(() => {
    const storedChildId = activeChild?.id || localStorage.getItem('current_child_id');
    if (storedChildId) {
      setChildId(storedChildId);
    } else {
      // No child selected - show helpful message instead of loading forever
      setPageState('no-child');
    }
  }, [activeChild]);

  // Fetch challenge details
  useEffect(() => {
    const fetchChallenge = async () => {
      if (!childId || !challengeId) return;

      try {
        const response = await api.getMimicChallengeDetail(challengeId as string, childId);
        if (response.success && response.data) {
          setChallenge(response.data);
          setPageState('ready');
        } else {
          setError(response.error || 'Failed to load challenge');
          setPageState('error');
        }
      } catch {
        setError('Network error');
        setPageState('error');
      }
    };

    if (childId) {
      fetchChallenge();
    }
  }, [challengeId, childId]);

  // Play Peppi's pronunciation
  const playPronunciation = useCallback(async () => {
    if (!challenge) return;

    setIsPlaying(true);
    if (pageState === 'ready') setPageState('listening');

    try {
      // Use pre-recorded audio if available, otherwise TTS
      if (challenge.audio_url) {
        const audio = new Audio(challenge.audio_url);
        audioRef.current = audio;
        audio.onended = () => {
          setIsPlaying(false);
          if (pageState === 'listening') setPageState('ready');
        };
        audio.onerror = () => {
          setIsPlaying(false);
          if (pageState === 'listening') setPageState('ready');
        };
        audio.play();
      } else {
        // Fallback: Use TTS
        const result = await api.getAudio(challenge.word || '', challenge.language || 'HINDI', 'kid_friendly');
        if (result.success && result.audioUrl) {
          const audio = new Audio(result.audioUrl);
          audio.onended = () => {
            setIsPlaying(false);
            if (pageState === 'listening') setPageState('ready');
          };
          audio.play();
        } else {
          setIsPlaying(false);
          if (pageState === 'listening') setPageState('ready');
        }
      }
    } catch {
      setIsPlaying(false);
      if (pageState === 'listening') setPageState('ready');
    }
  }, [challenge, pageState]);

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 48000,
        }
      });

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        stream.getTracks().forEach(track => track.stop());
        handleSubmitRecording(audioBlob);
      };

      mediaRecorder.start(100);
      setIsRecording(true);
      setPageState('recording');
      setRecordingTime(0);

      // Timer for recording duration
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      // Auto-stop after 10 seconds
      setTimeout(() => {
        if (mediaRecorderRef.current?.state === 'recording') {
          stopRecording();
        }
      }, 10000);
    } catch (err: unknown) {
      const error = err as { name?: string };
      if (error.name === 'NotAllowedError') {
        setError('Microphone permission denied. Please allow microphone access in your browser settings.');
      } else {
        setError('Could not access microphone. Please try again.');
      }
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  // Submit recording
  const handleSubmitRecording = async (blob: Blob) => {
    if (!childId) {
      setError('Please select a child profile first');
      setPageState('ready');
      return;
    }

    setPageState('processing');
    setError(null);

    try {
      // 1. Upload the audio
      const uploadRes = await api.uploadMimicAudio(childId, blob) as { success: boolean; data?: { audio_url: string }; error?: string };

      if (!uploadRes?.success || !uploadRes?.data?.audio_url) {
        setError(uploadRes?.error || 'Failed to upload audio. Please try again.');
        setPageState('ready');
        return;
      }

      // 2. Submit the attempt
      // Ensure duration_ms is at least 100 (backend minimum) and at most 10000 (backend maximum)
      const durationMs = Math.max(100, Math.min(10000, recordingTime * 1000 || 1000));

      const submitRes = await api.submitMimicAttempt(
        childId,
        challengeId as string,
        {
          audio_url: uploadRes.data.audio_url,
          duration_ms: durationMs
        }
      ) as { success: boolean; data?: MimicResult; error?: string };

      if (submitRes?.success && submitRes?.data) {
        // Show results inline instead of redirecting
        setResult(submitRes.data);
        setPageState('results');
      } else {
        setError(submitRes?.error || 'Could not analyze pronunciation. Please try again!');
        setPageState('ready');
      }
    } catch (err) {
      console.error('Mimic error:', err);
      setError('Something went wrong. Please try again!');
      setPageState('ready');
    }
  };

  // Try again - reset to ready state
  const handleTryAgain = () => {
    setResult(null);
    setError(null);
    setAttemptNumber(prev => prev + 1);
    setPageState('ready');
  };

  // No child selected state
  if (pageState === 'no-child') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-sm">
          <div className="text-5xl mb-4">👶</div>
          <h1 className="text-xl font-bold text-gray-900 mb-2">No Child Selected</h1>
          <p className="text-gray-500 mb-6">Please select a child profile to practice pronunciation.</p>
          <button
            onClick={() => router.push('/settings/children')}
            className="px-6 py-3 bg-purple-500 text-white rounded-full font-semibold"
          >
            Select Child
          </button>
        </div>
      </div>
    );
  }

  // Loading state
  if (pageState === 'loading' || !challenge) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading challenge...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (pageState === 'error' && !challenge) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-sm">
          <div className="text-5xl mb-4">😔</div>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Oops!</h1>
          <p className="text-gray-500 mb-6">{error}</p>
          <button
            onClick={() => router.back()}
            className="px-6 py-3 bg-purple-500 text-white rounded-full font-semibold"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 p-4">
      <div className="max-w-lg mx-auto pt-4 pb-8">
        {/* Back button header */}
        <button
          onClick={() => router.back()}
          className="mb-4 flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
        >
          <span>←</span>
          <span>Back to Challenges</span>
        </button>

        {/* Header card with word */}
        <div className="bg-white rounded-3xl shadow-xl p-6 mb-6">
          {/* Peppi intro */}
          <div className="text-center mb-6">
            <div className="text-6xl mb-2">🐱</div>
            <p className="text-gray-600 italic">
              {challenge.peppi_intro || "Listen carefully and repeat after me!"}
            </p>
          </div>

          {/* Word display */}
          <div className="text-center mb-6 p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl">
            <p className="text-5xl font-bold text-purple-800 mb-2">{challenge.word}</p>
            <p className="text-xl text-gray-600 mb-1">({challenge.romanization})</p>
            <p className="text-sm text-gray-500">&ldquo;{challenge.meaning}&rdquo;</p>
          </div>

          {/* Listen button */}
          <button
            onClick={playPronunciation}
            disabled={isPlaying || isRecording || pageState === 'processing'}
            className={`w-full py-4 rounded-2xl font-bold text-lg flex items-center justify-center gap-3 transition-all ${
              isPlaying
                ? 'bg-green-100 text-green-700'
                : 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600'
            } disabled:opacity-50`}
          >
            {isPlaying ? (
              <>
                <span className="animate-pulse">🔊</span>
                Playing...
              </>
            ) : (
              <>
                <span>🔊</span>
                Listen to Peppi
              </>
            )}
          </button>
        </div>

        {/* Recording section - show when not in results state */}
        {pageState !== 'results' && (
          <div className="bg-white rounded-3xl shadow-xl p-6 mb-6">
            <h2 className="text-lg font-bold text-center text-gray-800 mb-4">
              {isRecording ? '🔴 Recording...' : '🎤 Your Turn!'}
            </h2>

            {/* Error message */}
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-center">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            {/* Recording indicator */}
            {isRecording && (
              <div className="text-center mb-4">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-red-100 rounded-full">
                  <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
                  <span className="text-red-700 font-medium">{recordingTime}s</span>
                </div>
              </div>
            )}

            {/* Processing indicator */}
            {pageState === 'processing' && (
              <div className="text-center mb-4">
                <div className="animate-spin rounded-full h-10 w-10 border-4 border-purple-500 border-t-transparent mx-auto mb-3"></div>
                <p className="text-purple-600 font-medium">🎧 Analyzing your pronunciation...</p>
              </div>
            )}

            {/* Big microphone button */}
            <div className="flex justify-center mb-4">
              <button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isPlaying || pageState === 'processing'}
                className={`w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl ${
                  isRecording
                    ? 'bg-gradient-to-r from-red-500 to-red-600 scale-110'
                    : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105'
                } disabled:opacity-50 disabled:scale-100`}
                style={{
                  animation: isRecording ? 'pulse 1s infinite' : 'none'
                }}
              >
                {pageState === 'processing' ? (
                  <span className="text-5xl">⏳</span>
                ) : isRecording ? (
                  <span className="text-5xl">⏹️</span>
                ) : (
                  <span className="text-5xl">🎤</span>
                )}
              </button>
            </div>

            {/* Instructions */}
            <p className="text-center text-gray-600">
              {pageState === 'processing'
                ? 'Please wait...'
                : isRecording
                  ? 'Tap to stop recording'
                  : 'Tap the microphone and say the word!'
              }
            </p>

            <p className="text-center text-xs text-gray-400 mt-2">
              Recording stops automatically after 10 seconds
            </p>
          </div>
        )}

        {/* Results section - show inline */}
        {pageState === 'results' && result && (
          <div className="bg-white rounded-3xl shadow-xl p-6 mb-6">
            {/* Score display */}
            <div className="text-center mb-6">
              {/* Emoji feedback */}
              <div className="text-7xl mb-3">
                {result.evaluation?.feedback?.emoji ||
                  (result.stars >= 3 ? '🌟' : result.stars >= 2 ? '⭐' : result.stars >= 1 ? '👍' : '💪')}
              </div>

              {/* Stars */}
              <div className="flex justify-center gap-2 mb-3">
                {[1, 2, 3].map((star) => (
                  <span
                    key={star}
                    className={`text-4xl transition-all ${
                      star <= result.stars ? 'scale-100' : 'scale-75 grayscale opacity-30'
                    }`}
                  >
                    ⭐
                  </span>
                ))}
              </div>

              {/* Score percentage */}
              <div className="text-5xl font-bold text-purple-600 mb-2">
                {result.score}%
              </div>

              {/* Points earned */}
              {result.points_earned > 0 && (
                <p className="text-green-600 font-medium">+{result.points_earned} points!</p>
              )}

              {/* Personal best badge */}
              {result.is_personal_best && (
                <div className="inline-block mt-2 px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm font-medium">
                  🏆 Personal Best!
                </div>
              )}
            </div>

            {/* Feedback messages */}
            <div className="text-center mb-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl">
              {result.evaluation?.feedback ? (
                <>
                  <p className="text-2xl font-bold text-purple-700 mb-1">
                    {result.evaluation.feedback.message_hindi}
                  </p>
                  <p className="text-lg text-gray-600 mb-2">
                    {result.evaluation.feedback.message_english}
                  </p>
                  <p className="text-pink-600">
                    {result.evaluation.feedback.encouragement}
                  </p>
                </>
              ) : (
                <p className="text-lg text-purple-700">{result.peppi_feedback}</p>
              )}
            </div>

            {/* What you said */}
            <div className="bg-gray-50 rounded-xl p-4 mb-4 text-center">
              <p className="text-sm text-gray-500 mb-1">You said:</p>
              <p className="text-2xl font-bold text-gray-800">
                {result.evaluation?.heard?.native || result.transcription || '(no speech detected)'}
              </p>
              {result.evaluation?.heard?.roman && (
                <p className="text-purple-600">({result.evaluation.heard.roman})</p>
              )}
            </div>

            {/* Word comparison */}
            {result.evaluation?.word_comparison && result.evaluation.word_comparison.length > 0 && (
              <div className="mb-4">
                <p className="text-sm text-gray-500 text-center mb-2">Word by word:</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {result.evaluation.word_comparison.map((word, index) => (
                    <div
                      key={index}
                      className={`px-3 py-2 rounded-lg text-center min-w-[60px] ${
                        word.is_correct
                          ? 'bg-green-100 border border-green-300'
                          : 'bg-red-100 border border-red-300'
                      }`}
                    >
                      <div className="flex items-center justify-center mb-1">
                        {word.is_correct ? (
                          <span className="text-green-600">✓</span>
                        ) : (
                          <span className="text-red-600">✗</span>
                        )}
                      </div>
                      <p className="font-bold text-sm">{word.expected}</p>
                      <p className="text-xs text-gray-600">({word.expected_roman})</p>
                      {word.hint && !word.is_correct && (
                        <p className="text-xs text-red-600 mt-1">💡 {word.hint}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Pronunciation hints */}
            {result.evaluation?.hints && result.evaluation.hints.length > 0 && (
              <div className="bg-yellow-50 rounded-xl p-4 mb-4 border border-yellow-200">
                <p className="text-sm font-medium text-yellow-800 mb-2">💡 Tips to improve:</p>
                <ul className="text-yellow-700 text-sm space-y-1">
                  {result.evaluation.hints.map((hint, index) => (
                    <li key={index}>• {hint}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Coach tip */}
            {result.coach_tip && (
              <div className="bg-blue-50 rounded-xl p-4 mb-4 border border-blue-200">
                <p className="text-sm font-medium text-blue-800 mb-1">🎯 Coach&apos;s Tip:</p>
                <p className="text-blue-700 text-sm">{result.coach_tip}</p>
              </div>
            )}

            {/* Score breakdown (optional - for advanced users) */}
            {result.score_breakdown && (
              <details className="mb-4">
                <summary className="text-sm text-gray-500 cursor-pointer hover:text-gray-700">
                  View score breakdown
                </summary>
                <div className="mt-2 p-3 bg-gray-50 rounded-lg text-sm space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Speech Confidence</span>
                    <span className="font-medium">{Math.round(result.score_breakdown.stt_confidence.raw * 100)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Text Match</span>
                    <span className="font-medium">{Math.round(result.score_breakdown.text_match.raw)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Audio Energy</span>
                    <span className="font-medium">{Math.round(result.score_breakdown.energy.raw)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Duration Match</span>
                    <span className="font-medium">{Math.round(result.score_breakdown.duration.raw)}%</span>
                  </div>
                </div>
              </details>
            )}

            {/* Action buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleTryAgain}
                className="flex-1 py-4 rounded-2xl font-bold text-lg bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 transition-all flex items-center justify-center gap-2"
              >
                <span>🔄</span>
                Try Again
              </button>

              {result.stars >= 2 && (
                <button
                  onClick={() => router.push('/practice/mimic')}
                  className="flex-1 py-4 rounded-2xl font-bold text-lg bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600 transition-all flex items-center justify-center gap-2"
                >
                  <span>→</span>
                  Next Challenge
                </button>
              )}
            </div>
          </div>
        )}

        {/* Attempt counter */}
        {attemptNumber > 1 && (
          <p className="text-center text-gray-400 text-sm">
            Attempt #{attemptNumber}
          </p>
        )}
      </div>

      {/* CSS for pulse animation */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1.1); }
          50% { transform: scale(1.15); }
        }
      `}</style>
    </div>
  );
}