"""Story services - StoryWeaver integration."""
import logging
import requests
from django.conf import settings
from django.utils.text import slugify
from .models import Story, StoryPage

logger = logging.getLogger(__name__)


class StoryWeaverService:
    """Service for interacting with StoryWeaver API."""

    BASE_URL = 'https://storyweaver.org.in/api/v1'

    # Map our language codes to StoryWeaver language codes
    LANGUAGE_MAP = {
        'HINDI': 'Hindi',
        'TAMIL': 'Tamil',
        'GUJARATI': 'Gujarati',
        'PUNJABI': 'Punjabi',
        'TELUGU': 'Telugu',
        'MALAYALAM': 'Malayalam',
        'MARATHI': 'Marathi',
        'BENGALI': 'Bengali',
        'KANNADA': 'Kannada',
        'URDU': 'Urdu',
    }

    # Map reading levels to our 1-5 scale
    LEVEL_MAP = {
        '1': 1,  # Level 1 - Early reader
        '2': 2,  # Level 2 - Beginner
        '3': 3,  # Level 3 - Intermediate
        '4': 4,  # Level 4 - Advanced
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

    def search_stories(self, language='HINDI', level=1, query='', page=1, per_page=20):
        """Search stories from StoryWeaver."""
        try:
            sw_language = self.LANGUAGE_MAP.get(language, 'Hindi')

            params = {
                'language': sw_language,
                'reading_level': str(level),
                'page': page,
                'per_page': per_page,
            }

            if query:
                params['query'] = query

            response = self.session.get(
                f'{self.BASE_URL}/stories',
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            stories = data.get('data', [])

            return {
                'stories': [self._transform_story(s) for s in stories],
                'total': data.get('metadata', {}).get('totalCount', 0),
                'page': page,
                'per_page': per_page,
            }

        except requests.RequestException as e:
            logger.error(f"StoryWeaver API error: {e}")
            return {'stories': [], 'total': 0, 'page': page, 'per_page': per_page}

    def get_story(self, external_id):
        """Get a single story from StoryWeaver."""
        try:
            response = self.session.get(
                f'{self.BASE_URL}/stories/{external_id}',
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return data.get('data')

        except requests.RequestException as e:
            logger.error(f"StoryWeaver API error: {e}")
            return None

    def sync_story(self, external_id):
        """Sync a story from StoryWeaver to local database."""
        # Check if already synced
        existing = Story.objects.filter(external_id=str(external_id)).first()
        if existing:
            return existing

        # Fetch from API
        story_data = self.get_story(external_id)
        if not story_data:
            return None

        # Create story
        story = Story.objects.create(
            external_id=str(external_id),
            source=Story.Source.STORYWEAVER,
            title=story_data.get('name', ''),
            slug=slugify(story_data.get('name', '')),
            synopsis=story_data.get('synopsis', ''),
            language=self._reverse_language_map(story_data.get('language', '')),
            level=self.LEVEL_MAP.get(story_data.get('readingLevel', '1'), 1),
            reading_level=story_data.get('readingLevel', ''),
            page_count=len(story_data.get('pages', [])),
            cover_image_url=story_data.get('coverImage', {}).get('url', ''),
            thumbnail_url=story_data.get('thumbnail', ''),
            categories=story_data.get('categories', []),
            tags=story_data.get('tags', []),
            authors=[a.get('name', '') for a in story_data.get('authors', [])],
            illustrators=[i.get('name', '') for i in story_data.get('illustrators', [])],
            publisher=story_data.get('publisher', ''),
            copyright_info=story_data.get('copyright', ''),
        )

        # Create pages
        for idx, page_data in enumerate(story_data.get('pages', []), 1):
            StoryPage.objects.create(
                story=story,
                page_number=idx,
                text=page_data.get('content', ''),
                image_url=page_data.get('image', {}).get('url', ''),
            )

        return story

    def _transform_story(self, data):
        """Transform StoryWeaver story to our format."""
        return {
            'external_id': str(data.get('id', '')),
            'source': 'STORYWEAVER',
            'title': data.get('name', ''),
            'synopsis': data.get('synopsis', ''),
            'language': self._reverse_language_map(data.get('language', '')),
            'level': self.LEVEL_MAP.get(data.get('readingLevel', '1'), 1),
            'reading_level': data.get('readingLevel', ''),
            'cover_image_url': data.get('coverImage', {}).get('url', ''),
            'thumbnail_url': data.get('thumbnail', ''),
            'authors': [a.get('name', '') for a in data.get('authors', [])],
            'read_count': data.get('reads', 0),
            'like_count': data.get('likes', 0),
        }

    def _reverse_language_map(self, sw_language):
        """Convert StoryWeaver language name to our code."""
        for code, name in self.LANGUAGE_MAP.items():
            if name.lower() == sw_language.lower():
                return code
        return 'HINDI'


def generate_recommendations(child):
    """Generate story recommendations for a child."""
    from apps.progress.models import Progress

    # Get child's language and level
    language = child.language
    level = child.level

    # Get stories they haven't read yet
    read_story_ids = Progress.objects.filter(
        child=child
    ).values_list('story_id', flat=True)

    recommended_stories = Story.objects.filter(
        language=language,
        level__lte=level + 1,  # Current level or one above
        level__gte=level - 1,  # Current level or one below
        is_active=True
    ).exclude(
        id__in=read_story_ids
    ).order_by('-read_count')[:10]

    # Create recommendations
    from .models import StoryRecommendation

    # Clear old recommendations
    StoryRecommendation.objects.filter(child=child).delete()

    for idx, story in enumerate(recommended_stories):
        score = 100 - (idx * 10)  # Simple scoring based on popularity
        reason = "Popular story at your level" if story.level == level else "Challenge yourself!"

        StoryRecommendation.objects.create(
            child=child,
            story=story,
            score=score,
            reason=reason
        )
