/**
 * Example usage of PictureWordGame component
 *
 * This file demonstrates how to use the PictureWordGame component
 * with sample data for testing and integration.
 */

import { PictureWordGame } from './PictureWordGame';

// Sample word data for testing
const sampleWords = [
  {
    id: '1',
    word: 'सेब',
    transliteration: 'seb',
    meaning: 'apple',
    imageUrl: '/images/vocabulary/apple.jpg',
    audioUrl: '/audio/words/seb.mp3', // Optional
  },
  {
    id: '2',
    word: 'केला',
    transliteration: 'kela',
    meaning: 'banana',
    imageUrl: '/images/vocabulary/banana.jpg',
  },
  {
    id: '3',
    word: 'बिल्ली',
    transliteration: 'billi',
    meaning: 'cat',
    imageUrl: '/images/vocabulary/cat.jpg',
  },
  {
    id: '4',
    word: 'कुत्ता',
    transliteration: 'kutta',
    meaning: 'dog',
    imageUrl: '/images/vocabulary/dog.jpg',
  },
  {
    id: '5',
    word: 'फूल',
    transliteration: 'phool',
    meaning: 'flower',
    imageUrl: '/images/vocabulary/flower.jpg',
  },
  {
    id: '6',
    word: 'किताब',
    transliteration: 'kitaab',
    meaning: 'book',
    imageUrl: '/images/vocabulary/book.jpg',
  },
  {
    id: '7',
    word: 'पानी',
    transliteration: 'paani',
    meaning: 'water',
    imageUrl: '/images/vocabulary/water.jpg',
  },
  {
    id: '8',
    word: 'सूरज',
    transliteration: 'suraj',
    meaning: 'sun',
    imageUrl: '/images/vocabulary/sun.jpg',
  },
];

export function PictureWordGameExample() {
  const handleGameComplete = (score: number, totalQuestions: number) => {
    console.log(`Game completed! Score: ${score}/${totalQuestions * 10}`);
    // You can add logic here to:
    // - Save score to database
    // - Update user progress
    // - Show achievements
    // - Navigate to next lesson
  };

  const handleBack = () => {
    console.log('Back button clicked');
    // Navigate back to games list or previous page
  };

  return (
    <PictureWordGame
      words={sampleWords}
      language="HINDI"
      onGameComplete={handleGameComplete}
      onBack={handleBack}
    />
  );
}

/**
 * Usage in a page or component:
 *
 * import { PictureWordGame } from '@/components/games';
 * import { useWords } from '@/hooks/useWords'; // Hypothetical hook to fetch words
 *
 * export default function VocabularyGamePage() {
 *   const { words, loading } = useWords({ category: 'fruits' });
 *
 *   if (loading) return <div>Loading...</div>;
 *
 *   return (
 *     <PictureWordGame
 *       words={words}
 *       language="HINDI"
 *       onGameComplete={(score, total) => {
 *         // Save progress
 *         console.log(`Score: ${score}/${total * 10}`);
 *       }}
 *       onBack={() => router.back()}
 *     />
 *   );
 * }
 */

export default PictureWordGameExample;
