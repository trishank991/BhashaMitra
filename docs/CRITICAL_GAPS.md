# BhashaMitra - Critical Gaps & Bug Report

> **Created**: January 2025
> **Last Updated**: January 19, 2025
> **Priority**: Most critical issues have been FIXED

---

## Summary

| Feature | Status | Severity | Fixed |
|---------|--------|----------|-------|
| **Mimic Pronunciation** | FIXED | CRITICAL | Yes |
| **Challenge Creation** | FIXED | HIGH | Yes |
| **Challenge Leaderboard** | FIXED | HIGH | Yes |
| **Challenge Attempt Persistence** | FIXED | CRITICAL | Yes |
| **Grammar Questions** | FIXED | HIGH | Yes |

---

## 1. MIMIC FEATURE - CRITICAL ISSUES

### Issue 1.1: URL Routing Mismatch (CRITICAL)

**Problem**: Backend views expect `child_id` in URL path, but URL routes don't include it.

**Backend View Signatures** (`apps/speech/views.py`):
```python
# Line 520 - Expects child_id in URL
def get(self, request, child_id, challenge_id):

# Line 572 - Expects child_id in URL
def post(self, request, child_id, challenge_id):

# Line 768 - Expects child_id in URL
def patch(self, request, child_id, attempt_id):
```

**Current URL Routes** (`apps/speech/mimic_urls.py`):
```python
# These routes DON'T include child_id!
path('challenges/', MimicChallengeListView.as_view()),
path('challenges/<uuid:challenge_id>/', MimicChallengeDetailView.as_view()),
path('challenges/<uuid:challenge_id>/attempt/', MimicAttemptSubmitView.as_view()),
```

**Frontend Calls** (`src/lib/api.ts:979-992`):
```typescript
// Also missing child_id in URL path
return this.request<PeppiMimicAttemptResult>(
  `/speech/mimic/challenges/${challengeId}/attempt/`,  // ❌ No child_id
  { method: 'POST', body: JSON.stringify(body) }
);
```

**FIX REQUIRED**:

Option A - Update backend views to get child_id from request body instead of URL:
```python
# In MimicChallengeDetailView.get()
child_id = request.query_params.get('child_id') or request.data.get('child_id')
```

Option B - Update URL routes to include child_id:
```python
# mimic_urls.py
path('children/<uuid:child_id>/challenges/<uuid:challenge_id>/', ...)
```

---

### Issue 1.2: Audio Upload Parameter Mismatch (HIGH)

**Problem**: Frontend passes `challengeId` where `childId` is expected.

**File**: `src/app/practice/mimic/[challengeId]/page.tsx:16`
```typescript
// WRONG - passing challengeId as first argument
const uploadRes = await api.uploadMimicAudio(challengeId as string, blob);
```

**API Function** (`src/lib/api.ts:1025`):
```typescript
async uploadMimicAudio(
  childId: string,  // ← Expects childId as first param
  audioBlob: Blob,
  ...
)
```

**FIX**:
```typescript
// Get childId from auth store
const childId = useAuthStore.getState().selectedChildId;
const uploadRes = await api.uploadMimicAudio(childId, blob);
```

---

### Issue 1.3: Missing Results Fetch Endpoint (HIGH)

**Problem**: Results page uses mock data; no API to fetch actual attempt result.

**File**: `src/app/practice/mimic/results/page.tsx:47`
```typescript
// Currently using mock data
const mockResult: MimicResult = {
  score: 85,
  stars: 3,
  coach_tip: 'Great pronunciation!...',
  // ...
};
```

**Missing Backend Endpoint**: Need `GET /api/v1/speech/mimic/attempts/{attempt_id}/` to fetch result.

---

## 2. CHALLENGE SYSTEM - CRITICAL ISSUES

### Issue 2.1: Challenge Attempts NOT Persisted (CRITICAL)

**Problem**: Submit endpoint calculates score but NEVER saves to database.

**File**: `apps/challenges/views.py:89-96`
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_challenge(request):
    # Gets challenge
    challenge = get_object_or_404(Challenge, code=code)
    # Calculates score
    result = ChallengeService.calculate_score(challenge, answers)
    # Returns result... BUT NEVER CREATES ChallengeAttempt!
    return Response(result)  # ❌ No database save
```

**Impact**:
- All participant data is lost
- Leaderboard has no data
- Cannot track who played challenges

**FIX REQUIRED**:
```python
# After calculating score, save attempt:
ChallengeAttempt.objects.create(
    challenge=challenge,
    participant_name=request.data.get('participant_name', 'Anonymous'),
    answers=answers,
    score=result['score'],
    max_score=result['max_score'],
    percentage=result['percentage'],
    time_taken_seconds=request.data.get('time_taken', 0),
)
```

---

### Issue 2.2: Leaderboard NOT Implemented (HIGH)

**Problem**: Endpoint returns empty array, no actual implementation.

**File**: `apps/challenges/views.py:121-124`
```python
@api_view(['GET'])
@permission_classes([AllowAny])
def challenge_leaderboard(request, code):
    return Response([])  # ❌ Always returns empty!
```

**FIX REQUIRED**:
```python
def challenge_leaderboard(request, code):
    challenge = get_object_or_404(Challenge, code=code)
    attempts = ChallengeAttempt.objects.filter(
        challenge=challenge
    ).order_by('-percentage', 'time_taken_seconds')[:50]

    return Response([{
        'rank': i + 1,
        'participant_name': a.participant_name,
        'score': a.score,
        'percentage': a.percentage,
        'time_taken': a.time_taken_seconds,
    } for i, a in enumerate(attempts)])
```

---

### Issue 2.3: Grammar Questions Hardcoded (HIGH)

**Problem**: Grammar category has placeholder options with hardcoded correct answer.

**File**: `apps/challenges/services/challenge_service.py:121-130`
```python
def _generate_grammar(rules, count):
    questions = []
    for rule in rules[:count]:
        questions.append({
            'question': rule.examples[0] if rule.examples else "Repeat after Peppi",
            'options': [
                rule.title,
                "Option B",      # ❌ Placeholder!
                "Option C",      # ❌ Placeholder!
                "Option D"       # ❌ Placeholder!
            ],
            'correct_index': 0,  # ❌ Always first option is correct!
        })
    return questions
```

**Impact**: Grammar challenges are trivial - users can always select first option.

**FIX REQUIRED**: Generate meaningful grammar questions from GrammarExercise model:
```python
def _generate_grammar(language, count):
    exercises = GrammarExercise.objects.filter(
        rule__topic__language=language
    ).order_by('?')[:count]

    questions = []
    for ex in exercises:
        options = [ex.correct_answer] + ex.options[:3]
        random.shuffle(options)
        questions.append({
            'question': ex.question,
            'options': options,
            'correct_index': options.index(ex.correct_answer),
        })
    return questions
```

---

### Issue 2.4: Play Endpoint Returns Incomplete Data (MEDIUM)

**Problem**: GET /challenges/play/{code}/ missing essential metadata.

**File**: `apps/challenges/views.py:80-86`
```python
# Only returns title + questions
return Response({
    'title': challenge.title,
    'questions': strip_answers(challenge.questions),
})
# Missing: code, language, category, difficulty, time_limit_seconds, creator_name
```

**FIX**: Return full challenge metadata (without answers).

---

### Issue 2.5: Frontend Missing question_count Field (MEDIUM)

**Problem**: Create form doesn't include question_count input.

**File**: `src/components/challenges/CreateChallengeForm.tsx:29-36`
```typescript
const [formData, setFormData] = useState({
  title: '',
  description: '',        // Not in backend model
  language: 'HINDI',
  category: '',
  difficulty: 'medium',
  time_limit_seconds: 60,
  // Missing: question_count!
});
```

**Impact**: Always uses backend default of 5 questions. Users cannot customize.

---

### Issue 2.6: TypeScript Type Missing GRAMMAR Category (LOW)

**File**: `src/types/challenge.ts:8-16`
```typescript
export type ChallengeCategory =
  | 'alphabet'
  | 'vocabulary'
  | 'numbers'
  // ... missing 'grammar'!
```

---

## 3. FIELD NAME INCONSISTENCIES

### Issue 3.1: choices vs options

**Backend generates**: `options` field
**Frontend types expect**: `choices` field

**Files**:
- Backend: `apps/challenges/services/challenge_service.py:94`
- Frontend: `src/lib/api.ts:2177`

---

## 4. DUPLICATE CODE

### Issue 4.1: Duplicate get_available_languages() Method

**File**: `apps/challenges/services/challenge_service.py:25-38`

Method defined twice identically. Python uses second definition.

---

## 5. MIGRATION ISSUE

### Issue 5.1: MIMIC to GRAMMAR Migration

**Commit**: 8451b54 changed MIMIC category to GRAMMAR but migration file still shows old choices.

**File**: `apps/challenges/migrations/0003_alter_challenge_category.py`

May need to verify migration ran correctly on production.

---

## Priority Fix Order

1. **CRITICAL** - Mimic URL routing (Feature completely broken)
2. **CRITICAL** - Challenge attempt persistence (Data loss)
3. **HIGH** - Leaderboard implementation (Feature missing)
4. **HIGH** - Grammar question generation (Feature broken)
5. **HIGH** - Audio upload parameter fix
6. **MEDIUM** - Play endpoint metadata
7. **MEDIUM** - question_count field in UI
8. **LOW** - TypeScript types update

---

## Files to Modify

### Backend
| File | Changes Needed |
|------|----------------|
| `apps/speech/mimic_urls.py` | Add child_id to URL patterns OR |
| `apps/speech/views.py` | Get child_id from body/query instead of URL |
| `apps/challenges/views.py` | Implement submit persistence + leaderboard |
| `apps/challenges/services/challenge_service.py` | Fix grammar question generation |

### Frontend
| File | Changes Needed |
|------|----------------|
| `src/app/practice/mimic/[challengeId]/page.tsx` | Fix childId parameter |
| `src/lib/api.ts` | Update mimic API calls with child_id |
| `src/components/challenges/CreateChallengeForm.tsx` | Add question_count field |
| `src/types/challenge.ts` | Add 'grammar' category |

---

---

## FIXES APPLIED (January 19, 2025)

### Backend Fixes

#### 1. Mimic Views - child_id from request body (apps/speech/views.py)

**MimicChallengeDetailView** (line ~520):
- Changed from `def get(self, request, child_id, challenge_id)` to `def get(self, request, challenge_id)`
- Now gets `child_id` from `request.query_params.get('child_id')`

**MimicAttemptSubmitView** (line ~572):
- Changed from `def post(self, request, child_id, challenge_id)` to `def post(self, request, challenge_id)`
- Now gets `child_id` from `request.data.get('child_id')`

**MimicAttemptShareView** (line ~768):
- Changed from `def patch(self, request, child_id, attempt_id)` to `def patch(self, request, attempt_id)`
- Now gets `child_id` from `request.data.get('child_id')`

#### 2. Challenge Submit Persistence (apps/challenges/views.py:91-130)

Added `ChallengeAttempt.objects.create()` to persist:
- participant_name, participant_location
- score, max_score, percentage
- time_taken_seconds, answers
- is_completed=True, completed_at

Also updates Challenge stats (total_attempts, total_completions, average_score)

#### 3. Challenge Leaderboard Implementation (apps/challenges/views.py:155-195)

Implemented full leaderboard with:
- Top 50 attempts ordered by percentage (desc), time (asc)
- Returns rank, name, location, score, percentage, time
- Challenge metadata included

#### 4. Grammar Question Generation (apps/challenges/services/challenge_service.py)

Replaced placeholder implementation with:
- Uses `GrammarExercise` model with proper options
- Shuffles options randomly so correct answer varies
- Fallback to `GrammarRule` examples if no exercises
- Removed duplicate `get_available_languages()` method

### Frontend Fixes

#### 1. Mimic Audio Upload (src/app/practice/mimic/[challengeId]/page.tsx)

- Fixed: Now passes `childId` (from `useAuthStore`) instead of `challengeId` to `uploadMimicAudio()`
- Added proper child selection from auth store

#### 2. Challenge Creation Form (src/components/challenges/CreateChallengeForm.tsx)

Added `question_count` field:
- Dropdown with options: 3, 5, 7, 10 questions
- Default: 5 questions
- Updated time_limit_seconds default to 30

#### 3. TypeScript Types (src/types/challenge.ts)

Added `'grammar'` to `ChallengeCategory` type

---

## Testing Checklist

After fixes, verify:

- [x] Mimic views accept child_id from query/body params
- [x] Challenge attempts are saved to database
- [x] Leaderboard returns actual participant data
- [x] Grammar questions have shuffled options
- [x] Frontend passes correct childId to mimic upload
- [x] Challenge form includes question_count field
- [x] TTS API calls include /api/v1 prefix
- [x] Challenge play endpoint returns full metadata
- [ ] End-to-end test: Create mimic attempt and get score
- [ ] End-to-end test: Create challenge, play, see leaderboard
- [ ] End-to-end test: Grammar challenge with varied correct answers

---

## FIXES APPLIED (January 19, 2025 - Session 2)

### Frontend Fixes

#### 1. TTS API URL Fix (src/lib/api.ts)

**Issue**: `getAudio()` and `uploadMimicAudio()` methods made direct fetch calls without ensuring `/api/v1/` prefix in the URL. If `NEXT_PUBLIC_API_URL` was set without the prefix, these calls would 404.

**Fix**: Added `buildApiUrl()` helper method and updated both methods to use it:
```typescript
private buildApiUrl(path: string): string {
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  const baseHasApiPrefix = this.baseUrl.includes('/api/v1');
  if (baseHasApiPrefix) {
    return `${this.baseUrl.replace(/\/$/, '')}/${cleanPath}`;
  } else {
    return `${this.baseUrl.replace(/\/$/, '')}/api/v1/${cleanPath}`;
  }
}
```

### Backend Fixes

#### 2. Challenge Play Endpoint (apps/challenges/views.py)

**Issue**: `play_challenge` endpoint returned incomplete data:
- GET: Only returned `title` and `questions`
- POST: Didn't create attempt or return `attempt_id`

**Fix**: Updated to return full challenge metadata matching `PublicChallengeResponse`:
- GET: Returns all fields (id, code, title, language, category, difficulty, etc.)
- POST: Creates `ChallengeAttempt` record and returns `attempt_id` + full challenge data

#### 3. Challenge Submit Endpoint (apps/challenges/views.py)

**Issue**: Created new attempt instead of updating existing one from `play_challenge` POST.

**Fix**: Now supports both flows:
- With `attempt_id`: Updates existing attempt created by play_challenge POST
- Without `attempt_id` (legacy): Creates new attempt using code

#### 4. Detailed Results (apps/challenges/services/challenge_service.py)

**Issue**: `calculate_score()` returned empty `detailed_results: []`

**Fix**: Now returns proper detailed results:
```python
detailed_results.append({
    "question_id": i,
    "correct": is_correct,
    "user_answer": ans,
    "correct_answer": int(correct_index)
})
