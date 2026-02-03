"""Seed Peppi outfits and accessories."""
from django.core.management.base import BaseCommand
from apps.gamification.models import (
    PeppiOutfit, PeppiOutfitTranslation, PeppiAccessory,
    DailyChallengeTemplate, Language, OutfitCategory, Rarity, UnlockType,
    AccessorySlot, ChallengeType, ChallengeDifficulty
)


class Command(BaseCommand):
    help = 'Seed Peppi outfits, accessories, and daily challenge templates'

    def handle(self, *args, **options):
        self.seed_outfits()
        self.seed_accessories()
        self.seed_daily_challenges()
        self.stdout.write(self.style.SUCCESS('Successfully seeded Peppi gamification data'))

    def seed_outfits(self):
        """Seed Peppi outfits."""
        outfits_data = [
            # ========== HINDI BELT OUTFITS ==========
            {
                'code': 'hindi_white_kurta',
                'name_english': 'White Kurta Pajama',
                'description': 'Simple, elegant white kurta pajama - perfect for everyday learning',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.HINDI,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 1,
                'translations': {
                    Language.HINDI: {'name': 'सफ़ेद कुर्ता पायजामा', 'description': 'सरल, सुंदर सफ़ेद कुर्ता पायजामा'},
                }
            },
            {
                'code': 'hindi_chikankari_kurta',
                'name_english': 'Chikankari Kurta',
                'description': 'Beautiful Lucknowi chikankari embroidered kurta',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.UNCOMMON,
                'primary_language': Language.HINDI,
                'unlock_type': UnlockType.VOCABULARY_MASTERED,
                'unlock_value': 50,
                'sort_order': 2,
                'translations': {
                    Language.HINDI: {'name': 'चिकनकारी कुर्ता', 'description': 'सुंदर लखनवी चिकनकारी कशीदाकारी कुर्ता'},
                }
            },
            {
                'code': 'hindi_banarasi_saree',
                'name_english': 'Banarasi Saree',
                'description': 'Magnificent Banarasi silk saree with golden zari work',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.RARE,
                'primary_language': Language.HINDI,
                'unlock_type': UnlockType.LEVEL,
                'unlock_value': 5,
                'sort_order': 3,
                'translations': {
                    Language.HINDI: {'name': 'बनारसी साड़ी', 'description': 'सुनहरी जरी वाली भव्य बनारसी रेशमी साड़ी'},
                }
            },
            {
                'code': 'hindi_sherwani',
                'name_english': 'Royal Sherwani',
                'description': 'Elegant royal sherwani fit for celebrations',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.EPIC,
                'primary_language': Language.HINDI,
                'unlock_type': UnlockType.STREAK_DAYS,
                'unlock_value': 30,
                'sort_order': 4,
                'translations': {
                    Language.HINDI: {'name': 'शाही शेरवानी', 'description': 'उत्सव के लिए शाही शेरवानी'},
                }
            },

            # ========== TAMIL OUTFITS ==========
            {
                'code': 'tamil_veshti_sattai',
                'name_english': 'Veshti Sattai',
                'description': 'Traditional Tamil veshti with matching sattai shirt',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.TAMIL,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 10,
                'translations': {
                    Language.TAMIL: {'name': 'வேஷ்டி சட்டை', 'description': 'பாரம்பரிய தமிழ் வேஷ்டி சட்டை'},
                }
            },
            {
                'code': 'tamil_pattu_pavadai',
                'name_english': 'Pattu Pavadai',
                'description': 'Beautiful silk pavadai for little girls',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.UNCOMMON,
                'primary_language': Language.TAMIL,
                'unlock_type': UnlockType.STORIES_COMPLETED,
                'unlock_value': 10,
                'sort_order': 11,
                'translations': {
                    Language.TAMIL: {'name': 'பட்டு பாவாடை', 'description': 'அழகான பட்டு பாவாடை'},
                }
            },
            {
                'code': 'tamil_kanjivaram',
                'name_english': 'Kanjivaram Saree',
                'description': 'Luxurious Kanjivaram silk saree with temple border',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.RARE,
                'primary_language': Language.TAMIL,
                'unlock_type': UnlockType.LEVEL,
                'unlock_value': 7,
                'sort_order': 12,
                'translations': {
                    Language.TAMIL: {'name': 'காஞ்சிபுரம் புடவை', 'description': 'கோயில் எல்லையுடன் அழகான காஞ்சிபுரம் பட்டு புடவை'},
                }
            },
            {
                'code': 'tamil_bharatanatyam',
                'name_english': 'Bharatanatyam Costume',
                'description': 'Colorful Bharatanatyam dance costume',
                'category': OutfitCategory.DANCE,
                'rarity': Rarity.EPIC,
                'primary_language': Language.TAMIL,
                'unlock_type': UnlockType.PERFECT_SCORES,
                'unlock_value': 20,
                'sort_order': 13,
                'translations': {
                    Language.TAMIL: {'name': 'பரதநாட்டிய உடை', 'description': 'வண்ணமயமான பரதநாட்டிய நடன உடை'},
                }
            },

            # ========== GUJARATI OUTFITS ==========
            {
                'code': 'gujarati_chaniya_choli',
                'name_english': 'Chaniya Choli',
                'description': 'Vibrant Gujarati chaniya choli for garba nights',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.GUJARATI,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 20,
                'translations': {
                    Language.GUJARATI: {'name': 'ચણિયા ચોલી', 'description': 'ગરબા માટે રંગબેરંગી ગુજરાતી ચણિયા ચોલી'},
                }
            },
            {
                'code': 'gujarati_kediyu',
                'name_english': 'Kediyu Chorno',
                'description': 'Traditional Gujarati kediyu with colorful chorno',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.UNCOMMON,
                'primary_language': Language.GUJARATI,
                'unlock_type': UnlockType.VOCABULARY_MASTERED,
                'unlock_value': 30,
                'sort_order': 21,
                'translations': {
                    Language.GUJARATI: {'name': 'કેડિયું ચોરણો', 'description': 'રંગીન ચોરણો સાથે પરંપરાગત ગુજરાતી કેડિયું'},
                }
            },
            {
                'code': 'gujarati_navratri',
                'name_english': 'Navratri Garba Special',
                'description': 'Sparkling Navratri special outfit with mirror work',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.RARE,
                'primary_language': Language.GUJARATI,
                'unlock_type': UnlockType.FESTIVAL,
                'unlock_value': 0,
                'unlock_festival': 'navratri',
                'sort_order': 22,
                'translations': {
                    Language.GUJARATI: {'name': 'નવરાત્રી ગરબા સ્પેશિયલ', 'description': 'અરીસાકામ સાથે ચમકદાર નવરાત્રી ખાસ પોશાક'},
                }
            },

            # ========== PUNJABI OUTFITS ==========
            {
                'code': 'punjabi_salwar_kameez',
                'name_english': 'Salwar Kameez',
                'description': 'Classic Punjabi salwar kameez with phulkari dupatta',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.PUNJABI,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 30,
                'translations': {
                    Language.PUNJABI: {'name': 'ਸਲਵਾਰ ਕਮੀਜ਼', 'description': 'ਫੁਲਕਾਰੀ ਦੁਪੱਟੇ ਨਾਲ ਕਲਾਸਿਕ ਪੰਜਾਬੀ ਸਲਵਾਰ ਕਮੀਜ਼'},
                }
            },
            {
                'code': 'punjabi_patiala',
                'name_english': 'Patiala Suit',
                'description': 'Royal Patiala suit with heavy embroidery',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.UNCOMMON,
                'primary_language': Language.PUNJABI,
                'unlock_type': UnlockType.STREAK_DAYS,
                'unlock_value': 7,
                'sort_order': 31,
                'translations': {
                    Language.PUNJABI: {'name': 'ਪਟਿਆਲਾ ਸੂਟ', 'description': 'ਭਾਰੀ ਕਢਾਈ ਵਾਲਾ ਸ਼ਾਹੀ ਪਟਿਆਲਾ ਸੂਟ'},
                }
            },
            {
                'code': 'punjabi_bhangra',
                'name_english': 'Bhangra Costume',
                'description': 'Energetic bhangra dance costume',
                'category': OutfitCategory.DANCE,
                'rarity': Rarity.RARE,
                'primary_language': Language.PUNJABI,
                'unlock_type': UnlockType.GAMES_WON,
                'unlock_value': 25,
                'sort_order': 32,
                'translations': {
                    Language.PUNJABI: {'name': 'ਭੰਗੜਾ ਪੋਸ਼ਾਕ', 'description': 'ਊਰਜਾਵਾਨ ਭੰਗੜਾ ਨਾਚ ਪੋਸ਼ਾਕ'},
                }
            },
            {
                'code': 'punjabi_baisakhi',
                'name_english': 'Baisakhi Special',
                'description': 'Festive Baisakhi celebration outfit',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.EPIC,
                'primary_language': Language.PUNJABI,
                'unlock_type': UnlockType.FESTIVAL,
                'unlock_value': 0,
                'unlock_festival': 'baisakhi',
                'sort_order': 33,
                'translations': {
                    Language.PUNJABI: {'name': 'ਵਿਸਾਖੀ ਸਪੈਸ਼ਲ', 'description': 'ਵਿਸਾਖੀ ਮਨਾਉਣ ਲਈ ਤਿਉਹਾਰ ਪੋਸ਼ਾਕ'},
                }
            },

            # ========== TELUGU OUTFITS ==========
            {
                'code': 'telugu_langa_voni',
                'name_english': 'Langa Voni',
                'description': 'Traditional Telugu langa voni for girls',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.TELUGU,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 40,
                'translations': {
                    Language.TELUGU: {'name': 'లంగా వోని', 'description': 'అమ్మాయిల కోసం సంప్రదాయ తెలుగు లంగా వోని'},
                }
            },
            {
                'code': 'telugu_pochampally',
                'name_english': 'Pochampally Ikat',
                'description': 'Beautiful Pochampally ikat weave saree',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.RARE,
                'primary_language': Language.TELUGU,
                'unlock_type': UnlockType.LEVEL,
                'unlock_value': 6,
                'sort_order': 41,
                'translations': {
                    Language.TELUGU: {'name': 'పోచంపల్లి ఇక్కట్', 'description': 'అందమైన పోచంపల్లి ఇక్కట్ నేత చీర'},
                }
            },
            {
                'code': 'telugu_kuchipudi',
                'name_english': 'Kuchipudi Costume',
                'description': 'Elegant Kuchipudi classical dance costume',
                'category': OutfitCategory.DANCE,
                'rarity': Rarity.EPIC,
                'primary_language': Language.TELUGU,
                'unlock_type': UnlockType.PERFECT_SCORES,
                'unlock_value': 15,
                'sort_order': 42,
                'translations': {
                    Language.TELUGU: {'name': 'కూచిపూడి దుస్తులు', 'description': 'సొగసైన కూచిపూడి శాస్త్రీయ నృత్య దుస్తులు'},
                }
            },

            # ========== MALAYALAM OUTFITS ==========
            {
                'code': 'malayalam_kasavu',
                'name_english': 'Kasavu Saree',
                'description': 'Elegant Kerala kasavu saree with golden border',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.MALAYALAM,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 50,
                'translations': {
                    Language.MALAYALAM: {'name': 'കസവ് സാരി', 'description': 'സ്വർണ്ണ ബോർഡർ ഉള്ള കേരള കസവ് സാരി'},
                }
            },
            {
                'code': 'malayalam_onam',
                'name_english': 'Onam Special',
                'description': 'Beautiful Onam festival attire',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.RARE,
                'primary_language': Language.MALAYALAM,
                'unlock_type': UnlockType.FESTIVAL,
                'unlock_value': 0,
                'unlock_festival': 'onam',
                'sort_order': 51,
                'translations': {
                    Language.MALAYALAM: {'name': 'ഓണം സ്പെഷ്യൽ', 'description': 'മനോഹരമായ ഓണം ഉത്സവ വേഷം'},
                }
            },
            {
                'code': 'malayalam_kathakali',
                'name_english': 'Kathakali Costume',
                'description': 'Magnificent Kathakali dance costume with makeup',
                'category': OutfitCategory.DANCE,
                'rarity': Rarity.LEGENDARY,
                'primary_language': Language.MALAYALAM,
                'unlock_type': UnlockType.BADGES_EARNED,
                'unlock_value': 10,
                'sort_order': 52,
                'translations': {
                    Language.MALAYALAM: {'name': 'കഥകളി വേഷം', 'description': 'മേക്കപ്പോടുകൂടിയ മനോഹരമായ കഥകളി നൃത്ത വേഷം'},
                }
            },

            # ========== FIJI HINDI OUTFITS ==========
            {
                'code': 'fiji_sulu_fusion',
                'name_english': 'Sulu Fusion',
                'description': 'Indo-Fijian fusion sulu with kurta elements',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.COMMON,
                'primary_language': Language.FIJI_HINDI,
                'unlock_type': UnlockType.DEFAULT,
                'unlock_value': 0,
                'sort_order': 60,
                'translations': {
                    Language.FIJI_HINDI: {'name': 'सुलू फ्यूजन', 'description': 'कुर्ता तत्वों के साथ इंडो-फिजियन फ्यूजन सुलू'},
                }
            },
            {
                'code': 'fiji_bula_shirt',
                'name_english': 'Bula Shirt',
                'description': 'Colorful Fijian bula shirt with tropical prints',
                'category': OutfitCategory.TRADITIONAL,
                'rarity': Rarity.UNCOMMON,
                'primary_language': Language.FIJI_HINDI,
                'unlock_type': UnlockType.STORIES_COMPLETED,
                'unlock_value': 15,
                'sort_order': 61,
                'translations': {
                    Language.FIJI_HINDI: {'name': 'बुला शर्ट', 'description': 'ट्रॉपिकल प्रिंट के साथ रंगीन फिजियन बुला शर्ट'},
                }
            },

            # ========== UNIVERSAL/SPECIAL OUTFITS ==========
            {
                'code': 'diwali_sparkle',
                'name_english': 'Diwali Sparkle',
                'description': 'Glittering Diwali celebration outfit with sparklers',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.RARE,
                'unlock_type': UnlockType.FESTIVAL,
                'unlock_value': 0,
                'unlock_festival': 'diwali',
                'sort_order': 100,
            },
            {
                'code': 'holi_rainbow',
                'name_english': 'Holi Rainbow',
                'description': 'Color-splashed Holi celebration outfit',
                'category': OutfitCategory.FESTIVE,
                'rarity': Rarity.RARE,
                'unlock_type': UnlockType.FESTIVAL,
                'unlock_value': 0,
                'unlock_festival': 'holi',
                'sort_order': 101,
            },
            {
                'code': 'superhero_cape',
                'name_english': 'Superhero Cape',
                'description': 'Heroic cape for language learning champions',
                'category': OutfitCategory.SILLY,
                'rarity': Rarity.EPIC,
                'unlock_type': UnlockType.STREAK_DAYS,
                'unlock_value': 100,
                'sort_order': 110,
            },
            {
                'code': 'wizard_hat',
                'name_english': 'Wizard Hat',
                'description': 'Magical wizard hat for word wizards',
                'category': OutfitCategory.SILLY,
                'rarity': Rarity.RARE,
                'unlock_type': UnlockType.VOCABULARY_MASTERED,
                'unlock_value': 200,
                'sort_order': 111,
            },
            {
                'code': 'royal_crown',
                'name_english': 'Royal Crown',
                'description': 'Golden crown for language royalty',
                'category': OutfitCategory.LEGENDARY,
                'rarity': Rarity.LEGENDARY,
                'unlock_type': UnlockType.LEVEL,
                'unlock_value': 10,
                'sort_order': 120,
            },
            {
                'code': 'rainbow_wings',
                'name_english': 'Rainbow Wings',
                'description': 'Magical rainbow wings for learning to fly',
                'category': OutfitCategory.LEGENDARY,
                'rarity': Rarity.LEGENDARY,
                'unlock_type': UnlockType.ALPHABET_MASTERED,
                'unlock_value': 1,
                'sort_order': 121,
            },
        ]

        created_count = 0
        for outfit_data in outfits_data:
            translations = outfit_data.pop('translations', {})
            unlock_festival = outfit_data.pop('unlock_festival', '')

            outfit, created = PeppiOutfit.objects.get_or_create(
                code=outfit_data['code'],
                defaults={**outfit_data, 'unlock_festival': unlock_festival}
            )

            if created:
                created_count += 1
                # Create translations
                for lang, trans_data in translations.items():
                    PeppiOutfitTranslation.objects.get_or_create(
                        outfit=outfit,
                        language=lang,
                        defaults=trans_data
                    )

        self.stdout.write(f'Created {created_count} outfits')

    def seed_accessories(self):
        """Seed Peppi accessories."""
        accessories_data = [
            # HEAD accessories
            {'code': 'party_hat', 'name_english': 'Party Hat', 'slot': AccessorySlot.HEAD, 'rarity': Rarity.COMMON, 'unlock_type': UnlockType.DEFAULT},
            {'code': 'flower_crown', 'name_english': 'Flower Crown', 'slot': AccessorySlot.HEAD, 'rarity': Rarity.UNCOMMON, 'unlock_type': UnlockType.STREAK_DAYS, 'unlock_value': 3},
            {'code': 'star_tiara', 'name_english': 'Star Tiara', 'slot': AccessorySlot.HEAD, 'rarity': Rarity.RARE, 'unlock_type': UnlockType.LEVEL, 'unlock_value': 5},

            # NECK accessories
            {'code': 'friendship_collar', 'name_english': 'Friendship Collar', 'slot': AccessorySlot.NECK, 'rarity': Rarity.COMMON, 'unlock_type': UnlockType.DEFAULT},
            {'code': 'bell_collar', 'name_english': 'Bell Collar', 'slot': AccessorySlot.NECK, 'rarity': Rarity.UNCOMMON, 'unlock_type': UnlockType.STORIES_COMPLETED, 'unlock_value': 5},
            {'code': 'marigold_garland', 'name_english': 'Marigold Garland', 'slot': AccessorySlot.NECK, 'rarity': Rarity.RARE, 'unlock_type': UnlockType.FESTIVAL, 'unlock_value': 0},

            # PAWS accessories
            {'code': 'learning_bangles', 'name_english': 'Learning Bangles', 'slot': AccessorySlot.PAWS, 'rarity': Rarity.COMMON, 'unlock_type': UnlockType.DEFAULT},
            {'code': 'rainbow_socks', 'name_english': 'Rainbow Socks', 'slot': AccessorySlot.PAWS, 'rarity': Rarity.UNCOMMON, 'unlock_type': UnlockType.GAMES_WON, 'unlock_value': 10},

            # BACKGROUND accessories
            {'code': 'sparkle_aura', 'name_english': 'Sparkle Aura', 'slot': AccessorySlot.BACKGROUND, 'rarity': Rarity.RARE, 'unlock_type': UnlockType.PERFECT_SCORES, 'unlock_value': 10},
            {'code': 'rainbow_aura', 'name_english': 'Rainbow Aura', 'slot': AccessorySlot.BACKGROUND, 'rarity': Rarity.LEGENDARY, 'unlock_type': UnlockType.STREAK_DAYS, 'unlock_value': 50},
        ]

        created_count = 0
        for acc_data in accessories_data:
            _, created = PeppiAccessory.objects.get_or_create(
                code=acc_data['code'],
                defaults=acc_data
            )
            if created:
                created_count += 1

        self.stdout.write(f'Created {created_count} accessories')

    def seed_daily_challenges(self):
        """Seed daily challenge templates."""
        challenges_data = [
            # EASY challenges
            {'code': 'read_1_story', 'challenge_type': ChallengeType.STORY_READ, 'title_english': 'Story Time', 'description_english': 'Read 1 story today', 'target': 1, 'xp_reward': 25, 'coin_reward': 50, 'difficulty': ChallengeDifficulty.EASY, 'icon': 'book'},
            {'code': 'learn_3_words', 'challenge_type': ChallengeType.VOCABULARY, 'title_english': 'Word Explorer', 'description_english': 'Learn 3 new words', 'target': 3, 'xp_reward': 30, 'coin_reward': 60, 'difficulty': ChallengeDifficulty.EASY, 'icon': 'abc'},
            {'code': 'record_1_voice', 'challenge_type': ChallengeType.VOICE_RECORD, 'title_english': 'Voice Star', 'description_english': 'Make 1 voice recording', 'target': 1, 'xp_reward': 20, 'coin_reward': 40, 'difficulty': ChallengeDifficulty.EASY, 'icon': 'mic'},
            {'code': 'play_1_game', 'challenge_type': ChallengeType.GAME_PLAY, 'title_english': 'Game Time', 'description_english': 'Play 1 learning game', 'target': 1, 'xp_reward': 20, 'coin_reward': 40, 'difficulty': ChallengeDifficulty.EASY, 'icon': 'gamepad'},

            # MEDIUM challenges
            {'code': 'read_3_stories', 'challenge_type': ChallengeType.STORY_READ, 'title_english': 'Story Marathon', 'description_english': 'Read 3 stories today', 'target': 3, 'xp_reward': 75, 'coin_reward': 150, 'difficulty': ChallengeDifficulty.MEDIUM, 'icon': 'books', 'min_level': 2},
            {'code': 'learn_10_words', 'challenge_type': ChallengeType.VOCABULARY, 'title_english': 'Word Master', 'description_english': 'Learn 10 new words', 'target': 10, 'xp_reward': 100, 'coin_reward': 200, 'difficulty': ChallengeDifficulty.MEDIUM, 'icon': 'dictionary', 'min_level': 2},
            {'code': 'record_5_voices', 'challenge_type': ChallengeType.VOICE_RECORD, 'title_english': 'Voice Champion', 'description_english': 'Make 5 voice recordings', 'target': 5, 'xp_reward': 80, 'coin_reward': 160, 'difficulty': ChallengeDifficulty.MEDIUM, 'icon': 'microphone', 'min_level': 2},
            {'code': 'play_3_games', 'challenge_type': ChallengeType.GAME_PLAY, 'title_english': 'Game Champion', 'description_english': 'Play 3 learning games', 'target': 3, 'xp_reward': 60, 'coin_reward': 120, 'difficulty': ChallengeDifficulty.MEDIUM, 'icon': 'trophy', 'min_level': 2},
            {'code': 'perfect_1_lesson', 'challenge_type': ChallengeType.PERFECT_LESSON, 'title_english': 'Perfect Score', 'description_english': 'Get a perfect score in any lesson', 'target': 1, 'xp_reward': 100, 'coin_reward': 200, 'difficulty': ChallengeDifficulty.MEDIUM, 'icon': 'star', 'min_level': 2},

            # HARD challenges
            {'code': 'read_5_stories', 'challenge_type': ChallengeType.STORY_READ, 'title_english': 'Story Legend', 'description_english': 'Read 5 stories today', 'target': 5, 'xp_reward': 150, 'coin_reward': 300, 'difficulty': ChallengeDifficulty.HARD, 'icon': 'library', 'min_level': 4},
            {'code': 'learn_20_words', 'challenge_type': ChallengeType.VOCABULARY, 'title_english': 'Word Wizard', 'description_english': 'Learn 20 new words', 'target': 20, 'xp_reward': 200, 'coin_reward': 400, 'difficulty': ChallengeDifficulty.HARD, 'icon': 'wizard', 'min_level': 4},
            {'code': 'perfect_3_lessons', 'challenge_type': ChallengeType.PERFECT_LESSON, 'title_english': 'Perfectionist', 'description_english': 'Get 3 perfect scores in lessons', 'target': 3, 'xp_reward': 250, 'coin_reward': 500, 'difficulty': ChallengeDifficulty.HARD, 'icon': 'stars', 'min_level': 4},
        ]

        created_count = 0
        for challenge_data in challenges_data:
            _, created = DailyChallengeTemplate.objects.get_or_create(
                code=challenge_data['code'],
                defaults=challenge_data
            )
            if created:
                created_count += 1

        self.stdout.write(f'Created {created_count} daily challenge templates')
