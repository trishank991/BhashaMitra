"""Tests for children management endpoints."""
import pytest
from rest_framework import status
from datetime import date


@pytest.mark.django_db
class TestChildrenList:
    """Test children list and create endpoints."""

    def test_list_children_empty(self, auth_client):
        """Test listing children when none exist."""
        url = '/api/v1/children/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Handle paginated response (with 'results' key) or direct list
        if isinstance(response.data, dict):
            data = response.data.get('results', response.data.get('data', []))
        else:
            data = response.data
        assert data == [] or len(data) == 0

    def test_list_children_with_child(self, auth_client, child):
        """Test listing children when one exists."""
        url = '/api/v1/children/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Handle paginated response (with 'results' key) or direct list
        if isinstance(response.data, dict):
            data = response.data.get('results', response.data.get('data', []))
        else:
            data = response.data
        assert len(data) == 1
        assert data[0]['name'] == child.name

    def test_create_child_success(self, auth_client):
        """Test creating a child successfully."""
        url = '/api/v1/children/'
        data = {
            'name': 'New Child',
            'date_of_birth': '2019-03-15',
            'language': 'HINDI'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        # Response may be wrapped in 'data' or returned directly
        result = response.data.get('data', response.data) if isinstance(response.data, dict) else response.data
        assert result.get('name') == 'New Child'
        assert result.get('language') == 'HINDI'

    def test_create_child_missing_name(self, auth_client):
        """Test creating a child without name fails."""
        url = '/api/v1/children/'
        data = {
            'date_of_birth': '2019-03-15',
            'language': 'HINDI'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_child_unauthenticated(self, api_client):
        """Test creating a child without auth fails."""
        url = '/api/v1/children/'
        data = {
            'name': 'New Child',
            'date_of_birth': '2019-03-15',
            'language': 'HINDI'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestChildDetail:
    """Test child detail, update, delete endpoints."""

    def test_get_child_detail(self, auth_client, child):
        """Test getting child details."""
        url = f'/api/v1/children/{child.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Response may be wrapped in 'data' or returned directly
        data = response.data.get('data', response.data) if isinstance(response.data, dict) else response.data
        assert data.get('name') == child.name
        assert data.get('language') == child.language

    def test_get_child_other_user(self, api_client, child):
        """Test getting another user's child fails."""
        from apps.users.models import User
        from rest_framework_simplejwt.tokens import RefreshToken

        other_user = User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='testpass123',
            name='Other Parent'
        )
        refresh = RefreshToken.for_user(other_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = f'/api/v1/children/{child.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_child(self, auth_client, child):
        """Test updating a child."""
        url = f'/api/v1/children/{child.id}/'
        data = {'name': 'Updated Name'}
        response = auth_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Response may be wrapped in 'data' or returned directly
        result = response.data.get('data', response.data) if isinstance(response.data, dict) else response.data
        assert result.get('name') == 'Updated Name'

    def test_delete_child(self, auth_client, child):
        """Test soft deleting a child."""
        url = f'/api/v1/children/{child.id}/'
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify child is soft deleted
        from apps.children.models import Child
        child.refresh_from_db()
        assert child.deleted_at is not None


@pytest.mark.django_db
class TestChildStats:
    """Test child statistics endpoint."""

    def test_get_child_stats(self, auth_client, child):
        """Test getting child statistics."""
        url = f'/api/v1/children/{child.id}/stats/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Stats response is wrapped in 'data'
        data = response.data.get('data', {})
        # API uses points_earned and stories_completed
        assert 'points_earned' in data
        assert 'stories_completed' in data
