"""Festival serializers."""
from rest_framework import serializers
from apps.festivals.models import Festival, FestivalStory, FestivalActivity, FestivalProgress
from apps.stories.serializers import StoryListSerializer


class FestivalActivitySerializer(serializers.ModelSerializer):
    """Serializer for FestivalActivity model."""

    is_age_appropriate = serializers.SerializerMethodField()
    festival_name = serializers.CharField(source='festival.name', read_only=True)

    class Meta:
        model = FestivalActivity
        fields = [
            'id',
            'festival',
            'festival_name',
            'title',
            'activity_type',
            'description',
            'instructions',
            'materials_needed',
            'min_age',
            'max_age',
            'duration_minutes',
            'difficulty_level',
            'points_reward',
            'image_url',
            'video_url',
            'is_active',
            'is_age_appropriate',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'festival_name', 'is_age_appropriate']

    def get_is_age_appropriate(self, obj):
        """Check if activity is appropriate for the child in context."""
        child_age = self.context.get('child_age')
        if child_age is not None:
            return obj.is_age_appropriate(child_age)
        return None


class FestivalProgressSerializer(serializers.ModelSerializer):
    """Serializer for FestivalProgress model."""

    festival_name = serializers.CharField(source='festival.name', read_only=True)
    activity_title = serializers.CharField(source='activity.title', read_only=True, allow_null=True)
    story_title = serializers.CharField(source='story.title', read_only=True, allow_null=True)
    child_name = serializers.CharField(source='child.name', read_only=True)

    class Meta:
        model = FestivalProgress
        fields = [
            'id',
            'child',
            'child_name',
            'festival',
            'festival_name',
            'activity',
            'activity_title',
            'story',
            'story_title',
            'is_completed',
            'completed_at',
            'points_earned',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'completed_at',
            'points_earned',
            'created_at',
            'updated_at',
            'festival_name',
            'activity_title',
            'story_title',
            'child_name',
        ]

    def validate(self, data):
        """Ensure either activity or story is provided."""
        if not data.get('activity') and not data.get('story'):
            raise serializers.ValidationError(
                "Either activity or story must be provided."
            )
        return data


class FestivalSerializer(serializers.ModelSerializer):
    """Serializer for Festival model."""

    localized_name = serializers.SerializerMethodField()
    activity_count = serializers.SerializerMethodField()
    story_count = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = [
            'id',
            'name',
            'name_native',
            'name_hindi',
            'name_tamil',
            'name_gujarati',
            'name_punjabi',
            'name_telugu',
            'name_malayalam',
            'localized_name',
            'religion',
            'description',
            'significance',
            'typical_month',
            'is_lunar_calendar',
            'image_url',
            'is_active',
            'activity_count',
            'story_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'localized_name', 'activity_count', 'story_count']

    def get_localized_name(self, obj):
        """Get festival name in user's preferred language."""
        child_language = self.context.get('child_language')
        if child_language:
            return obj.get_name_for_language(child_language)
        return obj.name

    def get_activity_count(self, obj):
        """Get count of active activities for this festival."""
        return obj.activities.filter(is_active=True).count()

    def get_story_count(self, obj):
        """Get count of stories linked to this festival."""
        return obj.festival_stories.count()


class FestivalDetailSerializer(FestivalSerializer):
    """Detailed serializer for Festival with related stories and activities."""

    stories = serializers.SerializerMethodField()
    activities = FestivalActivitySerializer(many=True, read_only=True)

    class Meta(FestivalSerializer.Meta):
        fields = FestivalSerializer.Meta.fields + ['stories', 'activities']

    def get_stories(self, obj):
        """Get stories linked to this festival."""
        festival_stories = obj.festival_stories.select_related('story').all()
        return [{
            'story': StoryListSerializer(fs.story).data,
            'is_primary': fs.is_primary,
        } for fs in festival_stories]


class FestivalStorySerializer(serializers.ModelSerializer):
    """Serializer for FestivalStory junction model."""

    festival = FestivalSerializer(read_only=True)
    story = StoryListSerializer(read_only=True)
    festival_id = serializers.UUIDField(write_only=True)
    story_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = FestivalStory
        fields = [
            'id',
            'festival',
            'story',
            'festival_id',
            'story_id',
            'is_primary',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a festival-story link."""
        from apps.festivals.models import Festival
        from apps.stories.models import Story

        festival = Festival.objects.get(id=validated_data['festival_id'])
        story = Story.objects.get(id=validated_data['story_id'])

        return FestivalStory.objects.create(
            festival=festival,
            story=story,
            is_primary=validated_data.get('is_primary', False)
        )
