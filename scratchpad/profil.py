#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
JS=r"""(ms)=>new Promise(res=>{
  const T={masse:[],noms:[],traces:[],degage:[],pose:[]};
  const w=(nom,f)=>function(){const a=performance.now();const r=f.apply(this,arguments);
    T[nom].push(performance.now()-a);return r;};
  window.dessineMasse=w('masse',window.dessineMasse);
  window.placeNoms=w('noms',window.placeNoms);
  window.dessineTraces=w('traces',window.dessineTraces);
  window.degageNoms=w('degage',window.degageNoms);
  const op=window.orbitePose; window.orbitePose=w('pose',op);
  const t0=performance.now();
  (function tick(){ if(performance.now()-t0<ms) requestAnimationFrame(tick);
    else { const st=a=>a.length?{n:a.length,moy:+(a.reduce((x,y)=>x+y,0)/a.length).toFixed(2),
             max:+Math.max.apply(null,a).toFixed(2)}:null;
      res({masse:st(T.masse),noms:st(T.noms),traces:st(T.traces),degage:st(T.degage),pose:st(T.pose)});}})();
})"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':1000}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-SPHERE.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=120000); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.querySelectorAll('figure').forEach((f,i)=>{if(i>0)f.remove();});}")
    pg.wait_for_timeout(500)
    for k,v in pg.evaluate(JS,5000).items(): print('  %-8s %s'%(k,v))
    b.close()
