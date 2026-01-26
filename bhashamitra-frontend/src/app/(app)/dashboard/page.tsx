'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

/**
 * Dashboard page - redirects to /home for now.
 * In the future, this can be expanded to show a multi-child dashboard.
 */
export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/home');
  }, [router]);

  return null;
}
