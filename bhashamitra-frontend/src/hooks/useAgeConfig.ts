'use client';

import { useMemo } from 'react';
import { useAuthStore } from '@/stores';
import { calculateAge } from '@/lib/utils';

export type AgeVariant = 'junior' | 'standard' | 'teen';

interface AgeConfig {
  variant: AgeVariant;
  fontSize: {
    heading: string;
    body: string;
    small: string;
  };
  spacing: {
    gap: string;
    padding: string;
  };
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
  };
  animations: {
    duration: number;
    bounce: boolean;
    particles: boolean;
  };
  content: {
    showRomanization: boolean;
    showHindiScript: boolean;
    showMeaning: boolean;
    showExamples: boolean;
  };
  game: {
    maxOptionsPerQuestion: number;
    timeLimit: number; // 0 for no limit
    hintsEnabled: boolean;
    difficultyMultiplier: number;
  };
  peppi: {
    size: 'sm' | 'md' | 'lg';
    frequency: 'low' | 'medium' | 'high'; // How often Peppi appears
    voicePitch: number; // 0.8 for slower/younger, 1.2 for faster/older
  };
  // Legacy properties for backward compatibility
  showHindiScript: boolean;
  useSimplifiedUI: boolean;
  maxOptionsPerQuestion: number;
}

const AGE_CONFIGS: Record<AgeVariant, AgeConfig> = {
  junior: {
    variant: 'junior',
    fontSize: { heading: 'text-3xl', body: 'text-xl', small: 'text-lg' },
    spacing: { gap: 'gap-6', padding: 'p-6' },
    colors: {
      primary: 'from-pink-400 to-purple-400',
      secondary: 'from-yellow-300 to-orange-300',
      accent: 'text-pink-500',
      background: 'bg-gradient-to-b from-pink-50 to-purple-50',
    },
    animations: { duration: 0.5, bounce: true, particles: true },
    content: {
      showRomanization: true,
      showHindiScript: true,
      showMeaning: true,
      showExamples: false,
    },
    game: {
      maxOptionsPerQuestion: 3,
      timeLimit: 0,
      hintsEnabled: true,
      difficultyMultiplier: 0.7,
    },
    peppi: { size: 'lg', frequency: 'high', voicePitch: 0.9 },
    // Legacy properties
    showHindiScript: true,
    useSimplifiedUI: true,
    maxOptionsPerQuestion: 3,
  },
  standard: {
    variant: 'standard',
    fontSize: { heading: 'text-2xl', body: 'text-lg', small: 'text-base' },
    spacing: { gap: 'gap-4', padding: 'p-4' },
    colors: {
      primary: 'from-blue-400 to-indigo-400',
      secondary: 'from-green-300 to-teal-300',
      accent: 'text-blue-500',
      background: 'bg-gradient-to-b from-blue-50 to-indigo-50',
    },
    animations: { duration: 0.3, bounce: true, particles: true },
    content: {
      showRomanization: true,
      showHindiScript: true,
      showMeaning: true,
      showExamples: true,
    },
    game: {
      maxOptionsPerQuestion: 4,
      timeLimit: 0,
      hintsEnabled: true,
      difficultyMultiplier: 1.0,
    },
    peppi: { size: 'md', frequency: 'medium', voicePitch: 1.0 },
    // Legacy properties
    showHindiScript: true,
    useSimplifiedUI: false,
    maxOptionsPerQuestion: 4,
  },
  teen: {
    variant: 'teen',
    fontSize: { heading: 'text-xl', body: 'text-base', small: 'text-sm' },
    spacing: { gap: 'gap-3', padding: 'p-3' },
    colors: {
      primary: 'from-slate-500 to-gray-600',
      secondary: 'from-emerald-400 to-cyan-400',
      accent: 'text-emerald-500',
      background: 'bg-gradient-to-b from-slate-50 to-gray-100',
    },
    animations: { duration: 0.2, bounce: false, particles: false },
    content: {
      showRomanization: true,
      showHindiScript: true,
      showMeaning: true,
      showExamples: true,
    },
    game: {
      maxOptionsPerQuestion: 4,
      timeLimit: 60,
      hintsEnabled: false,
      difficultyMultiplier: 1.3,
    },
    peppi: { size: 'sm', frequency: 'low', voicePitch: 1.1 },
    // Legacy properties
    showHindiScript: true,
    useSimplifiedUI: false,
    maxOptionsPerQuestion: 4,
  },
};

function getAgeVariant(age: number): AgeVariant {
  if (age <= 6) return 'junior';
  if (age <= 10) return 'standard';
  return 'teen';
}

export function useAgeConfig(): AgeConfig {
  const { activeChild } = useAuthStore();

  return useMemo(() => {
    if (!activeChild?.date_of_birth) {
      // If no date_of_birth, use age field if available
      if (activeChild?.age) {
        const variant = getAgeVariant(activeChild.age);
        return AGE_CONFIGS[variant];
      }
      return AGE_CONFIGS.standard; // Default
    }

    const age = calculateAge(activeChild.date_of_birth);
    const variant = getAgeVariant(age);
    return AGE_CONFIGS[variant];
  }, [activeChild?.date_of_birth, activeChild?.age]);
}

export function getAgeConfigByAge(age: number): AgeConfig {
  const variant = getAgeVariant(age);
  return AGE_CONFIGS[variant];
}

export default useAgeConfig;
