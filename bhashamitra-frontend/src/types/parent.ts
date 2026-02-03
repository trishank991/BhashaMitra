/**
 * Parent engagement types
 */

export type NotificationFrequency = 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'NONE';

export type GoalType = 'DAILY_MINUTES' | 'WEEKLY_STORIES' | 'MONTHLY_POINTS' | 'LEVEL_TARGET';

export type ActivityType = 'READ_TOGETHER' | 'PRACTICE_LETTERS' | 'CULTURAL_CRAFT' | 'COOKING_ACTIVITY' | 'FESTIVAL_ACTIVITY';

export interface ParentPreferences {
  id: string;
  userId: string;
  notificationFrequency: NotificationFrequency;
  emailReports: boolean;
  pushNotifications: boolean;
  smsAlerts: boolean;
  preferredReportDay: number;
  timezone: string;
}

export interface LearningGoal {
  id: string;
  childId: string;
  goalType: GoalType;
  targetValue: number;
  currentValue: number;
  startDate: string;
  endDate: string | null;
  isActive: boolean;
  progressPercentage: number;
}

export interface WeeklyReport {
  id: string;
  childId: string;
  weekStart: string;
  weekEnd: string;
  totalTimeMinutes: number;
  storiesCompleted: number;
  pointsEarned: number;
  newWordsLearned: number;
  achievementsUnlocked: Achievement[];
  areasOfStrength: string[];
  areasForImprovement: string[];
  peppiInteractions: number;
  sentAt: string | null;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  earnedAt: string;
}

export interface ParentChildActivity {
  id: string;
  title: string;
  activityType: ActivityType;
  description: string;
  language: string;
  minAge: number;
  maxAge: number;
  durationMinutes: number;
  materialsNeeded: string[];
  learningOutcomes: string[];
  isFeatured: boolean;
}

export interface ParentDashboardData {
  children: ChildSummary[];
  weeklyReports: WeeklyReport[];
  suggestedActivities: ParentChildActivity[];
  goals: LearningGoal[];
  familyStats: FamilyStats;
}

export interface ChildSummary {
  id: string;
  name: string;
  avatar: string;
  level: number;
  points: number;
  currentStreak: number;
  lastActiveAt: string;
  weeklyProgress: number;
}

export interface FamilyStats {
  totalTimeThisWeek: number;
  totalStoriesThisWeek: number;
  totalPointsThisWeek: number;
  mostActiveChild: string;
  improvementFromLastWeek: number;
}

export interface ParentEngagementState {
  preferences: ParentPreferences | null;
  goals: LearningGoal[];
  weeklyReports: WeeklyReport[];
  suggestedActivities: ParentChildActivity[];
  dashboardData: ParentDashboardData | null;
  isLoading: boolean;
  error: string | null;
}
