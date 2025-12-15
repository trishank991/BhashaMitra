# BhashaMitra - Complete Heritage Language Learning Platform

> **Version**: 2.0 | **Last Updated**: December 2024  
> **Mission**: Empower diaspora children to connect with their linguistic heritage through comprehensive, joyful learning

---

## 🎯 Project Overview

BhashaMitra is a **complete language learning platform** designed specifically for Indian diaspora children (ages 4-14) in New Zealand, Australia, and globally. Unlike generic language apps, BhashaMitra provides:

- **📚 Alphabets & Script Learning** - Learn Devanagari, Tamil, and other scripts
- **📖 Vocabulary Building** - 2000+ words with spaced repetition
- **✏️ Grammar Foundations** - Age-appropriate grammar lessons
- **📕 Story-Based Reading** - 53,000+ StoryWeaver stories
- **🗣️ Speaking & Pronunciation** - AI-powered feedback
- **🎮 Educational Games** - 10+ interactive game types
- **📊 Assessments & Certificates** - Track mastery and celebrate achievements

---

## 🌐 Target Languages

| Language | Script | Phase | Status |
|----------|--------|-------|--------|
| **Hindi** | Devanagari | Phase 1 | 🟢 MVP |
| **Tamil** | Tamil Script | Phase 2 | 🟡 Month 2-3 |
| **Gujarati** | Gujarati Script | Phase 3 | ⚪ Month 4 |
| **Punjabi** | Gurmukhi | Phase 3 | ⚪ Month 5 |
| **Telugu** | Telugu Script | Phase 4 | ⚪ Month 6 |
| **Malayalam** | Malayalam Script | Phase 4 | ⚪ Month 7 |

---

## 👥 Target Users

| User Type | Age | Needs |
|-----------|-----|-------|
| **Children** | 4-14 | Fun, engaging learning with rewards |
| **Parents** | 25-50 | Progress tracking, curriculum control |
| **Grandparents** | 50+ | Voice recording contributions |
| **Teachers** | Any | Classroom management (B2B) |

---

## 🏗️ Technology Stack

### Backend (Django)
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Django 5.x | Core backend |
| **API** | Django REST Framework | RESTful API |
| **Database** | PostgreSQL (Supabase) | Data persistence |
| **Auth** | JWT (SimpleJWT) | Authentication |
| **Cache** | Redis | Session & API caching |
| **Storage** | Supabase Storage / R2 | Audio, images |

### External Services
| Service | Provider | Purpose |
|---------|----------|---------|
| **Stories** | StoryWeaver | 53,000+ CC stories |
| **TTS/STT** | Bhashini (Govt. India) | Speech services |
| **Email** | Resend | Transactional email |
| **Analytics** | PostHog | User analytics |
| **Monitoring** | Sentry | Error tracking |

### Frontend (Separate Repo)
| Component | Technology |
|-----------|------------|
| **Framework** | Next.js 14 |
| **Styling** | Tailwind CSS + Shadcn/ui |
| **State** | Zustand + React Query |
| **Deployment** | Vercel |

---

## 📁 Documentation Structure

```
bhashamitra-docs/
├── README.md                           # This file - Project overview
├── IMPLEMENTATION/
│   ├── 01_COMPLETE_SETUP.md           # Full project setup guide
│   ├── 02_DATABASE_SCHEMA.md          # All 30+ models
│   ├── 03_API_SPECIFICATION.md        # Complete API endpoints
│   ├── 04_CURRICULUM_DESIGN.md        # Learning modules design
│   └── 05_DEPLOYMENT_GUIDE.md         # Production deployment
├── BUSINESS/
│   ├── BUSINESS_PLAN.md               # Business strategy
│   └── FEATURE_ROADMAP.md             # Feature timeline
└── DEVELOPMENT/
    ├── TESTING_STRATEGY.md            # QA approach
    └── CONTRIBUTING.md                # Contribution guidelines
```

---

## 📊 Complete Database Schema

### Core Models (8)
| Model | Purpose |
|-------|---------|
| `User` | Parent accounts |
| `Child` | Child profiles |
| `Story` | Cached stories from StoryWeaver |
| `StoryPage` | Individual story pages |
| `Progress` | Reading progress tracking |
| `DailyActivity` | Daily activity aggregation |
| `Badge` | Achievement definitions |
| `Streak` | Daily streak tracking |

### Curriculum Models (22)
| Category | Models |
|----------|--------|
| **Script/Alphabet** | Script, AlphabetCategory, Letter, Matra, LetterActivity, LetterProgress |
| **Vocabulary** | VocabularyTheme, VocabularyWord, WordProgress, FlashcardSession |
| **Grammar** | GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress |
| **Games** | Game, GameContent, GameSession, GameLeaderboard |
| **Assessment** | Assessment, AssessmentQuestion, AssessmentAttempt, Certificate |

**Total: 30+ Models**

---

## 🔌 Complete API Endpoints

### Authentication
```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/logout/
POST   /api/v1/auth/refresh/
GET    /api/v1/auth/me/
```

### Children Management
```
GET    /api/v1/children/
POST   /api/v1/children/
GET    /api/v1/children/{id}/
PATCH  /api/v1/children/{id}/
DELETE /api/v1/children/{id}/
GET    /api/v1/children/{id}/stats/
```

### Stories & Reading
```
GET    /api/v1/stories/?language=HINDI&level=1
GET    /api/v1/stories/{id}/
GET    /api/v1/stories/{id}/pages/
GET    /api/v1/children/{id}/progress/
POST   /api/v1/children/{id}/progress/action/
```

### Gamification
```
GET    /api/v1/children/{id}/badges/
GET    /api/v1/children/{id}/streak/
GET    /api/v1/children/{id}/level/
GET    /api/v1/children/{id}/recordings/
POST   /api/v1/children/{id}/recordings/
```

### Speech Services
```
POST   /api/v1/speech/tts/
POST   /api/v1/speech/stt/
```

### Curriculum - Alphabets
```
GET    /api/v1/scripts/
GET    /api/v1/scripts/{lang}/letters/
GET    /api/v1/scripts/{lang}/letters/{id}/
POST   /api/v1/children/{id}/letters/progress/
```

### Curriculum - Vocabulary
```
GET    /api/v1/vocabulary/themes/
GET    /api/v1/vocabulary/themes/{id}/words/
GET    /api/v1/children/{id}/vocabulary/due/
POST   /api/v1/children/{id}/vocabulary/review/
```

### Curriculum - Grammar
```
GET    /api/v1/grammar/topics/
GET    /api/v1/grammar/topics/{id}/
GET    /api/v1/grammar/topics/{id}/exercises/
POST   /api/v1/children/{id}/grammar/submit/
```

### Curriculum - Games
```
GET    /api/v1/games/
GET    /api/v1/games/{id}/
POST   /api/v1/children/{id}/games/start/
POST   /api/v1/children/{id}/games/end/
GET    /api/v1/games/{id}/leaderboard/
```

### Curriculum - Assessments
```
GET    /api/v1/assessments/
POST   /api/v1/children/{id}/assessments/start/
POST   /api/v1/children/{id}/assessments/submit/
GET    /api/v1/children/{id}/certificates/
```

---

## 📚 Learning Modules

### Module 1: Script & Alphabets (🔤)
**Goal**: Learn to recognize and write the script

| Component | Description |
|-----------|-------------|
| Letter Recognition | See letter, identify sound |
| Letter Tracing | Practice writing with guides |
| Letter Sounds | Audio pronunciation |
| Matra System | Vowel marks on consonants |
| Letter Games | Interactive learning |

**Hindi Devanagari**: 13 vowels + 33 consonants + matras

### Module 2: Vocabulary Building (📖)
**Goal**: Build a strong word foundation

| Component | Description |
|-----------|-------------|
| Thematic Lists | Family, Colors, Numbers, etc. |
| Flashcards | SRS-based spaced repetition |
| Audio | Native speaker pronunciation |
| Images | Visual association |
| Example Sentences | Contextual usage |

**Target**: 500+ words per language across 5 levels

### Module 3: Stories (📕)
**Goal**: Develop reading comprehension

| Component | Description |
|-----------|-------------|
| Story Library | 53,000+ StoryWeaver stories |
| Read-Along | TTS audio support |
| Comprehension | Story-based vocabulary |
| Voice Recording | Practice pronunciation |
| Progress Tracking | Pages, time, completion |

### Module 4: Grammar Foundations (✏️)
**Goal**: Understand sentence structure

| Component | Description |
|-----------|-------------|
| Rules | Age-appropriate explanations |
| Examples | Clear, relatable examples |
| Exercises | Fill-blank, reorder, translate |
| Progress | Track mastery per topic |

**Topics**: Sentence structure, Gender, Number, Pronouns, Verbs

### Module 5: Speaking & Pronunciation (🗣️)
**Goal**: Develop speaking confidence

| Component | Description |
|-----------|-------------|
| Listen & Repeat | Shadow native speakers |
| Pronunciation Feedback | STT-based scoring |
| Conversation Practice | Dialogue exercises |
| Family Recordings | Grandparent voice messages |

### Module 6: Games & Activities (🎮)
**Goal**: Make learning fun

| Game Type | Skills |
|-----------|--------|
| Memory Match | Vocabulary recall |
| Word Search | Letter recognition |
| Quiz Challenge | Mixed skills |
| Hangman | Spelling |
| Word Builder | Letter combination |
| Sentence Jumble | Grammar |
| Speed Round | Quick recall |

### Module 7: Assessments (📊)
**Goal**: Measure and certify progress

| Assessment Type | Purpose |
|-----------------|---------|
| Placement Test | Initial level determination |
| Level-Up Test | Advance to next level |
| Module Test | Topic mastery |
| Skill Assessment | Reading, Writing, etc. |
| Certificates | Shareable achievements |

---

## 🗺️ Implementation Timeline

### Phase 1: Foundation (Week 1-2) ✅
- [x] Django project setup
- [x] User authentication (JWT)
- [x] Child profile management
- [x] Core database models

### Phase 2: Stories & Progress (Week 2-3) ✅
- [x] StoryWeaver integration
- [x] Story caching system
- [x] Progress tracking
- [x] Basic gamification (points, badges, streaks)

### Phase 3: Speech Services (Week 3-4) ✅
- [x] Bhashini TTS integration
- [x] Bhashini STT integration
- [x] Voice recording storage

### Phase 4: Vocabulary Module (Week 4-5) 🔄
- [ ] Vocabulary theme models
- [ ] Spaced Repetition System (SRS)
- [ ] Flashcard API
- [ ] Vocabulary games

### Phase 5: Alphabet Module (Week 5-6) 🔄
- [ ] Script/Letter models
- [ ] Letter activities
- [ ] Tracing exercises
- [ ] Letter games

### Phase 6: Grammar Module (Week 6-7) ⏳
- [ ] Grammar topic models
- [ ] Exercise system
- [ ] Progress tracking

### Phase 7: Games Module (Week 7-8) ⏳
- [ ] Game framework
- [ ] 5+ game types
- [ ] Leaderboards

### Phase 8: Assessments (Week 8-9) ⏳
- [ ] Assessment system
- [ ] Certificate generation
- [ ] Level progression

### Phase 9: Polish & Launch (Week 9-10) ⏳
- [ ] UI/UX polish
- [ ] Performance optimization
- [ ] Security audit
- [ ] Production deployment

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for caching)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/bhashamitra-backend.git
cd bhashamitra-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py migrate

# Seed initial data
python manage.py seed_badges
python manage.py seed_hindi_alphabet  # Coming soon
python manage.py seed_vocabulary      # Coming soon

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
pytest -v
```

### Environment Variables

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=bhashamitra_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Bhashini API
BHASHINI_USER_ID=your-user-id
BHASHINI_API_KEY=your-api-key

# Storage (Production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

---

## 📈 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| User Registration | 500+ families | Month 1 |
| Daily Active Users | 40% of registered | Week 2+ |
| Story Completion | 50%+ started stories | Ongoing |
| Vocabulary Retention | 80%+ after 30 days | SRS tracking |
| Letter Mastery | 100% in 4 weeks | Progress tracking |
| Level Completion | 1 level per month | Assessment pass rate |
| Parent Satisfaction | 4.5/5 stars | In-app survey |

---

## 📄 License

MIT License - See LICENSE file for details.

StoryWeaver content used under CC 4.0 license with attribution.

---

## 🤝 Contributing

See CONTRIBUTING.md for guidelines on:
- Code contributions
- Content contributions (curriculum, translations)
- Voice recording contributions
- Bug reports and feature requests

---

## 📞 Contact

- **Founder**: Genius (Orvyn Consulting)
- **Email**: contact@bhashamitra.co.nz
- **Website**: https://bhashamitra.co.nz
