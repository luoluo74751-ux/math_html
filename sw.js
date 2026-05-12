const CACHE_NAME = 'kaoyan-math-v2.0.1';
const URLS_TO_CACHE = [
  './',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Main-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Math-Italic.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Size1-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Size2-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Size3-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Size4-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_AMS-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Caligraphic-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Fraktur-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_SansSerif-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Script-Regular.woff2',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/KaTeX_Typewriter-Regular.woff2'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(URLS_TO_CACHE.map(url => cache.add(url).catch(() => {})));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetched = fetch(event.request).then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => cached);
      return cached || fetched;
    })
  );
});
