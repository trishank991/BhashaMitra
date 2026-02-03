# BhashaMitra Test Credentials

**Last Updated:** January 6, 2026  
**Purpose:** MVP Launch Testing

---

## 🔐 Test Login Credentials

### All Environments (Localhost & Production)

| Tier | Email | Password | Features |
|------|-------|----------|----------|
| **FREE** | `free@test.com` | `test1234` | Cache-only TTS, 4 stories, no games |
| **STANDARD** | `standard@test.com` | `test1234` | Svara TTS, 8 stories, games access |
| **PREMIUM** | `premium@test.com` | `test1234` | Sarvam AI TTS, unlimited, all features |

---

## 🌐 Environment URLs

### Local Development

| Service | URL | Port |
|---------|-----|------|
| **Frontend (Next.js)** | http://localhost:3000 | 3000 |
| **Backend (Django)** | http://localhost:8000 | 8000 |
| **Admin Panel** | http://localhost:8000/admin | 8000 |

### Production (Live Website)

| Service | URL |
|---------|-----|
| **Frontend** | https://bhashamitra.co.nz |
| **Backend API** | https://bhashamitra.onrender.com |
| **Admin** | https://bhashamitra.onrender.com/admin |

---

## 👶 Test Children (Auto-Created)

| Parent Account | Child Name | Avatar | Language |
|----------------|------------|--------|----------|
| free@test.com | Aarav | 🐼 | Hindi |
| standard@test.com | Priya | 🦊 | Hindi |
| premium@test.com | Arjun | 🦁 | Hindi |

---

## 🔧 Developer Setup Commands

### Backend (Django)

```bash
cd bhashamitra-backend

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run migrations
python manage.py migrate

# Seed test data
python manage.py seed_test_users
python manage.py seed_mimic_challenges

# Start development server
python manage.py runserver
```

### Frontend (Next.js)

```bash
cd bhashamitra-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🧪 Key Features to Test

### 1. Mimic Feature (Pronunciation Practice)
- **URL:** `/practice/mimic`
- **Test:** Login as any user, select child, practice Hindi words
- **Data:** 33 challenges across 7 categories (Greetings, Family, Numbers, Colors, Animals, Food, Festivals)

### 2. Challenge Friends (Family Competition)
- **URL:** `/challenges` (Viral Quiz)
- **URL:** Family dashboard via parent panel
- **Test:** Create challenge, share code, invite family members

### 3. Subscription Tiers
- **URL:** `/pricing`
- **Test:** Verify features match tier (free vs paid differences)

---

## 👥 Team Assignments for MVP Launch

| Role | Responsibility |
|------|----------------|
| **Frontend Developer** | Test UI flows, fix visual bugs, verify API integration |
| **Backend Developer** | Monitor API logs, fix server errors, verify data integrity |
| **CTO** | Code review, approve deployments, supervise launch |

---

## ✅ Pre-Launch Checklist

- [x] Test users seeded (3 accounts)
- [x] Mimic challenges seeded (33 Hindi words)
- [x] Family feature API implemented
- [x] Challenge creation working
- [ ] End-to-end flow tested
- [ ] Production deployment verified
- [ ] Error monitoring enabled (Sentry)

---

**Note:** For production live website, test accounts may need to be created via the registration flow or seeded to the production database.
