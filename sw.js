var C='kaoyan-v2';

self.addEventListener('install',function(e){
  e.waitUntil(
    caches.open(C).then(function(c){
      return c.addAll([
        './',
        '考研数学练卡_v4.html',
        'manifest.json',
        'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
        'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
        'https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap'
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){return k!==C}).map(function(k){return caches.delete(k)}));
  }));
  self.clients.claim();
});

self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;
  e.respondWith(
    caches.match(e.request).then(function(r){
      if(r)return r;
      return fetch(e.request).then(function(res){
        if(res&&res.status===200){
          var clone=res.clone();
          caches.open(C).then(function(c){c.put(e.request,clone)});
        }
        return res;
      }).catch(function(){
        return new Response('离线模式 - 请联网后重试',{status:503});
      });
    })
  );
});
