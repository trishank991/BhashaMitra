"""Games serializers."""
from rest_framework import serializers
from apps.curriculum.models.games import Game, GameSession, GameLeaderboard


class GameSerializer(serializers.ModelSerializer):
    """Basic game serializer."""

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'game_type',
            'skill_focus', 'language', 'level',
            'duration_seconds', 'questions_per_round',
            'lives', 'is_premium', 'is_active'
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    """Detailed game serializer with instructions."""

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'instructions',
            'game_type', 'skill_focus', 'language', 'level',
            'duration_seconds', 'questions_per_round', 'lives',
            'points_per_correct', 'bonus_completion',
            'is_premium', 'is_active'
        ]


class GameSessionSerializer(serializers.ModelSerializer):
    """Game session serializer."""
    game = GameSerializer(read_only=True)
    accuracy = serializers.ReadOnlyField()

    class Meta:
        model = GameSession
        fields = [
            'id', 'game', 'score', 'questions_attempted',
            'questions_correct', 'accuracy', 'time_taken_seconds',
            'completed', 'lives_remaining', 'points_earned',
            'created_at'
        ]


class GameSessionCreateSerializer(serializers.Serializer):
    """Serializer for starting a game session."""
    game_id = serializers.UUIDField()


class GameSessionSubmitSerializer(serializers.Serializer):
    """Serializer for submitting game results."""
    score = serializers.IntegerField(min_value=0)
    questions_attempted = serializers.IntegerField(min_value=0)
    questions_correct = serializers.IntegerField(min_value=0)
    time_taken_seconds = serializers.IntegerField(min_value=0)
    completed = serializers.BooleanField()
    lives_remaining = serializers.IntegerField(min_value=0, default=0)


class GameLeaderboardSerializer(serializers.ModelSerializer):
    """Game leaderboard serializer."""
    child_name = serializers.CharField(source='child.name', read_only=True)
    child_avatar = serializers.CharField(source='child.avatar', read_only=True)

    class Meta:
        model = GameLeaderboard
        fields = [
            'id', 'child_name', 'child_avatar',
            'high_score', 'best_accuracy', 'games_played'
        ]


class GlobalLeaderboardSerializer(serializers.Serializer):
    """Serializer for global leaderboard entry."""
    rank = serializers.IntegerField()
    child_id = serializers.UUIDField()
    child_name = serializers.CharField()
    child_avatar = serializers.CharField(allow_null=True)
    total_points = serializers.IntegerField()
    games_played = serializers.IntegerField()
    level = serializers.IntegerField()
