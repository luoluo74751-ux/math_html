var C='kmath-v4';

self.addEventListener('install',function(e){
  e.waitUntil(
    caches.open(C).then(function(c){
      return c.addAll([
        '考研数学练卡_v4.html',
        'manifest.json',
        'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
        'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'
      ]);
    }).then(function(){return self.skipWaiting()})
  );
});

self.addEventListener('activate',function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.filter(function(k){return k!==C}).map(function(k){return caches.delete(k)}));
    }).then(function(){return self.clients.claim()})
  );
});

self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;

  e.respondWith(
    caches.match(e.request).then(function(hit){
      if(hit)return hit;

      return fetch(e.request).then(function(res){
        if(res&&res.status===200){
          var r2=res.clone();
          caches.open(C).then(function(c){c.put(e.request,r2)});
        }
        return res;
      }).catch(function(){
        // Offline fallback for page navigations
        if(e.request.mode==='navigate'||e.request.destination==='document'){
          return caches.match('考研数学练卡_v4.html');
        }
        return new Response('',{status:504});
      });
    })
  );
});
