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
  register: (email: string, password: string, name: string) => Promise<boolean>;
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

      register: async (email: string, password: string, name: string) => {
        set({ isLoading: true });

        const response = await api.register({ email, password, name, role: 'parent' });

        if (response.success && response.data) {
          // Extract tokens from the nested response structure (same as login)
          const { user, session } = response.data.data;
          const tokens: AuthTokens = {
            access: session.access_token,
            refresh: session.refresh_token,
          };

          api.setAccessToken(tokens.access);

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
            },
            tokens,
            isAuthenticated: true,
            isLoading: false,
          });

          return true;
        }

        set({ isLoading: false });
        return false;
      },

      logout: () => {
        api.setAccessToken(null);
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
        console.log('[fetchChildren] Starting fetch...');
        console.log('[fetchChildren] Current API token:', api.getAccessToken() ? 'SET' : 'NOT SET');

        const response = await api.getChildren();

        console.log('[fetchChildren] API response:', JSON.stringify(response, null, 2));

        if (response.success && response.data) {
          console.log('[fetchChildren] Success! Children count:', response.data.length);
          if (response.data.length > 0) {
            console.log('[fetchChildren] First child:', response.data[0].name, response.data[0].id);
          }
          set({ children: response.data });

          // Update active child with fresh data from server
          const { activeChild } = get();
          if (activeChild && response.data.length > 0) {
            // Find the matching child and update with server data
            const freshChild = response.data.find(c => c.id === activeChild.id);
            if (freshChild) {
              console.log('[fetchChildren] Updating active child with fresh data:', freshChild.name);
              set({ activeChild: freshChild });
            } else {
              // If previous active child no longer exists, use first child
              console.log('[fetchChildren] Previous active child not found, using first child');
              set({ activeChild: response.data[0] });
            }
          } else if (!activeChild && response.data.length > 0) {
            // No active child, set the first one
            console.log('[fetchChildren] No active child, setting first child:', response.data[0].name);
            set({ activeChild: response.data[0] });
          }
        } else {
          console.error('[fetchChildren] API call failed or returned no data:', response.error);
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
          console.log('[updateActiveChildLanguage] No active child, fetching children first...');

          if (!tokens?.access) {
            console.error('[updateActiveChildLanguage] No access token available');
            return false;
          }

          await get().fetchChildren();
          // Re-get state after fetch
          const updatedState = get();
          activeChild = updatedState.activeChild;

          console.log('[updateActiveChildLanguage] After fetch - activeChild:', activeChild?.name, 'children count:', updatedState.children.length);
        }

        if (!activeChild?.id) {
          console.error('[updateActiveChildLanguage] No active child after fetch');
          return false;
        }

        console.log('[updateActiveChildLanguage] Updating language to:', language, 'for child:', activeChild.id);

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const response = await api.updateChild(activeChild.id, { language } as any);

        console.log('[updateActiveChildLanguage] API response:', response);

        if (response.success && response.data) {
          // Create an updated child object with the new language
          // Force language to be the new value (API returns string)
          const updatedChild: ChildProfile = {
            ...activeChild,
            ...response.data,
            language: language, // Explicitly set the language to ensure it's updated
          };

          console.log('[updateActiveChildLanguage] Updated child with language:', updatedChild.language);

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

          // Verify state was updated
          const newState = get();
          console.log('[updateActiveChildLanguage] State after update - activeChild.language:', newState.activeChild?.language);

          return true;
        }

        console.error('[updateActiveChildLanguage] API call failed:', response.error);
        return false;
      },
    }),
    {
      name: 'bhashamitra-auth',
      // SECURITY FIX: Don't persist tokens to localStorage - only keep in memory
      // This prevents XSS attacks from stealing JWT tokens
      // Users will need to log in again after closing browser (security best practice)
      partialize: (state) => ({
        // Only persist child preference, NOT tokens or auth status
        activeChild: state.activeChild,
      }),
      onRehydrateStorage: () => (_state, error) => {
        if (error) {
          console.error('[authStore] Rehydration error:', error);
          return;
        }
        // On rehydration, tokens are gone (memory-only for security)
        // Clear isAuthenticated since we have no valid tokens
        console.log('[authStore] Session expired, tokens cleared for security');
        useAuthStore.setState({
          isAuthenticated: false,
          tokens: null,
          user: null,
        });
      },
    }
  )
);
