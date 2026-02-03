"""Educational games models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Game(TimeStampedModel):
    """Educational game definition."""

    class GameType(models.TextChoices):
        MEMORY = 'MEMORY', 'Memory Match'
        WORDSEARCH = 'WORDSEARCH', 'Word Search'
        HANGMAN = 'HANGMAN', 'Hangman'
        QUIZ = 'QUIZ', 'Quiz Challenge'
        DRAGDROP = 'DRAGDROP', 'Drag and Drop'
        LISTENING = 'LISTENING', 'Listening Challenge'
        SPEED = 'SPEED', 'Speed Round'
        BUILDER = 'BUILDER', 'Word Builder'
        JUMBLE = 'JUMBLE', 'Sentence Jumble'
        PICTURE = 'PICTURE', 'Picture Match'

    class SkillFocus(models.TextChoices):
        ALPHABET = 'ALPHABET', 'Alphabet Recognition'
        VOCABULARY = 'VOCAB', 'Vocabulary'
        GRAMMAR = 'GRAMMAR', 'Grammar'
        LISTENING = 'LISTENING', 'Listening'
        READING = 'READING', 'Reading'
        SPELLING = 'SPELLING', 'Spelling'
        MIXED = 'MIXED', 'Mixed Skills'

    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    game_type = models.CharField(max_length=20, choices=GameType.choices)
    skill_focus = models.CharField(max_length=20, choices=SkillFocus.choices)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    duration_seconds = models.IntegerField(default=300)
    questions_per_round = models.IntegerField(default=10)
    lives = models.IntegerField(default=3)
    points_per_correct = models.IntegerField(default=10)
    bonus_completion = models.IntegerField(default=50)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'games'
        ordering = ['level', 'name']


class GameSession(TimeStampedModel):
    """Record of a game play session."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    score = models.IntegerField(default=0)
    questions_attempted = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    lives_remaining = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)

    class Meta:
        db_table = 'game_sessions'

    @property
    def accuracy(self) -> float:
        return (self.questions_correct / self.questions_attempted * 100) if self.questions_attempted else 0.0


class GameLeaderboard(TimeStampedModel):
    """Leaderboard entries."""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='leaderboard')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='leaderboard_entries')
    high_score = models.IntegerField(default=0)
    best_accuracy = models.FloatField(default=0)
    games_played = models.IntegerField(default=0)

    class Meta:
        db_table = 'game_leaderboard'
        unique_together = ['game', 'child']
        ordering = ['-high_score']

    def update_from_session(self, session: GameSession):
        self.games_played += 1
        if session.score > self.high_score:
            self.high_score = session.score
        if session.accuracy > self.best_accuracy:
            self.best_accuracy = session.accuracy
        self.save()
