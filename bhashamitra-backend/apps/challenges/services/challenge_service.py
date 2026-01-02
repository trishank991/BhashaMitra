"""
Challenge Service - Generate quiz questions from curriculum data.

Question Types:
1. Alphabet Recognition - Show letter, pick correct romanization
2. Vocabulary - Show word, pick correct translation
3. Reverse Vocabulary - Show English, pick correct native word
4. Image Match - Show image, pick correct word
"""

import random
from typing import List, Dict, Any, Optional
from django.db.models import Q

from apps.curriculum.models import Letter, VocabularyWord, VocabularyTheme, AlphabetCategory, Script, GrammarTopic
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
        """
        Generate questions for a challenge based on category and difficulty.
        """
        # Normalize language to uppercase to match DB entries (HINDI, GUJARATI)
        lang_upper = language.upper()

        if category == ChallengeCategory.ALPHABET:
            return cls._generate_alphabet_questions(lang_upper, difficulty, count)
        elif category == ChallengeCategory.VOCABULARY:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count)
        elif category == ChallengeCategory.NUMBERS:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Numbers')
        elif category == ChallengeCategory.COLORS:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Colors')
        elif category == ChallengeCategory.ANIMALS:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Animals')
        elif category == ChallengeCategory.FAMILY:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Family')
        elif category == ChallengeCategory.FOOD:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Food')
        elif category == ChallengeCategory.GREETINGS:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count, theme_name='Greetings')
        elif category == ChallengeCategory.MIMIC:
            return cls._generate_mimic_questions(lang_upper, difficulty, count)
        else:
            return cls._generate_vocabulary_questions(lang_upper, difficulty, count)

    @classmethod
    def _generate_alphabet_questions(
        cls,
        language: str,
        difficulty: str,
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate alphabet recognition questions."""
        questions = []

        # Use filter().first() to handle cases with duplicate Script entries safely
        script = Script.objects.filter(language=language).first()
        
        if not script:
            return []

        letters = list(Letter.objects.filter(
            category__script=script,
            is_active=True
        ).exclude(romanization=''))

        if len(letters) < cls.CHOICES_COUNT:
            return []

        random.shuffle(letters)
        selected_letters = letters[:count]

        for idx, letter in enumerate(selected_letters):
            other_letters = [l for l in letters if l.id != letter.id]
            wrong_choices = random.sample(other_letters, min(cls.CHOICES_COUNT - 1, len(other_letters)))

            choices = [letter.romanization] + [l.romanization for l in wrong_choices]
            random.shuffle(choices)
            correct_index = choices.index(letter.romanization)

            question = {
                "id": idx + 1,
                "type": "alphabet_recognition",
                "question": "What sound does this letter make?",
                "prompt": letter.character,
                "prompt_native": letter.character,
                "choices": choices,
                "correct_index": correct_index,
                "image_url": letter.example_image.url if letter.example_image else None,
                "audio_url": letter.audio_url.url if letter.audio_url else None,
                "hint": letter.pronunciation_guide or None,
            }
            questions.append(question)

        return questions

    @classmethod
    def _generate_vocabulary_questions(
        cls,
        language: str,
        difficulty: str,
        count: int,
        theme_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate vocabulary questions."""
        questions = []
        query = Q(theme__language=language, theme__is_active=True)

        if theme_name:
            query &= Q(theme__name__icontains=theme_name)

        if difficulty == ChallengeDifficulty.EASY:
            query &= Q(theme__level__lte=2)
        elif difficulty == ChallengeDifficulty.MEDIUM:
            query &= Q(theme__level__lte=3)

        words = list(VocabularyWord.objects.filter(query).select_related('theme'))

        if len(words) < cls.CHOICES_COUNT:
            words = list(VocabularyWord.objects.filter(
                theme__language=language,
                theme__is_active=True
            ).select_related('theme'))

        if len(words) < cls.CHOICES_COUNT:
            return []

        random.shuffle(words)
        selected_words = words[:count]

        for idx, word in enumerate(selected_words):
            question_type = idx % 2
            other_words = [w for w in words if w.id != word.id]
            wrong_choices = random.sample(other_words, min(cls.CHOICES_COUNT - 1, len(other_words)))

            if question_type == 0:
                choices = [word.translation] + [w.translation for w in wrong_choices]
                random.shuffle(choices)
                correct_index = choices.index(word.translation)

                question = {
                    "id": idx + 1,
                    "type": "vocabulary_to_english",
                    "question": "What does this word mean?",
                    "prompt": word.word,
                    "prompt_native": word.word,
                    "romanization": word.romanization,
                    "choices": choices,
                    "correct_index": correct_index,
                    "image_url": word.image_url.url if word.image_url else None,
                    "audio_url": word.pronunciation_audio_url.url if word.pronunciation_audio_url else None,
                    "hint": None,
                }
            else:
                choices = [word.word] + [w.word for w in wrong_choices]
                random.shuffle(choices)
                correct_index = choices.index(word.word)

                question = {
                    "id": idx + 1,
                    "type": "english_to_vocabulary",
                    "question": f"How do you say '{word.translation}'?",
                    "prompt": word.translation,
                    "prompt_native": None,
                    "romanization": None,
                    "choices": choices,
                    "correct_index": correct_index,
                    "image_url": word.image_url.url if word.image_url else None,
                    "audio_url": None,
                    "hint": word.romanization,
                }
            questions.append(question)

        return questions

    @classmethod
    def _generate_mimic_questions(
        cls,
        language: str,
        difficulty: str,
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate mimic the sentence questions using GrammarTopic."""
        questions = []
        query = Q(language=language)
        
        if difficulty == ChallengeDifficulty.EASY:
            query &= Q(level__lte=2)
        elif difficulty == ChallengeDifficulty.MEDIUM:
            query &= Q(level__lte=4)
        
        # Corrected model name from Grammar to GrammarTopic
        sentences = list(GrammarTopic.objects.filter(query))
        
        if not sentences:
            return []
        
        random.shuffle(sentences)
        selected_sentences = sentences[:count]
        
        for idx, sentence in enumerate(selected_sentences):
            question = {
                "id": idx + 1,
                "type": "mimic",
                "question": "Repeat the following sentence:",
                "prompt": sentence.sentence,
                "prompt_native": sentence.sentence,
                "translation": sentence.translation,
                "audio_url": sentence.audio_url.url if sentence.audio_url else None,
                "correct_index": 0,
                "choices": [],
            }
            questions.append(question)
            
        return questions

    @classmethod
    def get_available_categories(cls, language: str) -> List[Dict[str, Any]]:
        """Get categories that have enough content for quizzes."""
        available = []
        lang_upper = language.upper()

        # Check alphabet
        script = Script.objects.filter(language=lang_upper).first()
        if script:
            letter_count = Letter.objects.filter(
                category__script=script,
                is_active=True
            ).count()
            if letter_count >= cls.CHOICES_COUNT:
                available.append({
                    "value": ChallengeCategory.ALPHABET,
                    "label": "Alphabet Recognition",
                    "item_count": letter_count,
                })

        # Check vocabulary themes
        themes = VocabularyTheme.objects.filter(
            language=lang_upper,
            is_active=True
        )

        total_words = sum(theme.word_count for theme in themes)
        if total_words >= cls.CHOICES_COUNT:
            available.append({
                "value": ChallengeCategory.VOCABULARY,
                "label": "Vocabulary",
                "item_count": total_words,
            })

        theme_mapping = {
            'number': ChallengeCategory.NUMBERS,
            'color': ChallengeCategory.COLORS,
            'animal': ChallengeCategory.ANIMALS,
            'family': ChallengeCategory.FAMILY,
            'food': ChallengeCategory.FOOD,
            'fruit': ChallengeCategory.FOOD,
            'greeting': ChallengeCategory.GREETINGS,
        }

        for theme in themes:
            theme_name_lower = theme.name.lower()
            for keyword, category in theme_mapping.items():
                if keyword in theme_name_lower and theme.word_count >= cls.CHOICES_COUNT:
                    if not any(c['value'] == category for c in available):
                        available.append({
                            "value": category,
                            "label": dict(ChallengeCategory.choices).get(category, category),
                            "item_count": theme.word_count,
                        })

        # Corrected model name from Grammar to GrammarTopic
        grammar_count = GrammarTopic.objects.filter(language=lang_upper).count()
        if grammar_count > 0:
            available.append({
                "value": ChallengeCategory.MIMIC,
                "label": "Mimic the Sentence",
                "item_count": grammar_count,
            })

        return available

    @classmethod
    def calculate_score(
        cls,
        questions: List[Dict[str, Any]],
        answers: List[int]
    ) -> Dict[str, Any]:
        """Calculate score from submitted answers."""
        if len(answers) != len(questions):
            raise ValueError("Number of answers must match number of questions")

        score = 0
        detailed_results = []

        for q, user_answer in zip(questions, answers):
            correct = user_answer == q['correct_index']
            if correct:
                score += 1

            detailed_results.append({
                "question_id": q['id'],
                "correct": correct,
                "user_answer": user_answer,
                "correct_answer": q['correct_index'],
            })

        max_score = len(questions)
        percentage = (score / max_score * 100) if max_score > 0 else 0.0

        return {
            "score": score,
            "max_score": max_score,
            "percentage": round(percentage, 1),
            "detailed_results": detailed_results,
        }

    @classmethod
    def strip_answers(cls, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove correct_index from questions for public API response."""
        return [
            {k: v for k, v in q.items() if k != 'correct_index'}
            for q in questions
        ]
    