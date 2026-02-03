import { ReactNode } from 'react';

/**
 * Auth layout - minimal centered layout for authentication pages.
 * Used for: login, register, onboarding, forgot-password, reset-password, verify-email
 */
export default function AuthLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
