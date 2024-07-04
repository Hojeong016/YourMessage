// service-worker.js

// 캐시 이름 정의
const CACHE_NAME = 'my-pwa-cache';

// 필요한 자원들을 캐싱
const urlsToCache = [
  '/',
  '/index.html',
  '/styles.css',
  '/script.js',
  '/icon-192x192.png',
  '/icon-512x512.png'
];

// 서비스 워커 설치 (웹 페이지와 별개로 실행됨)
self.addEventListener('install', function(event) {
  // 캐시 생성 후 자원 캐싱
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 서비스 워커 활성화
self.addEventListener('activate', function(event) {
  // 오래된 캐시 정리
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName !== CACHE_NAME;
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

// 네트워크 요청을 가로채서 캐시에서 먼저 찾고 없으면 네트워크에서 가져오기
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // 캐시에 맞는 자원 반환
        if (response) {
          return response;
        }

        // 캐시에 없으면 네트워크 요청 처리
        return fetch(event.request);
      })
  );
});
