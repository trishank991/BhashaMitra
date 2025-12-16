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
- **Framework**: Django 6.0 + Django REST Framework 3.16
- **Database**: SQLite (dev) / PostgreSQL (prod via Supabase)
- **Auth**: JWT (SimpleJWT)
- **Cache**: Redis (optional)
- **Storage**: Cloudflare R2 / AWS S3 (production)
- **TTS**: HuggingFace Spaces (Svara TTS + Parler TTS fallback)

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
| HuggingFace Spaces | TTS (Svara TTS + Parler fallback) | `HUGGINGFACE_API_TOKEN` in .env |
| StoryWeaver | 53K+ CC-licensed stories | Public API |
| Supabase | PostgreSQL database (prod) | `DB_*` vars in .env |
| Cloudflare R2 | Media storage | `R2_*` vars in .env |
| Resend | Email service | `RESEND_API_KEY` in .env |
| Sentry | Error tracking | `SENTRY_DSN` in .env |

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

1. **Svara TTS (Tier 1 & 2)**: HuggingFace Space `kenpath/svara-tts`
   - Free tier: Only serves pre-cached content (alphabet, vocabulary, stories)
   - Standard tier: Real-time generation for any content
   - ~50-70s per generation, good quality AI voice
   - Supports 12 Indian languages

2. **Sarvam AI Bulbul V2 (Tier 3 Premium)**:
   - API: `https://api.sarvam.ai/text-to-speech`
   - Model: `bulbul:v2`
   - Human-like voice quality, ~1.5s generation (40x faster than Svara)
   - Languages: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Odia
   - Cost: ~NZD $1.80/user/month estimated, ~$0.36 with 80% cache hit rate
   - **Selected Voices (Dec 2024):**
     - Female: **manisha** (clear, energetic) - primary voice for curriculum
     - Male: **abhilash** (friendly teacher voice)
   - Available voices (all tested, can switch anytime):
     - Female: anushka (warm), manisha (clear), vidya (expressive), arya (friendly)
     - Male: abhilash (friendly), karun (professional), hitesh (casual)

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
# Sarvam AI TTS (Tier 3 - Premium)
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

Uses Sarvam AI Bulbul V2 voices for premium quality narration:

```python
PEPPI_VOICE_CONFIG = {
    'hindi': {
        'male': {'speaker': 'arvind', 'pitch': 0.4, 'pace': 0.85, 'model': 'bulbul:v2'},
        'female': {'speaker': 'meera', 'pitch': 0.3, 'pace': 0.85, 'model': 'bulbul:v2'}
    },
    'tamil': {
        'male': {'speaker': 'kumar', 'pitch': 0.4, 'pace': 0.85, 'model': 'bulbul:v2'},
        'female': {'speaker': 'manisha', 'pitch': 0.3, 'pace': 0.85, 'model': 'bulbul:v2'}
    },
    'gujarati': {
        'male': {'speaker': 'arvind', 'pitch': 0.4, 'pace': 0.85, 'model': 'bulbul:v2'},
        'female': {'speaker': 'meera', 'pitch': 0.3, 'pace': 0.85, 'model': 'bulbul:v2'}
    },
    'punjabi': {
        'male': {'speaker': 'arvind', 'pitch': 0.4, 'pace': 0.85, 'model': 'bulbul:v2'},
        'female': {'speaker': 'meera', 'pitch': 0.3, 'pace': 0.85, 'model': 'bulbul:v2'}
    }
}
```

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

## Development Notes

- When working on backend, always check if venv is activated
- Backend uses Django 6.0 (upgraded from 5.x)
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
