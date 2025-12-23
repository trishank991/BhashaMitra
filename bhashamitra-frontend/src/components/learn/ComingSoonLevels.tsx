'use client';

import { ComingSoonCard } from '@/components/ui/ComingSoonCard';
import { Sprout, Sun, Droplets, Star } from 'lucide-react';

const upcomingLevels = [
  {
    code: 'L2',
    title: 'Level 2',
    titleHindi: 'अंकुर (Sprout)',
    description: 'Build on basics with matras, more vocabulary, and simple sentences',
    releaseHint: 'Coming Q1 2025',
    color: '#27ae60',
    icon: <Sprout className="w-10 h-10 text-green-600" />,
    peppiMessage: 'L2 में हम साथ में matras सीखेंगे! का, कि, की...',
  },
  {
    code: 'L3',
    title: 'Level 3',
    titleHindi: 'किरण (Ray)',
    description: 'Reading simple words, writing practice, and basic grammar',
    releaseHint: 'Coming Q2 2025',
    color: '#2980b9',
    icon: <Sun className="w-10 h-10 text-blue-600" />,
    peppiMessage: 'Soon you\'ll read your first Hindi book!',
  },
  {
    code: 'L4',
    title: 'Level 4',
    titleHindi: 'धारा (Stream)',
    description: 'Sentence formation, storytelling, and expanded vocabulary',
    releaseHint: 'Coming 2025',
    color: '#8e44ad',
    icon: <Droplets className="w-10 h-10 text-purple-600" />,
    peppiMessage: 'Ready to tell stories in Hindi?',
  },
  {
    code: 'L5',
    title: 'Level 5',
    titleHindi: 'तारा (Star)',
    description: 'Fluent reading, creative writing, and cultural immersion',
    releaseHint: 'Coming 2025',
    color: '#f39c12',
    icon: <Star className="w-10 h-10 text-yellow-600" />,
    peppiMessage: 'You\'ll shine like a star! ⭐',
  },
];

interface ComingSoonLevelsProps {
  onWaitlistClick?: (levelCode: string) => void;
  className?: string;
}

export function ComingSoonLevels({ onWaitlistClick, className }: ComingSoonLevelsProps) {
  return (
    <div className={className}>
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Your Learning Journey</h2>
        <p className="text-gray-600">Complete L1 to unlock the next level!</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {upcomingLevels.map((level) => (
          <ComingSoonCard
            key={level.code}
            title={level.title}
            titleHindi={level.titleHindi}
            description={level.description}
            releaseHint={level.releaseHint}
            peppiMessage={level.peppiMessage}
            type="level"
            icon={level.icon}
            color={level.color}
            showWaitlist
            onWaitlistClick={() => onWaitlistClick?.(level.code)}
          />
        ))}
      </div>
    </div>
  );
}

export default ComingSoonLevels;
