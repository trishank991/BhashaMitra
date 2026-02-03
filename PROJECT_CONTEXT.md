# BhashaMitra - Project Knowledge Base

> This file provides context and memory for the BhashaMitra project. It documents all decisions, configurations, and implementation details.


## Project Overview

**BhashaMitra** is a heritage language learning platform for Indian diaspora children (ages 4-14) in New Zealand/Australia. It teaches Indian languages through stories, games, and interactive curriculum.

**Owner**: Trishank
**Domain**: bhashamitra.co.nz
**Status**: MVP Development Phase

## Deployment (Dec 2024)

### Production URLs

| Service | Platform | URL |
|---------|----------|-----|
| **Backend API** | Render | https://bhashamitra.onrender.com |
| **Frontend** | Vercel | https://bhashamitra-frontend.vercel.app |
| **Database** | Render PostgreSQL | Internal connection via DATABASE_URL |

### Deployment Configuration

**Backend (Render):**
- Config file: `bhashamitra-backend/render.yaml`
- Build script: `bhashamitra-backend/build.sh`
- Start command: `gunicorn config.wsgi:application`
- Environment variables set in Render dashboard
- Auto-deploys from `develop` branch

**Frontend (Vercel):**
- Framework: Next.js (auto-detected)
- Root directory: `bhashamitra-frontend`
- Environment variable: `NEXT_PUBLIC_API_URL=https://bhashamitra.onrender.com/api/v1`
- Auto-deploys from `develop` branch

### Environment Variables (Production)

**Render (Backend):**
- `DJANGO_ENV=prod`
- `SECRET_KEY` (auto-generated)
- `DATABASE_URL` (from linked database)
- `ALLOWED_HOSTS=.onrender.com`
- `CORS_ALLOWED_ORIGINS=https://bhashamitra-frontend.vercel.app`

**Vercel (Frontend):**
- `NEXT_PUBLIC_API_URL=https://bhashamitra.onrender.com/api/v1`

---

## Git Workflow (Dec 2024)

### Branch Strategy

| Branch | Purpose | Deploys To |
|--------|---------|------------|
| `main` | Production-ready code | Production (manual) |
| `develop` | Integration & staging | Render + Vercel (auto) |
| `feature/*` | New features | Local only |
| `fix/*` | Bug fixes | Local only |
| `hotfix/*` | Urgent production fixes | Created from `main` |

### Development Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEVELOPMENT WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. LOCAL DEVELOPMENT (localhost)                                    │
│     ├── Backend: http://localhost:8000                               │
│     ├── Frontend: http://localhost:3000                              │
│     └── Test all changes thoroughly before committing                │
│                                                                      │
│  2. FEATURE BRANCH (local → GitHub)                                  │
│     ├── Create: git checkout -b feature/my-feature develop          │
│     ├── Commit: git commit -m "feat: description"                    │
│     └── Push: git push -u origin feature/my-feature                  │
│                                                                      │
│  3. PULL REQUEST → develop                                           │
│     ├── Create PR on GitHub: feature/* → develop                     │
│     ├── Code review & approval required                              │
│     └── Merge triggers auto-deploy to Render + Vercel                │
│                                                                      │
│  4. STAGING TEST (develop branch)                                    │
│     ├── Backend: https://bhashamitra.onrender.com                    │
│     ├── Frontend: https://bhashamitra-frontend.vercel.app            │
│     └── Full integration testing on staging                          │
│                                                                      │
│  5. PRODUCTION RELEASE (main branch)                                 │
│     ├── Create PR: develop → main                                    │
│     ├── Final review & approval                                      │
│     └── Merge to main = Production release                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Quick Reference Commands

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Work locally, test, then commit
git add .
git commit -m "feat: description"
git push -u origin feature/my-feature

# Create PR on GitHub: feature/my-feature → develop
# After PR approved and merged, changes auto-deploy to staging

# When ready for production:
# Create PR on GitHub: develop → main
# After approval, merge to main for production release
```

### Branch Commands

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Start bug fix
git checkout develop
git pull origin develop
git checkout -b fix/bug-description

# Merge feature to develop (via PR or locally)
git checkout develop
git merge feature/my-feature
git push origin develop

# Release to main (when ready)
git checkout main
git merge develop
git push origin main
```

### Commit Message Convention

```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Tests
- chore: Maintenance

Examples:
- feat(tts): add Sarvam AI provider
- fix(alphabet): correct Tamil letter audio playback
- docs(readme): update setup instructions
```

### Current Repository Status

- **Remote**: `origin` (GitHub)
- **Current Branch**: `develop`
- **Main Branch**: `main` (protected)

---

## Development Workflow Guidelines (Dec 2024)

### Two Senior Developers Model
This project uses a **parallel development approach** with two specialized developers working together:

| Role | Specialization | Codebase |
|------|----------------|----------|
| **Backend Developer** | Python/Django | `/bhashamitra-backend` |
| **Frontend Developer** | JavaScript/TypeScript/Next.js | `/bhashamitra-frontend` |

**When implementing features:**
1. Launch both backend and frontend work in parallel using Task agents when possible
2. Backend developer handles: Django models, APIs, services, database migrations
3. Frontend developer handles: React components, hooks, stores, UI/UX

### Decision-Making Process
Before recommending any solution or making architectural decisions:

1. **Thorough Investigation Required**
   - Read existing code first to understand patterns
   - Check how similar features are implemented elsewhere in the codebase
   - Verify assumptions by reading relevant files

2. **SWOT Analysis + Web Search**
   Before recommending any third-party service, library, or architectural approach:
   - Perform web search to get current information (pricing, features, alternatives)
   - Present SWOT analysis:
     - **S**trengths: What are the advantages?
     - **W**eaknesses: What are the limitations?
     - **O**pportunities: How does it help BhashaMitra specifically?
     - **T**hreats: What are the risks or concerns?
   - Include cost analysis where applicable
   - Let user make informed decision

3. **Verification Before Conclusions**
   - Don't assume features work without testing
   - Verify integrations by checking actual API responses
   - Test premium vs free tier differences explicitly
   - Check cache status and database state

### Example SWOT Format
```
## Recommendation: [Service/Library Name]

### SWOT Analysis

| Strengths | Weaknesses |
|-----------|------------|
| - Point 1 | - Point 1 |
| - Point 2 | - Point 2 |

| Opportunities | Threats |
|---------------|---------|
| - Point 1     | - Point 1 |
| - Point 2     | - Point 2 |

### Cost Analysis
- Free tier: ...
- Paid tier: ...
- Estimated monthly cost for BhashaMitra: ...

### Web Search Sources
- [Source 1](url)
- [Source 2](url)
```

## Tech Stack

### Backend (`/bhashamitra-backend`)
- **Framework**: Django 5.x + Django REST Framework 3.14+
- **Database**: SQLite (dev) / PostgreSQL (prod via Render)
- **Auth**: JWT (SimpleJWT)
- **Cache**: Redis (django-redis)
- **Storage**: Cloudflare R2 / AWS S3 (production)
- **TTS**: Svara TTS (free/standard) + Sarvam AI Bulbul V2 (premium)
- **Async Tasks**: Celery + Redis (optional)
- **Monitoring**: Sentry

### Frontend (`/bhashamitra-frontend`)
- **Framework**: Next.js 14.2 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 3.4
- **State**: Zustand 5.x
- **Animation**: Framer Motion 12.x
- **UI Components**: Headless UI

## Project Structure

```
BhashaMitra/
├── PROJECT_CONTEXT.md       # This file - project knowledge base
├── docs/                    # Project documentation
│   ├── BHASHAMITRA_README.md
│   ├── BHASHAMITRA_PROJECT_INDEX.md
│   ├── IMPLEMENTATION_PART1_CORE.md
│   ├── IMPLEMENTATION_PART2_FEATURES.md
│   ├── IMPLEMENTATION_PART3_CURRICULUM.md
│   ├── BHASHAMITRA_TTS_IMPLEMENTATION_GUIDE.md
│   ├── COST_FREE_BUILD_STRATEGY.md
│   └── django_implementation_guide.md
│
├── voice_samples/           # Voice samples for TTS voice cloning
│   └── hindi/               # Hindi voice samples (15 files)
│       ├── hindi_female_long_*.wav  # 10 female voice samples
│       ├── hindi_male_long_*.wav    # 5 male voice samples
│       └── sample_info.txt          # Transcriptions for each sample
│
├── indicf5_voices/          # Generated TTS outputs from IndicF5
│   ├── female_warm_sample_*.wav
│   ├── female_clear_sample_*.wav
│   └── male_deep_sample_*.wav
│
├── bhashamitra-backend/     # Django API backend
│   ├── apps/                # Django apps
│   │   ├── core/            # Base models, pagination, exceptions
│   │   ├── users/           # User authentication (custom User model)
│   │   ├── children/        # Child profiles management
│   │   ├── stories/         # StoryWeaver integration
│   │   ├── progress/        # Reading progress tracking
│   │   ├── gamification/    # Points, badges, streaks, levels
│   │   ├── speech/          # TTS/STT services
│   │   └── curriculum/      # Scripts, vocabulary, grammar, games, assessments
│   ├── config/              # Django settings (base, dev, prod)
│   ├── external/            # External API clients
│   │   ├── storyweaver/     # StoryWeaver API client
│   │   ├── huggingface/     # HuggingFace inference client
│   │   └── bhashini/        # Bhashini API client (future)
│   ├── scripts/             # Seed data scripts
│   ├── requirements/        # Python dependencies (base.txt, dev.txt)
│   ├── tests/               # Test files
│   ├── venv/                # Python virtual environment
│   ├── .env                 # Environment variables (NEVER COMMIT)
│   └── db.sqlite3           # SQLite database (dev)
│
└── bhashamitra-frontend/    # Next.js frontend
    ├── src/
    │   ├── app/             # Next.js App Router pages
    │   │   ├── page.tsx     # Landing page
    │   │   ├── login/       # Login page
    │   │   ├── register/    # Registration page
    │   │   ├── home/        # Child dashboard
    │   │   ├── stories/     # Story library
    │   │   ├── games/       # Games section
    │   │   ├── progress/    # Progress tracking
    │   │   └── profile/     # User profile
    │   ├── components/      # React components
    │   │   ├── ui/          # Base UI components (Button, Card, etc.)
    │   │   ├── layout/      # Layout components (Header, BottomNav)
    │   │   └── peppi/       # Peppi assistant character
    │   ├── stores/          # Zustand state stores
    │   │   ├── authStore.ts
    │   │   ├── progressStore.ts
    │   │   └── peppiStore.ts
    │   ├── lib/             # Utilities
    │   │   ├── api.ts       # API client
    │   │   ├── utils.ts     # Helper functions
    │   │   └── constants.ts
    │   └── types/           # TypeScript types
    ├── .env.local           # Frontend env vars (NEVER COMMIT)
    └── package.json
```

## Key Commands

### Backend
```bash
cd ~/BhashaMitra/bhashamitra-backend
source venv/bin/activate     # Activate virtual environment
python manage.py runserver   # Start dev server (port 8000)
python manage.py migrate     # Run migrations
python manage.py makemigrations  # Create new migrations
python manage.py check       # Verify Django configuration
python manage.py test        # Run Django tests
pytest -v                    # Run pytest tests
python manage.py createsuperuser  # Create admin user
python manage.py shell       # Django shell
```

### Frontend
```bash
cd ~/BhashaMitra/bhashamitra-frontend
npm run dev                  # Start dev server (port 3000)
npm run build                # Production build
npm run lint                 # Run linter
npm run start                # Start production server
```

### Quick Start (Both)
```bash
# Terminal 1 - Backend
cd ~/BhashaMitra/bhashamitra-backend && source venv/bin/activate && python manage.py runserver

# Terminal 2 - Frontend
cd ~/BhashaMitra/bhashamitra-frontend && npm run dev
```

## API Endpoints (Base: `/api/v1/`)

| Category | Endpoints |
|----------|-----------|
| Auth | `/auth/register/`, `/auth/login/`, `/auth/logout/`, `/auth/refresh/`, `/auth/me/` |
| Children | `/children/`, `/children/{id}/`, `/children/{id}/stats/` |
| Stories | `/stories/`, `/stories/{id}/`, `/stories/{id}/pages/` |
| Progress | `/children/{id}/progress/`, `/children/{id}/progress/action/` |
| Gamification | `/children/{id}/badges/`, `/children/{id}/streak/`, `/children/{id}/level/` |
| Speech | `/speech/tts/`, `/speech/stt/` |
| Curriculum | `/scripts/`, `/vocabulary/`, `/grammar/`, `/games/`, `/assessments/` |

## Django Apps Overview

| App | Purpose | Key Models |
|-----|---------|------------|
| `users` | Authentication | `User` (custom user model) |
| `children` | Child profiles | `Child` |
| `stories` | Story content | `Story`, `StoryPage` |
| `progress` | Reading tracking | `Progress`, `DailyActivity` |
| `gamification` | Rewards system | `Badge`, `ChildBadge`, `Streak` |
| `speech` | TTS/STT | `TTSUsageLog`, `VoiceRecording` |
| `curriculum` | Learning content | `Script`, `Letter`, `VocabularyWord`, `GrammarTopic`, `Game`, `Assessment` |

## Target Languages

| Language | Script | Priority | Status |
|----------|--------|----------|--------|
| Hindi | Devanagari | Phase 1 (MVP) | In Progress |
| Tamil | Tamil | Phase 2 | Planned |
| Gujarati | Gujarati | Phase 3 | Planned |
| Punjabi | Gurmukhi | Phase 3 | Planned |
| Telugu | Telugu | Phase 4 | Planned |
| Malayalam | Malayalam | Phase 4 | Planned |

## External Services

| Service | Purpose | Config Location |
|---------|---------|-----------------|
| Render PostgreSQL | Production database | `DATABASE_URL` in Render dashboard |
| HuggingFace Spaces | TTS (Svara TTS - free/standard) | `HUGGINGFACE_API_TOKEN` in .env |
| Sarvam AI | TTS (Bulbul V2 - premium tier) | `SARVAM_API_KEY` in .env |
| StoryWeaver | 53K+ CC-licensed stories | Public API |
| Cloudflare R2 | Media storage | `R2_*` vars in .env |
| Resend | Email service | `RESEND_API_KEY` in .env |
| Sentry | Error tracking | `SENTRY_DSN` in .env |
| Redis | Caching + Celery broker | `REDIS_URL` in .env |

## Environment Variables

### Backend (.env)
```bash
# Django
DJANGO_ENV=dev
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
USE_SQLITE=true              # Set to false for PostgreSQL
DB_NAME=bhashamitra_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# TTS (HuggingFace)
HUGGINGFACE_API_TOKEN=your-token
HUGGINGFACE_ACCOUNT_TYPE=free
TTS_SPACE_ID=parler-tts/parler_tts
TTS_CACHE_TTL_SECONDS=86400
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Security Rules

**NEVER commit these files:**
- `.env` (backend secrets)
- `.env.local` (frontend secrets)
- `*.pem`, `*.key` (certificates)
- `secrets.json`, `credentials.json`
- `db.sqlite3` (database file)

**API Keys to protect:**
- `SECRET_KEY` (Django)
- `HUGGINGFACE_API_TOKEN`
- `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`
- `RESEND_API_KEY`
- `SENTRY_DSN`
- Database credentials

## Development Guidelines

1. **Always activate venv** before backend work: `source venv/bin/activate`
2. **Run migrations** after model changes: `python manage.py makemigrations && python manage.py migrate`
3. **Check Django config** before committing: `python manage.py check`
4. **Test locally** before committing
5. **Follow existing code patterns** in each codebase
6. **Use TypeScript** for all frontend code
7. **UI should be colorful and child-friendly** - the target users are children ages 4-14

## Frontend Pages

| Route | Description | Status |
|-------|-------------|--------|
| `/` | Landing page | Implemented |
| `/login` | User login | Implemented |
| `/register` | User registration | Implemented |
| `/home` | **Child Dashboard** - Shows stats, streak, quick actions | Implemented |
| `/learn` | **Curriculum Dashboard** - Main learning hub | Implemented |
| `/learn/levels` | **Curriculum Levels** - L1-L10 learning journey | Implemented |
| `/learn/levels/[id]` | **Level Detail** - Modules within a level | Implemented |
| `/learn/modules/[id]` | **Module Detail** - Lessons within a module | Implemented |
| `/learn/lessons/[id]` | **Lesson Detail** - Lesson content and progress | Implemented |
| `/learn/alphabet` | **Alphabet Learning** - Hindi Devanagari letters | Implemented |
| `/learn/vocabulary` | **Vocabulary** - Word themes and flashcards | Implemented |
| `/learn/grammar` | **Grammar** - Grammar topics and rules | Implemented |
| `/stories` | Story library | Implemented |
| `/games` | Games section | Implemented |
| `/progress` | Progress & badges | Implemented |
| `/profile` | User profile | Implemented |
| `/family` | Parent Dashboard | **Not implemented** |
| `/peppi` | Peppi AI Chat | **Not implemented** |

### Child Dashboard (`/home`)
The main dashboard for children showing:
- Quick Stats (streak, stories read, words learned)
- Current language being learned
- Continue Learning section
- Quick Actions (Stories, Games, Badges, Profile)
- Daily Goal tracker

### Curriculum Dashboard (`/learn`)
Main learning hub with:
- Quick stats (letters, words, grammar topics)
- Study Materials grid (Alphabet, Vocabulary, Grammar, Stories)
- Daily Challenge tracker
- Continue Learning section

### Alphabet Page (`/learn/alphabet`)
Hindi Devanagari script learning:
- 10 Vowels (स्वर) with pronunciation
- 31 Consonants (व्यंजन) with pronunciation
- Interactive letter cards - tap to see details
- Progress tracking (0/49 letters)

### Vocabulary Page (`/learn/vocabulary`)
Word learning with themes:
- 8 themes (Family, Colors, Numbers, Animals, Food, Body Parts, Greetings, Actions)
- 80 total words with romanization and translation
- Sample word cards with Hindi script
- Fetches from backend API

### Grammar Page (`/learn/grammar`)
Grammar lessons:
- 5 topics (Sentence Structure, Gender, Pronouns, Verbs, Numbers)
- 6 rules with examples
- Expandable topic cards
- Quick grammar tips with Hindi examples

## Current Implementation Status

### Completed
- [x] Django project setup with modular settings
- [x] User authentication (JWT with SimpleJWT)
- [x] Child profile management
- [x] Core database models (30+ models)
- [x] StoryWeaver integration
- [x] Progress tracking system
- [x] Gamification (points, badges, streaks, levels)
- [x] TTS integration (Google Cloud TTS + Sarvam AI + Svara TTS)
- [x] Curriculum models (scripts, vocabulary, grammar, games, assessments)
- [x] Frontend base setup (Next.js 14, Tailwind, Zustand)
- [x] Frontend pages (login, register, home, stories, games, progress, profile)
- [x] UI components (Button, Card, Avatar, Badge, etc.)
- [x] Peppi assistant character (avatar component)
- [x] Games module gameplay (Letter Match, Match Pairs, Picture Word)
- [x] Audio playback for letters and words (integrated)
- [x] Visual vocabulary with images (110 Hindi words)
- [x] Age-adaptive UI (3 variants: Junior, Standard, Teen)
- [x] Content validation system (VerifiedLetter, VerifiedWord models)
- [x] Parent Dashboard backend APIs
- [x] Sound effects system (12 sounds)
- [x] Animation components (Celebration, LevelUp, StarBurst, SuccessCheck)
- [x] Peppi narration for stories and songs

### In Progress / Not Yet Implemented
- [ ] Parent Dashboard frontend (`/parent/dashboard` - backend ready)
- [ ] Peppi AI Chat (models deployed, needs full integration)
- [ ] SRS Flashcard review system (backend ready, frontend needs review UI)
- [ ] Assessment system (tests/quizzes)
- [ ] Additional games (Word Builder, Spelling Bee - 2/8 remaining)

### Recently Completed (Dec 2024)
- [x] `/learn` - Curriculum dashboard page
- [x] `/learn/alphabet` - Hindi alphabet learning with 41 letters
- [x] `/learn/vocabulary` - Vocabulary themes display
- [x] `/learn/grammar` - Grammar topics display
- [x] API methods for curriculum endpoints in `api.ts`
- [x] Bottom navigation updated to include "Learn" link
- [x] **Language Selector Component** - Added to home page for switching learning language
- [x] **LanguageSelector.tsx** - New UI component with dropdown, flags, "Coming Soon" section
- [x] **updateActiveChildLanguage** - New method in authStore to update child's language via API
- [x] **Fixed huggingface_hub import error** - Upgraded from 0.36.0 to 1.2.2
- [x] **TTS Testing** - Tested Svara TTS and AI4Bharat IndicF5 voice cloning
- [x] **Voice Samples Downloaded** - 15 Hindi voice samples for IndicF5 reference audio
- [x] **IndicF5 Integration Test** - Successfully generated TTS with 3 different voices

### Week 2-4 Implementation (Dec 2024)

**Summary**: During weeks 2-4 of December 2024, BhashaMitra evolved from a UI shell to a functional learning platform. Major achievements include implementing 3 new interactive games, adding visual vocabulary support with 110+ images, creating an age-adaptive UI system with 3 variants, building a content validation system, integrating sound effects and animations, and developing backend APIs for parent dashboard.

**Key Metrics:**
- Games: 2 → 5 (Letter Match, Match Pairs, Picture Word added)
- Vocabulary images: 0 → 110 Hindi words with Unsplash images
- Sound effects: 0 → 12 interactive sounds
- Animation components: 0 → 4 (Celebration, LevelUp, StarBurst, SuccessCheck)
- Age variants: 1 → 3 (Junior, Standard, Teen)
- Verified content: 0 → 41 Hindi letters seeded
- Frontend components created: 20+ new components
- Backend models added: 2 (VerifiedLetter, VerifiedWord)

#### Games System Enhancements
- **Letter Match Game** - Memory card game matching letters to sounds
  - Component: `src/components/games/LetterMatchGame.tsx`
  - Features: Card flip animations, sound effects, age-adaptive difficulty
  - Status: Fully playable

- **Match Pairs Game** - Two-column matching game with drag-and-drop
  - Component: `src/components/games/MatchPairsGame.tsx`
  - Features: Word-to-meaning matching, visual feedback
  - Status: Fully playable

- **Picture Word Game** - Image-based vocabulary game
  - Component: `src/components/games/PictureWordGame.tsx`
  - Features: 4-option multiple choice, image display, pronunciation audio
  - Status: Fully playable

- **Games Available**: 5/8 games implemented
  - ✅ Word Match, Listen & Speak, Letter Match, Match Pairs, Picture Word
  - ⏳ Word Builder, Spelling Bee, Story Builder (planned)

#### Visual Flashcard System
- **VisualFlashcard Component** - 3D flip animation with image support
  - File: `src/components/curriculum/VisualFlashcard.tsx`
  - Features: Front/back flip, image display, romanization, translation
  - Age-adaptive sizing and animations

- **Vocabulary Images** - 110 Hindi words with Unsplash images
  - Database field: `VocabularyWord.image_url`
  - Seed command: `python manage.py seed_vocabulary_images`
  - Source: Unsplash API (free tier)
  - Coverage: All core themes (Family, Colors, Numbers, Animals, Food, Body Parts, Greetings, Actions)

#### Age-Adaptive UI System
- **useAgeConfig Hook** - Enhanced with 20+ age-specific properties
  - File: `src/hooks/useAgeConfig.ts`
  - Three variants: Junior (≤6), Standard (7-10), Teen (11+)
  - Properties: fontSize, spacing, colors, animations, content visibility, game difficulty, Peppi behavior

- **AgeThemeProvider** - Context provider for consistent theming
  - File: `src/components/layout/AgeThemeProvider.tsx`
  - Provides age-appropriate colors, spacing, font sizes throughout app

- **Age-Specific Differences**:
  - Junior (4-6): Large text, bright colors, high Peppi frequency, 3 options/question, no time limits
  - Standard (7-10): Medium text, balanced colors, medium Peppi, 4 options/question, optional time limits
  - Teen (11+): Compact UI, muted colors, low Peppi frequency, 4 options/question, time challenges

#### Content Validation System
- **VerifiedLetter Model** - Quality-checked alphabet letters
  - File: `apps/curriculum/models/verified_content.py`
  - Fields: character, romanization, pronunciation_guide, example_word, audio_url
  - Verification workflow: PENDING → VERIFIED/REJECTED/NEEDS_REVISION
  - Quality scores: pronunciation_accuracy, example_relevance (1-5)

- **VerifiedWord Model** - Quality-checked vocabulary words
  - Fields: word, romanization, translation, part_of_speech, gender, example_sentence, audio_url, image_url
  - Quality scores: translation_accuracy, cultural_appropriateness, age_appropriateness (1-5)
  - Supports multi-tier content curation

- **Hindi Letters Seeded** - 41 verified letters
  - Command: `python manage.py seed_verified_hindi`
  - Content: 10 vowels (स्वर), 31 consonants (व्यंजन)
  - All letters have romanization, pronunciation guides, example words

#### Alphabet Quiz System
- **AlphabetQuiz Component** - Quiz after learning sections
  - File: `src/components/curriculum/AlphabetQuiz.tsx`
  - Quiz types: sound-to-letter, letter-to-sound
  - Age-adaptive: 5-10 questions based on age
  - Features: Audio playback, multiple choice, immediate feedback
  - Peppi integration: Encouragement and hints

#### Parent Dashboard (Backend)
- **Parent Dashboard APIs**:
  - `GET /api/v1/parent/dashboard/` - Summary of all children's progress
  - `GET /api/v1/parent/children/{id}/progress/` - Detailed child progress
  - Response includes: lessons completed, streak days, vocabulary mastered, games played, recent activities

- **Frontend Page** (Partial):
  - Route: `/parent/dashboard`
  - File: `src/app/parent/dashboard/page.tsx`
  - Status: Backend complete, frontend UI in progress
  - Features planned: Child summaries, progress charts, recent activity feed

#### Sound Effects System
- **Sound Service** - 12 sound effects for interactions
  - File: `src/lib/soundService.ts`
  - Sounds: click, success, error, pop, whoosh, chime, levelUp, celebration, starCollect, streak, badge, achievement
  - Source: Public domain MP3 files (4.4 MB total)
  - Location: `public/audio/sounds/`

- **useSounds Hook** - React integration
  - File: `src/hooks/useSounds.ts`
  - Methods: onClick, onCorrect, onWrong, onLevelUp, onCelebration, onStreak, onBadge, onAchievement
  - Volume control, mute toggle, preloading

#### Animation Components
- **Celebration** - Confetti animation with sound
  - File: `src/components/animations/Celebration.tsx`
  - Triggers: Lesson completion, perfect score, milestone achievements

- **LevelUp** - Level progression animation
  - File: `src/components/animations/LevelUp.tsx`
  - Features: Badge reveal, sound effect, congratulatory message

- **StarBurst** - Streak milestone animation
  - File: `src/components/animations/StarBurst.tsx`
  - Usage: Daily streak achievements

- **SuccessCheck** - Checkmark animation for correct answers
  - File: `src/components/animations/SuccessCheck.tsx`
  - Instant feedback for quiz/game responses

#### Peppi Enhancements
- **PeppiFeedbackBubble** - Contextual feedback component
  - File: `src/components/peppi/PeppiFeedbackBubble.tsx`
  - Provides hints, encouragement, explanations
  - Age-adaptive language complexity

- **usePeppiFeedback Hook** - Feedback logic
  - File: `src/hooks/usePeppiFeedback.ts`
  - Random encouragement messages
  - Context-aware hints based on mistakes

### Recently Completed (Dec 26, 2024) - TTS & Bug Fixes

- [x] **Google Cloud TTS Integration** - Added `google-cloud-texttospeech` to render.txt for production
- [x] **Base64 Credentials Support** - Google credentials can be passed via `GOOGLE_CREDENTIALS_BASE64` env var
- [x] **Peppi Narration Fix** - Changed from file URLs to base64 audio response (fixes VARCHAR(64) cache_key error)
- [x] **TTS Pace Adjustment** - Sarvam AI pace changed from 0.5 → 0.7 (balanced for children)
- [x] **Grammar Section Fix** - Fixed useAudio hook circular dependency (`stopAudio` in dependency array)
- [x] **Grammar handlePlayExample Fix** - Wrapped in useCallback to prevent re-renders
- [x] **Songs Seed Files Fix** - Added `language` field to all song seed files (Hindi, Tamil, Punjabi, Fiji Hindi)
- [x] **STANDARD Tier TTS** - Fixed User model `tts_provider` property to give `google` TTS to STANDARD tier

**Files Modified:**
- `bhashamitra-backend/requirements/render.txt` - Added google-cloud-texttospeech
- `bhashamitra-backend/apps/speech/services/google_provider.py` - Base64 credentials support
- `bhashamitra-backend/apps/speech/services/sarvam_provider.py` - DEFAULT_PACE = 0.7
- `bhashamitra-backend/apps/speech/services/peppi_tts.py` - All voice configs pace = 0.7
- `bhashamitra-backend/apps/speech/peppi_views.py` - Return base64 audio instead of file URLs
- `bhashamitra-backend/apps/users/models.py` - tts_provider returns 'google' for STANDARD tier
- `bhashamitra-frontend/src/hooks/useAudio.ts` - Fixed circular dependency
- `bhashamitra-frontend/src/app/learn/grammar/[id]/page.tsx` - useCallback for handlePlayExample
- `bhashamitra-frontend/src/components/peppi/PeppiNarrator.tsx` - Handle base64 audio_data
- `bhashamitra-frontend/src/components/peppi/PeppiSongNarrator.tsx` - Handle base64 audio_data
- `bhashamitra-backend/apps/curriculum/management/commands/seed_*.py` - Added language field to songs

### Recently Completed (Dec 19, 2024) - Curriculum Architecture
- [x] **Curriculum Hierarchy Models** - CurriculumLevel, CurriculumModule, Lesson, LessonContent
- [x] **Progress Tracking Models** - LevelProgress, ModuleProgress, LessonProgress
- [x] **L1-L10 Levels Seeded** - All 10 levels with Hindi names, emojis, theme colors
- [x] **Curriculum API Endpoints** - Full CRUD for levels, modules, lessons, progress
- [x] **Frontend Curriculum Types** - TypeScript interfaces for curriculum hierarchy
- [x] **Frontend Curriculum Components** - ProgressRing, LevelCard, ModuleCard, LessonCard
- [x] **Frontend Curriculum Pages** - /learn/levels, /learn/levels/[id], /learn/modules/[id], /learn/lessons/[id]
- [x] **Child Model Update** - Extended level support from L1-L5 to L1-L10
- [x] **Learn Page Update** - Added "My Journey" link to /learn/levels

## TTS System

The TTS system uses a multi-provider approach via HuggingFace Spaces:

### Current Providers
1. **Primary**: Svara TTS (`kenpath/svara-tts`) - Best for Indian languages
2. **Fallback**: Parler TTS (`parler-tts/parler_tts`) - English fallback

### Tested Alternative: AI4Bharat IndicF5
**Status**: Tested and working (Dec 2024)
- **Space**: `ai4bharat/IndicF5`
- **Type**: Voice cloning TTS (requires reference audio)
- **Performance**: ~10s average generation (12x faster than Svara's ~129s)
- **Quality**: Higher quality, more natural sounding
- **Requirement**: Needs 5-15 second reference audio + transcription
- **HuggingFace Pro**: Required for higher GPU quotas

### Voice Samples for IndicF5
Pre-downloaded human voice samples for voice cloning:
- **Location**: `/home/trishank/BhashaMitra/voice_samples/hindi/`
- **Female voices**: 10 samples (15-24 seconds each)
- **Male voices**: 5 samples (15-19 seconds each)
- **Source**: IndicVoices dataset (open-source)

Sample files:
- `hindi_female_long_1.wav` to `hindi_female_long_10.wav`
- `hindi_male_long_1.wav` to `hindi_male_long_5.wav`
- `sample_info.txt` - Contains transcriptions for each sample

### Generated Voice Samples
Test outputs with IndicF5 voice cloning:
- **Location**: `/home/trishank/BhashaMitra/indicf5_voices/`
- Files: `female_warm_sample_*.wav`, `female_clear_sample_*.wav`, `male_deep_sample_*.wav`

### TTS Comparison Results (Dec 2024)
| Metric | Svara TTS | IndicF5 |
|--------|-----------|---------|
| Avg Gen Time | ~129s | ~10s |
| Requires Ref Audio | No | Yes |
| Voice Cloning | No | Yes |
| Languages | 12 Indian | 11 Indian |

Features:
- Supports 12 Indian languages
- Two-tier caching (memory + file/S3)
- Cost tracking and optimization
- No local GPU required (uses Gradio client)

### TTS Strategy Decision (Dec 2024)

**3-Tier Membership Model with Different TTS Providers:**

| Tier | Price | TTS Provider | Features |
|------|-------|--------------|----------|
| **Free** | $0 | Pre-cached Svara | Limited content, pre-generated audio only |
| **Standard** | $12/month | Svara TTS | All content, real-time generation |
| **Premium** | $20/month | Sarvam AI Bulbul V2 | Human-like voices, highest quality |

**Provider Details:**

1. **Google Cloud TTS (Primary for Peppi)**:
   - API: Google Cloud Text-to-Speech
   - Authentication: `GOOGLE_CREDENTIALS_BASE64` (base64-encoded JSON credentials)
   - WaveNet voices for premium quality
   - Speaking rate: 1.0 for stories, 0.85 for songs
   - Package: `google-cloud-texttospeech>=2.33.0` (in render.txt)

2. **Sarvam AI Bulbul V2 (Fallback)**:
   - API: `https://api.sarvam.ai/text-to-speech`
   - Model: `bulbul:v2`
   - Human-like voice quality, ~1.5s generation
   - **Pace: 0.7** (balanced for children - not too slow, not too fast)
   - Languages: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Odia
   - Cost: ~NZD $1.80/user/month estimated, ~$0.36 with 80% cache hit rate
   - **Selected Voices (Dec 2024):**
     - Female: **manisha** (clear, energetic) - primary voice for curriculum
     - Male: **abhilash** (friendly teacher voice)
   - Available voices (all tested, can switch anytime):
     - Female: anushka (warm), manisha (clear), vidya (expressive), arya (friendly)
     - Male: abhilash (friendly), karun (professional), hitesh (casual)

3. **Svara TTS (Legacy - Not actively used)**:
   - HuggingFace Space `kenpath/svara-tts`
   - ~50-70s per generation, slower than Sarvam
   - Supports 12 Indian languages

**Unit Economics Analysis:**
- Average kid reads 3 stories/day × 5 pages × 50 words = 750 words/day
- Monthly: 750 × 30 = 22,500 words
- With 80% cache hit rate: 4,500 new words/month
- Sarvam cost: ~4,500 chars × $0.0001/char = ~$0.45/user/month

**Future Vision (Post-MVP Validation):**
- Move to ElevenLabs voice cloning ($11/month for 100,000 chars)
- Hire professional Indian voice actors (male + female per language)
- Clone voices for authentic, culturally appropriate pronunciation
- Target: Miss Rachel-style engaging educational voices

**Environment Variables:**
```bash
# Google Cloud TTS (Primary)
GOOGLE_CREDENTIALS_BASE64=<base64-encoded-json-credentials>

# Sarvam AI TTS (Fallback)
SARVAM_API_KEY=your_key_here
```

**Provider Files:**
- `apps/speech/services/mms_provider.py` - Svara TTS provider
- `apps/speech/services/sarvam_provider.py` - Sarvam AI provider (to be created)
- `apps/speech/services/tts_service.py` - Main TTS service with tier routing

### Language Purity Rule (Dec 2024)

**CRITICAL**: Each language must use ONLY content in that language. Never mix languages in:
- TTS text sent to speech APIs
- Database content (pronunciation_guide, explanation, translation fields)
- Frontend UI text and connector words

**Bug Fixed (Dec 2024)**: Premium tier was sending `"க से கல்"` (Tamil letter + Hindi "से" + Tamil word) to TTS. Fixed to use Tamil connector: `"க, உதாரணமாக கல்"`.

**Language-Specific Connectors for Alphabet TTS:**

| Language | Connector Phrase | Example |
|----------|------------------|---------|
| Hindi | `से` (se) | `"अ से अनार"` |
| Tamil | `உதாரணமாக` (for example) | `"அ, உதாரணமாக அம்மா"` |
| Gujarati | `માટે` (for) | `"અ, ઉદાહરણ અનાર"` |
| Punjabi | `ਲਈ` (for) | `"ਅ, ਉਦਾਹਰਨ ਅਨਾਰ"` |
| Telugu | `కోసం` (for) | `"అ, ఉదాహరణ అమ్మ"` |
| Bengali | `জন্য` (for) | `"অ, উদাহরণ আম"` |
| Malayalam | `ഉദാഹരണം` (example) | `"അ, ഉദാഹരണം അമ്മ"` |

**When Adding New Languages:**
1. Define language-specific connector words in frontend alphabet page
2. Ensure all database seed data uses pure target language
3. Update `handlePlayLetter()` in `src/app/learn/alphabet/page.tsx`
4. Test TTS output contains no foreign language words

**Files to Check:**
- `bhashamitra-frontend/src/app/learn/alphabet/page.tsx` - TTS text construction
- `bhashamitra-backend/apps/curriculum/models.py` - Database fields
- Any seed data scripts for curriculum content

## Documentation

Full documentation is in `/docs/`:
- `BHASHAMITRA_README.md` - Complete project overview
- `BHASHAMITRA_PROJECT_INDEX.md` - Documentation index
- `IMPLEMENTATION_PART1_CORE.md` - Core implementation guide
- `IMPLEMENTATION_PART2_FEATURES.md` - Features implementation
- `IMPLEMENTATION_PART3_CURRICULUM.md` - Curriculum modules
- `BHASHAMITRA_TTS_IMPLEMENTATION_GUIDE.md` - TTS system guide
- `COST_FREE_BUILD_STRATEGY.md` - Zero-cost development approach
- `django_implementation_guide.md` - Django implementation guide

## Database Content (as of Dec 2024)

| Content Type | Count | Details |
|--------------|-------|---------|
| **Stories** | 12 total | Hindi: 5, Tamil: 3, Gujarati: 2, Punjabi: 2 |
| **Alphabets** | 49 letters | Hindi Devanagari script only |
| **Vocabulary** | 80 words | 8 themes (Family, Colors, Numbers, Animals, Food, Body Parts, Greetings, Actions) |
| **Grammar** | 6 rules | 5 topics (Sentence Structure, Gender, Pronouns, Verbs, Numbers) |

**Note**: StoryWeaver API currently returns 403 Forbidden. Sample stories were manually created. When API access is restored, run: `python manage.py sync_stories --language=HINDI --limit=50`

## IndicF5 TTS Usage

To use IndicF5 voice cloning with HuggingFace Pro:

```python
from gradio_client import Client, handle_file
from huggingface_hub import login

# Login with token from .env
login(token='your_hf_token')

# Connect to IndicF5
client = Client('ai4bharat/IndicF5')

# Generate speech with voice cloning
result = client.predict(
    text='नमस्ते! भाषामित्र में आपका स्वागत है।',
    ref_audio=handle_file('/path/to/voice_samples/hindi/hindi_female_long_5.wav'),
    ref_text='मेरा दूसरा प्रोडक्ट है साबुन जो मैंने...',  # transcription of ref_audio
    api_name='/synthesize_speech'
)
```

Reference audio requirements:
- Duration: 5-15 seconds
- Clear speech, minimal background noise
- Must provide accurate transcription

## Important Notes

### Curriculum Data Availability
- **Only Hindi has curriculum content** (alphabet, vocabulary, grammar)
- Other languages (Tamil, Telugu, etc.) have 0 curriculum items
- The Language Selector shows other languages as "Coming Soon"
- If user switches to non-Hindi language, curriculum pages will be empty

### Language Selector Behavior
- Located on `/home` page
- Only Hindi is selectable
- Tamil, Gujarati, Punjabi, Telugu, Malayalam, Bengali shown as "Coming Soon"
- Changing language updates the child profile via `PATCH /children/{id}/`

## Peppi Narrator & Festival Stories Strategy (Dec 2024)

### Peppi Character Overview

**Peppi** is a ragdoll cat AI tutor character that serves as the friendly guide and narrator for BhashaMitra.

**Character Design:**
- **Type**: Ragdoll cat (soft, friendly appearance)
- **Variants**: Gender-based variants to match cultural context
- **Visual Style**: Cute, animated, child-friendly

**Language-Specific Names:**
| Language | Male Version | Female Version |
|----------|--------------|----------------|
| Hindi | Peppi Bhaiya (पेप्पी भैया) | Peppi Didi (पेप्पी दीदी) |
| Tamil | Peppi Anna (பெப்பி அண்ணா) | Peppi Akka (பெப்பி அக்கா) |
| Telugu | Peppi Anna (పెప్పి అన్న) | Peppi Akka (పెప్పి అక్క) |
| Gujarati | Peppi Bhai (પેપ્પી ભાઈ) | Peppi Ben (પેપ્પી બેન) |
| Punjabi | Peppi Veerji (ਪੈਪੀ ਵੀਰਜੀ) | Peppi Bhainji (ਪੈਪੀ ਭੈਣਜੀ) |

### Peppi Voice Configuration

Uses Google Cloud TTS (primary) with Sarvam AI as fallback:

```python
# Peppi TTS priority:
# 1. Google Cloud TTS WaveNet (if GOOGLE_CREDENTIALS_BASE64 set)
# 2. Sarvam AI Bulbul V2 (fallback, pace: 0.7)

PEPPI_VOICE_CONFIG = {
    'HINDI': {
        'male': {'speaker': 'arvind', 'pitch': 0.4, 'pace': 0.7, 'model': 'bulbul:v2'},
        'female': {'speaker': 'anushka', 'pitch': 0.3, 'pace': 0.7, 'model': 'bulbul:v2'}
    },
    'TAMIL': {
        'male': {'speaker': 'kumar', 'pitch': 0.4, 'pace': 0.7, 'model': 'bulbul:v2'},
        'female': {'speaker': 'anushka', 'pitch': 0.3, 'pace': 0.7, 'model': 'bulbul:v2'}
    },
    # ... other languages use same pattern with pace: 0.7
}
```

**Peppi Narration Response Format (Dec 2024):**
- Returns audio as base64 data (not file URLs) to avoid ephemeral storage issues on Render
- Frontend converts base64 to blob URL for playback
- TTSService handles caching internally using text hash

### Peppi Home Page Story Time Feature (Dec 2024)

**User Flow:**
1. User sees floating Peppi character at bottom-right of home page
2. Clicking Peppi shows an action menu with "Story Time" option
3. Selecting "Story Time" navigates to `/festivals` page showing available festival stories
4. User selects a festival story (e.g., Diwali - Ramayana story)
5. Peppi narrates the story page-by-page using TTS

**Implementation:**
- `PeppiAssistant.tsx` - Modified to show action menu on click with "Story Time" option
- `peppiStore.ts` - Already has `startNarration()` and `stopNarration()` methods
- `/festivals` page - New page listing festivals with their stories
- `/festivals/[id]` page - Festival story reader with Peppi narration

**Components:**
```
src/components/peppi/
  PeppiAssistant.tsx    - Floating Peppi with action menu
  PeppiNarrator.tsx     - Story narration component (exists)
  PeppiAvatar.tsx       - Peppi character avatar (exists)

src/app/festivals/
  page.tsx              - Festival list page (NEW)
  [id]/page.tsx         - Festival story reader (NEW)
```

**API Integration:**
- `GET /api/v1/festivals/` - List festivals with their stories
- `GET /api/v1/festivals/{id}/` - Festival details with associated stories
- `POST /api/v1/speech/tts/` - Generate narration audio for story text

**Database Seeded:**
- Diwali festival with 6-page Ramayana story (Hindi)
- Command: `python manage.py seed_diwali`

### Festival Stories Curriculum

**Target**: ~100 festival stories covering 6 major religions practiced by Indian diaspora:

| Religion | Number of Festivals | Example Festivals |
|----------|---------------------|-------------------|
| Hindu | 15-20 | Diwali, Holi, Navratri, Ganesh Chaturthi, Raksha Bandhan |
| Muslim | 8-10 | Eid ul-Fitr, Eid ul-Adha, Muharram, Milad un-Nabi |
| Sikh | 8-10 | Baisakhi, Guru Nanak Jayanti, Lohri, Gurpurab |
| Christian | 5-8 | Christmas, Easter, Good Friday |
| Jain | 5-6 | Mahavir Jayanti, Paryushana, Diwali |
| Buddhist | 5-6 | Buddha Purnima, Vesak |

**Story Structure:**
- 3-5 pages per story
- Age-appropriate for 4-14 years
- Includes cultural context and moral lessons
- Available in all supported languages

### Free Story Sources (CC-BY 4.0 Licensed)

1. **StoryWeaver** (storyweaver.org.in)
   - 53,000+ free stories
   - API: `api.storyweaver.org.in`
   - License: CC-BY 4.0
   - Languages: All Indian languages supported

2. **Free Kids Books** (freekidsbooks.org)
   - Multicultural stories
   - PDF downloads available
   - CC-BY license

3. **SikhNet** (sikhnet.com)
   - Sikh history and festival stories
   - Free educational content

4. **Pratham Books** (prathambooks.org)
   - Indian children's literature
   - CC-BY 4.0 license

### Database Schema for Festivals

```sql
-- Festival model
CREATE TABLE festivals_festival (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_hindi VARCHAR(100),
    name_tamil VARCHAR(100),
    name_gujarati VARCHAR(100),
    name_punjabi VARCHAR(100),
    religion VARCHAR(20) NOT NULL,  -- HINDU, MUSLIM, SIKH, CHRISTIAN, JAIN, BUDDHIST
    description TEXT,
    typical_month INTEGER,  -- 1-12
    is_lunar_calendar BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Festival-Story junction
CREATE TABLE festivals_festivalstory (
    id SERIAL PRIMARY KEY,
    festival_id INTEGER REFERENCES festivals_festival(id),
    story_id INTEGER REFERENCES stories_story(id),
    is_primary BOOLEAN DEFAULT FALSE,
    UNIQUE(festival_id, story_id)
);

-- Narration audio cache for Peppi
CREATE TABLE stories_narrationaudio (
    id SERIAL PRIMARY KEY,
    story_id INTEGER REFERENCES stories_story(id),
    language VARCHAR(20) NOT NULL,
    peppi_gender VARCHAR(10) NOT NULL,  -- male, female
    audio_file VARCHAR(500) NOT NULL,
    duration_seconds FLOAT,
    provider VARCHAR(20) DEFAULT 'sarvam',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(story_id, language, peppi_gender)
);
```

### Peppi API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/festivals/` | GET | List all festivals (with language filter) |
| `/api/v1/festivals/{id}/` | GET | Festival details with stories |
| `/api/v1/festivals/upcoming/` | GET | Next 30 days of festivals |
| `/api/v1/festivals/{id}/stories/` | GET | Stories for a festival |
| `/api/v1/peppi/narrate/` | POST | Generate Peppi narration for text |
| `/api/v1/stories/{id}/narration/` | GET | Get pre-cached Peppi narration |

### Pre-caching Strategy

For premium users, pre-generate Peppi narrations:
1. Generate audio for all story pages in all languages
2. Cache both male and female Peppi variants
3. Store in Cloudflare R2 for fast delivery
4. Estimated storage: ~500MB for 100 stories × 4 languages × 2 genders

### Implementation Priority

**Phase 1 (MVP):**
- [ ] Create Festival model and admin
- [ ] Add 20 festival entries (5 major per religion)
- [ ] Integrate StoryWeaver API for festival stories
- [ ] Implement Peppi narration endpoint

**Phase 2:**
- [ ] Festival calendar with upcoming festivals
- [ ] Pre-cache narrations for top 50 stories
- [ ] Add Peppi character animations
- [ ] Festival-themed UI decorations

**Phase 3:**
- [ ] Full 100+ festival coverage
- [ ] Regional variant stories
- [ ] User preference for Peppi gender
- [ ] Interactive Peppi chat (AI powered)

### Files to Create/Modify

**Backend:**
- `apps/festivals/models.py` - Festival, FestivalStory models
- `apps/festivals/views.py` - Festival API views
- `apps/festivals/serializers.py` - DRF serializers
- `apps/speech/services/peppi_tts.py` - Peppi voice service
- `apps/stories/models.py` - Add NarrationAudio model

**Frontend:**
- `src/components/peppi/PeppiNarrator.tsx` - Peppi narration component
- `src/app/festivals/page.tsx` - Festival calendar page
- `src/app/festivals/[id]/page.tsx` - Festival detail page
- `src/stores/peppiStore.ts` - Update with narration state

---

## Strategy v3.0 Gap Features (Dec 2024)

The following features are planned for implementation based on the v3.0 Strategy document:

### Gap 1: Offline Mode (PWA)
- **Status**: Not implemented
- **Apps**: `apps/offline/` (new)
- **Models**: `OfflinePackage`, `ChildOfflineContent`
- **Frontend**: Service workers, IndexedDB, background sync

### Gap 2: Parent Engagement System
- **Status**: Not implemented
- **Apps**: `apps/parent_engagement/` (new)
- **Models**: `ParentPreferences`, `LearningGoal`, `WeeklyReport`, `ParentChildActivity`
- **Frontend**: `/family/` pages for goals, reports, settings

### Gap 3: Live Classes & Moderation
- **Status**: Not implemented
- **Apps**: `apps/live_classes/` (new)
- **Models**: `Teacher`, `LiveSession`, `SessionRating`, `SessionModerationLog`
- **External**: Daily.co or similar for WebRTC

### Gap 4: Teacher QA System
- **Status**: Not implemented
- **Models**: `TeacherCertification`, `TeacherQualityAudit`, `TeacherPerformanceMetrics`
- **Features**: Random audits, performance tiers, automatic probation

### Gap 5: Localization (NZ/AU/IN/UK/US)
- **Status**: Not implemented
- **Apps**: `apps/localization/` (new)
- **Models**: `MarketConfig`, `FestivalCalendar`
- **Features**: Multi-currency, regional pricing, local payment methods

### Gap 6: Referral System
- **Status**: Not implemented
- **Apps**: `apps/referrals/` (new)
- **Models**: `ReferralCode`, `Referral`, `AmbassadorProgram`
- **Features**: Viral referral loops, ambassador tiers

### Gap 7: Certification System
- **Status**: Not implemented
- **Apps**: `apps/certifications/` (new)
- **Models**: `CertificateTemplate`, `Certificate`, `AnnualProgressReport`
- **Features**: Shareable certificates, annual reports

### Gap 8: Age-Adaptive Peppi
- **Status**: Partially planned (Peppi exists, age variants don't)
- **Models**: `PeppiAgeVariant` (Junior 4-6, Standard 7-10, Teen 11-14)
- **Features**: Age-specific prompts, voice modifiers, personality traits

### Gap 9: Analytics Engine
- **Status**: Not implemented
- **Apps**: `apps/analytics/` (new)
- **Models**: `LessonAnalytics`, `CohortAnalytics`, `PeppiAnalytics`, `EventLog`
- **Features**: Founder dashboard, retention metrics, cost tracking

### Gap 10: Multi-Child Family Features
- **Status**: Not implemented
- **Apps**: `apps/family/` (new)
- **Models**: `Family`, `FamilyLeaderboard`, `SiblingChallenge`
- **Features**: Family discounts, sibling competitions, combined stats

### Subscription Tiers (Strategy v3.0)

| Tier | NZ Price | Features |
|------|----------|----------|
| **Free** | $0 | Pre-cached content, limited AI |
| **Standard** | $14.99/mo | All content, Svara TTS, unlimited Peppi |
| **Premium** | $24.99/mo | Sarvam AI voices, priority support |
| **Elite** | $49.99/mo | Live classes, premium teachers |

---

## Development Notes

- When working on backend, always check if venv is activated
- Backend uses Django 5.x
- Frontend uses Next.js 14 App Router (not Pages Router)
- The project targets children, so UI should be colorful and engaging
- StoryWeaver API currently blocked (403) - using manual sample stories
- Hindi is the primary MVP language, others come later
- TTS uses remote HuggingFace Spaces (no local torch required)
- The NVIDIA CUDA packages in venv are from transformers dependency but not needed for current TTS implementation
- Check `/docs/` for detailed implementation guides before major changes
- Use `python manage.py check` to verify Django configuration after changes
- **HuggingFace Pro membership** is configured - use `huggingface_hub.login()` with token from .env
- **IndicF5 requires reference audio** - use samples from `/voice_samples/hindi/`
- **After completing any task, update the project documentation** to avoid repeating work

---

## Implementation Roadmap (Dec 2024)

### Critical Analysis Summary (Dec 18, 2024)

**Overall Project Status:**
- Backend: 65% structurally complete, 65% functionally complete
- Frontend: 60% structurally complete, 30% functionally complete
- Production Ready: NO

**Critical Blockers Identified:**
1. Games don't work (models exist, no gameplay logic)
2. Audio not integrated (TTS APIs ready, useAudio hook unused)
3. 8 apps are skeletons (models but no views/serializers)
4. Zero interactive exercises (0/8 types implemented)
5. Content validation missing (no VerifiedLetter/Word models)
6. Parent Dashboard missing (store drafted, no UI)
7. Age variants missing (one UI for ages 4-14)
8. Peppi not teaching (avatar on home page only)

### Week 1 Implementation (CRITICAL - MVP Blockers) - ✅ COMPLETED

**Total: 21 hours**

| Day | Task | Status | Owner |
|-----|------|--------|-------|
| Day 1 | Audio Pre-generation System | ✅ Complete | Backend |
| Day 2 | Audio Integration in Frontend | ✅ Complete | Frontend |
| Day 3 | ListenAndTap Exercise Component | ✅ Complete | Frontend |
| Day 4 | Peppi Integration in Lessons | ✅ Complete | Frontend |
| Day 5 | Marketing Fixes + Testing | ✅ Complete | Both |

**Week 1 Success Criteria:**
- [x] All 50 Hindi letters have audio files
- [x] 100 core vocabulary words have audio files
- [x] Letters play audio when tapped
- [x] Words play audio when tapped
- [x] ListenAndTap exercise is functional
- [x] Peppi appears in lesson intro/outro
- [x] Marketing claims updated (no false promises)

### Week 2-4 Implementation (MVP Completion) - ✅ COMPLETED

**Total: 67 hours**

| Day | Task | Status | Owner |
|-----|------|--------|-------|
| Day 1-2 | Letter Match Game (Memory Game) | ✅ Complete | Frontend |
| Day 2-3 | Parent Dashboard MVP - Backend | ✅ Complete | Backend |
| Day 3-4 | Parent Dashboard MVP - Frontend | 🔄 Partial | Frontend |
| Day 4 | Match Pairs Exercise | ✅ Complete | Frontend |
| Day 4-5 | Content Validation System | ✅ Complete | Backend |
| Day 5 | Age-Adaptive UI Polish | ✅ Complete | Frontend |

**Week 2-4 Success Criteria:**
- [x] Letter Match game fully playable
- [x] Parent can see child's progress summary (backend ready)
- [x] Parent can see recent activity (backend ready)
- [x] Match Pairs exercise functional
- [x] VerifiedWord model exists and enforced
- [x] Hindi letters verified in database (41 letters)
- [x] Age-specific UI differences visible (3 variants)
- [x] Visual vocabulary with images (110 words)
- [x] Sound effects system integrated (12 sounds)
- [x] Animation components created (4 types)
- [x] Picture Word game implemented
- [x] Alphabet quiz system created

### Files Created/Modified (Week 2-4 Sprint)

**Backend - Games & Content:**
- `apps/curriculum/models/verified_content.py` - VerifiedLetter and VerifiedWord models
- `apps/curriculum/migrations/0009_verifiedletter_verifiedword.py` - Verified content migration
- `apps/curriculum/management/commands/seed_verified_hindi.py` - Seed 41 Hindi letters
- `apps/curriculum/management/commands/seed_vocabulary_images.py` - Add images to vocabulary
- `apps/curriculum/models/vocabulary.py` - Added image_url field
- `apps/parent_engagement/views.py` - Parent dashboard API endpoints
- `apps/parent_engagement/serializers.py` - Parent dashboard serializers

**Backend - TTS & Speech:**
- `apps/speech/services/google_provider.py` - Google Cloud TTS provider (base64 credentials)
- `apps/speech/services/sarvam_provider.py` - Sarvam AI provider (pace: 0.7)
- `apps/speech/services/peppi_tts.py` - Peppi voice configurations
- `apps/speech/peppi_views.py` - Return base64 audio instead of URLs
- `apps/speech/models.py` - Added streak tracking fields
- `apps/speech/migrations/0005_add_streak_tracking.py` - Streak tracking migration
- `requirements/render.txt` - Added google-cloud-texttospeech>=2.33.0

**Backend - Auth & Users:**
- `apps/users/models.py` - Email verification, tts_provider property fix
- `apps/users/migrations/0005_add_email_verification.py` - Email verification fields
- `apps/users/email_service.py` - Email verification service
- `apps/users/views.py` - Email verification endpoints
- `apps/users/serializers.py` - Updated user serializers

**Backend - Songs & Curriculum:**
- `apps/curriculum/models/songs.py` - Added language field
- `apps/curriculum/migrations/0008_add_language_to_song.py` - Song language migration
- `apps/curriculum/views/songs.py` - Filter songs by child's language
- `apps/curriculum/management/commands/seed_l1_content.py` - Updated with language
- `apps/curriculum/management/commands/seed_l1_songs_stories.py` - Updated with language
- `apps/curriculum/management/commands/seed_fiji_hindi.py` - Updated with language
- `apps/curriculum/management/commands/seed_punjabi_l1_l2.py` - Updated with language
- `apps/curriculum/management/commands/seed_tamil_l1_l2.py` - Updated with language

**Frontend - Games:**
- `src/components/games/LetterMatchGame.tsx` - Memory card game (NEW)
- `src/components/games/MatchPairsGame.tsx` - Two-column matching (NEW)
- `src/components/games/PictureWordGame.tsx` - Image-based vocabulary game (NEW)
- `src/app/games/[id]/page.tsx` - Updated to integrate new games

**Frontend - Visual & Flashcards:**
- `src/components/curriculum/VisualFlashcard.tsx` - 3D flip flashcard component (NEW)
- `src/components/curriculum/AlphabetQuiz.tsx` - Alphabet quiz component (NEW)
- `src/app/learn/alphabet/page.tsx` - Integrated quiz and audio
- `src/app/learn/vocabulary/[id]/page.tsx` - Integrated visual flashcards

**Frontend - Age-Adaptive UI:**
- `src/hooks/useAgeConfig.ts` - Enhanced age-based configuration (20+ properties)
- `src/components/layout/AgeThemeProvider.tsx` - Age theme provider (NEW)

**Frontend - Sound & Animations:**
- `src/lib/soundService.ts` - Sound effects service with 12 sounds (NEW)
- `src/hooks/useSounds.ts` - React hook for sound effects (NEW)
- `public/audio/sounds/*.mp3` - 12 sound effect files (NEW)
- `src/components/animations/Celebration.tsx` - Confetti animation (NEW)
- `src/components/animations/LevelUp.tsx` - Level up animation (NEW)
- `src/components/animations/StarBurst.tsx` - Streak animation (NEW)
- `src/components/animations/SuccessCheck.tsx` - Checkmark animation (NEW)

**Frontend - Peppi Enhancements:**
- `src/components/peppi/PeppiFeedbackBubble.tsx` - Contextual feedback (NEW)
- `src/components/peppi/PeppiNarrator.tsx` - Updated for base64 audio
- `src/components/peppi/PeppiSongNarrator.tsx` - Updated for base64 audio
- `src/components/peppi/PeppiAvatar.tsx` - Fixed SVG animation errors
- `src/hooks/usePeppiFeedback.ts` - Feedback logic hook (NEW)
- `src/components/peppi/index.ts` - Updated exports

**Frontend - Auth & User Management:**
- `src/app/verify-email/page.tsx` - Email verification page (NEW)
- `src/app/forgot-password/page.tsx` - Password reset request page (NEW)
- `src/app/reset-password/page.tsx` - Password reset page (NEW)
- `src/stores/authStore.ts` - Fixed rehydration errors, simplified persistence
- `src/app/login/page.tsx` - Added forgot password link

**Frontend - Parent Dashboard:**
- `src/app/parent/dashboard/page.tsx` - Parent dashboard UI (NEW, partial)
- `src/lib/api.ts` - Added parent dashboard API methods

**Frontend - Bug Fixes:**
- `src/hooks/useAudio.ts` - Fixed circular dependency
- `src/app/learn/grammar/[id]/page.tsx` - Wrapped handlePlayExample in useCallback
- `src/app/learn/songs/page.tsx` - Filter songs by child's language
- `src/hooks/index.ts` - Export useSounds and usePeppiFeedback

**Infrastructure:**
- `bhashamitra-backend/build.sh` - Added google-cloud-texttospeech verification
- `bhashamitra-frontend/vercel.json` - Vercel configuration (NEW)
- `bhashamitra-frontend/.env.production` - Production environment variables (NEW)

---

## Curriculum Hierarchy Architecture (Dec 2024)

### L1-L10 Curriculum Levels - IMPLEMENTED

The curriculum follows an NCERT-aligned structure adapted for diaspora learners (ages 4-14).

**Hierarchy:** `Level → Module → Lesson → LessonContent`

### Curriculum Levels (L1-L10)

| Level | Hindi Name | English Name | Age Range | Emoji | Theme Color |
|-------|------------|--------------|-----------|-------|-------------|
| L1 | अंकुर (Ankur) | Sprout | 4-5 | 🌱 | #86efac |
| L2 | पौधा (Paudha) | Seedling | 5-6 | 🌿 | #4ade80 |
| L3 | वृक्ष (Vriksh) | Tree | 6-7 | 🌳 | #22c55e |
| L4 | पुष्प (Pushp) | Flower | 7-8 | 🌻 | #fbbf24 |
| L5 | तारा (Tara) | Star | 8-9 | ⭐ | #facc15 |
| L6 | ज्योति (Jyoti) | Light | 9-10 | 🔥 | #fb923c |
| L7 | शिखर (Shikhar) | Peak | 10-11 | 🏔️ | #60a5fa |
| L8 | उड़ान (Udaan) | Flight | 11-12 | 🚀 | #3b82f6 |
| L9 | रत्न (Ratna) | Gem | 12-13 | 💎 | #8b5cf6 |
| L10 | मुकुट (Mukut) | Crown | 13-14 | 👑 | #a855f7 |

### Module Types

Each level contains modules of these types:
- `LISTENING` - Listening & Recognition (👂)
- `SPEAKING` - Speaking & Pronunciation (🗣️)
- `VOCABULARY` - Vocabulary Building (📚)
- `ALPHABET` - Alphabet & Letters (🔤)
- `READING` - Reading Practice (📖)
- `GRAMMAR` - Grammar Concepts (📝)
- `STORIES` - Story Time (📕)
- `SONGS` - Songs & Rhymes (🎵)
- `GAMES` - Games & Activities (🎮)
- `CULTURE` - Cultural Learning (🏛️)

### Backend Models

**Location:** `apps/curriculum/models/`

| Model | File | Description |
|-------|------|-------------|
| `CurriculumLevel` | `level.py` | L1-L10 levels with learning objectives |
| `CurriculumModule` | `level.py` | Modules within levels |
| `Lesson` | `level.py` | Individual lessons |
| `LessonContent` | `level.py` | Links lessons to content (vocabulary, grammar, etc.) |
| `LevelProgress` | `progress.py` | Child's level progress tracking |
| `ModuleProgress` | `progress.py` | Child's module progress tracking |
| `LessonProgress` | `progress.py` | Child's lesson progress tracking |

**Key Fields:**
- All models use UUID primary keys
- `TimeStampedModel` base class for created_at/updated_at
- Progress models have `update_progress(score)` method that cascades completion

### Backend API Endpoints

**Base URL:** `/api/v1/curriculum/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/levels/` | GET | List all curriculum levels |
| `/levels/<id>/` | GET | Get level details |
| `/levels/<id>/modules/` | GET | Get modules in a level |
| `/modules/<id>/` | GET | Get module details |
| `/modules/<id>/lessons/` | GET | Get lessons in a module |
| `/lessons/<id>/` | GET | Get lesson details |
| `/lessons/<id>/progress/` | POST | Update lesson progress |
| `/progress/levels/` | GET | Get child's curriculum progress |

**Query Parameters:**
- `?child_id=<uuid>` - Include child's progress in responses

### Frontend Types

**Location:** `src/types/curriculum.ts`

```typescript
// Core types
interface CurriculumLevel {
  id: string;
  code: string; // L1, L2, etc.
  name_english: string;
  name_hindi: string;
  name_romanized: string;
  min_age: number;
  max_age: number;
  emoji: string;
  theme_color: string;
  learning_objectives: string[];
  peppi_welcome: string;
  peppi_completion: string;
  progress?: LevelProgress;
}

interface CurriculumModule {
  id: string;
  level: string;
  code: string; // L1.M1, etc.
  module_type: ModuleType;
  name_english: string;
  name_hindi: string;
  emoji: string;
  peppi_intro: string;
  progress?: ModuleProgress;
}

interface Lesson {
  id: string;
  module: string;
  code: string; // L1.M1.LS1, etc.
  title_english: string;
  title_hindi: string;
  points_available: number;
  mastery_threshold: number;
  peppi_intro: string;
  peppi_success: string;
  progress?: LessonProgress;
}
```

### Frontend Components

**Location:** `src/components/curriculum/`

| Component | Description |
|-----------|-------------|
| `ProgressRing.tsx` | Circular progress indicator |
| `LevelCard.tsx` | Curriculum level card with progress |
| `ModuleCard.tsx` | Module card with type info |
| `LessonCard.tsx` | Lesson card with stars |
| `index.ts` | Exports all components |

### Frontend Pages

| Route | Description |
|-------|-------------|
| `/learn/levels` | List all L1-L10 curriculum levels |
| `/learn/levels/[id]` | Level detail with modules |
| `/learn/modules/[id]` | Module detail with lessons |
| `/learn/lessons/[id]` | Lesson detail page |

### API Methods

**Location:** `src/lib/api.ts`

```typescript
// Curriculum API methods
api.getCurriculumLevels(childId?)
api.getCurriculumLevel(levelId, childId?)
api.getLevelModules(levelId, childId?)
api.getCurriculumModule(moduleId, childId?)
api.getModuleLessons(moduleId, childId?)
api.getLesson(lessonId, childId?)
api.updateLessonProgress(lessonId, childId, score)
api.getChildCurriculumProgress(childId)
```

### Database Migrations

```bash
# Migrations created
children.0004_alter_child_level  # Extended level from 1-5 to 1-10
curriculum.0002_curriculumlevel_curriculummodule_lesson_and_more  # All curriculum models
```

### Seed Command

```bash
# Seed all 10 curriculum levels
python manage.py seed_curriculum_levels --settings=config.settings.dev
```

### Child Model Update

**Changed:** `apps/children/models.py`
- `level` field: `MaxValueValidator(5)` → `MaxValueValidator(10)`

### URL Configuration

**Changed:** `config/urls.py`
```python
# Added global curriculum endpoint
path('api/v1/curriculum/', include('apps.curriculum.urls', namespace='curriculum-global')),
```

### Next Steps for Content

The architecture is ready. To add content:
1. Create modules for each level using admin or management command
2. Create lessons within modules
3. Link lessons to existing content (vocabulary, grammar, games) via LessonContent
4. Peppi welcome/completion messages are included for each level/module/lesson

---

## Phase 1 Completion Status (Dec 26, 2024)

### ✅ Phase 1: Google Cloud TTS + Fun Features - COMPLETE

**Backend Implementation: 100% Complete**

| Component | File | Status |
|-----------|------|--------|
| Google TTS Provider | `apps/speech/services/google_provider.py` | ✅ 610 lines, WaveNet + Standard |
| TTS Service | `apps/speech/services/tts_service.py` | ✅ Tier-based routing, fallback chain |
| Peppi TTS | `apps/speech/services/peppi_tts.py` | ✅ Language voices, pace 0.7, genders |
| TTS API Views | `apps/speech/views.py` | ✅ All endpoints working |
| Peppi Narration | `apps/speech/peppi_views.py` | ✅ Story/song/text narration |
| Dependencies | `requirements/render.txt` | ✅ google-cloud-texttospeech>=2.33.0 |

**Frontend Implementation: 100% Complete**

| Component | File | Status |
|-----------|------|--------|
| Sound Service | `src/lib/soundService.ts` | ✅ 12 sound effects, volume control |
| useSounds Hook | `src/hooks/useSounds.ts` | ✅ React integration |
| Sound Files | `public/audio/sounds/` | ✅ 12 MP3s (4.4 MB) |
| Celebration | `src/components/animations/Celebration.tsx` | ✅ Confetti + sound |
| LevelUp | `src/components/animations/LevelUp.tsx` | ✅ Animation + sound |
| StarBurst | `src/components/animations/StarBurst.tsx` | ✅ Streak animation |
| SuccessCheck | `src/components/animations/SuccessCheck.tsx` | ✅ Checkmark animation |
| Peppi Narrator | `src/components/peppi/PeppiNarrator.tsx` | ✅ Story narration |
| Peppi Scripts | `src/data/peppi-scripts.ts` | ✅ Age-specific dialogues |

---

## Phase 2: Critical Strategy Analysis (Dec 26, 2024)

### Executive Summary

**Current State**: BhashaMitra has a polished UI shell with robust backend TTS infrastructure, but the **learning experience is fundamentally broken**. A child can complete lessons without learning anything, games can be cheated, and Peppi is decorative rather than instructional.

**Core Problem**: The app is **60% UI shell, 40% functional learning system**.

### Critical Problems Identified

#### 🔴 Severity: CRITICAL (Blocks MVP)

| Problem | Impact | Evidence |
|---------|--------|----------|
| **Fake lesson completion** | Children get 100% without learning | `handleCompleteLesson()` auto-scores 100% |
| **No pronunciation validation** | Listen & Speak game is cheatable | No speech recognition, child self-reports |
| **Sound service unused** | Zero audio feedback for actions | `soundService` not imported anywhere |
| **Progress is static** | Alphabet shows 0/41 forever | Progress bar hardcoded, never updates |

#### 🟠 Severity: HIGH (Degrades Experience)

| Problem | Impact | Evidence |
|---------|--------|----------|
| **Peppi is decorative** | No guidance, no teaching | Only greets/congratulates |
| **No visual vocabulary** | Words without pictures | Critical for ages 4-8 |
| **4/6 games missing** | Limited engagement | Only Word Match & Listen/Speak work |
| **No adaptive learning** | Same content for ages 4-14 | No age-specific difficulty |

### User Journey Gap Analysis

```
CURRENT EXPERIENCE (What Child Sees):
├── HOME: Peppi says "Hi!" but doesn't guide
├── ALPHABET: Tap letters, hear sound, progress stays 0/41
├── VOCABULARY: Flip cards, no pictures, passive learning
├── GAMES: 2 work (1 cheatable), 4 say "Coming Soon"
└── LESSONS: Click "Complete" → 100% (no actual quiz)

IDEAL EXPERIENCE (What Child Should See):
├── HOME: Peppi says "Learn 5 letters today!" with clear mission
├── ALPHABET: Tap → immediate audio → progress updates → celebration
├── VOCABULARY: See PICTURE + word + audio → practice → feedback
├── GAMES: Picture Word, Listen & Tap, real scoring
└── LESSONS: Peppi teaches → quiz required → real score
```

### Phase 2 Implementation Strategy

#### Phase 2A: Fix the Foundation (Week 1)
**Goal**: Make existing features honest and engaging

| Day | Task | Priority | Owner |
|-----|------|----------|-------|
| Day 1 | Wire soundService to all interactions | P0 | Frontend |
| Day 1 | - Alphabet page: sound on letter tap | | |
| Day 1 | - Vocabulary page: sound on card flip | | |
| Day 1 | - Games: correct/wrong sounds | | |
| Day 2 | Fix lesson completion (real scoring) | P0 | Frontend |
| Day 2 | - Remove auto-100% scoring | | |
| Day 2 | - Add simple quiz requirement | | |
| Day 3 | Make alphabet progress real | P0 | Frontend |
| Day 3 | - Track viewed/mastered letters | | |
| Day 3 | - Persist progress to backend | | |
| Day 3 | Add Celebration component triggers | P0 | Frontend |
| Day 4 | Peppi feedback integration | P1 | Frontend |
| Day 4 | - Random encouragement on correct | | |
| Day 4 | - Helpful hints on wrong | | |
| Day 5 | Testing + bug fixes | P0 | Both |

**Week 1 Success Criteria:**
- [ ] Sound effects play on all interactions
- [ ] Lesson completion requires passing quiz (60%+)
- [ ] Alphabet progress updates and persists
- [ ] Celebration animation triggers on milestones
- [ ] Peppi provides contextual feedback

**Files to Modify (Week 1):**
```
Frontend:
├── src/app/learn/alphabet/page.tsx      # Add soundService, real progress
├── src/app/learn/vocabulary/[id]/page.tsx  # Add soundService
├── src/app/learn/lessons/[id]/page.tsx  # Fix completion, add quiz
├── src/app/games/[id]/page.tsx          # Add soundService
├── src/components/peppi/PeppiMascot.tsx # Add feedback triggers
└── src/hooks/index.ts                   # Ensure useSounds exported
```

#### Phase 2B: Core Learning Exercises (Week 2-3)
**Goal**: Add the missing interactive learning

| Day | Task | Priority | Owner |
|-----|------|----------|-------|
| Day 1-2 | ListenAndTap exercise component | P0 | Frontend |
| Day 1-2 | - Audio plays automatically | | |
| Day 1-2 | - 4 image options to tap | | |
| Day 1-2 | - Immediate sound feedback | | |
| Day 3-4 | Picture Word game | P0 | Frontend |
| Day 3-4 | - Show image + 4 word options | | |
| Day 3-4 | - Audio pronunciation on select | | |
| Day 3-4 | - Progressive difficulty | | |
| Day 5 | Alphabet section quizzes | P1 | Frontend |
| Day 5 | - Quiz after vowels (10 letters) | | |
| Day 5 | - Must pass to complete section | | |
| Day 6-7 | Lesson quiz validation | P1 | Both |

**Week 2-3 Success Criteria:**
- [ ] ListenAndTap exercise fully functional
- [ ] Picture Word game playable with images
- [ ] Alphabet has section quizzes
- [ ] Lessons require quiz to complete
- [ ] 4/6 games now playable (up from 2/6)

**Files to Create (Week 2-3):**
```
Frontend:
├── src/components/exercises/ListenAndTap.tsx    # NEW
├── src/components/exercises/ExerciseWrapper.tsx # NEW
├── src/components/games/PictureWordGame.tsx     # NEW
├── src/components/curriculum/AlphabetQuiz.tsx   # NEW
└── src/components/curriculum/LessonQuiz.tsx     # NEW
```

#### Phase 2C: Visual Content (Week 4)
**Goal**: Support younger learners with images

| Day | Task | Priority | Owner |
|-----|------|----------|-------|
| Day 1-2 | Curate 200 vocabulary images | P0 | Content |
| Day 1-2 | - Use free sources (Unsplash, Pexels) | | |
| Day 1-2 | - Organize by theme | | |
| Day 3 | Integrate images in vocabulary | P0 | Frontend |
| Day 4 | Visual flashcard mode | P1 | Frontend |
| Day 5 | Testing + polish | P0 | Both |

**Week 4 Success Criteria:**
- [ ] 100+ vocabulary words have images
- [ ] Visual flashcard mode available
- [ ] Picture Word game has all needed images
- [ ] Images optimized for web (WebP, lazy loading)

**Free Image Sources:**
- Unsplash (https://unsplash.com) - High quality, free
- Pexels (https://pexels.com) - Free, commercial use
- OpenMoji (https://openmoji.org) - Free emoji-style icons
- Flaticon (https://flaticon.com) - Free with attribution

### Phase 2 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Lesson completion accuracy | 100% (fake) | 70% average (real) |
| Sound effects triggered | 0 | 100% of interactions |
| Games playable | 2/6 (33%) | 4/6 (67%) |
| Vocabulary with images | 0% | 50%+ |
| Real progress tracking | 0 pages | All curriculum pages |
| Interactive exercises | 0 | 2+ (ListenAndTap, PictureWord) |

### Deferred to Phase 3

| Feature | Reason for Deferral |
|---------|---------------------|
| Speech Recognition | Web Speech API inconsistent for Indian languages |
| Parent Dashboard | Fix children's experience first |
| Peppi AI Chat | Requires LLM integration (cost, complexity) |
| Adaptive Difficulty | Need usage data first |
| Spelling Bee Game | Requires keyboard component |
| Story Builder Game | Complex, lower priority |
| Offline Mode (PWA) | Post-MVP feature |
| Live Classes | Elite tier, post-launch |

### Technical Decisions for Phase 2

**Sound Integration Pattern:**
```typescript
// In any component that needs sounds:
import { useSounds } from '@/hooks/useSounds';

function MyComponent() {
  const { onCorrect, onWrong, onClick } = useSounds();

  const handleAnswer = (isCorrect: boolean) => {
    if (isCorrect) {
      onCorrect();
      // Show celebration...
    } else {
      onWrong();
      // Show hint...
    }
  };
}
```

**Progress Tracking Pattern:**
```typescript
// Track letter/word as "viewed" or "mastered"
const trackProgress = async (itemId: string, type: 'viewed' | 'mastered') => {
  await api.post(`/curriculum/progress/`, {
    child_id: activeChild.id,
    item_id: itemId,
    item_type: 'letter', // or 'word'
    status: type,
  });
};
```

**Quiz Validation Pattern:**
```typescript
// Lesson must have quiz, score determines completion
const handleLessonComplete = async (quizScore: number) => {
  const passed = quizScore >= 60; // 60% threshold

  if (passed) {
    await api.updateLessonProgress(lessonId, childId, quizScore);
    onCelebration(); // Trigger celebration
  } else {
    // Show "Try again" with hints
  }
};
```

### Daily Standup Questions (Use During Implementation)

1. What did I complete yesterday?
2. What am I working on today?
3. Are there any blockers?
4. Did I update PROJECT_CONTEXT.md?

### Definition of Done (Phase 2)

- [ ] All Week 1 success criteria met
- [ ] All Week 2-3 success criteria met
- [ ] All Week 4 success criteria met
- [ ] No fake 100% scores possible
- [ ] Sound effects on all interactions
- [ ] At least 2 interactive exercises working
- [ ] At least 4 games playable
- [ ] 100+ vocabulary images added
- [ ] All changes tested on mobile
- [ ] PROJECT_CONTEXT.md updated with any new learnings

---

## 🚨 TODO: UX Gap Fixes (Dec 27, 2024)

> **DELETE THIS SECTION** once all items are completed.

### Critical UX Gaps Identified

Based on comprehensive analysis of auth, onboarding, and help systems:

---

### P0 - CRITICAL (Fix First)

#### 1. Email Verification NOT Enforced
**Problem:** Users can register and access everything without verifying email.

**Files to Modify:**
- `bhashamitra-backend/apps/users/serializers.py` - Add `email_verified` to UserSerializer output
- `bhashamitra-backend/apps/users/views.py` - Add middleware to check `email_verified` before protected routes
- `bhashamitra-frontend/src/stores/authStore.ts` - Check `email_verified` status after login
- `bhashamitra-frontend/src/app/verify-email/page.tsx` - Add "Resend Verification" button

**Tasks:**
- [ ] Add `email_verified` field to UserSerializer
- [ ] Create middleware to block unverified users from protected routes
- [ ] Add frontend check to redirect unverified users
- [ ] Add "Resend Verification Email" UI button
- [ ] Block subscription purchase without verified email

#### 2. Onboarding Flow MISSING
**Problem:** First-time users land on complex homepage with no guidance. Broken link at `parent/dashboard/page.tsx:327`.

**Files to Create:**
- `bhashamitra-frontend/src/app/onboarding/page.tsx` (NEW) - Welcome screen
- `bhashamitra-frontend/src/app/onboarding/child/page.tsx` (NEW) - Add first child (fix broken link)
- `bhashamitra-frontend/src/app/onboarding/language/page.tsx` (NEW) - Select language
- `bhashamitra-frontend/src/app/onboarding/tour/page.tsx` (NEW) - Feature tour
- `bhashamitra-frontend/src/hooks/useOnboarding.ts` (NEW) - Onboarding state management

**Backend Changes:**
- `bhashamitra-backend/apps/users/models.py` - Add `is_onboarded` and `onboarding_completed_at` fields
- `bhashamitra-backend/apps/users/migrations/` - Create migration for new fields

**Tasks:**
- [ ] Create `/onboarding` welcome page
- [ ] Create `/onboarding/child` page (fix broken link from parent dashboard)
- [ ] Create `/onboarding/language` page
- [ ] Create `/onboarding/tour` page (5-screen feature tour)
- [ ] Add `is_onboarded` field to User model
- [ ] Redirect new users to onboarding flow after registration
- [ ] Store onboarding state in localStorage as backup

#### 3. Social Login MISSING ⏸️ NEEDS STRATEGY DISCUSSION
**Problem:** Parents expect quick Google/Apple sign-in.

**Status:** Implementation strategy pending discussion with Trishank.

**Detailed roadmap:** See `ROADMAP_REMAINING_FEATURES.md` (Phase 3A-3C)

**Tasks:**
- [ ] **DISCUSS:** Google OAuth credentials setup (Google Cloud Console)
- [ ] **DISCUSS:** Apple Developer account ($99/year) for Apple Sign-In
- [ ] Add Google OAuth integration (django-allauth)
- [ ] Add Apple Sign-In (required for iOS App Store)
- [ ] Update frontend login/register pages with social buttons

---

### P1 - HIGH PRIORITY

#### 4. Help Page & Dead Button
**Problem:** "Help & Support" button in profile does nothing (`profile/page.tsx:181-200`).

**Files to Create/Modify:**
- `bhashamitra-frontend/src/app/help/page.tsx` (NEW) - FAQ and help content
- `bhashamitra-frontend/src/app/profile/page.tsx` - Fix Help & Support button onClick

**Tasks:**
- [ ] Create `/help` page with FAQ accordion
- [ ] Fix dead "Help & Support" button in profile (add onClick handler)
- [ ] Add contextual help icons to complex features (XP, Levels, Streak)
- [ ] Add "Contact Support" form or email link

#### 5. Terms of Service Checkbox
**Problem:** Registration has no ToS/Privacy acceptance.

**Files to Modify:**
- `bhashamitra-frontend/src/app/register/page.tsx` - Add checkbox and validation

**Tasks:**
- [ ] Add ToS checkbox to registration form
- [ ] Link to existing `/terms` and `/privacy` pages
- [ ] Block registration until ToS accepted

#### 6. Improve Error Messages
**Problem:** Generic "Registration failed" gives no specific reason.

**Files to Modify:**
- `bhashamitra-frontend/src/stores/authStore.ts` - Parse and display specific errors
- `bhashamitra-frontend/src/app/register/page.tsx` - Show password requirements inline

**Tasks:**
- [ ] Parse backend error responses for specific messages
- [ ] Show password requirements inline (uppercase, numbers, etc.)
- [ ] Add password strength indicator

---

### P2 - MEDIUM PRIORITY

#### 7. Feature Tour Library
**Tasks:**
- [ ] Install `react-joyride` or similar
- [ ] Create tour for Home page
- [ ] Create tour for Learn page
- [ ] Create tour for Mimic (recording) feature

#### 8. Tooltips for Complex Features
**Files to Create:**
- `bhashamitra-frontend/src/components/ui/Tooltip.tsx` (NEW)

**Tasks:**
- [ ] Create Tooltip component
- [ ] Add tooltips to XP bar (explain XP system)
- [ ] Add tooltips to Level indicator
- [ ] Add tooltips to Streak counter

#### 9. User Manual/Documentation
**Tasks:**
- [ ] Create in-app documentation for parents
- [ ] Explain curriculum structure (L1-L10)
- [ ] How-to guide for Mimic (recording) feature

---

### Post-MVP: Offline Mode (PWA) ⏸️ NEEDS STRATEGY DISCUSSION

**Problem:** App doesn't work without internet; parents in areas with poor connectivity can't use the app.

**Status:** Implementation strategy pending discussion with Trishank.

**Current State (Dec 27, 2024):**
- Infrastructure exists: `manifest.json`, `sw.js`, `offlineStore.ts`
- Service Worker NOT registered
- API endpoints NOT implemented (TODO stubs)
- Content caching is mock data

**Data Analysis Completed:**
| Language | Letters | Vocab | Stories | Current Size | With Audio |
|----------|---------|-------|---------|--------------|------------|
| Hindi | 49 | 110 | 42 | ~15 MB | ~59 MB |
| Tamil | 37 | 70 | 21 | ~3 MB | ~22 MB |
| Gujarati | 48 | 0 | 7 | ~4.4 MB | ~8 MB |
| Punjabi | 45 | 70 | 18 | ~4.2 MB | ~24 MB |
| Fiji Hindi | 46 | 107 | 15 | ~0 MB | ~21 MB |

**Key Decision Points:**
- [ ] **DISCUSS:** FREE tier only (~25 MB/lang) vs Full content (~51 MB/lang)?
- [ ] **DISCUSS:** Cache audio on-demand or pre-download?
- [ ] **DISCUSS:** Priority languages for offline?
- [ ] **DISCUSS:** Storage limit warning thresholds?

**Detailed roadmap:** See `ROADMAP_REMAINING_FEATURES.md` (Phase 4A-4D)

---

### Security Improvements (P1)

**Tasks:**
- [ ] Add 2FA support (TOTP)
- [ ] Implement account lockout after 5 failed login attempts
- [ ] Add login notification emails for new devices
- [ ] Add session management (view/revoke active sessions)

---

### Quick Reference - Key Files

| Issue | Primary File | Line Reference |
|-------|--------------|----------------|
| Dead Help button | `src/app/profile/page.tsx` | Lines 181-200 |
| Broken onboarding link | `src/app/parent/dashboard/page.tsx` | Line 327 |
| Generic register error | `src/stores/authStore.ts` | Line 44 |
| Missing ToS checkbox | `src/app/register/page.tsx` | Form section |
| Email verification | `apps/users/views.py` | RegisterView |

---

### Testing Checklist

After implementing fixes, verify:
- [ ] New user is redirected to onboarding after registration
- [ ] Unverified users cannot access protected routes
- [ ] Help button in profile navigates to /help page
- [ ] Registration shows specific error messages
- [ ] ToS checkbox blocks registration when unchecked
- [ ] All onboarding pages work on mobile
