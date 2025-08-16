// Codex ∞ Service Worker — cache shell + Markdown + API responses
const CACHE = 'codex-cache-v1';
const ASSETS = [
  './',
  'index.html',
  'view.html',
  'go.html',
  'codex_memory_anchor.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
  );
});

// Network-first for GitHub API (keeps manifest fresh), cache-first for everything else
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Only handle GET
  if (e.request.method !== 'GET') return;

  // GitHub API responses (manifest)
  const isAPI = url.hostname === 'api.github.com' && /\/contents\//.test(url.pathname);
  if (isAPI) {
    e.respondWith(
      fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }

  // Markdown and same-origin HTML/JS/CSS/images
  const isMD = url.pathname.endsWith('.md');
  const sameOrigin = url.origin === self.location.origin;

  if (isMD || sameOrigin) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        const fetchAndCache = fetch(e.request).then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        }).catch(() => cached);
        // Prefer cache first for speed; update in background
        return cached || fetchAndCache;
      })
    );
  }
});
