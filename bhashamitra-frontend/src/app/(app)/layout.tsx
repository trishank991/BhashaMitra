import { ReactNode } from 'react';

/**
 * App layout - full application layout for authenticated users.
 * Individual pages use MainLayout component for header, bottom nav, and Peppi chat.
 */
export default function AppLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
