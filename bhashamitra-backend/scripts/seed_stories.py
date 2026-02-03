"""
Seed script for Peppi Academy original stories.

These are Creative Commons (CC BY 4.0) stories created for Peppi Academy,
representing India's diverse traditions, regions, religions, and cultures.

Run: python manage.py shell < scripts/seed_stories.py
"""

from apps.stories.models import Story, StoryPage
from apps.children.models import Child

# Clear existing Peppi stories (keep StoryWeaver ones if any)
Story.objects.filter(storyweaver_id__startswith='peppi-').delete()

# =============================================================================
# PEPPI ACADEMY ORIGINAL STORIES
# Representing ALL of India's diversity
# =============================================================================

STORIES = [
    # =========================================================================
    # LEVEL 1 - BEGINNERS (Ages 4-6) - Simple sentences, basic vocabulary
    # =========================================================================

    # STORY 1: Universal values - Friendship
    {
        'storyweaver_id': 'peppi-001',
        'title': 'चार दोस्त',
        'title_translit': 'Chaar Dost (Four Friends)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A heartwarming tale of four friends from different backgrounds who help each other.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Friendship', 'Values', 'Diversity'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'एक गाँव में चार दोस्त रहते थे।\n\nEk gaon mein chaar dost rehte the.\n\n(Four friends lived in a village.)',
            },
            {
                'page_number': 2,
                'text_content': 'आमिर को किताबें पढ़ना पसंद था।\n\nAamir ko kitaabein padhna pasand tha.\n\n(Aamir loved reading books.)',
            },
            {
                'page_number': 3,
                'text_content': 'प्रिया को चित्र बनाना पसंद था।\n\nPriya ko chitra banana pasand tha.\n\n(Priya loved drawing pictures.)',
            },
            {
                'page_number': 4,
                'text_content': 'गुरप्रीत को खेलना पसंद था।\n\nGurpreet ko khelna pasand tha.\n\n(Gurpreet loved playing.)',
            },
            {
                'page_number': 5,
                'text_content': 'जॉन को गाना पसंद था।\n\nJohn ko gaana pasand tha.\n\n(John loved singing.)',
            },
            {
                'page_number': 6,
                'text_content': 'सब मिलकर खुश रहते थे।\n\nSab milkar khush rehte the.\n\n(Together, they all lived happily.)',
            },
        ]
    },

    # STORY 2: Nature and Animals
    {
        'storyweaver_id': 'peppi-002',
        'title': 'मोर और मोरनी',
        'title_translit': 'Mor aur Morni (Peacock and Peahen)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A beautiful story about India\'s national bird, the peacock.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Nature', 'Animals', 'India'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'जंगल में एक सुंदर मोर था।\n\nJangal mein ek sundar mor tha.\n\n(There was a beautiful peacock in the forest.)',
            },
            {
                'page_number': 2,
                'text_content': 'उसके पंख नीले और हरे थे।\n\nUske pankh neele aur hare the.\n\n(Its feathers were blue and green.)',
            },
            {
                'page_number': 3,
                'text_content': 'बारिश आई तो मोर ने नाचा।\n\nBaarish aayi to mor ne naacha.\n\n(When rain came, the peacock danced.)',
            },
            {
                'page_number': 4,
                'text_content': 'सब जानवर खुश हो गए।\n\nSab jaanwar khush ho gaye.\n\n(All animals became happy.)',
            },
        ]
    },

    # STORY 3: Festival Story - Diwali (Hindu)
    {
        'storyweaver_id': 'peppi-003',
        'title': 'दीवाली की रोशनी',
        'title_translit': 'Diwali ki Roshni (Light of Diwali)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A simple story about celebrating the festival of lights.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Festival', 'Diwali', 'Hindu'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'आज दीवाली है!\n\nAaj Diwali hai!\n\n(Today is Diwali!)',
            },
            {
                'page_number': 2,
                'text_content': 'माँ ने दीये जलाए।\n\nMaa ne diye jalaye.\n\n(Mother lit the lamps.)',
            },
            {
                'page_number': 3,
                'text_content': 'घर रोशनी से भर गया।\n\nGhar roshni se bhar gaya.\n\n(The house filled with light.)',
            },
            {
                'page_number': 4,
                'text_content': 'सबने मिठाई खाई।\n\nSabne mithai khayi.\n\n(Everyone ate sweets.)',
            },
            {
                'page_number': 5,
                'text_content': 'दीवाली मुबारक!\n\nDiwali Mubarak!\n\n(Happy Diwali!)',
            },
        ]
    },

    # STORY 4: Festival Story - Eid (Muslim)
    {
        'storyweaver_id': 'peppi-004',
        'title': 'ईद की खुशी',
        'title_translit': 'Eid ki Khushi (Joy of Eid)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A heartwarming story about celebrating Eid with family.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Festival', 'Eid', 'Muslim'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'आज ईद है!\n\nAaj Eid hai!\n\n(Today is Eid!)',
            },
            {
                'page_number': 2,
                'text_content': 'अब्बू ने नमाज़ पढ़ी।\n\nAbbu ne namaaz padhi.\n\n(Father offered prayers.)',
            },
            {
                'page_number': 3,
                'text_content': 'अम्मी ने सेवइयाँ बनाईं।\n\nAmmi ne sewaiyan banayin.\n\n(Mother made sweet vermicelli.)',
            },
            {
                'page_number': 4,
                'text_content': 'सबने गले मिले।\n\nSabne gale mile.\n\n(Everyone hugged each other.)',
            },
            {
                'page_number': 5,
                'text_content': 'ईद मुबारक!\n\nEid Mubarak!\n\n(Happy Eid!)',
            },
        ]
    },

    # STORY 5: Festival Story - Gurpurab (Sikh)
    {
        'storyweaver_id': 'peppi-005',
        'title': 'गुरु का प्रकाश',
        'title_translit': 'Guru ka Prakash (Light of the Guru)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A story about celebrating Gurpurab and the spirit of seva.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Festival', 'Gurpurab', 'Sikh'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'आज गुरपुरब है!\n\nAaj Gurpurab hai!\n\n(Today is Gurpurab!)',
            },
            {
                'page_number': 2,
                'text_content': 'हरप्रीत गुरुद्वारा गई।\n\nHarpreet Gurudwara gayi.\n\n(Harpreet went to the Gurudwara.)',
            },
            {
                'page_number': 3,
                'text_content': 'उसने लंगर में सेवा की।\n\nUsne langar mein seva ki.\n\n(She did service in the langar.)',
            },
            {
                'page_number': 4,
                'text_content': 'सबको खाना मिला।\n\nSabko khana mila.\n\n(Everyone got food.)',
            },
            {
                'page_number': 5,
                'text_content': 'सेवा में खुशी है।\n\nSeva mein khushi hai.\n\n(There is joy in service.)',
            },
        ]
    },

    # STORY 6: Festival Story - Christmas (Christian)
    {
        'storyweaver_id': 'peppi-006',
        'title': 'क्रिसमस का तारा',
        'title_translit': 'Christmas ka Taara (The Christmas Star)',
        'language': 'HINDI',
        'level': 1,
        'synopsis': 'A joyful story about celebrating Christmas.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Festival', 'Christmas', 'Christian'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'आज क्रिसमस है!\n\nAaj Christmas hai!\n\n(Today is Christmas!)',
            },
            {
                'page_number': 2,
                'text_content': 'मैरी ने पेड़ सजाया।\n\nMary ne ped sajaya.\n\n(Mary decorated the tree.)',
            },
            {
                'page_number': 3,
                'text_content': 'ऊपर एक तारा चमका।\n\nUpar ek taara chamka.\n\n(A star shone on top.)',
            },
            {
                'page_number': 4,
                'text_content': 'सबने कैरोल गाए।\n\nSabne carol gaaye.\n\n(Everyone sang carols.)',
            },
            {
                'page_number': 5,
                'text_content': 'मेरी क्रिसमस!\n\nMerry Christmas!\n\n(Merry Christmas!)',
            },
        ]
    },

    # =========================================================================
    # LEVEL 2 - ELEMENTARY (Ages 6-8) - Longer sentences, more vocabulary
    # =========================================================================

    # STORY 7: Panchatantra - Universal wisdom
    {
        'storyweaver_id': 'peppi-007',
        'title': 'एकता में शक्ति',
        'title_translit': 'Ekta mein Shakti (Unity is Strength)',
        'language': 'HINDI',
        'level': 2,
        'synopsis': 'The classic Panchatantra story about pigeons who escape a hunter through unity.',
        'author': 'Peppi Academy (adapted from Panchatantra)',
        'illustrator': 'Peppi Academy',
        'categories': ['Panchatantra', 'Values', 'Wisdom'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'एक जंगल में बहुत सारे कबूतर रहते थे। उनका राजा था चित्रग्रीव।\n\n(Many pigeons lived in a forest. Their king was Chitragriva.)',
            },
            {
                'page_number': 2,
                'text_content': 'एक दिन एक शिकारी ने जाल बिछाया। उसमें दाने डाले।\n\n(One day a hunter spread a net. He put grains in it.)',
            },
            {
                'page_number': 3,
                'text_content': 'कबूतर दाने खाने आए। सब जाल में फंस गए!\n\n(Pigeons came to eat the grains. They all got trapped in the net!)',
            },
            {
                'page_number': 4,
                'text_content': 'चित्रग्रीव ने कहा - "घबराओ नहीं! सब मिलकर उड़ेंगे!"\n\n(Chitragriva said - "Don\'t panic! We will fly together!")',
            },
            {
                'page_number': 5,
                'text_content': 'सब कबूतरों ने एक साथ उड़ान भरी। जाल उनके साथ उठ गया!\n\n(All pigeons flew together. The net lifted with them!)',
            },
            {
                'page_number': 6,
                'text_content': 'शिकारी देखता रह गया। कबूतर आज़ाद हो गए।\n\n(The hunter kept watching. The pigeons became free.)',
            },
            {
                'page_number': 7,
                'text_content': 'सीख: एकता में बड़ी शक्ति होती है।\n\n(Moral: There is great strength in unity.)',
            },
        ]
    },

    # STORY 8: Regional Story - Kerala
    {
        'storyweaver_id': 'peppi-008',
        'title': 'केरल की नाव',
        'title_translit': 'Kerala ki Naav (The Boat of Kerala)',
        'language': 'HINDI',
        'level': 2,
        'synopsis': 'A story about the beautiful backwaters of Kerala and a boat ride.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Regional', 'Kerala', 'Nature'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'अनु केरल में अपनी नानी के घर आई थी।\n\n(Anu had come to her grandmother\'s house in Kerala.)',
            },
            {
                'page_number': 2,
                'text_content': 'नानी ने कहा - "चलो, बैकवाटर में नाव की सैर करें!"\n\n(Grandma said - "Let\'s go for a boat ride in the backwaters!")',
            },
            {
                'page_number': 3,
                'text_content': 'नाव धीरे-धीरे चलने लगी। चारों ओर हरे नारियल के पेड़ थे।\n\n(The boat started moving slowly. There were green coconut trees all around.)',
            },
            {
                'page_number': 4,
                'text_content': 'मछुआरे जाल डाल रहे थे। पक्षी उड़ रहे थे।\n\n(Fishermen were casting nets. Birds were flying.)',
            },
            {
                'page_number': 5,
                'text_content': 'नानी ने कहा - "यह है भगवान का अपना देश!"\n\n(Grandma said - "This is God\'s own country!")',
            },
            {
                'page_number': 6,
                'text_content': 'अनु को केरल बहुत पसंद आया।\n\n(Anu loved Kerala very much.)',
            },
        ]
    },

    # STORY 9: Regional Story - Rajasthan
    {
        'storyweaver_id': 'peppi-009',
        'title': 'राजस्थान का ऊँट',
        'title_translit': 'Rajasthan ka Oont (The Camel of Rajasthan)',
        'language': 'HINDI',
        'level': 2,
        'synopsis': 'A story about the desert state and its ships - the camels.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Regional', 'Rajasthan', 'Animals'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'राजस्थान में रेत के बड़े-बड़े टीले हैं।\n\n(Rajasthan has big sand dunes.)',
            },
            {
                'page_number': 2,
                'text_content': 'वहाँ ऊँट रहते हैं। ऊँट को "रेगिस्तान का जहाज" कहते हैं।\n\n(Camels live there. Camels are called "ships of the desert.")',
            },
            {
                'page_number': 3,
                'text_content': 'छोटू एक ऊँट था। वह बहुत मेहनती था।\n\n(Chhotu was a camel. He was very hardworking.)',
            },
            {
                'page_number': 4,
                'text_content': 'वह लोगों को एक गाँव से दूसरे गाँव ले जाता था।\n\n(He would take people from one village to another.)',
            },
            {
                'page_number': 5,
                'text_content': 'छोटू बिना पानी के भी कई दिन चल सकता था।\n\n(Chhotu could walk for many days without water.)',
            },
            {
                'page_number': 6,
                'text_content': 'सब छोटू से प्यार करते थे। वह सबका दोस्त था।\n\n(Everyone loved Chhotu. He was everyone\'s friend.)',
            },
        ]
    },

    # STORY 10: Northeast India - Assam
    {
        'storyweaver_id': 'peppi-010',
        'title': 'असम का एक सींग वाला गैंडा',
        'title_translit': 'Assam ka Ek Seeng wala Gainda (The One-Horned Rhino of Assam)',
        'language': 'HINDI',
        'level': 2,
        'synopsis': 'A story about the famous one-horned rhinoceros of Kaziranga.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Regional', 'Assam', 'Northeast', 'Wildlife'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'असम में काज़ीरंगा नाम का एक जंगल है।\n\n(There is a forest called Kaziranga in Assam.)',
            },
            {
                'page_number': 2,
                'text_content': 'यहाँ एक खास जानवर रहता है - एक सींग वाला गैंडा!\n\n(A special animal lives here - the one-horned rhino!)',
            },
            {
                'page_number': 3,
                'text_content': 'रिनो बहुत बड़ा था। उसकी त्वचा मोटी थी।\n\n(Rhino was very big. His skin was thick.)',
            },
            {
                'page_number': 4,
                'text_content': 'वह घास खाता था और कीचड़ में खेलता था।\n\n(He ate grass and played in the mud.)',
            },
            {
                'page_number': 5,
                'text_content': 'जंगल के लोग उसकी रक्षा करते हैं।\n\n(Forest people protect him.)',
            },
            {
                'page_number': 6,
                'text_content': 'गैंडा भारत का गौरव है।\n\n(The rhino is India\'s pride.)',
            },
        ]
    },

    # =========================================================================
    # LEVEL 3 - INTERMEDIATE (Ages 8-10) - Complex sentences, rich vocabulary
    # =========================================================================

    # STORY 11: Historical - Freedom Fighter
    {
        'storyweaver_id': 'peppi-011',
        'title': 'भगत सिंह का साहस',
        'title_translit': 'Bhagat Singh ka Saahas (Bhagat Singh\'s Courage)',
        'language': 'HINDI',
        'level': 3,
        'synopsis': 'An inspiring story about the brave freedom fighter Bhagat Singh.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['History', 'Freedom Fighter', 'Courage'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'भगत सिंह का जन्म पंजाब के एक छोटे से गाँव में हुआ था।\n\n(Bhagat Singh was born in a small village in Punjab.)',
            },
            {
                'page_number': 2,
                'text_content': 'बचपन से ही वे बहुत बहादुर थे। उन्हें देश से बहुत प्यार था।\n\n(From childhood, he was very brave. He loved his country very much.)',
            },
            {
                'page_number': 3,
                'text_content': 'उन दिनों भारत पर अंग्रेजों का राज था। लोग आज़ादी चाहते थे।\n\n(In those days, British ruled India. People wanted freedom.)',
            },
            {
                'page_number': 4,
                'text_content': 'भगत सिंह ने कहा - "मैं अपने देश के लिए कुछ भी करूँगा!"\n\n(Bhagat Singh said - "I will do anything for my country!")',
            },
            {
                'page_number': 5,
                'text_content': 'उन्होंने आज़ादी की लड़ाई में अपना जीवन दे दिया।\n\n(He gave his life in the fight for freedom.)',
            },
            {
                'page_number': 6,
                'text_content': 'आज भी हम उन्हें "शहीद भगत सिंह" कहते हैं। वे हमारे नायक हैं।\n\n(Even today we call him "Shaheed Bhagat Singh". He is our hero.)',
            },
            {
                'page_number': 7,
                'text_content': '"इंकलाब ज़िंदाबाद" - यह उनका नारा था।\n\n("Long Live Revolution" - This was his slogan.)',
            },
        ]
    },

    # STORY 12: Science - Indian Scientist
    {
        'storyweaver_id': 'peppi-012',
        'title': 'APJ अब्दुल कलाम का सपना',
        'title_translit': 'APJ Abdul Kalam ka Sapna (APJ Abdul Kalam\'s Dream)',
        'language': 'HINDI',
        'level': 3,
        'synopsis': 'An inspiring story about Dr. APJ Abdul Kalam, the Missile Man of India.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Science', 'Biography', 'Inspiration'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'तमिलनाडु के रामेश्वरम में एक गरीब परिवार में अब्दुल कलाम का जन्म हुआ।\n\n(Abdul Kalam was born in a poor family in Rameswaram, Tamil Nadu.)',
            },
            {
                'page_number': 2,
                'text_content': 'बचपन में वे अखबार बेचते थे। पर पढ़ाई में बहुत होशियार थे।\n\n(As a child, he sold newspapers. But he was very bright in studies.)',
            },
            {
                'page_number': 3,
                'text_content': 'उनका सपना था - भारत के लिए रॉकेट बनाना।\n\n(His dream was - to make rockets for India.)',
            },
            {
                'page_number': 4,
                'text_content': 'बड़े होकर वे वैज्ञानिक बने। उन्होंने भारत के लिए मिसाइल बनाई।\n\n(He grew up to become a scientist. He made missiles for India.)',
            },
            {
                'page_number': 5,
                'text_content': 'लोगों ने उन्हें "मिसाइल मैन" कहा।\n\n(People called him the "Missile Man.")',
            },
            {
                'page_number': 6,
                'text_content': 'वे भारत के राष्ट्रपति भी बने। बच्चों से उन्हें बहुत प्यार था।\n\n(He also became the President of India. He loved children very much.)',
            },
            {
                'page_number': 7,
                'text_content': 'उनका संदेश था - "सपने देखो और उन्हें पूरा करो!"\n\n(His message was - "Dream and fulfill your dreams!")',
            },
        ]
    },

    # STORY 13: Jataka Tale - Buddhist wisdom
    {
        'storyweaver_id': 'peppi-013',
        'title': 'बुद्धिमान हाथी',
        'title_translit': 'Buddhimaan Haathi (The Wise Elephant)',
        'language': 'HINDI',
        'level': 3,
        'synopsis': 'A Jataka tale about a wise elephant who saves his herd.',
        'author': 'Peppi Academy (adapted from Jataka Tales)',
        'illustrator': 'Peppi Academy',
        'categories': ['Jataka', 'Buddhist', 'Wisdom'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'बहुत समय पहले एक जंगल में हाथियों का एक बड़ा झुंड रहता था।\n\n(Long ago, a large herd of elephants lived in a forest.)',
            },
            {
                'page_number': 2,
                'text_content': 'उनका मुखिया था एक बूढ़ा और बुद्धिमान हाथी।\n\n(Their leader was an old and wise elephant.)',
            },
            {
                'page_number': 3,
                'text_content': 'एक बार भयंकर सूखा पड़ा। पानी और घास ख़त्म हो गई।\n\n(Once there was a terrible drought. Water and grass ran out.)',
            },
            {
                'page_number': 4,
                'text_content': 'बूढ़े हाथी ने अपनी याददाश्त पर ज़ोर दिया। उसे एक झील याद आई।\n\n(The old elephant thought hard. He remembered a lake.)',
            },
            {
                'page_number': 5,
                'text_content': '"मुझे पता है पानी कहाँ है! मेरे पीछे आओ!" उसने कहा।\n\n("I know where water is! Follow me!" he said.)',
            },
            {
                'page_number': 6,
                'text_content': 'सब हाथी उसके पीछे चले। कई दिनों की यात्रा के बाद झील मिल गई!\n\n(All elephants followed him. After many days of travel, they found the lake!)',
            },
            {
                'page_number': 7,
                'text_content': 'सबकी जान बच गई। अनुभव और बुद्धि की जीत हुई।\n\n(Everyone\'s life was saved. Experience and wisdom won.)',
            },
        ]
    },

    # STORY 14: Akbar-Birbal (Mughal era wisdom)
    {
        'storyweaver_id': 'peppi-014',
        'title': 'बीरबल की चतुराई',
        'title_translit': 'Birbal ki Chaturai (Birbal\'s Cleverness)',
        'language': 'HINDI',
        'level': 3,
        'synopsis': 'A classic Akbar-Birbal story showing wisdom and wit.',
        'author': 'Peppi Academy (adapted from folk tales)',
        'illustrator': 'Peppi Academy',
        'categories': ['Akbar-Birbal', 'Mughal', 'Wit'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'बादशाह अकबर के दरबार में बीरबल सबसे बुद्धिमान थे।\n\n(In Emperor Akbar\'s court, Birbal was the wisest.)',
            },
            {
                'page_number': 2,
                'text_content': 'एक दिन अकबर ने पूछा - "बीरबल, शहर में कितने कौवे हैं?"\n\n(One day Akbar asked - "Birbal, how many crows are in the city?")',
            },
            {
                'page_number': 3,
                'text_content': 'सब सोच में पड़ गए। यह तो असंभव सवाल था!\n\n(Everyone was puzzled. This was an impossible question!)',
            },
            {
                'page_number': 4,
                'text_content': 'बीरबल ने मुस्कुराते हुए कहा - "जहाँपनाह, शहर में 95,463 कौवे हैं।"\n\n(Birbal smiled and said - "Your Majesty, there are 95,463 crows in the city.")',
            },
            {
                'page_number': 5,
                'text_content': 'अकबर ने पूछा - "अगर गिनती ज़्यादा या कम निकली तो?"\n\n(Akbar asked - "What if the count is more or less?")',
            },
            {
                'page_number': 6,
                'text_content': 'बीरबल बोले - "कम हों तो कुछ रिश्तेदारों से मिलने गए होंगे।\nज़्यादा हों तो कुछ मेहमान आए होंगे!"\n\n(Birbal said - "If less, some must have gone to visit relatives.\nIf more, some guests must have come!")',
            },
            {
                'page_number': 7,
                'text_content': 'अकबर हँस पड़े। बीरबल की बुद्धि का कोई जवाब नहीं था!\n\n(Akbar laughed. There was no match for Birbal\'s wisdom!)',
            },
        ]
    },

    # =========================================================================
    # LEVEL 4 - ADVANCED (Ages 10-12) - Complex narratives
    # =========================================================================

    # STORY 15: Women in History
    {
        'storyweaver_id': 'peppi-015',
        'title': 'रानी लक्ष्मीबाई की वीरता',
        'title_translit': 'Rani Lakshmibai ki Veerta (The Valor of Rani Lakshmibai)',
        'language': 'HINDI',
        'level': 4,
        'synopsis': 'The inspiring story of the brave Queen of Jhansi.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['History', 'Women', 'Freedom Fighter'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'रानी लक्ष्मीबाई झाँसी की महारानी थीं। वे बचपन से ही बहादुर थीं।\n\n(Rani Lakshmibai was the Queen of Jhansi. She was brave since childhood.)',
            },
            {
                'page_number': 2,
                'text_content': 'उन्होंने घुड़सवारी, तलवारबाज़ी और धनुर्विद्या सीखी। वे किसी भी पुरुष से कम नहीं थीं।\n\n(She learned horse riding, sword fighting, and archery. She was no less than any man.)',
            },
            {
                'page_number': 3,
                'text_content': '1857 में जब अंग्रेज़ों ने झाँसी पर कब्ज़ा करना चाहा, रानी ने कहा - "मैं अपनी झाँसी नहीं दूँगी!"\n\n(In 1857, when the British wanted to capture Jhansi, the Queen said - "I will not give up my Jhansi!")',
            },
            {
                'page_number': 4,
                'text_content': 'उन्होंने अपनी सेना को इकट्ठा किया। महिलाओं को भी युद्ध के लिए तैयार किया।\n\n(She gathered her army. She also prepared women for war.)',
            },
            {
                'page_number': 5,
                'text_content': 'युद्ध में वे अपने घोड़े पर बैठकर, पीठ पर बच्चे को बाँधकर लड़ीं।\n\n(In battle, she fought on horseback with her child tied to her back.)',
            },
            {
                'page_number': 6,
                'text_content': 'अंग्रेज़ सेनापति ने कहा - "भारतीय विद्रोहियों में वह सबसे बहादुर थीं।"\n\n(The British general said - "She was the bravest among Indian rebels.")',
            },
            {
                'page_number': 7,
                'text_content': 'आज भी हम गाते हैं - "खूब लड़ी मर्दानी, वह तो झाँसी वाली रानी थी!"\n\n(Even today we sing - "She fought bravely like a man, she was the Queen of Jhansi!")',
            },
        ]
    },

    # STORY 16: Cultural Diversity - Unity in Diversity
    {
        'storyweaver_id': 'peppi-016',
        'title': 'भारत के रंग',
        'title_translit': 'Bharat ke Rang (Colors of India)',
        'language': 'HINDI',
        'level': 4,
        'synopsis': 'A story celebrating India\'s incredible diversity and unity.',
        'author': 'Peppi Academy',
        'illustrator': 'Peppi Academy',
        'categories': ['Diversity', 'Culture', 'Unity'],
        'pages': [
            {
                'page_number': 1,
                'text_content': 'भारत एक अनोखा देश है। यहाँ अलग-अलग धर्म, भाषाएँ और संस्कृतियाँ एक साथ रहती हैं।\n\n(India is a unique country. Different religions, languages, and cultures live together here.)',
            },
            {
                'page_number': 2,
                'text_content': 'उत्तर में हिमालय की बर्फीली चोटियाँ हैं। दक्षिण में नीला समुद्र है।\n\n(In the north are the snowy peaks of the Himalayas. In the south is the blue sea.)',
            },
            {
                'page_number': 3,
                'text_content': 'यहाँ हिंदू मंदिर जाते हैं, मुस्लिम मस्जिद जाते हैं, सिख गुरुद्वारा जाते हैं, ईसाई चर्च जाते हैं।\n\n(Here Hindus go to temples, Muslims go to mosques, Sikhs go to Gurudwaras, Christians go to churches.)',
            },
            {
                'page_number': 4,
                'text_content': 'दीवाली पर सब दीये जलाते हैं। ईद पर सब सेवइयाँ बाँटते हैं। क्रिसमस पर सब तोहफे देते हैं।\n\n(On Diwali everyone lights lamps. On Eid everyone shares vermicelli. On Christmas everyone gives gifts.)',
            },
            {
                'page_number': 5,
                'text_content': '22 भाषाएँ, सैकड़ों बोलियाँ - पर सबके दिल में एक ही धड़कन: "भारत माता की जय!"\n\n(22 languages, hundreds of dialects - but one heartbeat in all: "Victory to Mother India!")',
            },
            {
                'page_number': 6,
                'text_content': 'यही है भारत की खूबसूरती - अनेकता में एकता।\n\n(This is the beauty of India - Unity in Diversity.)',
            },
        ]
    },
]


def seed_stories():
    """Seed stories and their pages."""
    created_count = 0

    for story_data in STORIES:
        pages_data = story_data.pop('pages')

        story, created = Story.objects.get_or_create(
            storyweaver_id=story_data['storyweaver_id'],
            defaults={
                **story_data,
                'page_count': len(pages_data),
                'cover_image_url': f"https://peppiacademy.com/stories/covers/{story_data['storyweaver_id']}.jpg"
            }
        )

        if created:
            created_count += 1
            # Create pages
            for page_data in pages_data:
                StoryPage.objects.create(
                    story=story,
                    **page_data
                )
            # Use transliterated title for Windows console compatibility
            display_title = story.title_translit or story.storyweaver_id
            print(f"[+] Created: {display_title}")
        else:
            display_title = story.title_translit or story.storyweaver_id
            print(f"[=] Exists: {display_title}")

    print(f"\n{'='*50}")
    print(f"Stories seeded: {created_count} new, {len(STORIES) - created_count} existing")
    print(f"Total stories: {Story.objects.filter(storyweaver_id__startswith='peppi-').count()}")
    return created_count


if __name__ == '__main__':
    seed_stories()
