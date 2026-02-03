'use client';

import { ReactNode } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AgeThemeProvider } from './AgeThemeProvider';

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';

export function ClientProviders({ children }: { children: ReactNode }) {
  // Always wrap with GoogleOAuthProvider to avoid "components used outside provider" errors
  // When no client ID is provided, use a placeholder (auth will fail gracefully)
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID || 'placeholder-client-id'}>
      <AgeThemeProvider>{children}</AgeThemeProvider>
    </GoogleOAuthProvider>
  );
}
