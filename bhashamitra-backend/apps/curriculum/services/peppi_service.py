"""Peppi AI companion service."""
import random
from typing import Dict, Optional
from django.utils import timezone
from apps.curriculum.models import PeppiPersonality, PeppiLearningContext, VocabularyWord
from apps.children.models import Child


class PeppiAIService:
    """Service for Peppi AI companion interactions."""

    @staticmethod
    def get_personality_for_age(age: int) -> Optional[PeppiPersonality]:
        """Get appropriate personality for child's age."""
        if 4 <= age <= 5:
            age_group = '4-5'
        elif 6 <= age <= 8:
            age_group = '6-8'
        elif 9 <= age <= 11:
            age_group = '9-11'
        elif 12 <= age <= 14:
            age_group = '12-14'
        else:
            return None

        return PeppiPersonality.objects.filter(
            age_group=age_group,
            is_active=True
        ).first()

    @staticmethod
    def get_or_create_context(child: Child) -> PeppiLearningContext:
        """Get or create learning context for a child."""
        context, created = PeppiLearningContext.objects.get_or_create(
            child=child,
            defaults={
                'mood': 'neutral',
                'total_sessions': 0,
                'streak_days': 0,
            }
        )
        return context

    @staticmethod
    def get_greeting(child: Child, time_of_day: str = None) -> Dict[str, str]:
        """Generate age-appropriate Hindi greeting."""
        personality = PeppiAIService.get_personality_for_age(child.age)
        context = PeppiAIService.get_or_create_context(child)

        # Increment session count
        context.total_sessions += 1
        context.save()

        # Determine time-based greeting
        if not time_of_day:
            hour = timezone.now().hour
            if hour < 12:
                time_of_day = 'morning'
            elif hour < 17:
                time_of_day = 'afternoon'
            elif hour < 21:
                time_of_day = 'evening'
            else:
                time_of_day = 'night'

        # Age-appropriate greetings
        greetings = {
            'morning': {
                '4-5': {
                    'hindi': 'सुप्रभात',
                    'romanized': 'Suprabhat',
                    'english': 'Good morning'
                },
                '6-8': {
                    'hindi': 'सुप्रभात',
                    'romanized': 'Suprabhat',
                    'english': 'Good morning'
                },
                '9-11': {
                    'hindi': 'शुभ प्रभात',
                    'romanized': 'Shubh Prabhat',
                    'english': 'Good morning'
                },
                '12-14': {
                    'hindi': 'शुभ प्रभात',
                    'romanized': 'Shubh Prabhat',
                    'english': 'Good morning'
                },
            },
            'afternoon': {
                '4-5': {
                    'hindi': 'नमस्ते',
                    'romanized': 'Namaste',
                    'english': 'Hello'
                },
                '6-8': {
                    'hindi': 'नमस्ते',
                    'romanized': 'Namaste',
                    'english': 'Hello'
                },
                '9-11': {
                    'hindi': 'नमस्ते',
                    'romanized': 'Namaste',
                    'english': 'Hello'
                },
                '12-14': {
                    'hindi': 'नमस्कार',
                    'romanized': 'Namaskar',
                    'english': 'Greetings'
                },
            },
            'evening': {
                '4-5': {
                    'hindi': 'शुभ संध्या',
                    'romanized': 'Shubh Sandhya',
                    'english': 'Good evening'
                },
                '6-8': {
                    'hindi': 'शुभ संध्या',
                    'romanized': 'Shubh Sandhya',
                    'english': 'Good evening'
                },
                '9-11': {
                    'hindi': 'शुभ संध्या',
                    'romanized': 'Shubh Sandhya',
                    'english': 'Good evening'
                },
                '12-14': {
                    'hindi': 'शुभ संध्या',
                    'romanized': 'Shubh Sandhya',
                    'english': 'Good evening'
                },
            },
            'night': {
                '4-5': {
                    'hindi': 'शुभ रात्रि',
                    'romanized': 'Shubh Ratri',
                    'english': 'Good night'
                },
                '6-8': {
                    'hindi': 'शुभ रात्रि',
                    'romanized': 'Shubh Ratri',
                    'english': 'Good night'
                },
                '9-11': {
                    'hindi': 'शुभ रात्रि',
                    'romanized': 'Shubh Ratri',
                    'english': 'Good night'
                },
                '12-14': {
                    'hindi': 'शुभ रात्रि',
                    'romanized': 'Shubh Ratri',
                    'english': 'Good night'
                },
            },
        }

        age_group = personality.age_group if personality else '4-5'
        greeting_data = greetings.get(time_of_day, {}).get(age_group, greetings['morning']['4-5'])

        # Addressing preference
        if child.peppi_addressing == Child.PeppiAddressing.BY_NAME:
            addressing = child.name
        else:
            if child.peppi_gender == Child.PeppiGender.MALE:
                addressing = 'भैया' if age_group in ['4-5', '6-8'] else 'भाई साहब'
            else:
                addressing = 'दीदी' if age_group in ['4-5', '6-8'] else 'बहन जी'

        return {
            'greeting_hindi': greeting_data['hindi'],
            'greeting_romanized': greeting_data['romanized'],
            'greeting_english': greeting_data['english'],
            'message_hindi': f"{greeting_data['hindi']} {addressing}! आज हिंदी सीखने के लिए तैयार हो?",
            'message_romanized': f"{greeting_data['romanized']} {addressing}! Aaj Hindi seekhne ke liye taiyar ho?",
            'message_english': f"{greeting_data['english']} {addressing}! Ready to learn Hindi today?",
            'expression': 'waving',
            'peppi_mood': context.mood,
            'session_count': context.total_sessions,
            'streak': context.streak_days,
        }

    @staticmethod
    def teach_word(word: VocabularyWord, child_age: int) -> Dict[str, str]:
        """Generate teaching script for vocabulary word."""
        if child_age <= 5:
            script_hindi = f"आओ एक नया शब्द सीखें! {word.word}। इसे कहते हैं {word.romanization}। क्या तुम बोल सकते हो?"
            script_romanized = f"Aao ek naya shabd seekhen! {word.word}. Ise kehte hain {word.romanization}. Kya tum bol sakte ho?"
            script_english = f"Let's learn a new word! {word.word}. It is called {word.romanization}. Can you say it?"
        elif child_age <= 8:
            script_hindi = f"आज का शब्द है {word.word} - {word.romanization}। इसका मतलब है {word.translation}।"
            script_romanized = f"Aaj ka shabd hai {word.word} - {word.romanization}. Iska matlab hai {word.translation}."
            script_english = f"Today's word is {word.word} - {word.romanization}. It means {word.translation}."
        else:
            script_hindi = f"शब्द {word.word} ({word.romanization}) का अर्थ है {word.translation}।"
            script_romanized = f"Shabd {word.word} ({word.romanization}) ka arth hai {word.translation}."
            script_english = f"The word {word.word} ({word.romanization}) means {word.translation}."

        return {
            'word_hindi': word.word,
            'word_romanized': word.romanization,
            'word_english': word.translation,
            'teaching_script_hindi': script_hindi,
            'teaching_script_romanized': script_romanized,
            'teaching_script_english': script_english,
            'part_of_speech': word.part_of_speech,
            'audio_url': word.pronunciation_audio_url or '',
            'example_sentence': word.example_sentence or '',
        }

    @staticmethod
    def give_feedback(is_correct: bool, child_age: int, activity_type: str = 'general') -> Dict[str, str]:
        """Generate encouragement or correction feedback."""
        if is_correct:
            if child_age <= 5:
                phrases = [
                    {'hindi': 'शाबाश!', 'romanized': 'Shabash!', 'english': 'Well done!'},
                    {'hindi': 'बहुत अच्छा!', 'romanized': 'Bahut Accha!', 'english': 'Very good!'},
                    {'hindi': 'वाह!', 'romanized': 'Waah!', 'english': 'Wow!'},
                    {'hindi': 'क्या बात है!', 'romanized': 'Kya baat hai!', 'english': 'How wonderful!'},
                ]
            elif child_age <= 8:
                phrases = [
                    {'hindi': 'बढ़िया!', 'romanized': 'Badhiya!', 'english': 'Excellent!'},
                    {'hindi': 'शाबाश!', 'romanized': 'Shabash!', 'english': 'Bravo!'},
                    {'hindi': 'बहुत सुंदर!', 'romanized': 'Bahut Sundar!', 'english': 'Beautiful!'},
                    {'hindi': 'ज़बरदस्त!', 'romanized': 'Zabardast!', 'english': 'Awesome!'},
                ]
            else:
                phrases = [
                    {'hindi': 'उत्तम!', 'romanized': 'Uttam!', 'english': 'Outstanding!'},
                    {'hindi': 'बेहतरीन!', 'romanized': 'Behtareen!', 'english': 'Fantastic!'},
                    {'hindi': 'कमाल!', 'romanized': 'Kamaal!', 'english': 'Amazing!'},
                    {'hindi': 'लाजवाब!', 'romanized': 'Lajawaab!', 'english': 'Incomparable!'},
                ]

            phrase = random.choice(phrases)
            return {
                'feedback_hindi': phrase['hindi'],
                'feedback_romanized': phrase['romanized'],
                'feedback_english': phrase['english'],
                'is_correct': True,
                'expression': 'celebrating',
                'message_hindi': f"{phrase['hindi']} तुम बहुत अच्छा कर रहे हो!",
                'message_romanized': f"{phrase['romanized']} Tum bahut accha kar rahe ho!",
                'message_english': f"{phrase['english']} You're doing great!",
            }
        else:
            if child_age <= 5:
                return {
                    'feedback_hindi': 'कोई बात नहीं!',
                    'feedback_romanized': 'Koi baat nahi!',
                    'feedback_english': "That's okay!",
                    'is_correct': False,
                    'expression': 'encouraging',
                    'message_hindi': 'कोई बात नहीं! चलो फिर से कोशिश करते हैं!',
                    'message_romanized': 'Koi baat nahi! Chalo phir se koshish karte hain!',
                    'message_english': "That's okay! Let's try again together!",
                }
            else:
                return {
                    'feedback_hindi': 'फिर से कोशिश करें!',
                    'feedback_romanized': 'Phir se koshish karen!',
                    'feedback_english': 'Try again!',
                    'is_correct': False,
                    'expression': 'thinking',
                    'message_hindi': 'बिल्कुल सही नहीं! मैं तुम्हारी मदद करता हूँ।',
                    'message_romanized': 'Bilkul sahi nahi! Main tumhari madad karta hoon.',
                    'message_english': 'Not quite right! Let me help you.',
                }

    @staticmethod
    def get_story_narration(story_title: str, page_number: int, page_text: str) -> Dict[str, str]:
        """Generate story narration with engagement."""
        if page_number == 1:
            intro_hindi = 'चलो एक कहानी सुनते हैं! '
            intro_romanized = 'Chalo ek kahani sunte hain! '
            intro_english = "Let's read a story together! "
        elif page_number == 2:
            intro_hindi = 'और फिर... '
            intro_romanized = 'Aur phir... '
            intro_english = 'And then... '
        else:
            intro_hindi = 'आगे... '
            intro_romanized = 'Aage... '
            intro_english = 'Next... '

        return {
            'narration_hindi': f'{intro_hindi}{page_text}',
            'narration_romanized': f'{intro_romanized}',
            'narration_english': f'{intro_english}',
            'page_number': page_number,
            'engagement_prompt_hindi': 'आगे क्या होगा?' if page_number > 1 else 'शुरू करें?',
            'engagement_prompt_romanized': 'Aage kya hoga?' if page_number > 1 else 'Shuru karen?',
            'engagement_prompt_english': 'What do you think happens next?' if page_number > 1 else 'Ready to start?',
        }
