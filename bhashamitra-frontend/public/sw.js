/**
 * BhashaMitra Service Worker
 * Enables offline functionality and caching for PWA
 */

const CACHE_NAME = 'bhashamitra-v1';
const OFFLINE_CACHE = 'bhashamitra-offline-v1';

// Resources to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png',
];

// API routes that should use network-first strategy
const API_ROUTES = [
  '/api/',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Install complete');
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME && name !== OFFLINE_CACHE)
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Activate complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  // API routes - network first, fall back to cache
  if (API_ROUTES.some((route) => url.pathname.startsWith(route))) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Static assets - cache first
  event.respondWith(cacheFirst(request));
});

// Cache-first strategy
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);

    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    console.error('[SW] Fetch failed:', error);

    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      const offlinePage = await caches.match('/');
      if (offlinePage) {
        return offlinePage;
      }
    }

    throw error;
  }
}

// Network-first strategy
async function networkFirst(request) {
  try {
    const response = await fetch(request);

    // Cache successful API responses
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', request.url);

    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }

    throw error;
  }
}

// Background sync for offline progress
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-progress') {
    event.waitUntil(syncProgress());
  }
});

async function syncProgress() {
  console.log('[SW] Syncing offline progress');

  // Get pending sync data from IndexedDB
  // This will be implemented with the offline store

  // Notify clients that sync is complete
  const clients = await self.clients.matchAll();
  clients.forEach((client) => {
    client.postMessage({
      type: 'SYNC_COMPLETE',
      payload: { timestamp: new Date().toISOString() },
    });
  });
}

// Push notification handler
self.addEventListener('push', (event) => {
  if (!event.data) return;

  const data = event.data.json();

  const options = {
    body: data.body,
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/',
    },
    actions: data.actions || [],
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  const url = event.notification.data?.url || '/';

  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clients) => {
      // Focus existing window if available
      for (const client of clients) {
        if (client.url === url && 'focus' in client) {
          return client.focus();
        }
      }
      // Open new window
      if (self.clients.openWindow) {
        return self.clients.openWindow(url);
      }
    })
  );
});

// Message handler for communication with main app
self.addEventListener('message', (event) => {
  const { type, payload } = event.data || {};

  switch (type) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;

    case 'CACHE_CONTENT':
      cacheContent(payload);
      break;

    case 'CLEAR_CACHE':
      clearCache(payload);
      break;

    default:
      console.log('[SW] Unknown message type:', type);
  }
});

// Cache offline content packages
async function cacheContent(manifest) {
  const cache = await caches.open(OFFLINE_CACHE);

  const urls = [
    ...manifest.stories,
    ...manifest.audioFiles,
    ...manifest.images,
  ];

  let cached = 0;

  for (const url of urls) {
    try {
      await cache.add(url);
      cached++;

      // Report progress
      const clients = await self.clients.matchAll();
      clients.forEach((client) => {
        client.postMessage({
          type: 'DOWNLOAD_PROGRESS',
          payload: { cached, total: urls.length },
        });
      });
    } catch (error) {
      console.error('[SW] Failed to cache:', url, error);
    }
  }
}

// Clear specific cache entries
async function clearCache(packageId) {
  const cache = await caches.open(OFFLINE_CACHE);
  const keys = await cache.keys();

  for (const request of keys) {
    if (request.url.includes(packageId)) {
      await cache.delete(request);
    }
  }
}
