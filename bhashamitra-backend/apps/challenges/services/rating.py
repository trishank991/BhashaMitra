"""ELO-based rating service for competitive challenges."""
import math
from typing import Tuple, Optional
from django.conf import settings
from django.db import transaction

from apps.challenges.models import PlayerRating, RatingHistory, ChallengeAttempt
from apps.children.models import Child


class RatingService:
    """Calculate and update ELO ratings for competitive play."""

    def __init__(self):
        self.config = settings.RATING_CONFIG

    def get_k_factor(self, player_rating: PlayerRating) -> int:
        """Get K-factor based on number of games played."""
        if player_rating.total_matches < self.config['GAMES_THRESHOLD']:
            return self.config['K_FACTOR_NEW']
        return self.config['K_FACTOR_ESTABLISHED']

    def calculate_expected_score(self, player_rating: int, opponent_rating: int) -> float:
        """Calculate expected score (probability of winning)."""
        return 1 / (1 + math.pow(10, (opponent_rating - player_rating) / 400))

    def calculate_rating_change(
        self,
        player_rating: int,
        opponent_rating: int,
        actual_score: float,  # 1 for win, 0 for loss, 0.5 for draw
        k_factor: int
    ) -> int:
        """Calculate rating change based on ELO formula."""
        expected = self.calculate_expected_score(player_rating, opponent_rating)
        change = k_factor * (actual_score - expected)
        return round(change)

    def get_or_create_rating(self, child: Child) -> PlayerRating:
        """Get or create rating for a child."""
        rating, created = PlayerRating.objects.get_or_create(
            child=child,
            defaults={
                'current_rating': self.config['INITIAL_RATING'],
                'highest_rating': self.config['INITIAL_RATING'],
                'lowest_rating': self.config['INITIAL_RATING'],
            }
        )
        return rating

    @transaction.atomic
    def update_ratings_after_match(
        self,
        winner_attempt: ChallengeAttempt,
        loser_attempt: ChallengeAttempt,
        is_draw: bool = False
    ) -> Tuple[Optional[int], Optional[int]]:
        """
        Update ratings after a match.
        Returns (winner_change, loser_change) or (None, None) if guests involved.
        """
        # Skip if either player is a guest (no child associated)
        winner_child = winner_attempt.participant_child
        loser_child = loser_attempt.participant_child

        if not winner_child or not loser_child:
            return None, None

        winner_rating = self.get_or_create_rating(winner_child)
        loser_rating = self.get_or_create_rating(loser_child)

        winner_k = self.get_k_factor(winner_rating)
        loser_k = self.get_k_factor(loser_rating)

        # Calculate changes
        if is_draw:
            winner_score, loser_score = 0.5, 0.5
        else:
            winner_score, loser_score = 1.0, 0.0

        winner_change = self.calculate_rating_change(
            winner_rating.current_rating,
            loser_rating.current_rating,
            winner_score,
            winner_k
        )

        loser_change = self.calculate_rating_change(
            loser_rating.current_rating,
            winner_rating.current_rating,
            loser_score,
            loser_k
        )

        # Store old ratings for history
        winner_old = winner_rating.current_rating
        loser_old = loser_rating.current_rating

        # Update winner
        winner_rating.current_rating += winner_change
        winner_rating.highest_rating = max(winner_rating.highest_rating, winner_rating.current_rating)
        winner_rating.total_matches += 1

        if not is_draw:
            winner_rating.wins += 1
            winner_rating.current_win_streak += 1
            winner_rating.best_win_streak = max(winner_rating.best_win_streak, winner_rating.current_win_streak)
            winner_rating.current_loss_streak = 0

            # Check for underdog win
            if winner_old < loser_old:
                winner_rating.underdog_wins += 1
                if loser_old - winner_old >= 200:
                    winner_rating.giant_slayer_wins += 1
        else:
            winner_rating.draws += 1
            winner_rating.current_win_streak = 0
            winner_rating.current_loss_streak = 0

        winner_rating.save()
        winner_rating.update_rank_title()

        # Update loser
        loser_rating.current_rating += loser_change
        loser_rating.lowest_rating = min(loser_rating.lowest_rating, loser_rating.current_rating)
        loser_rating.total_matches += 1

        if not is_draw:
            loser_rating.losses += 1
            loser_rating.current_loss_streak += 1
            loser_rating.current_win_streak = 0
        else:
            loser_rating.draws += 1
            loser_rating.current_win_streak = 0
            loser_rating.current_loss_streak = 0

        loser_rating.save()
        loser_rating.update_rank_title()

        # Record history
        RatingHistory.objects.create(
            player_rating=winner_rating,
            challenge_attempt=winner_attempt,
            rating_before=winner_old,
            rating_after=winner_rating.current_rating,
            rating_change=winner_change,
            opponent_rating=loser_old,
            is_win=not is_draw,
        )

        RatingHistory.objects.create(
            player_rating=loser_rating,
            challenge_attempt=loser_attempt,
            rating_before=loser_old,
            rating_after=loser_rating.current_rating,
            rating_change=loser_change,
            opponent_rating=winner_old,
            is_win=False,
        )

        return winner_change, loser_change

    def get_rank_title(self, rating: int) -> str:
        """Get rank title for a given rating."""
        titles = self.config['RANK_TITLES']

        for rating_threshold in sorted(titles.keys(), reverse=True):
            if rating >= rating_threshold:
                return titles[rating_threshold]

        return 'Beginner'

    def get_leaderboard(self, language: str = None, limit: int = 50):
        """Get global or language-specific leaderboard."""
        queryset = PlayerRating.objects.select_related('child').filter(
            total_matches__gte=5  # Minimum games to appear
        )

        if language:
            queryset = queryset.filter(child__language=language)

        return queryset.order_by('-current_rating')[:limit]
