'use client';

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { PeppiAvatar } from './PeppiAvatar';
import { usePeppiStore } from '@/stores';
import api from '@/lib/api';
import type { LanguageCode, PeppiGender, SubscriptionTier } from '@/types';
import { cn } from '@/lib/utils';

interface PeppiSongNarratorProps {
  songId: string | number;
  songTitle?: string;
  language?: LanguageCode;
  defaultGender?: PeppiGender;
  subscriptionTier: SubscriptionTier;
  onComplete?: () => void;
}

// Language-specific gender labels
const GENDER_LABELS: Record<LanguageCode, { male: string; female: string }> = {
  HINDI: { male: 'पेप्पी भैया', female: 'पेप्पी दीदी' },
  FIJI_HINDI: { male: 'पेप्पी भैया', female: 'पेप्पी दीदी' },
  TAMIL: { male: 'பெப்பி அண்ணா', female: 'பெப்பி அக்கா' },
  TELUGU: { male: 'పెప్పి అన్న', female: 'పెప్పి అక్క' },
  GUJARATI: { male: 'પેપ્પી ભાઈ', female: 'પેપ્પી બેન' },
  PUNJABI: { male: 'ਪੈਪੀ ਵੀਰਜੀ', female: 'ਪੈਪੀ ਭੈਣਜੀ' },
  MALAYALAM: { male: 'Peppi Chettan', female: 'Peppi Chechi' },
  BENGALI: { male: 'Peppi Dada', female: 'Peppi Didi' },
  MARATHI: { male: 'पेप्पी भाऊ', female: 'पेप्पी ताई' },
  KANNADA: { male: 'Peppi Anna', female: 'Peppi Akka' },
  ODIA: { male: 'Peppi Bhai', female: 'Peppi Bhauni' },
  ASSAMESE: { male: 'Peppi Bhaiti', female: 'Peppi Bahini' },
  URDU: { male: 'پیپی بھائی', female: 'پیپی آپا' },
};

export function PeppiSongNarrator({
  songId,
  language = 'HINDI',
  defaultGender = 'female',
  subscriptionTier,
  onComplete,
}: PeppiSongNarratorProps) {
  const [gender, setGender] = useState<PeppiGender>(defaultGender);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [audioProgress, setAudioProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [showUpgrade, setShowUpgrade] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const { setMood } = usePeppiStore();

  // Check if Peppi narration is available (Standard and Premium tiers)
  const isPeppiAvailable = subscriptionTier === 'STANDARD' || subscriptionTier === 'PREMIUM';

  // Fetch song narration when component mounts or gender changes
  useEffect(() => {
    if (!isPeppiAvailable) {
      setShowUpgrade(true);
      return;
    }

    const fetchNarration = async () => {
      setIsLoading(true);
      setError(null);
      setMood('thinking');

      try {
        const response = await api.getPeppiSongNarration(songId, language, gender);

        if (response.success && response.data) {
          // Handle both audio_url (legacy) and audio_data (base64)
          if (response.data.audio_url) {
            setAudioUrl(response.data.audio_url);
          } else if (response.data.audio_data) {
            // Convert base64 to blob URL
            const binaryString = atob(response.data.audio_data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            const blob = new Blob([bytes], { type: 'audio/mp3' });
            const blobUrl = URL.createObjectURL(blob);
            setAudioUrl(blobUrl);
          }
          setMood('happy');
        } else {
          setError(response.error || 'Failed to load narration');
          setMood('sleepy');
        }
      } catch (err) {
        console.error('[PeppiSongNarrator] Error fetching song narration:', err);
        setError('Unable to load narration');
        setMood('sleepy');
      } finally {
        setIsLoading(false);
      }
    };

    fetchNarration();
  }, [songId, gender, language, isPeppiAvailable, setMood]);

  // Handle audio playback
  const handlePlayPause = () => {
    if (!audioRef.current || !audioUrl) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
      setMood('happy');
    } else {
      audioRef.current.play();
      setIsPlaying(true);
      setMood('excited');
    }
  };

  // Audio event handlers
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => {
      const progress = (audio.currentTime / audio.duration) * 100;
      setAudioProgress(progress);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setAudioProgress(0);
      setMood('celebrating');

      setTimeout(() => {
        setMood('happy');
      }, 2000);

      if (onComplete) {
        onComplete();
      }
    };

    const handleError = () => {
      setIsPlaying(false);
      setError('Audio playback failed');
      setMood('sleepy');
    };

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleError);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleError);
    };
  }, [onComplete, setMood]);

  // Stop audio and cleanup blob URLs when component unmounts
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      // Cleanup blob URL if it exists
      if (audioUrl && audioUrl.startsWith('blob:')) {
        URL.revokeObjectURL(audioUrl);
      }
      setIsPlaying(false);
      setMood('happy');
    };
  }, [setMood, audioUrl]);

  // Upgrade prompt for FREE tier
  if (showUpgrade && !isPeppiAvailable) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl p-6 border-2 border-pink-200"
      >
        <div className="flex items-center gap-4">
          <PeppiAvatar size="md" showBubble={false} />
          <div className="flex-1">
            <h3 className="font-bold text-gray-900 mb-1">Listen with Peppi</h3>
            <p className="text-sm text-gray-600 mb-3">
              Unlock song narration by Peppi to learn songs more easily!
            </p>
            <button
              onClick={() => window.location.href = '/profile'}
              className="px-4 py-2 bg-gradient-to-r from-pink-500 to-rose-500 text-white rounded-full font-medium hover:from-pink-600 hover:to-rose-600 transition-all shadow-md text-sm"
            >
              Upgrade to Standard
            </button>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Audio element */}
      {audioUrl && (
        <audio ref={audioRef} src={audioUrl} preload="auto" />
      )}

      {/* Narrator UI */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl p-6 border-2 border-pink-200"
      >
        <div className="flex items-center gap-4 mb-4">
          {/* Peppi Avatar */}
          <div className="flex-shrink-0">
            <PeppiAvatar size="md" showBubble={false} />
          </div>

          {/* Controls */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-bold text-gray-900">Listen with Peppi</h3>

              {/* Gender Selector */}
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value as PeppiGender)}
                disabled={isPlaying || isLoading}
                className="px-3 py-1 bg-white border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-pink-400 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50"
              >
                <option value="male">{GENDER_LABELS[language]?.male || 'Peppi Bhaiya'}</option>
                <option value="female">{GENDER_LABELS[language]?.female || 'Peppi Didi'}</option>
              </select>
            </div>

            {/* Peppi Voice Badge */}
            {isPeppiAvailable && (
              <div className="mb-2">
                <span className="inline-flex items-center gap-1 px-2 py-1 bg-gradient-to-r from-pink-400 to-rose-400 text-white rounded-full text-xs font-bold">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  {gender === 'female' ? (GENDER_LABELS[language]?.female || 'Peppi Didi') : (GENDER_LABELS[language]?.male || 'Peppi Bhaiya')} Voice
                </span>
              </div>
            )}

            {/* Play/Pause Button */}
            {!error && audioUrl && (
              <div className="flex items-center gap-3">
                <button
                  onClick={handlePlayPause}
                  disabled={isLoading}
                  className={cn(
                    "flex items-center justify-center w-12 h-12 rounded-full transition-all shadow-lg",
                    isPlaying
                      ? "bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600"
                      : "bg-gradient-to-r from-pink-400 to-rose-400 hover:from-pink-500 hover:to-rose-500",
                    isLoading && "opacity-50 cursor-not-allowed"
                  )}
                >
                  {isLoading ? (
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : isPlaying ? (
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>

                {/* Progress Bar */}
                <div className="flex-1">
                  <div className="h-2 bg-pink-200 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-pink-500 to-rose-500"
                      initial={{ width: 0 }}
                      animate={{ width: `${audioProgress}%` }}
                      transition={{ duration: 0.1 }}
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {isPlaying ? 'Playing...' : isLoading ? 'Loading...' : 'Ready to play'}
                  </p>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="flex items-center gap-2 text-red-600 text-sm">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default PeppiSongNarrator;
