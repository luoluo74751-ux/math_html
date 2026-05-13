const CACHE = 'math-v9';
const SHELL_KEY = '/__shell__';

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
        if (cached) {
          // Background refresh
          fetch(event.request).then((res) => {
            if (res && res.status === 200) {
              cache.put(event.request, res.clone());
            }
          }).catch(() => {});
          return cached;
        }

        // Not cached, try network
        return fetch(event.request).then((res) => {
          if (res && res.status === 200) {
            cache.put(event.request, res.clone());
            if (event.request.mode === 'navigate') {
              cache.put(new Request(SHELL_KEY), res.clone());
            }
          }
          return res;
        }).catch(() => {
          if (event.request.mode === 'navigate') {
            return cache.match(SHELL_KEY).then((r) => {
              return r || new Response('需要联网加载，请连接网络后打开', {
                status: 503,
                headers: { 'Content-Type': 'text/plain; charset=utf-8' }
              });
            });
          }
          return new Response('', { status: 408 });
        });
      });
    })
  );
});
