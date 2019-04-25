var staticCacheName = "cinemapp-v" + new Date().getTime();;

self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return cache.addAll([
                "/manifest.json",
                "/home",
                "/consultar-saldo",
                "/notificaciones",
                "static/pwa/html/404.html",
                "static/pwa/html/offline.html",
                "/static/bower_components/bootstrap/dist/css/bootstrap.min.css",
                "/static/bower_components/font-awesome/css/font-awesome.min.css",
                "/static/bower_components/Ionicons/css/ionicons.min.css",
                "/static/dist/css/AdminLTE.min.css",
                "/static/dist/css/bootstrap-material-design.min.css",
                "/static/dist/css/ripples.min.css",
                "/static/dist/css/MaterialAdminLTE.min.css",
                "/static/bower_components/jquery/dist/jquery.min.js",
                "/static/bower_components/bootstrap/dist/js/bootstrap.min.js",
                "/static/dist/js/material.min.js",
                "/static/dist/js/ripples.min.js"
            ]);
        })
    );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [staticCacheName];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', event => {
  //console.log('Fetch event for ', event.request.url);
  event.respondWith(
    caches.match(event.request)
    .then(response => {
      if (response) {
        //console.log('Found ', event.request.url, ' in cache');
        return response;
      }
      //console.log('Network request for ', event.request.url);
      return fetch(event.request)
      .then(response => {
        if (response.status === 404) {
          return caches.match('static/pwa/html/404.html');
        }
        return caches.open(staticCacheName)
        .then(cache => {
          cache.put(event.request.url, response.clone());
          return response;
        });
      });
    }).catch(error => {
      //console.log('Error, ', error);
      return caches.match('static/pwa/html/offline.html');
    })
  );
});
