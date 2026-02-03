"""Services for family challenges and progress tracking."""
from typing import List, Dict, Any
from django.db.models import Count
from django.utils import timezone
from .models import (
    Family, CurriculumChallenge, CurriculumChallengeParticipant,
    CurriculumChallengeAttempt
)
from .serializers import CurriculumChallengeParticipantSerializer


class CurriculumChallengeService:
    """Service for curriculum-based challenges."""

    @staticmethod
    def get_child_progress_summary(child_id: str) -> Dict[str, Any]:
        """Get summary of child's curriculum progress for challenge generation.
        
        Returns dict with:
        - completed_letters: List of letters child has learned
        - completed_words: List of words child has learned
        - completed_lessons: List of lesson IDs child has completed
        - current_level: Child's current curriculum level
        """
        from apps.children.models import Child
        from apps.curriculum.models import AlphabetProgress, VocabularyProgress
        from apps.curriculum.models import LessonProgress
        
        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return {}
        
        # Get alphabet progress
        alphabet_progress = AlphabetProgress.objects.filter(
            child=child
        ).values('letter', 'status')
        
        completed_letters = [
            p['letter'] for p in alphabet_progress 
            if p['status'] in ['MASTERED', 'LEARNING']
        ]
        
        # Get vocabulary progress
        vocab_progress = VocabularyProgress.objects.filter(
            child=child
        ).values('word_id', 'status')
        
        completed_words = [
            p['word_id'] for p in vocab_progress 
            if p['status'] in ['MASTERED', 'LEARNING']
        ]
        
        # Get lesson progress
        lesson_progress = LessonProgress.objects.filter(
            child=child
        ).values('lesson_id', 'status')
        
        completed_lessons = [
            p['lesson_id'] for p in lesson_progress 
            if p['status'] == 'COMPLETED'
        ]
        
        return {
            'child_id': str(child.id),
            'child_name': child.name,
            'level': child.level,
            'language': child.language,
            'completed_letters': completed_letters,
            'completed_words': completed_words,
            'completed_lessons': completed_lessons,
        }

    @staticmethod
    def generate_questions_for_challenge(
        challenge: CurriculumChallenge,
        child_id: str
    ) -> List[Dict[str, Any]]:
        """Generate questions for a challenge based on child's progress.
        
        Questions are ONLY generated from content the child has already learned.
        This ensures fair competition.
        """
        questions = []
        child_progress = CurriculumChallengeService.get_child_progress_summary(child_id)
        
        challenge_type = challenge.challenge_type
        
        if challenge_type == CurriculumChallenge.ChallengeType.ALPHABET:
            questions = CurriculumChallengeService._generate_alphabet_questions(
                challenge, child_progress
            )
        elif challenge_type == CurriculumChallenge.ChallengeType.VOCABULARY:
            questions = CurriculumChallengeService._generate_vocabulary_questions(
                challenge, child_progress
            )
        elif challenge_type == CurriculumChallenge.ChallengeType.SENTENCES:
            questions = CurriculumChallengeService._generate_sentence_questions(
                challenge, child_progress
            )
        elif challenge_type == CurriculumChallenge.ChallengeType.MIMIC_PRONUNCIATION:
            questions = CurriculumChallengeService._generate_mimic_questions(
                challenge, child_progress
            )
        elif challenge_type == CurriculumChallenge.ChallengeType.DICTATION:
            questions = CurriculumChallengeService._generate_dictation_questions(
                challenge, child_progress
            )
        
        return questions

    @staticmethod
    def _generate_alphabet_questions(
        challenge: CurriculumChallenge,
        child_progress: Dict
    ) -> List[Dict[str, Any]]:
        """Generate alphabet recognition questions from learned letters."""
        from apps.curriculum.models import VerifiedLetter
        
        if not (completed_letters := child_progress.get('completed_letters', [])):
            # Fallback: get letters from child's level if no progress yet
            level = child_progress.get('level', 1)
            letters = VerifiedLetter.objects.filter(
                difficulty__lte=level
            ).order_by('?')[:challenge.target_count]
        else:
            letters = VerifiedLetter.objects.filter(
                character__in=completed_letters
            ).order_by('?')[:challenge.target_count]
        
        questions = [{
                'item_type': 'ALPHABET',
                'item_id': str(letter.id),
                'item_value': letter.character,
                'question': f"What letter is this?",
                'question_native': f"यह कौन सा अक्षर है?",
                'correct_answer': letter.character,
                'romanization': letter.romanization,
                'audio_url': letter.audio_url,
        } for letter in letters]
        return questions

    @staticmethod
    def _generate_vocabulary_questions(
        challenge: CurriculumChallenge,
        child_progress: Dict
    ) -> List[Dict[str, Any]]:
        """Generate vocabulary questions from learned words."""
        from apps.curriculum.models import VocabularyWord, VocabularyTheme
        
        if not (completed_words := child_progress.get('completed_words', [])):
            # Fallback: get words from themes child has started
            level = child_progress.get('level', 1)
            words = VocabularyWord.objects.filter(
                difficulty__lte=level
            ).order_by('?')[:challenge.target_count]
        else:
            words = VocabularyWord.objects.filter(
                id__in=completed_words
            ).order_by('?')[:challenge.target_count]
        
        questions = [{
                'item_type': 'VOCABULARY',
                'item_id': str(word.id),
                'item_value': word.word,
                'question': f"What does \"{word.word}\" mean?",
                'question_native': f"\"{word.word}\" का क्या मतलब है?",
                'correct_answer': word.translation,
                'romanization': word.romanization,
                'audio_url': word.pronunciation_audio_url,
                'image_url': word.image_url,
        } for word in words]
        return questions

    @staticmethod
    def _generate_sentence_questions(
        challenge: CurriculumChallenge,
        child_progress: Dict
    ) -> List[Dict[str, Any]]:
        """Generate sentence building questions from completed lessons."""
        from apps.curriculum.models import Lesson, LessonContent
        
        completed_lessons = child_progress.get('completed_lessons', [])
        
        # Get sentence exercises from completed lessons
        contents = LessonContent.objects.filter(
            lesson_id__in=completed_lessons,
            content_type='GRAMMAR_RULE'
        ).select_related('grammar_rule').order_by('?')[:challenge.target_count]
        
        questions = [{
                    'item_type': 'SENTENCE',
                    'item_id': str(content.grammar_rule.id),
                    'item_value': content.grammar_rule.title,
                    'question': content.grammar_rule.explanation,
                    'correct_answer': content.grammar_rule.formula,
                    'examples': content.grammar_rule.examples,
        } for content in contents if content.grammar_rule]
        return questions

    @staticmethod
    def _generate_mimic_questions(
        challenge: CurriculumChallenge,
        child_progress: Dict
    ) -> List[Dict[str, Any]]:
        """Generate pronunciation practice questions."""
        from apps.speech.models import PeppiMimicChallenge
        
        # Use custom words from challenge, or fall back to child's learned words
        custom_words = challenge.custom_words or []
        
        if custom_words:
            # Parent specified words - create questions for each
            questions = [{
                    'item_type': 'PRONUNCIATION',
                    'item_id': word,  # Use word as ID for custom words
                    'item_value': word,
                    'question': f"Say this word: {word}",
                    'question_native': f"इस शब्द को बोलो: {word}",
                    'correct_answer': word,
                    'is_custom': True,
            } for word in custom_words[:challenge.target_count]]
        else:
            # Use Peppi Mimic challenges from child's learned words
            completed_words = child_progress.get('completed_words', [])
            
            if completed_words:
                challenges = PeppiMimicChallenge.objects.filter(
                    word__in=completed_words[:50]  # Limit query
                ).order_by('?')[:challenge.target_count]
            else:
                # Fallback to any available challenges at child's level
                level = child_progress.get('level', 1)
                challenges = PeppiMimicChallenge.objects.filter(
                    difficulty__lte=level
                ).order_by('?')[:challenge.target_count]
            
            questions = [{
                    'item_type': 'PRONUNCIATION',
                    'item_id': str(challenge_obj.id),
                    'item_value': challenge_obj.word,
                    'question': challenge_obj.peppi_intro,
                    'question_native': None,
                    'correct_answer': challenge_obj.word,
                    'romanization': challenge_obj.romanization,
                    'audio_url': challenge_obj.audio_url,
                    'is_custom': False,
            } for challenge_obj in challenges]
        return questions

    @staticmethod
    def _generate_dictation_questions(
        challenge: CurriculumChallenge,
        child_progress: Dict
    ) -> List[Dict[str, Any]]:
        """Generate dictation questions (parent-led)."""
        custom_words = challenge.custom_words or []
        
        if not custom_words:
            # Fallback to learned words
            from apps.curriculum.models import VocabularyWord
            if completed_words := child_progress.get('completed_words', []):
                words = VocabularyWord.objects.filter(
                    id__in=completed_words
                ).order_by('?')[:challenge.target_count]
            else:
                level = child_progress.get('level', 1)
                words = VocabularyWord.objects.filter(
                    difficulty__lte=level
                ).order_by('?')[:challenge.target_count]
            
            custom_words = [w.word for w in words]
        
        questions = [{
                'item_type': 'DICTATION',
                'item_id': word,  # Use word as ID
                'item_value': word,
                'question': f"Parent will say: \"{word}\". Tap microphone and say it!",
                'question_native': f"अभिभावक बोलेंगे: \"{word}\". माइक्रोफोन पर टैप करें और बोलें!",
                'correct_answer': word,
                'is_custom': True,
        } for word in custom_words[:challenge.target_count]]
        return questions

    @staticmethod
    def generate_preview_questions(challenge: CurriculumChallenge) -> List[Dict[str, Any]]:
        """Generate a small preview of questions for display."""
        # Get first participant to generate preview
        first_participant = challenge.participants.first()
        
        if not first_participant:
            return []
        
        # Generate questions with limit
        all_questions = CurriculumChallengeService.generate_questions_for_challenge(
            challenge, str(first_participant.child.id)
        )
        
        # Return first 3 questions for preview
        return all_questions[:3]

    @staticmethod
    def evaluate_answer(
        challenge: CurriculumChallenge,
        participant: CurriculumChallengeParticipant,
        answer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a challenge answer and return result."""
        item_type = answer_data.get('item_type')
        user_answer = answer_data.get('user_answer', '').strip()
        correct_answer = answer_data.get('item_value', '').strip()
        audio_url = answer_data.get('audio_url')
        transcription = answer_data.get('transcription', '').strip()
        
        is_correct = False
        accuracy_score = 0.0
        
        if item_type in ['ALPHABET', 'VOCABULARY', 'SENTENCE']:
            # Direct comparison for text-based answers
            is_correct = user_answer.lower() == correct_answer.lower()
            accuracy_score = 100.0 if is_correct else 0.0
        
        elif item_type == 'DICTATION':
            # Compare what child said to expected word
            # Use fuzzy matching for slight variations
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, transcription.lower(), correct_answer.lower()).ratio()
            is_correct = similarity >= 0.7  # 70% threshold
            accuracy_score = similarity * 100
        elif item_type == 'PRONUNCIATION':
            # For pronunciation, use accuracy if provided by STT
            # or calculate similarity to expected word
            if transcription:
                from difflib import SequenceMatcher
                similarity = SequenceMatcher(None, transcription.lower(), correct_answer.lower()).ratio()
                accuracy_score = similarity * 100
                is_correct = similarity >= 0.7
            elif audio_url:
                # Fallback: if we have audio but no transcription, assume in progress
                accuracy_score = 50.0
                is_correct = False
        
        # Create attempt record
        attempt = CurriculumChallengeAttempt.objects.create(
            participant=participant,
            item_type=item_type,
            item_id=answer_data.get('item_id', ''),
            item_value=answer_data.get('item_value', ''),
            user_answer=user_answer,
            is_correct=is_correct,
            audio_url=audio_url,
            transcription=transcription,
            accuracy_score=accuracy_score,
        )
        
        # Update participant progress
        participant.update_progress(is_correct)
        
        # Check if participant completed the challenge
        is_complete = participant.completed_count >= challenge.target_count
        
        # Generate feedback message
        if is_correct:
            message = (
                "🎉 Perfect! Excellent work!" if accuracy_score >= 90
                else "👍 Great job! Keep it up!" if accuracy_score >= 70
                else "✓ Correct! Good effort!"
            )
        elif item_type == 'DICTATION':
            message = f"Not quite. The word was \"{correct_answer}\". Try again!"
        else:
            message = f"Not quite. The answer was \"{correct_answer}\". Try again!"
        
        return {
            'is_correct': is_correct,
            'accuracy_score': accuracy_score,
            'current_progress': CurriculumChallengeParticipantSerializer(participant).data,
            'is_complete': is_complete,
            'message': message,
        }

    @staticmethod
    def calculate_winner(challenge: CurriculumChallenge) -> CurriculumChallengeParticipant:
        """Calculate and set the winner of a challenge.
        
        Winner is determined by highest accuracy. Time is not considered
        for L1-L2 learning stage (as per product decision).
        """
        participants = challenge.participants.all()
        
        if not participants.exists():
            return None
        
        # Order by accuracy descending, then by completed_count descending
        winner = participants.order_by(
            '-accuracy_score', '-completed_count'
        ).first()
        
        if winner:
            challenge.winner = winner.child
            challenge.status = CurriculumChallenge.Status.COMPLETED
            challenge.save(update_fields=['winner', 'status'])
            
            # Mark all participants as complete
            for participant in participants:
                if not participant.completed_at:
                    participant.mark_complete()
        
        return winner

    @staticmethod
    def start_challenge(challenge: CurriculumChallenge):
        """Start a challenge (change from PENDING to ACTIVE)."""
        if challenge.status != CurriculumChallenge.Status.PENDING:
            return False
        
        challenge.status = CurriculumChallenge.Status.ACTIVE
        challenge.save(update_fields=['status'])
        
        return True

    @staticmethod
    def get_active_challenges_for_child(child_id: str) -> List[CurriculumChallenge]:
        """Get all active challenges a child can participate in."""
        from apps.children.models import Child
        
        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return []
        
        # Get challenges from child's family
        if not child.family:
            return []
        
        return CurriculumChallenge.objects.filter(
            family=child.family,
            status=CurriculumChallenge.Status.ACTIVE,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            participants__child=child
        ).distinct()

    @staticmethod
    def get_participant_progress(
        challenge: CurriculumChallenge,
        child_id: str
    ) -> CurriculumChallengeParticipant:
        """Get or create participant record for a child in a challenge."""
        participant, created = CurriculumChallengeParticipant.objects.get_or_create(
            challenge=challenge,
            child_id=child_id
        )
        return participant


class FamilyService:
    """Service for family management."""

    @staticmethod
    def create_family_for_user(user, name: str = "") -> Family:
        """Create a new family for a user."""
        if hasattr(user, 'families_owned') and user.families_owned.exists():
            raise ValueError("User already has a family")
        
        return Family.objects.create(
            primary_parent=user,
            created_by=user,
            name=name or f"{user.name}'s Family"
        )

    @staticmethod
    def join_family_via_code(user, invite_code: str) -> Family:
        """Join a family using an invite code.
        
        This adds all of the user's children to the family.
        """
        try:
            family = Family.objects.get(invite_code=invite_code.upper())
        except Family.DoesNotExist:
            raise ValueError("Invalid invite code")
        
        if not family.is_invite_code_valid():
            raise ValueError("Invite code has expired")
        
        if family.primary_parent == user:
            raise ValueError("You cannot join your own family")
        
        # Add all user's children to the family
        from apps.children.models import Child
        children = Child.objects.filter(parent=user)
        
        for child in children:
            family.add_child(child)
        
        return family

    @staticmethod
    def add_child_to_family(family: Family, child) -> bool:
        """Add a single child to a family."""
        if child.family == family:
            return False  # Already in family
        
        family.add_child(child)
        return True

    @staticmethod
    def remove_child_from_family(family: Family, child) -> bool:
        """Remove a child from a family."""
        if child.family != family:
            return False  # Not in family
        
        family.remove_child(child)
        return True

    @staticmethod
    def get_family_for_user(user) -> Family:
        """Get the family for a user (if exists)."""
        families = user.families_owned.all()
        return families.first() if families.exists() else None

    @staticmethod
    def refresh_family_code(family: Family) -> str:
        """Generate a new invite code for the family."""
        family.refresh_invite_code()
        return family.invite_code
