'use client';

import { useCallback, useEffect, useState } from 'react';
import { soundService, SoundName } from '@/lib/soundService';

interface UseSoundsOptions {
  /** Preload sounds on mount */
  preload?: boolean;
}

interface UseSoundsReturn {
  /** Play a specific sound */
  play: (sound: SoundName, volume?: number) => void;
  /** Whether sounds are enabled */
  enabled: boolean;
  /** Toggle sounds on/off */
  toggle: () => void;
  /** Set enabled state */
  setEnabled: (enabled: boolean) => void;
  /** Current volume (0-1) */
  volume: number;
  /** Set volume (0-1) */
  setVolume: (volume: number) => void;
  // Convenience methods
  onCorrect: () => void;
  onWrong: () => void;
  onLevelUp: () => void;
  onBadge: () => void;
  onClick: () => void;
  onPageTurn: () => void;
  onCelebration: () => void;
  onPeppiMeow: () => void;
  onStreak: () => void;
  onStoryComplete: () => void;
  onPop: () => void;
  onWhoosh: () => void;
}

/**
 * React hook for playing UI sound effects.
 *
 * Provides easy access to sound playback with state management
 * for enabled/disabled status and volume control.
 *
 * @example
 * ```tsx
 * function QuizQuestion() {
 *   const { onCorrect, onWrong } = useSounds();
 *
 *   const handleAnswer = (isCorrect: boolean) => {
 *     if (isCorrect) {
 *       onCorrect();
 *     } else {
 *       onWrong();
 *     }
 *   };
 *
 *   return <Button onClick={() => handleAnswer(true)}>Submit</Button>;
 * }
 * ```
 */
export function useSounds(options: UseSoundsOptions = {}): UseSoundsReturn {
  const { preload = true } = options;

  const [enabled, setEnabledState] = useState(soundService.isEnabled());
  const [volume, setVolumeState] = useState(soundService.getVolume());

  // Preload sounds on mount
  useEffect(() => {
    if (preload) {
      soundService.preload();
    }
  }, [preload]);

  const play = useCallback((sound: SoundName, vol?: number) => {
    soundService.play(sound, vol);
  }, []);

  const toggle = useCallback(() => {
    const newState = soundService.toggle();
    setEnabledState(newState);
  }, []);

  const setEnabled = useCallback((value: boolean) => {
    soundService.setEnabled(value);
    setEnabledState(value);
  }, []);

  const setVolume = useCallback((value: number) => {
    soundService.setVolume(value);
    setVolumeState(value);
  }, []);

  // Convenience methods - memoized for stable references
  const onCorrect = useCallback(() => soundService.onCorrect(), []);
  const onWrong = useCallback(() => soundService.onWrong(), []);
  const onLevelUp = useCallback(() => soundService.onLevelUp(), []);
  const onBadge = useCallback(() => soundService.onBadge(), []);
  const onClick = useCallback(() => soundService.onClick(), []);
  const onPageTurn = useCallback(() => soundService.onPageTurn(), []);
  const onCelebration = useCallback(() => soundService.onCelebration(), []);
  const onPeppiMeow = useCallback(() => soundService.onPeppiMeow(), []);
  const onStreak = useCallback(() => soundService.onStreak(), []);
  const onStoryComplete = useCallback(() => soundService.onStoryComplete(), []);
  const onPop = useCallback(() => soundService.onPop(), []);
  const onWhoosh = useCallback(() => soundService.onWhoosh(), []);

  return {
    play,
    enabled,
    toggle,
    setEnabled,
    volume,
    setVolume,
    onCorrect,
    onWrong,
    onLevelUp,
    onBadge,
    onClick,
    onPageTurn,
    onCelebration,
    onPeppiMeow,
    onStreak,
    onStoryComplete,
    onPop,
    onWhoosh,
  };
}

export default useSounds;
