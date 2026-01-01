# Parent Engagement App

## Overview

The Parent Engagement app provides comprehensive APIs for parents to monitor and track their children's learning progress in BhashaMitra. This app enables parents to view dashboards, track progress, review activity feeds, and access detailed statistics about their children's learning journey.

## Features

### 1. Dashboard Summary
- View all children at a glance
- Current streak tracking
- Weekly XP summary
- Recent activity counts
- Quick overview of each child's progress

### 2. Detailed Progress Tracking
- Curriculum progression (levels, modules, lessons)
- Vocabulary mastery statistics
- Total learning time tracking
- Badge collection overview

### 3. Activity Feed
- Real-time activity logging
- Filterable by activity type
- Recent activities (last 7 days default)
- Paginated results

### 4. Weekly/Monthly Statistics
- Days active tracking
- Lessons completed count
- Words learned (newly mastered)
- Games played statistics
- Time spent analytics

### 5. Additional Features
- Weekly reports with highlights and suggestions
- Report cards with skill mastery breakdown
- Monthly comparison charts
- Learning goals tracking
- Parent preferences management

## API Endpoints

All endpoints are prefixed with `/api/v1/parent/`

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard/` | GET | Summary of all children |
| `/children/{child_id}/progress/` | GET | Detailed progress for a child |
| `/children/{child_id}/activity/` | GET | Recent activity feed |
| `/children/{child_id}/stats/` | GET | Weekly/monthly statistics |

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API reference.

## File Structure

```
apps/parent_engagement/
├── models.py                    # Data models (ParentPreferences, LearningGoal, etc.)
├── serializers.py               # DRF serializers for API responses
├── views.py                     # API view classes
├── urls.py                      # URL routing configuration
├── admin.py                     # Django admin configuration
├── tests.py                     # Unit tests
├── test_parent_dashboard.py    # API integration tests
├── API_DOCUMENTATION.md         # Complete API documentation
└── README.md                    # This file
```

## Models

### ParentPreferences
Stores parent notification and engagement preferences:
- Notification frequency (DAILY, WEEKLY, MONTHLY, NONE)
- Email reports toggle
- Push notifications toggle
- SMS alerts toggle
- Preferred report day
- Timezone

### LearningGoal
Parent-set learning goals for children:
- Goal types: DAILY_MINUTES, WEEKLY_STORIES, MONTHLY_POINTS, LEVEL_TARGET
- Target value and current progress
- Start/end dates
- Active status

### WeeklyReport
Auto-generated weekly progress reports:
- Total time, stories completed, points earned
- New words learned
- Achievements unlocked
- Areas of strength/improvement
- Peppi interaction count

### ParentChildActivity
Suggested parent-child activities:
- Activity types: READ_TOGETHER, PRACTICE_LETTERS, CULTURAL_CRAFT, etc.
- Age-appropriate filtering
- Materials needed
- Learning outcomes

## Usage Examples

### Get Dashboard Summary

```python
# In your Django view or API client
from apps.parent_engagement.views import ParentDashboardView

# The view automatically filters children for the authenticated user
# GET /api/v1/parent/dashboard/
# Returns all children with weekly stats
```

### Get Child Progress

```python
# GET /api/v1/parent/children/{child_id}/progress/
# Returns:
# - Curriculum progress (levels, modules, lessons)
# - Vocabulary stats (mastered, in-progress, reviews)
# - Time spent (minutes, hours)
# - Badges earned
```

### Get Activity Feed

```python
# GET /api/v1/parent/children/{child_id}/activity/?days=7&type=LESSON_COMPLETED
# Returns paginated activity log with filters
```

### Get Weekly Stats

```python
# GET /api/v1/parent/children/{child_id}/stats/?period=week
# Returns aggregated stats for the current week
```

## Security & Permissions

All views implement:
1. **Authentication Required**: Uses `IsAuthenticated` permission class
2. **Parent-Child Validation**: Verifies child belongs to authenticated parent
3. **Soft-Delete Filtering**: Only returns non-deleted children
4. **404 Protection**: Returns 404 (not 403) for unauthorized access

Example validation code:
```python
child = get_object_or_404(
    Child,
    id=child_id,
    user=request.user,
    deleted_at__isnull=True
)
```

## Testing

Run the test suite:

```bash
# Run all parent engagement tests
python manage.py test apps.parent_engagement

# Run specific test class
python manage.py test apps.parent_engagement.test_parent_dashboard.ParentDashboardAPITest

# Run with coverage
coverage run --source='apps.parent_engagement' manage.py test apps.parent_engagement
coverage report
```

## Dependencies

The app integrates with:
- `apps.children` - Child profiles
- `apps.users` - Parent user accounts
- `apps.progress` - DailyProgress, ActivityLog
- `apps.gamification` - Streak, ChildBadge, Badge
- `apps.curriculum` - LevelProgress, ModuleProgress, LessonProgress
- `apps.curriculum.models.vocabulary` - WordProgress, VocabularyWord

## Data Flow

```
Parent authenticates
    ↓
GET /api/v1/parent/dashboard/
    ↓
ParentDashboardView queries:
    - Child.objects.filter(user=request.user)
    - Streak.objects (for streak_count)
    - DailyProgress.objects (for xp_this_week)
    - ActivityLog.objects (for recent_activity_count)
    ↓
ChildSummarySerializer formats response
    ↓
Returns JSON with all children data
```

## Performance Considerations

1. **Efficient Queries**: Uses `aggregate()` and `annotate()` for statistics
2. **Pagination**: Activity feed uses pagination to limit response size
3. **Query Optimization**: Minimal database hits per request
4. **Caching**: Consider adding cache for frequently accessed data

Example optimization:
```python
# Instead of multiple queries
xp_this_week = DailyProgress.objects.filter(...).aggregate(total_xp=Sum('points_earned'))['total_xp'] or 0

# Could be cached:
@cache_page(60 * 5)  # Cache for 5 minutes
def get_xp_this_week(child):
    ...
```

## Future Enhancements

Potential improvements:
1. **Real-time Updates**: WebSocket support for live activity feed
2. **Export Reports**: PDF/CSV export functionality
3. **Comparison Charts**: Visual progress charts over time
4. **Notifications**: Push notifications for achievements
5. **Goals Recommendations**: AI-powered goal suggestions
6. **Multi-child Comparison**: Compare progress across siblings
7. **Downloadable Reports**: Monthly/yearly summary PDFs

## Contributing

When adding new features:
1. Add models to `models.py` if needed
2. Create serializers in `serializers.py`
3. Implement views in `views.py`
4. Add URL routes in `urls.py`
5. Write tests in `test_parent_dashboard.py`
6. Update `API_DOCUMENTATION.md`

## Support

For issues or questions:
- Create an issue in the BhashaMitra repository
- Contact the development team
- Check the API documentation for endpoint details

## License

Part of the BhashaMitra project.
