'use client';

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import { Card, Button } from '@/components/ui';
import { useSounds } from '@/hooks';

interface StoryBuilderGameProps {
  onComplete?: (score: number, passed: boolean) => void;
  onBack?: () => void;
}

// Story building blocks
const STORY_BLOCKS = {
  starters: [
    { id: 's1', text: 'एक बार', emoji: '📖' },
    { id: 's2', text: 'कल सुबह', emoji: '🌅' },
    { id: 's3', text: 'एक दिन', emoji: '☀️' },
    { id: 's4', text: 'छुट्टियों में', emoji: '🎉' },
  ],
  characters: [
    { id: 'c1', text: 'एक छोटी लड़की', emoji: '👧' },
    { id: 'c2', text: 'एक बहादुर लड़का', emoji: '👦' },
    { id: 'c3', text: 'एक प्यारा पिल्ला', emoji: '🐶' },
    { id: 'c4', text: 'एक चतुर लोमड़ी', emoji: '🦊' },
  ],
  actions: [
    { id: 'a1', text: 'जंगल में गया', emoji: '🌳' },
    { id: 'a2', text: 'खजाना खोजा', emoji: '💎' },
    { id: 'a3', text: 'नई दोस्ती बनाई', emoji: '🤝' },
    { id: 'a4', text: 'सपना पूरा किया', emoji: '✨' },
  ],
  endings: [
    { id: 'e1', text: 'और खुश रहे।', emoji: '😊' },
    { id: 'e2', text: 'और कभी नहीं भूले।', emoji: '💭' },
    { id: 'e3', text: 'सबको बताया।', emoji: '📢' },
    { id: 'e4', text: 'नई कहानी की शुरुआत हुई।', emoji: '🔄' },
  ],
};

interface StoryPart {
  id: string;
  text: string;
  emoji: string;
  category: 'starters' | 'characters' | 'actions' | 'endings';
}

export default function StoryBuilderGame({ onComplete, onBack }: StoryBuilderGameProps) {
  const [story, setStory] = useState<StoryPart[]>([]);
  const [availableBlocks, setAvailableBlocks] = useState({
    starters: STORY_BLOCKS.starters,
    characters: STORY_BLOCKS.characters,
    actions: STORY_BLOCKS.actions,
    endings: STORY_BLOCKS.endings,
  });
  const [score, setScore] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const { onCorrect, onLevelUp, onClick } = useSounds();

  const categories: Array<'starters' | 'characters' | 'actions' | 'endings'> = ['starters', 'characters', 'actions', 'endings'];

  const currentCategoryIndex = story.length;
  const currentCategory = categories[currentCategoryIndex];

  const handleAddBlock = useCallback((block: StoryPart) => {
    onClick();
    
    // Remove from available
    setAvailableBlocks(prev => ({
      ...prev,
      [block.category]: prev[block.category].filter(b => b.id !== block.id),
    }));
    
    // Add to story
    setStory(prev => [...prev, block]);
    setScore(s => s + 10);
    
    // Check if story complete
    if (currentCategoryIndex === categories.length - 1) {
      setIsComplete(true);
      const finalScore = score + 10 + 20; // Add last block + completion bonus
      
      onCorrect();
      onLevelUp();
      
      confetti({
        particleCount: 150,
        spread: 100,
        origin: { y: 0.5 },
        colors: ['#f59e0b', '#22c55e', '#3b82f6', '#ec4899'],
      });
      
      onComplete?.(finalScore, true);
    }
  }, [currentCategoryIndex, score, onCorrect, onLevelUp, onComplete, onClick]);

  const handleUndo = useCallback(() => {
    if (story.length === 0) return;
    
    const lastBlock = story[story.length - 1];
    
    // Add back to available
    setAvailableBlocks(prev => ({
      ...prev,
      [lastBlock.category]: [...prev[lastBlock.category], lastBlock].sort((a, b) => a.id.localeCompare(b.id)),
    }));
    
    // Remove from story
    setStory(prev => prev.slice(0, -1));
    setScore(s => Math.max(0, s - 10));
  }, [story]);

  const handleReset = useCallback(() => {
    setStory([]);
    setAvailableBlocks({
      starters: STORY_BLOCKS.starters,
      characters: STORY_BLOCKS.characters,
      actions: STORY_BLOCKS.actions,
      endings: STORY_BLOCKS.endings,
    });
    setScore(0);
    setIsComplete(false);
  }, []);

  if (isComplete) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-100 flex items-center justify-center p-4">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="max-w-2xl w-full"
        >
          <Card className="p-8 bg-white shadow-xl">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">📚</div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">शाबाश!</h2>
              <p className="text-gray-600">आपने अपनी कहानी पूरी कर ली!</p>
            </div>

            {/* Story Display */}
            <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 mb-6 border-2 border-yellow-200">
              <div className="flex flex-wrap gap-2 items-center justify-center">
                {story.map((part, index) => (
                  <motion.span
                    key={part.id}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="inline-flex items-center gap-1 bg-white px-3 py-2 rounded-lg shadow-sm"
                  >
                    <span>{part.emoji}</span>
                    <span className="font-medium">{part.text}</span>
                  </motion.span>
                ))}
              </div>
            </div>

            {/* Score */}
            <div className="text-center mb-6">
              <div className="text-5xl font-bold text-primary-600">
                {score + 20}
              </div>
              <p className="text-sm text-gray-500">अंक (+20 बोनस)</p>
            </div>

            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={onBack}>
                वापस जाएं
              </Button>
              <Button 
                variant="primary" 
                onClick={handleReset}
              >
                नई कहानी बनाएं
              </Button>
            </div>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-100">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Button variant="ghost" size="sm" onClick={onBack}>
            ← वापस
          </Button>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              भाग {story.length + 1} / {categories.length}
            </span>
            <div className="w-32 h-3 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-yellow-500"
                initial={{ width: 0 }}
                animate={{ width: `${(story.length / categories.length) * 100}%` }}
              />
            </div>
          </div>
          <span className="text-lg font-bold text-primary-600">
            {score} XP
          </span>
        </div>
      </div>

      {/* Story Progress */}
      <div className="max-w-4xl mx-auto p-4">
        <Card className="p-4 mb-4 bg-white shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 mb-2">आपकी कहानी:</h3>
          <div className="flex flex-wrap gap-2 items-center">
            {story.length === 0 ? (
              <p className="text-gray-400 italic">कहानी शुरू करने के लिए नीचे से चुनें...</p>
            ) : (
              story.map((part) => (
                <motion.span
                  key={part.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="inline-flex items-center gap-1 bg-yellow-100 px-3 py-1.5 rounded-lg"
                >
                  <span>{part.emoji}</span>
                  <span className="text-sm">{part.text}</span>
                </motion.span>
              ))
            )}
          </div>
          
          {/* Undo Button */}
          {story.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleUndo}
              className="mt-3"
            >
              ↩️ वापस करें
            </Button>
          )}
        </Card>
      </div>

      {/* Current Category */}
      <div className="max-w-4xl mx-auto p-4">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentCategory}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Card className="p-6 bg-white shadow-lg">
              <div className="flex items-center gap-3 mb-4">
                {currentCategory === 'starters' && <span className="text-3xl">🌱</span>}
                {currentCategory === 'characters' && <span className="text-3xl">👤</span>}
                {currentCategory === 'actions' && <span className="text-3xl">⚡</span>}
                {currentCategory === 'endings' && <span className="text-3xl">🏁</span>}
                <div>
                  <h2 className="text-xl font-bold text-gray-900">
                    {currentCategory === 'starters' && 'कहानी की शुरुआत चुनें'}
                    {currentCategory === 'characters' && 'मुख्य पात्र चुनें'}
                    {currentCategory === 'actions' && 'क्या हुआ चुनें'}
                    {currentCategory === 'endings' && 'कहानी का अंत चुनें'}
                  </h2>
                  <p className="text-sm text-gray-500">
                    {currentCategory === 'starters' && 'कहानी कब और कहाँ शुरू होती है?'}
                    {currentCategory === 'characters' && 'कौन है इस कहानी का नायक?'}
                    {currentCategory === 'actions' && 'क्या किया उन्होंने?'}
                    {currentCategory === 'endings' && 'कहानी कैसे खत्म होती है?'}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {availableBlocks[currentCategory].map((block) => (
                  <motion.button
                    key={block.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleAddBlock({ ...block, category: currentCategory })}
                    className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 hover:from-yellow-100 hover:to-orange-100 rounded-xl border-2 border-yellow-200 hover:border-yellow-300 transition-colors text-left"
                  >
                    <span className="text-2xl mb-2 block">{block.emoji}</span>
                    <span className="font-medium text-gray-800">{block.text}</span>
                  </motion.button>
                ))}
              </div>
            </Card>
          </motion.div>
        </AnimatePresence>

        {/* Progress Indicator */}
        <div className="flex justify-center gap-2 mt-6">
          {categories.map((cat, index) => (
            <div
              key={cat}
              className={`w-3 h-3 rounded-full transition-colors ${
                index < story.length
                  ? 'bg-green-500'
                  : index === story.length
                    ? 'bg-yellow-500'
                    : 'bg-gray-300'
              }`}
            />
          ))}
        </div>

        {/* Reset Button */}
        <div className="flex justify-center mt-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleReset}
            disabled={story.length === 0}
          >
            🔄 कहानी रीसेट करें
          </Button>
        </div>
      </div>
    </div>
  );
}
