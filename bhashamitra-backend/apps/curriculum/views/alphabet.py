"""Alphabet/Script views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from apps.curriculum.models.script import Script, Letter, LetterProgress
from apps.curriculum.models.verified_content import VerifiedLetter
from apps.curriculum.serializers.script import (
    ScriptSerializer,
    ScriptDetailSerializer,
    LetterSerializer,
    LetterDetailSerializer,
    LetterProgressSerializer,
)
from apps.curriculum.services.alphabet_service import AlphabetService


class ScriptListView(APIView):
    """List available scripts/alphabets."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id=None):
        """Get scripts available for the child's language (optional child_id)."""
        language = None
        
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
                language = request.query_params.get('language', child.language)
            except Child.DoesNotExist:
                return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # No child_id provided, use query param or default to HINDI
            language = request.query_params.get('language', 'HINDI')
        
        scripts = Script.objects.filter(language=language.upper() if language else None)
        serializer = ScriptSerializer(scripts, many=True)

        return Response({'data': serializer.data})


class ScriptDetailView(APIView):
    """Get script details with categories and letters."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            script = Script.objects.prefetch_related(
                'categories__letters', 'matras'
            ).get(pk=pk)
        except Script.DoesNotExist:
            return Response({'detail': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScriptDetailSerializer(script)
        return Response({'data': serializer.data})


class ScriptLettersView(APIView):
    """Get all letters for a script organized by category."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        category_type = request.query_params.get('category_type')

        try:
            result = AlphabetService.get_letters_by_category(pk, category_type)
            return Response({'data': result})
        except Script.DoesNotExist:
            return Response({'detail': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)

class LetterListView(APIView):
    """List letters with optional filtering."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        # FIX: Normalize language to UPPERCASE to match DB entries (HINDI, GUJARATI)
        raw_language = request.query_params.get('language', child.language)
        language = raw_language.upper() if raw_language else ""
        
        category_type = request.query_params.get('category_type')

        # Query Letter model
        letters = Letter.objects.filter(
            category__script__language=language,
            is_active=True
        ).select_related('category')

        if category_type:
            letters = letters.filter(category__category_type=category_type)

        letters = letters.order_by('category__order', 'order')
        
        # Query VerifiedLetter model (specifically for Hindi)
        verified_letters = VerifiedLetter.objects.filter(
            language=language,
            status='VERIFIED'
        ).order_by('character')
        
        # Serialize standard results
        letter_data = LetterSerializer(letters, many=True).data
        
        # Convert VerifiedLetter to the same format as Letter
        verified_letter_data = []
        for vl in verified_letters:
            verified_letter_data.append({
                'id': str(vl.id),
                'character': vl.character,
                'romanization': vl.romanization,
                'ipa': '',
                'pronunciation_guide': vl.pronunciation_guide,
                'audio_url': vl.audio_url if vl.audio_url else '',
                'example_image': vl.example_image if vl.example_image else '',
                'order': 0
            })
        
        # Merge both datasets
        all_letters = list(letter_data) + verified_letter_data

        return Response({'data': all_letters})

class LetterDetailView(APIView):
    """Get letter details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            letter = Letter.objects.get(pk=pk)
        except Letter.DoesNotExist:
            return Response({'detail': 'Letter not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get child's progress for this letter
        progress = LetterProgress.objects.filter(child=child, letter=letter).first()

        serializer = LetterDetailSerializer(letter)
        data = serializer.data

        if progress:
            data['progress'] = LetterProgressSerializer(progress).data

        return Response({'data': data})


class LetterProgressView(APIView):
    """Update progress for a letter."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        """Get progress for a specific letter."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            progress = LetterProgress.objects.select_related('letter').get(
                child=child, letter_id=pk
            )
            serializer = LetterProgressSerializer(progress)
            return Response({'data': serializer.data})
        except LetterProgress.DoesNotExist:
            return Response({'detail': 'No progress found for this letter'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, child_id, pk):
        """Update progress for a letter skill."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        skill_type = request.data.get('skill_type')
        score = request.data.get('score')

        if not skill_type or score is None:
            return Response(
                {'detail': 'skill_type and score are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_skills = ['recognition', 'listening', 'tracing', 'writing', 'pronunciation']
        if skill_type not in valid_skills:
            return Response(
                {'detail': f'skill_type must be one of: {valid_skills}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            progress = AlphabetService.update_letter_progress(
                child_id=str(child.id),
                letter_id=str(pk),
                skill_type=skill_type,
                score=int(score)
            )
            serializer = LetterProgressSerializer(progress)
            return Response({'data': serializer.data})
        except Letter.DoesNotExist:
            return Response({'detail': 'Letter not found'}, status=status.HTTP_404_NOT_FOUND)


class AlphabetProgressView(APIView):
    """Get overall alphabet learning progress."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language).upper()
        progress = AlphabetService.get_child_alphabet_progress(str(child.id), language)

        # Get next letters to learn
        next_letters = AlphabetService.get_next_letters_to_learn(str(child.id), language, limit=5)

        # Get letters needing practice
        needs_practice = AlphabetService.get_letters_needing_practice(str(child.id), language, limit=5)

        return Response({
            'data': {
                **progress,
                'next_to_learn': next_letters,
                'needs_practice': needs_practice,
            }
        })