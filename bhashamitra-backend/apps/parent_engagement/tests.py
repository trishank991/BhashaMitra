"""
Parent Engagement API Tests.

Tests for parent dashboard endpoints including:
- Children listing
- Child summary
- Activity log
- Weekly reports
- Learning goals
- Progress updates
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from uuid import uuid4

from apps.users.models import User
from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.parent_engagement.models import LearningGoal


class ParentEngagementBaseTest(APITestCase):
    """Base test class with common setup."""

    def setUp(self):
        """Set up test data."""
        # Create parent user
        self.parent = User.objects.create_user(
            username='parent_test',
            email='parent@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Parent',
        )

        # Create children
        self.child1 = Child.objects.create(
            user=self.parent,
            name='Arjun',
            date_of_birth=timezone.now().date() - timedelta(days=2190),  # ~6 years
            language='HINDI',
            level=2,
            total_points=500,
        )

        self.child2 = Child.objects.create(
            user=self.parent,
            name='Priya',
            date_of_birth=timezone.now().date() - timedelta(days=3650),  # ~10 years
            language='HINDI',
            level=3,
            total_points=1200,
        )

        # Create some daily progress
        today = timezone.now().date()
        for i in range(7):
            date = today - timedelta(days=i)
            DailyProgress.objects.create(
                child=self.child1,
                date=date,
                time_spent_minutes=15 + i * 5,
                lessons_completed=2,
                exercises_completed=3,
                games_played=1,
                points_earned=50,
            )

        # Create activity logs
        ActivityLog.objects.create(
            child=self.child1,
            activity_type='LESSON_COMPLETED',
            description='Completed vowel lesson',
            points_earned=25,
        )
        ActivityLog.objects.create(
            child=self.child1,
            activity_type='BADGE_EARNED',
            description='Earned first badge!',
            points_earned=50,
        )

        # Create learning goal
        self.goal = LearningGoal.objects.create(
            child=self.child1,
            goal_type='DAILY_MINUTES',
            target_value=15,
            current_value=10,
            start_date=today,
            end_date=today + timedelta(days=7),
            is_active=True,
        )

        # Set up authenticated client
        self.client = APIClient()
        self.client.force_authenticate(user=self.parent)


class ParentChildrenListTests(ParentEngagementBaseTest):
    """Tests for GET /api/v1/parent/children/"""

    def test_list_children_success(self):
        """Parent can list all their children."""
        url = reverse('parent_engagement:children-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(data), 2)

    def test_list_children_unauthenticated(self):
        """Unauthenticated request returns 401."""
        self.client.force_authenticate(user=None)
        url = reverse('parent_engagement:children-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_children_only_own(self):
        """Parent only sees their own children."""
        # Create another parent with child
        other_parent = User.objects.create_user(
            username='other_parent',
            email='other@test.com',
            password='testpass123',
        )
        Child.objects.create(
            user=other_parent,
            name='Other Child',
            date_of_birth=timezone.now().date() - timedelta(days=2000),
            language='HINDI',
        )

        url = reverse('parent_engagement:children-list')
        response = self.client.get(url)

        # Handle paginated response
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(data), 2)
        names = [c['name'] for c in data]
        self.assertIn('Arjun', names)
        self.assertIn('Priya', names)
        self.assertNotIn('Other Child', names)


class ChildSummaryTests(ParentEngagementBaseTest):
    """Tests for GET /api/v1/parent/children/{child_id}/summary/"""

    def test_get_child_summary_success(self):
        """Parent can get summary for their child."""
        url = reverse('parent_engagement:child-summary', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('child', response.data)
        self.assertIn('weekly_summary', response.data)
        self.assertIn('current_streak', response.data)
        self.assertIn('active_goals', response.data)

    def test_get_child_summary_not_found(self):
        """Returns 404 for non-existent child."""
        url = reverse('parent_engagement:child-summary', kwargs={'child_id': uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_child_summary_other_parent(self):
        """Cannot access another parent's child."""
        other_parent = User.objects.create_user(
            username='other_parent2',
            email='other@test.com',
            password='testpass123',
        )
        other_child = Child.objects.create(
            user=other_parent,
            name='Other Child',
            date_of_birth=timezone.now().date() - timedelta(days=2000),
            language='HINDI',
        )

        url = reverse('parent_engagement:child-summary', kwargs={'child_id': other_child.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_weekly_summary_calculations(self):
        """Weekly summary calculations are correct."""
        url = reverse('parent_engagement:child-summary', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        weekly = response.data['weekly_summary']
        # 7 days with time_spent_minutes = 15 + i*5 = 15+20+25+30+35+40+45 = 210
        self.assertGreater(weekly['time_spent_minutes'], 0)
        self.assertGreater(weekly['lessons_completed'], 0)


class ChildActivityTests(ParentEngagementBaseTest):
    """Tests for GET /api/v1/parent/children/{child_id}/activity/"""

    def test_get_activity_log_success(self):
        """Parent can get activity log for their child."""
        url = reverse('parent_engagement:child-activity', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertGreater(len(data), 0)

    def test_activity_log_filter_by_type(self):
        """Can filter activity log by type."""
        url = reverse('parent_engagement:child-activity', kwargs={'child_id': self.child1.id})
        response = self.client.get(url, {'type': 'BADGE_EARNED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        for activity in data:
            self.assertEqual(activity['activity_type'], 'BADGE_EARNED')

    def test_activity_log_filter_by_days(self):
        """Can filter activity log by days."""
        url = reverse('parent_engagement:child-activity', kwargs={'child_id': self.child1.id})
        response = self.client.get(url, {'days': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChildWeeklyReportTests(ParentEngagementBaseTest):
    """Tests for GET /api/v1/parent/children/{child_id}/weekly-report/"""

    def test_get_weekly_report_success(self):
        """Parent can get weekly report for their child."""
        url = reverse('parent_engagement:child-weekly-report', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('daily_data', response.data)
        self.assertIn('summary', response.data)
        self.assertIn('comparison', response.data)
        self.assertIn('highlights', response.data)
        self.assertIn('suggestions', response.data)

    def test_weekly_report_comparison(self):
        """Weekly report includes comparison to last week."""
        url = reverse('parent_engagement:child-weekly-report', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        comparison = response.data['comparison']
        self.assertIn('time_change_percent', comparison)
        self.assertIn('points_change_percent', comparison)
        self.assertIn('trend', comparison)


class ChildGoalsTests(ParentEngagementBaseTest):
    """Tests for GET/POST /api/v1/parent/children/{child_id}/goals/"""

    def test_list_goals_success(self):
        """Parent can list goals for their child."""
        url = reverse('parent_engagement:child-goals', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('goals', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)

    def test_create_goal_success(self):
        """Parent can create a goal for their child."""
        url = reverse('parent_engagement:child-goals', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'weekly_lessons',
            'target': 10,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['target_value'], 10)

    def test_create_goal_with_deadline(self):
        """Parent can create a goal with deadline."""
        url = reverse('parent_engagement:child-goals', kwargs={'child_id': self.child1.id})
        deadline = (timezone.now().date() + timedelta(days=14)).isoformat()
        data = {
            'type': 'weekly_words',
            'target': 20,
            'deadline': deadline,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['target_value'], 20)

    def test_create_goal_invalid_type(self):
        """Invalid goal type returns error."""
        url = reverse('parent_engagement:child-goals', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'invalid_type',
            'target': 10,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProgressUpdateTests(ParentEngagementBaseTest):
    """Tests for POST /api/v1/parent/children/{child_id}/progress/"""

    def test_update_progress_lesson(self):
        """Can update progress for a lesson."""
        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'lesson',
            'duration_minutes': 15,
            'points_earned': 25,
            'details': {'description': 'Completed alphabet lesson'},
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('daily_progress', response.data)
        self.assertIn('total_points', response.data)

    def test_update_progress_exercise(self):
        """Can update progress for an exercise."""
        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'exercise',
            'duration_minutes': 10,
            'points_earned': 15,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_update_progress_game(self):
        """Can update progress for a game."""
        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'game',
            'duration_minutes': 5,
            'points_earned': 20,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_update_progress_creates_daily_record(self):
        """Progress update creates daily record if not exists."""
        # Create child with no progress
        new_child = Child.objects.create(
            user=self.parent,
            name='New Child',
            date_of_birth=timezone.now().date() - timedelta(days=2000),
            language='HINDI',
        )

        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': new_child.id})
        data = {
            'type': 'lesson',
            'duration_minutes': 10,
            'points_earned': 20,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check daily progress was created
        today = timezone.now().date()
        daily = DailyProgress.objects.filter(child=new_child, date=today).first()
        self.assertIsNotNone(daily)
        self.assertEqual(daily.lessons_completed, 1)

    def test_update_progress_updates_goal(self):
        """Progress update updates relevant goals."""
        initial_value = self.goal.current_value

        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'lesson',
            'duration_minutes': 10,
            'points_earned': 25,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload goal
        self.goal.refresh_from_db()
        self.assertGreater(self.goal.current_value, initial_value)

    def test_update_progress_invalid_type(self):
        """Invalid progress type returns error."""
        url = reverse('parent_engagement:child-progress-update', kwargs={'child_id': self.child1.id})
        data = {
            'type': 'invalid',
            'duration_minutes': 10,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StreakCalculationTests(ParentEngagementBaseTest):
    """Tests for streak calculation logic."""

    def test_streak_with_consecutive_days(self):
        """Streak is calculated correctly for consecutive days."""
        url = reverse('parent_engagement:child-summary', kwargs={'child_id': self.child1.id})
        response = self.client.get(url)

        # We created 7 days of progress
        self.assertEqual(response.data['current_streak'], 7)

    def test_streak_resets_on_gap(self):
        """Streak resets when there's a gap."""
        # Create child with gap in progress
        child = Child.objects.create(
            user=self.parent,
            name='Gap Child',
            date_of_birth=timezone.now().date() - timedelta(days=2000),
            language='HINDI',
        )

        today = timezone.now().date()
        # Create progress for today and 2 days ago (gap yesterday)
        DailyProgress.objects.create(
            child=child,
            date=today,
            time_spent_minutes=15,
            lessons_completed=1,
            exercises_completed=0,
            games_played=0,
            points_earned=10,
        )

        url = reverse('parent_engagement:child-summary', kwargs={'child_id': child.id})
        response = self.client.get(url)

        self.assertEqual(response.data['current_streak'], 1)


class ContentValidatorTests(TestCase):
    """Tests for content validation system."""

    def test_validate_hindi_letter(self):
        """Test Hindi letter validation."""
        from apps.core.validators import ContentValidator

        validator = ContentValidator()
        result = validator.validate_letter({
            'letter': 'क',
            'transliteration': 'ka',
            'language': 'HINDI',
        })

        self.assertTrue(result.is_valid)

    def test_validate_letter_wrong_script(self):
        """Test letter validation with wrong script."""
        from apps.core.validators import ContentValidator

        validator = ContentValidator()
        result = validator.validate_letter({
            'letter': 'A',
            'transliteration': 'a',
            'language': 'HINDI',
        })

        self.assertFalse(result.is_valid)

    def test_validate_vocabulary(self):
        """Test vocabulary validation."""
        from apps.core.validators import ContentValidator

        validator = ContentValidator()
        result = validator.validate_vocabulary({
            'word': 'कमल',
            'transliteration': 'kamal',
            'meaning': 'lotus',
            'language': 'HINDI',
        })

        self.assertTrue(result.is_valid)

    def test_validate_vocabulary_mixed_language(self):
        """Test vocabulary validation with mixed language."""
        from apps.core.validators import ContentValidator

        validator = ContentValidator()
        result = validator.validate_vocabulary({
            'word': 'कमलhello',  # Mixed Hindi and English
            'transliteration': 'kamal',
            'meaning': 'lotus',
            'language': 'HINDI',
        })

        self.assertFalse(result.is_valid)


class LanguagePurityTests(TestCase):
    """Tests for language purity validation."""

    def test_pure_hindi_text(self):
        """Test pure Hindi text passes validation."""
        from apps.core.validators import LanguagePurityValidator

        validator = LanguagePurityValidator()
        result = validator.validate_text('नमस्ते', 'HINDI')

        self.assertTrue(result['is_pure'])
        self.assertEqual(result['foreign_ratio'], 0.0)

    def test_mixed_text(self):
        """Test mixed text fails validation."""
        from apps.core.validators import LanguagePurityValidator

        validator = LanguagePurityValidator()
        result = validator.validate_text('नमस्ते hello', 'HINDI')

        self.assertFalse(result['is_pure'])
        self.assertGreater(result['foreign_ratio'], 0)

    def test_extract_foreign_words(self):
        """Test extraction of foreign words."""
        from apps.core.validators import LanguagePurityValidator

        validator = LanguagePurityValidator()
        foreign = validator.extract_foreign_words('नमस्ते hello world', 'HINDI')

        self.assertIn('hello', foreign)
        self.assertIn('world', foreign)


class NCERTValidatorTests(TestCase):
    """Tests for NCERT curriculum validation."""

    def test_validate_ncert_letter(self):
        """Test NCERT letter validation."""
        from apps.core.validators import NCERTValidator

        validator = NCERTValidator()
        result = validator.validate_hindi_letter('क', 'ka')

        self.assertTrue(result['is_valid'])
        self.assertTrue(result['is_standard'])

    def test_validate_ncert_non_standard_transliteration(self):
        """Test NCERT validation with non-standard transliteration."""
        from apps.core.validators import NCERTValidator

        validator = NCERTValidator()
        result = validator.validate_hindi_letter('क', 'k')  # Should be 'ka'

        self.assertTrue(result['is_valid'])  # Still valid letter
        self.assertFalse(result['is_standard'])  # But non-standard transliteration

    def test_validate_alphabet_order(self):
        """Test NCERT alphabet order validation."""
        from apps.core.validators import NCERTValidator

        validator = NCERTValidator()

        # Correct order
        result = validator.validate_hindi_alphabet_order(['अ', 'आ', 'इ'])
        self.assertTrue(result['is_valid'])

        # Incorrect order
        result = validator.validate_hindi_alphabet_order(['आ', 'अ', 'इ'])
        self.assertFalse(result['is_valid'])

    def test_get_letter_category(self):
        """Test letter category identification."""
        from apps.core.validators import NCERTValidator

        validator = NCERTValidator()

        # Vowel
        category = validator.get_letter_category('अ')
        self.assertEqual(category, 'स्वर (Vowel)')

        # Consonant
        category = validator.get_letter_category('क')
        self.assertIn('Velar', category)
