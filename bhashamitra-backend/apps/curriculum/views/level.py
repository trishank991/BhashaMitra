"""Views for curriculum hierarchy (levels, modules, lessons)."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.children.models import Child
from apps.curriculum.models.level import CurriculumLevel, CurriculumModule, Lesson
from apps.curriculum.models.progress import LevelProgress, ModuleProgress, LessonProgress
from apps.curriculum.serializers.level import (
    CurriculumLevelSerializer,
    CurriculumLevelDetailSerializer,
    CurriculumModuleSerializer,
    CurriculumModuleDetailSerializer,
    LessonSerializer,
    LessonDetailSerializer,
    LevelProgressSerializer,
    ModuleProgressSerializer,
    LessonProgressSerializer,
    LessonProgressUpdateSerializer,
)


class CurriculumLevelListView(APIView):
    """List all curriculum levels."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id=None):
        """Get all active curriculum levels with optional child's progress.

        child_id can come from:
        - URL path parameter (when called via /children/{child_id}/curriculum/levels/)
        - Query parameter (when called via /curriculum/levels/?child_id=xxx)
        """
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        levels = CurriculumLevel.objects.filter(is_active=True).order_by('order')
        serializer = CurriculumLevelSerializer(levels, many=True)

        # Get progress for each level if child is provided
        progress_map = {}
        if child:
            progress_map = {
                str(p.level_id): p
                for p in LevelProgress.objects.filter(child=child)
            }

        data = serializer.data
        for level_data in data:
            progress = progress_map.get(level_data['id'])
            level_data['progress'] = {
                'started': progress is not None,
                'modules_completed': progress.modules_completed if progress else 0,
                'total_points': progress.total_points if progress else 0,
                'is_complete': progress.is_complete if progress else False,
                'completed_at': progress.completed_at if progress else None,
            }
            # Add total_modules and completed_modules for frontend compatibility
            level_data['total_modules'] = level_data.get('module_count', 0)
            level_data['completed_modules'] = progress.modules_completed if progress else 0

        return Response(data)


class CurriculumLevelDetailView(APIView):
    """Get level details with modules."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, child_id=None):
        """Get level detail with modules and optional progress."""
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        level = get_object_or_404(CurriculumLevel, pk=pk)
        serializer = CurriculumLevelDetailSerializer(level)

        # Get level progress if child is provided
        progress_data = {
            'started': False,
            'modules_completed': 0,
            'total_points': 0,
            'is_complete': False,
            'completed_at': None,
        }
        if child:
            try:
                level_progress = LevelProgress.objects.get(child=child, level=level)
                progress_data = {
                    'started': True,
                    'modules_completed': level_progress.modules_completed,
                    'total_points': level_progress.total_points,
                    'is_complete': level_progress.is_complete,
                    'completed_at': level_progress.completed_at,
                }
            except LevelProgress.DoesNotExist:
                pass

        # Add total_modules and completed_modules for frontend compatibility
        data = serializer.data
        data['total_modules'] = data.get('module_count', 0)
        data['completed_modules'] = progress_data.get('modules_completed', 0)

        return Response({
            **data,
            'progress': progress_data,
        })


class CurriculumModuleListView(APIView):
    """List modules for a level."""
    permission_classes = [IsAuthenticated]

    def get(self, request, level_id, child_id=None):
        """Get modules for a level with optional child's progress."""
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        level = get_object_or_404(CurriculumLevel, pk=level_id)
        modules = CurriculumModule.objects.filter(level=level, is_active=True).order_by('order')
        serializer = CurriculumModuleSerializer(modules, many=True)

        # Get progress for each module if child is provided
        progress_map = {}
        if child:
            progress_map = {
                str(p.module_id): p
                for p in ModuleProgress.objects.filter(child=child, module__level=level)
            }

        data = serializer.data
        for module_data in data:
            progress = progress_map.get(module_data['id'])
            module_data['progress'] = {
                'started': progress is not None,
                'lessons_completed': progress.lessons_completed if progress else 0,
                'total_points': progress.total_points if progress else 0,
                'is_complete': progress.is_complete if progress else False,
                'completed_at': progress.completed_at if progress else None,
            }
            # Add total_lessons and completed_lessons for frontend compatibility
            module_data['total_lessons'] = module_data.get('lesson_count', 0)
            module_data['completed_lessons'] = progress.lessons_completed if progress else 0

        return Response(data)


class CurriculumModuleDetailView(APIView):
    """Get module details with lessons."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, child_id=None):
        """Get module detail with lessons and optional progress."""
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        module = get_object_or_404(CurriculumModule, pk=pk)
        serializer = CurriculumModuleDetailSerializer(module)

        # Get module progress if child is provided
        progress_data = {
            'started': False,
            'lessons_completed': 0,
            'total_points': 0,
            'is_complete': False,
            'completed_at': None,
        }
        if child:
            try:
                module_progress = ModuleProgress.objects.get(child=child, module=module)
                progress_data = {
                    'started': True,
                    'lessons_completed': module_progress.lessons_completed,
                    'total_points': module_progress.total_points,
                    'is_complete': module_progress.is_complete,
                    'completed_at': module_progress.completed_at,
                }
            except ModuleProgress.DoesNotExist:
                pass

        # Add total_lessons and completed_lessons for frontend compatibility
        data = serializer.data
        data['total_lessons'] = data.get('lesson_count', 0)
        data['completed_lessons'] = progress_data.get('lessons_completed', 0)

        return Response({
            **data,
            'progress': progress_data,
        })


class LessonListView(APIView):
    """List lessons for a module."""
    permission_classes = [IsAuthenticated]

    def get(self, request, module_id, child_id=None):
        """Get lessons for a module with optional child's progress."""
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        module = get_object_or_404(CurriculumModule, pk=module_id)
        lessons = Lesson.objects.filter(module=module, is_active=True).order_by('order')
        serializer = LessonSerializer(lessons, many=True)

        # Get progress for each lesson if child is provided
        progress_map = {}
        if child:
            progress_map = {
                str(p.lesson_id): p
                for p in LessonProgress.objects.filter(child=child, lesson__module=module)
            }

        data = serializer.data
        for lesson_data in data:
            progress = progress_map.get(lesson_data['id'])
            lesson_data['progress'] = {
                'started': progress is not None,
                'score': progress.score if progress else 0,
                'best_score': progress.best_score if progress else 0,
                'attempts': progress.attempts if progress else 0,
                'is_complete': progress.is_complete if progress else False,
                'completed_at': progress.completed_at if progress else None,
            }

        return Response(data)


class LessonDetailView(APIView):
    """Get lesson details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, child_id=None):
        """Get lesson detail with contents and optional progress."""
        # Try to get child_id from URL param first, then from query param
        if child_id is None:
            child_id = request.query_params.get('child_id')

        child = None
        if child_id:
            try:
                child = Child.objects.get(pk=child_id, user=request.user)
            except Child.DoesNotExist:
                return Response(
                    {'detail': 'Child not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonDetailSerializer(lesson)

        # Get lesson progress if child is provided
        progress_data = {
            'started': False,
            'score': 0,
            'best_score': 0,
            'attempts': 0,
            'is_complete': False,
            'completed_at': None,
        }
        if child:
            try:
                lesson_progress = LessonProgress.objects.get(child=child, lesson=lesson)
                progress_data = {
                    'started': True,
                    'score': lesson_progress.score,
                    'best_score': lesson_progress.best_score,
                    'attempts': lesson_progress.attempts,
                    'is_complete': lesson_progress.is_complete,
                    'completed_at': lesson_progress.completed_at,
                }
            except LessonProgress.DoesNotExist:
                pass

        return Response({
            **serializer.data,
            'progress': progress_data,
        })


class LessonProgressUpdateView(APIView):
    """Update lesson progress."""
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        """Update lesson progress with score.

        child_id should be passed in request body, not URL.
        """
        # Get child_id from request body
        child_id = request.data.get('child_id')
        if not child_id:
            return Response(
                {'detail': 'child_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {'detail': 'Child not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        lesson = get_object_or_404(Lesson, pk=lesson_id)

        serializer = LessonProgressUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get or create lesson progress
        lesson_progress, created = LessonProgress.objects.get_or_create(
            child=child,
            lesson=lesson
        )

        # Update progress
        lesson_progress.update_progress(serializer.validated_data['score'])

        # Calculate points to award
        points_awarded = 0
        if lesson_progress.is_complete:
            # Award points based on score
            base_points = lesson.points_available or 10
            score_multiplier = lesson_progress.best_score / 100
            points_awarded = int(base_points * score_multiplier)

        response_serializer = LessonProgressSerializer(lesson_progress)
        return Response({
            'data': response_serializer.data,
            'points_awarded': points_awarded,
            'message': 'Lesson completed!' if lesson_progress.is_complete else 'Progress saved!'
        })


class ChildLevelProgressView(APIView):
    """Get all level progress for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        """Get all level progress for child."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {'detail': 'Child not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        progress = LevelProgress.objects.filter(child=child).select_related('level')
        serializer = LevelProgressSerializer(progress, many=True)

        return Response({'data': serializer.data})


class ChildHomepageProgressView(APIView):
    """Get homepage-optimized progress summary for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        """Get progress summary for homepage display."""
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {'detail': 'Child not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the user's subscription tier for feature gating
        user = request.user
        is_paid = user.subscription_tier in ['STANDARD', 'PREMIUM']

        # Get current level progress
        current_level = None
        current_module = None
        current_lesson = None
        levels_completed = 0
        total_points = 0

        # Find the child's current active level
        level_progress_list = LevelProgress.objects.filter(
            child=child
        ).select_related('level').order_by('-level__order')

        for lp in level_progress_list:
            if lp.is_complete:
                levels_completed += 1
            total_points += lp.total_points

            if not lp.is_complete and current_level is None:
                current_level = lp.level

        # If no in-progress level found, get the first level
        if current_level is None:
            current_level = CurriculumLevel.objects.filter(is_active=True).order_by('order').first()

        # Find current module and lesson within the level
        if current_level:
            module_progress_list = ModuleProgress.objects.filter(
                child=child,
                module__level=current_level
            ).select_related('module').order_by('module__order')

            for mp in module_progress_list:
                if not mp.is_complete:
                    current_module = mp.module
                    break

            # If no in-progress module, get first module
            if current_module is None:
                current_module = CurriculumModule.objects.filter(
                    level=current_level,
                    is_active=True
                ).order_by('order').first()

            # Find current lesson
            if current_module:
                lesson_progress_list = LessonProgress.objects.filter(
                    child=child,
                    lesson__module=current_module
                ).select_related('lesson').order_by('lesson__order')

                for lsp in lesson_progress_list:
                    if not lsp.is_complete:
                        current_lesson = lsp.lesson
                        break

                if current_lesson is None:
                    current_lesson = Lesson.objects.filter(
                        module=current_module,
                        is_active=True
                    ).order_by('order').first()

        # Build response
        response_data = {
            'child': {
                'id': str(child.id),
                'name': child.name,
                'avatar': child.avatar,
                'level': child.level,
            },
            'summary': {
                'levels_completed': levels_completed,
                'total_points': total_points,
                'current_streak': child.get_current_streak(),
            },
            'current_progress': None,
        }

        # Include curriculum progress for ALL users (paid get full, free get basic)
        if current_level:
            if is_paid:
                # Paid users get full curriculum navigation
                response_data['current_progress'] = {
                    'level': {
                        'id': str(current_level.id),
                        'name': current_level.name_english,
                        'hindi_name': current_level.name_hindi,
                        'order': current_level.order,
                    },
                    'module': {
                        'id': str(current_module.id),
                        'name': current_module.name_english,
                        'hindi_name': current_module.name_hindi,
                        'order': current_module.order,
                    } if current_module else None,
                    'lesson': {
                        'id': str(current_lesson.id),
                        'title': current_lesson.title_english,
                        'hindi_title': current_lesson.title_hindi,
                        'order': current_lesson.order,
                    } if current_lesson else None,
                    'continue_url': f'/learn/lessons/{current_lesson.id}' if current_lesson else f'/learn/levels/{current_level.id}',
                }
            else:
                # Free users get basic navigation (to alphabet or vocabulary)
                response_data['current_progress'] = {
                    'level': {
                        'id': 'free',
                        'name': 'Free Learning',
                        'hindi_name': 'मुफ़्त सीखना',
                        'order': 0,
                    },
                    'module': {
                        'id': 'alphabet',
                        'name': 'Hindi Alphabet',
                        'hindi_name': 'हिंदी वर्णमाला',
                        'order': 1,
                    },
                    'lesson': None,
                    'continue_url': '/learn/alphabet',
                }
                # Also include upgrade prompt
                response_data['upgrade_prompt'] = {
                    'message': 'Unlock structured learning with L1-L10 curriculum!',
                    'cta': 'Upgrade to Standard',
                    'price': 'NZD $20/month',
                }
        else:
            # No levels in database - provide default path
            response_data['current_progress'] = {
                'level': {
                    'id': 'default',
                    'name': 'Start Learning',
                    'hindi_name': 'सीखना शुरू करें',
                    'order': 0,
                },
                'module': None,
                'lesson': None,
                'continue_url': '/learn/alphabet',
            }

        return Response({'data': response_data})
