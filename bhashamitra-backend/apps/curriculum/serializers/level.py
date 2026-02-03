"""Serializers for curriculum hierarchy (levels, modules, lessons)."""
from rest_framework import serializers
from apps.curriculum.models.level import (
    CurriculumLevel, CurriculumModule, Lesson, LessonContent
)
from apps.curriculum.models.progress import (
    LevelProgress, ModuleProgress, LessonProgress
)


class LessonContentSerializer(serializers.ModelSerializer):
    """Serializer for lesson content links."""

    class Meta:
        model = LessonContent
        fields = [
            'id', 'content_type', 'content_id', 'sequence_order', 'is_required'
        ]


class LessonSerializer(serializers.ModelSerializer):
    """Basic lesson serializer."""

    class Meta:
        model = Lesson
        fields = [
            'id', 'code', 'title_english', 'title_hindi', 'title_romanized',
            'lesson_type', 'description', 'order', 'estimated_minutes',
            'points_available', 'mastery_threshold', 'is_free', 'is_active'
        ]


class LessonDetailSerializer(serializers.ModelSerializer):
    """Detailed lesson serializer with contents and content JSON."""
    contents = LessonContentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'code', 'title_english', 'title_hindi', 'title_romanized',
            'lesson_type', 'description', 'peppi_intro', 'peppi_success', 'content',
            'order', 'estimated_minutes', 'points_available', 'mastery_threshold',
            'is_free', 'is_active', 'contents'
        ]


class CurriculumModuleSerializer(serializers.ModelSerializer):
    """Basic module serializer."""
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumModule
        fields = [
            'id', 'code', 'name_english', 'name_hindi', 'name_romanized',
            'module_type', 'description', 'objectives', 'emoji', 'order',
            'estimated_minutes', 'xp_reward', 'is_active', 'lesson_count'
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.filter(is_active=True).count()


class CurriculumModuleDetailSerializer(serializers.ModelSerializer):
    """Detailed module serializer with lessons."""
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumModule
        fields = [
            'id', 'code', 'name_english', 'name_hindi', 'name_romanized',
            'module_type', 'description', 'objectives', 'peppi_intro', 'peppi_completion',
            'emoji', 'order', 'estimated_minutes', 'xp_reward', 'is_active',
            'lesson_count', 'lessons'
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.filter(is_active=True).count()


class CurriculumLevelSerializer(serializers.ModelSerializer):
    """Basic level serializer."""
    module_count = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumLevel
        fields = [
            'id', 'code', 'name_english', 'name_hindi', 'name_romanized',
            'min_age', 'max_age', 'description', 'emoji', 'theme_color',
            'order', 'estimated_hours', 'min_xp_required', 'xp_reward',
            'is_free', 'is_active', 'module_count'
        ]

    def get_module_count(self, obj):
        return obj.modules.filter(is_active=True).count()


class CurriculumLevelDetailSerializer(serializers.ModelSerializer):
    """Detailed level serializer with modules."""
    modules = CurriculumModuleSerializer(many=True, read_only=True)
    module_count = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumLevel
        fields = [
            'id', 'code', 'name_english', 'name_hindi', 'name_romanized',
            'min_age', 'max_age', 'description', 'learning_objectives',
            'peppi_welcome', 'peppi_completion', 'emoji', 'theme_color',
            'order', 'estimated_hours', 'min_xp_required', 'xp_reward',
            'is_free', 'is_active', 'module_count', 'modules'
        ]

    def get_module_count(self, obj):
        return obj.modules.filter(is_active=True).count()


# Progress Serializers
class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for lesson progress."""
    lesson = LessonSerializer(read_only=True)
    points_awarded = serializers.SerializerMethodField()

    class Meta:
        model = LessonProgress
        fields = [
            'id', 'lesson', 'started_at', 'completed_at', 'score',
            'attempts', 'best_score', 'is_complete', 'points_awarded'
        ]

    def get_points_awarded(self, obj):
        """Calculate points awarded based on completion status."""
        if obj.is_complete:
            return obj.lesson.points_available
        return 0


class ModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for module progress."""
    module = CurriculumModuleSerializer(read_only=True)

    class Meta:
        model = ModuleProgress
        fields = [
            'id', 'module', 'started_at', 'completed_at',
            'lessons_completed', 'total_points', 'is_complete'
        ]


class LevelProgressSerializer(serializers.ModelSerializer):
    """Serializer for level progress."""
    level = CurriculumLevelSerializer(read_only=True)

    class Meta:
        model = LevelProgress
        fields = [
            'id', 'level', 'started_at', 'completed_at',
            'modules_completed', 'total_points', 'is_complete'
        ]


class LessonProgressUpdateSerializer(serializers.Serializer):
    """Serializer for updating lesson progress."""
    score = serializers.IntegerField(min_value=0, max_value=100)
