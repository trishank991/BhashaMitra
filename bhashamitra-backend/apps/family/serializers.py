"""Serializers for family API."""
from rest_framework import serializers
from django.utils import timezone
from .models import Family, FamilyMembership, FamilyLeaderboard, CurriculumChallenge, CurriculumChallengeParticipant, CurriculumChallengeAttempt


class FamilyMembershipSerializer(serializers.ModelSerializer):
    """Serializer for family membership."""
    child_name = serializers.CharField(source='child.name', read_only=True)
    child_avatar = serializers.URLField(source='child.avatar_url', read_only=True)
    child_level = serializers.IntegerField(source='child.level', read_only=True)

    class Meta:
        model = FamilyMembership
        fields = [
            'id', 'child', 'child_name', 'child_avatar', 'child_level',
            'role', 'joined_at', 'is_active'
        ]


class FamilySerializer(serializers.ModelSerializer):
    """Serializer for Family model."""
    primary_parent_email = serializers.EmailField(source='primary_parent.email', read_only=True)
    children_count = serializers.SerializerMethodField()
    invite_code_valid = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Family
        fields = [
            'id', 'name', 'primary_parent', 'primary_parent_email',
            'invite_code', 'invite_code_expires_at', 'invite_code_valid',
            'discount_tier', 'total_children', 'children_count',
            'collective_points', 'created_at', 'children'
        ]
        read_only_fields = ['id', 'primary_parent', 'collective_points', 'created_at']

    def get_children_count(self, obj):
        return obj.total_children

    def get_invite_code_valid(self, obj):
        return obj.is_invite_code_valid()

    def get_children(self, obj):
        from apps.children.serializers import ChildProfileSerializer
        children = obj.get_children()
        return ChildProfileSerializer(children, many=True).data


class FamilyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a family."""

    class Meta:
        model = Family
        fields = ['name']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['primary_parent'] = request.user
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class FamilyDetailSerializer(serializers.ModelSerializer):
    """Detailed family serializer with all info."""
    primary_parent_email = serializers.EmailField(source='primary_parent.email', read_only=True)
    invite_code_valid = serializers.SerializerMethodField()
    children_data = serializers.SerializerMethodField()

    class Meta:
        model = Family
        fields = [
            'id', 'name', 'primary_parent', 'primary_parent_email',
            'invite_code', 'invite_code_expires_at', 'invite_code_valid',
            'discount_tier', 'total_children', 'collective_points',
            'created_at', 'children_data'
        ]

    def get_invite_code_valid(self, obj):
        return obj.is_invite_code_valid()

    def get_children_data(self, obj):
        from apps.children.serializers import ChildProfileSerializer
        children = obj.get_children()
        return ChildProfileSerializer(children, many=True).data


class CurriculumChallengeParticipantSerializer(serializers.ModelSerializer):
    """Serializer for challenge participant."""
    child_name = serializers.CharField(source='child.name', read_only=True)
    child_avatar = serializers.URLField(source='child.avatar_url', read_only=True)

    class Meta:
        model = CurriculumChallengeParticipant
        fields = [
            'id', 'child', 'child_name', 'child_avatar',
            'completed_count', 'correct_count', 'accuracy_score',
            'best_accuracy', 'started_at', 'completed_at'
        ]


class CurriculumChallengeAttemptSerializer(serializers.ModelSerializer):
    """Serializer for challenge attempt."""
    child_name = serializers.CharField(source='participant.child.name', read_only=True)

    class Meta:
        model = CurriculumChallengeAttempt
        fields = [
            'id', 'item_type', 'item_id', 'item_value',
            'user_answer', 'is_correct', 'audio_url',
            'transcription', 'accuracy_score', 'created_at', 'child_name'
        ]


class CurriculumChallengeSerializer(serializers.ModelSerializer):
    """Serializer for curriculum challenges."""
    challenge_type_display = serializers.CharField(source='get_challenge_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    participants_data = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True, allow_null=True)

    class Meta:
        model = CurriculumChallenge
        fields = [
            'id', 'title', 'description', 'challenge_type', 'challenge_type_display',
            'difficulty', 'difficulty_display', 'min_level', 'max_level',
            'custom_words', 'target_count', 'status', 'status_display',
            'start_date', 'end_date', 'is_active', 'winner', 'winner_name',
            'created_by', 'created_by_name', 'created_at', 'participants_data'
        ]

    def get_participants_data(self, obj):
        participants = obj.participants.all()
        return CurriculumChallengeParticipantSerializer(participants, many=True).data

    def get_is_active(self, obj):
        return obj.is_active()


class CurriculumChallengeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating curriculum challenges."""
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        help_text='List of child IDs to participate'
    )

    class Meta:
        model = CurriculumChallenge
        fields = [
            'title', 'description', 'challenge_type', 'difficulty',
            'min_level', 'max_level', 'custom_words', 'target_count',
            'start_date', 'end_date', 'participant_ids'
        ]

    def validate(self, data):
        """Validate challenge dates and types."""
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        
        challenge_type = data.get('challenge_type')
        custom_words = data.get('custom_words', [])
        
        if challenge_type in ['MIMIC_PRONUNCIATION', 'DICTATION']:
            if not custom_words:
                raise serializers.ValidationError({
                    'custom_words': 'Custom words are required for pronunciation and dictation challenges'
                })
        
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        participant_ids = validated_data.pop('participant_ids', [])
        
        validated_data['created_by'] = request.user
        validated_data['family'] = self.context.get('family')
        
        challenge = CurriculumChallenge.objects.create(**validated_data)
        
        # Add participants
        from apps.children.models import Child
        for child_id in participant_ids:
            try:
                child = Child.objects.get(id=child_id, family=challenge.family)
                CurriculumChallengeParticipant.objects.create(
                    challenge=challenge,
                    child=child
                )
            except Child.DoesNotExist:
                pass
        
        return challenge


class CurriculumChallengeDetailSerializer(serializers.ModelSerializer):
    """Detailed challenge serializer with questions/preview."""
    challenge_type_display = serializers.CharField(source='get_challenge_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    participants_data = CurriculumChallengeParticipantSerializer(many=True, read_only=True)
    is_active = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    can_complete = serializers.SerializerMethodField()
    preview_questions = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumChallenge
        fields = [
            'id', 'title', 'description', 'challenge_type', 'challenge_type_display',
            'difficulty', 'difficulty_display', 'min_level', 'max_level',
            'custom_words', 'target_count', 'status', 'status_display',
            'start_date', 'end_date', 'is_active', 'is_expired', 'can_complete',
            'winner', 'created_by', 'created_at', 'participants_data', 'preview_questions'
        ]

    def get_is_active(self, obj):
        return obj.is_active()

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_can_complete(self, obj):
        return obj.can_be_completed()

    def get_preview_questions(self, obj):
        """Generate preview questions based on challenge type."""
        from .services import CurriculumChallengeService
        questions = CurriculumChallengeService.generate_preview_questions(obj)
        return questions


class ChallengeSubmitAnswerSerializer(serializers.Serializer):
    """Serializer for submitting challenge answers."""
    child_id = serializers.UUIDField()
    item_type = serializers.ChoiceField(choices=[
        ('ALPHABET', 'Alphabet'),
        ('VOCABULARY', 'Vocabulary'),
        ('SENTENCE', 'Sentence'),
        ('PRONUNCIATION', 'Pronunciation'),
        ('DICTATION', 'Dictation'),
    ])
    item_id = serializers.CharField(max_length=100)
    item_value = serializers.CharField()
    user_answer = serializers.CharField(required=False, allow_blank=True)
    audio_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    transcription = serializers.CharField(required=False, allow_blank=True)


class ChallengeResultSerializer(serializers.Serializer):
    """Serializer for challenge result."""
    is_correct = serializers.BooleanField()
    accuracy_score = serializers.FloatField()
    current_progress = CurriculumChallengeParticipantSerializer()
    is_complete = serializers.BooleanField()
    message = serializers.CharField()
