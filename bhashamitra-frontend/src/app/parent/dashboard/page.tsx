'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { MainLayout } from '@/components/layout';
import { Card, CardContent, CardHeader, CardTitle, Loading, Badge, Avatar, Button, SubscriptionBadge } from '@/components/ui';
import { useAuthStore } from '@/stores';
import api from '@/lib/api';
import { ParentDashboard, Activity, ChildSummary } from '@/types';
import { fadeInUp } from '@/lib/constants';

// Child Summary Card Component
function ChildSummaryCard({ child }: { child: ChildSummary }) {
  const router = useRouter();
  const levelProgress = (child.total_xp % 100) / 100 * 100; // Mock calculation

  return (
    <Card
      interactive
      className="overflow-hidden"
      onClick={() => router.push(`/parent/children/${child.id}`)}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            <Avatar
              src={child.avatar}
              name={child.name}
              size="lg"
              ring
            />
            <div>
              <h3 className="font-bold text-gray-900">{child.name}</h3>
              <Badge variant="primary" size="sm">
                Level {child.level}
              </Badge>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          {/* Streak */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Streak</span>
            <div className="flex items-center gap-1">
              <span className="text-lg">🔥</span>
              <span className="font-bold text-orange-600">{child.streak_count} days</span>
            </div>
          </div>

          {/* XP This Week */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">XP This Week</span>
            <span className="font-bold text-primary-600">{child.xp_this_week} XP</span>
          </div>

          {/* Progress Bar */}
          <div className="mt-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-gray-500">Progress to Level {child.level + 1}</span>
              <span className="text-xs font-medium text-gray-700">{levelProgress.toFixed(0)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${levelProgress}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          className="w-full mt-4"
          onClick={(e) => {
            e?.stopPropagation();
            router.push(`/parent/children/${child.id}`);
          }}
        >
          View Details
        </Button>
      </CardContent>
    </Card>
  );
}

// Activity Feed Component
function ActivityFeed({ activities }: { activities: Activity[] }) {
  const getActivityIcon = (type: Activity['activity_type']) => {
    switch (type) {
      case 'lesson':
        return '📚';
      case 'game':
        return '🎮';
      case 'badge':
        return '🏆';
      default:
        return '✨';
    }
  };

  const getTimeAgo = (timestamp: string) => {
    const now = new Date();
    const activityDate = new Date(timestamp);
    const diffMs = now.getTime() - activityDate.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p className="text-lg mb-2">No recent activities</p>
        <p className="text-sm">Activities will appear here as your children learn</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {activities.map((activity) => (
        <motion.div
          key={activity.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-start gap-3 p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors"
        >
          <span className="text-2xl">{getActivityIcon(activity.activity_type)}</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-gray-900">
              <span className="font-semibold">{activity.child_name}</span> {activity.description}
            </p>
            <p className="text-xs text-gray-500 mt-1">{getTimeAgo(activity.timestamp)}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

// Main Parent Dashboard Page
export default function ParentDashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<ParentDashboard | null>(null);
  const [recentActivities, setRecentActivities] = useState<Activity[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Check authentication and role
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (user?.role !== 'parent') {
      router.push('/home');
      return;
    }
  }, [isAuthenticated, user, router]);

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!isAuthenticated || user?.role !== 'parent') {
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        // Fetch parent dashboard
        const dashboardRes = await api.getParentDashboard();
        if (!dashboardRes.success || !dashboardRes.data) {
          throw new Error(dashboardRes.error || 'Failed to load dashboard');
        }

        setDashboardData(dashboardRes.data);

        // Fetch recent activities for all children
        const activityPromises = dashboardRes.data.children.map((child) =>
          api.getChildActivity(child.id)
        );

        const activityResults = await Promise.all(activityPromises);
        const allActivities: Activity[] = [];

        activityResults.forEach((result) => {
          if (result.success && result.data) {
            allActivities.push(...result.data);
          }
        });

        // Sort by timestamp and take last 10
        allActivities.sort(
          (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        );
        setRecentActivities(allActivities.slice(0, 10));
      } catch (err) {
        console.error('[ParentDashboard] Error fetching data:', err);
        setError(err instanceof Error ? err.message : 'Failed to load dashboard');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, [isAuthenticated, user]);

  // Show loading state
  if (isLoading || !user) {
    return (
      <MainLayout>
        <div className="min-h-[60vh] flex items-center justify-center">
          <Loading size="lg" text="Loading your dashboard..." />
        </div>
      </MainLayout>
    );
  }

  // Show error state
  if (error) {
    return (
      <MainLayout>
        <div className="min-h-[60vh] flex flex-col items-center justify-center">
          <div className="text-6xl mb-4">😔</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Oops!</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </MainLayout>
    );
  }

  // Calculate total family streak (all kids with active streaks)
  const totalFamilyStreak = dashboardData?.children.reduce(
    (sum, child) => sum + (child.streak_count > 0 ? 1 : 0),
    0
  ) || 0;

  return (
    <MainLayout showPeppi={false}>
      {/* Header Section */}
      <motion.div variants={fadeInUp} initial="initial" animate="animate" className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Family Dashboard</h1>
            <p className="text-gray-600 mt-1">Welcome back, {user.name}!</p>
          </div>
          {user.subscription_tier && (
            <SubscriptionBadge tier={user.subscription_tier} size="lg" />
          )}
        </div>
      </motion.div>

      {/* Quick Stats */}
      <motion.div
        variants={fadeInUp}
        initial="initial"
        animate="animate"
        transition={{ delay: 0.1 }}
        className="grid grid-cols-3 gap-4 mb-6"
      >
        {/* Total Family Time */}
        <Card variant="elevated" padding="sm">
          <CardContent className="text-center py-3">
            <div className="text-3xl mb-2">⏱️</div>
            <div className="text-2xl font-bold text-primary-600">
              {dashboardData?.total_family_time || 0}
            </div>
            <div className="text-xs text-gray-600 mt-1">Minutes This Week</div>
          </CardContent>
        </Card>

        {/* Family Streak */}
        <Card variant="elevated" padding="sm">
          <CardContent className="text-center py-3">
            <div className="text-3xl mb-2">🔥</div>
            <div className="text-2xl font-bold text-orange-600">{totalFamilyStreak}</div>
            <div className="text-xs text-gray-600 mt-1">Active Streaks</div>
          </CardContent>
        </Card>

        {/* Badges This Week */}
        <Card variant="elevated" padding="sm">
          <CardContent className="text-center py-3">
            <div className="text-3xl mb-2">🏆</div>
            <div className="text-2xl font-bold text-accent-600">
              {dashboardData?.badges_this_week || 0}
            </div>
            <div className="text-xs text-gray-600 mt-1">Badges Earned</div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Children Summary Cards */}
      <motion.div
        variants={fadeInUp}
        initial="initial"
        animate="animate"
        transition={{ delay: 0.2 }}
        className="mb-6"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-4">Your Children</h2>
        {dashboardData?.children && dashboardData.children.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {dashboardData.children.map((child) => (
              <ChildSummaryCard key={child.id} child={child} />
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="text-center py-8">
              <div className="text-6xl mb-4">👨‍👩‍👧‍👦</div>
              <p className="text-gray-600 mb-4">No children profiles yet</p>
              <Button onClick={() => router.push('/onboarding/child')}>Add a Child</Button>
            </CardContent>
          </Card>
        )}
      </motion.div>

      {/* Recent Activity Feed */}
      <motion.div
        variants={fadeInUp}
        initial="initial"
        animate="animate"
        transition={{ delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <ActivityFeed activities={recentActivities} />
          </CardContent>
        </Card>
      </motion.div>
    </MainLayout>
  );
}
