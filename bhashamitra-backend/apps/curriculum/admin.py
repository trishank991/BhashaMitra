"""Curriculum admin configuration."""
from django.contrib import admin
from .models import (
    Script, AlphabetCategory, Letter, Matra, LetterProgress,
    VocabularyTheme, VocabularyWord, WordProgress,
    GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress,
    Game, GameSession, GameLeaderboard,
    Assessment, AssessmentQuestion, AssessmentAttempt, Certificate,
)


# Script Admin
class LetterInline(admin.TabularInline):
    model = Letter
    extra = 0


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'total_letters']
    list_filter = ['language']


@admin.register(AlphabetCategory)
class AlphabetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'script', 'category_type', 'order']
    list_filter = ['script', 'category_type']
    inlines = [LetterInline]


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['character', 'romanization', 'category', 'order', 'is_active']
    list_filter = ['category__script', 'category__category_type', 'is_active']
    search_fields = ['character', 'romanization']


@admin.register(Matra)
class MatraAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'script', 'example_with_ka', 'order']
    list_filter = ['script']


# Vocabulary Admin
class VocabularyWordInline(admin.TabularInline):
    model = VocabularyWord
    extra = 0


@admin.register(VocabularyTheme)
class VocabularyThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'level', 'word_count', 'is_active']
    list_filter = ['language', 'level', 'is_premium', 'is_active']
    inlines = [VocabularyWordInline]


@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'romanization', 'translation', 'theme', 'part_of_speech']
    list_filter = ['theme__language', 'part_of_speech', 'gender']
    search_fields = ['word', 'romanization', 'translation']


# Grammar Admin
class GrammarRuleInline(admin.TabularInline):
    model = GrammarRule
    extra = 0


class GrammarExerciseInline(admin.TabularInline):
    model = GrammarExercise
    extra = 0


@admin.register(GrammarTopic)
class GrammarTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'level', 'is_active']
    list_filter = ['language', 'level', 'is_active']
    inlines = [GrammarRuleInline]


@admin.register(GrammarRule)
class GrammarRuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'order']
    list_filter = ['topic__language', 'topic']
    inlines = [GrammarExerciseInline]


# Games Admin
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_type', 'skill_focus', 'language', 'level', 'is_active']
    list_filter = ['game_type', 'skill_focus', 'language', 'level', 'is_premium', 'is_active']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['child', 'game', 'score', 'completed', 'created_at']
    list_filter = ['game', 'completed', 'created_at']


# Assessment Admin
class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 0


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'assessment_type', 'language', 'level', 'passing_score', 'is_active']
    list_filter = ['assessment_type', 'language', 'level', 'is_active']
    inlines = [AssessmentQuestionInline]


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ['child', 'assessment', 'score', 'percentage', 'passed', 'started_at']
    list_filter = ['assessment', 'passed', 'started_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'child', 'title', 'certificate_type', 'issued_at']
    list_filter = ['certificate_type', 'language', 'issued_at']
    readonly_fields = ['certificate_id', 'issued_at']
