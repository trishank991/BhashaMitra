'use client';

import { useState, useEffect, useCallback } from 'react';
import api, {
  SubscriptionFeatures,
  SubscriptionLimits,
  UpgradeCTA,
} from '@/lib/api';
import { useAuthStore, useSubscriptionStore } from '@/stores';

export interface SubscriptionState {
  tier: 'FREE' | 'STANDARD' | 'PREMIUM';
  isPaidTier: boolean;
  isActive: boolean;
  homepageMode: 'playground' | 'classroom';
  homepageTitle: string;
  features: SubscriptionFeatures;
  limits: SubscriptionLimits;
  upgradeCta: UpgradeCTA | null;
  loading: boolean;
  error: string | null;
}

export interface ChildProgress {
  child: {
    id: string;
    name: string;
    avatar: string;
    level: number;
  };
  summary: {
    levels_completed: number;
    total_points: number;
    current_streak: number;
  };
  currentProgress: {
    level: { id: string; name: string; hindi_name: string; order: number };
    module: { id: string; name: string; hindi_name: string; order: number } | null;
    lesson: { id: string; title: string; hindi_title: string; order: number } | null;
    continue_url: string;
  } | null;
  upgradePrompt?: {
    message: string;
    cta: string;
    price: string;
  };
  loading: boolean;
  error: string | null;
}

export function useSubscription() {
  const { isAuthenticated } = useAuthStore();
  const store = useSubscriptionStore();

  // Fetch subscription on mount if authenticated and not recently fetched
  useEffect(() => {
    if (isAuthenticated && store._hasHydrated) {
      store.fetchSubscription();
    } else if (!isAuthenticated && store._hasHydrated) {
      store.clearSubscription();
    }
  }, [isAuthenticated, store._hasHydrated]);

  // Show loading while store is hydrating or data is loading
  const isLoading = !store._hasHydrated || store.loading;

  return {
    tier: store.tier,
    isPaidTier: store.isPaidTier,
    isActive: store.isActive,
    homepageMode: store.homepageMode,
    homepageTitle: store.homepageTitle,
    features: store.features,
    limits: store.limits,
    upgradeCta: store.upgradeCta,
    loading: isLoading,
    error: store.error,
    hasHydrated: store._hasHydrated,
    refetch: store.fetchSubscription,
    isFree: store.tier === 'FREE',
    isStandard: store.tier === 'STANDARD',
    isPremium: store.tier === 'PREMIUM',
    canAccessCurriculum: store.features.has_curriculum_progression,
    canAccessPeppiChat: store.features.has_peppi_ai_chat,
    canAccessLiveClasses: store.features.has_live_classes,
  };
}

export function useChildHomepageProgress(childId: string | null) {
  const [progress, setProgress] = useState<ChildProgress>({
    child: { id: '', name: '', avatar: '', level: 1 },
    summary: { levels_completed: 0, total_points: 0, current_streak: 0 },
    currentProgress: null,
    loading: true,
    error: null,
  });

  const fetchProgress = useCallback(async () => {
    if (!childId) {
      setProgress((prev) => ({ ...prev, loading: false }));
      return;
    }

    setProgress((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await api.getChildHomepageProgress(childId);

      if (response.success && response.data) {
        const data = response.data.data;
        setProgress({
          child: data.child,
          summary: data.summary,
          currentProgress: data.current_progress,
          upgradePrompt: data.upgrade_prompt,
          loading: false,
          error: null,
        });
      } else {
        setProgress((prev) => ({
          ...prev,
          loading: false,
          error: response.error || 'Failed to load progress',
        }));
      }
    } catch (err) {
      setProgress((prev) => ({
        ...prev,
        loading: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }));
    }
  }, [childId]);

  useEffect(() => {
    fetchProgress();
  }, [fetchProgress]);

  return {
    ...progress,
    refetch: fetchProgress,
  };
}
