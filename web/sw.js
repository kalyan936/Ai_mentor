// AI Mentor - Service Worker for PWA (v2)
const CACHE_NAME = 'ai-mentor-v2';
const ASSETS = [
    './',
    './index.html',
    './css/style.css',
    './js/data.js',
    './js/db.js',
    './js/llm.js',
    './js/agents.js',
    './js/components.js',
    './js/app.js',
    './manifest.json',
];

self.addEventListener('install', (event) => {
    event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))));
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('api-inference') || event.request.url.includes('deepseek')) {
        event.respondWith(fetch(event.request));
        return;
    }
    event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request)));
});
