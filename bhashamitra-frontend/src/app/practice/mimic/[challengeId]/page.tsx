'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';
import { PeppiMimicChallengeWithProgress } from '@/types/mimic';

type PageState = 'loading' | 'ready' | 'listening' | 'recording' | 'processing' | 'error';

export default function MimicChallengePage() {
  const { challengeId } = useParams();
  const router = useRouter();

  // State
  const [pageState, setPageState] = useState<PageState>('loading');
  const [challenge, setChallenge] = useState<PeppiMimicChallengeWithProgress | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

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
      } catch (err) {
        setError('Network error');
        setPageState('error');
      }
    };

    if (childId) {
      fetchChallenge();
    }
  }, [challengeId, childId]);

  // Play Peppi's pronunciation
  const playPronunciation = async () => {
    if (!challenge?.audio_url) {
      // Fallback: Use TTS if no pre-recorded audio
      setIsPlaying(true);
      setPageState('listening');
      try {
        const result = await api.getAudio(challenge?.word || '', challenge?.language || 'HINDI', 'kid_friendly');
        if (result.success && result.audioUrl) {
          const audio = new Audio(result.audioUrl);
          audio.onended = () => {
            setIsPlaying(false);
            setPageState('ready');
          };
          audio.play();
        } else {
          setIsPlaying(false);
          setPageState('ready');
        }
      } catch {
        setIsPlaying(false);
        setPageState('ready');
      }
      return;
    }

    // Play pre-recorded audio
    setIsPlaying(true);
    setPageState('listening');
    const audio = new Audio(challenge.audio_url);
    audioRef.current = audio;
    audio.onended = () => {
      setIsPlaying(false);
      setPageState('ready');
    };
    audio.onerror = () => {
      setIsPlaying(false);
      setPageState('ready');
    };
    audio.play();
  };

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        stream.getTracks().forEach(track => track.stop());
        handleSubmitRecording(audioBlob);
      };

      mediaRecorder.start();
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
    } catch (err) {
      alert('Microphone access denied. Please allow microphone access to record.');
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
      alert('Please select a child profile first');
      return;
    }

    setPageState('processing');

    try {
      // 1. Upload the audio
      const uploadRes = await api.uploadMimicAudio(childId, blob) as any;

      if (!uploadRes?.success || !uploadRes?.data?.audio_url) {
        alert(uploadRes?.error || 'Upload failed');
        setPageState('ready');
        return;
      }

      // 2. Submit the attempt
      const submitRes = await api.submitMimicAttempt(
        childId,
        challengeId as string,
        {
          audio_url: uploadRes.data.audio_url,
          duration_ms: recordingTime * 1000
        }
      ) as any;

      if (submitRes?.success) {
        // Store result in sessionStorage for results page
        sessionStorage.setItem('mimicResult', JSON.stringify(submitRes.data));
        router.push(`/practice/mimic/results?id=${challengeId}`);
      } else {
        alert(submitRes?.error || 'Submission failed');
        setPageState('ready');
      }
    } catch (error) {
      console.error('Mimic error:', error);
      alert('An unexpected error occurred.');
      setPageState('ready');
    }
  };

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
  if (pageState === 'error') {
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
      <div className="max-w-lg mx-auto pt-8">
        {/* Header */}
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
            <p className="text-xl text-gray-600 mb-1">{challenge.romanization}</p>
            <p className="text-sm text-gray-500">"{challenge.meaning}"</p>
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
                Listening...
              </>
            ) : (
              <>
                <span>🔊</span>
                Listen to Peppi
              </>
            )}
          </button>
        </div>

        {/* Recording section */}
        <div className="bg-white rounded-3xl shadow-xl p-6">
          <h2 className="text-lg font-bold text-center text-gray-800 mb-4">
            {isRecording ? 'Recording...' : 'Your Turn!'}
          </h2>

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
              <div className="animate-spin rounded-full h-8 w-8 border-4 border-purple-500 border-t-transparent mx-auto mb-2"></div>
              <p className="text-purple-600 font-medium">Analyzing pronunciation...</p>
            </div>
          )}

          {/* Record button */}
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isPlaying || pageState === 'processing'}
            className={`w-full py-5 rounded-2xl font-bold text-xl flex items-center justify-center gap-3 transition-all ${
              isRecording
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white'
            } disabled:opacity-50`}
          >
            {isRecording ? (
              <>
                <span>⏹️</span>
                Stop Recording
              </>
            ) : (
              <>
                <span>🎤</span>
                Start Recording
              </>
            )}
          </button>

          <p className="text-center text-xs text-gray-400 mt-4">
            Tap to start, then say the word clearly. Recording stops automatically after 10 seconds.
          </p>
        </div>

        {/* Back button */}
        <button
          onClick={() => router.back()}
          className="mt-6 w-full py-3 bg-gray-100 text-gray-600 rounded-xl font-medium hover:bg-gray-200 transition-colors"
        >
          ← Back to Challenges
        </button>
      </div>
    </div>
  );
}