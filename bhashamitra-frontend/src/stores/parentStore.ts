/**
 * Parent engagement store
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '@/lib/api';
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
          const response = await api.getParentDashboard();
          if (response.success && response.data) {
            // Map API ChildSummary to parent.ts ChildSummary format
            const children = (response.data.children || []).map(child => ({
              id: child.id,
              name: child.name,
              avatar: child.avatar,
              level: child.level,
              points: child.total_xp || 0,
              currentStreak: child.streak_count || 0,
              lastActiveAt: new Date().toISOString(),
              weeklyProgress: child.xp_this_week || 0,
            }));

            set({
              dashboardData: {
                children,
                weeklyReports: [],
                suggestedActivities: [],
                goals: [],
                familyStats: {
                  totalTimeThisWeek: 0,
                  totalStoriesThisWeek: 0,
                  totalPointsThisWeek: children.reduce((sum, c) => sum + c.weeklyProgress, 0),
                  mostActiveChild: children[0]?.name || '',
                  improvementFromLastWeek: 0,
                },
              },
              isLoading: false,
            });
          } else {
            set({ isLoading: false, error: response.error || 'Failed to fetch dashboard' });
          }
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
          const response = await api.getParentPreferences();
          if (response.success && response.data) {
            const data = response.data;
            set({
              preferences: {
                id: data.id || crypto.randomUUID(),
                userId: '',
                notificationFrequency: (data.notification_frequency || 'WEEKLY') as NotificationFrequency,
                emailReports: data.email_reports ?? true,
                pushNotifications: data.push_notifications ?? true,
                smsAlerts: data.sms_alerts ?? false,
                preferredReportDay: data.preferred_report_day ?? 0,
                timezone: data.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
              },
              isLoading: false,
            });
          } else {
            // Use defaults on error
            set({
              preferences: {
                id: crypto.randomUUID(),
                userId: '',
                notificationFrequency: 'WEEKLY',
                emailReports: true,
                pushNotifications: true,
                smsAlerts: false,
                preferredReportDay: 0,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
              },
              isLoading: false,
            });
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
          const apiUpdates: Record<string, unknown> = {};
          if (updates.notificationFrequency !== undefined) apiUpdates.notification_frequency = updates.notificationFrequency;
          if (updates.emailReports !== undefined) apiUpdates.email_reports = updates.emailReports;
          if (updates.pushNotifications !== undefined) apiUpdates.push_notifications = updates.pushNotifications;
          if (updates.smsAlerts !== undefined) apiUpdates.sms_alerts = updates.smsAlerts;
          if (updates.preferredReportDay !== undefined) apiUpdates.preferred_report_day = updates.preferredReportDay;
          if (updates.timezone !== undefined) apiUpdates.timezone = updates.timezone;

          const response = await api.updateParentPreferences(apiUpdates);
          if (response.success) {
            set(state => ({
              preferences: state.preferences
                ? { ...state.preferences, ...updates }
                : null,
              isLoading: false,
            }));
            return true;
          } else {
            set({ isLoading: false, error: response.error || 'Failed to update preferences' });
            return false;
          }
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
          const response = await api.getChildGoals(childId);
          if (response.success && response.data) {
            const goalsData = response.data.goals || [];
            const goals: LearningGoal[] = goalsData.map((g) => ({
              id: String(g.id),
              childId,
              goalType: (g.goal_type || 'DAILY_MINUTES') as GoalType,
              targetValue: g.target_value || 0,
              currentValue: g.current_value || 0,
              startDate: g.start_date || new Date().toISOString(),
              endDate: g.end_date,
              isActive: g.is_active,
              progressPercentage: g.progress_percentage || 0,
            }));
            set({ goals, isLoading: false });
          } else {
            set({ goals: [], isLoading: false });
          }
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
          // Map frontend goal types to API types
          const typeMap: Record<GoalType, string> = {
            'DAILY_MINUTES': 'daily_time',
            'WEEKLY_STORIES': 'weekly_lessons',
            'MONTHLY_POINTS': 'weekly_words',
            'LEVEL_TARGET': 'streak',
          };

          const response = await api.createChildGoal(childId, {
            type: typeMap[goalType] || 'daily_time',
            target: targetValue,
            deadline: endDate,
          });

          if (response.success && response.data) {
            const goal: LearningGoal = {
              id: String(response.data.id),
              childId,
              goalType,
              targetValue: response.data.target_value,
              currentValue: response.data.current_value,
              startDate: response.data.start_date,
              endDate: response.data.end_date,
              isActive: response.data.is_active,
              progressPercentage: response.data.progress_percentage,
            };

            set(state => ({
              goals: [...state.goals, goal],
              isLoading: false,
            }));
            return true;
          } else {
            set({ isLoading: false, error: response.error || 'Failed to create goal' });
            return false;
          }
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
        const goals = get().goals;
        const goal = goals.find(g => g.id === goalId);
        if (!goal) return false;

        try {
          const response = await api.deleteChildGoal(goal.childId, goalId);
          if (response.success) {
            set(state => ({
              goals: state.goals.filter(g => g.id !== goalId),
            }));
            return true;
          }
          return false;
        } catch {
          return false;
        }
      },

      fetchWeeklyReports: async (childId: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await api.getChildWeeklyReport(childId);
          if (response.success && response.data) {
            const report: WeeklyReport = {
              id: crypto.randomUUID(),
              childId,
              weekStart: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
              weekEnd: new Date().toISOString(),
              totalTimeMinutes: response.data.summary.total_time_minutes,
              storiesCompleted: response.data.summary.total_lessons,
              pointsEarned: response.data.summary.total_points,
              newWordsLearned: 0,
              achievementsUnlocked: [],
              areasOfStrength: response.data.highlights.map(h => h.message),
              areasForImprovement: response.data.suggestions.map(s => s.message),
              peppiInteractions: 0,
              sentAt: null,
            };
            set({ weeklyReports: [report], isLoading: false });
          } else {
            set({ weeklyReports: [], isLoading: false });
          }
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
          const response = await api.getParentActivities(language, age);
          if (response.success && response.data) {
            const activities: ParentChildActivity[] = response.data.activities.map(a => ({
              id: a.id,
              title: a.title,
              activityType: a.activity_type as ParentChildActivity['activityType'],
              description: a.description,
              language,
              minAge: parseInt(a.age_range.split('-')[0]) || 2,
              maxAge: parseInt(a.age_range.split('-')[1]) || 10,
              durationMinutes: a.duration_minutes,
              materialsNeeded: a.materials_needed,
              learningOutcomes: a.learning_outcomes,
              isFeatured: a.is_featured,
            }));
            set({ suggestedActivities: activities, isLoading: false });
          } else {
            set({ suggestedActivities: [], isLoading: false });
          }
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
