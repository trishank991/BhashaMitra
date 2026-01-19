# BhashaMitra - Complete Heritage Language Learning Platform

> **Version**: 3.0 | **Last Updated**: January 2025
> **Mission**: Empower diaspora children to connect with their linguistic heritage through comprehensive, joyful learning

---

## Project Overview

BhashaMitra is a **complete language learning platform** designed specifically for Indian diaspora children (ages 4-14) in New Zealand, Australia, and globally. Unlike generic language apps, BhashaMitra provides:

- **Alphabets & Script Learning** - Learn Devanagari, Tamil, and other scripts
- **Vocabulary Building** - 2000+ words with spaced repetition (SM-2 algorithm)
- **Grammar Foundations** - Age-appropriate grammar lessons
- **Story-Based Reading** - 53,000+ StoryWeaver stories
- **Speaking & Pronunciation** - Peppi Mimic with hybrid scoring
- **Educational Games** - 10+ interactive game types
- **Assessments & Certificates** - Track mastery and celebrate achievements
- **Peppi AI Tutor** - Gemini 2.0 powered conversational assistant
- **Viral Challenge System** - Shareable quizzes with leaderboards
- **Festival Activities** - Cultural learning through celebrations

---

## Target Languages

| Language | Script | Status |
|----------|--------|--------|
| **Hindi** | Devanagari | Active |
| **Tamil** | Tamil Script | Active |
| **Gujarati** | Gujarati Script | Active |
| **Punjabi** | Gurmukhi | Active |
| **Telugu** | Telugu Script | Active |
| **Malayalam** | Malayalam Script | Active |
| **Fiji Hindi** | Devanagari | Active |

---

## Technology Stack

### Backend (Django)
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Django 5.x | Core backend |
| **API** | Django REST Framework | RESTful API |
| **Database** | PostgreSQL (Supabase) | Data persistence |
| **Auth** | JWT (SimpleJWT) + Google OAuth | Authentication |
| **Deployment** | Render.com | Production hosting |

### External Services (CURRENT)
| Service | Provider | Purpose |
|---------|----------|---------|
| **Stories** | StoryWeaver | 53,000+ CC stories |
| **TTS (Primary)** | Hugging Face Indic Parler | Indian language TTS |
| **TTS (Fallback)** | Google Cloud TTS | Reliable fallback |
| **STT** | Google Cloud STT / Sarvam | Speech recognition |
| **AI Chat** | Google Gemini 2.0 Flash | Peppi AI conversations |
| **Payments** | Stripe | Subscription billing |
| **Email** | Resend | Transactional email |

> **Note**: Bhashini (Govt. India) is DEPRECATED. Current TTS chain: Cache → Hugging Face Indic Parler → Google Cloud TTS

### Frontend
| Component | Technology |
|-----------|------------|
| **Framework** | Next.js 14.2 (App Router) |
| **Language** | TypeScript 5.9 |
| **Styling** | Tailwind CSS 3.4 |
| **State** | Zustand 5.0 with persistence |
| **Deployment** | Vercel |

---

## Backend Architecture (23 Django Apps)

```
apps/
├── core/               - Base models, utilities, health checks
├── users/              - Authentication, subscription tiers
├── children/           - Child profiles
├── stories/            - StoryWeaver integration
├── speech/             - TTS/STT, Peppi Mimic pronunciation
├── challenges/         - Viral shareable quiz system
├── curriculum/         - L1-L10 comprehensive curriculum
├── peppi_chat/         - Peppi AI chatbot with moderation
├── gamification/       - Points, badges, streaks, Peppi evolution
├── family/             - Multi-child family grouping
├── payments/           - Stripe subscriptions
├── festivals/          - Cultural festivals with activities
├── progress/           - Learning progress tracking
├── parent_engagement/  - Parent dashboard features
├── live_classes/       - Live teaching sessions (premium)
├── analytics/          - Event tracking & cohorts
├── certifications/     - Achievement certificates
├── offline/            - Offline content support
├── referrals/          - User referral program
└── localization/       - Multi-language support
```

**Total: 103 Models, 147+ API Endpoints**

---

## Database Schema (Key Models)

### Core Models
| Model | Purpose |
|-------|---------|
| `User` | Parent accounts with subscription tiers |
| `Child` | Child profiles with language, level, Peppi preferences |
| `Story` / `StoryPage` | Cached StoryWeaver content |
| `Progress` | Reading progress tracking |
| `DailyActivity` | Daily activity aggregation |

### Gamification Models
| Model | Purpose |
|-------|---------|
| `Badge` / `ChildBadge` | Achievement badges |
| `Streak` | Daily streak tracking |
| `PeppiEvolution` | Peppi character evolution states |

### Speech & Mimic Models
| Model | Purpose |
|-------|---------|
| `AudioCache` | Permanent TTS audio storage |
| `VoiceCharacter` | Voice profiles (Peppi, Grandmother, Teacher) |
| `PeppiMimicChallenge` | Pronunciation practice words |
| `PeppiMimicAttempt` | Child's pronunciation recordings with scores |
| `PeppiMimicProgress` | Progress tracking per challenge |

### Challenge Models
| Model | Purpose |
|-------|---------|
| `Challenge` | Shareable 4-char code quizzes |
| `ChallengeAttempt` | Participant attempts (no auth needed) |
| `UserChallengeQuota` | Daily limits (FREE: 2, PAID: unlimited) |

### Curriculum Models
| Category | Models |
|----------|--------|
| **Levels** | CurriculumLevel, CurriculumModule, Lesson, LessonContent |
| **Alphabet** | Script, AlphabetCategory, Letter, Matra, LetterProgress |
| **Vocabulary** | VocabularyTheme, VocabularyWord, WordProgress |
| **Grammar** | GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress |
| **Games** | Game, GameSession, GameLeaderboard |
| **Assessment** | Assessment, AssessmentQuestion, AssessmentAttempt, Certificate |

### Peppi Chat Models
| Model | Purpose |
|-------|---------|
| `PeppiConversation` | Chat sessions with modes |
| `PeppiChatMessage` | Multi-language messages |
| `PeppiSafetyLog` | Content moderation audit |
| `PeppiChatUsage` | Rate limiting per child |

---

## Subscription Tiers

| Feature | FREE | STANDARD ($20/mo) | PREMIUM ($30/mo) |
|---------|------|-------------------|------------------|
| Challenges/day | 2 | Unlimited | Unlimited |
| Child profiles | 1 | 2+ | Unlimited |
| Stories | L1 only | All | All |
| TTS Provider | cache_only | Google Standard | Google WaveNet |
| Games/day | 2 | Unlimited | Unlimited |
| Peppi AI Chat | No | Yes | Yes |
| Live Classes/mo | 0 | 2 | Unlimited |
| Content Access | L1 browse | L1-current level | L1-L10 |

---

## API Endpoints Overview

### Authentication (13 endpoints)
```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/logout/
POST   /api/v1/auth/refresh/
POST   /api/v1/auth/google/
POST   /api/v1/auth/verify-email/
POST   /api/v1/auth/resend-verification/
POST   /api/v1/auth/password-reset/
POST   /api/v1/auth/password-reset/confirm/
GET    /api/v1/auth/me/
POST   /api/v1/auth/complete-onboarding/
GET    /api/v1/auth/subscription-tiers/
GET    /api/v1/auth/subscription/
```

### Challenges (9 endpoints)
```
# Public (no auth required)
GET/POST /api/v1/challenges/play/{code}/
POST     /api/v1/challenges/submit/
GET      /api/v1/challenges/leaderboard/{code}/

# Authenticated
GET/POST /api/v1/challenges/
GET      /api/v1/challenges/quota/
GET      /api/v1/challenges/categories/
GET      /api/v1/challenges/languages/
GET      /api/v1/challenges/{code}/
```

### Speech & Mimic (10+ endpoints)
```
POST   /api/v1/speech/tts/
GET    /api/v1/speech/stories/{uuid}/pages/{page}/audio/
POST   /api/v1/speech/upload-audio/
GET    /api/v1/speech/mimic/challenges/
GET    /api/v1/speech/mimic/challenges/{id}/
POST   /api/v1/speech/mimic/challenges/{id}/attempt/
GET    /api/v1/speech/mimic/progress/
PATCH  /api/v1/speech/mimic/attempts/{id}/share/
```

### Peppi Chat (8 endpoints)
```
GET/POST /api/v1/children/{child_id}/peppi-chat/
GET      /api/v1/children/{child_id}/peppi-chat/status/
GET      /api/v1/children/{child_id}/peppi-chat/{id}/
DELETE   /api/v1/children/{child_id}/peppi-chat/{id}/
POST     /api/v1/children/{child_id}/peppi-chat/{id}/messages/
POST     /api/v1/children/{child_id}/peppi-chat/{id}/end/
POST     /api/v1/children/{child_id}/peppi-chat/{id}/escalate/
```

### Curriculum (60+ endpoints)
```
# Levels & Modules
GET /api/v1/curriculum/levels/
GET /api/v1/curriculum/modules/{uuid}/lessons/
GET /api/v1/curriculum/lessons/{uuid}/

# Alphabet
GET /api/v1/curriculum/alphabet/scripts/
GET /api/v1/curriculum/alphabet/scripts/{uuid}/letters/

# Vocabulary
GET /api/v1/curriculum/vocabulary/themes/
GET /api/v1/curriculum/vocabulary/flashcards/due/
POST /api/v1/curriculum/vocabulary/flashcards/review/

# Grammar
GET /api/v1/curriculum/grammar/topics/
POST /api/v1/curriculum/grammar/exercises/{uuid}/submit/

# Games
GET /api/v1/curriculum/games/
POST /api/v1/curriculum/games/{uuid}/start/

# Assessments
GET /api/v1/curriculum/assessments/
POST /api/v1/curriculum/assessments/{uuid}/submit/
```

---

## Frontend Architecture

### State Management (8 Zustand Stores)
| Store | Purpose |
|-------|---------|
| `authStore` | Authentication, tokens, children |
| `progressStore` | XP, levels, badges, streaks |
| `peppiStore` | Peppi AI state, mood, preferences |
| `peppiChatStore` | Chat conversations, messages |
| `subscriptionStore` | Tier info, feature limits |
| `familyStore` | Family groups, invites |
| `parentStore` | Dashboard data |
| `offlineStore` | Offline queue |

### Key Pages
| Route | Feature |
|-------|---------|
| `/home` | Main dashboard with Peppi |
| `/learn/levels` | L1-L10 curriculum |
| `/learn/alphabet` | Script learning |
| `/learn/vocabulary` | Flashcards |
| `/learn/grammar` | Grammar exercises |
| `/stories` | Story library |
| `/games/{id}` | Interactive games |
| `/practice/mimic/{id}` | Pronunciation practice |
| `/challenges` | Create/manage quizzes |
| `/c/{code}` | Play shared quiz (public) |
| `/parent/dashboard` | Parent analytics |
| `/festivals` | Cultural activities |

---

## Peppi AI System

### Peppi Chat Modes
1. **HOMEWORK_HELP** - Answer questions about lessons
2. **CASUAL_CHAT** - Friendly conversation
3. **FESTIVAL_STORY** - Festival-themed storytelling

### Peppi Evolution
```
Kitten (0-500 XP) → Young Cat (500-2000 XP) → Adult Cat (2000-5000 XP) → Wise Cat (5000+ XP)
```

### Mimic Pronunciation Scoring (V2 Hybrid)
| Component | Weight |
|-----------|--------|
| STT Match | 50% |
| Text Match | 30% |
| Audio Energy | 15% |
| Duration Match | 5% |

**Star Thresholds**: 3 stars (85+), 2 stars (65-84), 1 star (40-64), 0 stars (<40)

---

## Environment Variables

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=bhashamitra.onrender.com

# Database (Supabase)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db.xxx.supabase.co
DB_PORT=5432

# Google AI (Peppi Chat)
GOOGLE_GEMINI_API_KEY=your-key
GEMINI_MODEL_ID=gemini-2.0-flash

# TTS Providers
GOOGLE_TTS_API_KEY=your-key
HUGGINGFACE_API_TOKEN=your-token
TTS_SPACE_ID=ai4bharat/indic-parler-tts

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Frontend
FRONTEND_URL=https://bhashamitra.app
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Node.js 18+

### Backend Setup
```bash
cd bhashamitra-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python manage.py migrate
python manage.py seed_all
python manage.py runserver
```

### Frontend Setup
```bash
cd bhashamitra-frontend
npm install
cp .env.example .env.local
# Edit .env.local
npm run dev
```

---

## Known Issues & Critical Gaps

See [CRITICAL_GAPS.md](./CRITICAL_GAPS.md) for:
- Mimic feature URL routing issues
- Challenge creation/leaderboard issues
- Grammar question generation issues

---

## Contact

- **Email**: contact@bhashamitra.co.nz
- **Website**: https://bhashamitra.app
