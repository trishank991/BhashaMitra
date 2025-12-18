'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Volume2, VolumeX, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { api } from '@/lib/api';

interface AudioButtonProps {
  text?: string;
  audioUrl?: string;
  language?: string;
  voiceStyle?: 'kid_friendly' | 'calm_story' | 'enthusiastic' | 'male_teacher';
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'ghost';
  autoPlay?: boolean;
  className?: string;
  onPlayStart?: () => void;
  onPlayEnd?: () => void;
  onError?: (error: string) => void;
}

const sizeStyles = {
  sm: 'w-8 h-8',
  md: 'w-12 h-12',
  lg: 'w-16 h-16',
};

const iconSizes = {
  sm: 16,
  md: 24,
  lg: 32,
};

const variantStyles = {
  primary: 'bg-primary-500 hover:bg-primary-600 text-white shadow-md',
  secondary: 'bg-secondary-100 hover:bg-secondary-200 text-secondary-700',
  ghost: 'bg-transparent hover:bg-gray-100 text-gray-600',
};

export function AudioButton({
  text,
  audioUrl,
  language = 'HINDI',
  voiceStyle = 'kid_friendly',
  size = 'md',
  variant = 'primary',
  autoPlay = false,
  className,
  onPlayStart,
  onPlayEnd,
  onError,
}: AudioButtonProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioUrlRef = useRef<string | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (audioUrlRef.current && !audioUrl) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, [audioUrl]);

  // Auto-play on mount if enabled
  useEffect(() => {
    if (autoPlay && (text || audioUrl)) {
      playAudio();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoPlay]);

  const playAudio = useCallback(async () => {
    if (isLoading || isPlaying) return;
    if (!text && !audioUrl) return;

    setIsLoading(true);

    try {
      let urlToPlay = audioUrl;

      // If no direct URL, generate via TTS
      if (!urlToPlay && text) {
        const result = await api.getAudio(text, language, voiceStyle);
        if (!result.success || !result.audioUrl) {
          throw new Error(result.error || 'Failed to generate audio');
        }
        urlToPlay = result.audioUrl;
        audioUrlRef.current = result.audioUrl;
      }

      if (!urlToPlay) {
        throw new Error('No audio source available');
      }

      // Create and play audio
      const audio = new Audio(urlToPlay);
      audioRef.current = audio;

      audio.onplay = () => {
        setIsPlaying(true);
        setIsLoading(false);
        onPlayStart?.();
      };

      audio.onended = () => {
        setIsPlaying(false);
        onPlayEnd?.();
      };

      audio.onerror = () => {
        setIsPlaying(false);
        setIsLoading(false);
        onError?.('Failed to play audio');
      };

      await audio.play();
    } catch (error) {
      setIsLoading(false);
      setIsPlaying(false);
      onError?.(error instanceof Error ? error.message : 'Audio playback failed');
    }
  }, [text, audioUrl, language, voiceStyle, isLoading, isPlaying, onPlayStart, onPlayEnd, onError]);

  const stopAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
  }, []);

  const handleClick = () => {
    if (isPlaying) {
      stopAudio();
    } else {
      playAudio();
    }
  };

  return (
    <motion.button
      onClick={handleClick}
      disabled={isLoading}
      className={cn(
        'rounded-full flex items-center justify-center transition-all',
        sizeStyles[size],
        variantStyles[variant],
        isLoading && 'opacity-70 cursor-wait',
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      animate={isPlaying ? { scale: [1, 1.1, 1] } : {}}
      transition={isPlaying ? { duration: 0.5, repeat: Infinity } : {}}
    >
      {isLoading ? (
        <Loader2 size={iconSizes[size]} className="animate-spin" />
      ) : isPlaying ? (
        <VolumeX size={iconSizes[size]} />
      ) : (
        <Volume2 size={iconSizes[size]} />
      )}
    </motion.button>
  );
}

export default AudioButton;
