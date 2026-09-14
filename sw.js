const CACHE = 'sa-u9-nationals-v2';
const ASSETS = ['./','./index.html','./styles.css','./app.js','./app-data.js','./manifest.webmanifest','./assets/nationals-logo.jpeg','./assets/u9-team-art.jpeg','./assets/u9-roster.jpeg','./assets/nationals-poster.jpeg'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => { if (e.request.method !== 'GET') return; e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request))); });
