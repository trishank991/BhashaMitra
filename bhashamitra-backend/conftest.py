"""Pytest configuration and fixtures for BhashaMitra backend tests."""
import pytest
from django.test import override_settings
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Return an API client for making requests."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    from apps.users.models import User
    return User.objects.create_user(
        username='testparent@example.com',
        email='testparent@example.com',
        password='testpass123',
        name='Test Parent'
    )


@pytest.fixture
def auth_client(api_client, user):
    """Return an authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def child(db, user):
    """Create and return a test child."""
    from apps.children.models import Child
    from datetime import date
    return Child.objects.create(
        user=user,
        name='Test Child',
        date_of_birth=date(2018, 6, 15),
        language='HINDI',
        level=1
    )


@pytest.fixture
def story(db):
    """Create and return a test story."""
    from apps.stories.models import Story
    return Story.objects.create(
        storyweaver_id='test-story-123',
        title='Test Hindi Story',
        language='HINDI',
        level=1,
        page_count=5,
        cover_image_url='https://example.com/cover.jpg',
        synopsis='A test story for testing purposes.',
        author='Test Author'
    )


@pytest.fixture
def story_with_pages(story):
    """Create a story with pages."""
    from apps.stories.models import StoryPage
    for i in range(1, 6):
        StoryPage.objects.create(
            story=story,
            page_number=i,
            text_content=f'यह पेज {i} है।',
            image_url=f'https://example.com/page{i}.jpg'
        )
    return story


@pytest.fixture
def badge(db):
    """Create and return a test badge."""
    from apps.gamification.models import Badge
    return Badge.objects.create(
        name='First Story',
        description='Complete your first story',
        icon='https://example.com/badge.png',
        criteria_type='STORIES_COMPLETED',
        criteria_value=1,
        display_order=1,
        points_bonus=50
    )


@pytest.fixture
def script(db):
    """Create and return a test script (Devanagari for Hindi)."""
    from apps.curriculum.models import Script
    return Script.objects.create(
        language='HINDI',
        name='Devanagari',
        name_native='देवनागरी',
        description='The script used for Hindi and other Indian languages',
        total_letters=46
    )


@pytest.fixture
def alphabet_category(script):
    """Create and return an alphabet category."""
    from apps.curriculum.models import AlphabetCategory
    return AlphabetCategory.objects.create(
        script=script,
        name='Vowels',
        name_native='स्वर',
        category_type='VOWEL',
        description='Hindi vowels',
        order=1
    )


@pytest.fixture
def letter(alphabet_category):
    """Create and return a test letter."""
    from apps.curriculum.models import Letter
    return Letter.objects.create(
        category=alphabet_category,
        character='अ',
        romanization='a',
        ipa='ə',
        pronunciation_guide='Like "a" in "about"',
        example_word='अनार',
        example_word_romanization='anaar',
        example_word_translation='pomegranate',
        order=1
    )


@pytest.fixture
def vocabulary_theme(db):
    """Create and return a vocabulary theme."""
    from apps.curriculum.models import VocabularyTheme
    return VocabularyTheme.objects.create(
        language='HINDI',
        name='Family',
        name_native='परिवार',
        description='Family members vocabulary',
        icon='https://example.com/family.png',
        level=1,
        order=1
    )


@pytest.fixture
def vocabulary_word(vocabulary_theme):
    """Create and return a vocabulary word."""
    from apps.curriculum.models import VocabularyWord
    return VocabularyWord.objects.create(
        theme=vocabulary_theme,
        word='माँ',
        romanization='maa',
        translation='mother',
        part_of_speech='NOUN',
        gender='FEMININE',
        example_sentence='मेरी माँ सुंदर है।',
        difficulty=1,
        order=1
    )
