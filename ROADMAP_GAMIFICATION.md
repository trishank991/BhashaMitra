# BhashaMitra - Peppi Gamification Roadmap

> **Decision Date:** December 27, 2024
> **Status:** DEFERRED TO POST-MVP
> **Rationale:** Ship core product first, gather family feedback to guide gamification priorities

---

## Executive Summary

The Peppi Gamification System has been designed and partially implemented at the database layer. However, a strategic decision was made to **defer full implementation until post-MVP launch** to:

1. **Ship faster** - Focus on core learning experience
2. **Get real feedback** - Let families tell us what gamification they want
3. **Reduce risk** - Avoid over-engineering features that may not resonate

---

## What's Built (Database Ready)

The following models exist in the database and are ready for future activation:

### Models Created (Migration Applied)

| Model | Purpose | Records Seeded |
|-------|---------|----------------|
| `PeppiOutfit` | Culturally-authentic outfits | 29 outfits |
| `PeppiOutfitTranslation` | Multi-language outfit names | Per-outfit translations |
| `PeppiAccessory` | Accessories for slots | 10 accessories |
| `ChildPeppiState` | Evolution, happiness, coins | Per-child state |
| `ChildUnlockedOutfit` | Track outfit unlocks | - |
| `ChildUnlockedAccessory` | Track accessory unlocks | - |
| `ChildEquippedAccessories` | Current equipped items | - |
| `DailyChallengeTemplate` | Challenge definitions | 12 templates |
| `ChildDailyChallenge` | Per-child daily challenges | - |

### Outfit Categories by Language

| Language | Outfits | Examples |
|----------|---------|----------|
| Hindi | 4 | Kurta Pajama, Diwali, Holi, Wedding |
| Tamil | 4 | Veshti, Pongal, Bharatanatyam, Temple |
| Gujarati | 4 | Kediya, Navratri, Garba, Bandhani |
| Punjabi | 4 | Kurta Patiala, Baisakhi, Bhangra, Phulkari |
| Telugu | 3 | Pancha, Sankranti, Kuchipudi |
| Malayalam | 3 | Mundu, Onam, Kathakali |
| Fiji Hindi | 3 | Fiji Kurta, Festival, Meke Dance |
| Universal | 4 | Classic, Golden, Streak Master, Rainbow |

### Accessory Slots

- Head (party hat, flower crown, reading glasses)
- Neck (bell collar, friendship band)
- Paws (paw warmers, anklets)
- Tail (ribbon bow, starry trail)
- Background (sparkles)

### Daily Challenge Types

| Type | Easy | Medium | Hard |
|------|------|--------|------|
| Story Read | Read 1 story | Read 3 stories | Read 5 stories |
| Vocabulary | Learn 5 words | Learn 10 words | Learn 20 words |
| Voice Recording | Record 2x | Record 5x | Record 10x |
| Game Play | Win 1 game | Win 3 games | Win 5 games |

---

## What's NOT Built (Deferred)

### Backend Services (0% Complete)

| Service | Purpose | Priority Post-MVP |
|---------|---------|-------------------|
| `PeppiStateService` | Evolution, happiness decay, coins | P1 |
| `OutfitService` | Unlock logic, equip/unequip | P1 |
| `AccessoryService` | Same for accessories | P2 |
| `DailyChallengeService` | Assign/track daily challenges | P1 |
| `UnlockTriggerService` | Auto-unlock on milestones | P2 |

### API Endpoints (0% Complete)

| Endpoint | Methods | Purpose |
|----------|---------|---------|
| `/gamification/peppi/state/` | GET, PATCH | Get/update Peppi state |
| `/gamification/peppi/outfits/` | GET | List outfits with unlock status |
| `/gamification/peppi/outfits/<id>/equip/` | POST | Equip an outfit |
| `/gamification/peppi/accessories/` | GET | List accessories |
| `/gamification/daily-challenges/` | GET | Today's challenges |
| `/gamification/daily-challenges/<id>/claim/` | POST | Claim reward |

### Frontend Components (0% Complete)

| Component | Purpose |
|-----------|---------|
| `PeppiCustomization.tsx` | Full outfit/accessory selector |
| `OutfitCarousel.tsx` | Browse unlocked outfits |
| `DailyChallenges.tsx` | Show today's challenges |
| `UnlockCelebration.tsx` | Confetti animation on unlock |
| `CoinDisplay.tsx` | Animated coin counter |

### Frontend Stores (0% Complete)

| Store | Purpose |
|-------|---------|
| `usePeppiStore.ts` | Peppi state, coins, equipped items |
| `useDailyChallengesStore.ts` | Today's challenges, progress |

---

## MVP Peppi Implementation (Currently Active)

The current Peppi works without gamification:

```
┌─────────────────────────────────────┐
│  MVP Peppi (Active)                 │
├─────────────────────────────────────┤
│  ✅ PeppiCharacter.tsx              │  Basic animated cat
│  ✅ PeppiSpeech.tsx                 │  Speech bubbles
│  ✅ PeppiFeedbackBubble.tsx         │  Correct/wrong feedback
│  ✅ PeppiChatPanel.tsx              │  AI chat (PREMIUM)
│  ✅ PeppiPreferenceSelector.tsx     │  Bhaiya/Didi selection
│  ✅ PeppiNarrator.tsx               │  Story narration
└─────────────────────────────────────┘
```

---

## Post-MVP Implementation Plan

### Phase 1: Core Gamification (After Family Feedback)

**Trigger:** Families request more engagement features

1. Implement `PeppiStateService` (coins, happiness)
2. Add outfit equip/unequip API
3. Create basic `PeppiCustomization.tsx` component
4. Add 3 starter outfits unlocked by default

**Estimated Effort:** 2-3 days

### Phase 2: Daily Challenges

**Trigger:** Families want daily engagement hooks

1. Implement `DailyChallengeService`
2. Add challenge assignment logic (3 challenges/day)
3. Create `DailyChallenges.tsx` component
4. Integrate with existing progress tracking

**Estimated Effort:** 2-3 days

### Phase 3: Unlock System

**Trigger:** Families respond well to achievement systems

1. Implement unlock triggers (streak → outfit)
2. Add `UnlockCelebration.tsx` with confetti
3. Create unlock notification system
4. Connect to existing badge/streak systems

**Estimated Effort:** 3-4 days

### Phase 4: Evolution & Advanced

**Trigger:** High engagement, families want depth

1. Implement Peppi evolution (kitten → wise cat)
2. Add happiness decay (Celery scheduled task)
3. Create feeding/petting mini-interactions
4. Add accessory system

**Estimated Effort:** 4-5 days

---

## Metrics to Track (Post-MVP)

Before implementing each phase, we'll measure:

| Metric | Purpose |
|--------|---------|
| DAU/MAU | Daily vs monthly active users |
| Session length | Time spent in app |
| Retention D1/D7/D30 | Return rate |
| Feature requests | What families ask for |
| Streak completion | % maintaining streaks |

---

## Database Schema Reference

### PeppiOutfit Model

```python
class PeppiOutfit(TimeStampedModel):
    code = CharField(unique=True)        # "hindi_kurta"
    name_english = CharField()           # "Kurta Pajama"
    category = CharField()               # traditional/festive/dance/silly
    rarity = CharField()                 # common/uncommon/rare/epic/legendary
    primary_language = CharField(null=True)  # HINDI, TAMIL, etc.
    unlock_type = CharField()            # default/streak_days/level/festival
    unlock_value = IntegerField()        # e.g., 7 for 7-day streak
    unlock_festival = CharField(blank=True)  # "diwali" for festival unlocks
    image_url = URLField()
    is_active = BooleanField()
```

### ChildPeppiState Model

```python
class ChildPeppiState(TimeStampedModel):
    child = OneToOneField(Child)
    happiness = IntegerField(0-100)
    hunger = IntegerField(0-100)
    evolution_stage = CharField()        # kitten/young_cat/adult_cat/wise_cat
    coins = IntegerField(default=100)
    gems = IntegerField(default=0)
    current_outfit = ForeignKey(PeppiOutfit, null=True)
    total_pets = IntegerField()
    last_fed_at = DateTimeField(null=True)
```

---

## Notes

- All gamification models use UUIDs as primary keys
- Translations support all 7 languages
- Seed data is already in database (just not exposed via API)
- Existing gamification (badges, streaks, levels) continues to work
- No breaking changes to current Peppi implementation

---

## Appendix: Seed Command

To re-seed gamification data:

```bash
cd bhashamitra-backend
source venv/bin/activate
python manage.py seed_peppi_outfits
```

Output:
```
Created 29 outfits
Created 10 accessories
Created 12 daily challenge templates
Successfully seeded Peppi gamification data
```

---

*Last Updated: December 27, 2024*
