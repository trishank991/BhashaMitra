# DEPLOY_VER: 2026-01-03-V6-FINAL
import random
import logging
from typing import List, Dict, Any
from django.db.models import Count
from django.apps import apps 

from apps.curriculum.models import (
    Script, Letter, VocabularyTheme, VocabularyWord, GrammarRule
)

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
            return ["HINDI"] # Safe fallback
        return list(Language.objects.filter(is_active=True).values_list('code', flat=True))

    @staticmethod
    def get_available_languages() -> List[str]:
        if not Language:
            logger.error("Language model could not be loaded.")
            return ["HINDI"]
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

        # 3. Mimic
        grammar_count = GrammarRule.objects.filter(topic__language=lang_upper, topic__is_active=True).count()
        if grammar_count >= cls.CHOICES_COUNT:
            available.append({"value": "MIMIC", "label": "Peppi Mimic", "item_count": grammar_count})

        return available

    @classmethod
    def get_random_questions(cls, language: str, category: str, difficulty: str = 'easy', count: int = 5) -> List[Dict]:
        generators = {
            'ALPHABET': cls._generate_alphabet,
            'VOCABULARY': cls._generate_vocabulary,
            'MIMIC': cls._generate_mimic,
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
            "question": f"Which character is '{item.name}'?",
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
    def _generate_mimic(cls, lang: str, count: int) -> List[Dict]:
        items = list(GrammarRule.objects.filter(topic__language=lang, topic__is_active=True))
        if not items: return []
        selected = random.sample(items, min(len(items), count))
        return [{
            "id": str(item.id),
            "question": item.examples[0] if item.examples else "Repeat after Peppi",
            "options": [item.explanation[:50], "Option B", "Option C", "Option D"],
            "correct_index": 0
        } for item in selected]

    @classmethod
    def calculate_score(cls, questions: List[Dict], answers: List[int]) -> Dict:
        score = sum(
            str(ans) == str(questions[i].get('correct_index'))
            for i, ans in enumerate(answers)
            if i < len(questions)
        )
        max_score = len(questions)
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score * 100), 1) if max_score > 0 else 0,
            "detailed_results": []
        }

    @staticmethod
    def strip_answers(questions: List[Dict]) -> List[Dict]:
        return [{k: v for k, v in q.items() if k != 'correct_index'} for q in questions]