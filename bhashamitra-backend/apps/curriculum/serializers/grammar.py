"""Grammar serializers."""
from rest_framework import serializers
from apps.curriculum.models.grammar import GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress


class GrammarExerciseSerializer(serializers.ModelSerializer):
    """Grammar exercise serializer."""

    class Meta:
        model = GrammarExercise
        fields = [
            'id', 'exercise_type', 'question', 'options',
            'hint', 'difficulty', 'points', 'order'
        ]
        # Note: correct_answer and acceptable_answers are excluded for security


class GrammarExerciseDetailSerializer(serializers.ModelSerializer):
    """Detailed exercise serializer (for after answering)."""

    class Meta:
        model = GrammarExercise
        fields = [
            'id', 'exercise_type', 'question', 'correct_answer',
            'acceptable_answers', 'options', 'hint', 'explanation',
            'difficulty', 'points', 'order'
        ]


class GrammarRuleSerializer(serializers.ModelSerializer):
    """Grammar rule serializer."""
    exercise_count = serializers.SerializerMethodField()

    class Meta:
        model = GrammarRule
        fields = [
            'id', 'title', 'explanation', 'explanation_simple',
            'formula', 'examples', 'exceptions', 'tips',
            'order', 'exercise_count'
        ]

    def get_exercise_count(self, obj):
        return obj.exercises.count()


class GrammarRuleDetailSerializer(serializers.ModelSerializer):
    """Detailed rule serializer with exercises."""
    exercises = GrammarExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarRule
        fields = [
            'id', 'title', 'explanation', 'explanation_simple',
            'formula', 'examples', 'exceptions', 'tips',
            'order', 'exercises'
        ]


class GrammarTopicSerializer(serializers.ModelSerializer):
    """Basic grammar topic serializer."""
    rule_count = serializers.SerializerMethodField()

    class Meta:
        model = GrammarTopic
        fields = [
            'id', 'language', 'name', 'name_native',
            'description', 'description_simple', 'level',
            'order', 'is_active', 'rule_count'
        ]

    def get_rule_count(self, obj):
        return obj.rules.count()


class GrammarTopicDetailSerializer(serializers.ModelSerializer):
    """Detailed topic serializer with rules."""
    rules = GrammarRuleSerializer(many=True, read_only=True)
    prerequisites = GrammarTopicSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarTopic
        fields = [
            'id', 'language', 'name', 'name_native',
            'description', 'description_simple', 'level',
            'order', 'is_active', 'prerequisites', 'rules'
        ]


class GrammarProgressSerializer(serializers.ModelSerializer):
    """Grammar progress serializer."""
    topic = GrammarTopicSerializer(read_only=True)
    accuracy = serializers.ReadOnlyField()

    class Meta:
        model = GrammarProgress
        fields = [
            'id', 'topic', 'exercises_attempted', 'exercises_correct',
            'accuracy', 'mastered', 'mastered_at'
        ]


class ExerciseSubmitSerializer(serializers.Serializer):
    """Serializer for submitting exercise answer."""
    answer = serializers.CharField()


class ExerciseResultSerializer(serializers.Serializer):
    """Serializer for exercise result."""
    is_correct = serializers.BooleanField()
    correct_answer = serializers.CharField()
    explanation = serializers.CharField(allow_blank=True)
    points = serializers.IntegerField()
