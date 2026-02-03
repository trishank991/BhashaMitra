import { ReactNode } from 'react';

/**
 * Marketing layout - clean layout without bottom nav for public pages.
 * Used for: landing page, pricing, terms, privacy, help, etc.
 */
export default function MarketingLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
