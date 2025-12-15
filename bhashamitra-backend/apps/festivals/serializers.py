"""Festival serializers."""
from rest_framework import serializers
from apps.festivals.models import Festival, FestivalStory
from apps.stories.serializers import StoryListSerializer


class FestivalSerializer(serializers.ModelSerializer):
    """Serializer for Festival model."""

    class Meta:
        model = Festival
        fields = [
            'id',
            'name',
            'name_native',
            'religion',
            'description',
            'typical_month',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class FestivalDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Festival with related stories."""

    stories = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = [
            'id',
            'name',
            'name_native',
            'religion',
            'description',
            'typical_month',
            'is_active',
            'created_at',
            'stories',
        ]
        read_only_fields = ['id', 'created_at']

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
