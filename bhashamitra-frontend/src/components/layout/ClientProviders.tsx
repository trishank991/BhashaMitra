'use client';

import { ReactNode } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AgeThemeProvider } from './AgeThemeProvider';

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';

export function ClientProviders({ children }: { children: ReactNode }) {
  // Only wrap with GoogleOAuthProvider if client ID is configured
  const content = <AgeThemeProvider>{children}</AgeThemeProvider>;

  if (GOOGLE_CLIENT_ID) {
    return (
      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        {content}
      </GoogleOAuthProvider>
    );
  }

  return content;
}
