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

  // Cleanup audio URL on unmount
  useEffect(() => {
    return () => {
      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
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
      console.log('[useAudio] Empty text, skipping');
      return;
    }

    console.log('[useAudio] playAudio called:', { text, language, voiceStyle });

    // Stop any currently playing audio - inline to avoid circular dependency
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);

    setIsLoading(true);
    setError(null);

    try {
      console.log('[useAudio] Calling api.getAudio...');
      const result = await api.getAudio(text, language, voiceStyle);
      console.log('[useAudio] api.getAudio result:', { success: result.success, hasAudioUrl: !!result.audioUrl, error: result.error });

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
      };

      audio.onerror = () => {
        setError('Failed to play audio');
        setIsPlaying(false);
        setIsLoading(false);
      };

      await audio.play();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to play audio');
      setIsLoading(false);
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
