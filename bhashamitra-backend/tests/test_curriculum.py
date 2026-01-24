"""Tests for curriculum endpoints (alphabet, vocabulary)."""
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAlphabet:
    """Test alphabet/script endpoints."""

    def test_list_scripts(self, auth_client, script, child):
        """Test listing scripts."""
        url = f'/api/v1/curriculum/children/{child.id}/alphabet/scripts/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_script_detail(self, auth_client, script, child):
        """Test getting script details."""
        url = f'/api/v1/curriculum/children/{child.id}/alphabet/scripts/{script.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('data', {})
        assert data.get('name') == script.name

    def test_list_letters(self, auth_client, letter, child):
        """Test listing letters."""
        url = f'/api/v1/curriculum/children/{child.id}/alphabet/letters/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_letter_detail(self, auth_client, letter, child):
        """Test getting letter details."""
        url = f'/api/v1/curriculum/children/{child.id}/alphabet/letters/{letter.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('data', {})
        assert data.get('character') == letter.character


@pytest.mark.django_db
class TestVocabulary:
    """Test vocabulary endpoints."""

    def test_list_themes(self, auth_client, vocabulary_theme, child):
        """Test listing vocabulary themes."""
        url = f'/api/v1/curriculum/children/{child.id}/vocabulary/themes/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_theme_detail(self, auth_client, vocabulary_theme, child):
        """Test getting theme details."""
        url = f'/api/v1/curriculum/children/{child.id}/vocabulary/themes/{vocabulary_theme.id}/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('data', {})
        assert data.get('name') == vocabulary_theme.name

    def test_list_theme_words(self, auth_client, vocabulary_word, child):
        """Test listing words in a theme."""
        url = f'/api/v1/curriculum/children/{child.id}/vocabulary/themes/{vocabulary_word.theme.id}/words/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_due_flashcards(self, auth_client, child):
        """Test getting due flashcards."""
        url = f'/api/v1/curriculum/children/{child.id}/vocabulary/flashcards/due/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGamification:
    """Test gamification endpoints."""

    def test_get_badges(self, auth_client, child, badge):
        """Test getting child's badges."""
        url = f'/api/v1/children/{child.id}/stats/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_streak(self, auth_client, child):
        """Test getting child's streak via stats."""
        url = f'/api/v1/children/{child.id}/stats/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_level(self, auth_client, child):
        """Test getting child's level info via stats."""
        url = f'/api/v1/children/{child.id}/stats/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
