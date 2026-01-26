'use client';

import { useParams } from 'next/navigation';
import { useAuthStore } from '@/stores';
import { ChildProfile } from '@/types';

interface UseChildResult {
  child: ChildProfile | null;
  childId: string | null;
  isLoading: boolean;
}

/**
 * Hook that provides the active child context.
 * Reads optional childId from URL params, falls back to activeChild from Zustand store.
 * This enables hybrid routing where childId can come from URL or context.
 */
export function useChild(): UseChildResult {
  const params = useParams();
  const { activeChild, children, isLoading } = useAuthStore();

  // Check for childId in URL params (hybrid routing support)
  const urlChildId = params?.childId as string | undefined;

  if (urlChildId) {
    // Find child by URL param
    const urlChild = children.find(c => c.id === urlChildId) || null;
    return {
      child: urlChild || activeChild,
      childId: urlChildId,
      isLoading,
    };
  }

  // Fall back to Zustand activeChild
  return {
    child: activeChild,
    childId: activeChild?.id || null,
    isLoading,
  };
}
