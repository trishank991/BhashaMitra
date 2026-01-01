'use client';

import { createContext, useContext, ReactNode } from 'react';
import { useAgeConfig } from '@/hooks/useAgeConfig';

const AgeThemeContext = createContext<ReturnType<typeof useAgeConfig> | null>(null);

export function AgeThemeProvider({ children }: { children: ReactNode }) {
  const ageConfig = useAgeConfig();

  return (
    <AgeThemeContext.Provider value={ageConfig}>
      <div className={ageConfig.colors.background}>
        {children}
      </div>
    </AgeThemeContext.Provider>
  );
}

export function useAgeTheme() {
  const context = useContext(AgeThemeContext);
  if (!context) {
    throw new Error('useAgeTheme must be used within AgeThemeProvider');
  }
  return context;
}
