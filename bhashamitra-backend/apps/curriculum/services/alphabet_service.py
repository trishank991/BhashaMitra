"""Alphabet learning service."""
from django.utils import timezone
from django.db import transaction
from typing import List, Optional
from apps.curriculum.models.script import Script, Letter, LetterProgress, AlphabetCategory


class AlphabetService:
    """Service for managing alphabet learning progress."""

    @staticmethod
    def get_script_for_language(language: str) -> Optional[Script]:
        """Get the script/alphabet for a language."""
        return Script.objects.filter(language=language).first()

    @staticmethod
    def get_letters_by_category(script_id: str, category_type: str = None) -> dict:
        """
        Get all letters organized by category.
        Optionally filter by category type.
        """
        script = Script.objects.prefetch_related(
            'categories__letters'
        ).get(id=script_id)

        result = {
            'script_id': str(script.id),
            'script_name': script.name,
            'categories': []
        }

        categories = script.categories.all()
        if category_type:
            categories = categories.filter(category_type=category_type)

        for category in categories:
            result['categories'].append({
                'id': str(category.id),
                'name': category.name,
                'name_native': category.name_native,
                'category_type': category.category_type,
                'letters': [{
                    'id': str(letter.id),
                    'character': letter.character,
                    'romanization': letter.romanization,
                    'ipa': letter.ipa,
                    'audio_url': letter.audio_url,
                    'example_word': letter.example_word,
                    'example_word_romanization': letter.example_word_romanization,
                    'example_word_translation': letter.example_word_translation,
                } for letter in category.letters.filter(is_active=True).order_by('order')]
            })

        return result

    @staticmethod
    @transaction.atomic
    def update_letter_progress(
        child_id: str,
        letter_id: str,
        skill_type: str,
        score: int
    ) -> LetterProgress:
        """
        Update progress for a specific letter skill.

        skill_type: 'recognition', 'listening', 'tracing', 'writing', 'pronunciation'
        score: 0-100
        """
        progress, created = LetterProgress.objects.get_or_create(
            child_id=child_id,
            letter_id=letter_id
        )

        # Update the appropriate score field
        skill_field_map = {
            'recognition': 'recognition_score',
            'listening': 'listening_score',
            'tracing': 'tracing_score',
            'writing': 'writing_score',
            'pronunciation': 'pronunciation_score',
        }

        field_name = skill_field_map.get(skill_type)
        if field_name:
            # Use weighted average with previous score
            current_score = getattr(progress, field_name)
            if progress.times_practiced > 0:
                # Weighted average: 70% new, 30% old
                new_score = int((score * 0.7) + (current_score * 0.3))
            else:
                new_score = score
            setattr(progress, field_name, new_score)

        progress.times_practiced += 1
        progress.save()

        # Check for mastery
        progress.check_mastery()

        return progress

    @staticmethod
    def get_child_alphabet_progress(child_id: str, language: str) -> dict:
        """
        Get alphabet learning progress for a child.
        Returns summary and per-letter progress.
        """
        script = AlphabetService.get_script_for_language(language)
        if not script:
            return {'error': f'No script found for language: {language}'}

        total_letters = Letter.objects.filter(
            category__script=script,
            is_active=True
        ).count()

        progress_records = LetterProgress.objects.filter(
            child_id=child_id,
            letter__category__script=script
        ).select_related('letter')

        letters_practiced = progress_records.count()
        letters_mastered = progress_records.filter(mastered=True).count()

        # Calculate average scores by skill
        skill_averages = {
            'recognition': 0,
            'listening': 0,
            'tracing': 0,
            'writing': 0,
            'pronunciation': 0,
        }

        if letters_practiced > 0:
            for skill in skill_averages.keys():
                scores = [getattr(p, f'{skill}_score') for p in progress_records]
                skill_averages[skill] = round(sum(scores) / len(scores), 1)

        return {
            'language': language,
            'script_name': script.name,
            'total_letters': total_letters,
            'letters_practiced': letters_practiced,
            'letters_mastered': letters_mastered,
            'progress_percentage': round((letters_mastered / total_letters) * 100, 1) if total_letters else 0,
            'skill_averages': skill_averages,
            'overall_average': round(sum(skill_averages.values()) / len(skill_averages), 1),
        }

    @staticmethod
    def get_next_letters_to_learn(child_id: str, language: str, limit: int = 5) -> List[dict]:
        """
        Get the next letters a child should learn.
        Prioritizes unlearned letters in category order.
        """
        script = AlphabetService.get_script_for_language(language)
        if not script:
            return []

        # Get IDs of letters already being practiced
        practiced_ids = LetterProgress.objects.filter(
            child_id=child_id,
            letter__category__script=script
        ).values_list('letter_id', flat=True)

        # Get next unpracticed letters
        next_letters = Letter.objects.filter(
            category__script=script,
            is_active=True
        ).exclude(
            id__in=practiced_ids
        ).select_related('category').order_by(
            'category__order', 'order'
        )[:limit]

        return [{
            'id': str(letter.id),
            'character': letter.character,
            'romanization': letter.romanization,
            'category': letter.category.name,
            'category_type': letter.category.category_type,
            'audio_url': letter.audio_url,
            'example_word': letter.example_word,
            'example_word_translation': letter.example_word_translation,
        } for letter in next_letters]

    @staticmethod
    def get_letters_needing_practice(child_id: str, language: str, limit: int = 10) -> List[dict]:
        """
        Get letters that need more practice (low scores, not mastered).
        """
        script = AlphabetService.get_script_for_language(language)
        if not script:
            return []

        # Get letters with low overall scores
        progress_records = LetterProgress.objects.filter(
            child_id=child_id,
            letter__category__script=script,
            mastered=False
        ).select_related('letter', 'letter__category')

        # Sort by overall score (lowest first)
        records_with_scores = []
        for progress in progress_records:
            records_with_scores.append({
                'progress': progress,
                'overall_score': progress.overall_score
            })

        records_with_scores.sort(key=lambda x: x['overall_score'])

        return [{
            'id': str(item['progress'].letter.id),
            'character': item['progress'].letter.character,
            'romanization': item['progress'].letter.romanization,
            'category': item['progress'].letter.category.name,
            'overall_score': item['overall_score'],
            'times_practiced': item['progress'].times_practiced,
            'weakest_skill': AlphabetService._get_weakest_skill(item['progress']),
        } for item in records_with_scores[:limit]]

    @staticmethod
    def _get_weakest_skill(progress: LetterProgress) -> str:
        """Get the skill with the lowest score."""
        skills = {
            'recognition': progress.recognition_score,
            'listening': progress.listening_score,
            'tracing': progress.tracing_score,
            'writing': progress.writing_score,
            'pronunciation': progress.pronunciation_score,
        }
        return min(skills, key=skills.get)
