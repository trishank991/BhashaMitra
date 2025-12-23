'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Classroom, ClassroomThemeType, CLASSROOM_THEMES } from '@/types/curriculum';

interface ClassroomBackgroundProps {
  classroom?: Classroom;
  theme?: ClassroomThemeType;
  children: React.ReactNode;
  className?: string;
  showElements?: boolean;
}

// Get theme-specific background styles
const getThemeStyles = (theme: ClassroomThemeType) => {
  switch (theme) {
    case 'GARDEN':
      return 'bg-gradient-to-b from-green-100 via-green-50 to-yellow-50';
    case 'TREEHOUSE':
      return 'bg-gradient-to-b from-amber-100 via-orange-50 to-green-100';
    case 'FOREST':
      return 'bg-gradient-to-b from-green-200 via-green-100 to-emerald-50';
    case 'MEADOW':
      return 'bg-gradient-to-b from-yellow-100 via-green-50 to-yellow-50';
    case 'NIGHT_SKY':
      return 'bg-gradient-to-b from-indigo-900 via-purple-900 to-blue-900';
    case 'LIBRARY':
      return 'bg-gradient-to-b from-amber-100 via-orange-50 to-amber-50';
    case 'MOUNTAIN':
      return 'bg-gradient-to-b from-blue-200 via-slate-100 to-blue-50';
    case 'SPACE':
      return 'bg-gradient-to-b from-slate-900 via-purple-900 to-indigo-900';
    case 'PALACE':
      return 'bg-gradient-to-b from-purple-100 via-pink-50 to-purple-50';
    case 'ROYAL_COURT':
      return 'bg-gradient-to-b from-yellow-200 via-amber-100 to-orange-50';
    default:
      return 'bg-gradient-to-b from-blue-50 to-white';
  }
};

// Get text color based on theme (for dark backgrounds)
const getTextColor = (theme: ClassroomThemeType) => {
  if (theme === 'NIGHT_SKY' || theme === 'SPACE') {
    return 'text-white';
  }
  return 'text-gray-800';
};

// Decorative elements for each theme
const ThemeElements: React.FC<{ theme: ClassroomThemeType; elements?: string[] }> = ({ theme, elements }) => {
  const renderElement = (element: string, index: number) => {
    const elementEmojis: Record<string, string> = {
      flowers: '🌸',
      butterflies: '🦋',
      sunshine: '☀️',
      watering_can: '🚿',
      wooden_cabin: '🏠',
      birds: '🐦',
      leaves: '🍃',
      rope_ladder: '🪜',
      tall_trees: '🌲',
      mushrooms: '🍄',
      sunrays: '✨',
      forest_animals: '🦊',
      wildflowers: '🌻',
      grass: '🌿',
      rainbow: '🌈',
      stars: '⭐',
      moon: '🌙',
      constellations: '✨',
      shooting_stars: '💫',
      bookshelves: '📚',
      scrolls: '📜',
      candles: '🕯️',
      reading_desk: '📖',
      snow_peak: '🏔️',
      clouds: '☁️',
      eagles: '🦅',
      prayer_flags: '🎏',
      planets: '🪐',
      spacecraft: '🚀',
      nebula: '🌌',
      crystals: '💎',
      gems: '💠',
      pillars: '🏛️',
      fountains: '⛲',
      throne: '🪑',
      crown: '👑',
      chandeliers: '🏮',
      royal_carpet: '🎗️',
    };

    const emoji = elementEmojis[element] || '✨';

    return (
      <span
        key={`${element}-${index}`}
        className="absolute text-2xl opacity-30 animate-float pointer-events-none select-none"
        style={{
          left: `${10 + (index * 20) % 80}%`,
          top: `${10 + (index * 15) % 70}%`,
          animationDelay: `${index * 0.5}s`,
        }}
      >
        {emoji}
      </span>
    );
  };

  const themeElements = elements || CLASSROOM_THEMES[theme]?.name ? [] : [];

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {themeElements.map((element, index) => renderElement(element, index))}
    </div>
  );
};

export function ClassroomBackground({
  classroom,
  theme,
  children,
  className,
  showElements = true,
}: ClassroomBackgroundProps) {
  const activeTheme = classroom?.theme || theme || 'GARDEN';
  const themeInfo = CLASSROOM_THEMES[activeTheme];

  return (
    <div
      className={cn(
        'relative min-h-screen w-full transition-all duration-500',
        getThemeStyles(activeTheme),
        getTextColor(activeTheme),
        className
      )}
      style={classroom?.background_color ? { backgroundColor: classroom.background_color } : undefined}
    >
      {/* Background Image (if available) */}
      {classroom?.background_image_url && (
        <div
          className="absolute inset-0 bg-cover bg-center opacity-20"
          style={{ backgroundImage: `url(${classroom.background_image_url})` }}
        />
      )}

      {/* Decorative Elements */}
      {showElements && (
        <ThemeElements theme={activeTheme} elements={classroom?.elements} />
      )}

      {/* Theme Badge */}
      <div className="absolute top-4 right-4 flex items-center gap-2 bg-white/80 backdrop-blur-sm rounded-full px-3 py-1 shadow-sm">
        <span className="text-lg">{themeInfo?.emoji || '📚'}</span>
        <span className="text-sm font-medium">{classroom?.name || themeInfo?.name || 'Learning Space'}</span>
      </div>

      {/* Main Content */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}

// Simple wrapper without decorative elements
export function ClassroomCard({
  classroom,
  theme,
  children,
  className,
}: Omit<ClassroomBackgroundProps, 'showElements'>) {
  const activeTheme = classroom?.theme || theme || 'GARDEN';
  const themeInfo = CLASSROOM_THEMES[activeTheme];

  return (
    <div
      className={cn(
        'rounded-xl p-4 transition-all duration-300 shadow-md',
        getThemeStyles(activeTheme),
        getTextColor(activeTheme),
        className
      )}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">{themeInfo?.emoji || '📚'}</span>
        <span className="font-semibold">{classroom?.name || themeInfo?.name}</span>
        {classroom?.name_hindi && (
          <span className="text-sm opacity-70">({classroom.name_hindi})</span>
        )}
      </div>
      {children}
    </div>
  );
}

export default ClassroomBackground;
