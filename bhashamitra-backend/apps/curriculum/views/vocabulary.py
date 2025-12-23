"""Vocabulary views with SRS flashcards."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord, WordProgress
from apps.curriculum.serializers.vocabulary import (
    VocabularyThemeSerializer,
    VocabularyThemeDetailSerializer,
    VocabularyWordSerializer,
    VocabularyWordDetailSerializer,
    WordProgressSerializer,
)
from apps.curriculum.services.srs_service import SRSService
from apps.core.validators import safe_level, safe_limit, safe_int


class VocabularyThemeListView(APIView):
    """List vocabulary themes."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)
        level = request.query_params.get('level')

        themes = VocabularyTheme.objects.filter(
            language=language,
            is_active=True
        )

        if level:
            themes = themes.filter(level__lte=safe_level(level))

        themes = themes.order_by('level', 'order')
        serializer = VocabularyThemeSerializer(themes, many=True)

        # Add progress info for each theme
        data = serializer.data
        for theme_data in data:
            stats = SRSService.get_theme_stats(str(child.id), theme_data['id'])
            theme_data['progress'] = {
                'words_started': stats['words_started'],
                'words_mastered': stats['words_mastered'],
                'words_due': stats['words_due'],
                'progress_percentage': stats['progress_percentage'],
            }

        return Response({'data': data})


class ThemeDetailView(APIView):
    """Get theme details with words."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            theme = VocabularyTheme.objects.prefetch_related('words').get(pk=pk)
        except VocabularyTheme.DoesNotExist:
            return Response({'detail': 'Theme not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VocabularyThemeDetailSerializer(theme)
        return Response({'data': serializer.data})


class ThemeWordsView(APIView):
    """Get words for a theme with progress info."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            theme = VocabularyTheme.objects.get(pk=pk)
        except VocabularyTheme.DoesNotExist:
            return Response({'detail': 'Theme not found'}, status=status.HTTP_404_NOT_FOUND)

        words = VocabularyWord.objects.filter(theme=theme).order_by('order')
        serializer = VocabularyWordSerializer(words, many=True)

        # Get progress for each word
        progress_map = {
            str(p.word_id): p
            for p in WordProgress.objects.filter(child=child, word__theme=theme)
        }

        data = serializer.data
        for word_data in data:
            progress = progress_map.get(word_data['id'])
            if progress:
                word_data['progress'] = {
                    'mastered': progress.mastered,
                    'times_reviewed': progress.times_reviewed,
                    'accuracy': progress.accuracy,
                    'next_review': progress.next_review.isoformat(),
                }
            else:
                word_data['progress'] = None

        return Response({'data': data})


class ThemeStatsView(APIView):
    """Get detailed statistics for a theme."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            stats = SRSService.get_theme_stats(str(child.id), str(pk))
            return Response({'data': stats})
        except VocabularyTheme.DoesNotExist:
            return Response({'detail': 'Theme not found'}, status=status.HTTP_404_NOT_FOUND)


class WordDetailView(APIView):
    """Get word details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            word = VocabularyWord.objects.get(pk=pk)
        except VocabularyWord.DoesNotExist:
            return Response({'detail': 'Word not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VocabularyWordDetailSerializer(word)
        data = serializer.data

        # Get progress
        progress = WordProgress.objects.filter(child=child, word=word).first()
        if progress:
            data['progress'] = WordProgressSerializer(progress).data

        return Response({'data': data})


class FlashcardsDueView(APIView):
    """Get flashcards due for review."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        theme_id = request.query_params.get('theme_id')
        limit = safe_limit(request.query_params.get('limit'), default=20, max_limit=50)

        due_words = SRSService.get_due_words(str(child.id), theme_id, limit)

        data = [{
            'word_id': str(p.word.id),
            'word': p.word.word,
            'romanization': p.word.romanization,
            'translation': p.word.translation,
            'part_of_speech': p.word.part_of_speech,
            'gender': p.word.gender,
            'example_sentence': p.word.example_sentence,
            'pronunciation_audio_url': p.word.pronunciation_audio_url,
            'image_url': p.word.image_url,
            'times_reviewed': p.times_reviewed,
            'interval_days': p.interval_days,
            'is_new': False,
        } for p in due_words]

        return Response({
            'data': data,
            'meta': {'total_due': len(data)}
        })


class FlashcardReviewView(APIView):
    """Submit a single flashcard review."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        word_id = request.data.get('word_id')
        quality = request.data.get('quality')

        if not word_id or quality is None:
            return Response(
                {'detail': 'word_id and quality are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (0 <= int(quality) <= 5):
            return Response(
                {'detail': 'quality must be between 0 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = SRSService.record_review(str(child.id), word_id, int(quality))

        # Award points for correct answers (quality >= 3)
        points_earned = 0
        if result['correct']:
            points_earned = 5  # 5 XP per correct review
            child.total_points += points_earned
            child.save(update_fields=['total_points'])

        result['points_earned'] = points_earned
        result['total_points'] = child.total_points

        return Response({'data': result})


class FlashcardSessionView(APIView):
    """Get or submit a flashcard session."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        """Get a mixed flashcard session (due + new words)."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        theme_id = request.query_params.get('theme_id')
        count = safe_limit(request.query_params.get('count'), default=10, max_limit=30)

        if not theme_id:
            return Response(
                {'detail': 'theme_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        flashcards = SRSService.get_flashcard_session(str(child.id), theme_id, count)

        return Response({
            'data': flashcards,
            'meta': {
                'total': len(flashcards),
                'new_count': sum(1 for f in flashcards if f['is_new']),
                'review_count': sum(1 for f in flashcards if not f['is_new']),
            }
        })

    def post(self, request, child_id):
        """Submit batch flashcard reviews."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        reviews = request.data.get('reviews', [])

        if not reviews:
            return Response(
                {'detail': 'reviews array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = SRSService.batch_review(str(child.id), reviews)

        # Award points to child
        if result['points_earned'] > 0:
            child.total_points += result['points_earned']
            child.save(update_fields=['total_points'])

        return Response({'data': result})
