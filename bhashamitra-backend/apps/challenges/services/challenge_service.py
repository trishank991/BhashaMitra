import random
import logging
from typing import List, Dict, Any
from django.db.models import Sum, Count

# Correct imports pointing to the curriculum app
from apps.challenges.models import Challenge, ChallengeAttempt, ChallengeCategory
from apps.curriculum.models import Script, Letter, VocabularyTheme, GrammarRule

logger = logging.getLogger(__name__)

class ChallengeService:
    CHOICES_COUNT = 4

    @classmethod
    def get_available_categories(cls, language: str) -> List[Dict[str, Any]]:
        available = []
        lang_upper = language.upper()

        # 1. Alphabet - Checking letters in the script
        script = Script.objects.filter(language=lang_upper).first()
        if script:
            # We count letters directly related to the active script
            letter_count = Letter.objects.filter(
                category__script=script, 
                is_active=True
            ).count()
            
            if letter_count >= cls.CHOICES_COUNT:
                available.append({
                    "value": ChallengeCategory.ALPHABET, 
                    "label": "Alphabet", 
                    "item_count": letter_count
                })

        # 2. Vocabulary - Counting themes or items
        # Replaced the crashing Sum('word_count') with a count of active themes
        vocab_data = VocabularyTheme.objects.filter(
            language=lang_upper, 
            is_active=True
        ).aggregate(total=Count('id'))
        
        total_vocab = vocab_data['total'] or 0
        if total_vocab >= cls.CHOICES_COUNT:
            available.append({
                "value": ChallengeCategory.VOCABULARY, 
                "label": "Vocabulary", 
                "item_count": total_vocab
            })

        # 3. Mimic - Checking for grammar rules with examples
        grammar_count = GrammarRule.objects.filter(
            topic__language=lang_upper, 
            topic__is_active=True
        ).exclude(examples__isnull=True).count()

        if grammar_count > 0:
            available.append({
                "value": ChallengeCategory.MIMIC,
                "label": "Peppi Mimic",
                "item_count": grammar_count,
            })

        return available

    @classmethod
    def get_random_questions(cls, questions: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """
        Shuffles the question pool and returns a specific number of questions.
        """
        if not questions:
            return []
        
        # Create a copy to protect original data, shuffle and slice
        shuffled_pool = list(questions)
        random.shuffle(shuffled_pool)
        return shuffled_pool[:count]

    @classmethod
    def calculate_score(cls, questions: List[Dict[str, Any]], answers: List[int]) -> Dict[str, Any]:
        """
        Calculates the user's score based on submitted answers.
        """
        score = 0
        results = []
        
        for q, user_ans in zip(questions, answers):
            correct_idx = q.get('correct_index')
            try:
                # Type casting ensures string "1" matches integer 1
                is_correct = (int(user_ans) == int(correct_idx))
            except (ValueError, TypeError):
                is_correct = False

            if is_correct: 
                score += 1
                
            results.append({
                "question_id": q.get('id'), 
                "user_answer": user_ans,
                "correct_answer": correct_idx,
                "is_correct": is_correct,
                "correct": is_correct # Duplicate key for frontend compatibility
            })

        max_score = len(questions)
        return {
            "score": score,
            "total_questions": max_score,
            "max_score": max_score,
            "percentage": round((score / max_score * 100), 1) if max_score > 0 else 0,
            "detailed_results": results
        }

    @staticmethod
    def strip_answers(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Removes the correct answer index before sending questions to the client.
        """
        if not questions:
            return []
        return [{k: v for k, v in q.items() if k != 'correct_index'} for q in questions]
    @classmethod
    def get_random_questions(cls, questions: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """
        Shuffles the question pool and returns a specific number of questions.
        """
        if not questions:
            return []
            
        # Create a copy so we don't shuffle the original data in the DB/Cache
        shuffled_pool = list(questions)
        random.shuffle(shuffled_pool)
        
        # Return only the amount requested (e.g., 5)
        return shuffled_pool[:count]