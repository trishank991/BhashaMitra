# VisualFlashcard Component

A beautiful, interactive flashcard component designed for vocabulary learning with age-adaptive features, 3D flip animations, and visual learning support.

## Location

`/bhashamitra-frontend/src/components/curriculum/VisualFlashcard.tsx`

## Features

### Core Features

1. **3D Flip Animation**
   - Smooth card flip using framer-motion
   - Click/tap anywhere on the card to flip
   - Age-adaptive animation speed (slower for younger children)
   - Bounce effect for junior learners

2. **Visual Learning Support**
   - Large image area for vocabulary words
   - Category-based gradient placeholders when no image is available
   - 8 themed categories with unique icons and gradients

3. **Age-Adaptive Design**
   - **Junior (≤6 years)**: Larger fonts, simplified UI, colorful, bounce animations
   - **Standard (7-10 years)**: Medium fonts, full features, moderate animations
   - **Teen (11+ years)**: Compact, shows all information, subtle animations

4. **Audio Integration**
   - Speaker button with loading and playing states
   - Click-to-hear pronunciation
   - Visual sound wave animation when playing

5. **Educational Metadata**
   - Gender badges (M/F) with color coding
   - Part of speech labels
   - Example sentences (hidden for junior learners)
   - Romanization support

## Props Interface

```typescript
interface VisualFlashcardProps {
  word: string;              // Word in native script (e.g., "पिता")
  romanization: string;       // Romanized version (e.g., "pitā")
  translation: string;        // English translation (e.g., "father")
  imageUrl?: string;          // Optional image URL
  audioUrl?: string;          // Optional audio URL (not currently used)
  gender?: string;            // Gender: "masculine", "feminine", "M", "F"
  partOfSpeech?: string;      // e.g., "noun", "verb", "adjective"
  exampleSentence?: string;   // Example usage in native language
  isFlipped: boolean;         // Current flip state
  onFlip: () => void;         // Callback when card is flipped
  onAudioPlay?: (word: string) => void;  // Callback for audio playback
  className?: string;         // Additional CSS classes
  category?: string;          // Category for placeholder styling
}
```

## Categories and Theming

### Available Categories

Each category has a unique icon and gradient when no image is provided:

| Category | Icon | Gradient Colors |
|----------|------|----------------|
| Family | 👨‍👩‍👧 | Pink → Purple → Indigo |
| Colors | 🎨 | Red → Yellow → Blue |
| Numbers | 🔢 | Cyan → Blue → Indigo |
| Animals | 🐾 | Green → Emerald → Teal |
| Food | 🍎 | Orange → Amber → Yellow |
| Body Parts | 🖐️ | Rose → Pink → Fuchsia |
| Greetings | 👋 | Violet → Purple → Indigo |
| Actions | 🏃 | Lime → Green → Emerald |
| Default | 📚 | Purple → Pink |

## Usage Examples

### Basic Usage

```tsx
import { useState } from 'react';
import { VisualFlashcard } from '@/components/curriculum';

function MyComponent() {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <VisualFlashcard
      word="पिता"
      romanization="pitā"
      translation="father"
      imageUrl="/images/vocabulary/father.jpg"
      gender="masculine"
      partOfSpeech="noun"
      category="Family"
      isFlipped={isFlipped}
      onFlip={() => setIsFlipped(!isFlipped)}
      onAudioPlay={(word) => console.log('Playing:', word)}
    />
  );
}
```

### Without Image (Category Placeholder)

```tsx
<VisualFlashcard
  word="नमस्ते"
  romanization="namaste"
  translation="hello"
  category="Greetings"
  partOfSpeech="interjection"
  isFlipped={isFlipped}
  onFlip={() => setIsFlipped(!isFlipped)}
/>
```

### With Audio Integration

```tsx
import { useAudio } from '@/hooks/useAudio';

function FlashcardWithAudio() {
  const [isFlipped, setIsFlipped] = useState(false);
  const { playAudio } = useAudio({ language: 'HINDI' });

  const handleAudioPlay = async (word: string) => {
    await playAudio(word);
  };

  return (
    <VisualFlashcard
      word="कुत्ता"
      romanization="kuttā"
      translation="dog"
      category="Animals"
      isFlipped={isFlipped}
      onFlip={() => setIsFlipped(!isFlipped)}
      onAudioPlay={handleAudioPlay}
    />
  );
}
```

### Multiple Cards with Navigation

See `VisualFlashcard.example.tsx` for a complete example with:
- Multiple cards
- Progress indicator
- Previous/Next navigation
- Auto-reset flip state on card change

## Card Layout

### Front of Card (Not Flipped)

```
┌─────────────────────┐
│                     │
│   [Large Image]     │
│   or Placeholder    │
│                     │
├─────────────────────┤
│                     │
│      पिता           │  ← Large native script
│      (pitā)         │  ← Romanization
│                     │
│      [🔊]           │  ← Audio button
│                     │
│ "Tap to see meaning"│  ← Hint text
└─────────────────────┘
```

### Back of Card (Flipped)

```
┌─────────────────────┐
│   [Small Image]     │  ← Smaller version at top
├─────────────────────┤
│      पिता           │  ← Native script
│      (pitā)         │  ← Romanization
│     --------        │  ← Divider
│                     │
│     FATHER          │  ← Translation (large, bold)
│                     │
│   [M] [noun]        │  ← Gender & Part of Speech badges
│                     │
│ "मेरे पिता डॉक्टर हैं।" │  ← Example sentence (if provided)
│                     │
│  "Tap to flip back" │  ← Hint text
└─────────────────────┘
```

## Age-Adaptive Behavior

### Junior (≤6 years)
- **Font Sizes**: Extra large (text-5xl/6xl for words)
- **Animation**: Slower (0.5s) with bounce
- **UI**: Simplified (no small image on back, no example sentence)
- **Hints**: "Tap to see what it means!" (more friendly)
- **Speaker Button**: Large size

### Standard (7-10 years)
- **Font Sizes**: Large (text-4xl/5xl for words)
- **Animation**: Medium speed (0.3s) with bounce
- **UI**: Full features (all metadata shown)
- **Hints**: "Tap to see meaning"
- **Speaker Button**: Medium size

### Teen (11+ years)
- **Font Sizes**: Compact (text-3xl/4xl for words)
- **Animation**: Fast (0.2s) without bounce
- **UI**: Full features, more information density
- **Hints**: "Tap to see meaning"
- **Speaker Button**: Medium size

## Animation Details

The component uses framer-motion for smooth 3D transformations:

```typescript
// Flip animation
animate={{ rotateY: isFlipped ? 180 : 0 }}

// Hover/Tap effects
whileHover={{ scale: 1.02 }}
whileTap={{ scale: 0.98 }}

// CSS for 3D effect
.perspective-1000 { perspective: 1000px; }
.preserve-3d { transform-style: preserve-3d; }
.backface-hidden { backface-visibility: hidden; }
```

## Accessibility

- **Keyboard Support**: Card is clickable and keyboard accessible
- **ARIA Labels**: Speaker button has proper aria-label
- **Visual Feedback**: Hover and tap animations provide clear interaction feedback
- **Loading States**: Visual spinner when audio is loading

## Integration Points

### Works With

1. **useAgeConfig Hook**: Automatically adapts to child's age
2. **SpeakerButton Component**: Provides audio playback UI
3. **useAudio Hook**: For actual audio playback functionality
4. **VocabularyWord API Type**: Matches backend data structure

### Data Source

The component expects data in this format (from `/lib/api.ts`):

```typescript
interface VocabularyWord {
  id: string;
  word: string;
  romanization: string;
  translation: string;
  part_of_speech: string;
  gender: string;
  example_sentence: string;
  pronunciation_audio_url?: string;
  image_url?: string;
}
```

## Customization

### Custom Styling

Add custom classes via the `className` prop:

```tsx
<VisualFlashcard
  // ... other props
  className="max-w-md mx-auto my-4"
/>
```

### Custom Categories

To add new categories, update these constants in the component:

```typescript
const CATEGORY_ICONS: Record<string, string> = {
  'MyCategory': '🎯',  // Add your icon
  // ...
};

const CATEGORY_GRADIENTS: Record<string, string> = {
  'MyCategory': 'from-red-100 to-blue-100',  // Add your gradient
  // ...
};
```

## Performance Considerations

1. **Image Optimization**: Uses Next.js Image component for automatic optimization
2. **Error Handling**: Falls back to placeholder if image fails to load
3. **Lazy Loading**: Images load only when needed
4. **Animation Performance**: Uses GPU-accelerated transforms (rotateY)

## Future Enhancements

Potential improvements for future versions:

- [ ] Swipe gestures for mobile (left/right to navigate)
- [ ] Keyboard shortcuts (space to flip, arrows to navigate)
- [ ] Star/favorite functionality
- [ ] Difficulty rating after review
- [ ] Progress tracking integration
- [ ] Offline support with cached images
- [ ] Multiple image support (slideshow)
- [ ] Text-to-speech integration for example sentences

## Related Components

- **FlashcardReview**: SRS-based flashcard review system
- **WordCard**: Simpler word display component
- **VocabularyThemeDetailPage**: Uses flashcards for vocabulary practice

## See Also

- [Usage Examples](./VisualFlashcard.example.tsx)
- [Age Config Hook](../../hooks/useAgeConfig.ts)
- [Speaker Button](../ui/SpeakerButton.tsx)
- [Vocabulary Page](../../app/learn/vocabulary/[id]/page.tsx)
