'use client';

import { useEffect, useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Users,
  Clock,
  BookOpen,
  Star,
  TrendingUp,
  TrendingDown,
  Target,
  Bell,
  Settings,
  ChevronRight,
  Loader2,
  AlertCircle,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useParentStore } from '@/stores';
import parentApi, {
  ChildBasic,
  ChildSummary as ApiChildSummary,
  WeeklyReport as ApiWeeklyReport,
  LearningGoal as ApiLearningGoal,
} from '@/services/parentApi';
import type {
  ChildSummary,
  WeeklyReport,
  LearningGoal,
  FamilyStats,
} from '@/types/parent';
import ChildProgressCard from './ChildProgressCard';
import GoalCard from './GoalCard';
import ActivitySuggestion from './ActivitySuggestion';
import WeeklyReportCard from './WeeklyReportCard';

interface ParentDashboardProps {
  className?: string;
}

// Transform API response to component format
function transformChildToSummary(child: ChildBasic, summary?: ApiChildSummary): ChildSummary {
  return {
    id: child.id,
    name: child.name,
    avatar: child.avatar_url || '/avatars/default.png',
    level: child.level,
    points: child.total_points,
    currentStreak: summary?.current_streak || 0,
    lastActiveAt: child.created_at,
    weeklyProgress: summary ? Math.min(100, Math.round((summary.weekly_summary.time_spent_minutes / 60) * 100 / 7)) : 0,
  };
}

function transformGoal(goal: ApiLearningGoal, childId: string): LearningGoal {
  return {
    id: goal.id,
    childId,
    goalType: goal.type.toUpperCase() as 'DAILY_MINUTES' | 'WEEKLY_STORIES' | 'MONTHLY_POINTS' | 'LEVEL_TARGET',
    targetValue: goal.target_value,
    currentValue: goal.current_value,
    startDate: new Date().toISOString(),
    endDate: goal.deadline,
    isActive: !goal.is_completed,
    progressPercentage: goal.percentage,
  };
}

function transformReport(report: ApiWeeklyReport, childId: string): WeeklyReport {
  return {
    id: `${childId}-weekly`,
    childId,
    weekStart: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
    weekEnd: new Date().toISOString(),
    totalTimeMinutes: report.summary.total_time_minutes,
    storiesCompleted: report.summary.total_lessons,
    pointsEarned: report.summary.total_points,
    newWordsLearned: report.summary.total_lessons * 3, // Estimate
    achievementsUnlocked: [],
    areasOfStrength: report.highlights.map(h => h.message),
    areasForImprovement: report.suggestions.map(s => s.message),
    peppiInteractions: 0,
    sentAt: null,
  };
}

export function ParentDashboard({ className }: ParentDashboardProps) {
  const {
    suggestedActivities,
    fetchSuggestedActivities,
  } = useParentStore();

  const [children, setChildren] = useState<ChildSummary[]>([]);
  const [goals, setGoals] = useState<LearningGoal[]>([]);
  const [weeklyReports, setWeeklyReports] = useState<WeeklyReport[]>([]);
  const [familyStats, setFamilyStats] = useState<FamilyStats>({
    totalTimeThisWeek: 0,
    totalStoriesThisWeek: 0,
    totalPointsThisWeek: 0,
    mostActiveChild: '',
    improvementFromLastWeek: 0,
  });
  const [selectedChild, setSelectedChild] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Fetch children
      const childrenData = await parentApi.getChildren();

      // Fetch detailed summaries for each child
      const summaries = await Promise.all(
        childrenData.map(child => parentApi.getChildSummary(child.id))
      );

      // Transform children data
      const transformedChildren = childrenData.map((child, idx) =>
        transformChildToSummary(child, summaries[idx])
      );
      setChildren(transformedChildren);

      // Calculate family stats
      let totalTime = 0;
      let totalLessons = 0;
      let totalPoints = 0;
      let mostActive = '';
      let maxTime = 0;
      let totalImprovement = 0;

      // Fetch goals and weekly reports for each child
      const allGoals: LearningGoal[] = [];
      const allReports: WeeklyReport[] = [];

      for (const summary of summaries) {
        // Null safety checks for summary data
        const weeklySummary = summary?.weekly_summary;
        const childData = summary?.child;

        if (weeklySummary) {
          totalTime += weeklySummary.time_spent_minutes || 0;
          totalLessons += weeklySummary.lessons_completed || 0;
          totalPoints += weeklySummary.points_earned || 0;

          if ((weeklySummary.time_spent_minutes || 0) > maxTime && childData?.name) {
            maxTime = weeklySummary.time_spent_minutes;
            mostActive = childData.name;
          }
        }

        // Transform and collect goals with null check
        if (summary?.active_goals && childData?.id) {
          summary.active_goals.forEach(goal => {
            allGoals.push(transformGoal(goal, childData.id));
          });
        }

        // Fetch weekly report with null check
        if (childData?.id) {
          try {
            const report = await parentApi.getWeeklyReport(childData.id);
            if (report) {
              allReports.push(transformReport(report, childData.id));
              totalImprovement += report.comparison?.time_change_percent || 0;
            }
          } catch {
            // Skip this child's report if fetch fails
          }
        }
      }

      setGoals(allGoals);
      setWeeklyReports(allReports);

      setFamilyStats({
        totalTimeThisWeek: totalTime,
        totalStoriesThisWeek: totalLessons,
        totalPointsThisWeek: totalPoints,
        mostActiveChild: mostActive,
        improvementFromLastWeek: Math.round(totalImprovement / Math.max(summaries.length, 1)),
      });

      // Fetch suggested activities
      fetchSuggestedActivities('HINDI', 6);

    } catch (err) {
      console.error('Failed to fetch parent dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [fetchSuggestedActivities]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  if (isLoading) {
    return (
      <div className={cn('min-h-screen bg-gray-50 flex items-center justify-center', className)}>
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-500">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={cn('min-h-screen bg-gray-50 flex items-center justify-center', className)}>
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-gray-700 mb-4">{error}</p>
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('min-h-screen bg-gray-50', className)}>
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Parent Dashboard</h1>
              <p className="text-sm text-gray-500">Track your children&apos;s learning progress</p>
            </div>
            <div className="flex items-center gap-3">
              <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors">
                <Bell size={20} />
              </button>
              <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors">
                <Settings size={20} />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
        {/* Family Stats Overview */}
        <section>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <Clock className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">This Week</p>
                  <p className="text-xl font-bold text-gray-900">
                    {formatDuration(familyStats.totalTimeThisWeek)}
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-secondary-100 rounded-full flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-secondary-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Lessons</p>
                  <p className="text-xl font-bold text-gray-900">
                    {familyStats.totalStoriesThisWeek}
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                  <Star className="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Points</p>
                  <p className="text-xl font-bold text-gray-900">
                    {familyStats.totalPointsThisWeek}
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100"
            >
              <div className="flex items-center gap-3">
                <div className={cn(
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  familyStats.improvementFromLastWeek >= 0 ? 'bg-green-100' : 'bg-red-100'
                )}>
                  {familyStats.improvementFromLastWeek >= 0 ? (
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  ) : (
                    <TrendingDown className="w-5 h-5 text-red-600" />
                  )}
                </div>
                <div>
                  <p className="text-sm text-gray-500">vs Last Week</p>
                  <p className={cn(
                    'text-xl font-bold',
                    familyStats.improvementFromLastWeek >= 0 ? 'text-green-600' : 'text-red-600'
                  )}>
                    {familyStats.improvementFromLastWeek >= 0 ? '+' : ''}
                    {familyStats.improvementFromLastWeek}%
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Children Progress */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Users className="w-5 h-5 text-primary-600" />
              Children&apos;s Progress
            </h2>
            <button className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
              View All <ChevronRight size={16} />
            </button>
          </div>

          {children.length > 0 ? (
            <div className="grid md:grid-cols-2 gap-4">
              {children.map((child, index) => (
                <motion.div
                  key={child.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <ChildProgressCard
                    child={child}
                    onClick={() => setSelectedChild(child.id)}
                    isSelected={selectedChild === child.id}
                  />
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-2xl p-8 text-center border border-gray-100">
              <Users className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No children added yet.</p>
              <button className="mt-3 text-primary-600 hover:text-primary-700 font-medium">
                Add your first child
              </button>
            </div>
          )}
        </section>

        {/* Learning Goals */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Target className="w-5 h-5 text-secondary-600" />
              Learning Goals
            </h2>
            <button className="text-sm text-primary-600 hover:text-primary-700">
              + Add Goal
            </button>
          </div>

          {goals.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {goals.map((goal, index) => (
                <motion.div
                  key={goal.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <GoalCard goal={goal} childName={children.find(c => c.id === goal.childId)?.name || 'Child'} />
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-2xl p-8 text-center border border-gray-100">
              <Target className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No learning goals set yet.</p>
              <button className="mt-3 text-primary-600 hover:text-primary-700 font-medium">
                Create your first goal
              </button>
            </div>
          )}
        </section>

        {/* Suggested Activities */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Suggested Activities
            </h2>
            <button className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
              See More <ChevronRight size={16} />
            </button>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {suggestedActivities.slice(0, 2).map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <ActivitySuggestion activity={activity} />
              </motion.div>
            ))}
          </div>
        </section>

        {/* Weekly Reports */}
        {weeklyReports.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">
                Weekly Reports
              </h2>
              <button className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1">
                View All <ChevronRight size={16} />
              </button>
            </div>

            <div className="space-y-4">
              {weeklyReports.slice(0, 2).map((report, index) => (
                <motion.div
                  key={report.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <WeeklyReportCard
                    report={report}
                    childName={children.find(c => c.id === report.childId)?.name || 'Child'}
                  />
                </motion.div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default ParentDashboard;
