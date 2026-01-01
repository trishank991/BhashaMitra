import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, ChildProfile, AuthTokens, SubscriptionTier, SubscriptionInfo } from '@/types';
import api from '@/lib/api';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  activeChild: ChildProfile | null;
  children: ChildProfile[];
  isLoading: boolean;
  isAuthenticated: boolean;

  // Actions
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, passwordConfirm: string, name: string) => Promise<{ success: boolean; needsOnboarding: boolean; error?: string }>;
  googleLogin: (googleToken: string) => Promise<{ success: boolean; needsOnboarding: boolean; error?: string }>;
  logout: () => void;
  setActiveChild: (child: ChildProfile | null) => void;
  fetchChildren: () => Promise<void>;
  refreshAccessToken: () => Promise<boolean>;
  loadUserProfile: () => Promise<void>;
  updateActiveChildLanguage: (language: string) => Promise<boolean>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      activeChild: null,
      children: [],
      isLoading: false,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true });

        const response = await api.login({ email, password });

        if (response.success && response.data) {
          // Extract tokens from the nested response structure
          const { user, session } = response.data.data;
          const tokens: AuthTokens = {
            access: session.access_token,
            refresh: session.refresh_token,
          };

          api.setAccessToken(tokens.access);
          api.setRefreshToken(tokens.refresh);

          set({
            user: {
              id: user.id,
              email: user.email,
              name: user.name,
              role: user.role as 'parent' | 'child',
              created_at: user.created_at,
              subscription_tier: user.subscription_tier as SubscriptionTier | undefined,
              subscription_expires_at: user.subscription_expires_at,
              subscription_info: user.subscription_info as SubscriptionInfo | undefined,
              tts_provider: user.tts_provider as 'cache_only' | 'svara' | 'sarvam' | 'google_wavenet' | undefined,
              email_verified: user.email_verified || false,
              is_onboarded: user.is_onboarded || false,
              onboarding_completed_at: user.onboarding_completed_at,
            },
            tokens,
            isAuthenticated: true,
            isLoading: false,
          });

          // Fetch children profiles
          await get().fetchChildren();

          return true;
        }

        set({ isLoading: false });
        return false;
      },

      register: async (email: string, password: string, passwordConfirm: string, name: string) => {
        set({ isLoading: true });

        const response = await api.register({ email, password, password_confirm: passwordConfirm, name, role: 'parent' });

        if (response.success && response.data) {
          // Extract tokens - register returns { data: user, session: tokens }
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const responseData = response.data as any;
          const user = responseData.data || responseData.user;
          const session = responseData.session;

          const tokens: AuthTokens = {
            access: session.access_token,
            refresh: session.refresh_token,
          };

          api.setAccessToken(tokens.access);
          api.setRefreshToken(tokens.refresh);

          const needsOnboarding = !user.is_onboarded;

          set({
            user: {
              id: user.id,
              email: user.email,
              name: user.name,
              role: user.role as 'parent' | 'child',
              created_at: new Date().toISOString(),
              subscription_tier: user.subscription_tier as SubscriptionTier | undefined || 'FREE',
              subscription_expires_at: user.subscription_expires_at,
              subscription_info: user.subscription_info as SubscriptionInfo | undefined,
              tts_provider: user.tts_provider as 'cache_only' | 'svara' | 'sarvam' | 'google_wavenet' | undefined || 'cache_only',
              email_verified: user.email_verified || false,
              is_onboarded: user.is_onboarded || false,
              onboarding_completed_at: user.onboarding_completed_at,
            },
            tokens,
            isAuthenticated: true,
            isLoading: false,
          });

          // Return object with success and needsOnboarding for redirect logic
          return { success: true, needsOnboarding };
        }

        set({ isLoading: false });
        // Parse and return specific error message
        const errorMessage = response.error || 'Registration failed. Please try again.';
        return { success: false, needsOnboarding: false, error: errorMessage };
      },

      googleLogin: async (googleToken: string) => {
        set({ isLoading: true });

        const response = await api.googleAuth(googleToken);

        if (response.success && response.data) {
          // Extract tokens from the nested response structure
          const { user, session } = response.data.data;
          const tokens: AuthTokens = {
            access: session.access_token,
            refresh: session.refresh_token,
          };

          api.setAccessToken(tokens.access);
          api.setRefreshToken(tokens.refresh);

          const needsOnboarding = !user.is_onboarded;

          set({
            user: {
              id: user.id,
              email: user.email,
              name: user.name,
              role: user.role as 'parent' | 'child',
              created_at: (user as { created_at?: string }).created_at || new Date().toISOString(),
              subscription_tier: user.subscription_tier as SubscriptionTier | undefined || 'FREE',
              subscription_expires_at: user.subscription_expires_at,
              subscription_info: user.subscription_info as SubscriptionInfo | undefined,
              tts_provider: user.tts_provider as 'cache_only' | 'svara' | 'sarvam' | 'google_wavenet' | undefined || 'cache_only',
              email_verified: user.email_verified || true, // Google users are auto-verified
              is_onboarded: user.is_onboarded || false,
              onboarding_completed_at: user.onboarding_completed_at,
            },
            tokens,
            isAuthenticated: true,
            isLoading: false,
          });

          // Fetch children profiles for returning users
          if (!response.data.meta?.is_new_user) {
            await get().fetchChildren();
          }

          return { success: true, needsOnboarding };
        }

        set({ isLoading: false });
        const errorMessage = response.error || 'Google authentication failed. Please try again.';
        return { success: false, needsOnboarding: false, error: errorMessage };
      },

      logout: () => {
        api.setAccessToken(null);
        api.setRefreshToken(null);
        set({
          user: null,
          tokens: null,
          activeChild: null,
          children: [],
          isAuthenticated: false,
        });
      },

      setActiveChild: (child: ChildProfile | null) => {
        set({ activeChild: child });
      },

      fetchChildren: async () => {
        const response = await api.getChildren();

        if (response.success && response.data) {
          set({ children: response.data });

          // Update active child with fresh data from server
          const { activeChild } = get();
          if (activeChild && response.data.length > 0) {
            // Find the matching child and update with server data
            const freshChild = response.data.find(c => c.id === activeChild.id);
            if (freshChild) {
              set({ activeChild: freshChild });
            } else {
              // If previous active child no longer exists, use first child
              set({ activeChild: response.data[0] });
            }
          } else if (!activeChild && response.data.length > 0) {
            // No active child, set the first one
            set({ activeChild: response.data[0] });
          }
        }
      },

      refreshAccessToken: async () => {
        const { tokens } = get();

        if (!tokens?.refresh) {
          get().logout();
          return false;
        }

        const response = await api.refreshToken(tokens.refresh);

        if (response.success && response.data) {
          const newTokens = {
            ...tokens,
            access: response.data.access,
          };

          api.setAccessToken(newTokens.access);
          set({ tokens: newTokens });
          return true;
        }

        get().logout();
        return false;
      },

      loadUserProfile: async () => {
        const response = await api.getProfile();

        if (response.success && response.data) {
          set({ user: response.data });
        }
      },

      updateActiveChildLanguage: async (language: string) => {
        let { activeChild } = get();
        const { tokens } = get();

        // Ensure API token is set
        if (tokens?.access) {
          api.setAccessToken(tokens.access);
        }

        // If no active child, try fetching children first (handles race condition on page load)
        if (!activeChild?.id) {
          if (!tokens?.access) {
            return false;
          }

          await get().fetchChildren();
          // Re-get state after fetch
          const updatedState = get();
          activeChild = updatedState.activeChild;
        }

        if (!activeChild?.id) {
          return false;
        }

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const response = await api.updateChild(activeChild.id, { language } as any);

        if (response.success && response.data) {
          // Create an updated child object with the new language
          // Force language to be the new value (API returns string)
          const updatedChild: ChildProfile = {
            ...activeChild,
            ...response.data,
            language: language, // Explicitly set the language to ensure it's updated
          };

          // Update both activeChild and children array in a SINGLE set call
          // This ensures atomic state update and proper re-render triggering
          const currentChildren = get().children;
          const updatedChildren = currentChildren.map((child) =>
            child.id === activeChild!.id ? updatedChild : child
          );

          set({
            activeChild: updatedChild,
            children: updatedChildren,
          });

          return true;
        }

        return false;
      },
    }),
    {
      name: 'bhashamitra-auth',
      // Persist essential auth state for session continuity
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        activeChild: state.activeChild,
        children: state.children,
        isAuthenticated: state.isAuthenticated,
      }),
      // Rehydrate API tokens and configure callbacks on store load
      onRehydrateStorage: () => (state) => {
        if (state?.tokens?.access) {
          api.setAccessToken(state.tokens.access);
        }
        if (state?.tokens?.refresh) {
          api.setRefreshToken(state.tokens.refresh);
        }
        // Set up auth callbacks for automatic token refresh
        api.setAuthCallbacks(
          // On token refreshed - update store with new access token
          (newAccessToken: string) => {
            const currentTokens = useAuthStore.getState().tokens;
            if (currentTokens) {
              useAuthStore.setState({
                tokens: { ...currentTokens, access: newAccessToken },
              });
            }
          },
          // On logout - clear auth state
          () => {
            useAuthStore.getState().logout();
          }
        );
      },
    }
  )
);
