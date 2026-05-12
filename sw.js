var CACHE='kmath-v3';

var PRELOAD=[
  './',
  '考研数学练卡_v4.html',
  'manifest.json',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
  'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'
];

self.addEventListener('install',function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){
      return Promise.allSettled(PRELOAD.map(function(u){return c.add(u).catch(function(){})}));
    }).then(function(){return self.skipWaiting()})
  );
});

self.addEventListener('activate',function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.filter(function(k){return k!==CACHE}).map(function(k){return caches.delete(k)}));
    }).then(function(){return self.clients.claim()})
  );
});

self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;
  e.respondWith(
    caches.match(e.request).then(function(hit){
      if(hit)return hit;
      return fetch(e.request).then(function(res){
        if(!res||res.status!==200)return res;
        var r2=res.clone();
        caches.open(CACHE).then(function(c){c.put(e.request,r2)});
        return res;
      }).catch(function(){
        if(e.request.mode==='navigate'){
          return caches.match('考研数学练卡_v4.html').then(function(r){return r||caches.match('./')});
        }
        return new Response('',{status:408});
      });
    })
  );
});
