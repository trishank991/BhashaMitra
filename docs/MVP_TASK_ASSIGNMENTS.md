pronunciation_scorer.py# BhashaMitra MVP Task Assignments

**Document Version:** 1.0  
**Last Updated:** January 6, 2026  
**Status:** Active Sprint - MVP Launch  

---

## 🎯 Project Overview

BhashaMitra is a heritage language learning platform for diaspora children (ages 3-10). This document assigns specific tasks to development agents (Frontend & Backend) under CTO supervision for the MVP launch.

---

## 👥 Team Structure

### CTO (Supervisor)
**Role:** Final approval authority on all technical decisions  
**Responsibilities:**
- Review all code changes before merge
- Approve architecture decisions
- Validate feature implementations match business requirements
- Sign off on MVP launch readiness

### Backend Developer Agent
**Stack:** Django 4.2, Django REST Framework, PostgreSQL, Cloudflare R2  
**Primary Files:**
- `bhashamitra-backend/apps/speech/` - STT/TTS services
- `bhashamitra-backend/apps/challenges/` - Challenge system
- `bhashamitra-backend/apps/family/` - Family feature
- `bhashamitra-backend/config/` - Django configuration

### Frontend Developer Agent
**Stack:** Next.js 14, TypeScript, TailwindCSS, Framer Motion  
**Primary Files:**
- `bhashamitra-frontend/src/app/` - App routes
- `bhashamitra-frontend/src/components/` - UI components
- `bhashamitra-frontend/src/lib/api.ts` - API client
- `bhashamitra-frontend/src/stores/` - Zustand stores

---

## 📋 Feature 1: Peppi Mimic (Pronunciation Practice)

### Overview
Children practice pronunciation by listening to a word, recording themselves, and receiving feedback via STT (Speech-to-Text) scoring.

### Backend Tasks
| Task | File | Status | Priority |
|------|------|--------|----------|
| ✅ Google STT Integration | `apps/speech/services/stt_service.py` | Complete | P0 |
| ✅ Pronunciation Scoring V2 | `apps/speech/services/pronunciation_scorer.py` | Complete | P0 |
| ✅ Mimic API Endpoints | `apps/speech/views.py` | Complete | P0 |
| ✅ Mimic Models | `apps/speech/models.py` | Complete | P0 |
| ⏳ Audio Upload to R2 | `apps/speech/views.py:AudioUploadView` | Needs Testing | P1 |
| ⏳ Reference Audio Caching | `apps/speech/services/cache_service.py` | Needs Verification | P2 |

**Scoring Algorithm (V2 Hybrid):**
```python
# Weight distribution for pronunciation scoring
WEIGHT_STT = 0.50      # STT confidence score (50%)
WEIGHT_TEXT = 0.30     # Text match score (30%)  
WEIGHT_ENERGY = 0.15   # Audio energy/volume (15%)
WEIGHT_DURATION = 0.05 # Duration match (5%)
EXACT_MATCH_BONUS = 10 # Bonus points for exact match

# Star thresholds
THREE_STAR = 85+   # "PURRRFECT!"
TWO_STAR = 65-84   # "Almost purrrfect!"
ONE_STAR = 40-64   # "Good try, let's try again!"
ZERO_STAR = <40    # Participation points
```

### Frontend Tasks
| Task | File | Status | Priority |
|------|------|--------|----------|
| ✅ Recording Interface | `components/mimic/RecordingInterface.tsx` | Complete | P0 |
| ✅ Challenge List Page | `app/practice/mimic/page.tsx` | Complete | P0 |
| ✅ API Integration | `lib/api.ts` | Fixed URL issues | P0 |
| ⏳ Challenge Detail Page | `app/practice/mimic/[id]/page.tsx` | Needs Creation | P1 |
| ⏳ Result Display | `components/mimic/ResultDisplay.tsx` | Needs Wiring | P1 |
| ⏳ Share to WhatsApp | `components/mimic/ShareButton.tsx` | Needs Testing | P2 |

### Integration Points (Frontend ↔ Backend)

**1. Get Challenges List**
```typescript
// Frontend (api.ts)
getMimicChallenges(childId, filters) 
→ GET /api/v1/speech/mimic/challenges/?child_id={childId}

// Backend response
{
  challenges: [{
    id: string,
    word: string,           // Hindi: "नमस्ते"
    romanization: string,   // "namaste"
    meaning: string,        // "Hello"
    audio_url: string,      // Reference pronunciation
    category: string,       // GREETING, FAMILY, etc.
    difficulty: 1|2|3,
    mastered: boolean,
    best_stars: 0|1|2|3,
    attempts: number
  }]
}
```

**2. Submit Attempt**
```typescript
// Frontend flow
1. RecordingInterface captures audio blob
2. uploadMimicAudio(childId, blob) → POST /api/v1/speech/upload-audio/
   Returns: { audio_url: string }
3. submitMimicAttempt(childId, challengeId, { audio_url, duration_ms })
   → POST /api/v1/children/{childId}/mimic/challenges/{challengeId}/attempt/

// Backend response
{
  attempt_id: string,
  transcription: string,     // What STT heard
  score: number,             // 0-100
  stars: 0|1|2|3,
  points_earned: number,
  is_personal_best: boolean,
  mastered: boolean,
  peppi_feedback: string,    // Peppi's encouragement
  share_message: string,     // WhatsApp share text
  score_breakdown: {         // V2 detailed breakdown
    stt_confidence: { raw, weighted, weight },
    text_match: { raw, weighted, weight },
    energy: { raw, weighted, weight },
    duration: { raw, weighted, weight },
    exact_match_bonus: number
  }
}
```

### Environment Variables Required
```bash
# Backend (.env)
GOOGLE_TTS_API_KEY=xxx          # For Google STT (same key as TTS)
GOOGLE_CREDENTIALS_BASE64=xxx   # OR base64-encoded service account
SARVAM_API_KEY=xxx              # Fallback STT provider
AWS_ACCESS_KEY_ID=xxx           # R2 storage
AWS_SECRET_ACCESS_KEY=xxx       # R2 storage
```

---

## 📋 Feature 2: Challenge Friends (Viral Quiz)

### Overview
Users create language quizzes that can be shared via WhatsApp links. Friends can play without account, see leaderboard.

### Backend Tasks
| Task | File | Status | Priority |
|------|------|--------|----------|
| ✅ Challenge Models | `apps/challenges/models.py` | Complete | P0 |
| ✅ Public Play Endpoint | `apps/challenges/views.py` | Complete | P0 |
| ✅ Leaderboard | `apps/challenges/views.py` | Complete | P0 |
| ⏳ Question Generation | `apps/challenges/services/` | Needs Logic Review | P1 |
| ⏳ Category Validation | `apps/challenges/views.py` | Fixed | P1 |

### Frontend Tasks
| Task | File | Status | Priority |
|------|------|--------|----------|
| ✅ Create Challenge Form | `components/challenges/CreateChallengeForm.tsx` | Complete | P0 |
| ✅ Challenge Quiz UI | `components/challenges/ChallengeQuiz.tsx` | Complete | P0 |
| ✅ Leaderboard Display | `components/challenges/ChallengeLeaderboard.tsx` | Complete | P0 |
| ⏳ Share Button | `components/challenges/ShareButton.tsx` | Needs Testing | P1 |
| ⏳ Result Display | `components/challenges/ChallengeResult.tsx` | Needs Wiring | P1 |

### Integration Points
```typescript
// Public challenge play (no auth required)
GET /api/v1/challenges/play/{CODE}/ → Challenge with questions
POST /api/v1/challenges/play/{CODE}/ → Start attempt
POST /api/v1/challenges/submit/ → Submit answers, get score
GET /api/v1/challenges/leaderboard/{CODE}/ → View rankings

// Auth required
GET /api/v1/challenges/ → My challenges
POST /api/v1/challenges/ → Create challenge
GET /api/v1/challenges/categories/?language=HINDI → Get categories
```

---

## 🔐 Test Credentials

### Localhost Development (port 3000 frontend, 8000 backend)
```
Email: free@test.com      | Password: test1234  | Tier: FREE
Email: standard@test.com  | Password: test1234  | Tier: STANDARD
Email: premium@test.com   | Password: test1234  | Tier: PREMIUM
```

### Production (Live Website)
```
Use Google OAuth or create new account
Environment: https://bhashamitra.com (configure in .env)
API: https://api.bhashamitra.com
```

---

## 🐛 Bugs Fixed This Sprint

### Critical (P0)
1. **[FIXED]** `apps/family/services.py:9` - Missing import `CurriculumChallengeParticipantSerializer`
2. **[FIXED]** `lib/api.ts:943` - Double URL prefix `/api/v1/api/v1/challenges/categories/`
3. **[FIXED]** `lib/api.ts:961` - Double URL prefix `/api/v1/api/v1/speech/mimic/challenges/`

### Medium (P1)
1. **[REVIEW NEEDED]** Audio upload to R2 storage - needs end-to-end test
2. **[REVIEW NEEDED]** STT transcription for children's voices - may need tuning

---

## 📊 MVP Launch Checklist

### Pre-Launch (CTO Approval Required)
- [ ] All P0 bugs fixed
- [ ] Test credentials working on localhost
- [ ] Mimic feature end-to-end tested
- [ ] Challenge feature end-to-end tested
- [ ] Google STT API key configured
- [ ] R2 storage configured for audio uploads
- [ ] Production environment variables set

### Launch Day
- [ ] Database migrations run
- [ ] Seed data deployed (mimic challenges)
- [ ] Frontend deployed to Vercel/Cloudflare Pages
- [ ] Backend deployed to Render/Railway
- [ ] Monitoring enabled (Sentry)
- [ ] WhatsApp share links working

---

## 📞 Communication Protocol

### Frontend → Backend Questions
1. Check API documentation first (`apps/*/views.py` docstrings)
2. Review existing tests (`tests/test_*.py`)
3. Escalate to CTO if architecture unclear

### Backend → Frontend Questions
1. Check type definitions (`src/types/*.ts`)
2. Review API client (`src/lib/api.ts`)
3. Escalate to CTO if UX requirements unclear

### Daily Sync
- Backend: Report API readiness status
- Frontend: Report UI integration status
- CTO: Review blockers, approve changes

---

## 🎓 Technical References

### STT Service Priority
1. **Google Cloud STT** (Primary) - Best accuracy for Indian languages
2. **Sarvam AI STT** (Fallback) - When Google unavailable
3. **Mock STT** (Development) - Returns expected word with random variation

### Pronunciation Scoring
The V2 hybrid scoring algorithm combines:
- **STT Confidence (50%):** How clearly the speech was recognized
- **Text Match (30%):** Levenshtein similarity to expected word
- **Audio Energy (15%):** RMS analysis for volume/clarity
- **Duration Match (5%):** Recording length vs reference

### Star Rating Feedback
```javascript
// Peppi's feedback messages (cat-themed)
3 stars: "MEOW! That was PURRRFECT! You're a paw-some language star!"
2 stars: "Meow meow! Almost purrrfect! You're doing great!"
1 star:  "Meow! Good try little cub! Let's try one more time!"
0 stars: "Meow! Keep practicing, you'll get it!"
```

---

**Document maintained by:** Development Team  
**Next Review:** Before MVP Launch  
**CTO Sign-off Required:** ✓
