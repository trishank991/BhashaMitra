'use client';

/**
 * Hook for triggering Peppi feedback responses
 * Use this to make Peppi react to user actions
 */
import { useCallback, useState } from 'react';
import { useSounds } from './useSounds';
import { useAgeConfig } from './useAgeConfig';
import { getPeppiScripts, getRandomScript, PeppiScript } from '@/data/peppi-scripts';

type FeedbackType = 'correct' | 'incorrect' | 'encouragement' | 'celebration' | 'streak' | 'hint';

interface PeppiFeedback {
  message: string;
  audioText: string;
  type: FeedbackType;
  mood: PeppiScript['mood'];
}

export function usePeppiFeedback() {
  const [currentFeedback, setCurrentFeedback] = useState<PeppiFeedback | null>(null);
  const [isShowing, setIsShowing] = useState(false);
  const { onCorrect, onWrong, onCelebration, onStreak } = useSounds();
  const { variant } = useAgeConfig();

  // Get age-appropriate scripts
  const scripts = getPeppiScripts(variant);

  const getScriptForType = (type: FeedbackType): PeppiScript => {
    switch (type) {
      case 'correct':
        return getRandomScript(scripts.correct);
      case 'incorrect':
        return getRandomScript(scripts.incorrect);
      case 'encouragement':
        return getRandomScript(scripts.encouragement);
      case 'celebration':
        return getRandomScript(scripts.lessonComplete);
      case 'streak':
        return getRandomScript(scripts.streak);
      case 'hint':
        return getRandomScript(scripts.hint);
      default:
        return getRandomScript(scripts.encouragement);
    }
  };

  const showFeedback = useCallback(
    (type: FeedbackType, duration = 2000) => {
      const script = getScriptForType(type);

      // Play appropriate sound
      if (type === 'correct') onCorrect();
      if (type === 'incorrect') onWrong();
      if (type === 'celebration') onCelebration();
      if (type === 'streak') onStreak();

      setCurrentFeedback({
        message: script.message,
        audioText: script.audioText || script.message,
        type,
        mood: script.mood,
      });
      setIsShowing(true);

      // Auto-hide after duration
      setTimeout(() => {
        setIsShowing(false);
        setTimeout(() => setCurrentFeedback(null), 300); // Wait for exit animation
      }, duration);
    },
    [onCorrect, onWrong, onCelebration, onStreak, variant, scripts]
  );

  const onPeppiCorrect = useCallback(() => showFeedback('correct'), [showFeedback]);
  const onPeppiWrong = useCallback(() => showFeedback('incorrect'), [showFeedback]);
  const onPeppiEncourage = useCallback(() => showFeedback('encouragement'), [showFeedback]);
  const onPeppiCelebrate = useCallback(() => showFeedback('celebration', 3000), [showFeedback]);
  const onPeppiStreak = useCallback(() => showFeedback('streak', 2500), [showFeedback]);
  const onPeppiHint = useCallback(() => showFeedback('hint', 2500), [showFeedback]);

  return {
    currentFeedback,
    isShowing,
    onPeppiCorrect,
    onPeppiWrong,
    onPeppiEncourage,
    onPeppiCelebrate,
    onPeppiStreak,
    onPeppiHint,
    showFeedback,
  };
}

export default usePeppiFeedback;
