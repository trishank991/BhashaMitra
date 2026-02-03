# BhashaMitra - Complete Implementation Guide

> **Part 2**: Stories, Progress, Gamification, and Speech Services

---

# Part 2: Stories, Progress, Gamification & Speech

## Table of Contents
1. [Stories & StoryWeaver Integration](#1-stories--storyweaver-integration)
2. [Progress Tracking](#2-progress-tracking)
3. [Gamification System](#3-gamification-system)
4. [Speech Services (Bhashini)](#4-speech-services-bhashini)
5. [External API Clients](#5-external-api-clients)

---

## 1. Stories & StoryWeaver Integration

### apps/stories/models.py
```python
"""Story models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Story(TimeStampedModel):
    """Story content cached from StoryWeaver."""
    
    storyweaver_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500)
    title_translit = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    page_count = models.IntegerField()
    cover_image_url = models.URLField()
    synopsis = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    illustrator = models.CharField(max_length=255, blank=True, null=True)
    categories = models.JSONField(default=list)
    cached_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stories'
        indexes = [
            models.Index(fields=['language', 'level']),
            models.Index(fields=['storyweaver_id']),
        ]
        verbose_name_plural = 'stories'
    
    def __str__(self):
        return f"{self.title} (Level {self.level})"


class StoryPage(TimeStampedModel):
    """Individual pages of a story."""
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    text_content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)  # Cached TTS
    
    class Meta:
        db_table = 'story_pages'
        unique_together = ['story', 'page_number']
        ordering = ['page_number']
    
    def __str__(self):
        return f"{self.story.title} - Page {self.page_number}"
```

### apps/stories/serializers.py
```python
"""Story serializers."""
from rest_framework import serializers
from .models import Story, StoryPage


class StoryPageSerializer(serializers.ModelSerializer):
    """Story page serializer."""
    
    class Meta:
        model = StoryPage
        fields = ['page_number', 'text_content', 'image_url', 'audio_url']


class StoryListSerializer(serializers.ModelSerializer):
    """Lightweight story list serializer."""
    
    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'title', 'title_translit', 'language',
            'level', 'page_count', 'cover_image_url', 'synopsis', 'author', 'categories'
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    """Full story with pages."""
    pages = StoryPageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'title', 'title_translit', 'language',
            'level', 'page_count', 'cover_image_url', 'synopsis', 'author',
            'illustrator', 'categories', 'pages'
        ]
```

### apps/stories/views.py
```python
"""Story views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Story
from .serializers import StoryListSerializer, StoryDetailSerializer


class StoryListView(APIView):
    """List stories with filters."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        language = request.query_params.get('language')
        level = request.query_params.get('level')
        limit = int(request.query_params.get('limit', 20))
        
        if not language:
            return Response(
                {'detail': 'language parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = Story.objects.filter(language=language)
        if level:
            queryset = queryset.filter(level=level)
        
        stories = queryset[:limit]
        serializer = StoryListSerializer(stories, many=True)
        
        return Response({
            'data': serializer.data,
            'meta': {'total': len(serializer.data)}
        })


class StoryDetailView(APIView):
    """Get story with pages."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            story = Story.objects.prefetch_related('pages').get(pk=pk)
        except Story.DoesNotExist:
            return Response({'detail': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StoryDetailSerializer(story)
        return Response({'data': serializer.data})
```

### apps/stories/urls.py
```python
"""Story URL configuration."""
from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
    path('<uuid:pk>/', views.StoryDetailView.as_view(), name='detail'),
]
```

---

## 2. Progress Tracking

### apps/progress/models.py
```python
"""Progress models."""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child
from apps.stories.models import Story


class Progress(TimeStampedModel):
    """Reading progress for a child on a story."""
    
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='progress_records')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='progress_records')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    current_page = models.IntegerField(default=0)
    pages_completed = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'progress'
        unique_together = ['child', 'story']
    
    def __str__(self):
        return f"{self.child.name} - {self.story.title} ({self.status})"


class DailyActivity(TimeStampedModel):
    """Aggregated daily activity for analytics."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField()
    stories_started = models.IntegerField(default=0)
    stories_completed = models.IntegerField(default=0)
    pages_read = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    recordings_made = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'daily_activities'
        unique_together = ['child', 'date']
```

### apps/progress/services.py
```python
"""Progress services."""
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from .models import Progress, DailyActivity


class ProgressService:
    """Service for managing progress."""
    
    @staticmethod
    @transaction.atomic
    def start_story(child, story) -> Progress:
        """Start or resume a story."""
        progress, created = Progress.objects.get_or_create(
            child=child,
            story=story,
            defaults={
                'status': Progress.Status.IN_PROGRESS,
                'started_at': timezone.now(),
                'last_read_at': timezone.now(),
            }
        )
        
        if created:
            points = settings.POINTS_CONFIG['STORY_STARTED']
            child.total_points += points
            child.save(update_fields=['total_points'])
            progress.points_earned = points
            progress.save()
            
            ProgressService._update_daily_activity(child, stories_started=1, points=points)
        
        return progress
    
    @staticmethod
    @transaction.atomic
    def update_progress(progress, current_page: int, time_spent: int = 0) -> Progress:
        """Update reading progress."""
        pages_read = max(0, current_page - progress.current_page)
        
        progress.current_page = current_page
        progress.pages_completed = current_page
        progress.time_spent_seconds += time_spent
        progress.last_read_at = timezone.now()
        
        if progress.status == Progress.Status.NOT_STARTED:
            progress.status = Progress.Status.IN_PROGRESS
            progress.started_at = timezone.now()
        
        if pages_read > 0:
            points = pages_read * settings.POINTS_CONFIG['PAGE_READ']
            progress.child.total_points += points
            progress.child.save(update_fields=['total_points'])
            progress.points_earned += points
            ProgressService._update_daily_activity(
                progress.child, pages_read=pages_read, time_spent=time_spent, points=points
            )
        
        progress.save()
        
        # Update streak
        from apps.gamification.services.streaks import StreakService
        StreakService.update_streak(progress.child)
        
        return progress
    
    @staticmethod
    @transaction.atomic
    def complete_story(progress, time_spent: int = 0) -> dict:
        """Mark story as completed."""
        remaining_pages = progress.story.page_count - progress.pages_completed
        page_points = remaining_pages * settings.POINTS_CONFIG['PAGE_READ']
        completion_points = settings.POINTS_CONFIG['STORY_COMPLETED_BASE'] * progress.story.level
        total_points = page_points + completion_points
        
        progress.status = Progress.Status.COMPLETED
        progress.current_page = progress.story.page_count
        progress.pages_completed = progress.story.page_count
        progress.time_spent_seconds += time_spent
        progress.completed_at = timezone.now()
        progress.points_earned += total_points
        progress.save()
        
        progress.child.total_points += total_points
        progress.child.save(update_fields=['total_points'])
        
        ProgressService._update_daily_activity(
            progress.child, stories_completed=1, pages_read=remaining_pages,
            time_spent=time_spent, points=total_points
        )
        
        # Update streak and check badges
        from apps.gamification.services.streaks import StreakService
        from apps.gamification.services.badges import BadgeService
        from apps.gamification.services.levels import LevelService
        
        StreakService.update_streak(progress.child)
        new_badges = BadgeService.check_and_award_badges(progress.child)
        level_up = LevelService.check_level_up(progress.child)
        
        return {
            'progress': progress,
            'points_awarded': total_points,
            'new_badges': new_badges,
            'level_up': level_up,
        }
    
    @staticmethod
    def _update_daily_activity(child, **kwargs):
        """Update daily activity record."""
        today = timezone.now().date()
        activity, _ = DailyActivity.objects.get_or_create(child=child, date=today)
        
        for field, value in kwargs.items():
            if hasattr(activity, field):
                setattr(activity, field, getattr(activity, field) + value)
        
        activity.save()
```

### apps/progress/views.py
```python
"""Progress views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from apps.stories.models import Story
from .models import Progress
from .services import ProgressService


class ProgressListView(APIView):
    """List progress records for a child."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_filter = request.query_params.get('status')
        queryset = Progress.objects.filter(child=child).select_related('story')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        data = [{
            'id': p.id,
            'story_id': p.story_id,
            'story_title': p.story.title,
            'status': p.status,
            'current_page': p.current_page,
            'total_pages': p.story.page_count,
            'last_read_at': p.last_read_at,
        } for p in queryset]
        
        return Response({'data': data})


class ProgressActionView(APIView):
    """Handle progress actions."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        action = request.data.get('action')
        story_id = request.data.get('story_id')
        
        if action == 'start':
            try:
                story = Story.objects.get(pk=story_id)
            except Story.DoesNotExist:
                return Response({'detail': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)
            
            progress = ProgressService.start_story(child, story)
            return Response({'data': {'id': progress.id, 'status': progress.status}})
        
        elif action == 'update':
            try:
                progress = Progress.objects.get(child=child, story_id=story_id)
            except Progress.DoesNotExist:
                return Response({'detail': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
            
            progress = ProgressService.update_progress(
                progress,
                request.data.get('current_page', 0),
                request.data.get('time_spent_seconds', 0)
            )
            return Response({'data': {'id': progress.id, 'current_page': progress.current_page}})
        
        elif action == 'complete':
            try:
                progress = Progress.objects.get(child=child, story_id=story_id)
            except Progress.DoesNotExist:
                return Response({'detail': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
            
            result = ProgressService.complete_story(
                progress, request.data.get('time_spent_seconds', 0)
            )
            return Response({
                'data': {'id': result['progress'].id, 'status': 'COMPLETED'},
                'meta': {
                    'points_awarded': result['points_awarded'],
                    'new_badges': [b.badge.name for b in result['new_badges']],
                    'level_up': result['level_up'],
                }
            })
        
        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
```

### apps/progress/urls.py
```python
"""Progress URL configuration."""
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressListView.as_view(), name='list'),
    path('action/', views.ProgressActionView.as_view(), name='action'),
]
```

---

## 3. Gamification System

### apps/gamification/models.py
```python
"""Gamification models."""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Badge(TimeStampedModel):
    """Achievement badges."""
    
    class CriteriaType(models.TextChoices):
        STORIES_COMPLETED = 'STORIES_COMPLETED', 'Stories Completed'
        STREAK_DAYS = 'STREAK_DAYS', 'Streak Days'
        POINTS_EARNED = 'POINTS_EARNED', 'Points Earned'
        TIME_SPENT_MINUTES = 'TIME_SPENT_MINUTES', 'Time Spent'
        VOICE_RECORDINGS = 'VOICE_RECORDINGS', 'Voice Recordings'
        LETTERS_MASTERED = 'LETTERS_MASTERED', 'Letters Mastered'
        WORDS_MASTERED = 'WORDS_MASTERED', 'Words Mastered'
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    criteria_type = models.CharField(max_length=30, choices=CriteriaType.choices)
    criteria_value = models.IntegerField()
    display_order = models.IntegerField(default=0)
    points_bonus = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'badges'
        ordering = ['display_order']
    
    def __str__(self):
        return self.name


class ChildBadge(TimeStampedModel):
    """Junction table for badges earned by children."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='child_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'child_badges'
        unique_together = ['child', 'badge']
    
    def __str__(self):
        return f"{self.child.name} - {self.badge.name}"


class Streak(TimeStampedModel):
    """Streak tracking for daily activity."""
    
    child = models.OneToOneField(Child, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'streaks'
    
    def __str__(self):
        return f"{self.child.name} - {self.current_streak} days"


class VoiceRecording(TimeStampedModel):
    """Voice recordings made by children."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='voice_recordings')
    story = models.ForeignKey('stories.Story', on_delete=models.SET_NULL, null=True, blank=True)
    page_number = models.IntegerField(null=True, blank=True)
    audio_url = models.URLField()
    duration_ms = models.IntegerField()
    transcription = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'voice_recordings'
        indexes = [models.Index(fields=['child', 'recorded_at'])]
    
    def __str__(self):
        return f"{self.child.name} - Recording {self.id}"
```

### apps/gamification/services/points.py
```python
"""Points service."""
from django.conf import settings


class PointsService:
    """Service for calculating points."""
    
    @staticmethod
    def calculate_story_completion_points(level: int) -> int:
        """Calculate points for story completion."""
        return settings.POINTS_CONFIG['STORY_COMPLETED_BASE'] * level
    
    @staticmethod
    def calculate_page_points(pages: int) -> int:
        """Calculate points for pages read."""
        return pages * settings.POINTS_CONFIG['PAGE_READ']
    
    @staticmethod
    def calculate_recording_points() -> int:
        """Calculate points for voice recording."""
        return settings.POINTS_CONFIG['VOICE_RECORDING']
    
    @staticmethod
    def award_points(child, points: int, reason: str = None):
        """Award points to a child."""
        child.total_points += points
        child.save(update_fields=['total_points'])
        return child.total_points
```

### apps/gamification/services/streaks.py
```python
"""Streak service."""
from django.utils import timezone
from datetime import timedelta
from ..models import Streak


class StreakService:
    """Service for managing streaks."""
    
    @staticmethod
    def update_streak(child) -> Streak:
        """Update streak based on activity."""
        streak, created = Streak.objects.get_or_create(child=child)
        today = timezone.now().date()
        
        if created or streak.last_activity_date is None:
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.last_activity_date = today
        elif streak.last_activity_date == today:
            # Already active today, no change
            pass
        elif streak.last_activity_date == today - timedelta(days=1):
            # Consecutive day
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_activity_date = today
        else:
            # Streak broken
            streak.current_streak = 1
            streak.last_activity_date = today
        
        streak.save()
        return streak
    
    @staticmethod
    def get_streak(child) -> dict:
        """Get streak information."""
        streak, _ = Streak.objects.get_or_create(child=child)
        today = timezone.now().date()
        
        is_active = (
            streak.last_activity_date == today or
            streak.last_activity_date == today - timedelta(days=1)
        )
        
        return {
            'current_streak': streak.current_streak,
            'longest_streak': streak.longest_streak,
            'last_activity_date': streak.last_activity_date,
            'is_active': is_active,
        }
```

### apps/gamification/services/badges.py
```python
"""Badge service."""
from django.db.models import Sum, Count
from ..models import Badge, ChildBadge


class BadgeService:
    """Service for managing badges."""
    
    @staticmethod
    def check_and_award_badges(child) -> list:
        """Check and award any earned badges."""
        earned_badge_ids = set(
            ChildBadge.objects.filter(child=child).values_list('badge_id', flat=True)
        )
        
        new_badges = []
        
        for badge in Badge.objects.exclude(id__in=earned_badge_ids):
            if BadgeService._check_criteria(child, badge):
                child_badge = ChildBadge.objects.create(child=child, badge=badge)
                new_badges.append(child_badge)
                
                # Award bonus points
                if badge.points_bonus > 0:
                    child.total_points += badge.points_bonus
                    child.save(update_fields=['total_points'])
        
        return new_badges
    
    @staticmethod
    def _check_criteria(child, badge) -> bool:
        """Check if child meets badge criteria."""
        from apps.progress.models import Progress
        
        if badge.criteria_type == Badge.CriteriaType.STORIES_COMPLETED:
            count = Progress.objects.filter(
                child=child, status=Progress.Status.COMPLETED
            ).count()
            return count >= badge.criteria_value
        
        elif badge.criteria_type == Badge.CriteriaType.STREAK_DAYS:
            from ..models import Streak
            streak = Streak.objects.filter(child=child).first()
            return streak and streak.current_streak >= badge.criteria_value
        
        elif badge.criteria_type == Badge.CriteriaType.POINTS_EARNED:
            return child.total_points >= badge.criteria_value
        
        elif badge.criteria_type == Badge.CriteriaType.VOICE_RECORDINGS:
            from ..models import VoiceRecording
            count = VoiceRecording.objects.filter(child=child).count()
            return count >= badge.criteria_value
        
        elif badge.criteria_type == Badge.CriteriaType.TIME_SPENT_MINUTES:
            total_seconds = Progress.objects.filter(child=child).aggregate(
                total=Sum('time_spent_seconds')
            )['total'] or 0
            return (total_seconds // 60) >= badge.criteria_value
        
        return False
    
    @staticmethod
    def get_badges_for_child(child) -> dict:
        """Get earned and available badges."""
        earned = ChildBadge.objects.filter(child=child).select_related('badge')
        all_badges = Badge.objects.all()
        earned_ids = set(cb.badge_id for cb in earned)
        
        return {
            'earned': [{
                'id': cb.badge.id,
                'name': cb.badge.name,
                'description': cb.badge.description,
                'icon': cb.badge.icon,
                'earned_at': cb.earned_at,
            } for cb in earned],
            'available': [{
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'icon': b.icon,
                'criteria_type': b.criteria_type,
                'criteria_value': b.criteria_value,
            } for b in all_badges if b.id not in earned_ids],
        }
```

### apps/gamification/services/levels.py
```python
"""Level service."""
from django.conf import settings


class LevelService:
    """Service for managing levels."""
    
    @staticmethod
    def calculate_level(total_points: int) -> int:
        """Calculate level based on total points."""
        thresholds = settings.LEVEL_THRESHOLDS
        level = 1
        
        for lvl, threshold in sorted(thresholds.items()):
            if total_points >= threshold:
                level = lvl
            else:
                break
        
        return level
    
    @staticmethod
    def check_level_up(child) -> dict:
        """Check if child leveled up."""
        current_level = child.level
        new_level = LevelService.calculate_level(child.total_points)
        
        if new_level > current_level:
            child.level = new_level
            child.save(update_fields=['level'])
            return {
                'leveled_up': True,
                'old_level': current_level,
                'new_level': new_level,
            }
        
        return {'leveled_up': False}
    
    @staticmethod
    def get_level_progress(child) -> dict:
        """Get level progress information."""
        thresholds = settings.LEVEL_THRESHOLDS
        current_threshold = thresholds.get(child.level, 0)
        next_threshold = thresholds.get(child.level + 1)
        
        if next_threshold:
            points_in_level = child.total_points - current_threshold
            points_needed = next_threshold - current_threshold
            progress_percent = int((points_in_level / points_needed) * 100)
        else:
            points_in_level = child.total_points - current_threshold
            points_needed = None
            progress_percent = 100
        
        return {
            'current_level': child.level,
            'total_points': child.total_points,
            'points_in_level': points_in_level,
            'points_to_next': points_needed,
            'progress_percent': progress_percent,
        }
```

### apps/gamification/views.py
```python
"""Gamification views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from .services.badges import BadgeService
from .services.streaks import StreakService
from .services.levels import LevelService
from .models import VoiceRecording


class BadgeListView(APIView):
    """Get badges for a child."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        badges = BadgeService.get_badges_for_child(child)
        return Response({'data': badges})


class StreakView(APIView):
    """Get streak for a child."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        streak = StreakService.get_streak(child)
        return Response({'data': streak})


class LevelView(APIView):
    """Get level progress for a child."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        level_info = LevelService.get_level_progress(child)
        return Response({'data': level_info})


class RecordingListView(APIView):
    """List and create voice recordings."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        recordings = VoiceRecording.objects.filter(child=child).order_by('-recorded_at')[:20]
        
        data = [{
            'id': r.id,
            'story_id': r.story_id,
            'page_number': r.page_number,
            'audio_url': r.audio_url,
            'duration_ms': r.duration_ms,
            'recorded_at': r.recorded_at,
        } for r in recordings]
        
        return Response({'data': data})
    
    def post(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        
        recording = VoiceRecording.objects.create(
            child=child,
            story_id=request.data.get('story_id'),
            page_number=request.data.get('page_number'),
            audio_url=request.data.get('audio_url'),
            duration_ms=request.data.get('duration_ms', 0),
        )
        
        # Award points
        from django.conf import settings
        points = settings.POINTS_CONFIG['VOICE_RECORDING']
        child.total_points += points
        child.save(update_fields=['total_points'])
        
        return Response({
            'data': {'id': recording.id},
            'meta': {'points_awarded': points}
        }, status=status.HTTP_201_CREATED)
```

### apps/gamification/urls.py
```python
"""Gamification URL configuration."""
from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('badges/', views.BadgeListView.as_view(), name='badges'),
    path('streak/', views.StreakView.as_view(), name='streak'),
    path('level/', views.LevelView.as_view(), name='level'),
    path('recordings/', views.RecordingListView.as_view(), name='recordings'),
]
```

---

## 4. Speech Services (Bhashini)

### apps/speech/views.py
```python
"""Speech API views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from external.bhashini.client import BhashiniClient


class TextToSpeechView(APIView):
    """Generate text-to-speech audio."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'speech'
    
    def post(self, request):
        text = request.data.get('text')
        language = request.data.get('language')
        
        if not text or not language:
            return Response(
                {'detail': 'text and language are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = BhashiniClient()
            result = client.text_to_speech(text, language)
            
            return Response({
                'data': {
                    'audio_content': result.get('audio_content'),
                    'audio_url': result.get('audio_url'),
                }
            })
        except Exception as e:
            return Response(
                {'detail': f'TTS service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class SpeechToTextView(APIView):
    """Transcribe speech to text."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'speech'
    
    def post(self, request):
        audio = request.data.get('audio')  # Base64 encoded
        language = request.data.get('language')
        
        if not audio or not language:
            return Response(
                {'detail': 'audio and language are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = BhashiniClient()
            result = client.speech_to_text(audio, language)
            
            return Response({
                'data': {
                    'transcription': result.get('transcription'),
                    'confidence': result.get('confidence'),
                }
            })
        except Exception as e:
            return Response(
                {'detail': f'STT service error: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
```

### apps/speech/urls.py
```python
"""Speech URL configuration."""
from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    path('tts/', views.TextToSpeechView.as_view(), name='tts'),
    path('stt/', views.SpeechToTextView.as_view(), name='stt'),
]
```

---

## 5. External API Clients

### external/bhashini/client.py
```python
"""Bhashini API client."""
import requests
import base64
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class BhashiniClient:
    """Client for Bhashini speech services."""
    
    LANGUAGE_CODES = {
        'HINDI': 'hi',
        'TAMIL': 'ta',
        'GUJARATI': 'gu',
        'PUNJABI': 'pa',
        'TELUGU': 'te',
        'MALAYALAM': 'ml',
    }
    
    def __init__(self):
        self.user_id = settings.BHASHINI_USER_ID
        self.api_key = settings.BHASHINI_API_KEY
        self.auth_url = settings.BHASHINI_AUTH_URL
        self._pipeline_cache = {}
    
    def text_to_speech(self, text: str, language: str) -> dict:
        """Convert text to speech."""
        lang_code = self.LANGUAGE_CODES.get(language, language.lower())
        
        # Get TTS pipeline
        pipeline = self._get_pipeline('tts', lang_code)
        if not pipeline:
            raise Exception(f"No TTS pipeline available for {language}")
        
        # Make TTS request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': pipeline.get('authorizationKey', self.api_key),
        }
        
        payload = {
            'pipelineTasks': [{
                'taskType': 'tts',
                'config': {
                    'language': {'sourceLanguage': lang_code},
                    'gender': 'female',
                }
            }],
            'inputData': {
                'input': [{'source': text}]
            }
        }
        
        response = requests.post(
            pipeline.get('callbackUrl'),
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        audio_content = data.get('pipelineResponse', [{}])[0].get('audio', [{}])[0].get('audioContent')
        
        return {'audio_content': audio_content}
    
    def speech_to_text(self, audio_base64: str, language: str) -> dict:
        """Convert speech to text."""
        lang_code = self.LANGUAGE_CODES.get(language, language.lower())
        
        # Get ASR pipeline
        pipeline = self._get_pipeline('asr', lang_code)
        if not pipeline:
            raise Exception(f"No ASR pipeline available for {language}")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': pipeline.get('authorizationKey', self.api_key),
        }
        
        payload = {
            'pipelineTasks': [{
                'taskType': 'asr',
                'config': {
                    'language': {'sourceLanguage': lang_code},
                }
            }],
            'inputData': {
                'audio': [{'audioContent': audio_base64}]
            }
        }
        
        response = requests.post(
            pipeline.get('callbackUrl'),
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        result = data.get('pipelineResponse', [{}])[0].get('output', [{}])[0]
        
        return {
            'transcription': result.get('source', ''),
            'confidence': result.get('confidence', 0),
        }
    
    def _get_pipeline(self, task_type: str, language: str) -> dict:
        """Get pipeline configuration from Bhashini."""
        cache_key = f"bhashini_pipeline_{task_type}_{language}"
        
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        headers = {
            'Content-Type': 'application/json',
            'userID': self.user_id,
            'ulcaApiKey': self.api_key,
        }
        
        payload = {
            'pipelineTasks': [{
                'taskType': task_type,
                'config': {
                    'language': {'sourceLanguage': language}
                }
            }],
            'pipelineRequestConfig': {
                'pipelineId': '64392f96dabc3f7a0c2543cd'
            }
        }
        
        try:
            response = requests.post(
                self.auth_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            pipeline = {
                'callbackUrl': data.get('pipelineInferenceAPIEndPoint', {}).get('callbackUrl'),
                'authorizationKey': data.get('pipelineInferenceAPIEndPoint', {}).get(
                    'inferenceApiKey', {}
                ).get('value'),
            }
            
            cache.set(cache_key, pipeline, settings.CACHE_TIMEOUT_PIPELINE)
            return pipeline
            
        except Exception as e:
            logger.error(f"Failed to get Bhashini pipeline: {e}")
            return None
```

### external/storyweaver/client.py
```python
"""StoryWeaver API client."""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class StoryWeaverClient:
    """Client for StoryWeaver API."""
    
    LANGUAGE_MAP = {
        'HINDI': 'Hindi',
        'TAMIL': 'Tamil',
        'GUJARATI': 'Gujarati',
        'PUNJABI': 'Punjabi',
        'TELUGU': 'Telugu',
        'MALAYALAM': 'Malayalam',
    }
    
    def __init__(self):
        self.base_url = settings.STORYWEAVER_BASE_URL
    
    def get_stories(self, language: str, level: int = None, limit: int = 20) -> list:
        """Fetch stories from StoryWeaver."""
        sw_language = self.LANGUAGE_MAP.get(language, language)
        
        params = {
            'language': sw_language,
            'page': 1,
            'per_page': limit,
            'sort': 'Relevance',
        }
        
        if level:
            params['reading_level'] = str(level)
        
        try:
            response = requests.get(
                f"{self.base_url}/stories",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            stories = []
            
            for item in data.get('data', []):
                stories.append({
                    'storyweaver_id': str(item.get('id')),
                    'title': item.get('title'),
                    'language': language,
                    'level': self._map_reading_level(item.get('reading_level')),
                    'page_count': item.get('pages_count', 0),
                    'cover_image_url': item.get('cover_image', {}).get('url', ''),
                    'synopsis': item.get('synopsis'),
                    'author': ', '.join([a.get('name', '') for a in item.get('authors', [])]),
                    'categories': [c.get('name') for c in item.get('categories', [])],
                })
            
            return stories
            
        except Exception as e:
            logger.error(f"Failed to fetch stories: {e}")
            return []
    
    def get_story_detail(self, storyweaver_id: str) -> dict:
        """Get story detail with pages."""
        try:
            response = requests.get(
                f"{self.base_url}/stories/{storyweaver_id}",
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json().get('data', {})
            
            pages = []
            for page in data.get('pages', []):
                pages.append({
                    'page_number': page.get('position', 0),
                    'text_content': page.get('content', ''),
                    'image_url': page.get('cover_image', {}).get('url'),
                })
            
            return {
                'storyweaver_id': str(data.get('id')),
                'title': data.get('title'),
                'pages': pages,
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch story detail: {e}")
            return None
    
    def _map_reading_level(self, sw_level: str) -> int:
        """Map StoryWeaver reading level to 1-5 scale."""
        level_map = {
            '1': 1, '2': 2, '3': 3, '4': 4,
            'Level 1': 1, 'Level 2': 2, 'Level 3': 3, 'Level 4': 4,
        }
        return level_map.get(str(sw_level), 1)
```

---

## URL Configuration

### config/urls.py
```python
"""Main URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('apps.users.urls', namespace='auth')),
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/children/<uuid:child_id>/progress/', include('apps.progress.urls', namespace='progress')),
    path('api/v1/children/<uuid:child_id>/', include('apps.gamification.urls', namespace='gamification')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
```

---

## Next Steps

Continue to **Part 3** for the complete **Curriculum Module**:
- Script/Alphabet Models and APIs
- Vocabulary with Spaced Repetition
- Grammar Rules and Exercises
- Games Framework
- Assessments and Certificates
- Seed Scripts
