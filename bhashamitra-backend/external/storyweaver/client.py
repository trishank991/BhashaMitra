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
        self.base_url = getattr(settings, 'STORYWEAVER_BASE_URL', 'https://storyweaver.org.in/api/v1')

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
