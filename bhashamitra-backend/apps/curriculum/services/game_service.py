"""Game service for educational games."""
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, Count
from typing import List, Optional
from datetime import date
from apps.curriculum.models.games import Game, GameSession, GameLeaderboard
from apps.children.models import Child


class GameService:
    """Service for managing educational games."""

    @staticmethod
    def get_available_games(language: str, level: int = None) -> List[Game]:
        """Get available games for a language, optionally filtered by level."""
        queryset = Game.objects.filter(
            language=language,
            is_active=True
        )

        if level:
            queryset = queryset.filter(level__lte=level)

        return list(queryset.order_by('level', 'name'))

    @staticmethod
    @transaction.atomic
    def start_game_session(child: Child, game: Game) -> GameSession:
        """Start a new game session."""
        return GameSession.objects.create(
            child=child,
            game=game,
            lives_remaining=game.lives
        )

    @staticmethod
    @transaction.atomic
    def submit_game_session(
        session: GameSession,
        score: int,
        questions_attempted: int,
        questions_correct: int,
        time_taken_seconds: int,
        completed: bool,
        lives_remaining: int = 0
    ) -> dict:
        """
        Submit game session results and update leaderboard.
        """
        game = session.game

        # Calculate points earned
        base_points = questions_correct * game.points_per_correct
        bonus_points = game.bonus_completion if completed else 0
        points_earned = base_points + bonus_points

        # Update session
        session.score = score
        session.questions_attempted = questions_attempted
        session.questions_correct = questions_correct
        session.time_taken_seconds = time_taken_seconds
        session.completed = completed
        session.lives_remaining = lives_remaining
        session.points_earned = points_earned
        session.save()

        # Update child's total points
        session.child.total_points += points_earned
        session.child.save(update_fields=['total_points'])

        # Update leaderboard
        leaderboard, _ = GameLeaderboard.objects.get_or_create(
            game=game,
            child=session.child
        )
        leaderboard.update_from_session(session)

        return {
            'session_id': str(session.id),
            'score': score,
            'accuracy': round((questions_correct / questions_attempted * 100), 1) if questions_attempted else 0,
            'points_earned': points_earned,
            'completed': completed,
            'new_high_score': score > (leaderboard.high_score - score),  # Was this a new high score?
        }

    @staticmethod
    def get_game_leaderboard(game_id: str, limit: int = 10) -> List[dict]:
        """Get leaderboard for a specific game."""
        entries = GameLeaderboard.objects.filter(
            game_id=game_id
        ).select_related('child').order_by('-high_score')[:limit]

        return [{
            'rank': i + 1,
            'child_id': str(entry.child.id),
            'child_name': entry.child.name,
            'child_avatar': entry.child.avatar,
            'high_score': entry.high_score,
            'best_accuracy': round(entry.best_accuracy, 1),
            'games_played': entry.games_played,
        } for i, entry in enumerate(entries)]

    @staticmethod
    def get_global_leaderboard(language: str, limit: int = 10) -> List[dict]:
        """
        Get global leaderboard across all games for a language.
        Ranked by total points.
        """
        # Get children with game sessions in this language
        children_with_games = Child.objects.filter(
            game_sessions__game__language=language
        ).annotate(
            total_game_points=Sum('game_sessions__points_earned'),
            total_games=Count('game_sessions')
        ).order_by('-total_game_points')[:limit]

        return [{
            'rank': i + 1,
            'child_id': str(child.id),
            'child_name': child.name,
            'child_avatar': child.avatar,
            'total_points': child.total_game_points or 0,
            'games_played': child.total_games or 0,
            'level': child.level,
        } for i, child in enumerate(children_with_games)]

    @staticmethod
    def get_child_game_history(child_id: str, game_id: str = None, limit: int = 20) -> List[dict]:
        """Get game history for a child."""
        queryset = GameSession.objects.filter(
            child_id=child_id
        ).select_related('game')

        if game_id:
            queryset = queryset.filter(game_id=game_id)

        sessions = queryset.order_by('-created_at')[:limit]

        return [{
            'session_id': str(session.id),
            'game_name': session.game.name,
            'game_type': session.game.game_type,
            'score': session.score,
            'accuracy': session.accuracy,
            'time_taken_seconds': session.time_taken_seconds,
            'completed': session.completed,
            'points_earned': session.points_earned,
            'played_at': session.created_at.isoformat(),
        } for session in sessions]

    @staticmethod
    def get_child_game_stats(child_id: str, language: str = None) -> dict:
        """Get overall game statistics for a child."""
        queryset = GameSession.objects.filter(child_id=child_id)

        if language:
            queryset = queryset.filter(game__language=language)

        sessions = list(queryset)

        if not sessions:
            return {
                'total_games_played': 0,
                'total_points_earned': 0,
                'total_time_seconds': 0,
                'average_score': 0,
                'average_accuracy': 0,
                'completion_rate': 0,
                'favorite_game': None,
            }

        total_games = len(sessions)
        total_points = sum(s.points_earned for s in sessions)
        total_time = sum(s.time_taken_seconds for s in sessions)
        total_score = sum(s.score for s in sessions)
        total_correct = sum(s.questions_correct for s in sessions)
        total_attempted = sum(s.questions_attempted for s in sessions)
        completed_count = sum(1 for s in sessions if s.completed)

        # Find favorite game (most played)
        game_counts = {}
        for session in sessions:
            game_id = str(session.game_id)
            if game_id not in game_counts:
                game_counts[game_id] = {'count': 0, 'name': session.game.name}
            game_counts[game_id]['count'] += 1

        favorite_game = max(game_counts.values(), key=lambda x: x['count'])['name'] if game_counts else None

        return {
            'total_games_played': total_games,
            'total_points_earned': total_points,
            'total_time_seconds': total_time,
            'average_score': round(total_score / total_games, 1),
            'average_accuracy': round((total_correct / total_attempted * 100), 1) if total_attempted else 0,
            'completion_rate': round((completed_count / total_games * 100), 1),
            'favorite_game': favorite_game,
        }

    @staticmethod
    def get_games_played_today(child_id: str) -> int:
        """Get the number of games played today by a child."""
        today = date.today()
        return GameSession.objects.filter(
            child_id=child_id,
            created_at__date=today
        ).count()

    @staticmethod
    def can_play_more_games(child_id: str, daily_limit: int) -> tuple:
        """
        Check if a child can play more games today based on daily limit.
        Returns (can_play, games_played, games_remaining)
        """
        if daily_limit == -1:  # Unlimited
            return (True, 0, -1)

        games_played = GameService.get_games_played_today(child_id)
        games_remaining = max(0, daily_limit - games_played)
        can_play = games_played < daily_limit

        return (can_play, games_played, games_remaining)

    @staticmethod
    def get_recommended_games(child: Child, language: str, limit: int = 3) -> List[Game]:
        """
        Get recommended games for a child based on their level and history.
        """
        # Get games appropriate for child's level
        available_games = Game.objects.filter(
            language=language,
            is_active=True,
            level__lte=child.level
        )

        # Get games the child has played
        played_game_ids = GameSession.objects.filter(
            child=child,
            game__language=language
        ).values_list('game_id', flat=True).distinct()

        # Prioritize unplayed games at child's level
        unplayed = available_games.exclude(id__in=played_game_ids).order_by('-level')[:limit]

        if unplayed.count() >= limit:
            return list(unplayed)

        # Fill remaining slots with played games (for practice)
        remaining = limit - unplayed.count()
        played = available_games.filter(id__in=played_game_ids).order_by('?')[:remaining]

        return list(unplayed) + list(played)
