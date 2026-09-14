const CACHE='sa-u9-nationals-v5';
const CORE=['./','./index.html','./styles.css?v=5','./app.js?v=5','./app-data.js?v=5','./manifest.webmanifest','./assets/sa-u9-home-hero.png','./assets/sa-u9-team-header.png','./assets/nationals-2026-header.png','./assets/app-icon-192.png','./assets/app-icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request,{cache:'no-store'}).then(r=>{const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r}).catch(()=>caches.match(e.request)))});
