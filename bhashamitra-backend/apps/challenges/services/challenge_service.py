# DEPLOY_VER: 2025-01-19-V7-GRAMMAR-FIX
import random
import logging
from typing import List, Dict, Any
from django.db.models import Count
from django.apps import apps

from apps.curriculum.models import (
    Script, Letter, VocabularyTheme, VocabularyWord, GrammarRule
)
from apps.curriculum.models.grammar import GrammarExercise

logger = logging.getLogger(__name__)

try:
    Language = apps.get_model('users', 'Language')
except (LookupError, ValueError):
    try:
        Language = apps.get_model('core', 'Language')
    except:
        Language = None

class ChallengeService:
    CHOICES_COUNT = 4

    @staticmethod
    def get_available_languages() -> List[str]:
        """Returns list of active language codes."""
        if not Language:
            logger.error("Language model could not be loaded.")
            return ["HINDI"]  # Safe fallback
        return list(Language.objects.filter(is_active=True).values_list('code', flat=True))

    @classmethod
    def get_available_categories(cls, language: str) -> List[Dict[str, Any]]:
        available = []
        lang_upper = language.upper()

        # 1. Alphabet
        script = Script.objects.filter(language=lang_upper).first()
        if script:
            letter_count = Letter.objects.filter(category__script=script, is_active=True).count()
            if letter_count >= cls.CHOICES_COUNT:
                available.append({"value": "ALPHABET", "label": "Alphabet", "item_count": letter_count})

        # 2. Vocabulary (Fixed to use VocabularyWord)
        vocab_count = VocabularyWord.objects.filter(theme__language=lang_upper).count()
        if vocab_count >= cls.CHOICES_COUNT:
            available.append({"value": "VOCABULARY", "label": "Vocabulary", "item_count": vocab_count})

        # 3. Grammar
        grammar_count = GrammarRule.objects.filter(topic__language=lang_upper, topic__is_active=True).count()
        if grammar_count >= cls.CHOICES_COUNT:
            available.append({"value": "GRAMMAR", "label": "Grammar", "item_count": grammar_count})

        return available

    @classmethod
    def get_random_questions(cls, language: str, category: str, difficulty: str = 'easy', count: int = 5) -> List[Dict]:
        generators = {
            'ALPHABET': cls._generate_alphabet,
            'VOCABULARY': cls._generate_vocabulary,
            'GRAMMAR': cls._generate_grammar,
        }
        handler = generators.get(category.upper())
        if not handler: return []
        try:
            return handler(language.upper(), count)
        except Exception as e:
            logger.error(f"Generation error for {category}: {e}", exc_info=True)
            return []

    @classmethod
    def _generate_alphabet(cls, lang: str, count: int) -> List[Dict]:
        items = list(Letter.objects.filter(category__script__language=lang, is_active=True))
        if len(items) < cls.CHOICES_COUNT: return []
        selected = random.sample(items, min(len(items), count))
        return [cls._build_alphabet_q(item, items) for item in selected]

    @classmethod
    def _build_alphabet_q(cls, item: Letter, pool: List[Letter]) -> Dict:
        distractors = random.sample([l for l in pool if l.id != item.id], 3)
        choices = [item.character] + [d.character for d in distractors]
        random.shuffle(choices)
        return {
            "id": str(item.id),
            "question": f"Which character is '{item.romanization}'?",
            "options": choices,
            "correct_index": choices.index(item.character),
            "audio_url": item.audio_url if item.audio_url else None
        }

    @classmethod
    def _generate_vocabulary(cls, lang: str, count: int) -> List[Dict]:
        # FIXED: Changed Word to VocabularyWord
        items = list(VocabularyWord.objects.filter(theme__language=lang))
        if len(items) < cls.CHOICES_COUNT: return []
        selected = random.sample(items, min(len(items), count))
        return [cls._build_vocab_q(item, items) for item in selected]

    @classmethod
    def _build_vocab_q(cls, item: VocabularyWord, pool: List[VocabularyWord]) -> Dict:
        distractors = random.sample([w for w in pool if w.id != item.id], 3)
        choices = [item.word] + [d.word for d in distractors]
        random.shuffle(choices)
        return {
            "id": str(item.id),
            "question": f"How do you say '{item.translation}'?",
            "options": choices,
            "correct_index": choices.index(item.word),
            "image_url": item.image_url if item.image_url else None
        }

    @classmethod
    def _generate_grammar(cls, lang: str, count: int) -> List[Dict]:
        """
        Generate grammar questions from GrammarExercise model.
        Uses multiple choice exercises with real options.
        """
        # Get multiple choice grammar exercises for this language
        exercises = list(GrammarExercise.objects.filter(
            rule__topic__language=lang,
            rule__topic__is_active=True,
            exercise_type='MC'  # Multiple Choice only
        ).select_related('rule', 'rule__topic'))

        if len(exercises) < cls.CHOICES_COUNT:
            # Fallback: Try to use any exercise type
            exercises = list(GrammarExercise.objects.filter(
                rule__topic__language=lang,
                rule__topic__is_active=True
            ).select_related('rule', 'rule__topic'))

        if not exercises:
            # Last fallback: Generate from GrammarRule examples
            return cls._generate_grammar_from_rules(lang, count)

        selected = random.sample(exercises, min(len(exercises), count))
        questions = []

        for ex in selected:
            # Build options from exercise's options field or generate them
            if ex.options and len(ex.options) >= cls.CHOICES_COUNT:
                # Use exercise's predefined options
                options = ex.options[:cls.CHOICES_COUNT]
                # Ensure correct answer is in options
                if ex.correct_answer not in options:
                    options[0] = ex.correct_answer
                random.shuffle(options)
                correct_index = options.index(ex.correct_answer)
            else:
                # Generate options from correct answer and distractors
                other_exercises = [e for e in exercises if e.id != ex.id and e.correct_answer != ex.correct_answer]
                distractors = random.sample(
                    [e.correct_answer for e in other_exercises],
                    min(cls.CHOICES_COUNT - 1, len(other_exercises))
                )
                # Pad with generic distractors if needed
                while len(distractors) < cls.CHOICES_COUNT - 1:
                    distractors.append(f"Option {len(distractors) + 2}")

                options = [ex.correct_answer] + distractors
                random.shuffle(options)
                correct_index = options.index(ex.correct_answer)

            questions.append({
                "id": str(ex.id),
                "question": ex.question,
                "options": options,
                "correct_index": correct_index,
                "hint": ex.hint if ex.hint else None,
                "topic": ex.rule.topic.name if ex.rule and ex.rule.topic else None,
            })

        return questions

    @classmethod
    def _generate_grammar_from_rules(cls, lang: str, count: int) -> List[Dict]:
        """Fallback: Generate questions from GrammarRule examples."""
        rules = list(GrammarRule.objects.filter(
            topic__language=lang,
            topic__is_active=True
        ).exclude(examples=[]))

        if not rules:
            return []

        selected = random.sample(rules, min(len(rules), count))
        questions = []

        for rule in selected:
            if not rule.examples:
                continue

            # Use the rule's example as the question
            example = rule.examples[0] if rule.examples else ""
            # Use the rule title/explanation as the correct answer
            correct_answer = rule.title

            # Get other rule titles as distractors
            other_rules = [r for r in rules if r.id != rule.id]
            distractors = random.sample(
                [r.title for r in other_rules],
                min(cls.CHOICES_COUNT - 1, len(other_rules))
            )

            options = [correct_answer] + distractors
            random.shuffle(options)

            questions.append({
                "id": str(rule.id),
                "question": f"What grammar rule applies to: '{example}'?",
                "options": options,
                "correct_index": options.index(correct_answer),
            })

        return questions

    @classmethod
    def calculate_score(cls, questions: List[Dict], answers: List[int]) -> Dict:
        detailed_results = []
        score = 0

        for i, ans in enumerate(answers):
            if i < len(questions):
                question = questions[i]
                correct_index = question.get('correct_index')

                # Log for debugging if correct_index is missing
                if correct_index is None:
                    logger.warning(f"Question {i} missing correct_index: {question.get('id', 'unknown')}")
                    # Try to infer correct_index from options if possible
                    # This handles edge cases where correct_index wasn't stored
                    is_correct = False
                else:
                    # Handle both int and string comparisons
                    is_correct = int(ans) == int(correct_index)

                if is_correct:
                    score += 1

                detailed_results.append({
                    "question_id": question.get('id', i),
                    "correct": is_correct,
                    "user_answer": ans,
                    "correct_answer": int(correct_index) if correct_index is not None else -1
                })

        max_score = len(questions)
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score * 100), 1) if max_score > 0 else 0,
            "detailed_results": detailed_results
        }

    @staticmethod
    def strip_answers(questions: List[Dict]) -> List[Dict]:
        """Remove correct_index from questions for public display."""
        # Handle None or empty questions
        if not questions:
            return []
        # Handle non-list input
        if not isinstance(questions, list):
            return []
        # Strip answers, handling malformed items
        return [
            {k: v for k, v in q.items() if k != 'correct_index'}
            for q in questions
            if isinstance(q, dict)
        ]