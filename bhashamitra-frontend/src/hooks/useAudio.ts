'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { api } from '@/lib/api';

type VoiceStyle = 'kid_friendly' | 'calm_story' | 'enthusiastic' | 'male_teacher';

interface UseAudioOptions {
  language?: string;
  voiceStyle?: VoiceStyle;
}

interface UseAudioReturn {
  isPlaying: boolean;
  isLoading: boolean;
  error: string | null;
  playAudio: (text: string) => Promise<void>;
  stopAudio: () => void;
}

/**
 * Hook for playing TTS audio with kid-friendly voices
 *
 * Uses Indic Parler-TTS for expressive, engaging voices
 * perfect for children's language learning.
 */
export function useAudio(options: UseAudioOptions = {}): UseAudioReturn {
  const { language = 'HINDI', voiceStyle = 'kid_friendly' } = options;

  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioUrlRef = useRef<string | null>(null);
  // Guard to prevent double API calls (React 18 Strict Mode issue)
  const isRequestInProgressRef = useRef(false);
  const lastTextRef = useRef<string | null>(null);

  // Cleanup audio URL on unmount
  useEffect(() => {
    return () => {
      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
      isRequestInProgressRef.current = false;
    };
  }, []);

  const stopAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
  }, []);

  const playAudio = useCallback(async (text: string) => {
    if (!text.trim()) {
      return;
    }

    // Prevent duplicate requests for the same text within a short window
    // This handles React 18 Strict Mode double-invoke
    if (isRequestInProgressRef.current && lastTextRef.current === text) {
      return;
    }

    // Mark request as in progress
    isRequestInProgressRef.current = true;
    lastTextRef.current = text;

    // Stop any currently playing audio - inline to avoid circular dependency
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);

    setIsLoading(true);
    setError(null);

    try {
      const result = await api.getAudio(text, language, voiceStyle);

      if (!result.success || !result.audioUrl) {
        setError(result.error || 'Failed to generate audio');
        setIsLoading(false);
        return;
      }

      // Cleanup previous audio URL
      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
      audioUrlRef.current = result.audioUrl;

      // Create and play audio
      const audio = new Audio(result.audioUrl);
      audioRef.current = audio;

      audio.onplay = () => {
        setIsPlaying(true);
        setIsLoading(false);
      };

      audio.onended = () => {
        setIsPlaying(false);
        isRequestInProgressRef.current = false;
      };

      audio.onerror = () => {
        setError('Failed to play audio');
        setIsPlaying(false);
        setIsLoading(false);
        isRequestInProgressRef.current = false;
      };

      await audio.play();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to play audio');
      setIsLoading(false);
      isRequestInProgressRef.current = false;
    }
  }, [language, voiceStyle]);

  return {
    isPlaying,
    isLoading,
    error,
    playAudio,
    stopAudio,
  };
}

export default useAudio;
