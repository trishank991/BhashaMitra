/**
 * Offline mode types for PWA support
 */

export type PackageType = 'FREE_TIER' | 'LANGUAGE_PACK' | 'CURRICULUM_MODULE' | 'FESTIVAL_PACK';

export type SyncStatus = 'PENDING' | 'SYNCED' | 'FAILED';

export interface OfflinePackage {
  id: string;
  name: string;
  packageType: PackageType;
  language: string;
  version: string;
  sizeMb: number;
  contentManifest: ContentManifest;
  isActive: boolean;
  minAppVersion: string;
  createdAt: string;
  updatedAt: string;
}

export interface ContentManifest {
  stories: string[];
  audioFiles: string[];
  images: string[];
  totalSize: number;
}

export interface ChildOfflineContent {
  id: string;
  childId: string;
  packageId: string;
  package: OfflinePackage;
  downloadedAt: string;
  lastSyncAt: string | null;
  syncStatus: SyncStatus;
  offlineProgress: OfflineProgress;
  storageUsedMb: number;
}

export interface OfflineProgress {
  storiesRead: string[];
  pagesCompleted: Record<string, number[]>;
  pointsEarned: number;
  timeSpentMinutes: number;
}

export interface OfflineState {
  isOnline: boolean;
  downloadedPackages: ChildOfflineContent[];
  availablePackages: OfflinePackage[];
  pendingSync: OfflineProgress[];
  storageUsedMb: number;
  storageQuotaMb: number;
  lastSyncAt: string | null;
  isSyncing: boolean;
  downloadProgress: number;
}

export interface SyncQueueItem {
  id: string;
  type: 'PROGRESS' | 'RECORDING' | 'PREFERENCE';
  data: unknown;
  createdAt: string;
  retryCount: number;
}

export interface ServiceWorkerMessage {
  type: 'SYNC_COMPLETE' | 'DOWNLOAD_PROGRESS' | 'ONLINE_STATUS' | 'CACHE_UPDATE';
  payload: unknown;
}
