/**
 * VisualFlashcard Component - Usage Examples
 *
 * This file demonstrates how to use the VisualFlashcard component
 * in different scenarios.
 */

'use client';

import { useState } from 'react';
import { VisualFlashcard } from './VisualFlashcard';

/**
 * Example 1: Basic Usage with Image
 * Most common use case with a vocabulary word that has an image
 */
export function BasicFlashcardExample() {
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
      onAudioPlay={(word) => console.log('Playing audio for:', word)}
    />
  );
}

/**
 * Example 2: Without Image (Uses Category-based Placeholder)
 * When no image is available, shows a gradient with category icon
 */
export function PlaceholderFlashcardExample() {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <VisualFlashcard
      word="नमस्ते"
      romanization="namaste"
      translation="hello"
      category="Greetings"
      gender="neutral"
      partOfSpeech="interjection"
      exampleSentence="नमस्ते! आप कैसे हैं?"
      isFlipped={isFlipped}
      onFlip={() => setIsFlipped(!isFlipped)}
      onAudioPlay={(word) => console.log('Playing audio for:', word)}
    />
  );
}

/**
 * Example 3: Multiple Flashcards with Navigation
 * Common pattern for vocabulary practice with multiple words
 */
export function FlashcardListExample() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const words = [
    {
      id: '1',
      word: 'माता',
      romanization: 'mātā',
      translation: 'mother',
      imageUrl: '/images/vocabulary/mother.jpg',
      gender: 'feminine',
      partOfSpeech: 'noun',
      category: 'Family',
      exampleSentence: 'मेरी माता बहुत दयालु हैं।'
    },
    {
      id: '2',
      word: 'पिता',
      romanization: 'pitā',
      translation: 'father',
      imageUrl: '/images/vocabulary/father.jpg',
      gender: 'masculine',
      partOfSpeech: 'noun',
      category: 'Family',
      exampleSentence: 'मेरे पिता डॉक्टर हैं।'
    },
    {
      id: '3',
      word: 'बहन',
      romanization: 'bahan',
      translation: 'sister',
      category: 'Family',
      gender: 'feminine',
      partOfSpeech: 'noun',
      exampleSentence: 'मेरी बहन विद्यालय जाती है।'
    }
  ];

  const currentWord = words[currentIndex];

  const handleNext = () => {
    if (currentIndex < words.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Progress Indicator */}
      <div className="text-center">
        <p className="text-sm text-gray-500">
          Card {currentIndex + 1} of {words.length}
        </p>
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div
            className="bg-primary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / words.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Flashcard */}
      <VisualFlashcard
        word={currentWord.word}
        romanization={currentWord.romanization}
        translation={currentWord.translation}
        imageUrl={currentWord.imageUrl}
        gender={currentWord.gender}
        partOfSpeech={currentWord.partOfSpeech}
        category={currentWord.category}
        exampleSentence={currentWord.exampleSentence}
        isFlipped={isFlipped}
        onFlip={() => setIsFlipped(!isFlipped)}
        onAudioPlay={(word) => console.log('Playing audio for:', word)}
      />

      {/* Navigation Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          className="flex-1 py-2 px-4 rounded-xl font-medium bg-gray-100 text-gray-600
                     hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          disabled={currentIndex === words.length - 1}
          className="flex-1 py-2 px-4 rounded-xl font-medium bg-primary-500 text-white
                     hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  );
}

/**
 * Example 4: Integration with Audio Playback
 * Shows how to integrate with the useAudio hook
 */
export function FlashcardWithAudioExample() {
  const [isFlipped, setIsFlipped] = useState(false);

  // In a real implementation, you would use the useAudio hook here
  const handleAudioPlay = async (word: string) => {
    console.log('Playing audio for:', word);
  };

  return (
    <VisualFlashcard
      word="कुत्ता"
      romanization="kuttā"
      translation="dog"
      category="Animals"
      gender="masculine"
      partOfSpeech="noun"
      exampleSentence="कुत्ता भौंक रहा है।"
      isFlipped={isFlipped}
      onFlip={() => setIsFlipped(!isFlipped)}
      onAudioPlay={handleAudioPlay}
    />
  );
}

/**
 * Single category card component - extracted to avoid hooks in callback
 */
function CategoryCard({ cat }: { cat: { name: string; word: string; romanization: string; translation: string } }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <VisualFlashcard
      word={cat.word}
      romanization={cat.romanization}
      translation={cat.translation}
      category={cat.name}
      partOfSpeech="noun"
      isFlipped={isFlipped}
      onFlip={() => setIsFlipped(!isFlipped)}
    />
  );
}

/**
 * Example 5: Different Categories
 * Shows various category-based placeholder styles
 */
export function CategoryExamplesGrid() {
  const categories = [
    { name: 'Family', word: 'परिवार', romanization: 'parivār', translation: 'family' },
    { name: 'Colors', word: 'लाल', romanization: 'lāl', translation: 'red' },
    { name: 'Numbers', word: 'एक', romanization: 'ek', translation: 'one' },
    { name: 'Animals', word: 'बिल्ली', romanization: 'billī', translation: 'cat' },
    { name: 'Food', word: 'सेब', romanization: 'seb', translation: 'apple' },
    { name: 'Body Parts', word: 'हाथ', romanization: 'hāth', translation: 'hand' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {categories.map((cat) => (
        <CategoryCard key={cat.name} cat={cat} />
      ))}
    </div>
  );
}
