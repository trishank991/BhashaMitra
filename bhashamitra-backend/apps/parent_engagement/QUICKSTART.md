# Quick Start Guide - Parent Dashboard APIs

## Testing the APIs

### Prerequisites

1. Django server running
2. Authentication token (JWT)
3. At least one child profile created
4. Some activity data in the database

### Step 1: Get Your Auth Token

```bash
# Login to get token
curl -X POST https://api.bhashamitra.com/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "parent@example.com", "password": "yourpassword"}'

# Response will include:
# {
#   "access": "your-jwt-token-here",
#   "refresh": "refresh-token-here",
#   "user": {...}
# }
```

Save the `access` token for use in subsequent requests.

### Step 2: Test the Dashboard

```bash
# Get dashboard summary
curl -X GET https://api.bhashamitra.com/api/v1/parent/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Expected response:
{
  "children": [
    {
      "id": "child-uuid-here",
      "name": "Child Name",
      "avatar_url": "🧒",
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

### Step 3: Get Child Progress

```bash
# Replace CHILD_UUID with the ID from dashboard response
curl -X GET https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/progress/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Expected response:
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

### Step 4: Get Activity Feed

```bash
# Get last 7 days of activity
curl -X GET "https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/activity/?days=7" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by type
curl -X GET "https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/activity/?type=LESSON_COMPLETED" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Step 5: Get Weekly Stats

```bash
# Weekly stats
curl -X GET "https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/stats/?period=week" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Monthly stats
curl -X GET "https://api.bhashamitra.com/api/v1/parent/children/CHILD_UUID/stats/?period=month" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using Postman

### 1. Create Environment

```json
{
  "api_base": "https://api.bhashamitra.com",
  "access_token": "your-token-here",
  "child_id": "child-uuid-here"
}
```

### 2. Create Collection

Import these requests:

**Request 1: Dashboard**
- Method: GET
- URL: `{{api_base}}/api/v1/parent/dashboard/`
- Headers: `Authorization: Bearer {{access_token}}`

**Request 2: Child Progress**
- Method: GET
- URL: `{{api_base}}/api/v1/parent/children/{{child_id}}/progress/`
- Headers: `Authorization: Bearer {{access_token}}`

**Request 3: Activity Feed**
- Method: GET
- URL: `{{api_base}}/api/v1/parent/children/{{child_id}}/activity/`
- Headers: `Authorization: Bearer {{access_token}}`
- Params: `days=7`

**Request 4: Weekly Stats**
- Method: GET
- URL: `{{api_base}}/api/v1/parent/children/{{child_id}}/stats/`
- Headers: `Authorization: Bearer {{access_token}}`
- Params: `period=week`

## Using Python Requests

```python
import requests

# Configuration
API_BASE = "https://api.bhashamitra.com"
TOKEN = "your-access-token"
CHILD_ID = "child-uuid"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Get dashboard
response = requests.get(f"{API_BASE}/api/v1/parent/dashboard/", headers=headers)
dashboard = response.json()
print(f"Found {dashboard['total_children']} children")

# Get child progress
response = requests.get(
    f"{API_BASE}/api/v1/parent/children/{CHILD_ID}/progress/",
    headers=headers
)
progress = response.json()
print(f"Lessons completed: {progress['curriculum_progress']['lessons_completed']}")

# Get activity feed
response = requests.get(
    f"{API_BASE}/api/v1/parent/children/{CHILD_ID}/activity/",
    headers=headers,
    params={"days": 7}
)
activities = response.json()
print(f"Recent activities: {len(activities['results'])}")

# Get weekly stats
response = requests.get(
    f"{API_BASE}/api/v1/parent/children/{CHILD_ID}/stats/",
    headers=headers,
    params={"period": "week"}
)
stats = response.json()
print(f"Days active this week: {stats['days_active']}")
```

## Running Django Tests

```bash
# Run all parent engagement tests
cd /home/trishank/BhashaMitra/bhashamitra-backend
python manage.py test apps.parent_engagement.test_parent_dashboard

# Run specific test
python manage.py test apps.parent_engagement.test_parent_dashboard.ParentDashboardAPITest.test_parent_dashboard

# Run with verbose output
python manage.py test apps.parent_engagement.test_parent_dashboard -v 2

# Run with coverage
coverage run --source='apps.parent_engagement' manage.py test apps.parent_engagement.test_parent_dashboard
coverage report
coverage html  # Generate HTML report
```

## Troubleshooting

### Error: 401 Unauthorized

**Problem:** Invalid or expired token

**Solution:**
```bash
# Get new token
curl -X POST https://api.bhashamitra.com/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com", "password": "yourpassword"}'
```

### Error: 404 Not Found

**Problem:** Child doesn't exist or doesn't belong to parent

**Solution:**
1. Verify child_id from dashboard response
2. Ensure child belongs to authenticated parent
3. Check if child was soft-deleted

```bash
# Get all your children
curl -X GET https://api.bhashamitra.com/api/v1/parent/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Error: Empty Data

**Problem:** No activity data in database

**Solution:**
1. Create some test data:
```python
# In Django shell
python manage.py shell

from apps.children.models import Child
from apps.progress.models import DailyProgress
from django.utils import timezone

child = Child.objects.first()
DailyProgress.objects.create(
    child=child,
    date=timezone.now().date(),
    time_spent_minutes=30,
    lessons_completed=2,
    points_earned=50
)
```

### Error: CORS Issues (Frontend)

**Problem:** Cross-Origin Request Blocked

**Solution:**
Check `settings.py` CORS configuration:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://bhashamitra.com"
]
```

## Creating Test Data

### Using Django Admin

1. Navigate to `/admin/`
2. Create child profiles under "Children"
3. Add daily progress entries
4. Create activity logs
5. Add badges

### Using Django Shell

```python
python manage.py shell

from apps.users.models import User
from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.gamification.models import Streak
from django.utils import timezone
from datetime import timedelta

# Get or create parent
parent = User.objects.get(email='parent@example.com')

# Create child
child = Child.objects.create(
    user=parent,
    name='Test Child',
    date_of_birth=timezone.now().date() - timedelta(days=365*6),
    language='HINDI',
    level=2,
    total_points=350
)

# Create streak
Streak.objects.create(
    child=child,
    current_streak=7,
    longest_streak=10
)

# Create daily progress
for i in range(7):
    DailyProgress.objects.create(
        child=child,
        date=timezone.now().date() - timedelta(days=i),
        time_spent_minutes=20 + (i * 3),
        lessons_completed=2,
        games_played=1,
        points_earned=30
    )

# Create activity logs
ActivityLog.objects.create(
    child=child,
    activity_type='LESSON_COMPLETED',
    description='Completed Hindi Alphabet lesson',
    points_earned=10
)
```

## Performance Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.bhashamitra.com/api/v1/parent/dashboard/

# Using wrk
wrk -t4 -c100 -d30s \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.bhashamitra.com/api/v1/parent/dashboard/
```

## Next Steps

1. Integrate with frontend using TypeScript types from FRONTEND_INTEGRATION.md
2. Add caching for frequently accessed endpoints
3. Implement real-time updates with WebSockets
4. Create data visualization components
5. Add export functionality (PDF/CSV)

## Support

- API Documentation: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Frontend Guide: [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)
- Full README: [README.md](./README.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
