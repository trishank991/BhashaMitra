# VisualFlashcard Integration Guide

This guide shows how to integrate the VisualFlashcard component into existing pages.

## Quick Integration into Vocabulary Page

### Current Implementation (page.tsx)

The vocabulary detail page currently has a simple flashcard implementation. Here's how to replace it with VisualFlashcard:

### Step 1: Import the Component

```tsx
// At the top of /app/learn/vocabulary/[id]/page.tsx
import { VisualFlashcard } from '@/components/curriculum';
```

### Step 2: Replace the Flashcard Section

Find the flashcard mode section (around line 313-378) and replace with:

```tsx
{mode === 'flashcard' && (
  <motion.div variants={fadeInUp} className="space-y-6">
    {/* Progress */}
    <div className="text-center">
      <p className="text-sm text-gray-500">
        Card {currentWordIndex + 1} of {words.length}
      </p>
      <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
        <div
          className="bg-primary-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${((currentWordIndex + 1) / words.length) * 100}%` }}
        />
      </div>
    </div>

    {/* VisualFlashcard Component */}
    <AnimatePresence mode="wait">
      <motion.div
        key={currentWordIndex}
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -50 }}
        transition={{ duration: 0.2 }}
      >
        <VisualFlashcard
          word={currentWord.word}
          romanization={currentWord.romanization}
          translation={currentWord.translation}
          imageUrl={currentWord.image_url}
          audioUrl={currentWord.pronunciation_audio_url}
          gender={currentWord.gender}
          partOfSpeech={currentWord.part_of_speech}
          exampleSentence={currentWord.example_sentence}
          category={themeName} // Use theme name as category
          isFlipped={showMeaning}
          onFlip={() => {
            onPageTurn(); // Play sound
            setShowMeaning(!showMeaning);
          }}
          onAudioPlay={handlePlayWord}
        />
      </motion.div>
    </AnimatePresence>

    {/* Navigation buttons remain the same */}
    <div className="flex gap-3">
      <Button
        variant="outline"
        onClick={handlePrevWord}
        disabled={currentWordIndex === 0}
        className="flex-1"
      >
        Previous
      </Button>
      <Button
        onClick={handleNextWord}
        disabled={currentWordIndex === words.length - 1}
        className="flex-1"
      >
        Next
      </Button>
    </div>

    {/* Completion card remains the same */}
  </motion.div>
)}
```

## Complete Standalone Page Example

Create a new page specifically for visual flashcard practice:

### File: `/app/learn/flashcards/page.tsx`

```tsx
'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { VisualFlashcard } from '@/components/curriculum';
import { Button, Loading } from '@/components/ui';
import { useAudio } from '@/hooks/useAudio';
import { useSounds } from '@/hooks';
import api, { VocabularyWord } from '@/lib/api';

export default function VisualFlashcardsPage() {
  const { activeChild } = useAuthStore();
  const [words, setWords] = useState<VocabularyWord[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);

  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  const { isPlaying, playAudio, stopAudio } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  const { onClick, onPageTurn, onCelebration } = useSounds();

  useEffect(() => {
    const fetchWords = async () => {
      if (!activeChild?.id) return;

      setLoading(true);
      try {
        // Fetch due flashcards
        const response = await api.getFlashcardsDue(activeChild.id, 20);
        if (response.success && response.data) {
          setWords(response.data);
        }
      } catch (error) {
        console.error('Failed to load flashcards:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWords();
  }, [activeChild?.id]);

  const handleNext = () => {
    if (currentIndex < words.length - 1) {
      onClick();
      setCurrentIndex(prev => prev + 1);
      setIsFlipped(false);
    } else if (currentIndex === words.length - 1) {
      onCelebration();
      // Show completion
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      onClick();
      setCurrentIndex(prev => prev - 1);
      setIsFlipped(false);
    }
  };

  const handleAudioPlay = (word: string) => {
    if (isPlaying) {
      stopAudio();
    } else {
      playAudio(word);
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <Loading size="lg" text="Loading flashcards..." />
      </MainLayout>
    );
  }

  if (words.length === 0) {
    return (
      <MainLayout>
        <div className="text-center py-12">
          <span className="text-6xl mb-4 block">✨</span>
          <h2 className="text-2xl font-bold mb-2">Great job!</h2>
          <p className="text-gray-600">No flashcards due for review right now.</p>
        </div>
      </MainLayout>
    );
  }

  const currentWord = words[currentIndex];

  return (
    <MainLayout headerTitle="Visual Flashcards">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Progress */}
        <div className="text-center">
          <p className="text-sm text-gray-500">
            Card {currentIndex + 1} of {words.length}
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div
              className="bg-primary-500 h-2 rounded-full transition-all"
              style={{ width: `${((currentIndex + 1) / words.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Flashcard */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <VisualFlashcard
              word={currentWord.word}
              romanization={currentWord.romanization}
              translation={currentWord.translation}
              imageUrl={currentWord.image_url}
              gender={currentWord.gender}
              partOfSpeech={currentWord.part_of_speech}
              exampleSentence={currentWord.example_sentence}
              isFlipped={isFlipped}
              onFlip={() => {
                onPageTurn();
                setIsFlipped(!isFlipped);
              }}
              onAudioPlay={handleAudioPlay}
            />
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            className="flex-1"
          >
            ← Previous
          </Button>
          <Button
            onClick={handleNext}
            className="flex-1"
          >
            {currentIndex === words.length - 1 ? 'Finish' : 'Next →'}
          </Button>
        </div>
      </div>
    </MainLayout>
  );
}
```

## Common Integration Patterns

### Pattern 1: Quiz Mode Integration

Use VisualFlashcard in a quiz context:

```tsx
const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
const [showResult, setShowResult] = useState(false);

<VisualFlashcard
  word={question.word}
  romanization={question.romanization}
  translation={question.translation}
  imageUrl={question.image_url}
  isFlipped={showResult}
  onFlip={() => setShowResult(true)}
  className={selectedAnswer ? 'pointer-events-none' : ''}
/>
```

### Pattern 2: Study Session with Timer

Add time pressure to flashcard review:

```tsx
const [timeLeft, setTimeLeft] = useState(30);

useEffect(() => {
  if (timeLeft > 0 && !isFlipped) {
    const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    return () => clearTimeout(timer);
  }
}, [timeLeft, isFlipped]);

<div className="space-y-4">
  <div className="text-center">
    <span className="text-2xl font-bold text-primary-600">
      {timeLeft}s
    </span>
  </div>
  <VisualFlashcard {...props} />
</div>
```

### Pattern 3: Spaced Repetition Integration

Track difficulty ratings after each card:

```tsx
const [difficulty, setDifficulty] = useState<number | null>(null);

const handleDifficultyRating = async (rating: 1 | 2 | 3 | 4) => {
  setDifficulty(rating);

  if (activeChild?.id) {
    await api.reviewFlashcard(activeChild.id, currentWord.id, rating);
  }

  // Move to next card
  setTimeout(() => {
    handleNext();
    setDifficulty(null);
  }, 500);
};

<div className="space-y-4">
  <VisualFlashcard {...props} />

  {isFlipped && !difficulty && (
    <div className="grid grid-cols-4 gap-2">
      <button onClick={() => handleDifficultyRating(1)}>
        😰 Again
      </button>
      <button onClick={() => handleDifficultyRating(2)}>
        🤔 Hard
      </button>
      <button onClick={() => handleDifficultyRating(3)}>
        😊 Good
      </button>
      <button onClick={() => handleDifficultyRating(4)}>
        😄 Easy
      </button>
    </div>
  )}
</div>
```

## Keyboard Shortcuts

Add keyboard navigation:

```tsx
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    switch (e.key) {
      case ' ':
      case 'Enter':
        e.preventDefault();
        setIsFlipped(!isFlipped);
        break;
      case 'ArrowRight':
        handleNext();
        break;
      case 'ArrowLeft':
        handlePrevious();
        break;
      case 'p':
      case 'P':
        handleAudioPlay(currentWord.word);
        break;
    }
  };

  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [isFlipped, currentIndex, currentWord]);
```

## Mobile Swipe Gestures

Add swipe support using framer-motion:

```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(e, { offset, velocity }) => {
    if (offset.x > 100) {
      handlePrevious();
    } else if (offset.x < -100) {
      handleNext();
    }
  }}
>
  <VisualFlashcard {...props} />
</motion.div>
```

## Performance Optimization

Preload images for smooth transitions:

```tsx
useEffect(() => {
  // Preload next 3 images
  const preloadIndices = [
    currentIndex + 1,
    currentIndex + 2,
    currentIndex + 3
  ].filter(i => i < words.length);

  preloadIndices.forEach(i => {
    if (words[i]?.image_url) {
      const img = new Image();
      img.src = words[i].image_url!;
    }
  });
}, [currentIndex, words]);
```

## Accessibility Enhancements

Add screen reader support:

```tsx
<div
  role="region"
  aria-label={`Flashcard ${currentIndex + 1} of ${words.length}`}
  aria-live="polite"
>
  <VisualFlashcard {...props} />
  <div className="sr-only">
    {isFlipped
      ? `Showing answer: ${currentWord.translation}`
      : `Question: ${currentWord.word}`
    }
  </div>
</div>
```

## Troubleshooting

### Issue: Cards not flipping smoothly

**Solution**: Ensure proper CSS is loaded for 3D transforms. The component includes inline styles, but if needed, add to globals.css:

```css
.perspective-1000 {
  perspective: 1000px;
}
.preserve-3d {
  transform-style: preserve-3d;
}
.backface-hidden {
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
```

### Issue: Images not loading

**Solution**: Verify image URLs are absolute or add domain to next.config.js:

```js
// next.config.js
module.exports = {
  images: {
    domains: ['your-cdn-domain.com'],
  },
}
```

### Issue: Audio not playing

**Solution**: Ensure useAudio hook is properly initialized and onAudioPlay callback is provided:

```tsx
const { playAudio } = useAudio({
  language: currentLanguage,
  voiceStyle: 'kid_friendly',
});

<VisualFlashcard
  {...props}
  onAudioPlay={(word) => playAudio(word)}
/>
```

## Best Practices

1. **Always reset flip state** when changing cards
2. **Provide category** for better placeholder visuals
3. **Use AnimatePresence** for smooth card transitions
4. **Implement loading states** when fetching data
5. **Handle empty states** gracefully
6. **Preload next images** for better UX
7. **Add keyboard shortcuts** for power users
8. **Track analytics** on card interactions
9. **Save progress** regularly
10. **Show completion feedback** after session

## Next Steps

1. Test the component in your vocabulary page
2. Add custom category mappings for your themes
3. Integrate with your SRS system
4. Add analytics tracking
5. Customize colors to match your theme
6. Add haptic feedback for mobile
7. Implement achievement system
8. Create study session presets
