"""Scoring engine for challenges with multipliers and bonuses."""
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from django.conf import settings


class ScoringEngine:
    """Calculate scores with time, difficulty, streak multipliers and underdog bonuses."""

    def __init__(self):
        self.config = settings.SCORING_CONFIG

    def calculate_time_multiplier(self, answer_time_seconds: float) -> Decimal:
        """Calculate multiplier based on answer speed."""
        time_config = self.config['TIME_MULTIPLIER']

        if answer_time_seconds <= time_config['FAST']['max_seconds']:
            return Decimal(str(time_config['FAST']['multiplier']))
        elif answer_time_seconds <= time_config['NORMAL']['max_seconds']:
            return Decimal(str(time_config['NORMAL']['multiplier']))
        elif answer_time_seconds <= time_config['SLOW']['max_seconds']:
            return Decimal(str(time_config['SLOW']['multiplier']))
        else:
            return Decimal(str(time_config['VERY_SLOW']['multiplier']))

    def calculate_difficulty_multiplier(self, difficulty: str) -> Decimal:
        """Calculate multiplier based on challenge difficulty."""
        multipliers = self.config['DIFFICULTY_MULTIPLIER']
        return Decimal(str(multipliers.get(difficulty.lower(), 1.0)))

    def calculate_streak_multiplier(self, consecutive_correct: int) -> Decimal:
        """Calculate multiplier based on consecutive correct answers."""
        if consecutive_correct < 2:
            return Decimal('1.0')

        streak_config = self.config['STREAK_MULTIPLIER']

        if consecutive_correct <= streak_config['LOW']['max']:
            return Decimal(str(streak_config['LOW']['multiplier']))
        elif consecutive_correct <= streak_config['MEDIUM']['max']:
            return Decimal(str(streak_config['MEDIUM']['multiplier']))
        else:
            return Decimal(str(streak_config['HIGH']['multiplier']))

    def calculate_underdog_bonus(
        self,
        player_rating: int,
        opponent_rating: int,
        player_won: bool
    ) -> Tuple[Decimal, int]:
        """
        Calculate underdog bonus when lower-rated player beats higher-rated.
        Returns (score_multiplier_bonus, flat_bonus_points)
        """
        if not player_won or player_rating >= opponent_rating:
            return Decimal('0'), 0

        rating_diff = opponent_rating - player_rating

        # Determine level difference based on rating ranges (200 points per level)
        level_diff = min(rating_diff // 200 + 1, 3)

        bonus_config = self.config['UNDERDOG_BONUS'].get(level_diff, {})
        score_bonus = Decimal(str(bonus_config.get('score_bonus', 0)))
        points_bonus = bonus_config.get('points', 0)

        return score_bonus, points_bonus

    def calculate_answer_score(
        self,
        base_points: int,
        answer_time_seconds: float,
        difficulty: str,
        consecutive_correct: int,
        is_correct: bool,
        is_first_attempt: bool = True
    ) -> Dict:
        """Calculate score for a single answer."""
        if not is_correct:
            return {
                'base_points': 0,
                'time_multiplier': Decimal('1.0'),
                'difficulty_multiplier': Decimal('1.0'),
                'streak_multiplier': Decimal('1.0'),
                'first_attempt_bonus': 0,
                'final_points': 0,
            }

        time_mult = self.calculate_time_multiplier(answer_time_seconds)
        diff_mult = self.calculate_difficulty_multiplier(difficulty)
        streak_mult = self.calculate_streak_multiplier(consecutive_correct)

        first_attempt_bonus = self.config['FIRST_ATTEMPT_BONUS'] if is_first_attempt else 0

        # Calculate final points
        multiplied_points = Decimal(str(base_points)) * time_mult * diff_mult * streak_mult
        final_points = int(multiplied_points) + first_attempt_bonus

        return {
            'base_points': base_points,
            'time_multiplier': float(time_mult),
            'difficulty_multiplier': float(diff_mult),
            'streak_multiplier': float(streak_mult),
            'first_attempt_bonus': first_attempt_bonus,
            'final_points': final_points,
        }

    def calculate_challenge_score(
        self,
        answers: List[Dict],
        difficulty: str,
        opponent_rating: Optional[int] = None,
        player_rating: Optional[int] = None,
        player_won: bool = False
    ) -> Dict:
        """
        Calculate total score for a completed challenge.

        answers format: [
            {"correct": bool, "time_seconds": float, "points": int},
            ...
        ]
        """
        total_score = 0
        correct_count = 0
        consecutive_correct = 0
        max_streak = 0
        answer_details = []

        for answer in answers:
            if answer.get('correct', False):
                consecutive_correct += 1
                correct_count += 1
                max_streak = max(max_streak, consecutive_correct)
            else:
                consecutive_correct = 0

            score_detail = self.calculate_answer_score(
                base_points=answer.get('points', self.config['CORRECT_ANSWER']),
                answer_time_seconds=answer.get('time_seconds', 30),
                difficulty=difficulty,
                consecutive_correct=consecutive_correct,
                is_correct=answer.get('correct', False),
            )

            total_score += score_detail['final_points']
            answer_details.append(score_detail)

        # Challenge completion bonus
        completion_bonus = self.config['CHALLENGE_COMPLETE']

        # Perfect round bonus
        is_perfect = correct_count == len(answers) and len(answers) > 0
        perfect_bonus = self.config['PERFECT_ROUND'] if is_perfect else 0

        # Underdog bonus
        underdog_score_bonus = Decimal('0')
        underdog_points_bonus = 0
        if opponent_rating and player_rating:
            underdog_score_bonus, underdog_points_bonus = self.calculate_underdog_bonus(
                player_rating, opponent_rating, player_won
            )

        # Apply underdog bonus to total
        if underdog_score_bonus > 0:
            total_score = int(Decimal(str(total_score)) * (1 + underdog_score_bonus))
        total_score += underdog_points_bonus

        final_score = total_score + completion_bonus + perfect_bonus

        # Calculate average multipliers
        if answer_details:
            avg_time_mult = sum(d['time_multiplier'] for d in answer_details) / len(answer_details)
        else:
            avg_time_mult = 1.0

        return {
            'base_score': total_score,
            'completion_bonus': completion_bonus,
            'perfect_bonus': perfect_bonus,
            'underdog_bonus': underdog_points_bonus,
            'final_score': final_score,
            'correct_answers': correct_count,
            'total_questions': len(answers),
            'accuracy': round((correct_count / len(answers) * 100), 1) if answers else 0,
            'max_streak': max_streak,
            'is_perfect': is_perfect,
            'answer_details': answer_details,
            'avg_time_multiplier': avg_time_mult,
            'difficulty_multiplier': float(self.calculate_difficulty_multiplier(difficulty)),
        }
