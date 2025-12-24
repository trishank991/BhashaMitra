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

### IMPORTANT: No AI Tool References
**DO NOT include any references to AI assistants or tools in:**
- Git commit messages
- Code comments
- Documentation files
- Pull request descriptions

This includes (but not limited to):
- "Generated with Claude Code"
- "Co-Authored-By: Claude"
- "Created by AI"
- Any similar AI tool attribution

All commits and documentation should appear as if written by human developers only.

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
| Hindi | Devanagari | Phase 1 (MVP) | ✅ Implemented (L1-L2) |
| Punjabi | Gurmukhi | Phase 1 (MVP) | ✅ Implemented (L1-L2) |
| Tamil | Tamil | Phase 1 (MVP) | ✅ Implemented (L1-L2) |
| Gujarati | Gujarati | Phase 3 | Planned |
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
- [x] TTS integration (Svara TTS + Parler fallback)
- [x] Curriculum models (scripts, vocabulary, grammar, games, assessments)
- [x] Frontend base setup (Next.js 14, Tailwind, Zustand)
- [x] Frontend pages (login, register, home, stories, games, progress, profile)
- [x] UI components (Button, Card, Avatar, Badge, etc.)
- [x] Peppi assistant character (avatar component)

### In Progress / Not Yet Implemented
- [ ] Parent Dashboard (`/family` page)
- [ ] Peppi AI Chat (`/peppi` page with AI integration)
- [ ] SRS Flashcard review system (backend ready, frontend needs review UI)
- [ ] Games module gameplay (actual game logic)
- [ ] Assessment system (tests/quizzes)
- [ ] Audio playback for letters and words (TTS integration)

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

### TTS Strategy Decision (Updated Dec 2024)

**Current TTS Strategy:**

| Tier | Price | TTS Provider | Features |
|------|-------|--------------|----------|
| **Free** | $0 | Cache only | Pre-cached curriculum content only |
| **Standard** | $20/month | Cache only | Pre-cached curriculum content only |
| **Premium** | $30/month | Google Cloud TTS WaveNet | Real-time on-demand generation, highest quality |

**Provider Routing:**
- **Premium tier**: Google TTS WaveNet → Google Standard → Sarvam AI → Svara TTS (fallback chain)
- **Standard/Free tiers**: Cache only (pre-warmed curriculum audio)

**Fallback Chain (Premium only):**
1. Cache (instant, free) - checked first for all tiers
2. Google TTS WaveNet - highest quality voices
3. Google TTS Standard - fallback if WaveNet fails
4. Sarvam AI - fallback if Google fails
5. Svara TTS - emergency backup

**Provider Details:**

1. **Google Cloud TTS (Premium tier)**:
   - API: Google Cloud Text-to-Speech
   - WaveNet voices: High quality, natural sounding
   - Cost: ~$16 per million characters (WaveNet)
   - Languages: Hindi, Tamil, Telugu, Gujarati, Malayalam, Bengali, Kannada, Marathi, Punjabi, Fiji Hindi (uses Hindi voice)

2. **Cache (Standard/Free tiers)**:
   - Pre-cached using `python manage.py prewarm_curriculum_audio`
   - All curriculum content (alphabet, vocabulary, stories) pre-generated
   - Instant playback, no generation delay

**Supported Languages:**
- Hindi, Tamil, Telugu, Gujarati, Punjabi, Malayalam, Bengali, Kannada, Marathi
- **Fiji Hindi** (uses Hindi TTS voice - hi-IN)

**Environment Variables:**
```bash
# Google Cloud TTS (Premium tier)
GOOGLE_TTS_API_KEY=your_key_here

# Sarvam AI TTS (fallback)
SARVAM_API_KEY=your_key_here
```

**Provider Files:**
- `apps/speech/services/google_provider.py` - Google Cloud TTS (primary for Premium)
- `apps/speech/services/sarvam_provider.py` - Sarvam AI (fallback)
- `apps/speech/services/mms_provider.py` - Svara TTS (emergency backup)
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

| Content Type | Hindi | Punjabi | Tamil | Gujarati | Total |
|--------------|-------|---------|-------|----------|-------|
| **Stories** | 42 | 18 | 21 | 7 | 88 |
| **Alphabets** | 49 letters | 55 letters | 37 letters | 48 letters | 189 |
| **Matras** | 12 | 10 | 12 | 12 | 46 |
| **Vocabulary** | 110 words | 70 words | 70 words | - | 250 |
| **Grammar Topics** | 6 | 5 | 5 | - | 16 |
| **Grammar Rules** | 20 | 14 | 28 | - | 62 |
| **Grammar Exercises** | 21 | 19 | 31 | - | 71 |
| **Songs** | 5 | 5 | 5 | - | 15 |
| **Games** | 5 | 5 | 5 | - | 15 |
| **Assessments** | 2 | 2 | 2 | - | 6 |
| **Peppi Phrases** | 49 | 12 | 12 | - | 73 |
| **Festival Stories** | 3 | 2 | 2 | 2 | 9 |

### Seeded Content Details

**Hindi L1-L2:**
- `python manage.py seed_l1_l2_curriculum` - Modules, lessons, exercises
- `python manage.py seed_l1_content` - Vocabulary, stories, songs

**Punjabi L1-L2:**
- `python manage.py seed_punjabi_l1_l2` - Complete curriculum with Gurmukhi script

**Tamil L1-L2:**
- `python manage.py seed_tamil_l1_l2 --clear` - Complete curriculum with Tamil script

**Grammar Content (All Languages):**
- `python manage.py seed_grammar_content` - Seed grammar for all languages (Hindi, Tamil, Punjabi)
- `python manage.py seed_grammar_content --language TAMIL` - Seed specific language
- `python manage.py seed_grammar_content --clear` - Clear existing before seeding
- Content: Topics (Sentence Structure, Gender/Case, Pronouns, Numbers, Verb Conjugation) with rules and exercises

**Stories (All Languages):**
- `python manage.py seed_stories` - Seed stories for all languages (Hindi, Tamil, Punjabi, Gujarati)
- `python manage.py seed_stories --language HINDI` - Seed specific language
- `python manage.py seed_stories --clear` - Clear existing before seeding
- Content: Regular stories + festival stories (Diwali, Holi, Pongal, Navratri, Raksha Bandhan, Vaisakhi)

**Audio Caching (All Languages):**
- `python manage.py cache_all_audio` - Cache audio for all curriculum content
- `python manage.py cache_all_audio --language TAMIL` - Cache for specific language
- `python manage.py cache_all_audio --dry-run` - Preview what would be cached

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

### Peppi Voice Configuration (Updated Dec 2024)

**Voice Progression Strategy:**
- **L1-L5 Levels**: Same Peppi voice (Google TTS WaveNet, child-friendly female)
- **L6+ Levels**: New voice to be introduced (TBD) - marks progression to advanced levels

The same Peppi voice is used throughout the entire course from L1 to L5 for consistency and familiarity. A new voice will be introduced starting from L6 to mark the learner's progression to advanced levels.

**Tier-Based Voice & Content Access (NZD Pricing):**

| Feature | Free ($0) | Standard ($20/mo) | Premium ($30/mo) |
|---------|-----------|-------------------|------------------|
| **Curriculum Levels** | Basic alphabets only | L1-L10 (full CBSE/ICSE) | L1-L10 (full CBSE/ICSE) |
| **Stories** | 5 stories | Unlimited | Unlimited |
| **Games** | 2 per day | Unlimited | Unlimited |
| **Child Profiles** | 1 | 3 | 5 |
| **Peppi AI Chat** | ❌ | ✅ | ✅ |
| **Peppi Story Narration** | ❌ | ✅ Google WaveNet | ✅ Google WaveNet |
| **Progress Reports** | ❌ | ✅ | ✅ |
| **Live Classes** | ❌ | ❌ | 2 FREE/month |
| **Premium Voices** | Pre-cached only | Pre-cached | Real-time Google TTS |
| **Offline Downloads** | ❌ | ❌ | ✅ |
| **Priority Support** | ❌ | ❌ | ✅ |

**Key Points:**
- **Peppi voice is consistent for paid tiers** - Always uses Google TTS WaveNet for narration
- **Free tier is browse mode** - Limited access to test the platform
- **Standard unlocks full curriculum** - Complete L1-L10 journey with Peppi chat and narration
- **Premium adds live classes and extras** - Real-time TTS, offline downloads, priority support

**Google TTS WaveNet Configuration (Peppi Voice):**
```python
# apps/speech/services/google_provider.py
VOICE_MAPPING = {
    'HINDI': {
        'language_code': 'hi-IN',
        'voice_name': 'hi-IN-Standard-A',      # Female, child-friendly (Peppi)
        'wavenet_voice': 'hi-IN-Wavenet-A',    # High quality female (Peppi)
    },
    'TAMIL': {
        'language_code': 'ta-IN',
        'voice_name': 'ta-IN-Standard-D',
        'wavenet_voice': 'ta-IN-Wavenet-D',
    },
    'PUNJABI': {
        'language_code': 'pa-IN',
        'voice_name': 'pa-IN-Standard-B',
        'wavenet_voice': 'pa-IN-Wavenet-D',
    },
    # ... other languages follow similar pattern
}
```

**Peppi Narration Endpoints:**
- `GET /api/v1/peppi/narrate/story/{story_id}/` - Full story narration
- `GET /api/v1/peppi/narrate/story/{story_id}/page/{page_number}/` - Single page narration
- `POST /api/v1/peppi/narrate/` - Arbitrary text narration

**Implementation Note:** Peppi narration always uses Google TTS WaveNet regardless of user subscription tier. This ensures consistent, high-quality voice for the mascot character.

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
- **After completing any task, update this CLAUDE.md file** to avoid repeating work

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

### Week 1 Implementation (CRITICAL - MVP Blockers)

**Total: 21 hours**

| Day | Task | Status | Owner |
|-----|------|--------|-------|
| Day 1 | Audio Pre-generation System | 🔄 In Progress | Backend |
| Day 2 | Audio Integration in Frontend | ⏳ Pending | Frontend |
| Day 3 | ListenAndTap Exercise Component | ⏳ Pending | Frontend |
| Day 4 | Peppi Integration in Lessons | ⏳ Pending | Frontend |
| Day 5 | Marketing Fixes + Testing | ⏳ Pending | Both |

**Week 1 Success Criteria:**
- [ ] All 50 Hindi letters have audio files
- [ ] 100 core vocabulary words have audio files
- [ ] Letters play audio when tapped
- [ ] Words play audio when tapped
- [ ] ListenAndTap exercise is functional
- [ ] Peppi appears in lesson intro/outro
- [ ] Marketing claims updated (no false promises)

### Week 2 Implementation (MVP Completion)

**Total: 67 hours**

| Day | Task | Status | Owner |
|-----|------|--------|-------|
| Day 1-2 | Letter Match Game (Memory Game) | ⏳ Pending | Frontend |
| Day 2-3 | Parent Dashboard MVP - Backend | ⏳ Pending | Backend |
| Day 3-4 | Parent Dashboard MVP - Frontend | ⏳ Pending | Frontend |
| Day 4 | Match Pairs Exercise | ⏳ Pending | Frontend |
| Day 4-5 | Content Validation System | ⏳ Pending | Backend |
| Day 5 | Age-Adaptive UI Polish | ⏳ Pending | Frontend |

**Week 2 Success Criteria:**
- [ ] Letter Match game fully playable
- [ ] Parent can see child's progress summary
- [ ] Parent can see recent activity
- [ ] Match Pairs exercise functional
- [ ] VerifiedWord model exists and enforced
- [ ] Hindi letters verified in database
- [ ] Age-specific UI differences visible

### Files Created/Modified This Sprint

**Backend (Week 1):**
- `apps/speech/management/commands/generate_audio_cache.py` - Audio generation command
- `apps/speech/services/tts_service.py` - TTS service with caching
- `apps/speech/views.py` - Audio URL API endpoints
- `apps/speech/urls.py` - URL routes for audio

**Frontend (Week 1):**
- `src/hooks/useAudio.ts` - Audio playback hook (updated)
- `src/hooks/useAgeConfig.ts` - Age-appropriate configuration hook (new)
- `src/components/ui/AudioButton.tsx` - Audio button component
- `src/components/curriculum/LetterCard.tsx` - Letter card with audio
- `src/components/curriculum/WordCard.tsx` - Word card with audio
- `src/components/exercises/ListenAndTap.tsx` - ListenAndTap exercise
- `src/components/exercises/ExerciseWrapper.tsx` - Exercise wrapper
- `src/components/peppi/PeppiAvatar.tsx` - Peppi avatar component
- `src/components/peppi/PeppiSpeech.tsx` - Peppi speech bubble
- `src/data/peppi-scripts.ts` - Peppi's pre-written scripts

**Backend (Week 2):**
- `apps/games/models.py` - Game models
- `apps/games/views.py` - Game API views
- `apps/parent_engagement/views.py` - Parent dashboard APIs
- `apps/curriculum/models/verified_content.py` - Verified content models
- `apps/curriculum/management/commands/seed_verified_hindi.py` - Hindi seed data

**Frontend (Week 2):**
- `src/components/games/LetterMatchGame.tsx` - Memory game
- `src/app/(main)/parent/dashboard/page.tsx` - Parent dashboard
- `src/components/exercises/MatchPairs.tsx` - Match pairs exercise
- `src/components/layout/AgeThemeProvider.tsx` - Age theme provider

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

---

## L1-L2 Hindi Curriculum Implementation (Dec 2024)

### Overview

Comprehensive L1-L2 Hindi curriculum has been implemented with full lesson content, vocabulary, and stories. The curriculum uses a proficiency-based approach (Discovery → Building Blocks) rather than age-based naming for clearer learning progression.

### Curriculum Structure

**L1 - Discovery (Beginners):**
- **Age Range:** 4-7 years
- **Focus:** Introduction to Hindi, basic sounds, simple words
- **Modules:** 4 modules, 16 lessons
- **Free Tier:** Yes (fully free)

| Module | Name | Lessons | Focus |
|--------|------|---------|-------|
| M1 | Meet Hindi | 3 | Introduction, Devanagari basics |
| M2 | Vowels (स्वर) | 5 | All 13 vowels with pronunciation |
| M3 | First Words | 4 | Basic vocabulary (20 words) |
| M4 | Listening Fun | 4 | Audio recognition exercises |

**L2 - Building Blocks (Elementary):**
- **Age Range:** 6-9 years
- **Focus:** Consonants, matras, reading basics
- **Modules:** 8 modules, 28 lessons
- **Free Tier:** No (Standard/Premium only)

| Module | Name | Lessons | Focus |
|--------|------|---------|-------|
| M1 | Ka-Group (क-वर्ग) | 3 | क ख ग घ ङ consonants |
| M2 | Cha-Group (च-वर्ग) | 3 | च छ ज झ ञ consonants |
| M3 | Ta-Retroflex (ट-वर्ग) | 3 | ट ठ ड ढ ण consonants |
| M4 | Ta-Dental (त-वर्ग) | 3 | त थ द ध न consonants |
| M5 | Pa-Group (प-वर्ग) | 3 | प फ ब भ म consonants |
| M6 | Matras (मात्राएँ) | 6 | All 12 matra signs |
| M7 | Remaining Consonants | 4 | य र ल व श ष स ह |
| M8 | Reading & Sentences | 3 | Simple sentence formation |

### Lesson Content Structure

Each lesson now has a rich `content` JSON field containing:

```json
{
  "introduction": "English introduction text",
  "introduction_hindi": "Hindi introduction text",
  "sections": [
    {
      "title": "Section Title",
      "items": ["Point 1", "Point 2", "..."]
    }
  ],
  "exercises": [
    {
      "type": "multiple_choice|fill_blank|true_false|pronunciation",
      "question": "Question text",
      "question_hindi": "Hindi question (optional)",
      "options": ["A", "B", "C", "D"],
      "correct": 0
    }
  ],
  "summary": ["Key takeaway 1", "Key takeaway 2"]
}
```

### Model Changes (Dec 2024)

**CurriculumLevel:** Added fields:
- `min_xp_required` - XP needed to unlock level
- `xp_reward` - XP earned on completion
- `is_free` - Available in free tier

**CurriculumModule:** Added fields:
- `objectives` - List of learning objectives
- `xp_reward` - XP earned on completion

**Lesson:** Added fields:
- `lesson_type` - INTRODUCTION, LEARNING, PRACTICE, REVIEW, STORY, ASSESSMENT
- `content` - JSONField for lesson content (sections, exercises, summary)
- `is_free` - Available in free tier

### Seed Command

```bash
# Seed all L1-L2 curriculum content
python manage.py seed_l1_l2_curriculum
```

**What it seeds:**
- 2 curriculum levels (L1 Discovery, L2 Building Blocks)
- 12 modules total (4 L1 + 8 L2)
- 44 lessons with full content JSON
- 70 vocabulary words (20 L1 + 50 L2)
- 10 stories with pages (3 L1 + 7 L2)

**Files:**
- `apps/curriculum/management/commands/seed_l1_l2_curriculum.py` - Comprehensive seed command

### Frontend Components

**LessonContentView.tsx** - New component that renders lesson content JSON:
- Stage-based progression: Introduction → Learning → Practice → Summary → Complete
- Interactive exercises (multiple choice, true/false)
- Audio playback for Hindi text
- Score tracking and star ratings
- Smooth animations with Framer Motion

**Location:** `src/components/curriculum/LessonContentView.tsx`

**Usage in lesson page:**
```tsx
<LessonContentView
  content={lesson.content}
  lessonType={lesson.lesson_type}
  language={activeChild?.language}
  onComplete={(score) => handleCompleteLesson()}
/>
```

### Type Definitions

**Location:** `src/types/curriculum.ts`

```typescript
type LessonType = 'INTRODUCTION' | 'LEARNING' | 'PRACTICE' | 'REVIEW' | 'STORY' | 'ASSESSMENT';

interface LessonContentSection {
  title: string;
  items: string[];
}

interface LessonExercise {
  type: 'multiple_choice' | 'fill_blank' | 'matching' | 'pronunciation' | 'listen_repeat' | 'true_false';
  question: string;
  question_hindi?: string;
  options?: string[];
  correct?: string | number;
  audio_text?: string;
  blank_answer?: string;
  pairs?: { hindi: string; english: string }[];
}

interface LessonContentJSON {
  introduction?: string;
  introduction_hindi?: string;
  sections?: LessonContentSection[];
  exercises?: LessonExercise[];
  summary?: string[];
}
```

### API Serializer Updates

**LessonDetailSerializer** now includes:
- `module` - Parent module UUID
- `lesson_type` - Type of lesson
- `content` - Full lesson content JSON
- `is_free` - Free tier availability

**CurriculumLevelSerializer** now includes:
- `min_xp_required` - XP required to unlock
- `xp_reward` - XP reward on completion
- `is_free` - Free tier availability

**CurriculumModuleSerializer** now includes:
- `objectives` - Learning objectives array
- `xp_reward` - XP reward on completion

### Vocabulary Themes Seeded

| Theme | L1 Words | L2 Words |
|-------|----------|----------|
| Family (परिवार) | 5 | 5 |
| Colors (रंग) | 5 | 5 |
| Numbers (संख्याएँ) | 5 | 5 |
| Animals (जानवर) | 5 | 5 |
| Actions (क्रियाएँ) | 0 | 5 |
| Body Parts (शरीर) | 0 | 5 |
| Food (खाना) | 0 | 5 |
| Nature (प्रकृति) | 0 | 5 |
| Greetings (अभिवादन) | 0 | 10 |

### Stories Seeded

**L1 Stories (Free, Simple):**
1. The Colorful Garden (रंगीन बाग़)
2. My Family (मेरा परिवार)
3. Counting Stars (तारे गिनना)

**L2 Stories (Standard/Premium):**
1. The Helpful Elephant (मददगार हाथी)
2. The Rainbow Fish (इंद्रधनुषी मछली)
3. A Day at School (स्कूल में एक दिन)
4. The Brave Mouse (बहादुर चूहा)
5. The Magic Garden (जादुई बगीचा)
6. The Little Cloud (छोटा बादल)
7. The Dancing Peacock (नाचता मोर)

### Implementation Notes

1. **Overlap Prevention:** Seed command uses `update_or_create` to safely update existing data
2. **Module Codes:** Use format `L1_M1_MODULE_NAME` for unique identification
3. **Lesson Codes:** Use format `L1_M1_L1` for hierarchical organization
4. **Content Quality:** Each lesson has 2-5 learning sections and 2-4 exercises
5. **Progressive Difficulty:** L1 exercises use English options, L2 introduces Hindi options

### Next Steps for L3-L10

The same structure can be extended:
- Create `seed_l3_l4_curriculum.py` following the same pattern
- Each level adds more complex content (grammar, compound words, reading)
- L6+ introduces Gyan (owl) as teacher for advanced learners

---

## L1-L2 Punjabi Curriculum Implementation (Dec 2024)

### Overview

Comprehensive L1-L2 Punjabi curriculum has been implemented following the same structure as Hindi. The curriculum includes Gurmukhi script, vocabulary, stories, songs, and games.

### Curriculum Structure

**L1 - Discovery (ਖੋਜ):**
- **Age Range:** 4-5 years
- **Focus:** Introduction to Punjabi, Gurmukhi script basics
- **Modules:** 4 modules, 16 lessons
- **Free Tier:** Yes (fully free)

**L2 - Building Blocks (ਨੀਂਹ):**
- **Age Range:** 5-6 years
- **Focus:** Consonants, matras, basic reading
- **Modules:** 8 modules, 28 lessons
- **Free Tier:** No (Standard/Premium only)

### Gurmukhi Script Content

| Category | Count | Examples |
|----------|-------|----------|
| Vowel Holders (ਮਾਤਰਾ ਵਾਹਕ) | 3 | ੳ, ਅ, ੲ |
| Vowels (ਸਵਰ) | 10 | ਆ, ਇ, ਈ, ਉ, ਊ, ਏ, ਐ, ਓ, ਔ, ਅੰ |
| Consonants (ਵਿਅੰਜਨ) | 32 | ਸ, ਹ, ਕ, ਖ, ਗ... |
| Matras (ਲਗਾਂ) | 10 | ਾ, ਿ, ੀ, ੁ, ੂ, ੇ, ੈ, ੋ, ੌ, ੰ |

### Vocabulary Themes Seeded

| Theme | L1 Words | L2 Words |
|-------|----------|----------|
| Family (ਪਰਿਵਾਰ) | 5 | 5 |
| Colors (ਰੰਗ) | 5 | 5 |
| Numbers (ਗਿਣਤੀ) | 5 | 5 |
| Animals (ਜਾਨਵਰ) | 5 | 5 |
| Body Parts (ਸਰੀਰ) | 0 | 5 |
| Actions (ਕਿਰਿਆਵਾਂ) | 0 | 5 |
| Food (ਖਾਣਾ) | 0 | 5 |
| Nature (ਕੁਦਰਤ) | 0 | 5 |
| Greetings (ਸਤਿਕਾਰ) | 0 | 5 |

**Total: 70 words**

### Stories Seeded

**L1 Stories (Free, Simple):**
1. Peppi's New Friend (ਪੈੱਪੀ ਦਾ ਨਵਾਂ ਦੋਸਤ)
2. The Red Apple (ਲਾਲ ਸੇਬ)
3. My Family (ਮੇਰਾ ਪਰਿਵਾਰ)

**L2 Stories (Standard/Premium):**
1. Vaisakhi Fair (ਵਿਸਾਖੀ ਦਾ ਮੇਲਾ)
2. The Clever Fox (ਚਤੁਰ ਲੂੰਬੜੀ)
3. Lohri Festival (ਲੋਹੜੀ ਦੀ ਰਾਤ)
4. Day at Farm (ਖੇਤ ਦਾ ਦਿਨ)
5. The Thirsty Crow (ਪਿਆਸਾ ਕਾਂ)
6. Guru Nanak's Birthday (ਗੁਰਪੁਰਬ)
7. Auckland Zoo (ਆਕਲੈਂਡ ਚਿੜੀਆਘਰ)

**Total: 12 stories** (including 2 pre-seeded stories)

### Songs Seeded

1. Hide and Seek (ਅੱਖ ਮਿਚੌਲੀ)
2. Uncle Moon (ਚੰਦਾ ਮਾਮਾ)
3. Alphabet Song (ਵਰਣਮਾਲਾ ਗੀਤ)
4. Colors Song (ਰੰਗ ਗੀਤ)
5. Lohri Song (ਲੋਹੜੀ ਗੀਤ)

### Peppi Punjabi Phrases

| Context | Punjabi | Romanized |
|---------|---------|-----------|
| Greeting | ਸਤ ਸ੍ਰੀ ਅਕਾਲ! | Sat Sri Akal! |
| Encouragement | ਬਹੁਤ ਵਧੀਆ! | Bahut vadiya! |
| Well Done | ਸ਼ਾਬਾਸ਼! | Shabash! |
| Let's Learn | ਚੱਲੋ ਸਿੱਖੀਏ! | Chalo sikhiye! |
| Try Again | ਫੇਰ ਕੋਸ਼ਿਸ਼ ਕਰੋ! | Pher koshish karo! |

### Seed Command

```bash
# Seed all Punjabi L1-L2 curriculum content
python manage.py seed_punjabi_l1_l2
```

**Files:**
- `apps/curriculum/management/commands/seed_punjabi_l1_l2.py` - Complete seed command

### Language Selector Update

Punjabi is now available in the language selector (moved from "Coming Soon"):
- File: `src/components/ui/LanguageSelector.tsx`
- Available languages: `['HINDI', 'PUNJABI', 'TAMIL']`

### Gurmukhi Keyboard Layout

The IndianLanguageKeyboard has been enhanced with complete Gurmukhi support:
- **Vowel Holders:** ੳ, ਅ, ੲ (unique to Gurmukhi)
- **Extended Consonants:** ੜ, ਸ਼, ਖ਼, ਗ਼, ਜ਼, ਫ਼, ਲ਼
- **Special Characters:** ੴ (Ik Onkar - sacred symbol)
- **Complete Matras:** Including ੰ (tippi) and ੱ (addak)

File: `src/components/ui/IndianLanguageKeyboard.tsx`

---

## L1-L2 Tamil Curriculum Implementation (Dec 2024)

### Overview

Comprehensive L1-L2 Tamil curriculum has been implemented following the same structure as Hindi and Punjabi. The curriculum includes Tamil script, vocabulary, stories, songs, and games.

### Curriculum Structure

**L1 - Discovery (கண்டுபிடிப்பு):**
- **Age Range:** 4-5 years
- **Focus:** Introduction to Tamil, script basics
- **Modules:** 4 modules, 16 lessons
- **Free Tier:** Yes (fully free)

**L2 - Building Blocks (அடித்தளம்):**
- **Age Range:** 5-6 years
- **Focus:** Consonants, matras, basic reading
- **Modules:** 8 modules, 28 lessons
- **Free Tier:** No (Standard/Premium only)

### Tamil Script Content

| Category | Count | Examples |
|----------|-------|----------|
| Vowels (உயிர் எழுத்துக்கள்) | 12 | அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ |
| Consonants (மெய் எழுத்துக்கள்) | 18 | க, ங, ச, ஞ, ட, ண, த, ந, ப, ம, ய, ர, ல, வ, ழ, ள, ற, ன |
| Grantha Letters | 6 | ஜ, ஷ, ஸ, ஹ, க்ஷ, ஶ்ரீ |
| Special (அஃது) | 1 | ஃ (Aytham) |
| Matras (உயிர்மெய்) | 12 | ா, ி, ீ, ு, ூ, ெ, ே, ை, ொ, ோ, ௌ, ் |

### Vocabulary Themes Seeded

| Theme | Words | Examples |
|-------|-------|----------|
| Family (குடும்பம்) | 6 | அம்மா, அப்பா, தாத்தா, பாட்டி |
| Colors (நிறங்கள்) | 5 | சிவப்பு, நீலம், மஞ்சள் |
| Numbers (எண்கள்) | 10 | ஒன்று, இரண்டு, மூன்று |
| Animals (விலங்குகள்) | 6 | நாய், பூனை, பசு |
| Body Parts (உடல் உறுப்புகள்) | 7 | தலை, கண், மூக்கு |
| Actions (செயல்கள்) | 6 | சாப்பிடு, குடி, தூங்கு |
| Food (உணவு) | 5 | பால், இட்லி, சாதம் |
| Nature (இயற்கை) | 5 | சூரியன், நிலா, மரம் |
| Home (வீடு) | 6 | வீடு, அறை, கதவு |
| Greetings (வாழ்த்துக்கள்) | 5 | வணக்கம், நன்றி |

**Total: 70 words**

### Stories Seeded

**L1 Stories (Free, Simple):**
1. Peppi's New Friend (பெப்பியின் புதிய நண்பன்)
2. The Red Apple (சிவப்பு ஆப்பிள்)
3. My Family (என் குடும்பம்)

**L2 Stories (Standard/Premium):**
1. Pongal Festival (பொங்கல் திருநாள்)
2. The Clever Crow (புத்திசாலி காகம்)
3. Diwali Night (தீபாவளி இரவு)
4. Day at Beach (கடற்கரை பயணம்)
5. The Thirsty Crow (தாகமுள்ள காகம்)
6. Onam Festival (ஓணம் பண்டிகை)
7. Auckland Zoo (ஆக்லாந்து உயிரியல் பூங்கா)

**Total: 10 stories**

### Songs Seeded

1. Moon Song (நிலா நிலா) - Classic nursery rhyme
2. Tamil Alphabet Song (தமிழ் அகராதி) - Letter learning
3. Colors Song (வண்ணங்கள் பாடல்) - Color vocabulary
4. Numbers Song (எண்கள் பாடல்) - Counting 1-10
5. Thirukkural Song (திருக்குறள் பாடல்) - Classic poetry

### Peppi Tamil Phrases

| Context | Tamil | Romanized |
|---------|-------|-----------|
| Greeting | வணக்கம்! | Vanakkam! |
| Encouragement | மிக நல்லது! | Miga nalladu! |
| Well Done | சபாஷ்! | Shabash! |
| Let's Go | வா போகலாம்! | Vaa pogalam! |
| Try Again | மறுபடியும் முயற்சி செய்! | Marupadiyum muyarchi sei! |
| Thanks | நன்றி! | Nandri! |

### Seed Command

```bash
# Seed all Tamil L1-L2 curriculum content
python manage.py seed_tamil_l1_l2 --clear
```

**Files:**
- `apps/curriculum/management/commands/seed_tamil_l1_l2.py` - Complete seed command (1135 lines)

### Language Selector Update

Tamil is now available in the language selector (moved from "Coming Soon"):
- File: `src/components/ui/LanguageSelector.tsx`
- Available languages: `['HINDI', 'PUNJABI', 'TAMIL']`

---

## Audio Caching System (Dec 2024)

### Overview

Multi-language audio caching command to pre-generate TTS audio for all curriculum content using Svara TTS (free tier via HuggingFace Spaces).

### Command Usage

```bash
# Cache all languages
python manage.py cache_all_audio

# Cache specific language
python manage.py cache_all_audio --language TAMIL

# Dry run to see what would be cached
python manage.py cache_all_audio --dry-run

# Force regenerate (overwrite cached)
python manage.py cache_all_audio --force

# Adjust delay between API calls
python manage.py cache_all_audio --delay 0.5
```

### Content Types Cached

| Type | Description |
|------|-------------|
| Letters | Each letter character + example word |
| Matras | Each matra symbol + example with consonant |
| Vocabulary | All vocabulary words |
| Peppi Phrases | Peppi feedback phrases (Hindi only) |

### Total Items by Language

| Language | Letters | Matras | Vocab | Peppi | Total |
|----------|---------|--------|-------|-------|-------|
| HINDI | 66 | 24 | 110 | 49 | 249 |
| PUNJABI | 89 | 20 | 70 | 0 | 179 |
| TAMIL | 42 | 24 | 70 | 0 | 136 |

**Grand Total: ~564 audio items**

### TTS Provider

Uses Svara TTS via HuggingFace Spaces (`kenpath/svara-tts`):
- Free tier (no API key required)
- Supports 12 Indian languages
- ~50-120 seconds per generation
- Requires `gradio-client` package

### Files

- `apps/speech/management/commands/cache_all_audio.py` - Main command
- `apps/speech/services/mms_provider.py` - Svara TTS provider
- `requirements/base.txt` - Added `gradio-client>=2.0.0`

---

## Bug Fixes and Improvements (Dec 2024)

### Backend Fixes

1. **Homepage Progress AttributeError Fix**
   - Fixed `AttributeError: 'CurriculumLevel' object has no attribute 'name'`
   - Changed to use correct field names: `name_english`, `name_hindi`, `title_english`, `title_hindi`
   - File: `apps/curriculum/views/level.py` (line 475)

2. **Peppi AI Google Gemini Integration**
   - Fixed invalid model ID `gemini-2.5-flash` to `gemini-2.0-flash-exp`
   - Made model settings configurable via Django settings
   - Added dynamic configuration from `.env` file
   - File: `apps/peppi_chat/services/gemini_service.py`

   **Required .env settings:**
   ```env
   GOOGLE_GEMINI_API_KEY=your-actual-api-key
   GEMINI_MODEL_ID=gemini-2.0-flash-exp
   PEPPI_CHAT_MAX_TOKENS=1024
   PEPPI_CHAT_TEMPERATURE=0.7
   ```

### Frontend Fixes

1. **Learn Page Dynamic Stats**
   - Removed hardcoded stats (49/80/5)
   - Now fetches real data from API for letters, words, grammar topics
   - Added loading state with `-` placeholder
   - File: `src/app/learn/page.tsx`

2. **Serializer Updates**
   - Updated `LessonDetailSerializer` to include `content`, `lesson_type`, `is_free`
   - Updated `CurriculumLevelSerializer` to include `min_xp_required`, `xp_reward`, `is_free`
   - Updated `CurriculumModuleSerializer` to include `objectives`, `xp_reward`
   - File: `apps/curriculum/serializers/level.py`

---

## Indian Language Keyboard (Dec 2024)

### Overview

A digital Indian language keyboard component supporting 7 languages for typing practice in Peppi chat and other input areas.

### Supported Languages

| Language | Script | Native Name | Flag |
|----------|--------|-------------|------|
| Hindi | Devanagari | हिंदी | 🇮🇳 |
| Tamil | Tamil Script | தமிழ் | 🇮🇳 |
| Telugu | Telugu Script | తెలుగు | 🇮🇳 |
| Gujarati | Gujarati Script | ગુજરાતી | 🇮🇳 |
| Punjabi | Gurmukhi | ਪੰਜਾਬੀ | 🇮🇳 |
| Bengali | Bengali Script | বাংলা | 🇮🇳 |
| Malayalam | Malayalam Script | മലയാളം | 🇮🇳 |
| **Fiji Hindi** | Devanagari | फ़िजी हिंदी | 🇫🇯 |

### Component Location

`src/components/ui/IndianLanguageKeyboard.tsx`

### Features

- **Tab-based layout:** Consonants, Vowels, Matras, Numbers
- **Language switching:** Click globe icon to switch languages
- **Matra preview:** Shows matras applied to a base consonant (क)
- **Smooth animations:** Framer Motion for transitions
- **Delete key:** Backspace functionality
- **Space and punctuation:** Available in Numbers tab

### Keyboard Layout Structure

Each language has:
- `vowels[]` - All vowel characters
- `consonants[][]` - Consonants organized in rows (vargas)
- `matras[]` - Combining vowel signs
- `numbers[]` - Native numerals
- `punctuation[]` - Common punctuation marks

### Integration with Peppi Chat

The keyboard is integrated into `PeppiChatInput.tsx`:
- Keyboard toggle button (keyboard icon)
- Language indicator shows current typing language
- Characters inserted at cursor position
- Delete removes last character

### Usage Example

```tsx
import { IndianLanguageKeyboard } from '@/components/ui';

<IndianLanguageKeyboard
  language="HINDI"
  onInput={(char) => setInput(prev => prev + char)}
  onDelete={() => setInput(prev => prev.slice(0, -1))}
  onClose={() => setShowKeyboard(false)}
  onLanguageChange={(lang) => setLanguage(lang)}
  isOpen={showKeyboard}
/>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `language` | LanguageCode | Current keyboard language |
| `onInput` | (char: string) => void | Called when a key is pressed |
| `onDelete` | () => void | Called when delete is pressed |
| `onClose` | () => void | Called when close button clicked |
| `onLanguageChange` | (lang: LanguageCode) => void | Called when language changed |
| `isOpen` | boolean | Whether keyboard is visible |
| `onPlaySound` | (char: string) => void | Optional audio callback |

---

## Fiji Hindi Language Support (Dec 2024)

### Overview

Fiji Hindi is a unique dialect spoken by the Indo-Fijian community, descendants of Indian indentured laborers (Girmitiya) who arrived in Fiji from 1879-1916. It has distinctive features that differentiate it from Standard Hindi.

### Key Linguistic Features

| Feature | Standard Hindi | Fiji Hindi |
|---------|----------------|------------|
| "Two" | दो (do) | दुइ (dui) |
| "Mother" | माँ (maa) | माई (maai) |
| "He/She" | वह (vah) | ऊ (oo) |
| "This" | यह (yah) | ई (ee) |
| "How are you?" | कैसे हो? | कइसे बा? |
| Past tense (masc.) | गया (gaya) | गइस (gais) |
| Past tense (fem.) | गई (gayi) | गइन (gain) |
| Copula "is" | है (hai) | बा (ba) |

### Fijian Loanwords

| Word | Romanized | Meaning |
|------|-----------|---------|
| बुला | bula | Hello (Fijian greeting) |
| विनाका | vinaka | Thank you (Fijian) |
| दालो | daalo | Taro root |
| कासावा | kaasava | Cassava |
| याकोना | yaakona | Kava drink |

### Curriculum Content

- **Vocabulary Themes**: 16 (107+ words)
- **Stories**: 15 (including Girmit history, Fiji Day, Diwali in Fiji)
- **Songs**: 5 (counting, greetings, family)
- **Grammar Topics**: 5 (unique Fiji Hindi features)
- **Games**: 5
- **Peppi Phrases**: 14 (with Fijian greetings)

### TTS Configuration

Fiji Hindi uses Hindi TTS voice (hi-IN) since it's based on Devanagari script:
```python
'FIJI_HINDI': {
    'language_code': 'hi-IN',
    'voice_name': 'hi-IN-Standard-D',
    'wavenet_voice': 'hi-IN-Wavenet-D',
}
```

### Seed Command

```bash
python manage.py seed_fiji_hindi          # Seed Fiji Hindi curriculum
python manage.py seed_fiji_hindi --clear  # Clear and reseed
```

### Files

- `apps/curriculum/management/commands/seed_fiji_hindi.py` - Seed command
- `apps/children/models.py` - FIJI_HINDI in Language choices
- `apps/speech/services/google_provider.py` - TTS voice mapping

---

## Grammar Content System (Dec 2024)

### Overview

Comprehensive grammar content has been seeded for Hindi, Tamil, and Punjabi languages. Each language has topics, rules, and exercises designed for children ages 4-14.

### Grammar Topics by Language

| Language | Topics | Rules | Exercises |
|----------|--------|-------|-----------|
| **Hindi** | 6 | 20 | 21 |
| **Tamil** | 5 | 28 | 31 |
| **Punjabi** | 5 | 14 | 19 |
| **Total** | 16 | 62 | 71 |

### Grammar Topics Structure

**Common Topics Across Languages:**
1. **Sentence Structure** (वाक्य संरचना / வாக்கிய அமைப்பு / ਵਾਕ ਬਣਤਰ)
   - Basic sentence order (Subject-Object-Verb in Indian languages)
   - Simple and complex sentences

2. **Gender/Case Markers** (लिंग / பால் / ਲਿੰਗ)
   - Masculine/Feminine distinctions
   - Case markers and postpositions

3. **Pronouns** (सर्वनाम / பிரதிபெயர்கள் / ਪੜਨਾਂਵ)
   - Personal pronouns (I, you, he, she, we, they)
   - Respectful vs. informal forms

4. **Numbers** (संख्याएँ / எண்கள் / ਗਿਣਤੀ)
   - Counting 1-100
   - Ordinal numbers

5. **Verb Conjugation** (क्रियाएँ / வினைச்சொற்கள் / ਕਿਰਿਆਵਾਂ)
   - Present, past, future tenses
   - Basic verb forms

### Seed Command

```bash
# Seed all languages
python manage.py seed_grammar_content

# Seed specific language
python manage.py seed_grammar_content --language TAMIL

# Clear and reseed
python manage.py seed_grammar_content --clear
```

**File:** `apps/curriculum/management/commands/seed_grammar_content.py`

---

## Stories Content System (Dec 2024)

### Overview

Stories have been seeded for all 4 languages (Hindi, Tamil, Punjabi, Gujarati), including regular stories and festival-specific stories linked to the festivals system.

### Stories by Language

| Language | Total Stories | BhashaMitra Stories | Festival Stories |
|----------|---------------|---------------------|------------------|
| **Hindi** | 42 | 13 | 3 (Diwali, Holi, Raksha Bandhan) |
| **Tamil** | 21 | 11 | 2 (Pongal, Diwali) |
| **Punjabi** | 18 | 8 | 2 (Vaisakhi, Diwali) |
| **Gujarati** | 7 | 7 | 2 (Navratri, Diwali) |
| **Total** | 88 | 39 | 9 |

### Regular Stories

**Available for all languages:**
1. **Peppi's New Friend** - Peppi the parrot makes a new friend in the garden
2. **The Red Apple** - A child finds a red apple and shares it with friends
3. **My Family** - A child introduces their loving family members
4. **The Thirsty Crow** - Classic fable about a clever crow (Level 2)
5. **The Clever Fox** - A fox uses wit to escape trouble (Level 2)
6. **The Greedy Dog** (Tamil only) - Classic fable about greed

### Festival Stories

Stories are linked to festivals via the `FestivalStory` junction table:

| Festival | Languages | Primary Story |
|----------|-----------|---------------|
| **Diwali** | Hindi, Tamil, Punjabi, Gujarati | Lights celebration |
| **Holi** | Hindi | Colors celebration |
| **Pongal** | Tamil | Harvest festival |
| **Navratri** | Gujarati | Garba and Dandiya |
| **Raksha Bandhan** | Hindi | Sibling bond |
| **Vaisakhi** | Punjabi | Harvest festival (story created, festival not linked*) |

*Note: Vaisakhi festival needs to be seeded separately for linking.

### Story Structure

Each story includes:
- `storyweaver_id`: Unique identifier (format: `bm-{lang}-{number}`)
- `title`: Native script title
- `title_translit`: Romanized title
- `language`: HINDI, TAMIL, PUNJABI, or GUJARATI
- `level`: 1-5 difficulty
- `page_count`: Number of pages
- `tier`: FREE, STANDARD, or PREMIUM
- `categories`: JSON array of tags (e.g., `['friendship', 'animals']`)
- `is_l1_content`: Boolean for L1 curriculum content

### Story Pages

Each story has multiple `StoryPage` records with:
- `page_number`: Sequential page number
- `text_content`: Native script text
- `text_romanized`: Romanized pronunciation guide

### Seed Command

```bash
# Seed all languages
python manage.py seed_stories

# Seed specific language
python manage.py seed_stories --language GUJARATI

# Clear and reseed
python manage.py seed_stories --clear
```

**File:** `apps/stories/management/commands/seed_stories.py`

---

## Recently Completed (Dec 22, 2024)

### Grammar Content Seeding
- [x] Created `seed_grammar_content.py` management command
- [x] Seeded 6 Hindi grammar topics with 20 rules and 21 exercises
- [x] Seeded 5 Tamil grammar topics with 28 rules and 31 exercises
- [x] Seeded 5 Punjabi grammar topics with 14 rules and 19 exercises
- [x] Total: 16 topics, 62 rules, 71 exercises across 3 languages

### Stories Content Seeding
- [x] Created `seed_stories.py` management command
- [x] Seeded 8 Hindi stories (5 regular + 3 festival)
- [x] Seeded 8 Tamil stories (6 regular + 2 festival)
- [x] Seeded 6 Punjabi stories (4 regular + 2 festival)
- [x] Seeded 5 Gujarati stories (3 regular + 2 festival)
- [x] Linked festival stories to Festival model
- [x] Total: 88 stories in database

### Festival Story Linking
- [x] Diwali linked in all 4 languages
- [x] Holi linked in Hindi
- [x] Pongal linked in Tamil
- [x] Navratri linked in Gujarati
- [x] Raksha Bandhan linked in Hindi

---
