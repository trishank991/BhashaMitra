# Parent Dashboard API Documentation

## Overview

The Parent Dashboard APIs provide comprehensive endpoints for parents to monitor their children's learning progress in BhashaMitra. All endpoints require authentication and ensure parents can only access data for their own children.

**Base URL:** `/api/v1/parent/`

**Authentication:** Required (JWT token in Authorization header)

---

## Endpoints

### 1. Parent Dashboard Summary

**GET** `/api/v1/parent/dashboard/`

Returns a summary of all children associated with the authenticated parent.

#### Response

```json
{
  "children": [
    {
      "id": "uuid",
      "name": "Child Name",
      "avatar_url": "emoji or avatar path",
      "level": 2,
      "total_points": 350,
      "streak_count": 7,
      "xp_this_week": 140,
      "recent_activity_count": 15,
      "age": 6,
      "language": "HINDI"
    }
  ],
  "total_children": 1
}
```

#### Fields

- `id`: Unique identifier for the child
- `name`: Child's display name
- `avatar_url`: Avatar emoji or image path
- `level`: Current curriculum level (1-10)
- `total_points`: All-time points earned
- `streak_count`: Current consecutive days active
- `xp_this_week`: Points earned this week (Monday-today)
- `recent_activity_count`: Number of activities in last 7 days
- `age`: Child's age in years
- `language`: Learning language (HINDI, GUJARATI, etc.)

---

### 2. Child Detailed Progress

**GET** `/api/v1/parent/children/{child_id}/progress/`

Returns detailed progress information for a specific child, including curriculum progress, vocabulary stats, and time spent.

#### Path Parameters

- `child_id` (UUID): The child's unique identifier

#### Response

```json
{
  "curriculum_progress": {
    "current_level": 2,
    "levels_completed": 1,
    "modules_completed": 8,
    "lessons_completed": 24,
    "total_modules": 10
  },
  "vocabulary_stats": {
    "words_mastered": 45,
    "words_in_progress": 12,
    "total_reviews": 230
  },
  "time_spent": {
    "total_minutes": 1240,
    "total_hours": 20.7
  },
  "badges_earned": 5,
  "current_level": 2
}
```

#### Fields

**curriculum_progress:**
- `current_level`: Current curriculum level
- `levels_completed`: Number of levels fully completed
- `modules_completed`: Number of modules completed
- `lessons_completed`: Total lessons finished
- `total_modules`: Total modules started

**vocabulary_stats:**
- `words_mastered`: Words marked as mastered (90%+ accuracy, 21+ day interval)
- `words_in_progress`: Words being learned but not yet mastered
- `total_reviews`: Total number of vocabulary reviews completed

**time_spent:**
- `total_minutes`: All-time learning time in minutes
- `total_hours`: All-time learning time in hours (rounded to 1 decimal)

---

### 3. Child Activity Feed

**GET** `/api/v1/parent/children/{child_id}/activity/`

Returns recent activity log for a child. Supports pagination and filtering.

#### Path Parameters

- `child_id` (UUID): The child's unique identifier

#### Query Parameters

- `type` (optional): Filter by activity type (LESSON_COMPLETED, GAME_COMPLETED, BADGE_EARNED, etc.)
- `days` (optional): Number of days to look back (default: 7)
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

#### Response

```json
{
  "count": 20,
  "next": "url_to_next_page",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "activity_type": "LESSON_COMPLETED",
      "description": "Completed lesson: Hindi Alphabet A-Ka",
      "points_earned": 10,
      "created_at": "2024-12-26T10:30:00Z",
      "time_ago": "2 hours ago",
      "icon": "✅"
    }
  ]
}
```

#### Activity Types

- `LESSON_STARTED`: Started a new lesson
- `LESSON_COMPLETED`: Completed a lesson
- `EXERCISE_COMPLETED`: Finished an exercise
- `GAME_COMPLETED`: Played a game
- `BADGE_EARNED`: Earned a badge
- `LEVEL_UP`: Advanced to next level
- `STREAK_MILESTONE`: Reached streak milestone
- `FIRST_LOGIN`: First time login

---

### 4. Child Stats (Weekly/Monthly)

**GET** `/api/v1/parent/children/{child_id}/stats/`

Returns aggregated statistics for a child over a specified time period.

#### Path Parameters

- `child_id` (UUID): The child's unique identifier

#### Query Parameters

- `period` (optional): Time period - `week` or `month` (default: `week`)
  - `week`: Current week (Monday to today)
  - `month`: Last 30 days

#### Response

```json
{
  "period": "This week",
  "days_active": 5,
  "lessons_completed": 8,
  "words_learned": 15,
  "games_played": 6,
  "total_time_minutes": 145,
  "total_points": 180
}
```

#### Fields

- `period`: Human-readable period label ("This week" or "Last 30 days")
- `days_active`: Number of days with learning activity (time_spent > 0)
- `lessons_completed`: Total lessons finished in period
- `words_learned`: New words mastered in this period
- `games_played`: Total games played
- `total_time_minutes`: Total learning time in minutes
- `total_points`: Total XP/points earned

---

## Additional Endpoints

### 5. Child Summary

**GET** `/api/v1/parent/children/{child_id}/summary/`

Comprehensive weekly summary with current streak, achievements, and active goals.

### 6. Weekly Report

**GET** `/api/v1/parent/children/{child_id}/weekly-report/`

Detailed 7-day breakdown with daily stats, highlights, and suggestions.

### 7. Report Card

**GET** `/api/v1/parent/children/{child_id}/report-card/?period=30`

Comprehensive report card with skill mastery breakdown.

### 8. Skills Breakdown

**GET** `/api/v1/parent/children/{child_id}/skills/`

Detailed skill mastery across all learning areas.

### 9. Monthly Stats Comparison

**GET** `/api/v1/parent/children/{child_id}/monthly-stats/?months=3`

Month-over-month progress comparison.

---

## Security & Permissions

All endpoints implement the following security measures:

1. **Authentication Required**: All requests must include a valid JWT token
2. **Parent-Child Validation**: Each request verifies that the child belongs to the authenticated parent
3. **Soft-Delete Filtering**: Only non-deleted children are returned
4. **404 on Unauthorized**: Returns 404 (not 403) if child doesn't belong to parent for security

### Example Error Responses

**401 Unauthorized** - Missing or invalid authentication
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found** - Child not found or doesn't belong to parent
```json
{
  "detail": "Not found."
}
```

---

## Usage Examples

### cURL Examples

#### Get Dashboard
```bash
curl -X GET \
  'https://api.bhashamitra.com/api/v1/parent/dashboard/' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

#### Get Child Progress
```bash
curl -X GET \
  'https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/progress/' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

#### Get Weekly Stats
```bash
curl -X GET \
  'https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/stats/?period=week' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

#### Get Activity Feed
```bash
curl -X GET \
  'https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/activity/?days=7&type=LESSON_COMPLETED' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

### JavaScript/TypeScript Example

```typescript
const API_BASE = 'https://api.bhashamitra.com';

// Get dashboard
async function getDashboard(token: string) {
  const response = await fetch(`${API_BASE}/api/v1/parent/dashboard/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return await response.json();
}

// Get child progress
async function getChildProgress(token: string, childId: string) {
  const response = await fetch(
    `${API_BASE}/api/v1/parent/children/${childId}/progress/`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return await response.json();
}

// Get child stats
async function getChildStats(
  token: string,
  childId: string,
  period: 'week' | 'month' = 'week'
) {
  const response = await fetch(
    `${API_BASE}/api/v1/parent/children/${childId}/stats/?period=${period}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return await response.json();
}
```

---

## Data Models Reference

### Child Model
```python
{
  'id': UUID,
  'user': User,
  'name': str,
  'avatar': str,
  'date_of_birth': date,
  'language': str,
  'level': int (1-10),
  'total_points': int,
  'peppi_addressing': str,
  'peppi_gender': str
}
```

### DailyProgress Model
```python
{
  'child': Child,
  'date': date,
  'time_spent_minutes': int,
  'lessons_completed': int,
  'exercises_completed': int,
  'games_played': int,
  'points_earned': int
}
```

### ActivityLog Model
```python
{
  'child': Child,
  'activity_type': str,
  'description': str,
  'points_earned': int,
  'metadata': dict,
  'created_at': datetime
}
```

### Streak Model
```python
{
  'child': Child,
  'current_streak': int,
  'longest_streak': int,
  'last_activity_date': date
}
```

---

## Rate Limiting

Standard rate limits apply:
- Authenticated requests: 100 requests/minute
- Dashboard endpoint: 30 requests/minute (heavier queries)

---

## Changelog

### Version 1.0 (December 2024)
- Initial release of Parent Dashboard APIs
- Dashboard summary endpoint
- Child progress endpoint
- Activity feed endpoint
- Stats endpoint (weekly/monthly)
- Proper authentication and authorization
- Parent-child relationship validation
