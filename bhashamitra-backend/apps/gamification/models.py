"""Gamification models for BhashaMitra."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


# ===========================================
# ENUMS / CHOICES
# ===========================================

class Language(models.TextChoices):
    """Supported languages."""
    HINDI = 'HINDI', 'Hindi'
    TAMIL = 'TAMIL', 'Tamil'
    GUJARATI = 'GUJARATI', 'Gujarati'
    PUNJABI = 'PUNJABI', 'Punjabi'
    TELUGU = 'TELUGU', 'Telugu'
    MALAYALAM = 'MALAYALAM', 'Malayalam'
    FIJI_HINDI = 'FIJI_HINDI', 'Fiji Hindi'


class OutfitCategory(models.TextChoices):
    """Outfit categories."""
    TRADITIONAL = 'traditional', 'Traditional'
    FESTIVE = 'festive', 'Festive'
    DANCE = 'dance', 'Dance'
    SILLY = 'silly', 'Silly'
    LEGENDARY = 'legendary', 'Legendary'
    ACCESSORY = 'accessory', 'Accessory'


class Rarity(models.TextChoices):
    """Item rarity levels."""
    COMMON = 'common', 'Common'
    UNCOMMON = 'uncommon', 'Uncommon'
    RARE = 'rare', 'Rare'
    EPIC = 'epic', 'Epic'
    LEGENDARY = 'legendary', 'Legendary'


class UnlockType(models.TextChoices):
    """How items are unlocked."""
    DEFAULT = 'default', 'Default (Available from Start)'
    STREAK_DAYS = 'streak_days', 'Streak Days'
    STORIES_COMPLETED = 'stories_completed', 'Stories Completed'
    VOCABULARY_MASTERED = 'vocabulary_mastered', 'Vocabulary Mastered'
    LEVEL = 'level', 'Level Reached'
    PERFECT_SCORES = 'perfect_scores', 'Perfect Scores'
    FESTIVAL = 'festival', 'Festival Event'
    LANGUAGE_SPECIFIC = 'language_specific', 'Language-Specific Achievement'
    RECORDINGS = 'recordings', 'Voice Recordings'
    GAMES_WON = 'games_won', 'Games Won'
    BADGES_EARNED = 'badges_earned', 'Badges Earned'
    ALPHABET_MASTERED = 'alphabet_mastered', 'Alphabet Mastered'
    SPECIAL_EVENT = 'special_event', 'Special Event'


class PeppiEvolutionStage(models.TextChoices):
    """Peppi's evolution stages."""
    KITTEN = 'kitten', 'Kitten'
    YOUNG_CAT = 'young_cat', 'Young Cat'
    ADULT_CAT = 'adult_cat', 'Adult Cat'
    WISE_CAT = 'wise_cat', 'Wise Cat'


class PeppiMood(models.TextChoices):
    """Peppi's mood states."""
    ECSTATIC = 'ecstatic', 'Ecstatic'
    HAPPY = 'happy', 'Happy'
    CONTENT = 'content', 'Content'
    BORED = 'bored', 'Bored'
    SAD = 'sad', 'Sad'
    CRYING = 'crying', 'Crying'


class AccessorySlot(models.TextChoices):
    """Accessory equipment slots."""
    HEAD = 'head', 'Head'
    NECK = 'neck', 'Neck'
    PAWS = 'paws', 'Paws'
    TAIL = 'tail', 'Tail'
    BACKGROUND = 'background', 'Background'


# Note: PeppiPhrase model exists in apps.curriculum.models.peppi
# Note: Festival model exists in apps.festivals.models


class ChallengeType(models.TextChoices):
    """Daily challenge types."""
    STORY_READ = 'story_read', 'Read Stories'
    VOCABULARY = 'vocabulary', 'Learn Vocabulary'
    VOICE_RECORD = 'voice_record', 'Voice Recording'
    GAME_PLAY = 'game_play', 'Play Games'
    PERFECT_LESSON = 'perfect_lesson', 'Perfect Lesson'
    STREAK = 'streak', 'Maintain Streak'


class ChallengeDifficulty(models.TextChoices):
    """Challenge difficulty levels."""
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'


class Badge(TimeStampedModel):
    """Achievement badges."""

    class CriteriaType(models.TextChoices):
        # Existing criteria
        STORIES_COMPLETED = 'STORIES_COMPLETED', 'Stories Completed'
        STREAK_DAYS = 'STREAK_DAYS', 'Streak Days'
        POINTS_EARNED = 'POINTS_EARNED', 'Points Earned'
        TIME_SPENT_MINUTES = 'TIME_SPENT_MINUTES', 'Time Spent'
        VOICE_RECORDINGS = 'VOICE_RECORDINGS', 'Voice Recordings'
        LETTERS_MASTERED = 'LETTERS_MASTERED', 'Letters Mastered'
        WORDS_MASTERED = 'WORDS_MASTERED', 'Words Mastered'

        # NEW: Challenge criteria
        CHALLENGES_COMPLETED = 'CHALLENGES_COMPLETED', 'Challenges Completed'
        CHALLENGES_WON = 'CHALLENGES_WON', 'Challenges Won'
        CHALLENGE_WIN_STREAK = 'CHALLENGE_WIN_STREAK', 'Challenge Win Streak'
        PERFECT_CHALLENGES = 'PERFECT_CHALLENGES', 'Perfect Challenges'
        UNDERDOG_WINS = 'UNDERDOG_WINS', 'Underdog Wins'
        GIANT_SLAYER = 'GIANT_SLAYER', 'Giant Slayer Wins'

        # NEW: Social criteria
        FRIENDS_INVITED = 'FRIENDS_INVITED', 'Friends Invited'
        FRIENDS_CONVERTED = 'FRIENDS_CONVERTED', 'Friends Converted to Users'
        MULTIPLAYER_GAMES = 'MULTIPLAYER_GAMES', 'Multiplayer Games'

        # NEW: Skill-based criteria
        RATING_ACHIEVED = 'RATING_ACHIEVED', 'Rating Achieved'
        ACCURACY_ACHIEVED = 'ACCURACY_ACHIEVED', 'Accuracy Percentage'

    class BadgeRarity(models.TextChoices):
        COMMON = 'COMMON', 'Common'
        UNCOMMON = 'UNCOMMON', 'Uncommon'
        RARE = 'RARE', 'Rare'
        EPIC = 'EPIC', 'Epic'
        LEGENDARY = 'LEGENDARY', 'Legendary'

    class BadgeCategory(models.TextChoices):
        ACHIEVEMENT = 'ACHIEVEMENT', 'Achievement'
        SKILL = 'SKILL', 'Skill'
        SOCIAL = 'SOCIAL', 'Social'
        STREAK = 'STREAK', 'Streak'
        SPECIAL = 'SPECIAL', 'Special'
        SEASONAL = 'SEASONAL', 'Seasonal'

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    criteria_type = models.CharField(max_length=30, choices=CriteriaType.choices)
    criteria_value = models.IntegerField()
    criteria_extra = models.JSONField(null=True, blank=True)  # For complex criteria

    # New fields for expanded badge system
    category = models.CharField(
        max_length=20,
        choices=BadgeCategory.choices,
        default=BadgeCategory.ACHIEVEMENT
    )
    rarity = models.CharField(
        max_length=20,
        choices=BadgeRarity.choices,
        default=BadgeRarity.COMMON
    )

    display_order = models.IntegerField(default=0)
    points_bonus = models.IntegerField(default=0)

    # Seasonal badges
    is_seasonal = models.BooleanField(default=False)
    available_from = models.DateField(null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'badges'
        ordering = ['category', 'display_order']

    def __str__(self):
        return f"{self.name} ({self.rarity})"


class ChildBadge(TimeStampedModel):
    """Junction table for badges earned by children."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='child_badges')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'child_badges'
        unique_together = ['child', 'badge']

    def __str__(self):
        return f"{self.child.name} - {self.badge.name}"


class Streak(TimeStampedModel):
    """Streak tracking for daily activity."""

    child = models.OneToOneField(Child, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'streaks'

    def __str__(self):
        return f"{self.child.name} - {self.current_streak} days"


class VoiceRecording(TimeStampedModel):
    """Voice recordings made by children."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='voice_recordings')
    story = models.ForeignKey('stories.Story', on_delete=models.SET_NULL, null=True, blank=True)
    page_number = models.IntegerField(null=True, blank=True)
    audio_url = models.URLField()
    duration_ms = models.IntegerField()
    transcription = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voice_recordings'
        indexes = [models.Index(fields=['child', 'recorded_at'])]

    def __str__(self):
        return f"{self.child.name} - Recording {self.id}"


# ===========================================
# PEPPI OUTFITS & ACCESSORIES
# ===========================================

class PeppiOutfit(TimeStampedModel):
    """Outfits that Peppi can wear."""

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique identifier code (e.g., "hindi_kurta", "diwali_special")'
    )
    name_english = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=OutfitCategory.choices)
    rarity = models.CharField(max_length=20, choices=Rarity.choices, default=Rarity.COMMON)

    # Unlock requirements
    primary_language = models.CharField(
        max_length=20,
        choices=Language.choices,
        null=True,
        blank=True,
        help_text='If language-specific, which language this belongs to'
    )
    unlock_type = models.CharField(max_length=30, choices=UnlockType.choices, default=UnlockType.DEFAULT)
    unlock_value = models.IntegerField(
        default=0,
        help_text='Value required to unlock (e.g., 7 for 7-day streak)'
    )
    unlock_festival = models.CharField(
        max_length=50,
        blank=True,
        help_text='Festival code if unlock_type is FESTIVAL'
    )

    # Media
    image_url = models.URLField(blank=True, help_text='Full outfit image URL')
    thumbnail_url = models.URLField(blank=True, help_text='Thumbnail preview URL')

    # Ordering
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'peppi_outfits'
        ordering = ['sort_order', 'name_english']
        indexes = [
            models.Index(fields=['category', 'rarity']),
            models.Index(fields=['unlock_type']),
            models.Index(fields=['primary_language']),
        ]

    def __str__(self):
        return f"{self.name_english} ({self.code})"


class PeppiOutfitTranslation(TimeStampedModel):
    """Translations for outfit names and descriptions."""

    outfit = models.ForeignKey(
        PeppiOutfit,
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(max_length=20, choices=Language.choices)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'peppi_outfit_translations'
        unique_together = ['outfit', 'language']
        indexes = [models.Index(fields=['outfit', 'language'])]

    def __str__(self):
        return f"{self.outfit.code} - {self.language}"


class PeppiAccessory(TimeStampedModel):
    """Accessories that can be equipped on Peppi."""

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique identifier (e.g., "party_hat", "flower_crown")'
    )
    name_english = models.CharField(max_length=100)
    slot = models.CharField(max_length=20, choices=AccessorySlot.choices)
    rarity = models.CharField(max_length=20, choices=Rarity.choices, default=Rarity.COMMON)

    # Unlock requirements
    unlock_type = models.CharField(max_length=30, choices=UnlockType.choices, default=UnlockType.DEFAULT)
    unlock_value = models.IntegerField(default=0)

    # Media
    image_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'peppi_accessories'
        ordering = ['slot', 'name_english']
        indexes = [
            models.Index(fields=['slot', 'rarity']),
            models.Index(fields=['unlock_type']),
        ]

    def __str__(self):
        return f"{self.name_english} ({self.slot})"


# PeppiPhrase and PeppiPhraseTranslation removed - use apps.curriculum.models.peppi.PeppiPhrase instead


# ===========================================
# CHILD PEPPI STATE
# ===========================================

class ChildPeppiState(TimeStampedModel):
    """Peppi state for each child."""

    child = models.OneToOneField(
        Child,
        on_delete=models.CASCADE,
        related_name='peppi_state'
    )

    # Peppi vitals
    happiness = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    hunger = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Lower is hungrier'
    )

    # Evolution
    evolution_stage = models.CharField(
        max_length=20,
        choices=PeppiEvolutionStage.choices,
        default=PeppiEvolutionStage.KITTEN
    )

    # Current appearance
    current_outfit = models.ForeignKey(
        PeppiOutfit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_children'
    )

    # Currency
    coins = models.IntegerField(default=100)
    gems = models.IntegerField(default=0)

    # Stats
    total_pets = models.IntegerField(default=0)
    last_fed_at = models.DateTimeField(null=True, blank=True)
    last_played_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'child_peppi_states'
        indexes = [models.Index(fields=['evolution_stage'])]

    def __str__(self):
        return f"{self.child.name}'s Peppi"

    @property
    def current_mood(self):
        """Calculate current mood based on happiness and hunger."""
        if self.happiness >= 90:
            return PeppiMood.ECSTATIC
        elif self.happiness >= 70:
            return PeppiMood.HAPPY
        elif self.happiness >= 50:
            return PeppiMood.CONTENT
        elif self.happiness >= 30:
            return PeppiMood.BORED
        elif self.happiness >= 15:
            return PeppiMood.SAD
        else:
            return PeppiMood.CRYING


class ChildUnlockedOutfit(TimeStampedModel):
    """Outfits unlocked by a child."""

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='unlocked_outfits'
    )
    outfit = models.ForeignKey(
        PeppiOutfit,
        on_delete=models.CASCADE,
        related_name='unlocked_by_children'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(
        default=True,
        help_text='Whether child has seen this unlock yet'
    )

    class Meta:
        db_table = 'child_unlocked_outfits'
        unique_together = ['child', 'outfit']
        indexes = [
            models.Index(fields=['child', 'unlocked_at']),
            models.Index(fields=['is_new']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.outfit.name_english}"


class ChildUnlockedAccessory(TimeStampedModel):
    """Accessories unlocked by a child."""

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='unlocked_accessories'
    )
    accessory = models.ForeignKey(
        PeppiAccessory,
        on_delete=models.CASCADE,
        related_name='unlocked_by_children'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'child_unlocked_accessories'
        unique_together = ['child', 'accessory']
        indexes = [
            models.Index(fields=['child', 'unlocked_at']),
            models.Index(fields=['is_new']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.accessory.name_english}"


class ChildUnlockedPhrase(TimeStampedModel):
    """Phrases unlocked by a child."""

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='unlocked_phrases'
    )
    # Reference to PeppiPhrase from curriculum app
    phrase = models.ForeignKey(
        'curriculum.PeppiPhrase',
        on_delete=models.CASCADE,
        related_name='unlocked_by_children'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'child_unlocked_phrases'
        unique_together = ['child', 'phrase']
        indexes = [
            models.Index(fields=['child', 'unlocked_at']),
            models.Index(fields=['is_new']),
        ]

    def __str__(self):
        return f"{self.child.name} - Phrase {self.phrase.id}"


class ChildEquippedAccessories(TimeStampedModel):
    """Currently equipped accessories for a child's Peppi."""

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='equipped_accessories'
    )
    accessory = models.ForeignKey(
        PeppiAccessory,
        on_delete=models.CASCADE,
        related_name='equipped_by_children'
    )
    slot = models.CharField(max_length=20, choices=AccessorySlot.choices)
    equipped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'child_equipped_accessories'
        unique_together = ['child', 'slot']
        indexes = [models.Index(fields=['child', 'slot'])]

    def __str__(self):
        return f"{self.child.name} - {self.accessory.name_english} ({self.slot})"


# ===========================================
# DAILY CHALLENGES
# ===========================================

class DailyChallengeTemplate(TimeStampedModel):
    """Template for daily challenges."""

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique identifier (e.g., "read_3_stories")'
    )
    challenge_type = models.CharField(max_length=20, choices=ChallengeType.choices)
    title_english = models.CharField(max_length=200)
    description_english = models.TextField()
    icon = models.CharField(max_length=50, default='star')

    # Challenge parameters
    target = models.IntegerField(
        help_text='Target value to complete (e.g., 3 for "read 3 stories")'
    )

    # Rewards
    xp_reward = models.IntegerField(default=50)
    coin_reward = models.IntegerField(default=100)

    # Difficulty & level gating
    difficulty = models.CharField(
        max_length=10,
        choices=ChallengeDifficulty.choices,
        default=ChallengeDifficulty.EASY
    )
    min_level = models.IntegerField(
        default=1,
        help_text='Minimum child level to receive this challenge'
    )
    max_level = models.IntegerField(
        default=10,
        help_text='Maximum child level to receive this challenge'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'daily_challenge_templates'
        ordering = ['difficulty', 'code']
        indexes = [
            models.Index(fields=['challenge_type', 'difficulty']),
            models.Index(fields=['min_level', 'max_level']),
        ]

    def __str__(self):
        return f"{self.title_english} ({self.code})"


class ChildDailyChallenge(TimeStampedModel):
    """Daily challenge assigned to a child."""

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='daily_challenges'
    )
    template = models.ForeignKey(
        DailyChallengeTemplate,
        on_delete=models.CASCADE,
        related_name='child_challenges'
    )
    date = models.DateField(help_text='Date this challenge was assigned')

    # Progress
    progress = models.IntegerField(
        default=0,
        help_text='Current progress towards target'
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    reward_claimed = models.BooleanField(
        default=False,
        help_text='Whether rewards have been claimed'
    )

    class Meta:
        db_table = 'child_daily_challenges'
        unique_together = ['child', 'template', 'date']
        indexes = [
            models.Index(fields=['child', 'date']),
            models.Index(fields=['is_completed', 'reward_claimed']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.template.title_english} ({self.date})"

    @property
    def progress_percentage(self):
        """Calculate progress as a percentage."""
        if self.template.target == 0:
            return 100
        return min(100, int((self.progress / self.template.target) * 100))


# Festival models removed - use apps.festivals.models.Festival instead
# The existing Festival model has comprehensive multi-language support
