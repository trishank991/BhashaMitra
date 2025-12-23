'use client';

import { useState, useEffect, useCallback } from 'react';
import api, {
  CurrentSubscriptionResponse,
  ChildHomepageProgressResponse,
  SubscriptionFeatures,
  SubscriptionLimits,
  UpgradeCTA,
} from '@/lib/api';
import { useAuthStore } from '@/stores';

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

const defaultFeatures: SubscriptionFeatures = {
  has_curriculum_progression: false,
  has_peppi_ai_chat: false,
  has_peppi_narration: false,
  has_live_classes: false,
  has_progress_reports: false,
  content_access_mode: 'browse',
  tts_provider: 'cache_only',
};

const defaultLimits: SubscriptionLimits = {
  story_limit: 5,
  games_per_day: 2,
  child_profiles: 1,
  free_live_classes: 0,
};

export function useSubscription() {
  const { isAuthenticated } = useAuthStore();
  const [subscription, setSubscription] = useState<SubscriptionState>({
    tier: 'FREE',
    isPaidTier: false,
    isActive: false,
    homepageMode: 'playground',
    homepageTitle: "Peppi's Playground",
    features: defaultFeatures,
    limits: defaultLimits,
    upgradeCta: null,
    loading: true,
    error: null,
  });

  const fetchSubscription = useCallback(async () => {
    if (!isAuthenticated) {
      setSubscription((prev) => ({
        ...prev,
        loading: false,
        tier: 'FREE',
        isPaidTier: false,
        isActive: false,
        homepageMode: 'playground',
        homepageTitle: "Peppi's Playground",
        features: defaultFeatures,
        limits: defaultLimits,
        upgradeCta: {
          message: 'Unlock the full learning journey!',
          button_text: 'Upgrade to Standard',
          price: 'NZD $20/month',
        },
      }));
      return;
    }

    setSubscription((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await api.getCurrentSubscription();

      if (response.success && response.data) {
        const data = response.data.data;
        setSubscription({
          tier: data.tier,
          isPaidTier: data.is_paid_tier,
          isActive: data.is_subscription_active,
          homepageMode: data.homepage_mode,
          homepageTitle: data.homepage_title,
          features: data.features,
          limits: data.limits,
          upgradeCta: data.upgrade_cta,
          loading: false,
          error: null,
        });
      } else {
        setSubscription((prev) => ({
          ...prev,
          loading: false,
          error: response.error || 'Failed to load subscription',
        }));
      }
    } catch (err) {
      setSubscription((prev) => ({
        ...prev,
        loading: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }));
    }
  }, [isAuthenticated]);

  useEffect(() => {
    fetchSubscription();
  }, [fetchSubscription]);

  return {
    ...subscription,
    refetch: fetchSubscription,
    isFree: subscription.tier === 'FREE',
    isStandard: subscription.tier === 'STANDARD',
    isPremium: subscription.tier === 'PREMIUM',
    canAccessCurriculum: subscription.features.has_curriculum_progression,
    canAccessPeppiChat: subscription.features.has_peppi_ai_chat,
    canAccessLiveClasses: subscription.features.has_live_classes,
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
