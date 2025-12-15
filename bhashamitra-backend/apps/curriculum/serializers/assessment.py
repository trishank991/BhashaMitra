"""Assessment and certificate serializers."""
from rest_framework import serializers
from apps.curriculum.models.assessment import (
    Assessment, AssessmentQuestion, AssessmentAttempt, Certificate
)


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    """Assessment question serializer (without answers)."""

    class Meta:
        model = AssessmentQuestion
        fields = [
            'id', 'question_type', 'skill_tested',
            'question_text', 'options', 'points', 'order'
        ]
        # Note: correct_answer is excluded for security


class AssessmentQuestionDetailSerializer(serializers.ModelSerializer):
    """Detailed question serializer (with answers, for review)."""

    class Meta:
        model = AssessmentQuestion
        fields = [
            'id', 'question_type', 'skill_tested', 'question_text',
            'correct_answer', 'acceptable_answers', 'options',
            'points', 'explanation', 'order'
        ]


class AssessmentSerializer(serializers.ModelSerializer):
    """Basic assessment serializer."""
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            'id', 'name', 'description', 'assessment_type',
            'language', 'level', 'passing_score',
            'time_limit_minutes', 'questions_count', 'question_count',
            'allow_retake', 'is_active'
        ]

    def get_question_count(self, obj):
        return obj.questions.count()


class AssessmentDetailSerializer(serializers.ModelSerializer):
    """Detailed assessment serializer with questions."""
    questions = AssessmentQuestionSerializer(many=True, read_only=True)
    prerequisite = AssessmentSerializer(source='prerequisite_assessment', read_only=True)

    class Meta:
        model = Assessment
        fields = [
            'id', 'name', 'description', 'assessment_type',
            'language', 'level', 'passing_score', 'time_limit_minutes',
            'questions_count', 'randomize_questions', 'show_correct_answers',
            'allow_retake', 'retake_cooldown_hours', 'required_level',
            'prerequisite', 'is_active', 'questions'
        ]


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    """Assessment attempt serializer."""
    assessment = AssessmentSerializer(read_only=True)

    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'assessment', 'score', 'max_score',
            'percentage', 'passed', 'started_at', 'completed_at',
            'time_taken_seconds', 'skill_breakdown'
        ]


class AssessmentAttemptDetailSerializer(serializers.ModelSerializer):
    """Detailed attempt serializer with answers."""
    assessment = AssessmentDetailSerializer(read_only=True)

    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'assessment', 'score', 'max_score',
            'percentage', 'passed', 'started_at', 'completed_at',
            'time_taken_seconds', 'answers', 'skill_breakdown'
        ]


class AssessmentSubmitSerializer(serializers.Serializer):
    """Serializer for submitting assessment answers."""
    answers = serializers.DictField(
        child=serializers.CharField(),
        help_text="Dictionary mapping question_id to answer"
    )


class AssessmentResultSerializer(serializers.Serializer):
    """Serializer for assessment result."""
    attempt_id = serializers.UUIDField()
    score = serializers.IntegerField()
    max_score = serializers.IntegerField()
    percentage = serializers.FloatField()
    passed = serializers.BooleanField()
    passing_score = serializers.IntegerField()
    time_taken_seconds = serializers.IntegerField()
    skill_breakdown = serializers.DictField()
    certificate_id = serializers.CharField(allow_null=True)
    results = serializers.ListField(allow_null=True)


class CertificateSerializer(serializers.ModelSerializer):
    """Certificate serializer."""
    child_name = serializers.CharField(source='child.name', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'certificate_id', 'child_name',
            'certificate_type', 'title', 'description',
            'language', 'level', 'issued_at', 'pdf_url'
        ]


class CertificateDetailSerializer(serializers.ModelSerializer):
    """Detailed certificate serializer."""
    child_name = serializers.CharField(source='child.name', read_only=True)
    assessment_attempt = AssessmentAttemptSerializer(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'certificate_id', 'child_name',
            'certificate_type', 'title', 'description',
            'language', 'level', 'assessment_attempt',
            'issued_at', 'pdf_url'
        ]
