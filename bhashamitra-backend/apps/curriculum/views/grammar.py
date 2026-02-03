"""Grammar views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from apps.children.models import Child
from apps.curriculum.models.grammar import GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress
from apps.curriculum.serializers.grammar import (
    GrammarTopicSerializer,
    GrammarTopicDetailSerializer,
    GrammarRuleSerializer,
    GrammarRuleDetailSerializer,
    GrammarExerciseSerializer,
    GrammarProgressSerializer,
)


class GrammarTopicListView(APIView):
    """List grammar topics."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)
        level = request.query_params.get('level')

        topics = GrammarTopic.objects.filter(
            language=language,
            is_active=True
        )

        if level:
            topics = topics.filter(level__lte=int(level))

        topics = topics.order_by('level', 'order')
        serializer = GrammarTopicSerializer(topics, many=True)

        # Add progress info
        progress_map = {
            str(p.topic_id): p
            for p in GrammarProgress.objects.filter(child=child)
        }

        data = serializer.data
        for topic_data in data:
            progress = progress_map.get(topic_data['id'])
            if progress:
                topic_data['progress'] = {
                    'exercises_attempted': progress.exercises_attempted,
                    'exercises_correct': progress.exercises_correct,
                    'accuracy': progress.accuracy,
                    'mastered': progress.mastered,
                }
            else:
                topic_data['progress'] = None

        return Response({'data': data})


class GrammarTopicDetailView(APIView):
    """Get topic details with rules."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            topic = GrammarTopic.objects.prefetch_related(
                'rules__exercises', 'prerequisites'
            ).get(pk=pk)
        except GrammarTopic.DoesNotExist:
            return Response({'detail': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GrammarTopicDetailSerializer(topic)
        return Response({'data': serializer.data})


class TopicRulesView(APIView):
    """Get rules for a topic."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            topic = GrammarTopic.objects.get(pk=pk)
        except GrammarTopic.DoesNotExist:
            return Response({'detail': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        rules = GrammarRule.objects.filter(topic=topic).order_by('order')
        serializer = GrammarRuleSerializer(rules, many=True)

        return Response({'data': serializer.data})


class TopicExercisesView(APIView):
    """Get exercises for a topic."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            topic = GrammarTopic.objects.get(pk=pk)
        except GrammarTopic.DoesNotExist:
            return Response({'detail': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        exercises = GrammarExercise.objects.filter(
            rule__topic=topic
        ).select_related('rule').order_by('rule__order', 'order')

        serializer = GrammarExerciseSerializer(exercises, many=True)

        return Response({'data': serializer.data})


class ExerciseDetailView(APIView):
    """Get exercise details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            exercise = GrammarExercise.objects.select_related('rule__topic').get(pk=pk)
        except GrammarExercise.DoesNotExist:
            return Response({'detail': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GrammarExerciseSerializer(exercise)
        data = serializer.data
        data['rule_title'] = exercise.rule.title
        data['topic_name'] = exercise.rule.topic.name

        return Response({'data': data})


class ExerciseSubmitView(APIView):
    """Submit answer for an exercise."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            exercise = GrammarExercise.objects.select_related('rule__topic').get(pk=pk)
        except GrammarExercise.DoesNotExist:
            return Response({'detail': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

        answer = request.data.get('answer', '')

        if not answer:
            return Response(
                {'detail': 'answer is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check answer
        result = exercise.check_answer(answer)

        # Update progress
        topic = exercise.rule.topic
        progress, created = GrammarProgress.objects.get_or_create(
            child=child,
            topic=topic
        )
        progress.exercises_attempted += 1
        if result['is_correct']:
            progress.exercises_correct += 1
            # Award points
            child.total_points += result['points']
            child.save(update_fields=['total_points'])

        # Check for mastery (80% accuracy with at least 10 exercises)
        if progress.exercises_attempted >= 10 and progress.accuracy >= 80:
            if not progress.mastered:
                from django.utils import timezone
                progress.mastered = True
                progress.mastered_at = timezone.now()

        progress.save()

        return Response({
            'data': {
                'is_correct': result['is_correct'],
                'correct_answer': result['correct_answer'],
                'explanation': result['explanation'],
                'points_earned': result['points'],
                'progress': {
                    'exercises_attempted': progress.exercises_attempted,
                    'exercises_correct': progress.exercises_correct,
                    'accuracy': progress.accuracy,
                    'mastered': progress.mastered,
                }
            }
        })


class GrammarProgressView(APIView):
    """Get overall grammar progress."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)

        # Get all topics
        topics = GrammarTopic.objects.filter(
            language=language,
            is_active=True
        )

        total_topics = topics.count()

        # Get progress records
        progress_records = GrammarProgress.objects.filter(
            child=child,
            topic__language=language
        ).select_related('topic')

        topics_started = progress_records.count()
        topics_mastered = progress_records.filter(mastered=True).count()

        total_attempted = sum(p.exercises_attempted for p in progress_records)
        total_correct = sum(p.exercises_correct for p in progress_records)

        return Response({
            'data': {
                'total_topics': total_topics,
                'topics_started': topics_started,
                'topics_mastered': topics_mastered,
                'progress_percentage': round((topics_mastered / total_topics) * 100, 1) if total_topics else 0,
                'total_exercises_attempted': total_attempted,
                'total_exercises_correct': total_correct,
                'overall_accuracy': round((total_correct / total_attempted) * 100, 1) if total_attempted else 0,
            }
        })
