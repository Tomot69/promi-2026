# WebKit : la plus longue image après l'ouverture d'une Nuée, et les rendus de dalle (appelant, durée) qui y tombent.
import sys
from playwright.sync_api import sync_playwright
POSE=r"""()=>{ window.__D=[]; const d=Toile.dalleTrame; Toile.dalleTrame=function(cv,id,k){ const t=performance.now(); const x=d.apply(this,arguments);
   const st=(new Error().stack||'').split('\n').slice(1,5).map(s=>{const m=s.match(/(\w[\w$.]*)?@.*?:(\d+):\d+/); return m?((m[1]||'?')+':'+m[2]):'';}).join(' < ');
   window.__D.push([Math.round(t-window.__t0), Math.round(performance.now()-t), id, cv.width+'x'+cv.height, st]); return x; };
 window.__N=[]; ['_ficheNuee','_ficheTout','_fichePose','_ficheDalle','peintMinis','dpRefresh','openNueeDetail','openEssaim','renderNueeDetail','closeAll','_nueePeaufiner'].forEach(function(n){ const f=window[n]; if(typeof f!=='function') return; window[n]=function(){ const t=performance.now(); const r=f.apply(this,arguments); window.__N.push([n,Math.round(t-(window.__t0||0)),Math.round(performance.now()-t)]); return r; }; }); }"""
SUIT=r"""()=>new Promise(res=>{ window.__t0=performance.now(); window.__N=[]; const F=[]; let k=null; for(const q in NUE){k=q;break;} closeAll(); openNueeDetail(k);
  let prev=performance.now(); (function f(){ const t=performance.now(); F.push([Math.round(prev-window.__t0), Math.round(t-prev)]); prev=t; if(t-window.__t0<3500) requestAnimationFrame(f); else res(F); })(); })"""
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(2500)
    pg.evaluate(POSE); F=pg.evaluate(SUIT); D=pg.evaluate("()=>window.__D")
    F=sorted(F,key=lambda x:-x[1])[:2]
    for a,dur in F:
        dd=[x for x in D if a<=x[0]<=a+dur]
        print('image de %d ms à %d : %d rendus, %d ms de rendu' % (dur,a,len(dd),sum(x[1] for x in dd)))
        for x in dd: print('    ',x)
        NN=pg.evaluate("()=>window.__N"); print('    fonctions dans cette image :', [n for n in NN if a<=n[1]<=a+dur])
    N=pg.evaluate("()=>window.__N")
    import collections; c=collections.defaultdict(lambda:[0,0])
    for n,a,d in N: c[n][0]+=1; c[n][1]+=d
    print('appels :', dict(c)); print('les plus longs :', sorted(N,key=lambda x:-x[2])[:8])
    b.close()
