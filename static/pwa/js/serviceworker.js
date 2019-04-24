var staticCacheName = 'cinemapp-v1';


self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return cache.addAll([
                '/home',
                '/templates/base_cliente.html'
            ]);
        })
    );
});

