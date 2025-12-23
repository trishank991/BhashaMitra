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
    padding: string;
    gap: string;
  };
  animations: {
    duration: number;
    bounce: boolean;
  };
  showHindiScript: boolean;
  useSimplifiedUI: boolean;
  maxOptionsPerQuestion: number;
}

const AGE_CONFIGS: Record<AgeVariant, AgeConfig> = {
  junior: {
    variant: 'junior',
    fontSize: {
      heading: 'text-4xl md:text-5xl',
      body: 'text-2xl md:text-3xl',
      small: 'text-xl',
    },
    spacing: {
      padding: 'p-6 md:p-8',
      gap: 'gap-6',
    },
    animations: {
      duration: 0.5,
      bounce: true,
    },
    showHindiScript: false, // Focus on sounds first
    useSimplifiedUI: true,
    maxOptionsPerQuestion: 2,
  },
  standard: {
    variant: 'standard',
    fontSize: {
      heading: 'text-3xl md:text-4xl',
      body: 'text-xl md:text-2xl',
      small: 'text-lg',
    },
    spacing: {
      padding: 'p-4 md:p-6',
      gap: 'gap-4',
    },
    animations: {
      duration: 0.3,
      bounce: true,
    },
    showHindiScript: true,
    useSimplifiedUI: false,
    maxOptionsPerQuestion: 4,
  },
  teen: {
    variant: 'teen',
    fontSize: {
      heading: 'text-2xl md:text-3xl',
      body: 'text-lg md:text-xl',
      small: 'text-base',
    },
    spacing: {
      padding: 'p-4',
      gap: 'gap-3',
    },
    animations: {
      duration: 0.2,
      bounce: false,
    },
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
  const { user } = useAuthStore();

  return useMemo(() => {
    if (!user?.date_of_birth) {
      return AGE_CONFIGS.standard; // Default
    }

    const age = calculateAge(user.date_of_birth);
    const variant = getAgeVariant(age);
    return AGE_CONFIGS[variant];
  }, [user?.date_of_birth]);
}

export function getAgeConfigByAge(age: number): AgeConfig {
  const variant = getAgeVariant(age);
  return AGE_CONFIGS[variant];
}

export default useAgeConfig;
