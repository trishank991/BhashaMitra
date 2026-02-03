/**
 * Parent Dashboard API Client
 *
 * Provides typed API calls for parent dashboard functionality.
 */

import { apiClient } from './api';

// Types
export interface ChildBasic {
  id: string;
  name: string;
  date_of_birth: string;
  age: number | null;
  language: string;
  avatar_url: string | null;
  total_points: number;
  level: number;
  created_at: string;
}

export interface ActivityLogEntry {
  id: string;
  activity_type: string;
  description: string;
  points_earned: number;
  created_at: string;
  time_ago: string;
  icon: string;
}

export interface DailyProgressEntry {
  date: string;
  day_name: string;
  time_spent_minutes: number;
  lessons_completed: number;
  exercises_completed: number;
  games_played: number;
  points_earned: number;
}

export interface LearningGoal {
  id: string;
  type: string;
  title: string;
  target_value: number;
  current_value: number;
  percentage: number;
  deadline: string | null;
  is_completed: boolean;
  reward_points: number;
}

export interface WeeklySummary {
  time_spent_minutes: number;
  lessons_completed: number;
  exercises_completed: number;
  games_played: number;
  points_earned: number;
}

export interface ChildSummary {
  child: ChildBasic;
  weekly_summary: WeeklySummary;
  current_streak: number;
  recent_achievements: number;
  active_goals: LearningGoal[];
}

export interface WeeklyComparison {
  time_change_percent: number;
  points_change_percent: number;
  trend: 'up' | 'down' | 'stable';
}

export interface Highlight {
  type: string;
  message: string;
  icon: string;
}

export interface Suggestion {
  type: string;
  message: string;
  action: string;
}

export interface WeeklyReport {
  daily_data: DailyProgressEntry[];
  summary: {
    total_time_minutes: number;
    total_lessons: number;
    total_exercises: number;
    total_games: number;
    total_points: number;
    days_active: number;
  };
  comparison: WeeklyComparison;
  highlights: Highlight[];
  suggestions: Suggestion[];
}

export interface ProgressUpdateRequest {
  type: 'lesson' | 'exercise' | 'game';
  duration_minutes?: number;
  points_earned?: number;
  details?: Record<string, unknown>;
}

export interface GoalCreateRequest {
  type: 'daily_time' | 'weekly_lessons' | 'weekly_words' | 'streak';
  target: number;
  deadline?: string;
}

// ========================================
// REPORT CARD TYPES
// ========================================

export interface ReportCardOverallStats {
  total_time_minutes: number;
  days_active: number;
  total_points: number;
  lessons_completed: number;
  stories_read: number;
  games_played: number;
  exercises_completed: number;
  current_level: number;
  words_learned: number;
}

export interface SkillMasteryItem {
  skill: string;
  display_name: string;
  mastery_level: 'novice' | 'beginner' | 'intermediate' | 'advanced' | 'expert';
  percentage: number;
  icon: string;
}

export interface ContentCompletionItem {
  content_type: string;
  total: number;
  completed: number;
  percentage: number;
}

export interface AchievementItem {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  earned_at: string;
  xp_reward: number;
}

export interface PronunciationStats {
  total_challenges: number;
  challenges_attempted: number;
  challenges_mastered: number;
  average_score: number;
  best_category: string;
  total_stars: number;
}

export interface StreakInfo {
  current_streak: number;
  longest_streak: number;
  streak_status: 'active' | 'broken' | 'new';
  streak_message: string;
}

export interface InsightItem {
  type: 'strength' | 'improvement' | 'milestone' | 'suggestion';
  title: string;
  message: string;
  icon: string;
}

export interface ReportCard {
  child_id: string;
  child_name: string;
  report_period: {
    start_date: string;
    end_date: string;
    period_type: 'weekly' | 'monthly' | 'all_time';
  };
  overall_stats: ReportCardOverallStats;
  skill_mastery: SkillMasteryItem[];
  content_completion: ContentCompletionItem[];
  achievements: AchievementItem[];
  pronunciation: PronunciationStats;
  streak: StreakInfo;
  insights: InsightItem[];
  generated_at: string;
}

export interface SkillsBreakdown {
  child_id: string;
  skills: SkillMasteryItem[];
  vocabulary: {
    total_words: number;
    words_mastered: number;
    words_learning: number;
    accuracy_rate: number;
  };
  grammar: {
    topics_completed: number;
    total_topics: number;
    accuracy_rate: number;
  };
  reading: {
    stories_read: number;
    average_comprehension: number;
    favorite_categories: string[];
  };
}

export interface MonthlyStatsItem {
  month: string;
  year: number;
  time_spent_minutes: number;
  points_earned: number;
  lessons_completed: number;
  days_active: number;
}

export interface MonthlyStats {
  child_id: string;
  current_month: MonthlyStatsItem;
  previous_month: MonthlyStatsItem;
  comparison: {
    time_change: number;
    points_change: number;
    lessons_change: number;
    trend: 'improving' | 'steady' | 'declining';
  };
  monthly_history: MonthlyStatsItem[];
}

export interface ParentPreferences {
  notification_frequency: 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'NONE';
  email_reports: boolean;
  push_notifications: boolean;
  sms_alerts: boolean;
  preferred_report_day: number;
  timezone: string;
}

// API Functions
export const parentApi = {
  /**
   * Get all children for the authenticated parent
   */
  async getChildren(): Promise<ChildBasic[]> {
    const response = await apiClient.get<ChildBasic[]>('/parent/children/');
    return response.data;
  },

  /**
   * Get detailed summary for a specific child
   */
  async getChildSummary(childId: string): Promise<ChildSummary> {
    const response = await apiClient.get<ChildSummary>(
      `/parent/children/${childId}/summary/`
    );
    return response.data;
  },

  /**
   * Get activity log for a child
   */
  async getChildActivity(
    childId: string,
    options?: { type?: string; days?: number }
  ): Promise<ActivityLogEntry[]> {
    const params = new URLSearchParams();
    if (options?.type) params.set('type', options.type);
    if (options?.days) params.set('days', options.days.toString());

    const queryString = params.toString();
    const url = `/parent/children/${childId}/activity/${queryString ? `?${queryString}` : ''}`;

    const response = await apiClient.get<ActivityLogEntry[]>(url);
    return response.data;
  },

  /**
   * Get weekly progress report for a child
   */
  async getWeeklyReport(childId: string): Promise<WeeklyReport> {
    const response = await apiClient.get<WeeklyReport>(
      `/parent/children/${childId}/weekly-report/`
    );
    return response.data;
  },

  /**
   * Get learning goals for a child
   */
  async getChildGoals(childId: string): Promise<{ goals: LearningGoal[]; count: number }> {
    const response = await apiClient.get<{ goals: LearningGoal[]; count: number }>(
      `/parent/children/${childId}/goals/`
    );
    return response.data;
  },

  /**
   * Create a new learning goal for a child
   */
  async createGoal(childId: string, goal: GoalCreateRequest): Promise<LearningGoal> {
    const response = await apiClient.post<LearningGoal>(
      `/parent/children/${childId}/goals/`,
      goal
    );
    return response.data;
  },

  /**
   * Record progress update for a learning activity
   */
  async updateProgress(
    childId: string,
    progress: ProgressUpdateRequest
  ): Promise<{ success: boolean; daily_progress: DailyProgressEntry; total_points: number }> {
    const response = await apiClient.post<{
      success: boolean;
      daily_progress: DailyProgressEntry;
      total_points: number;
    }>(`/parent/children/${childId}/progress/`, progress);
    return response.data;
  },

  // ========================================
  // REPORT CARD ENDPOINTS
  // ========================================

  /**
   * Get comprehensive report card for a child
   */
  async getReportCard(
    childId: string,
    period?: 'weekly' | 'monthly' | 'all_time'
  ): Promise<ReportCard> {
    const params = period ? `?period=${period}` : '';
    const response = await apiClient.get<ReportCard>(
      `/parent/children/${childId}/report-card/${params}`
    );
    return response.data;
  },

  /**
   * Get detailed skills breakdown for a child
   */
  async getSkillsBreakdown(childId: string): Promise<SkillsBreakdown> {
    const response = await apiClient.get<SkillsBreakdown>(
      `/parent/children/${childId}/skills/`
    );
    return response.data;
  },

  /**
   * Get monthly stats comparison for a child
   */
  async getMonthlyStats(childId: string): Promise<MonthlyStats> {
    const response = await apiClient.get<MonthlyStats>(
      `/parent/children/${childId}/monthly-stats/`
    );
    return response.data;
  },

  /**
   * Get parent preferences
   */
  async getPreferences(): Promise<ParentPreferences> {
    const response = await apiClient.get<ParentPreferences>(
      '/parent/preferences/'
    );
    return response.data;
  },

  /**
   * Update parent preferences
   */
  async updatePreferences(
    preferences: Partial<ParentPreferences>
  ): Promise<ParentPreferences> {
    const response = await apiClient.put<ParentPreferences>(
      '/parent/preferences/',
      preferences
    );
    return response.data;
  },

  /**
   * Update a learning goal
   */
  async updateGoal(
    childId: string,
    goalId: string,
    updates: Partial<GoalCreateRequest>
  ): Promise<LearningGoal> {
    const response = await apiClient.put<LearningGoal>(
      `/parent/children/${childId}/goals/${goalId}/`,
      updates
    );
    return response.data;
  },

  /**
   * Delete a learning goal
   */
  async deleteGoal(childId: string, goalId: string): Promise<void> {
    await apiClient.delete(`/parent/children/${childId}/goals/${goalId}/`);
  },
};

export default parentApi;
