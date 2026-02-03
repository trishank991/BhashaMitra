'use client';

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import api, {
  SubscriptionFeatures,
  SubscriptionLimits,
  UpgradeCTA,
} from '@/lib/api';

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
  lastFetched: number | null;
  _hasHydrated: boolean;

  // Actions
  fetchSubscription: () => Promise<void>;
  clearSubscription: () => void;
  setLoading: (loading: boolean) => void;
  setHasHydrated: (state: boolean) => void;
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

const initialState = {
  tier: 'FREE' as const,
  isPaidTier: false,
  isActive: false,
  homepageMode: 'playground' as const,
  homepageTitle: "Peppi's Playground",
  features: defaultFeatures,
  limits: defaultLimits,
  upgradeCta: null,
  loading: true, // Start with loading true until hydration completes
  error: null,
  lastFetched: null,
  _hasHydrated: false,
};

export const useSubscriptionStore = create<SubscriptionState>()(
  persist(
    (set, get) => ({
      ...initialState,

      fetchSubscription: async () => {
        // If we fetched recently (within 5 minutes), don't refetch
        const lastFetched = get().lastFetched;
        const now = Date.now();
        if (lastFetched && now - lastFetched < 5 * 60 * 1000 && !get().loading) {
          return;
        }

        set({ loading: true, error: null });

        try {
          const response = await api.getCurrentSubscription();

          if (response.success && response.data) {
            const data = response.data.data;
            set({
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
              lastFetched: Date.now(),
            });
          } else {
            set({
              loading: false,
              error: response.error || 'Failed to load subscription',
            });
          }
        } catch (err) {
          set({
            loading: false,
            error: err instanceof Error ? err.message : 'Unknown error',
          });
        }
      },

      clearSubscription: () => {
        set({ ...initialState, _hasHydrated: true, loading: false });
      },

      setLoading: (loading: boolean) => {
        set({ loading });
      },

      setHasHydrated: (state: boolean) => {
        set({ _hasHydrated: state });
      },
    }),
    {
      name: 'subscription-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        tier: state.tier,
        isPaidTier: state.isPaidTier,
        isActive: state.isActive,
        homepageMode: state.homepageMode,
        homepageTitle: state.homepageTitle,
        features: state.features,
        limits: state.limits,
        upgradeCta: state.upgradeCta,
        lastFetched: state.lastFetched,
      }),
      onRehydrateStorage: () => (state) => {
        // Called when state is rehydrated from localStorage
        if (state) {
          state.setHasHydrated(true);
          // If we have cached data and it's recent, set loading to false
          if (state.lastFetched && Date.now() - state.lastFetched < 5 * 60 * 1000) {
            state.setLoading(false);
          }
        }
      },
    }
  )
);
