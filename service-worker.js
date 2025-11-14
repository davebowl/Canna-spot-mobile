self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('cannaspot-mobile').then(function(cache) {
      return cache.addAll([
        'index.html',
        'manifest.json',
        'icon-192.png',
        'icon-512.png'
      ]);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});

self.addEventListener('push', function(event) {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title || 'CannaSpot', {
      body: data.body || 'You have a new notification!',
      icon: 'icon-192.png',
      badge: 'icon-192.png'
    })
  );
});
