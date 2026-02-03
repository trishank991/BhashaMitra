"""Views for Peppi AI companion."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.children.models import Child
from apps.curriculum.models import VocabularyWord
from apps.curriculum.services.peppi_service import PeppiAIService
from apps.curriculum.serializers.peppi import (
    PeppiLearningContextSerializer,
    PeppiGreetingRequestSerializer,
    PeppiTeachWordRequestSerializer,
    PeppiFeedbackRequestSerializer,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peppi_greeting(request, child_id):
    """Get Peppi greeting for a child."""
    child = get_object_or_404(Child, id=child_id, user=request.user)

    serializer = PeppiGreetingRequestSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    time_of_day = serializer.validated_data.get('time_of_day')
    greeting_data = PeppiAIService.get_greeting(child, time_of_day)

    return Response(greeting_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def peppi_teach_word(request, child_id):
    """Get Peppi teaching script for a word."""
    child = get_object_or_404(Child, id=child_id, user=request.user)

    serializer = PeppiTeachWordRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    word = get_object_or_404(VocabularyWord, id=serializer.validated_data['word_id'])
    teaching_data = PeppiAIService.teach_word(word, child.age)

    return Response(teaching_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def peppi_feedback(request, child_id):
    """Get Peppi feedback for child's performance."""
    child = get_object_or_404(Child, id=child_id, user=request.user)

    serializer = PeppiFeedbackRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    is_correct = serializer.validated_data['is_correct']
    activity_type = serializer.validated_data['activity_type']

    feedback_data = PeppiAIService.give_feedback(is_correct, child.age, activity_type)

    return Response(feedback_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peppi_context(request, child_id):
    """Get Peppi learning context for a child."""
    child = get_object_or_404(Child, id=child_id, user=request.user)
    context = PeppiAIService.get_or_create_context(child)

    serializer = PeppiLearningContextSerializer(context)
    return Response(serializer.data, status=status.HTTP_200_OK)
