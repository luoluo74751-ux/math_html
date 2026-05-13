const CACHE = 'math-v8';
const SHELL_KEY = '/__app_shell__';

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.open(CACHE).then((cache) => {
      return cache.match(event.request).then((cached) => {
        const net = fetch(event.request)
          .then((res) => {
            if (res && res.status === 200) {
              cache.put(event.request, res.clone());
              // Also cache navigations under a fixed key for offline fallback
              if (event.request.mode === 'navigate') {
                const shellRes = res.clone();
                cache.put(new Request(SHELL_KEY), shellRes);
              }
            }
            return res;
          })
          .catch(() => null);

        if (cached) return cached;
        if (event.request.mode === 'navigate') {
          return net.catch(() => cache.match(SHELL_KEY));
        }
        return net;
      });
    })
  );
});
