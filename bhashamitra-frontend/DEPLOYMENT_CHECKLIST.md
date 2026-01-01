# BhashaMitra Vercel Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Variables
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL
- [ ] `NEXT_PUBLIC_GOOGLE_CLIENT_ID` - Google OAuth Client ID
- [ ] `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (if using payments)

### 2. Icon Assets
Icons must be valid PNG files with RGB color mode (NOT indexed/colormap).

**To verify icons:**
```bash
file public/icon-192.png
# Should show: PNG image data, 192 x 192, 8-bit RGB, non-interlaced
# NOT: PNG image data, 192 x 192, 8-bit colormap, non-interlaced
```

**To regenerate icons (if needed):**
```bash
# Using Python with Pillow (recommended)
python3 scripts/generate-icons.py

# Or using Node.js
node scripts/generate-icons.js
```

### 3. Audio Assets
All audio files must have the correct extension matching their format.

**To verify audio files:**
```bash
file public/audio/sounds/*.wav
# All should show: WAVE audio, Microsoft PCM, 16 bit, stereo 44100 Hz

# If files show wrong extension, rename them:
for f in public/audio/sounds/*.mp3; do mv "$f" "${f%.mp3}.wav"; done
```

**Then update `src/lib/soundService.ts` to use `.wav` extension.**

### 4. Google OAuth Provider
Ensure `GoogleOAuthProvider` wraps the app in `src/components/layout/ClientProviders.tsx`:

```tsx
// Correct: Always wrap with provider (even if no client ID)
<GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID || 'placeholder'}>
  <AgeThemeProvider>{children}</AgeThemeProvider>
</GoogleOAuthProvider>
```

### 5. Meta Tags
The following meta tags are configured in `src/app/layout.tsx`:
- `mobile-web-app-capable: yes` - For PWA support
- `apple-mobile-web-app-capable` - For iOS PWA (deprecated but included for backward compatibility)

## Deployment Steps

### Local Build Test
```bash
cd bhashamitra-frontend
npm run build
```

### Vercel Deployment
1. Push changes to GitHub
2. Vercel will auto-deploy from main branch
3. Verify deployment at https://bhasha-mitra.vercel.app

### Post-Deployment Verification
- [ ] Login page loads without errors
- [ ] Google Sign-In works
- [ ] Sound effects play (click, correct, wrong, etc.)
- [ ] PWA install prompt appears on mobile
- [ ] App icon appears correctly on home screen

## Common Issues & Fixes

### Issue: "Google OAuth components must be used within GoogleOAuthProvider"
**Fix:** Ensure `ClientProviders` component wraps the app and includes `GoogleOAuthProvider`.

### Issue: "NotSupportedError: Failed to load because no supported source was found"
**Fix:** Audio files have wrong format/extension. Rename `.mp3` to `.wav` if they are actually WAV files.

### Issue: Icon not loading on mobile
**Fix:** Regenerate icons as RGB PNG (not colormap/indexed color).

## Automated Icon Generation

See `scripts/generate-icons.py` or `scripts/generate-icons.js` for automated icon generation.
