'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Loader2, Play } from 'lucide-react';
import { cn } from '@/lib/utils';
import { soundService } from '@/lib/soundService';
import { RecordingState, RecordingResult } from '@/types';

interface RecordingInterfaceProps {
  maxDuration?: number; // Maximum recording duration in ms (default: 5000)
  countdownDuration?: number; // Countdown before recording starts (default: 3)
  onRecordingStart?: () => void;
  onRecordingComplete: (result: RecordingResult) => void;
  onError?: (error: string) => void;
  disabled?: boolean;
  className?: string;
}

export function RecordingInterface({
  maxDuration = 5000,
  countdownDuration = 3,
  onRecordingStart,
  onRecordingComplete,
  onError,
  disabled = false,
  className,
}: RecordingInterfaceProps) {
  const [state, setState] = useState<RecordingState>('idle');
  const [countdown, setCountdown] = useState(countdownDuration);
  const [recordingProgress, setRecordingProgress] = useState(0);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const startTimeRef = useRef<number>(0);
  const progressIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const blobUrlRef = useRef<string | null>(null);

  // Check microphone permission on mount
  useEffect(() => {
    let permissionCleanup: (() => void) | undefined;

    const initPermission = async () => {
      permissionCleanup = await checkPermission();
    };

    initPermission();

    return () => {
      cleanup();
      if (permissionCleanup) {
        permissionCleanup();
      }
    };
  }, []);

  const checkPermission = async () => {
    try {
      const result = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      setHasPermission(result.state === 'granted');

      // Store the handler to remove it on cleanup
      const handleChange = () => {
        setHasPermission(result.state === 'granted');
      };
      result.addEventListener('change', handleChange);

      // Return cleanup function for useEffect
      return () => {
        result.removeEventListener('change', handleChange);
      };
    } catch {
      // permissions API not supported, will check when recording
      setHasPermission(null);
      return undefined;
    }
  };

  const cleanup = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    // Revoke blob URL on unmount to prevent memory leaks
    if (blobUrlRef.current) {
      URL.revokeObjectURL(blobUrlRef.current);
      blobUrlRef.current = null;
    }
  };

  const startCountdown = useCallback(() => {
    if (disabled) return;

    setState('countdown');
    setCountdown(countdownDuration);

    // Play initial beep for the first countdown number
    soundService.playCountdownBeep(countdownDuration);

    const countdownInterval = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(countdownInterval);
          startRecording();
          return 0;
        }
        // Play beep for each countdown number
        soundService.playCountdownBeep(prev - 1);
        return prev - 1;
      });
    }, 1000);
  }, [countdownDuration, disabled]);

  const startRecording = async () => {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      });

      streamRef.current = stream;
      setHasPermission(true);

      // Create MediaRecorder
      const options = { mimeType: 'audio/webm;codecs=opus' };
      let mediaRecorder: MediaRecorder;

      try {
        mediaRecorder = new MediaRecorder(stream, options);
      } catch {
        // Fallback to default mime type
        mediaRecorder = new MediaRecorder(stream);
      }

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const duration_ms = Date.now() - startTimeRef.current;

        // Revoke previous blob URL to prevent memory leaks
        if (blobUrlRef.current) {
          URL.revokeObjectURL(blobUrlRef.current);
        }

        const url = URL.createObjectURL(blob);
        blobUrlRef.current = url;

        setState('complete');
        onRecordingComplete({ blob, duration_ms, url });

        // Cleanup stream
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.onerror = () => {
        setState('idle');
        onError?.('Recording failed');
        stream.getTracks().forEach(track => track.stop());
      };

      // Start recording
      mediaRecorder.start(100); // Collect data every 100ms
      startTimeRef.current = Date.now();
      setState('recording');
      onRecordingStart?.();
      setRecordingProgress(0);

      // Play recording start sound
      soundService.onRecordingStart();

      // Progress tracking
      progressIntervalRef.current = setInterval(() => {
        const elapsed = Date.now() - startTimeRef.current;
        const progress = Math.min((elapsed / maxDuration) * 100, 100);
        setRecordingProgress(progress);

        // Auto-stop at max duration
        if (elapsed >= maxDuration) {
          stopRecording();
        }
      }, 50);

    } catch (error) {
      setState('idle');
      setHasPermission(false);

      if (error instanceof DOMException && error.name === 'NotAllowedError') {
        onError?.('Microphone access denied. Please allow microphone access to record.');
      } else {
        onError?.('Could not access microphone. Please check your device settings.');
      }
    }
  };

  const stopRecording = useCallback(() => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
      progressIntervalRef.current = null;
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      setState('processing');
      mediaRecorderRef.current.stop();
      // Play recording stop sound
      soundService.onRecordingStop();
    }
  }, []);

  const resetRecording = useCallback(() => {
    // Revoke blob URL to prevent memory leaks
    if (blobUrlRef.current) {
      URL.revokeObjectURL(blobUrlRef.current);
      blobUrlRef.current = null;
    }
    setState('idle');
    setCountdown(countdownDuration);
    setRecordingProgress(0);
    chunksRef.current = [];
  }, [countdownDuration]);

  const handleClick = () => {
    if (state === 'idle') {
      startCountdown();
    } else if (state === 'recording') {
      stopRecording();
    } else if (state === 'complete') {
      resetRecording();
    }
  };

  // Render different states
  const renderContent = () => {
    switch (state) {
      case 'countdown':
        return (
          <motion.div
            key="countdown"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 1.5, opacity: 0 }}
            className="text-center"
          >
            <motion.div
              key={countdown}
              initial={{ scale: 1.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-6xl font-bold text-primary-500"
            >
              {countdown}
            </motion.div>
            <p className="text-sm text-gray-600 mt-2">Get ready!</p>
          </motion.div>
        );

      case 'recording':
        return (
          <motion.div
            key="recording"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center"
          >
            {/* Pulsing mic icon */}
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
              className="relative"
            >
              <div className="w-24 h-24 mx-auto bg-red-500 rounded-full flex items-center justify-center shadow-lg">
                <Mic size={48} className="text-white" />
              </div>

              {/* Progress ring */}
              <svg className="absolute inset-0 w-24 h-24 mx-auto -rotate-90">
                <circle
                  cx="48"
                  cy="48"
                  r="44"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="4"
                />
                <circle
                  cx="48"
                  cy="48"
                  r="44"
                  fill="none"
                  stroke="#ef4444"
                  strokeWidth="4"
                  strokeDasharray={`${2 * Math.PI * 44}`}
                  strokeDashoffset={`${2 * Math.PI * 44 * (1 - recordingProgress / 100)}`}
                  className="transition-all duration-100"
                />
              </svg>
            </motion.div>

            <p className="text-lg font-semibold text-red-600 mt-4">
              Recording...
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Tap to stop
            </p>
          </motion.div>
        );

      case 'processing':
        return (
          <motion.div
            key="processing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center"
          >
            <div className="w-24 h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
              <Loader2 size={48} className="text-primary-500 animate-spin" />
            </div>
            <p className="text-lg font-semibold text-gray-700 mt-4">
              Processing...
            </p>
          </motion.div>
        );

      case 'complete':
        return (
          <motion.div
            key="complete"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-center"
          >
            <div className="w-24 h-24 mx-auto bg-green-100 rounded-full flex items-center justify-center">
              <Play size={48} className="text-green-600 ml-1" />
            </div>
            <p className="text-lg font-semibold text-green-700 mt-4">
              Recording complete!
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Tap to record again
            </p>
          </motion.div>
        );

      default:
        return (
          <motion.div
            key="idle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center"
          >
            <motion.button
              onClick={handleClick}
              disabled={disabled}
              whileHover={{ scale: disabled ? 1 : 1.05 }}
              whileTap={{ scale: disabled ? 1 : 0.95 }}
              className={cn(
                "w-24 h-24 mx-auto rounded-full flex items-center justify-center transition-all",
                "shadow-lg",
                disabled
                  ? "bg-gray-300 cursor-not-allowed"
                  : hasPermission === false
                    ? "bg-orange-500 hover:bg-orange-600"
                    : "bg-primary-500 hover:bg-primary-600"
              )}
            >
              {hasPermission === false ? (
                <MicOff size={48} className="text-white" />
              ) : (
                <Mic size={48} className="text-white" />
              )}
            </motion.button>

            <p className="text-lg font-semibold text-gray-700 mt-4">
              {hasPermission === false
                ? "Microphone blocked"
                : "Tap to record"
              }
            </p>
            {hasPermission === false && (
              <p className="text-sm text-orange-600 mt-1">
                Please enable microphone access
              </p>
            )}
          </motion.div>
        );
    }
  };

  return (
    <div
      className={cn(
        "relative p-8 flex flex-col items-center justify-center",
        className
      )}
      onClick={state === 'idle' || state === 'recording' || state === 'complete' ? handleClick : undefined}
    >
      <AnimatePresence mode="wait">
        {renderContent()}
      </AnimatePresence>
    </div>
  );
}

export default RecordingInterface;
