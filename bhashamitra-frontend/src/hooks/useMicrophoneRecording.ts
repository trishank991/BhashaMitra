'use client';

import { useState, useRef, useCallback, useEffect } from 'react';

export interface RecordingState {
  isRecording: boolean;
  duration: number;
  audioBlob: Blob | null;
  audioUrl: string | null;
  error: string | null;
  permissionStatus: 'prompt' | 'granted' | 'denied' | 'checking';
}

export interface UseMicrophoneRecordingOptions {
  maxDuration?: number; // in seconds
  onRecordingComplete?: (blob: Blob, url: string) => void;
  onError?: (error: string) => void;
}

export function useMicrophoneRecording(options: UseMicrophoneRecordingOptions = {}) {
  const { maxDuration = 10, onRecordingComplete, onError } = options;

  const [state, setState] = useState<RecordingState>({
    isRecording: false,
    duration: 0,
    audioBlob: null,
    audioUrl: null,
    error: null,
    permissionStatus: 'checking',
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const blobUrlRef = useRef<string | null>(null);

  // Check permission on mount
  useEffect(() => {
    checkPermission();
    return () => cleanup();
  }, []);

  const checkPermission = async () => {
    if (typeof window === 'undefined') {
      setState(prev => ({ ...prev, permissionStatus: 'denied' }));
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      setState(prev => ({
        ...prev,
        permissionStatus: 'denied',
        error: 'Microphone not supported in this browser',
      }));
      return;
    }

    try {
      if (navigator.permissions?.query) {
        const result = await navigator.permissions.query({ name: 'microphone' as PermissionName });
        setState(prev => ({ ...prev, permissionStatus: result.state as RecordingState['permissionStatus'] }));

        // Listen for permission changes
        result.addEventListener('change', () => {
          setState(prev => ({ ...prev, permissionStatus: result.state as RecordingState['permissionStatus'] }));
        });
      } else {
        setState(prev => ({ ...prev, permissionStatus: 'prompt' }));
      }
    } catch {
      setState(prev => ({ ...prev, permissionStatus: 'prompt' }));
    }
  };

  const cleanup = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (blobUrlRef.current) {
      URL.revokeObjectURL(blobUrlRef.current);
      blobUrlRef.current = null;
    }
    mediaRecorderRef.current = null;
    chunksRef.current = [];
  }, []);

  const startRecording = useCallback(async () => {
    cleanup();
    chunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 48000,
        },
      });

      streamRef.current = stream;
      setState(prev => ({ ...prev, permissionStatus: 'granted', error: null }));

      // Use WebM format (supported by Google STT)
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mimeType });

        // Revoke previous blob URL
        if (blobUrlRef.current) {
          URL.revokeObjectURL(blobUrlRef.current);
        }

        const url = URL.createObjectURL(blob);
        blobUrlRef.current = url;

        setState(prev => ({
          ...prev,
          audioBlob: blob,
          audioUrl: url,
          isRecording: false,
        }));

        onRecordingComplete?.(blob, url);

        // Stop stream tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.onerror = () => {
        const errorMsg = 'Recording failed';
        setState(prev => ({
          ...prev,
          error: errorMsg,
          isRecording: false,
        }));
        onError?.(errorMsg);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start(100); // Collect data every 100ms

      // Start duration timer
      const startTime = Date.now();
      timerRef.current = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        setState(prev => ({ ...prev, duration: elapsed }));

        if (elapsed >= maxDuration) {
          stopRecording();
        }
      }, 100);

      setState(prev => ({
        ...prev,
        isRecording: true,
        duration: 0,
        audioBlob: null,
        audioUrl: null,
        error: null,
      }));

    } catch (err: unknown) {
      const error = err as { name?: string; message?: string };
      const errorMsg = error.name === 'NotAllowedError'
        ? 'Microphone permission denied. Please allow microphone access.'
        : `Microphone error: ${error.message || 'Unknown error'}`;

      setState(prev => ({
        ...prev,
        error: errorMsg,
        permissionStatus: error.name === 'NotAllowedError' ? 'denied' : prev.permissionStatus,
        isRecording: false,
      }));
      onError?.(errorMsg);
    }
  }, [maxDuration, onRecordingComplete, onError, cleanup]);

  const stopRecording = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  }, []);

  const resetRecording = useCallback(() => {
    cleanup();
    setState(prev => ({
      ...prev,
      isRecording: false,
      duration: 0,
      audioBlob: null,
      audioUrl: null,
      error: null,
    }));
  }, [cleanup]);

  return {
    ...state,
    startRecording,
    stopRecording,
    resetRecording,
    isSupported: typeof window !== 'undefined' && !!navigator.mediaDevices?.getUserMedia,
  };
}

export default useMicrophoneRecording;
