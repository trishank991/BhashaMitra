# Frontend Integration Guide

## Quick Start for Frontend Developers

This guide helps you integrate the Parent Dashboard APIs into the BhashaMitra frontend.

## Authentication

All API requests require a JWT token in the Authorization header:

```typescript
const headers = {
  'Authorization': `Bearer ${userToken}`,
  'Content-Type': 'application/json'
};
```

## TypeScript Types

### Dashboard Types

```typescript
interface ChildSummary {
  id: string;
  name: string;
  avatar_url: string;
  level: number;
  total_points: number;
  streak_count: number;
  xp_this_week: number;
  recent_activity_count: number;
  age: number;
  language: 'HINDI' | 'GUJARATI' | 'PUNJABI' | 'TAMIL' | 'TELUGU' | 'MALAYALAM' | 'FIJI_HINDI';
}

interface DashboardResponse {
  children: ChildSummary[];
  total_children: number;
}
```

### Progress Types

```typescript
interface CurriculumProgress {
  current_level: number;
  levels_completed: number;
  modules_completed: number;
  lessons_completed: number;
  total_modules: number;
}

interface VocabularyStats {
  words_mastered: number;
  words_in_progress: number;
  total_reviews: number;
}

interface TimeSpent {
  total_minutes: number;
  total_hours: number;
}

interface ChildProgress {
  curriculum_progress: CurriculumProgress;
  vocabulary_stats: VocabularyStats;
  time_spent: TimeSpent;
  badges_earned: number;
  current_level: number;
}
```

### Activity Types

```typescript
type ActivityType =
  | 'LESSON_STARTED'
  | 'LESSON_COMPLETED'
  | 'EXERCISE_COMPLETED'
  | 'GAME_COMPLETED'
  | 'BADGE_EARNED'
  | 'LEVEL_UP'
  | 'STREAK_MILESTONE'
  | 'FIRST_LOGIN';

interface Activity {
  id: string;
  activity_type: ActivityType;
  description: string;
  points_earned: number;
  created_at: string;
  time_ago: string;
  icon: string;
}

interface ActivityResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Activity[];
}
```

### Stats Types

```typescript
interface ChildStats {
  period: string;
  days_active: number;
  lessons_completed: number;
  words_learned: number;
  games_played: number;
  total_time_minutes: number;
  total_points: number;
}
```

## API Service Implementation

### Create API Service

```typescript
// services/parentDashboard.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://api.bhashamitra.com';

export class ParentDashboardService {
  private static getHeaders(token: string) {
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  }

  /**
   * Get dashboard summary for all children
   */
  static async getDashboard(token: string): Promise<DashboardResponse> {
    const response = await fetch(`${API_BASE}/api/v1/parent/dashboard/`, {
      headers: this.getHeaders(token)
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch dashboard: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Get detailed progress for a specific child
   */
  static async getChildProgress(
    token: string,
    childId: string
  ): Promise<ChildProgress> {
    const response = await fetch(
      `${API_BASE}/api/v1/parent/children/${childId}/progress/`,
      { headers: this.getHeaders(token) }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch child progress: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Get activity feed for a child
   */
  static async getChildActivity(
    token: string,
    childId: string,
    options?: {
      type?: ActivityType;
      days?: number;
      page?: number;
    }
  ): Promise<ActivityResponse> {
    const params = new URLSearchParams();
    if (options?.type) params.append('type', options.type);
    if (options?.days) params.append('days', options.days.toString());
    if (options?.page) params.append('page', options.page.toString());

    const url = `${API_BASE}/api/v1/parent/children/${childId}/activity/?${params}`;
    const response = await fetch(url, {
      headers: this.getHeaders(token)
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch activity: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Get weekly or monthly stats for a child
   */
  static async getChildStats(
    token: string,
    childId: string,
    period: 'week' | 'month' = 'week'
  ): Promise<ChildStats> {
    const response = await fetch(
      `${API_BASE}/api/v1/parent/children/${childId}/stats/?period=${period}`,
      { headers: this.getHeaders(token) }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch stats: ${response.statusText}`);
    }

    return await response.json();
  }
}
```

## React Hooks

### useDashboard Hook

```typescript
// hooks/useDashboard.ts
import { useQuery } from '@tanstack/react-query';
import { ParentDashboardService } from '@/services/parentDashboard';

export function useDashboard(token: string) {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: () => ParentDashboardService.getDashboard(token),
    enabled: !!token,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### useChildProgress Hook

```typescript
// hooks/useChildProgress.ts
import { useQuery } from '@tanstack/react-query';
import { ParentDashboardService } from '@/services/parentDashboard';

export function useChildProgress(token: string, childId: string) {
  return useQuery({
    queryKey: ['child-progress', childId],
    queryFn: () => ParentDashboardService.getChildProgress(token, childId),
    enabled: !!token && !!childId,
    staleTime: 5 * 60 * 1000,
  });
}
```

### useChildActivity Hook

```typescript
// hooks/useChildActivity.ts
import { useQuery } from '@tanstack/react-query';
import { ParentDashboardService } from '@/services/parentDashboard';

export function useChildActivity(
  token: string,
  childId: string,
  options?: { type?: ActivityType; days?: number }
) {
  return useQuery({
    queryKey: ['child-activity', childId, options],
    queryFn: () => ParentDashboardService.getChildActivity(token, childId, options),
    enabled: !!token && !!childId,
    staleTime: 2 * 60 * 1000, // 2 minutes for recent activity
  });
}
```

### useChildStats Hook

```typescript
// hooks/useChildStats.ts
import { useQuery } from '@tanstack/react-query';
import { ParentDashboardService } from '@/services/parentDashboard';

export function useChildStats(
  token: string,
  childId: string,
  period: 'week' | 'month' = 'week'
) {
  return useQuery({
    queryKey: ['child-stats', childId, period],
    queryFn: () => ParentDashboardService.getChildStats(token, childId, period),
    enabled: !!token && !!childId,
    staleTime: 5 * 60 * 1000,
  });
}
```

## Component Examples

### Dashboard Component

```typescript
// components/ParentDashboard.tsx
'use client';

import { useDashboard } from '@/hooks/useDashboard';
import { useAuth } from '@/hooks/useAuth';

export function ParentDashboard() {
  const { token } = useAuth();
  const { data, isLoading, error } = useDashboard(token);

  if (isLoading) return <div>Loading dashboard...</div>;
  if (error) return <div>Error loading dashboard</div>;

  return (
    <div className="dashboard">
      <h1>My Children's Progress</h1>
      <div className="children-grid">
        {data?.children.map(child => (
          <ChildCard key={child.id} child={child} />
        ))}
      </div>
    </div>
  );
}
```

### Child Card Component

```typescript
// components/ChildCard.tsx
interface ChildCardProps {
  child: ChildSummary;
}

export function ChildCard({ child }: ChildCardProps) {
  return (
    <div className="child-card">
      <div className="avatar">{child.avatar_url}</div>
      <h3>{child.name}</h3>
      <div className="stats">
        <div className="stat">
          <span className="label">Level</span>
          <span className="value">{child.level}</span>
        </div>
        <div className="stat">
          <span className="label">Streak</span>
          <span className="value">🔥 {child.streak_count} days</span>
        </div>
        <div className="stat">
          <span className="label">This Week</span>
          <span className="value">⭐ {child.xp_this_week} XP</span>
        </div>
      </div>
      <Link href={`/parent/children/${child.id}`}>
        View Details
      </Link>
    </div>
  );
}
```

### Child Progress Page

```typescript
// app/parent/children/[id]/page.tsx
'use client';

import { useChildProgress, useChildStats, useChildActivity } from '@/hooks';
import { useAuth } from '@/hooks/useAuth';

export default function ChildProgressPage({ params }: { params: { id: string } }) {
  const { token } = useAuth();
  const { data: progress } = useChildProgress(token, params.id);
  const { data: stats } = useChildStats(token, params.id, 'week');
  const { data: activity } = useChildActivity(token, params.id, { days: 7 });

  return (
    <div className="child-progress-page">
      <ProgressOverview progress={progress} />
      <WeeklyStats stats={stats} />
      <ActivityFeed activities={activity?.results} />
    </div>
  );
}
```

### Activity Feed Component

```typescript
// components/ActivityFeed.tsx
interface ActivityFeedProps {
  activities?: Activity[];
}

export function ActivityFeed({ activities }: ActivityFeedProps) {
  if (!activities?.length) {
    return <div>No recent activities</div>;
  }

  return (
    <div className="activity-feed">
      <h2>Recent Activity</h2>
      <div className="activities">
        {activities.map(activity => (
          <div key={activity.id} className="activity-item">
            <span className="icon">{activity.icon}</span>
            <div className="content">
              <p className="description">{activity.description}</p>
              <span className="time">{activity.time_ago}</span>
            </div>
            <span className="points">+{activity.points_earned} XP</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Error Handling

```typescript
// utils/apiError.ts
export class APIError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function handleAPIResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new APIError(response.status, response.statusText, data);
  }
  return await response.json();
}

// Usage in service
static async getDashboard(token: string): Promise<DashboardResponse> {
  const response = await fetch(`${API_BASE}/api/v1/parent/dashboard/`, {
    headers: this.getHeaders(token)
  });
  return handleAPIResponse<DashboardResponse>(response);
}
```

## Loading States

```typescript
// components/LoadingStates.tsx
export function DashboardSkeleton() {
  return (
    <div className="dashboard-skeleton">
      <div className="skeleton-card" />
      <div className="skeleton-card" />
      <div className="skeleton-card" />
    </div>
  );
}

export function ProgressSkeleton() {
  return (
    <div className="progress-skeleton">
      <div className="skeleton-bar" />
      <div className="skeleton-stats" />
    </div>
  );
}
```

## Caching Strategy

```typescript
// queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

// Prefetch data
export async function prefetchDashboard(token: string) {
  await queryClient.prefetchQuery({
    queryKey: ['dashboard'],
    queryFn: () => ParentDashboardService.getDashboard(token),
  });
}
```

## Testing

```typescript
// __tests__/services/parentDashboard.test.ts
import { ParentDashboardService } from '@/services/parentDashboard';

describe('ParentDashboardService', () => {
  it('fetches dashboard data', async () => {
    const data = await ParentDashboardService.getDashboard('test-token');
    expect(data).toHaveProperty('children');
    expect(data).toHaveProperty('total_children');
  });

  it('handles authentication errors', async () => {
    await expect(
      ParentDashboardService.getDashboard('invalid-token')
    ).rejects.toThrow();
  });
});
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://api.bhashamitra.com
```

## Best Practices

1. **Always handle loading states**
2. **Implement proper error boundaries**
3. **Use React Query for caching**
4. **Validate child_id before API calls**
5. **Show skeleton loaders during fetches**
6. **Implement retry logic for failed requests**
7. **Cache aggressively for stats (5-10 minutes)**
8. **Keep activity feed fresh (2-3 minutes)**

## Common Pitfalls

1. **Not checking if token exists before API call**
2. **Forgetting to handle 404 for non-existent children**
3. **Not implementing pagination for activity feed**
4. **Hardcoding API URL instead of using env variable**
5. **Not handling network errors gracefully**

## Support

For frontend integration questions:
- Check API_DOCUMENTATION.md for endpoint details
- Review example components above
- Test endpoints with Postman/Insomnia first
- Contact backend team for API issues
