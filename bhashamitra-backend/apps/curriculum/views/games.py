"""Games views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from apps.curriculum.models.games import Game, GameSession
from apps.curriculum.serializers.games import (
    GameSerializer,
    GameDetailSerializer,
    GameSessionSerializer,
    GameLeaderboardSerializer,
)
from apps.curriculum.services.game_service import GameService
from apps.users.tier_config import get_daily_game_limit
from apps.core.validators import safe_level, safe_limit


class GameListView(APIView):
    """List available games for all tiers (with daily limits for FREE)."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get subscription tier and daily limit
        subscription_tier = getattr(request.user, 'subscription_tier', 'FREE')
        daily_limit = get_daily_game_limit(subscription_tier)

        # Check daily games remaining (for FREE tier)
        can_play, games_played, games_remaining = GameService.can_play_more_games(
            str(child.id), daily_limit
        )

        language = request.query_params.get('language', child.language)
        level = request.query_params.get('level', child.level)
        game_type = request.query_params.get('game_type')
        skill_focus = request.query_params.get('skill_focus')

        games = GameService.get_available_games(language, safe_level(level, default=child.level))

        if game_type:
            games = [g for g in games if g.game_type == game_type]
        if skill_focus:
            games = [g for g in games if g.skill_focus == skill_focus]

        serializer = GameSerializer(games, many=True)

        # Add recommended games
        recommended = GameService.get_recommended_games(child, language, limit=3)
        recommended_serializer = GameSerializer(recommended, many=True)

        return Response({
            'data': serializer.data,
            'meta': {
                'recommended': recommended_serializer.data,
                'access_restricted': False,
                'subscription_tier': subscription_tier,
                'daily_limit': daily_limit,
                'games_played_today': games_played,
                'games_remaining_today': games_remaining,
                'can_play_more': can_play,
            }
        })


class GameDetailView(APIView):
    """Get game details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({'detail': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameDetailSerializer(game)
        data = serializer.data

        # Get child's stats for this game
        stats = GameService.get_child_game_history(str(child.id), str(pk), limit=5)
        data['recent_sessions'] = stats

        # Get leaderboard position
        leaderboard = GameService.get_game_leaderboard(str(pk), limit=100)
        child_rank = None
        for entry in leaderboard:
            if entry['child_id'] == str(child.id):
                child_rank = entry['rank']
                break

        data['child_rank'] = child_rank

        return Response({'data': data})


class GameStartView(APIView):
    """Start a new game session (all tiers with daily limits)."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get subscription tier and daily limit
        subscription_tier = getattr(request.user, 'subscription_tier', 'FREE')
        daily_limit = get_daily_game_limit(subscription_tier)

        # Check if daily limit reached (for FREE tier)
        can_play, games_played, games_remaining = GameService.can_play_more_games(
            str(child.id), daily_limit
        )

        if not can_play:
            return Response({
                'detail': f'Daily game limit reached ({daily_limit} games per day for Free tier). Upgrade to unlock unlimited games!',
                'error_code': 'daily_limit_reached',
                'subscription_tier': subscription_tier,
                'games_played_today': games_played,
                'daily_limit': daily_limit,
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({'detail': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

        session = GameService.start_game_session(child, game)
        serializer = GameSessionSerializer(session)

        return Response({
            'data': serializer.data,
            'meta': {
                'game_config': {
                    'duration_seconds': game.duration_seconds,
                    'questions_per_round': game.questions_per_round,
                    'lives': game.lives,
                    'points_per_correct': game.points_per_correct,
                    'bonus_completion': game.bonus_completion,
                },
                'games_remaining_today': games_remaining - 1 if games_remaining != -1 else -1,
            }
        }, status=status.HTTP_201_CREATED)


class GameSubmitView(APIView):
    """Submit game results."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        session_id = request.data.get('session_id')
        if not session_id:
            return Response(
                {'detail': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = GameSession.objects.get(pk=session_id, child=child, game_id=pk)
        except GameSession.DoesNotExist:
            return Response({'detail': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if already submitted
        if session.completed or session.score > 0:
            return Response(
                {'detail': 'Session already submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = GameService.submit_game_session(
            session=session,
            score=request.data.get('score', 0),
            questions_attempted=request.data.get('questions_attempted', 0),
            questions_correct=request.data.get('questions_correct', 0),
            time_taken_seconds=request.data.get('time_taken_seconds', 0),
            completed=request.data.get('completed', False),
            lives_remaining=request.data.get('lives_remaining', 0),
        )

        return Response({'data': result})


class GameLeaderboardView(APIView):
    """Get leaderboard for a game."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        limit = safe_limit(request.query_params.get('limit'), default=10, max_limit=100)
        leaderboard = GameService.get_game_leaderboard(str(pk), limit)

        return Response({'data': leaderboard})


class GlobalLeaderboardView(APIView):
    """Get global leaderboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)
        limit = safe_limit(request.query_params.get('limit'), default=10, max_limit=100)

        leaderboard = GameService.get_global_leaderboard(language, limit)

        return Response({'data': leaderboard})


class GameHistoryView(APIView):
    """Get game history for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        game_id = request.query_params.get('game_id')
        limit = safe_limit(request.query_params.get('limit'), default=20, max_limit=100)

        history = GameService.get_child_game_history(str(child.id), game_id, limit)
        stats = GameService.get_child_game_stats(str(child.id))

        return Response({
            'data': history,
            'meta': {'stats': stats}
        })
