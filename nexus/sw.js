// NEXUS Command Center - Service Worker
// Enables offline functionality and caching

const CACHE_NAME = 'nexus-v2.0';
const CACHE_URLS = [
  '/nexus/index.html',
  '/nexus/manifest.json',
  '/nexus/projects.json'
];

// Install event - cache core assets
self.addEventListener('install', (event) => {
  console.log('[NEXUS SW] Installing service worker...');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[NEXUS SW] Caching core assets');
        return cache.addAll(CACHE_URLS);
      })
      .then(() => {
        console.log('[NEXUS SW] Installation complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[NEXUS SW] Installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[NEXUS SW] Activating service worker...');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => {
              console.log('[NEXUS SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[NEXUS SW] Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip external requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Return cached version if available
        if (cachedResponse) {
          console.log('[NEXUS SW] Serving from cache:', event.request.url);

          // Fetch in background to update cache
          fetch(event.request)
            .then((response) => {
              if (response && response.status === 200) {
                caches.open(CACHE_NAME)
                  .then((cache) => cache.put(event.request, response));
              }
            })
            .catch(() => {});

          return cachedResponse;
        }

        // Otherwise fetch from network
        console.log('[NEXUS SW] Fetching from network:', event.request.url);
        return fetch(event.request)
          .then((response) => {
            // Cache successful responses
            if (response && response.status === 200) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => cache.put(event.request, responseClone));
            }
            return response;
          })
          .catch((error) => {
            console.error('[NEXUS SW] Fetch failed:', error);

            // Return offline fallback for HTML requests
            if (event.request.headers.get('accept').includes('text/html')) {
              return new Response(
                `<!DOCTYPE html>
                <html>
                <head>
                  <title>NEXUS - Offline</title>
                  <style>
                    body {
                      background: #0a0a0f;
                      color: #00d4ff;
                      font-family: 'Courier New', monospace;
                      display: flex;
                      justify-content: center;
                      align-items: center;
                      height: 100vh;
                      margin: 0;
                      text-align: center;
                    }
                    .container { padding: 2rem; }
                    h1 { font-size: 2rem; margin-bottom: 1rem; }
                    p { opacity: 0.7; }
                    .pulse {
                      animation: pulse 2s infinite;
                    }
                    @keyframes pulse {
                      0%, 100% { opacity: 0.5; }
                      50% { opacity: 1; }
                    }
                  </style>
                </head>
                <body>
                  <div class="container">
                    <h1 class="pulse">◉ NEXUS OFFLINE</h1>
                    <p>Connection to command center lost.</p>
                    <p>Attempting to reconnect...</p>
                  </div>
                </body>
                </html>`,
                {
                  headers: { 'Content-Type': 'text/html' }
                }
              );
            }

            throw error;
          });
      })
  );
});

// Handle messages from the main app
self.addEventListener('message', (event) => {
  console.log('[NEXUS SW] Received message:', event.data);

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'CACHE_URLS') {
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(event.data.urls))
      .then(() => {
        event.ports[0].postMessage({ status: 'cached' });
      });
  }
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('[NEXUS SW] Background sync:', event.tag);

  if (event.tag === 'sync-activity') {
    event.waitUntil(syncActivity());
  }
});

async function syncActivity() {
  // Sync any queued activity when back online
  const db = await openActivityDB();
  const pending = await db.getAll('pending');

  for (const item of pending) {
    try {
      // Send to server when implemented
      console.log('[NEXUS SW] Syncing activity:', item);
      await db.delete('pending', item.id);
    } catch (error) {
      console.error('[NEXUS SW] Sync failed for:', item);
    }
  }
}

// Simple IndexedDB wrapper for offline activity storage
function openActivityDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('nexus-activity', 1);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const db = request.result;
      resolve({
        getAll: (store) => new Promise((res, rej) => {
          const tx = db.transaction(store, 'readonly');
          const req = tx.objectStore(store).getAll();
          req.onsuccess = () => res(req.result);
          req.onerror = () => rej(req.error);
        }),
        delete: (store, key) => new Promise((res, rej) => {
          const tx = db.transaction(store, 'readwrite');
          const req = tx.objectStore(store).delete(key);
          req.onsuccess = () => res();
          req.onerror = () => rej(req.error);
        }),
        add: (store, item) => new Promise((res, rej) => {
          const tx = db.transaction(store, 'readwrite');
          const req = tx.objectStore(store).add(item);
          req.onsuccess = () => res(req.result);
          req.onerror = () => rej(req.error);
        })
      });
    };

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('pending')) {
        db.createObjectStore('pending', { keyPath: 'id', autoIncrement: true });
      }
      if (!db.objectStoreNames.contains('activity')) {
        db.createObjectStore('activity', { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}

// Push notification handling (for future use)
self.addEventListener('push', (event) => {
  console.log('[NEXUS SW] Push received:', event);

  const options = {
    body: event.data ? event.data.text() : 'NEXUS has an update',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect fill="%230a0a0f" width="64" height="64" rx="8"/><circle cx="32" cy="32" r="20" fill="none" stroke="%2300d4ff" stroke-width="2"/><circle cx="32" cy="32" r="8" fill="%2300d4ff"/></svg>',
    badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle fill="%2300d4ff" cx="12" cy="12" r="12"/></svg>',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      { action: 'view', title: 'View' },
      { action: 'dismiss', title: 'Dismiss' }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('NEXUS Command Center', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('[NEXUS SW] Notification clicked:', event.action);

  event.notification.close();

  if (event.action === 'view' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' })
        .then((clientList) => {
          // Focus existing window if open
          for (const client of clientList) {
            if (client.url.includes('/nexus/') && 'focus' in client) {
              return client.focus();
            }
          }
          // Otherwise open new window
          if (clients.openWindow) {
            return clients.openWindow('/nexus/index.html');
          }
        })
    );
  }
});

console.log('[NEXUS SW] Service worker loaded');
