# PictureWordGame Component

An interactive picture-word matching game component for the BhashaMitra language learning application. Children see an image and must select the correct word from multiple options.

## Component Location

`/bhashamitra-frontend/src/components/games/PictureWordGame.tsx`

## Features

- **Image-based Learning**: Large, clear images help visual learners
- **Multiple Choice Options**: 3-4 word options based on child's age
- **Audio Support**: Plays word pronunciation with TTS or custom audio
- **Age-Adaptive UI**: Adjusts difficulty and UI based on child's age (junior/standard/teen)
- **Progressive Difficulty**: Tracks attempts (max 2) and adjusts scoring
- **Real-time Feedback**:
  - Correct answers: green highlight, correct sound, star animation
  - Wrong answers: red highlight, shake animation, wrong sound
- **Peppi Encouragement**: Friendly cat mascot provides contextual feedback
- **Score Tracking**: Points system (10 for first try, 5 for second, 3 for third)
- **Celebration Animation**: Confetti effect on game completion
- **Progress Indicators**: Question counter and progress bar
- **Responsive Design**: Works on mobile, tablet, and desktop

## Props Interface

```typescript
interface Word {
  id: string;
  word: string;              // Hindi word (e.g., "सेब")
  transliteration: string;   // Romanized form (e.g., "seb")
  meaning: string;           // English meaning (e.g., "apple")
  imageUrl: string;          // URL to image
  audioUrl?: string;         // Optional custom audio URL
}

interface PictureWordGameProps {
  words: Word[];                    // Array of words with images
  language?: string;                // Default: 'HINDI'
  onGameComplete: (score: number, totalQuestions: number) => void;
  onBack?: () => void;              // Optional back navigation
  className?: string;               // Optional container class
}
```

## Usage Examples

### Basic Usage

```tsx
import { PictureWordGame } from '@/components/games';

const words = [
  {
    id: '1',
    word: 'सेब',
    transliteration: 'seb',
    meaning: 'apple',
    imageUrl: '/images/vocabulary/apple.jpg',
  },
  // ... more words
];

function VocabularyGame() {
  const handleComplete = (score, total) => {
    console.log(`Score: ${score}/${total * 10}`);
    // Save to database, show achievement, etc.
  };

  return (
    <PictureWordGame
      words={words}
      onGameComplete={handleComplete}
    />
  );
}
```

### With Custom Audio

```tsx
const wordsWithAudio = [
  {
    id: '1',
    word: 'केला',
    transliteration: 'kela',
    meaning: 'banana',
    imageUrl: '/images/vocabulary/banana.jpg',
    audioUrl: '/audio/words/kela.mp3', // Custom pronunciation
  },
  // ... more words
];

<PictureWordGame
  words={wordsWithAudio}
  language="HINDI"
  onGameComplete={(score, total) => {
    saveProgress({ score, total });
  }}
  onBack={() => router.back()}
/>
```

### Integration with Next.js Page

```tsx
// app/games/vocabulary/[category]/page.tsx
import { PictureWordGame } from '@/components/games';
import { useRouter } from 'next/navigation';

export default function VocabularyGamePage({ params }) {
  const router = useRouter();
  const words = useWords(params.category); // Custom hook

  return (
    <PictureWordGame
      words={words}
      onGameComplete={async (score, total) => {
        // Save progress
        await api.saveGameProgress({
          gameType: 'picture_word',
          category: params.category,
          score,
          totalQuestions: total,
        });

        // Show achievement
        if (score >= total * 9) {
          showAchievement('Perfect Score!');
        }
      }}
      onBack={() => router.push('/games')}
    />
  );
}
```

## Game Flow

1. **Initialization**: Component shuffles words and creates questions (max 10)
2. **Question Display**:
   - Shows image in center
   - Displays audio button for word pronunciation
   - Shows word options below (3-4 based on age)
3. **Selection**: Child taps a word option
4. **Feedback**:
   - **Correct**: Green highlight → Star animation → Move to next (1.5s delay)
   - **Wrong**: Red shake → Allow retry (max 2 attempts) → Show correct answer
5. **Completion**: After all questions → Celebration animation → Score screen with stars

## Age-Based Adaptations

### Junior (≤6 years)
- 3 word options (simpler)
- Larger fonts (text-4xl headings)
- Focus on transliteration (not Hindi script)
- More encouraging messages
- Larger Peppi avatar

### Standard (7-10 years)
- 4 word options
- Medium fonts (text-3xl headings)
- Shows both Hindi script and transliteration
- Balanced difficulty

### Teen (11+ years)
- 4 word options
- Smaller fonts (text-2xl headings)
- Shows Hindi script, transliteration, and meaning
- More sophisticated UI

## Scoring System

- **First attempt correct**: 10 points
- **Second attempt correct**: 5 points
- **Third attempt (shown answer)**: 3 points
- **Maximum score**: `totalQuestions × 10`

## Star Rating (Game Complete)

- 5 stars: ≥90% score
- 4 stars: ≥75% score
- 3 stars: ≥60% score
- 2 stars: ≥40% score
- 1 star: <40% score

## Sound Effects

Uses `useSounds()` hook for audio feedback:
- `onCorrect()`: Cheerful chime for correct answers
- `onWrong()`: Gentle buzz for incorrect answers
- `onCelebration()`: Celebratory fanfare on completion

## Animations

- **Entry**: Fade in + slide up for questions
- **Option hover**: Scale up (1.05x)
- **Correct selection**: Green pulse + star burst
- **Wrong selection**: Red shake (horizontal vibration)
- **Progress bar**: Smooth width transition
- **Completion**: Confetti particles falling

## Dependencies

- `framer-motion`: Animations and transitions
- `lucide-react`: Icons (Trophy, Star, ArrowLeft, RefreshCw)
- `@/hooks/useAgeConfig`: Age-adaptive configuration
- `@/hooks/useSounds`: Sound effects management
- `@/components/ui/AudioButton`: TTS audio playback
- `@/components/peppi/PeppiSpeech`: Mascot feedback
- `@/components/animations/Celebration`: Confetti animation
- `@/lib/utils`: Utility functions (cn, shuffleArray)

## Accessibility

- **Keyboard Navigation**: Full keyboard support for option selection
- **Audio Support**: Text-to-speech for all words
- **Visual Feedback**: Clear color coding (green=correct, red=wrong)
- **Screen Readers**: Semantic HTML with proper ARIA labels
- **Large Touch Targets**: Mobile-friendly button sizes

## Performance Considerations

- **Image Optimization**: Use Next.js Image component for production
- **Audio Preloading**: Audio files loaded on-demand
- **Memoization**: useMemo for options count calculation
- **Animation Throttling**: Celebration effects cleared after completion
- **State Management**: Efficient re-renders with proper dependencies

## Customization

### Custom Styling

```tsx
<PictureWordGame
  words={words}
  className="custom-gradient-bg"
  onGameComplete={handleComplete}
/>
```

### Custom Language

```tsx
<PictureWordGame
  words={tamilWords}
  language="TAMIL"
  onGameComplete={handleComplete}
/>
```

## Testing

### Unit Test Example

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { PictureWordGame } from './PictureWordGame';

describe('PictureWordGame', () => {
  const mockWords = [
    { id: '1', word: 'सेब', transliteration: 'seb', meaning: 'apple', imageUrl: '/apple.jpg' },
    { id: '2', word: 'केला', transliteration: 'kela', meaning: 'banana', imageUrl: '/banana.jpg' },
    { id: '3', word: 'आम', transliteration: 'aam', meaning: 'mango', imageUrl: '/mango.jpg' },
    { id: '4', word: 'अंगूर', transliteration: 'angoor', meaning: 'grapes', imageUrl: '/grapes.jpg' },
  ];

  it('renders game with first question', () => {
    render(<PictureWordGame words={mockWords} onGameComplete={jest.fn()} />);
    expect(screen.getByText(/Picture Word Match/i)).toBeInTheDocument();
    expect(screen.getByText(/Question 1\//i)).toBeInTheDocument();
  });

  it('handles correct answer selection', () => {
    const onComplete = jest.fn();
    render(<PictureWordGame words={mockWords} onGameComplete={onComplete} />);

    // Select correct option
    const correctButton = screen.getByText('seb');
    fireEvent.click(correctButton);

    // Check for visual feedback
    expect(correctButton).toHaveClass('bg-green-100');
  });
});
```

## Troubleshooting

### Images not loading
- Verify `imageUrl` paths are correct
- Use absolute URLs or Next.js public folder
- Check CORS settings for external images

### Audio not playing
- Ensure TTS service is configured
- Check `audioUrl` format (mp3/wav supported)
- Verify browser audio permissions

### Wrong number of options
- Check `words` array has at least `optionsCount` items
- Verify `useAgeConfig` returns correct variant
- Console.warn shows if insufficient words

## Future Enhancements

- [ ] Time-based challenges
- [ ] Streak tracking
- [ ] Difficulty levels (easy/medium/hard)
- [ ] Hint system (reveal first letter)
- [ ] Multi-language support
- [ ] Leaderboard integration
- [ ] Offline mode support

## Related Components

- `MatchPairsGame`: Match words with meanings/images
- `LetterMatchGame`: Letter recognition game
- `AlphabetQuiz`: Alphabet learning quiz
- `VocabularyFlashcards`: Vocabulary flashcard review

## License

Part of the BhashaMitra language learning platform.
