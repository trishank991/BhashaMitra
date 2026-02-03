"""Tests for authentication endpoints."""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRegistration:
    """Test user registration endpoint."""

    def test_register_success(self, api_client):
        """Test successful user registration."""
        url = '/api/v1/auth/register/'
        data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'name': 'New User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        # Register returns session at top level (not nested under data)
        session = response.data.get('session', {})
        assert 'access_token' in session
        assert 'refresh_token' in session

    def test_register_duplicate_email(self, api_client, user):
        """Test registration with existing email fails."""
        url = '/api/v1/auth/register/'
        data = {
            'email': user.email,
            'password': 'SecurePass123!',
            'name': 'Another User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_email(self, api_client):
        """Test registration with invalid email fails."""
        url = '/api/v1/auth/register/'
        data = {
            'email': 'not-an-email',
            'password': 'SecurePass123!',
            'name': 'Test User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client):
        """Test registration with weak password fails."""
        url = '/api/v1/auth/register/'
        data = {
            'email': 'test@example.com',
            'password': '123',
            'name': 'Test User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    """Test user login endpoint."""

    def test_login_success(self, api_client, user):
        """Test successful login."""
        url = '/api/v1/auth/login/'
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        # API returns session.access_token/refresh_token
        session = response.data.get('data', {}).get('session', {})
        assert 'access_token' in session

    def test_login_wrong_password(self, api_client, user):
        """Test login with wrong password fails."""
        url = '/api/v1/auth/login/'
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user fails."""
        url = '/api/v1/auth/login/'
        data = {
            'email': 'nonexistent@example.com',
            'password': 'somepassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCurrentUser:
    """Test current user endpoint."""

    def test_get_current_user(self, auth_client, user):
        """Test getting current user info."""
        url = '/api/v1/auth/me/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # User data may be at data level or data.user level
        data = response.data.get('data', response.data)
        user_data = data.get('user', data) if isinstance(data, dict) else data
        assert user_data.get('email') == user.email
        assert user_data.get('name') == user.name

    def test_get_current_user_unauthenticated(self, api_client):
        """Test getting current user without auth fails."""
        url = '/api/v1/auth/me/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
