'use client';

import { useState, useEffect, useCallback } from 'react';
import { useAuthStore } from '@/stores';
import api from '@/lib/api';

interface OnboardingProgress {
  hasSeenWelcome: boolean;
  hasAddedChild: boolean;
  hasSelectedLanguage: boolean;
  hasCompletedTour: boolean;
}

interface UseOnboardingReturn {
  needsOnboarding: boolean;
  progress: OnboardingProgress;
  isLoading: boolean;
  saveProgress: (step: keyof OnboardingProgress) => void;
  completeOnboarding: () => Promise<boolean>;
  skipOnboarding: () => void;
}

const ONBOARDING_STORAGE_KEY = 'bhashamitra-onboarding';

const defaultProgress: OnboardingProgress = {
  hasSeenWelcome: false,
  hasAddedChild: false,
  hasSelectedLanguage: false,
  hasCompletedTour: false,
};

export function useOnboarding(): UseOnboardingReturn {
  const { user, isAuthenticated } = useAuthStore();
  const [progress, setProgress] = useState<OnboardingProgress>(defaultProgress);
  const [isLoading, setIsLoading] = useState(true);

  // Load progress from localStorage on mount
  useEffect(() => {
    const loadProgress = () => {
      try {
        const stored = localStorage.getItem(ONBOARDING_STORAGE_KEY);
        if (stored) {
          const parsedProgress = JSON.parse(stored) as OnboardingProgress;
          setProgress(parsedProgress);
        }
      } catch (error) {
        console.error('[useOnboarding] Error loading progress:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadProgress();
  }, []);

  // Check if user needs onboarding
  const needsOnboarding = useCallback((): boolean => {
    if (!isAuthenticated || !user) {
      return false;
    }

    // If user is already marked as onboarded in backend, no need
    if (user.is_onboarded) {
      return false;
    }

    // Check if all steps are complete
    const allStepsComplete =
      progress.hasSeenWelcome &&
      progress.hasAddedChild &&
      progress.hasSelectedLanguage &&
      progress.hasCompletedTour;

    return !allStepsComplete;
  }, [isAuthenticated, user, progress]);

  // Save progress for a specific step
  const saveProgress = useCallback((step: keyof OnboardingProgress) => {
    const updatedProgress = {
      ...progress,
      [step]: true,
    };

    setProgress(updatedProgress);

    try {
      localStorage.setItem(ONBOARDING_STORAGE_KEY, JSON.stringify(updatedProgress));
    } catch (error) {
      console.error('[useOnboarding] Error saving progress:', error);
    }
  }, [progress]);

  // Complete onboarding (call API and mark complete)
  const completeOnboarding = useCallback(async (): Promise<boolean> => {
    try {
      // Call API to mark user as onboarded
      const response = await api.completeOnboarding();

      if (response.success) {
        // Mark all steps as complete locally
        const completedProgress: OnboardingProgress = {
          hasSeenWelcome: true,
          hasAddedChild: true,
          hasSelectedLanguage: true,
          hasCompletedTour: true,
        };

        setProgress(completedProgress);
        localStorage.setItem(ONBOARDING_STORAGE_KEY, JSON.stringify(completedProgress));
        return true;
      }

      return false;
    } catch (error) {
      console.error('[useOnboarding] Error completing onboarding:', error);
      // Still save locally even if API fails
      const completedProgress: OnboardingProgress = {
        hasSeenWelcome: true,
        hasAddedChild: true,
        hasSelectedLanguage: true,
        hasCompletedTour: true,
      };
      setProgress(completedProgress);
      localStorage.setItem(ONBOARDING_STORAGE_KEY, JSON.stringify(completedProgress));
      return true;
    }
  }, []);

  // Skip onboarding
  const skipOnboarding = useCallback(() => {
    const skippedProgress: OnboardingProgress = {
      hasSeenWelcome: true,
      hasAddedChild: true,
      hasSelectedLanguage: true,
      hasCompletedTour: true,
    };

    setProgress(skippedProgress);
    localStorage.setItem(ONBOARDING_STORAGE_KEY, JSON.stringify(skippedProgress));
  }, []);

  return {
    needsOnboarding: needsOnboarding(),
    progress,
    isLoading,
    saveProgress,
    completeOnboarding,
    skipOnboarding,
  };
}
