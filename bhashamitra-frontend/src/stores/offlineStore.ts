/**
 * Offline mode store for PWA support
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  OfflinePackage,
  ChildOfflineContent,
  OfflineProgress,
  SyncQueueItem,
} from '@/types/offline';

interface OfflineState {
  // State
  isOnline: boolean;
  downloadedPackages: ChildOfflineContent[];
  availablePackages: OfflinePackage[];
  syncQueue: SyncQueueItem[];
  storageUsedMb: number;
  storageQuotaMb: number;
  lastSyncAt: string | null;
  isSyncing: boolean;
  isDownloading: boolean;
  downloadProgress: number;
  currentDownloadPackage: string | null;

  // Actions
  setOnlineStatus: (isOnline: boolean) => void;
  fetchAvailablePackages: (language: string) => Promise<void>;
  downloadPackage: (packageId: string, childId: string) => Promise<boolean>;
  deletePackage: (contentId: string) => Promise<boolean>;
  addToSyncQueue: (item: Omit<SyncQueueItem, 'id' | 'createdAt' | 'retryCount'>) => void;
  syncProgress: () => Promise<boolean>;
  getOfflineProgress: (childId: string) => OfflineProgress | null;
  updateOfflineProgress: (childId: string, progress: Partial<OfflineProgress>) => void;
  checkStorageQuota: () => Promise<void>;
}

export const useOfflineStore = create<OfflineState>()(
  persist(
    (set, get) => ({
      // Initial state
      isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
      downloadedPackages: [],
      availablePackages: [],
      syncQueue: [],
      storageUsedMb: 0,
      storageQuotaMb: 500, // Default 500MB quota
      lastSyncAt: null,
      isSyncing: false,
      isDownloading: false,
      downloadProgress: 0,
      currentDownloadPackage: null,

      setOnlineStatus: (isOnline: boolean) => {
        set({ isOnline });

        // Auto-sync when coming back online
        if (isOnline && get().syncQueue.length > 0) {
          get().syncProgress();
        }
      },

      fetchAvailablePackages: async (language: string) => {
        // TODO: Implement API call when backend endpoint is ready
        // For now, return mock data
        const mockPackages: OfflinePackage[] = [
          {
            id: 'free-tier-hindi',
            name: 'Hindi Starter Pack',
            packageType: 'FREE_TIER',
            language: 'HINDI',
            version: '1.0.0',
            sizeMb: 50,
            contentManifest: { stories: [], audioFiles: [], images: [], totalSize: 50 },
            isActive: true,
            minAppVersion: '1.0.0',
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          },
        ];

        set({ availablePackages: mockPackages.filter(p => p.language === language || p.packageType === 'FREE_TIER') });
      },

      downloadPackage: async (packageId: string, childId: string) => {
        const pkg = get().availablePackages.find(p => p.id === packageId);
        if (!pkg) return false;

        set({ isDownloading: true, downloadProgress: 0, currentDownloadPackage: packageId });

        try {
          // Simulate download progress
          for (let i = 0; i <= 100; i += 10) {
            await new Promise(resolve => setTimeout(resolve, 200));
            set({ downloadProgress: i });
          }

          // Add to downloaded packages
          const content: ChildOfflineContent = {
            id: `${childId}-${packageId}`,
            childId,
            packageId,
            package: pkg,
            downloadedAt: new Date().toISOString(),
            lastSyncAt: null,
            syncStatus: 'SYNCED',
            offlineProgress: {
              storiesRead: [],
              pagesCompleted: {},
              pointsEarned: 0,
              timeSpentMinutes: 0,
            },
            storageUsedMb: pkg.sizeMb,
          };

          set(state => ({
            downloadedPackages: [...state.downloadedPackages, content],
            storageUsedMb: state.storageUsedMb + pkg.sizeMb,
            isDownloading: false,
            downloadProgress: 100,
            currentDownloadPackage: null,
          }));

          return true;
        } catch {
          set({ isDownloading: false, downloadProgress: 0, currentDownloadPackage: null });
          return false;
        }
      },

      deletePackage: async (contentId: string) => {
        const content = get().downloadedPackages.find(p => p.id === contentId);
        if (!content) return false;

        set(state => ({
          downloadedPackages: state.downloadedPackages.filter(p => p.id !== contentId),
          storageUsedMb: Math.max(0, state.storageUsedMb - content.storageUsedMb),
        }));

        return true;
      },

      addToSyncQueue: (item) => {
        const queueItem: SyncQueueItem = {
          ...item,
          id: crypto.randomUUID(),
          createdAt: new Date().toISOString(),
          retryCount: 0,
        };

        set(state => ({
          syncQueue: [...state.syncQueue, queueItem],
        }));
      },

      syncProgress: async () => {
        if (!get().isOnline || get().isSyncing) return false;

        set({ isSyncing: true });

        try {
          const queue = get().syncQueue;

          for (const item of queue) {
            // TODO: Implement actual API sync when backend endpoint is ready
            void item;
          }

          set({
            syncQueue: [],
            lastSyncAt: new Date().toISOString(),
            isSyncing: false,
          });

          // Update sync status on all packages
          set(state => ({
            downloadedPackages: state.downloadedPackages.map(p => ({
              ...p,
              syncStatus: 'SYNCED' as const,
              lastSyncAt: new Date().toISOString(),
            })),
          }));

          return true;
        } catch {
          set({ isSyncing: false });
          return false;
        }
      },

      getOfflineProgress: (childId: string) => {
        const content = get().downloadedPackages.find(p => p.childId === childId);
        return content?.offlineProgress || null;
      },

      updateOfflineProgress: (childId: string, progress: Partial<OfflineProgress>) => {
        set(state => ({
          downloadedPackages: state.downloadedPackages.map(p => {
            if (p.childId !== childId) return p;

            return {
              ...p,
              syncStatus: 'PENDING' as const,
              offlineProgress: { ...p.offlineProgress, ...progress },
            };
          }),
        }));

        // Add to sync queue
        get().addToSyncQueue({
          type: 'PROGRESS',
          data: { childId, progress },
        });
      },

      checkStorageQuota: async () => {
        if (typeof navigator !== 'undefined' && 'storage' in navigator) {
          try {
            const estimate = await navigator.storage.estimate();
            const quotaMb = Math.round((estimate.quota || 0) / (1024 * 1024));
            const usedMb = Math.round((estimate.usage || 0) / (1024 * 1024));

            set({
              storageQuotaMb: quotaMb,
              storageUsedMb: usedMb,
            });
          } catch {
            // Storage quota check failed - continue with default values
          }
        }
      },
    }),
    {
      name: 'bhashamitra-offline',
      partialize: (state) => ({
        downloadedPackages: state.downloadedPackages,
        syncQueue: state.syncQueue,
        lastSyncAt: state.lastSyncAt,
      }),
    }
  )
);

// Set up online/offline listeners
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => {
    useOfflineStore.getState().setOnlineStatus(true);
  });

  window.addEventListener('offline', () => {
    useOfflineStore.getState().setOnlineStatus(false);
  });
}
