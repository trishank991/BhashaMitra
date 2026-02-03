"""Spaced Repetition Service using SM-2 algorithm."""
from django.utils import timezone
from django.db import transaction
from typing import List, Optional
from apps.curriculum.models.vocabulary import VocabularyWord, WordProgress, VocabularyTheme


class SRSService:
    """Service for managing spaced repetition vocabulary learning."""

    @staticmethod
    def get_due_words(child_id: str, theme_id: Optional[str] = None, limit: int = 20) -> List[WordProgress]:
        """
        Get words due for review based on SRS schedule.
        Returns words where next_review <= now and not mastered.
        """
        queryset = WordProgress.objects.filter(
            child_id=child_id,
            next_review__lte=timezone.now(),
            mastered=False
        ).select_related('word', 'word__theme')

        if theme_id:
            queryset = queryset.filter(word__theme_id=theme_id)

        return list(queryset.order_by('next_review')[:limit])

    @staticmethod
    def get_new_words(child_id: str, theme_id: str, limit: int = 5) -> List[VocabularyWord]:
        """
        Get new words not yet started by the child.
        Used to introduce new vocabulary.
        """
        started_word_ids = WordProgress.objects.filter(
            child_id=child_id,
            word__theme_id=theme_id
        ).values_list('word_id', flat=True)

        return list(
            VocabularyWord.objects.filter(theme_id=theme_id)
            .exclude(id__in=started_word_ids)
            .order_by('order')[:limit]
        )

    @staticmethod
    @transaction.atomic
    def start_word(child_id: str, word_id: str) -> WordProgress:
        """Initialize progress for a new word."""
        progress, created = WordProgress.objects.get_or_create(
            child_id=child_id,
            word_id=word_id,
            defaults={'next_review': timezone.now()}
        )
        return progress

    @staticmethod
    @transaction.atomic
    def record_review(child_id: str, word_id: str, quality: int) -> dict:
        """
        Record a review and update SRS schedule.

        Quality scale (SM-2):
        0 - Complete blackout, no memory
        1 - Incorrect, but recognized answer when shown
        2 - Incorrect, but answer seemed easy to recall
        3 - Correct with serious difficulty
        4 - Correct with some hesitation
        5 - Perfect recall, instant answer

        Returns dict with updated schedule info.
        """
        progress, created = WordProgress.objects.get_or_create(
            child_id=child_id,
            word_id=word_id,
            defaults={'next_review': timezone.now()}
        )

        # Update SRS using the model method
        progress.update_srs(quality)

        return {
            'word_id': str(word_id),
            'quality': quality,
            'correct': quality >= 3,
            'new_interval_days': progress.interval_days,
            'next_review': progress.next_review.isoformat(),
            'ease_factor': round(progress.ease_factor, 2),
            'repetitions': progress.repetitions,
            'mastered': progress.mastered,
        }

    @staticmethod
    @transaction.atomic
    def batch_review(child_id: str, reviews: List[dict]) -> dict:
        """
        Process multiple reviews at once.

        Args:
            child_id: Child's UUID
            reviews: List of dicts with 'word_id' and 'quality'

        Returns summary of the session.
        """
        results = []
        correct_count = 0
        points_earned = 0

        for review in reviews:
            result = SRSService.record_review(
                child_id=child_id,
                word_id=review['word_id'],
                quality=review['quality']
            )
            results.append(result)
            if result['correct']:
                correct_count += 1
                points_earned += 5  # Base points per correct answer

        return {
            'total_reviewed': len(reviews),
            'correct_count': correct_count,
            'accuracy': round((correct_count / len(reviews)) * 100, 1) if reviews else 0,
            'points_earned': points_earned,
            'results': results,
        }

    @staticmethod
    def get_theme_stats(child_id: str, theme_id: str) -> dict:
        """Get detailed learning statistics for a theme."""
        theme = VocabularyTheme.objects.get(id=theme_id)
        total_words = theme.words.count()

        progress_qs = WordProgress.objects.filter(
            child_id=child_id,
            word__theme_id=theme_id
        )

        words_started = progress_qs.count()
        words_mastered = progress_qs.filter(mastered=True).count()
        words_due = progress_qs.filter(
            next_review__lte=timezone.now(),
            mastered=False
        ).count()

        total_reviews = sum(p.times_reviewed for p in progress_qs)
        total_correct = sum(p.times_correct for p in progress_qs)

        return {
            'theme_id': str(theme_id),
            'theme_name': theme.name,
            'theme_name_native': theme.name_native,
            'total_words': total_words,
            'words_started': words_started,
            'words_mastered': words_mastered,
            'words_due': words_due,
            'words_remaining': total_words - words_started,
            'progress_percentage': round((words_mastered / total_words) * 100, 1) if total_words else 0,
            'total_reviews': total_reviews,
            'overall_accuracy': round((total_correct / total_reviews) * 100, 1) if total_reviews else 0,
        }

    @staticmethod
    def get_child_vocabulary_summary(child_id: str, language: str = None) -> dict:
        """Get overall vocabulary summary across all themes."""
        progress_qs = WordProgress.objects.filter(child_id=child_id)

        if language:
            progress_qs = progress_qs.filter(word__theme__language=language)

        total_started = progress_qs.count()
        total_mastered = progress_qs.filter(mastered=True).count()
        total_due = progress_qs.filter(
            next_review__lte=timezone.now(),
            mastered=False
        ).count()
        total_reviews = sum(p.times_reviewed for p in progress_qs)

        return {
            'total_words_started': total_started,
            'total_words_mastered': total_mastered,
            'total_words_due': total_due,
            'total_reviews': total_reviews,
            'mastery_percentage': round((total_mastered / total_started) * 100, 1) if total_started else 0,
        }

    @staticmethod
    def get_flashcard_session(child_id: str, theme_id: str = None, count: int = 10) -> List[dict]:
        """
        Get a mixed session of due words and new words for flashcard practice.
        Prioritizes due words, fills remaining slots with new words.
        """
        flashcards = []

        # Get due words first (priority)
        due_words = SRSService.get_due_words(child_id, theme_id, limit=count)
        for progress in due_words:
            word = progress.word
            flashcards.append({
                'word_id': str(word.id),
                'word': word.word,
                'romanization': word.romanization,
                'translation': word.translation,
                'part_of_speech': word.part_of_speech,
                'gender': word.gender,
                'example_sentence': word.example_sentence,
                'pronunciation_audio_url': word.pronunciation_audio_url,
                'image_url': word.image_url,
                'times_reviewed': progress.times_reviewed,
                'interval_days': progress.interval_days,
                'is_new': False,
            })

        # Fill remaining slots with new words
        remaining_slots = count - len(flashcards)
        if remaining_slots > 0 and theme_id:
            new_words = SRSService.get_new_words(child_id, theme_id, limit=remaining_slots)
            for word in new_words:
                # Initialize progress for new word
                SRSService.start_word(child_id, str(word.id))
                flashcards.append({
                    'word_id': str(word.id),
                    'word': word.word,
                    'romanization': word.romanization,
                    'translation': word.translation,
                    'part_of_speech': word.part_of_speech,
                    'gender': word.gender,
                    'example_sentence': word.example_sentence,
                    'pronunciation_audio_url': word.pronunciation_audio_url,
                    'image_url': word.image_url,
                    'times_reviewed': 0,
                    'interval_days': 0,
                    'is_new': True,
                })

        return flashcards
