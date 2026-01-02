"""
Challenge Service - Generate quiz questions from curriculum data.
Updated with GrammarRule logic and model name fixes.
"""

import random
from typing import List, Dict, Any, Optional
from django.db.models import Q

from apps.curriculum.models import Letter, VocabularyWord, VocabularyTheme, Script, GrammarRule
from apps.challenges.models import ChallengeCategory, ChallengeDifficulty


class ChallengeService:
    """Generate quiz questions from existing curriculum data."""

    # Number of answer choices per question
    CHOICES_COUNT = 4

    @classmethod
    def generate_questions(
        cls,
        language: str,
        category: str,
        difficulty: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        # Normalize language to uppercase to match DB entries (HINDI, GUJARATI)
        lang_upper = language.upper()

        if category == ChallengeCategory.ALPHABET:
            return cls._generate_alphabet_questions(lang_upper, difficulty, count)
        elif category == ChallengeCategory.VOCABULARY:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count)
        elif category == ChallengeCategory.MIMIC:
            return cls._generate_mimic_questions(lang_upper, difficulty, count)
        else:
            # Check for theme-based categories (Numbers, Colors, etc.)
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name=category)

    @classmethod
    def _generate_alphabet_questions(cls, language: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        script = Script.objects.filter(language=language).first()
        if not script:
            return []

        letters = list(Letter.objects.filter(category__script=script, is_active=True).exclude(romanization=''))
        if len(letters) < cls.CHOICES_COUNT:
            return []

        random.shuffle(letters)
        selected_letters = letters[:count]
        questions = []

        for idx, letter in enumerate(selected_letters):
            other_letters = [l for l in letters if l.id != letter.id]
            wrong_choices = random.sample(other_letters, min(cls.CHOICES_COUNT - 1, len(other_letters)))
            choices = [letter.romanization] + [l.romanization for l in wrong_choices]
            random.shuffle(choices)

            questions.append({
                "id": idx + 1,
                "type": "alphabet_recognition",
                "question": "What sound does this letter make?",
                "prompt": letter.character,
                "prompt_native": letter.character,
                "choices": choices,
                "correct_index": choices.index(letter.romanization),
                "image_url": letter.example_image.url if letter.example_image else None,
                "audio_url": letter.audio_url.url if letter.audio_url else None,
                "hint": letter.pronunciation_guide,
            })
        return questions

    @classmethod
    def _generate_vocabulary_questions(cls, language: str, difficulty: str, count: int, theme_name: Optional[str] = None) -> List[Dict[str, Any]]:
        query = Q(theme__language=language, theme__is_active=True)
        if theme_name:
            query &= Q(theme__name__icontains=theme_name)

        words = list(VocabularyWord.objects.filter(query).select_related('theme'))
        if len(words) < cls.CHOICES_COUNT:
            return []

        random.shuffle(words)
        selected_words = words[:count]
        questions = []

        for idx, word in enumerate(selected_words):
            # Alternate between Native-to-English and English-to-Native
            question_type = idx % 2
            other_words = [w for w in words if w.id != word.id]
            wrong_choices = random.sample(other_words, min(cls.CHOICES_COUNT - 1, len(other_words)))

            if question_type == 0:
                choices = [word.translation] + [w.translation for w in wrong_choices]
                random.shuffle(choices)
                questions.append({
                    "id": idx + 1,
                    "type": "vocabulary_to_english",
                    "question": "What does this word mean?",
                    "prompt": word.word,
                    "prompt_native": word.word,
                    "choices": choices,
                    "correct_index": choices.index(word.translation),
                    "image_url": word.image_url.url if word.image_url else None,
                    "audio_url": word.pronunciation_audio_url.url if word.pronunciation_audio_url else None,
                })
            else:
                choices = [word.word] + [w.word for w in wrong_choices]
                random.shuffle(choices)
                questions.append({
                    "id": idx + 1,
                    "type": "english_to_vocabulary",
                    "question": f"How do you say '{word.translation}'?",
                    "prompt": word.translation,
                    "prompt_native": None,
                    "choices": choices,
                    "correct_index": choices.index(word.word),
                    "image_url": word.image_url.url if word.image_url else None,
                })
        return questions

    @classmethod
    def _generate_mimic_questions(cls, language: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        """Generate mimic questions using GrammarRule examples."""
        query = Q(topic__language=language, topic__is_active=True)
        
        # Filter based on difficulty level if provided in the model
        if difficulty == ChallengeDifficulty.EASY:
            query &= Q(topic__level__lte=2)
        elif difficulty == ChallengeDifficulty.MEDIUM:
            query &= Q(topic__level__lte=4)

        rules = list(GrammarRule.objects.filter(query).exclude(examples__isnull=True).exclude(examples=[]))
        
        all_sentences = []
        for rule in rules:
            for ex in rule.examples:
                # Logic to find native text regardless of key name (hindi/native/etc)
                native_text = ex.get('native') or ex.get(language.lower()) or ex.get('hindi')
                english_text = ex.get('english') or ex.get('translation')
                
                if native_text and english_text:
                    all_sentences.append({
                        'sentence': native_text,
                        'translation': english_text,
                        'romanization': ex.get('romanized', '')
                    })

        if not all_sentences:
            return []
            
        random.shuffle(all_sentences)
        selected = all_sentences[:count]
        questions = []

        for idx, item in enumerate(selected):
            questions.append({
                "id": idx + 1,
                "type": ChallengeCategory.MIMIC,
                "question": "Repeat the following sentence:",
                "prompt": item['sentence'],
                "prompt_native": item['sentence'],
                "translation": item['translation'],
                "romanization": item['romanization'],
                "correct_index": 0,
                "choices": [],
            })
        return questions

    @classmethod
    def get_available_categories(cls, language: str) -> List[Dict[str, Any]]:
        available = []
        lang_upper = language.upper()

        # 1. Alphabet
        script = Script.objects.filter(language=lang_upper).first()
        if script:
            letter_count = Letter.objects.filter(category__script=script, is_active=True).count()
            if letter_count >= cls.CHOICES_COUNT:
                available.append({"value": ChallengeCategory.ALPHABET, "label": "Alphabet", "item_count": letter_count})

        # 2. Vocabulary (General & Themes)
        themes = VocabularyTheme.objects.filter(language=lang_upper, is_active=True)
        total_vocab = sum(t.word_count for t in themes)
        if total_vocab >= cls.CHOICES_COUNT:
            available.append({"value": ChallengeCategory.VOCABULARY, "label": "Vocabulary", "item_count": total_vocab})

        # 3. Mimic (Peppi Mimic) - Fixed NameError for 'Grammar'
        grammar_count = GrammarRule.objects.filter(
            topic__language=lang_upper, 
            topic__is_active=True
        ).exclude(examples__isnull=True).exclude(examples=[]).count()

        if grammar_count > 0:
            available.append({
                "value": ChallengeCategory.MIMIC,
                "label": "Peppi Mimic",
                "item_count": grammar_count,
            })

        return available

    @classmethod
    def calculate_score(cls, questions: List[Dict[str, Any]], answers: List[int]) -> Dict[str, Any]:
        score = 0
        results = []
        for q, user_ans in zip(questions, answers):
            is_correct = (user_ans == q['correct_index'])
            if is_correct: score += 1
            results.append({"question_id": q['id'], "correct": is_correct})

        max_score = len(questions)
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score * 100), 1) if max_score > 0 else 0,
            "detailed_results": results
}
    @staticmethod
    def strip_answers(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Removes the correct_index from questions before sending to the frontend.
        """
        if not questions:
            return []
        
        stripped = []
        for q in questions:
            # Create a copy so we don't modify the original database object/dict
            q_copy = q.copy()
            if 'correct_index' in q_copy:
                del q_copy['correct_index']
            stripped.append(q_copy)
        return stripped
        