"""Context builder for Peppi chat modes."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Builds context dictionaries for different Peppi chat modes.

    Handles:
    - Festival story context with page-by-page narration
    - Curriculum help context with lesson data
    - General chat context with child preferences
    """

    @classmethod
    def build_festival_story_context(
        cls,
        festival,
        story,
        current_page: int = 1,
    ) -> dict:
        """
        Build context for festival story narration mode.

        Args:
            festival: Festival model instance
            story: Story model instance
            current_page: Current page number (1-indexed)

        Returns:
            Context dictionary for prompt template
        """
        try:
            # Get story pages
            pages = list(story.pages.order_by('page_number'))
            total_pages = len(pages)

            # Get current page content
            current_page_obj = None
            if pages and 1 <= current_page <= total_pages:
                current_page_obj = pages[current_page - 1]

            current_page_text = ""
            if current_page_obj:
                current_page_text = current_page_obj.text_primary
                if current_page_obj.text_romanized:
                    current_page_text += f"\n(Romanized: {current_page_obj.text_romanized})"

            # Get vocabulary words for current page
            vocabulary_words = ""
            if current_page_obj and hasattr(current_page_obj, 'vocabulary_words'):
                words = current_page_obj.vocabulary_words.all()
                vocab_list = []
                for word in words:
                    vocab_list.append(
                        f"- {word.word_primary} ({word.word_romanized}): {word.word_english}"
                    )
                vocabulary_words = "\n".join(vocab_list) if vocab_list else "None specified"

            return {
                'festival_name': festival.name_english if festival else 'Indian Festival',
                'festival_name_hindi': festival.name_primary if festival else '',
                'festival_description': (festival.description_primary or festival.description_english) if festival else '',
                'story_title': (story.title_primary or story.title_english) if story else 'Story',
                'story_summary': (story.description_primary or story.description_english or "") if story else "",
                'current_page': current_page,
                'total_pages': total_pages,
                'current_page_text': current_page_text,
                'vocabulary_words': vocabulary_words,
            }
        except Exception as e:
            logger.error(f"Error building festival story context: {e}")
            # Return minimal context if something fails
            return {
                'festival_name': 'Indian Festival',
                'festival_name_hindi': '',
                'festival_description': '',
                'story_title': 'Story',
                'story_summary': '',
                'current_page': 1,
                'total_pages': 1,
                'current_page_text': '',
                'vocabulary_words': 'None specified',
            }

    @classmethod
    def build_curriculum_help_context(
        cls,
        child,
        lesson=None,
    ) -> dict:
        """
        Build context for curriculum help mode.

        Args:
            child: Child model instance
            lesson: Optional Lesson model instance

        Returns:
            Context dictionary for prompt template
        """
        try:
            # Get child's current level
            level = getattr(child, 'level', None)
            level_name = "Beginner"
            level_code = "L1"

            if level:
                level_name = getattr(level, 'name_english', None) or getattr(level, 'name', 'Beginner')
                level_code = getattr(level, 'code', 'L1')

            # Get recent vocabulary from child's progress
            recent_words = cls._get_recent_vocabulary(child)

            # Get areas needing improvement
            areas_to_improve = cls._get_areas_to_improve(child)

            # Build lesson content if provided
            lesson_title = ""
            lesson_content = ""
            vocabulary_in_scope = ""
            grammar_concepts = ""

            if lesson:
                lesson_title = getattr(lesson, 'title_primary', '') or getattr(lesson, 'title_english', '') or ""
                lesson_content = getattr(lesson, 'content_primary', '') or getattr(lesson, 'content_english', '') or ""

                # Get lesson vocabulary
                if hasattr(lesson, 'vocabulary_items'):
                    try:
                        vocab_items = lesson.vocabulary_items.all()[:10]
                        vocab_list = []
                        for item in vocab_items:
                            vocab_list.append(
                                f"- {item.word_primary} ({item.word_romanized}): {item.word_english}"
                            )
                        vocabulary_in_scope = "\n".join(vocab_list)
                    except Exception as e:
                        logger.debug(f"Could not fetch lesson vocabulary: {e}")

                # Get grammar concepts if any
                if hasattr(lesson, 'grammar_concepts'):
                    try:
                        concepts = lesson.grammar_concepts.all()[:5]
                        grammar_list = [f"- {c.title}: {c.explanation}" for c in concepts]
                        grammar_concepts = "\n".join(grammar_list)
                    except Exception as e:
                        logger.debug(f"Could not fetch grammar concepts: {e}")

            return {
                'level_name': level_name,
                'level_code': level_code,
                'current_topic': lesson_title or "General Practice",
                'recent_words': recent_words or "None tracked yet",
                'areas_to_improve': areas_to_improve or "Keep practicing!",
                'lesson_title': lesson_title,
                'lesson_content': lesson_content,
                'vocabulary_in_scope': vocabulary_in_scope or "No specific vocabulary",
                'grammar_concepts': grammar_concepts or "No specific grammar focus",
            }
        except Exception as e:
            logger.error(f"Error building curriculum help context: {e}")
            # Return minimal context if something fails
            return {
                'level_name': 'Beginner',
                'level_code': 'L1',
                'current_topic': 'General Practice',
                'recent_words': 'None tracked yet',
                'areas_to_improve': 'Keep practicing!',
                'lesson_title': '',
                'lesson_content': '',
                'vocabulary_in_scope': 'No specific vocabulary',
                'grammar_concepts': 'No specific grammar focus',
            }

    @classmethod
    def build_general_chat_context(cls, child) -> dict:
        """
        Build context for general chat mode.

        Args:
            child: Child model instance

        Returns:
            Context dictionary for prompt template
        """
        return {
            # General mode doesn't need much context beyond base personality
            'child_interests': cls._get_child_interests(child),
        }

    @classmethod
    def _get_recent_vocabulary(cls, child, limit: int = 10) -> str:
        """Get recently learned vocabulary words for child."""
        try:
            # Try to get from vocabulary progress
            from apps.progress.models import VocabularyProgress

            recent = VocabularyProgress.objects.filter(
                child=child,
                mastery_level__gte=2  # At least partially learned
            ).order_by('-last_practiced')[:limit]

            if recent:
                words = [f"{vp.vocabulary_item.word_primary}" for vp in recent if hasattr(vp, 'vocabulary_item')]
                return ", ".join(words) if words else "None tracked yet"

        except Exception as e:
            logger.debug(f"Could not fetch vocabulary progress: {e}")

        return "None tracked yet"

    @classmethod
    def _get_areas_to_improve(cls, child) -> str:
        """Get areas where child needs more practice."""
        try:
            from apps.progress.models import VocabularyProgress

            # Find words with low mastery
            struggling = VocabularyProgress.objects.filter(
                child=child,
                mastery_level__lte=1,
                attempts__gte=2  # Has tried but struggling
            ).order_by('-last_practiced')[:5]

            if struggling:
                areas = []
                for vp in struggling:
                    if hasattr(vp, 'vocabulary_item'):
                        areas.append(vp.vocabulary_item.word_primary)
                if areas:
                    return f"Practice these words: {', '.join(areas)}"

        except Exception as e:
            logger.debug(f"Could not fetch improvement areas: {e}")

        return "Keep practicing! You're doing great!"

    @classmethod
    def _get_child_interests(cls, child) -> str:
        """Get child's interests based on activity."""
        interests = []

        try:
            # Check what festivals they've explored
            from apps.festivals.models import FestivalProgress
            festival_progress = FestivalProgress.objects.filter(child=child).count()
            if festival_progress > 0:
                interests.append("festivals")

            # Check what stories they've read
            from apps.progress.models import StoryProgress
            story_progress = StoryProgress.objects.filter(child=child).count()
            if story_progress > 0:
                interests.append("stories")

        except Exception as e:
            logger.debug(f"Could not fetch interests: {e}")

        return ", ".join(interests) if interests else "learning new things"

    @classmethod
    def get_time_of_day(cls) -> str:
        """Get the current time of day for greetings."""
        from django.utils import timezone
        hour = timezone.now().hour

        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'

    @classmethod
    def build_conversation_context(
        cls,
        conversation,
        child,
    ) -> dict:
        """
        Build complete context based on conversation mode.

        Args:
            conversation: PeppiConversation instance
            child: Child instance

        Returns:
            Context dictionary for prompt template
        """
        mode = conversation.mode

        if mode == 'FESTIVAL_STORY':
            if conversation.festival and conversation.story:
                # Get current page from context snapshot
                current_page = conversation.context_snapshot.get('current_page', 1)
                return cls.build_festival_story_context(
                    conversation.festival,
                    conversation.story,
                    current_page,
                )
            else:
                logger.warning(f"Festival story mode without festival/story: {conversation.id}")
                return {}

        elif mode == 'CURRICULUM_HELP':
            return cls.build_curriculum_help_context(
                child,
                conversation.lesson,
            )

        else:  # GENERAL
            return cls.build_general_chat_context(child)

    @classmethod
    def update_story_page(cls, conversation, new_page: int):
        """
        Update the current page in conversation context.

        Args:
            conversation: PeppiConversation instance
            new_page: New page number
        """
        context = conversation.context_snapshot or {}
        context['current_page'] = new_page
        conversation.context_snapshot = context
        conversation.save(update_fields=['context_snapshot'])
