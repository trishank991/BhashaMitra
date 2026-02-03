"""Tests for stories and progress endpoints."""
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestStoryList:
    """Test story listing endpoint."""

    def test_list_stories(self, auth_client, story):
        """Test listing stories."""
        url = '/api/v1/stories/?language=HINDI'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_stories_filter_by_language(self, auth_client, story):
        """Test filtering stories by language."""
        url = '/api/v1/stories/?language=HINDI'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_stories_filter_by_level(self, auth_client, story):
        """Test filtering stories by level."""
        url = '/api/v1/stories/?language=HINDI&level=1'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_stories_unauthenticated(self, api_client, story):
        """Test listing stories without auth fails."""
        url = '/api/v1/stories/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestStoryDetail:
    """Test story detail endpoint."""

    def test_get_story_detail(self, auth_client, story_with_pages):
        """Test getting story details with pages."""
        url = f'/api/v1/stories/{story_with_pages.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('data', {})
        assert data.get('title') == story_with_pages.title
        assert 'pages' in data

    def test_get_story_nonexistent(self, auth_client):
        """Test getting non-existent story fails."""
        import uuid
        url = f'/api/v1/stories/{uuid.uuid4()}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestProgress:
    """Test reading progress endpoints."""

    def test_list_progress_empty(self, auth_client, child):
        """Test listing progress when none exists."""
        url = f'/api/v1/children/{child.id}/progress/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('data', []) == []

    def test_start_story(self, auth_client, child, story):
        """Test starting a story."""
        url = f'/api/v1/children/{child.id}/progress/action/'
        data = {
            'action': 'start',
            'story_id': str(story.id)
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        result = response.data.get('data', {})
        assert result.get('status') == 'IN_PROGRESS'

    def test_update_progress(self, auth_client, child, story):
        """Test updating reading progress."""
        # First start the story
        url = f'/api/v1/children/{child.id}/progress/action/'
        auth_client.post(url, {'action': 'start', 'story_id': str(story.id)}, format='json')

        # Then update progress
        data = {
            'action': 'update',
            'story_id': str(story.id),
            'current_page': 3,
            'time_spent_seconds': 120
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('data', {}).get('current_page') == 3

    def test_complete_story(self, auth_client, child, story, badge):
        """Test completing a story awards points and checks badges."""
        # First start the story
        url = f'/api/v1/children/{child.id}/progress/action/'
        auth_client.post(url, {'action': 'start', 'story_id': str(story.id)}, format='json')

        # Complete the story
        data = {
            'action': 'complete',
            'story_id': str(story.id),
            'time_spent_seconds': 300
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        result = response.data
        assert result.get('data', {}).get('status') == 'COMPLETED'
        assert 'meta' in result
        assert 'points_awarded' in result.get('meta', {})
