"""
Test suite for Parent Dashboard APIs.

This file demonstrates the API endpoints and can be used for testing.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from apps.users.models import User
from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.gamification.models import Streak, ChildBadge, Badge
from apps.curriculum.models.progress import LevelProgress, LessonProgress
from apps.curriculum.models.vocabulary import WordProgress, VocabularyWord, VocabularyTheme


class ParentDashboardAPITest(TestCase):
    """Test Parent Dashboard API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create parent user
        self.parent = User.objects.create_user(
            username='parent@test.com',
            email='parent@test.com',
            password='testpass123',
            name='Test Parent'
        )

        # Create child
        self.child = Child.objects.create(
            user=self.parent,
            name='Test Child',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 5),
            language='HINDI',
            level=2,
            total_points=150
        )

        # Create streak
        self.streak = Streak.objects.create(
            child=self.child,
            current_streak=7,
            longest_streak=10
        )

        # Create daily progress
        today = timezone.now().date()
        for i in range(7):
            date = today - timedelta(days=i)
            DailyProgress.objects.create(
                child=self.child,
                date=date,
                time_spent_minutes=15 + (i * 2),
                lessons_completed=2,
                exercises_completed=3,
                games_played=1,
                points_earned=20
            )

        # Create activity logs
        ActivityLog.objects.create(
            child=self.child,
            activity_type='LESSON_COMPLETED',
            description='Completed Hindi Alphabet lesson',
            points_earned=10
        )

        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.parent)

    def test_parent_dashboard(self):
        """Test GET /api/v1/parent/dashboard/"""
        url = reverse('parent_engagement:dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('children', response.data)
        self.assertEqual(response.data['total_children'], 1)

        child_data = response.data['children'][0]
        self.assertEqual(child_data['name'], 'Test Child')
        self.assertEqual(child_data['level'], 2)
        self.assertEqual(child_data['total_points'], 150)
        self.assertEqual(child_data['streak_count'], 7)
        self.assertGreater(child_data['xp_this_week'], 0)

    def test_child_detailed_progress(self):
        """Test GET /api/v1/parent/children/{child_id}/progress/"""
        url = reverse('parent_engagement:child-detailed-progress', kwargs={'child_id': self.child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('curriculum_progress', response.data)
        self.assertIn('vocabulary_stats', response.data)
        self.assertIn('time_spent', response.data)

        curriculum = response.data['curriculum_progress']
        self.assertEqual(curriculum['current_level'], 2)

    def test_child_activity_feed(self):
        """Test GET /api/v1/parent/children/{child_id}/activity/"""
        url = reverse('parent_engagement:child-activity', kwargs={'child_id': self.child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

        activity = response.data['results'][0]
        self.assertIn('activity_type', activity)
        self.assertIn('description', activity)

    def test_child_stats_weekly(self):
        """Test GET /api/v1/parent/children/{child_id}/stats/?period=week"""
        url = reverse('parent_engagement:child-stats', kwargs={'child_id': self.child.id})
        response = self.client.get(url, {'period': 'week'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('days_active', response.data)
        self.assertIn('lessons_completed', response.data)
        self.assertIn('total_time_minutes', response.data)

        self.assertEqual(response.data['period'], 'This week')
        self.assertGreater(response.data['days_active'], 0)

    def test_child_stats_monthly(self):
        """Test GET /api/v1/parent/children/{child_id}/stats/?period=month"""
        url = reverse('parent_engagement:child-stats', kwargs={'child_id': self.child.id})
        response = self.client.get(url, {'period': 'month'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['period'], 'Last 30 days')

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access endpoints."""
        self.client.force_authenticate(user=None)

        url = reverse('parent_engagement:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_parent_access(self):
        """Test that parents can only see their own children."""
        # Create another parent
        other_parent = User.objects.create_user(
            username='other@test.com',
            email='other@test.com',
            password='testpass123',
            name='Other Parent'
        )
        self.client.force_authenticate(user=other_parent)

        # Try to access first parent's child
        url = reverse('parent_engagement:child-detailed-progress', kwargs={'child_id': self.child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ParentDashboardIntegrationTest(TestCase):
    """Integration tests with full data."""

    def setUp(self):
        """Set up comprehensive test data."""
        self.parent = User.objects.create_user(
            username='parent2@test.com',
            email='parent2@test.com',
            password='testpass123',
            name='Test Parent'
        )

        self.child = Child.objects.create(
            user=self.parent,
            name='Test Child',
            date_of_birth=timezone.now().date() - timedelta(days=365 * 6),
            language='HINDI',
            level=3,
            total_points=500
        )

        # Create vocabulary theme and words
        self.theme = VocabularyTheme.objects.create(
            language='HINDI',
            name='Colors',
            name_native='रंग',
            level=1,
            order=1
        )

        self.word = VocabularyWord.objects.create(
            theme=self.theme,
            word='लाल',
            romanization='laal',
            translation='red',
            order=1
        )

        # Create word progress
        WordProgress.objects.create(
            child=self.child,
            word=self.word,
            mastered=True,
            mastered_at=timezone.now()
        )

        # Create badge
        self.badge = Badge.objects.create(
            name='First Steps',
            description='Complete your first lesson',
            icon='star',
            criteria_type='STORIES_COMPLETED',
            criteria_value=1
        )

        ChildBadge.objects.create(
            child=self.child,
            badge=self.badge
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.parent)

    def test_full_dashboard_data(self):
        """Test dashboard with all data types."""
        url = reverse('parent_engagement:dashboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        child_data = response.data['children'][0]

        # Verify all fields present
        required_fields = [
            'id', 'name', 'avatar_url', 'level', 'total_points',
            'streak_count', 'xp_this_week', 'recent_activity_count'
        ]
        for field in required_fields:
            self.assertIn(field, child_data)

    def test_progress_with_vocabulary(self):
        """Test progress endpoint includes vocabulary stats."""
        url = reverse('parent_engagement:child-detailed-progress', kwargs={'child_id': self.child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vocab_stats = response.data['vocabulary_stats']
        self.assertEqual(vocab_stats['words_mastered'], 1)
        self.assertGreaterEqual(vocab_stats['words_in_progress'], 0)

    def test_progress_with_badges(self):
        """Test progress endpoint includes badge count."""
        url = reverse('parent_engagement:child-detailed-progress', kwargs={'child_id': self.child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['badges_earned'], 1)
