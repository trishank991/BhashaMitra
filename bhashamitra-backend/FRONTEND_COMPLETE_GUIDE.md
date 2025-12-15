# Heritage Language Learning App - Complete Frontend Development Guide

> **For Claude Code Implementation**
> **Featuring: Peppi 🐱 - The AI Ragdoll Cat Tutor**

---

## Quick Reference

| Item | Value |
|------|-------|
| **Tech Stack** | Next.js 14, TypeScript, Tailwind CSS, Framer Motion, Zustand |
| **Target Users** | Indian diaspora children (4-14 years) |
| **Languages** | Hindi, Tamil, Gujarati, Punjabi |
| **Signature Feature** | Peppi - AI conversational tutor (Claude Haiku) |
| **Backend** | Django REST Framework + PostgreSQL |

---

## Part 1: Competitive Analysis & SWOT

### Global Language Apps

| App | Indian Languages | Child Focus | AI Tutor | Heritage Focus | Price |
|-----|------------------|-------------|----------|----------------|-------|
| **Duolingo** | Hindi, Bengali, Telugu (basic) | ⭐⭐⭐ | ❌ | ❌ | Free/$12.99 |
| **Babbel** | None | ⭐ | ❌ | ❌ | $12.95-$83/yr |
| **Rosetta Stone** | Hindi only | ❌ | ❌ | ❌ | $36-$199 |
| **Memrise** | Hindi (community) | ❌ | ❌ | ❌ | Free/$8.49/mo |
| **Busuu** | None | ❌ | ❌ | ❌ | $9.99/mo |

### Indian Language Apps

| App | Languages | Child Focus | AI Tutor | Issues |
|-----|-----------|-------------|----------|--------|
| **Language Curry** | 12 | ⭐ | ❌ | Expensive ($45-60/3mo), buggy, poor support |
| **Bhasha.io** | 3 | ❌ | ❌ | Expensive tutoring, no gamification |
| **Multibhashi** | 7 | ❌ | ❌ | Poor reviews, shallow learning |
| **Bhasha Sangam** | 22 | ❌ | ❌ | Basic phrases only, poor UX |

### Our SWOT

**Strengths:**
- Only app focused on heritage language preservation for diaspora children
- Peppi AI Tutor - unique conversational practice
- Story-based learning with 53,000+ free CC stories
- Duolingo-level gamification
- Family features (parent dashboard, grandparent recordings)

**Weaknesses:**
- New entrant, no brand recognition
- 4 languages initially (vs 12 for Language Curry)
- No live human tutors

**Opportunities:**
- 292,000+ Indians in NZ, 800,000+ in Australia
- Heritage language loss crisis (3rd generation)
- No competitor has AI tutor for Indian languages
- Free APIs (Bhashini, AI4Bharat, StoryWeaver)

**Threats:**
- Duolingo may expand Indian languages
- API dependencies may change
- Parent concerns about AI + children

### Competitive Matrix

| Feature | Duolingo | Language Curry | **Our App** |
|---------|----------|----------------|-------------|
| Gamification | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Child-Friendly | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| AI Tutor | ❌ | ❌ | ⭐⭐⭐⭐⭐ |
| Heritage Focus | ❌ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Story-Based | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Family Features | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ |

---

## Part 2: Design System

### Color Palette (Tailwind Config)

```javascript
// tailwind.config.ts
const config = {
  theme: {
    extend: {
      colors: {
        // Primary - Warm Orange
        primary: {
          50: '#FFF7ED', 100: '#FFEDD5', 200: '#FED7AA',
          300: '#FDBA74', 400: '#FB923C', 500: '#F97316',
          600: '#EA580C', 700: '#C2410C',
        },
        // Secondary - Teal
        secondary: {
          50: '#F0FDFA', 100: '#CCFBF1', 200: '#99F6E4',
          300: '#5EEAD4', 400: '#2DD4BF', 500: '#14B8A6',
          600: '#0D9488', 700: '#0F766E',
        },
        // Accent - Purple
        accent: {
          50: '#FAF5FF', 100: '#F3E8FF', 200: '#E9D5FF',
          300: '#D8B4FE', 400: '#C084FC', 500: '#A855F7',
          600: '#9333EA', 700: '#7E22CE',
        },
        // Warm Neutrals
        warm: {
          50: '#FFFBF7', 100: '#FFF5EB', 200: '#FFE8D6',
          300: '#D6CFC7', 400: '#A8A29E', 500: '#78716C',
          600: '#57534E', 700: '#44403C', 800: '#292524',
        },
        success: '#22C55E',
        warning: '#EAB308',
        error: '#EF4444',
      },
      fontFamily: {
        display: ['Baloo 2', 'cursive'],
        body: ['Nunito', 'sans-serif'],
        hindi: ['Noto Sans Devanagari'],
        tamil: ['Noto Sans Tamil'],
        gujarati: ['Noto Sans Gujarati'],
        punjabi: ['Noto Sans Gurmukhi'],
      },
    },
  },
};
```

### Peppi Color Reference (Seal Point Ragdoll)

```
BODY: #FDF5E6 (Warm cream)
POINTS: #5D4037 (Dark seal brown)
EYES: #1E88E5 (Vivid blue)
NOSE: #5D4037 (Seal brown)
COLLAR: #F97316 (Primary orange)
TAG: #14B8A6 (Teal)
```

---

## Part 3: Peppi AI Tutor

### Character Profile

| Attribute | Value |
|-----------|-------|
| Name | Peppi (पेप्पी) |
| Species | Seal Point Ragdoll Cat |
| Personality | Patient, encouraging, playful, gentle |
| Eyes | Signature blue (Ragdoll trait) |
| Catchphrase | "Meow-velous! Let's learn together!" |

### Expressions

| Expression | Trigger | Eyes | Animation |
|------------|---------|------|-----------|
| Happy | Default, correct answers | Wide, sparkly | Tail up |
| Thinking | Processing | Looking up | Paw on chin |
| Encouraging | After mistakes | Soft, warm | Head tilt |
| Excited | Achievements | Extra sparkly | Bouncing |
| Proud | Milestones | Half-closed | Chest puffed |
| Sleepy | Time reminders | Half-closed | Zzz effect |

### PeppiAvatar Component

```tsx
// src/components/peppi/PeppiAvatar.tsx
'use client';

import { motion } from 'framer-motion';

type Expression = 'happy' | 'thinking' | 'encouraging' | 'excited' | 'proud' | 'sleepy';

interface Props {
  expression?: Expression;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

const sizes = { xs: 32, sm: 48, md: 80, lg: 120, xl: 200 };

const eyeVariants = {
  happy: { scaleY: 1 },
  thinking: { scaleY: 1, y: -2 },
  encouraging: { scaleY: 0.9 },
  excited: { scaleY: 1.15 },
  proud: { scaleY: 0.4 },
  sleepy: { scaleY: 0.25 },
};

export function PeppiAvatar({ expression = 'happy', size = 'md' }: Props) {
  const dim = sizes[size];
  
  return (
    <motion.svg
      width={dim}
      height={dim}
      viewBox="0 0 200 200"
      initial={{ scale: 0.9 }}
      animate={{ scale: 1 }}
    >
      {/* Background */}
      <circle cx="100" cy="100" r="95" fill="#FDF5E6" />
      
      {/* Face */}
      <ellipse cx="100" cy="110" rx="70" ry="65" fill="#FDF5E6" />
      
      {/* Ears - Seal brown */}
      <path d="M45 60 Q30 20, 60 50 Q55 55, 50 60 Z" fill="#5D4037" />
      <path d="M155 60 Q170 20, 140 50 Q145 55, 150 60 Z" fill="#5D4037" />
      
      {/* Face mask */}
      <path
        d="M100 75 Q70 80, 55 100 Q50 115, 55 130 Q70 145, 100 150 
           Q130 145, 145 130 Q150 115, 145 100 Q130 80, 100 75"
        fill="#5D4037"
        opacity="0.3"
      />
      
      {/* Left Eye - Blue */}
      <motion.g animate={eyeVariants[expression]}>
        <ellipse cx="75" cy="105" rx="15" ry="18" fill="#FFF" />
        <ellipse cx="75" cy="105" rx="12" ry="15" fill="#1E88E5" />
        <ellipse cx="75" cy="105" rx="8" ry="10" fill="#1565C0" />
        <circle cx="72" cy="100" r="4" fill="#64B5F6" />
        <circle cx="78" cy="108" r="2" fill="#FFF" />
      </motion.g>
      
      {/* Right Eye - Blue */}
      <motion.g animate={eyeVariants[expression]}>
        <ellipse cx="125" cy="105" rx="15" ry="18" fill="#FFF" />
        <ellipse cx="125" cy="105" rx="12" ry="15" fill="#1E88E5" />
        <ellipse cx="125" cy="105" rx="8" ry="10" fill="#1565C0" />
        <circle cx="122" cy="100" r="4" fill="#64B5F6" />
        <circle cx="128" cy="108" r="2" fill="#FFF" />
      </motion.g>
      
      {/* Nose */}
      <ellipse cx="100" cy="125" rx="8" ry="6" fill="#5D4037" />
      
      {/* Mouth */}
      <path
        d={expression === 'excited' ? "M90 135 Q100 148, 110 135" : "M92 135 Q100 143, 108 135"}
        stroke="#5D4037"
        strokeWidth="2"
        fill="none"
      />
      
      {/* Whiskers */}
      <g stroke="#D6D3D1" strokeWidth="1.5">
        <line x1="55" y1="120" x2="28" y2="115" />
        <line x1="55" y1="125" x2="25" y2="125" />
        <line x1="55" y1="130" x2="28" y2="135" />
        <line x1="145" y1="120" x2="172" y2="115" />
        <line x1="145" y1="125" x2="175" y2="125" />
        <line x1="145" y1="130" x2="172" y2="135" />
      </g>
      
      {/* Collar - Orange */}
      <path
        d="M60 165 Q100 175, 140 165"
        stroke="#F97316"
        strokeWidth="8"
        fill="none"
      />
      
      {/* Tag - Teal */}
      <circle cx="100" cy="178" r="8" fill="#14B8A6" />
      <text x="100" y="182" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold">P</text>
      
      {/* Excited sparkles */}
      {expression === 'excited' && (
        <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <text x="40" y="65" fontSize="14">✨</text>
          <text x="150" y="65" fontSize="14">✨</text>
        </motion.g>
      )}
    </motion.svg>
  );
}
```

### Peppi Chat Hook

```typescript
// src/hooks/usePeppiChat.ts
import { useState, useCallback } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { peppiApi } from '@/lib/api/peppi';

interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
}

export function usePeppiChat({ childId, language }: { childId: string; language: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  
  const { data: quickReplies } = useQuery({
    queryKey: ['peppi-quick-replies', language],
    queryFn: () => peppiApi.getQuickReplies(language),
  });
  
  const mutation = useMutation({
    mutationFn: (content: string) => peppiApi.sendMessage({
      child_id: childId,
      message: content,
      session_id: sessionId,
    }),
    onSuccess: (data) => {
      if (data.session_id) setSessionId(data.session_id);
      setMessages(prev => [...prev, {
        id: data.message_id,
        role: 'assistant',
        content: data.response,
      }]);
    },
  });
  
  const sendMessage = useCallback(async (content: string) => {
    setMessages(prev => [...prev, { role: 'user', content }]);
    await mutation.mutateAsync(content);
  }, [mutation]);
  
  return {
    messages,
    isLoading: mutation.isPending,
    quickReplies: quickReplies?.quick_replies || [],
    sendMessage,
  };
}
```

### Backend Peppi Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/peppi/chat/` | Send message, get response |
| GET | `/api/v1/peppi/quick-replies/` | Get suggested replies |
| GET | `/api/v1/peppi/sessions/{id}/` | Get session history |
| DELETE | `/api/v1/peppi/sessions/{id}/` | End session |

### Cost Analysis

```
Claude Haiku Pricing:
- Input: $0.25 / million tokens
- Output: $1.25 / million tokens

Per message: ~$0.00046
50 families × 2 kids × 10 msg/day × 30 days = 30,000 messages
Monthly cost: ~$14

VERY AFFORDABLE ✅
```

---

## Part 4: Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Auth pages (no bottom nav)
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── onboarding/page.tsx
│   ├── (main)/                   # Main app (with bottom nav)
│   │   ├── home/page.tsx         # Dashboard
│   │   ├── stories/
│   │   │   ├── page.tsx          # Story list
│   │   │   └── [id]/page.tsx     # Story reader
│   │   ├── practice/page.tsx     # Games
│   │   ├── peppi/page.tsx        # AI Chat
│   │   ├── progress/page.tsx     # Stats
│   │   └── family/page.tsx
│   ├── layout.tsx
│   └── providers.tsx
│
├── components/
│   ├── ui/                       # Base components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Modal.tsx
│   ├── peppi/                    # Peppi components
│   │   ├── PeppiAvatar.tsx
│   │   ├── PeppiChat.tsx
│   │   └── PeppiQuickReplies.tsx
│   ├── gamification/
│   │   ├── StreakFlame.tsx
│   │   ├── XPCounter.tsx
│   │   ├── LevelBadge.tsx
│   │   └── LevelUpModal.tsx
│   └── stories/
│       ├── StoryCard.tsx
│       ├── StoryReader.tsx
│       └── AudioPlayer.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── usePeppiChat.ts
│   ├── useStreak.ts
│   └── useAudio.ts
│
├── stores/
│   ├── authStore.ts
│   └── childStore.ts
│
└── lib/
    ├── api/
    │   ├── client.ts
    │   ├── auth.ts
    │   ├── children.ts
    │   ├── stories.ts
    │   ├── progress.ts
    │   ├── peppi.ts
    │   └── speech.ts
    └── types/
        └── api.ts
```

---

## Part 5: Key Components

### Streak Flame

```tsx
// src/components/gamification/StreakFlame.tsx
import { motion } from 'framer-motion';

export function StreakFlame({ count, isActive = true }: { count: number; isActive?: boolean }) {
  const color = !isActive ? 'grayscale' : count >= 30 ? 'hue-rotate-15' : count >= 7 ? '' : 'hue-rotate-30';
  
  return (
    <div className="flex flex-col items-center">
      <motion.span
        className={`text-4xl ${color}`}
        animate={isActive ? { scale: [1, 1.1, 1], rotate: [-3, 3, -3] } : {}}
        transition={{ duration: 0.5, repeat: Infinity }}
      >
        🔥
      </motion.span>
      <span className="font-display font-bold">{count}</span>
      <span className="text-xs text-warm-500">{count === 1 ? 'day' : 'days'}</span>
    </div>
  );
}
```

### Level Up Modal

```tsx
// src/components/gamification/LevelUpModal.tsx
import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import { PeppiAvatar } from '../peppi/PeppiAvatar';

export function LevelUpModal({ isOpen, onClose, level, levelName }) {
  useEffect(() => {
    if (isOpen) {
      confetti({ particleCount: 100, spread: 70, colors: ['#F97316', '#14B8A6', '#A855F7'] });
      new Audio('/sounds/level-up.mp3').play().catch(() => {});
    }
  }, [isOpen]);
  
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-white rounded-3xl p-8 max-w-sm text-center"
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
          >
            <PeppiAvatar expression="excited" size="lg" />
            <h2 className="text-3xl font-display font-bold text-primary-500 mt-4">
              Level Up! 🎉
            </h2>
            <p className="text-warm-600 my-4">You've reached {levelName}!</p>
            <button
              onClick={onClose}
              className="w-full bg-primary-500 text-white py-3 rounded-2xl font-bold"
            >
              Keep Learning!
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

### Bottom Navigation

```tsx
// src/components/layout/BottomNav.tsx
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, BookOpen, Gamepad2, BarChart3, Users } from 'lucide-react';

const items = [
  { href: '/home', icon: Home, label: 'Home' },
  { href: '/stories', icon: BookOpen, label: 'Stories' },
  { href: '/practice', icon: Gamepad2, label: 'Play' },
  { href: '/progress', icon: BarChart3, label: 'Progress' },
  { href: '/family', icon: Users, label: 'Family' },
];

export function BottomNav() {
  const pathname = usePathname();
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t h-16">
      <div className="flex justify-around items-center h-full max-w-lg mx-auto">
        {items.map(({ href, icon: Icon, label }) => (
          <Link
            key={href}
            href={href}
            className={`flex flex-col items-center gap-1 px-3 py-2 ${
              pathname.startsWith(href) ? 'text-primary-500' : 'text-warm-400'
            }`}
          >
            <Icon size={24} />
            <span className="text-xs">{label}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
}
```

---

## Part 6: API Types

```typescript
// src/lib/types/api.ts

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'PARENT' | 'ADMIN';
}

export interface Child {
  id: string;
  name: string;
  avatar: string;
  dateOfBirth: string;
  language: 'HINDI' | 'TAMIL' | 'GUJARATI' | 'PUNJABI';
  level: number;
  totalPoints: number;
  streak?: { currentStreak: number; longestStreak: number; };
}

export interface Story {
  id: string;
  title: string;
  titleTranslit: string;
  language: string;
  level: number;
  pageCount: number;
  coverImageUrl: string;
  synopsis: string;
  categories: string[];
}

export interface StoryPage {
  pageNumber: number;
  textContent: string;
  imageUrl: string;
}

export interface Progress {
  id: string;
  storyId: string;
  status: 'IN_PROGRESS' | 'COMPLETED';
  currentPage: number;
  pointsEarned: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  earnedAt?: string;
}
```

---

## Part 7: Implementation Phases

### Phase 1: Foundation (Days 1-3)
- [x] Project setup (Next.js 14, TypeScript, Tailwind)
- [x] Tailwind config with custom colors
- [x] Auth store (Zustand)
- [x] API client setup
- [x] Layout components (BottomNav, Header)

### Phase 2: Core Features (Days 4-10)
- [ ] Home dashboard
- [ ] Story list page
- [ ] Story reader with audio
- [ ] Word popup vocabulary
- [ ] Basic gamification (XP, streak display)

### Phase 3: Peppi Chat (Days 11-14)
- [ ] PeppiAvatar SVG component
- [ ] PeppiChat interface
- [ ] usePeppiChat hook
- [ ] Quick replies
- [ ] TTS for Peppi's voice

### Phase 4: Games & Practice (Days 15-20)
- [ ] Quiz component
- [ ] Word match game
- [ ] Listening challenge
- [ ] Speaking practice

### Phase 5: Polish & Family (Days 21-28)
- [ ] Level up modal & celebrations
- [ ] Badge collection
- [ ] Progress statistics
- [ ] Parent dashboard
- [ ] Onboarding flow

### Phase 6: Testing & Launch (Days 29-30)
- [ ] E2E testing
- [ ] Performance optimization
- [ ] PWA setup
- [ ] Deployment

---

## Part 8: Backend API Reference

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register/` | POST | Register parent |
| `/api/v1/auth/login/` | POST | Login |
| `/api/v1/auth/logout/` | POST | Logout |
| `/api/v1/auth/me/` | GET | Current user |

### Children
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/children/` | GET | List children |
| `/api/v1/children/` | POST | Create child |
| `/api/v1/children/{id}/` | GET | Get child |
| `/api/v1/children/{id}/` | PATCH | Update child |
| `/api/v1/children/{id}/streak/` | GET | Get streak |
| `/api/v1/children/{id}/badges/` | GET | Get badges |
| `/api/v1/children/{id}/stats/` | GET | Get stats |

### Stories
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/stories/` | GET | List stories (with filters) |
| `/api/v1/stories/{id}/` | GET | Get story with pages |

### Progress
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/children/{id}/progress/` | GET | List progress |
| `/api/v1/children/{id}/progress/` | POST | Start/update/complete story |

### Peppi Chat
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/peppi/chat/` | POST | Send message |
| `/api/v1/peppi/quick-replies/` | GET | Get quick replies |
| `/api/v1/peppi/sessions/{id}/` | GET | Get session |
| `/api/v1/peppi/sessions/{id}/` | DELETE | End session |

### Speech
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/speech/tts/` | POST | Text to speech |
| `/api/v1/speech/stt/` | POST | Speech to text |

---

## Summary

This guide provides everything needed to build a production-ready children's heritage language learning app with:

✅ **Competitive Edge**: Only heritage-focused app with AI tutor
✅ **Peppi**: Friendly Ragdoll cat AI companion (Claude Haiku)
✅ **Child-First**: Bright colors, large buttons, celebrations
✅ **Gamification**: Streaks, XP, badges, levels
✅ **Modern Stack**: Next.js 14 + TypeScript + Tailwind
✅ **Complete Backend**: Django REST Framework ready

**Peppi makes this app unique** - no competitor has an AI conversational tutor for Indian heritage languages!
