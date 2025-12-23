/**
 * Parent engagement store
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  ParentPreferences,
  LearningGoal,
  WeeklyReport,
  ParentChildActivity,
  ParentDashboardData,
  GoalType,
  NotificationFrequency,
} from '@/types/parent';

interface ParentEngagementState {
  // State
  preferences: ParentPreferences | null;
  goals: LearningGoal[];
  weeklyReports: WeeklyReport[];
  suggestedActivities: ParentChildActivity[];
  dashboardData: ParentDashboardData | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchDashboard: () => Promise<void>;
  fetchPreferences: () => Promise<void>;
  updatePreferences: (updates: Partial<ParentPreferences>) => Promise<boolean>;
  fetchGoals: (childId: string) => Promise<void>;
  createGoal: (
    childId: string,
    goalType: GoalType,
    targetValue: number,
    endDate?: string
  ) => Promise<boolean>;
  updateGoalProgress: (goalId: string, value: number) => void;
  deleteGoal: (goalId: string) => Promise<boolean>;
  fetchWeeklyReports: (childId: string) => Promise<void>;
  fetchSuggestedActivities: (language: string, age: number) => Promise<void>;
}

export const useParentStore = create<ParentEngagementState>()(
  persist(
    (set, get) => ({
      // Initial state
      preferences: null,
      goals: [],
      weeklyReports: [],
      suggestedActivities: [],
      dashboardData: null,
      isLoading: false,
      error: null,

      fetchDashboard: async () => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call when backend endpoint is ready
          // const response = await api.getParentDashboard();

          set({ isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch dashboard',
          });
        }
      },

      fetchPreferences: async () => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          // For now, return default preferences if none exist
          if (!get().preferences) {
            const defaultPreferences: ParentPreferences = {
              id: crypto.randomUUID(),
              userId: '',
              notificationFrequency: 'WEEKLY',
              emailReports: true,
              pushNotifications: true,
              smsAlerts: false,
              preferredReportDay: 0, // Monday
              timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            };

            set({ preferences: defaultPreferences, isLoading: false });
          } else {
            set({ isLoading: false });
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch preferences',
          });
        }
      },

      updatePreferences: async (updates: Partial<ParentPreferences>) => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          set(state => ({
            preferences: state.preferences
              ? { ...state.preferences, ...updates }
              : null,
            isLoading: false,
          }));

          return true;
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to update preferences',
          });
          return false;
        }
      },

      fetchGoals: async (childId: string) => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          // Filter goals for specific child
          const childGoals = get().goals.filter(g => g.childId === childId);
          set({ goals: childGoals, isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch goals',
          });
        }
      },

      createGoal: async (
        childId: string,
        goalType: GoalType,
        targetValue: number,
        endDate?: string
      ) => {
        set({ isLoading: true, error: null });

        try {
          const goal: LearningGoal = {
            id: crypto.randomUUID(),
            childId,
            goalType,
            targetValue,
            currentValue: 0,
            startDate: new Date().toISOString(),
            endDate: endDate || null,
            isActive: true,
            progressPercentage: 0,
          };

          set(state => ({
            goals: [...state.goals, goal],
            isLoading: false,
          }));

          return true;
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to create goal',
          });
          return false;
        }
      },

      updateGoalProgress: (goalId: string, value: number) => {
        set(state => ({
          goals: state.goals.map(goal => {
            if (goal.id !== goalId) return goal;

            const progressPercentage = Math.min(100, (value / goal.targetValue) * 100);

            return {
              ...goal,
              currentValue: value,
              progressPercentage,
              isActive: progressPercentage < 100,
            };
          }),
        }));
      },

      deleteGoal: async (goalId: string) => {
        try {
          set(state => ({
            goals: state.goals.filter(g => g.id !== goalId),
          }));
          return true;
        } catch {
          return false;
        }
      },

      fetchWeeklyReports: async (childId: string) => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          // For now, return empty array or mock data
          set({ weeklyReports: [], isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch reports',
          });
        }
      },

      fetchSuggestedActivities: async (language: string, age: number) => {
        set({ isLoading: true, error: null });

        try {
          // TODO: Implement API call
          // For now, return mock activities
          const mockActivities: ParentChildActivity[] = [
            {
              id: '1',
              title: 'Read a Story Together',
              activityType: 'READ_TOGETHER',
              description: 'Pick a story from your child\'s current level and read it together, discussing the pictures and characters.',
              language,
              minAge: 2,
              maxAge: 8,
              durationMinutes: 15,
              materialsNeeded: ['A quiet space', 'The BhashaMitra app'],
              learningOutcomes: ['Vocabulary building', 'Bonding time', 'Reading comprehension'],
              isFeatured: true,
            },
            {
              id: '2',
              title: 'Letter Tracing Practice',
              activityType: 'PRACTICE_LETTERS',
              description: 'Practice writing letters together using the tracing guides in the app.',
              language,
              minAge: 3,
              maxAge: 7,
              durationMinutes: 10,
              materialsNeeded: ['Paper', 'Pencil', 'Tablet/phone'],
              learningOutcomes: ['Fine motor skills', 'Letter recognition', 'Writing practice'],
              isFeatured: false,
            },
          ];

          const filteredActivities = mockActivities.filter(
            a => age >= a.minAge && age <= a.maxAge
          );

          set({ suggestedActivities: filteredActivities, isLoading: false });
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to fetch activities',
          });
        }
      },
    }),
    {
      name: 'bhashamitra-parent',
      partialize: (state) => ({
        preferences: state.preferences,
        goals: state.goals,
      }),
    }
  )
);
