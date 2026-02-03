/**
 * Family store for multi-child features
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '@/lib/api';
import type {
  Family,
  FamilyLeaderboard,
  SiblingChallenge,
  ChallengeType,
} from '@/types/family';

interface FamilyState {
  // State
  family: Family | null;
  leaderboard: FamilyLeaderboard | null;
  activeChallenges: SiblingChallenge[];
  completedChallenges: SiblingChallenge[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchFamily: () => Promise<void>;
  createFamily: (name: string) => Promise<boolean>;
  joinFamily: (familyCode: string) => Promise<boolean>;
  fetchLeaderboard: () => Promise<void>;
  fetchChallenges: () => Promise<void>;
  createChallenge: (
    title: string,
    type: ChallengeType,
    targetValue: number,
    participantIds: string[],
    endDate: string,
    prizeDescription?: string
  ) => Promise<boolean>;
  updateChallengeProgress: (challengeId: string, childId: string, value: number) => void;
  cancelChallenge: (challengeId: string) => Promise<boolean>;
  calculateDiscount: () => number;
}

export const useFamilyStore = create<FamilyState>()(
  persist(
    (set, get) => ({
      // Initial state
      family: null,
      leaderboard: null,
      activeChallenges: [],
      completedChallenges: [],
      isLoading: false,
      error: null,

      fetchFamily: async () => {
        set({ isLoading: true, error: null });

        try {
          const response = await api.getFamily();
          
          if (response.success && response.data) {
            set({ family: response.data, isLoading: false });
          } else {
            set({ family: null, isLoading: false });
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch family',
          });
        }
      },

      createFamily: async (name: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await api.createFamily(name);
          
          if (response.success && response.data) {
            set({ family: response.data, isLoading: false });
            return true;
          } else {
            set({
              isLoading: false,
              error: response.error || 'Failed to create family',
            });
            return false;
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to create family',
          });
          return false;
        }
      },

      joinFamily: async (familyCode: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await api.joinFamilyViaCode(familyCode);
          
          if (response.success && response.data) {
            set({ family: response.data, isLoading: false });
            return true;
          } else {
            set({
              isLoading: false,
              error: response.error || 'Failed to join family',
            });
            return false;
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to join family',
          });
          return false;
        }
      },

      fetchLeaderboard: async () => {
        const family = get().family;
        if (!family) return;

        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          // For now, create mock leaderboard
          const leaderboard: FamilyLeaderboard = {
            id: crypto.randomUUID(),
            familyId: family.id,
            weekStart: new Date().toISOString(),
            totalPoints: family.collectivePoints,
            totalTimeMinutes: 0,
            storiesCompleted: 0,
            childRankings: [],
            rank: 0,
          };

          set({ leaderboard, isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch leaderboard',
          });
        }
      },

      fetchChallenges: async () => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          set({ isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch challenges',
          });
        }
      },

      createChallenge: async (
        title: string,
        type: ChallengeType,
        targetValue: number,
        participantIds: string[],
        endDate: string,
        prizeDescription = ''
      ) => {
        const family = get().family;
        if (!family) return false;

        set({ isLoading: true, error: null });

        try {
          const challenge: SiblingChallenge = {
            id: crypto.randomUUID(),
            familyId: family.id,
            title,
            challengeType: type,
            status: 'ACTIVE',
            participantIds,
            startDate: new Date().toISOString(),
            endDate,
            targetValue,
            participantProgress: Object.fromEntries(participantIds.map(id => [id, 0])),
            winnerId: null,
            prizeDescription,
            createdAt: new Date().toISOString(),
          };

          set(state => ({
            activeChallenges: [...state.activeChallenges, challenge],
            isLoading: false,
          }));

          return true;
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to create challenge',
          });
          return false;
        }
      },

      updateChallengeProgress: (challengeId: string, childId: string, value: number) => {
        set(state => ({
          activeChallenges: state.activeChallenges.map(challenge => {
            if (challenge.id !== challengeId) return challenge;

            const updatedProgress = {
              ...challenge.participantProgress,
              [childId]: value,
            };

            // Check if challenge is completed
            const targetReached = Object.values(updatedProgress).some(
              v => v >= challenge.targetValue
            );

            if (targetReached && challenge.status === 'ACTIVE') {
              // Find winner (first to reach target)
              const winnerId = Object.entries(updatedProgress).find(
                ([, v]) => v >= challenge.targetValue
              )?.[0];

              return {
                ...challenge,
                participantProgress: updatedProgress,
                status: 'COMPLETED' as const,
                winnerId: winnerId || null,
              };
            }

            return {
              ...challenge,
              participantProgress: updatedProgress,
            };
          }),
        }));
      },

      cancelChallenge: async (challengeId: string) => {
        try {
          set(state => ({
            activeChallenges: state.activeChallenges.map(c =>
              c.id === challengeId ? { ...c, status: 'CANCELLED' as const } : c
            ),
          }));
          return true;
        } catch {
          return false;
        }
      },

      calculateDiscount: () => {
        const family = get().family;
        if (!family) return 0;

        const childCount = family.totalChildren;

        if (childCount >= 4) return 25;
        if (childCount >= 3) return 15;
        if (childCount >= 2) return 10;
        return 0;
      },
    }),
    {
      name: 'bhashamitra-family',
      partialize: (state) => ({
        family: state.family,
        activeChallenges: state.activeChallenges,
      }),
    }
  )
);
