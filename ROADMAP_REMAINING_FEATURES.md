# BhashaMitra - Remaining Features Roadmap

> Last Updated: Dec 27, 2024

---

## 1. FAVICON FIX (Quick Win)

**Effort:** Minimal | **Priority:** Low | **Risk:** None

### Problem
- 500 error on `/favicon.ico` requests
- Duplicate favicon files exist in both `/public/` and `/src/app/`

### Steps
1. Remove duplicate: Delete `/src/app/favicon.ico` (keep `/public/favicon.ico`)
2. Verify Next.js serves from `/public/` correctly
3. Clear browser cache and test

### Files to Modify
- DELETE: `src/app/favicon.ico`

---

## 2. UNUSED IMPORT WARNINGS CLEANUP (Quick Win)

**Effort:** Minimal | **Priority:** Low | **Risk:** None

### Problem
- ~30 unused import warnings across components
- Don't affect build but clutter lint output

### Steps
1. Run `npm run lint` to get full list
2. Remove unused imports from each file
3. Verify build still passes

### Files to Modify (partial list)
- `src/components/festivals/FestivalBanner.tsx`
- `src/components/festivals/FestivalList.tsx`
- `src/components/home/FreeHomepage.tsx`
- `src/components/home/PaidHomepage.tsx`
- `src/components/mimic/RecordingInterface.tsx`
- `src/components/peppi/PeppiNarrator.tsx`
- `src/components/peppi/PeppiSongNarrator.tsx`
- `src/lib/api.ts`
- And ~10 more files

---

## 3. SOCIAL LOGIN (Google/Apple OAuth)

**Effort:** Significant | **Priority:** P0 | **Risk:** Medium (third-party dependencies)

### Problem
- Parents expect quick social sign-in options
- Required for iOS App Store (Apple Sign-In mandate)

### Architecture Decision
- **Backend:** django-allauth (handles OAuth flow, token exchange)
- **Frontend:** Social buttons + redirect handling

---

### Phase 3A: Backend - Google OAuth

#### Steps
1. Install django-allauth
   ```bash
   pip install django-allauth
   ```

2. Configure Django settings
   - Add allauth apps to INSTALLED_APPS
   - Configure authentication backends
   - Set up Google OAuth credentials

3. Create Google Cloud Console project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Configure redirect URIs

4. Add API endpoints
   - `POST /api/v1/auth/google/` - Initiate Google OAuth
   - `GET /api/v1/auth/google/callback/` - Handle callback

#### Files to Modify
- `bhashamitra-backend/config/settings.py`
- `bhashamitra-backend/config/urls.py`
- `bhashamitra-backend/apps/users/views.py`
- `bhashamitra-backend/requirements/base.txt`

---

### Phase 3B: Backend - Apple Sign-In

#### Steps
1. Configure Apple Developer account
   - Create App ID with Sign In with Apple capability
   - Create Services ID
   - Generate private key

2. Add Apple provider to django-allauth
   - Configure Apple credentials
   - Handle Apple's unique JWT token format

3. Add API endpoints
   - `POST /api/v1/auth/apple/` - Initiate Apple OAuth
   - `GET /api/v1/auth/apple/callback/` - Handle callback

#### Files to Modify
- `bhashamitra-backend/config/settings.py`
- `bhashamitra-backend/apps/users/views.py`

---

### Phase 3C: Frontend - Social Login UI

#### Steps
1. Create social login buttons component
   ```tsx
   // src/components/auth/SocialLoginButtons.tsx
   - Google Sign-In button (branded per guidelines)
   - Apple Sign-In button (branded per guidelines)
   ```

2. Update login page
   - Add social buttons with divider ("or")
   - Handle OAuth redirect flow

3. Update register page
   - Add social buttons
   - Handle account linking

4. Create OAuth callback handler
   ```tsx
   // src/app/auth/callback/page.tsx
   - Parse OAuth response
   - Exchange code for tokens
   - Redirect to home/onboarding
   ```

#### Files to Create/Modify
- NEW: `src/components/auth/SocialLoginButtons.tsx`
- NEW: `src/app/auth/callback/page.tsx`
- MODIFY: `src/app/login/page.tsx`
- MODIFY: `src/app/register/page.tsx`
- MODIFY: `src/lib/api.ts` (add OAuth endpoints)

---

## 4. OFFLINE MODE (PWA)

**Effort:** Significant | **Priority:** Post-MVP | **Risk:** Medium (complex caching logic)

### Problem
- App doesn't work without internet
- Parents in areas with poor connectivity can't use the app
- No content available for offline learning

### Architecture
```
┌─────────────────┐     ┌──────────────────┐
│   Frontend      │     │    Backend       │
│                 │     │                  │
│ ┌─────────────┐ │     │ ┌──────────────┐ │
│ │ Service     │ │     │ │ Offline      │ │
│ │ Worker      │◄──────►│ Packages API │ │
│ └─────────────┘ │     │ └──────────────┘ │
│        │        │     │                  │
│        ▼        │     │                  │
│ ┌─────────────┐ │     │                  │
│ │ IndexedDB   │ │     │                  │
│ │ Cache       │ │     │                  │
│ └─────────────┘ │     │                  │
└─────────────────┘     └──────────────────┘
```

---

### Phase 4A: Service Worker Registration

#### Steps
1. Register service worker in app layout
   ```tsx
   // src/app/layout.tsx - add SW registration
   useEffect(() => {
     if ('serviceWorker' in navigator) {
       navigator.serviceWorker.register('/sw.js');
     }
   }, []);
   ```

2. Test basic caching of static assets

#### Files to Modify
- `src/app/layout.tsx` or create `src/components/layout/ServiceWorkerRegistration.tsx`

---

### Phase 4B: Backend - Offline Packages API

#### Steps
1. Create OfflinePackage model
   ```python
   class OfflinePackage(models.Model):
       name = models.CharField(max_length=100)
       language = models.CharField(max_length=20)
       package_type = models.CharField()  # FREE_TIER, L1, L2, etc.
       version = models.CharField()
       size_mb = models.IntegerField()
       content_manifest = models.JSONField()  # List of files to cache
   ```

2. Create API endpoints
   - `GET /api/v1/offline/packages/` - List available packages
   - `GET /api/v1/offline/packages/{id}/manifest/` - Get file manifest
   - `POST /api/v1/offline/sync/` - Sync offline progress

3. Create content packaging script
   - Bundle stories, audio, images per package
   - Generate manifests with versioning

#### Files to Create
- NEW: `bhashamitra-backend/apps/offline/models.py`
- NEW: `bhashamitra-backend/apps/offline/views.py`
- NEW: `bhashamitra-backend/apps/offline/serializers.py`
- NEW: `bhashamitra-backend/apps/offline/urls.py`

---

### Phase 4C: Frontend - Download Manager UI

#### Steps
1. Create offline settings page
   ```tsx
   // src/app/settings/offline/page.tsx
   - Show available packages
   - Download progress indicators
   - Storage usage display
   - Delete downloaded content
   ```

2. Create download manager component
   ```tsx
   // src/components/offline/DownloadManager.tsx
   - Package cards with download buttons
   - Progress bars
   - Cancel/pause functionality
   ```

3. Create offline indicator component
   ```tsx
   // src/components/offline/OfflineIndicator.tsx
   - Show when offline
   - Show sync status
   ```

4. Connect offlineStore to real API
   - Replace mock data with actual API calls
   - Implement actual file caching via service worker

#### Files to Create/Modify
- NEW: `src/app/settings/offline/page.tsx`
- NEW: `src/components/offline/DownloadManager.tsx`
- NEW: `src/components/offline/OfflineIndicator.tsx`
- MODIFY: `src/stores/offlineStore.ts` (replace mocks)
- MODIFY: `public/sw.js` (enhance caching)
- MODIFY: `src/lib/api.ts` (add offline endpoints)

---

### Phase 4D: Offline Content Playback

#### Steps
1. Update story reader to check offline cache first
2. Update audio player to use cached audio
3. Handle graceful degradation when content not cached
4. Add "Available Offline" badges to content

#### Files to Modify
- `src/app/stories/[id]/page.tsx`
- `src/components/peppi/PeppiNarrator.tsx`
- Various content display components

---

## Summary: Effort Levels

| Feature | Effort | Steps | Dependencies |
|---------|--------|-------|--------------|
| Favicon Fix | 1 step | 1 | None |
| Unused Imports | 1 step | ~15 files | None |
| Google OAuth | 3 phases | ~10 files | Google Cloud Console |
| Apple Sign-In | 2 phases | ~5 files | Apple Developer Account ($99/yr) |
| Offline Mode | 4 phases | ~20 files | Content packaging strategy |

---

## Recommended Execution Order

### Immediate (Quick Wins)
1. ✅ Favicon fix
2. ✅ Unused imports cleanup

### Short-term (P0)
3. Google OAuth (most common social login)

### Medium-term (P0 for iOS)
4. Apple Sign-In (required before iOS App Store submission)

### Post-MVP
5. Offline Mode (complex, can defer)

---

## Notes

- Social login requires real OAuth credentials (can't fully test locally without them)
- Apple Sign-In requires paid Apple Developer account ($99/year)
- Offline mode storage estimate: ~50MB per language pack for FREE tier
- Consider using `next-pwa` package for easier PWA setup with Next.js
