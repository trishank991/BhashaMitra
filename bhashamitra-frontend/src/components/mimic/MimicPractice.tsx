'use client';

import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Volume2, RotateCcw, Loader2, CheckCircle, XCircle, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useMicrophoneRecording } from '@/hooks/useMicrophoneRecording';
import { speechApi, PronunciationEvaluation, WordComparison } from '@/services/speechApi';
import { soundService } from '@/lib/soundService';

interface MimicPracticeProps {
  text: string;
  romanization?: string;
  meaning?: string;
  language: string;
  audioUrl?: string;
  childId: string;
  onComplete?: (result: PronunciationEvaluation) => void;
  onNextWord?: () => void;
  className?: string;
}

export function MimicPractice({
  text,
  romanization,
  meaning,
  language,
  audioUrl,
  childId,
  onComplete,
  onNextWord,
  className,
}: MimicPracticeProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<PronunciationEvaluation | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [attemptNumber, setAttemptNumber] = useState(1);

  const {
    isRecording,
    duration,
    permissionStatus,
    error: recordingError,
    startRecording,
    stopRecording,
    resetRecording,
    isSupported,
  } = useMicrophoneRecording({
    maxDuration: 10,
    onRecordingComplete: handleRecordingComplete,
  });

  // Play reference audio (TTS)
  const playAudio = useCallback(async () => {
    if (!audioUrl) return;

    setIsPlaying(true);
    soundService.onClick();

    try {
      const audio = new Audio(audioUrl);
      audio.onended = () => setIsPlaying(false);
      audio.onerror = () => setIsPlaying(false);
      await audio.play();
    } catch {
      setIsPlaying(false);
    }
  }, [audioUrl]);

  // Handle completed recording
  async function handleRecordingComplete(blob: Blob) {
    setIsProcessing(true);
    setError(null);
    soundService.onRecordingStop();

    try {
      const response = await speechApi.evaluatePronunciation(
        childId,
        blob,
        language,
        text,
        attemptNumber
      );

      if (!response.success) {
        setError(response.error || 'Failed to process audio');
        return;
      }

      if (response.evaluation) {
        setResult(response.evaluation);
        onComplete?.(response.evaluation);

        // Play result sound
        if (response.evaluation.stars >= 3) {
          soundService.playMimicResult(3);
        } else if (response.evaluation.stars >= 2) {
          soundService.playMimicResult(2);
        } else {
          soundService.playMimicResult(1);
        }
      }
    } catch (err: unknown) {
      const error = err as { message?: string };
      setError(error.message || 'Failed to process audio');
    } finally {
      setIsProcessing(false);
    }
  }

  // Start recording with sound effect
  const handleStartRecording = () => {
    soundService.onRecordingStart();
    startRecording();
  };

  // Reset for another attempt
  const handleTryAgain = () => {
    setResult(null);
    setError(null);
    setAttemptNumber(prev => prev + 1);
    resetRecording();
    soundService.onClick();
  };

  // Move to next word
  const handleNext = () => {
    setResult(null);
    setError(null);
    setAttemptNumber(1);
    resetRecording();
    soundService.onClick();
    onNextWord?.();
  };

  // Render word comparison
  const renderWordComparison = (comparisons: WordComparison[]) => {
    if (!comparisons || comparisons.length === 0) return null;

    return (
      <div className="bg-gray-50 rounded-2xl p-4 mt-4">
        <p className="text-sm text-gray-500 mb-3 text-center">Word by word:</p>
        <div className="flex flex-wrap justify-center gap-3">
          {comparisons.map((word, index) => (
            <motion.div
              key={index}
              className={cn(
                "px-4 py-3 rounded-xl text-center min-w-[80px]",
                word.is_correct
                  ? "bg-green-100 border-2 border-green-300"
                  : "bg-red-100 border-2 border-red-300"
              )}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center justify-center gap-1 mb-1">
                {word.is_correct ? (
                  <CheckCircle className="w-4 h-4 text-green-600" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-600" />
                )}
              </div>
              <p className="font-bold text-lg">{word.expected || word.heard}</p>
              <p className="text-sm text-gray-600">({word.expected_roman || word.heard_roman})</p>
              {!word.is_correct && word.hint && (
                <p className="text-xs text-red-600 mt-1">{word.hint}</p>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    );
  };

  // Permission denied state
  if (!isSupported || permissionStatus === 'denied') {
    return (
      <div className={cn("p-6 bg-red-50 rounded-2xl text-center", className)}>
        <MicOff className="w-16 h-16 mx-auto text-red-400 mb-4" />
        <p className="text-red-600 font-bold text-lg">Microphone Needed!</p>
        <p className="text-red-500 mt-2">
          Please allow microphone access to practice speaking.
        </p>
      </div>
    );
  }

  return (
    <div className={cn("space-y-6", className)}>
      {/* Word to practice */}
      <motion.div
        className="text-center p-8 bg-gradient-to-r from-purple-100 to-pink-100 rounded-3xl shadow-lg"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
      >
        {/* Native script - large */}
        <p className="text-5xl font-bold text-gray-800 mb-3">{text}</p>

        {/* Roman transliteration - smaller */}
        {(romanization || result?.expected?.roman) && (
          <p className="text-xl text-purple-600 font-medium">
            ({romanization || result?.expected?.roman})
          </p>
        )}

        {/* Meaning */}
        {meaning && (
          <p className="text-gray-500 mt-2 italic">&ldquo;{meaning}&rdquo;</p>
        )}

        {/* Listen button */}
        {audioUrl && (
          <button
            onClick={playAudio}
            disabled={isPlaying || isRecording}
            className={cn(
              "mt-4 px-6 py-3 rounded-full font-semibold transition-all inline-flex items-center gap-2",
              isPlaying
                ? "bg-green-100 text-green-700"
                : "bg-white border-2 border-purple-300 text-purple-600 hover:bg-purple-50"
            )}
          >
            <Volume2 className={cn("w-5 h-5", isPlaying && "animate-pulse")} />
            {isPlaying ? 'Playing...' : 'Listen First'}
          </button>
        )}
      </motion.div>

      {/* Recording controls - show when no result */}
      {!result && (
        <div className="flex flex-col items-center space-y-6">
          {/* Big microphone button */}
          <motion.button
            onClick={isRecording ? stopRecording : handleStartRecording}
            disabled={isProcessing}
            className={cn(
              "w-32 h-32 rounded-full flex items-center justify-center",
              "transition-all duration-300 shadow-xl",
              isRecording
                ? "bg-gradient-to-r from-red-500 to-red-600 scale-110"
                : "bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105",
              isProcessing && "opacity-50 cursor-not-allowed"
            )}
            whileTap={{ scale: 0.95 }}
            animate={isRecording ? { scale: [1.1, 1.15, 1.1] } : {}}
            transition={{ repeat: isRecording ? Infinity : 0, duration: 1 }}
          >
            {isProcessing ? (
              <Loader2 className="w-14 h-14 text-white animate-spin" />
            ) : isRecording ? (
              <MicOff className="w-14 h-14 text-white" />
            ) : (
              <Mic className="w-14 h-14 text-white" />
            )}
          </motion.button>

          {/* Instructions */}
          <div className="text-center">
            <p className="text-xl font-medium text-gray-700">
              {isProcessing
                ? 'Listening to you...'
                : isRecording
                  ? `Recording: ${duration}s`
                  : 'Tap and say the word!'
              }
            </p>
            {isRecording && (
              <p className="text-sm text-gray-500 mt-1">Tap again when done</p>
            )}
          </div>

          {/* Error message */}
          {(error || recordingError) && (
            <motion.p
              className="text-red-500 text-center bg-red-50 px-4 py-2 rounded-lg"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {error || recordingError}
            </motion.p>
          )}
        </div>
      )}

      {/* Results display */}
      <AnimatePresence>
        {result && (
          <motion.div
            className="space-y-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {/* Big emoji and stars */}
            <div className="text-center">
              <motion.div
                className="text-8xl mb-4"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', bounce: 0.5 }}
              >
                {result.feedback.emoji}
              </motion.div>

              {/* Stars */}
              <div className="flex justify-center gap-2 mb-4">
                {[1, 2, 3].map((star, index) => (
                  <motion.span
                    key={star}
                    className={cn(
                      "text-5xl",
                      star <= result.stars ? "" : "grayscale opacity-30"
                    )}
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ delay: index * 0.1 + 0.2 }}
                  >
                    *
                  </motion.span>
                ))}
              </div>

              {/* Score */}
              <motion.div
                className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent"
                initial={{ scale: 0.5 }}
                animate={{ scale: 1 }}
              >
                {result.score}%
              </motion.div>
            </div>

            {/* Feedback messages */}
            <div className="text-center space-y-2">
              <p className="text-2xl font-bold text-purple-700">
                {result.feedback.message_hindi}
              </p>
              <p className="text-lg text-gray-600">
                {result.feedback.message_english}
              </p>
              <p className="text-md text-pink-600 font-medium">
                {result.feedback.encouragement}
              </p>
            </div>

            {/* What you said (with Hinglish) */}
            <div className="bg-white rounded-2xl p-6 shadow-md">
              <p className="text-sm text-gray-500 mb-2 text-center">You said:</p>
              <p className="text-3xl font-bold text-center text-gray-800">
                {result.heard.native || '(no speech detected)'}
              </p>
              {result.heard.roman && (
                <p className="text-lg text-center text-purple-600 mt-1">
                  ({result.heard.roman})
                </p>
              )}
            </div>

            {/* Word-by-word comparison */}
            {result.word_comparison && result.word_comparison.length > 0 && (
              renderWordComparison(result.word_comparison)
            )}

            {/* Pronunciation hints */}
            {result.hints && result.hints.length > 0 && (
              <div className="bg-yellow-50 rounded-2xl p-4">
                <p className="text-sm font-medium text-yellow-800 mb-2">Tips:</p>
                <ul className="space-y-1">
                  {result.hints.map((hint, index) => (
                    <li key={index} className="text-yellow-700">{hint}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action buttons */}
            <div className="flex gap-4 justify-center">
              <motion.button
                onClick={handleTryAgain}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full font-semibold transition-colors"
              >
                <RotateCcw className="w-5 h-5" />
                Try Again
              </motion.button>

              {result.is_correct && onNextWord && (
                <motion.button
                  onClick={handleNext}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-full font-semibold"
                >
                  Next Word
                  <ChevronRight className="w-5 h-5" />
                </motion.button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default MimicPractice;
