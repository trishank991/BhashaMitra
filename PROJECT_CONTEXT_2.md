# BhashaMitra - Project Context (Part 2)

> Continuation of PROJECT_CONTEXT.md - for updates after Dec 27, 2024

---

## Session Log: Dec 27, 2024

### Completed Tasks

1. **Favicon 500 Error Fixed**
   - Deleted duplicate `/src/app/favicon.ico`
   - Kept `/public/favicon.ico` (correct location for Next.js)

2. **Lint Errors Cleaned Up**
   - Fixed ~50 unused import warnings across frontend
   - Files cleaned: games, learn, onboarding, practice, components

3. **Registration Error Messages Improved**
   - Updated `authStore.ts` to return specific error messages
   - Updated `register/page.tsx` to display backend errors

4. **Offline Mode Data Analysis Completed**
   - Analyzed all seeded content by language
   - Calculated storage requirements per language
   - Created projections for adding new languages

5. **Roadmap Created**
   - `ROADMAP_REMAINING_FEATURES.md` with detailed implementation steps
   - Covers: Favicon, Unused imports, Google OAuth, Apple Sign-In, Offline PWA

---

## Pending Discussions

### 1. Social Login (Google/Apple OAuth)

**Decision Points:**
- [ ] Google Cloud Console project setup - who creates?
- [ ] OAuth redirect URIs for dev/staging/prod
- [ ] Apple Developer account purchase ($99/year)
- [ ] Timeline for iOS App Store submission (Apple Sign-In mandatory)

**Technical Notes:**
- Use `django-allauth` for backend OAuth handling
- Frontend needs `/auth/callback/page.tsx` for redirect handling
- Consider account linking if user has existing email+password account

### 2. Offline Mode (PWA)

**Decision Points:**
- [ ] FREE tier only (~25 MB/lang) vs Full content (~51 MB/lang)?
- [ ] Cache TTS audio on-demand or pre-download all?
- [ ] Which languages to prioritize for offline?
- [ ] Storage limit warnings - at what threshold?
- [ ] Should songs be included? (adds ~20 MB/lang)

**Current Data Summary:**
```
Language     Letters  Vocab  Stories  Current  With Audio
---------------------------------------------------------
Hindi           49     110       42    ~15 MB     ~59 MB
Tamil           37      70       21     ~3 MB     ~22 MB
Gujarati        48       0        7    ~4.4 MB     ~8 MB
Punjabi         45      70       18    ~4.2 MB    ~24 MB
Fiji Hindi      46     107       15     ~0 MB     ~21 MB
---------------------------------------------------------
TOTAL (5)      225     357      103    ~28 MB    ~134 MB
```

**If adding 4 more languages (Telugu, Marathi, Bengali, Kannada):**
- Estimated additional: ~204 MB
- Total with all 9 languages: ~338 MB (with audio)
- FREE tier only: ~180-225 MB (more manageable)

---

## Files Created This Session

| File | Purpose |
|------|---------|
| `ROADMAP_REMAINING_FEATURES.md` | Detailed implementation roadmap |
| `PROJECT_CONTEXT_2.md` | This file - continuation of project context |

---

## Next Actions (When Ready)

### If Social Login Approved:
1. Create Google Cloud Console project
2. Install `django-allauth`
3. Configure OAuth credentials
4. Create frontend social buttons
5. Test OAuth flow end-to-end

### If Offline Mode Approved:
1. Register Service Worker in layout.tsx
2. Create backend OfflinePackage model
3. Create manifest generation endpoints
4. Implement IndexedDB caching in frontend
5. Add download manager UI

---

## Reference Links

- Main context: `PROJECT_CONTEXT.md`
- Feature roadmap: `ROADMAP_REMAINING_FEATURES.md`
- Frontend: `bhashamitra-frontend/`
- Backend: `bhashamitra-backend/`

---

*Last updated: Dec 27, 2024*
