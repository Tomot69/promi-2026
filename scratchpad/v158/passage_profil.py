import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=sys.argv[1]; MONDES=sys.argv[2].split(',')
ESPION="""()=>{ window.__P={}; window.__on=false; const enveloppe=(o,k,nom)=>{ const f=o[k]; if(typeof f!=='function'||f.__esp) return; const g=function(){ if(!window.__on) return f.apply(this,arguments); const t=performance.now(); try{ return f.apply(this,arguments); } finally { const d=performance.now()-t; const e=window.__P[nom]||(window.__P[nom]=[0,0,0]); e[0]+=d; e[1]++; if(d>e[2]) e[2]=d; } }; g.__esp=1; for(const p in f) try{ g[p]=f[p]; }catch(x){} try{ o[k]=g; }catch(x){} };
  if(window.Toile) Object.keys(window.Toile).forEach(k=>enveloppe(window.Toile,k,'Toile.'+k));
  Object.keys(window).forEach(k=>{ if(/^(_|Toile_|build|paint|render|draw|peint|pose)/.test(k)) { try{ enveloppe(window,k,k); }catch(e){} } });
  const R=window.requestAnimationFrame; window.requestAnimationFrame=function(cb){ return R.call(window, function(t){ if(!window.__on) return cb(t); const a=performance.now(); try{ cb(t); } finally { const d=performance.now()-a; const nom='rAF:'+(cb.name||'anonyme')+':'+String(cb).slice(0,60).replace(/\\s+/g,' '); const e=window.__P[nom]||(window.__P[nom]=[0,0,0]); e[0]+=d; e[1]++; if(d>e[2]) e[2]=d; } }); };
  ['pointermove','touchmove'].forEach(n=>document.addEventListener(n,()=>{},true)); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,F)
    pg.evaluate("()=>{ try{setPremium(true)}catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    c=pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}"); pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(1200)
    pg.evaluate(ESPION)
    vus=[]
    for i in range(22):
        m=pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m in vus: break
        vus.append(m)
        if m in MONDES:
            pg.wait_for_timeout(1500); pg.evaluate("()=>{ window.__P={}; window.__on=true; }"); B.glisse(pg, B.droite([300,300],[80,300],10), pas=18); pg.wait_for_timeout(1400)
            P=pg.evaluate("()=>{ window.__on=false; return Object.entries(window.__P).sort((a,b)=>b[1][0]-a[1][0]).slice(0,7).map(([k,v])=>[k.slice(0,80), Math.round(v[0]), v[1], Math.round(v[2])]); }")
            print('== passage depuis', m); [print('   ', x) for x in P]; continue
            sp=pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
            pg.evaluate("()=>{ window.__P={}; window.__on=true; }"); x,y=sp
            B.glisse(pg, [[x+100*t/20,y] for t in range(21)]+[[x+100-200*t/30,y] for t in range(31)], pas=24); pg.wait_for_timeout(400)
            P=pg.evaluate("()=>{ window.__on=false; return Object.entries(window.__P).sort((a,b)=>b[1][0]-a[1][0]).slice(0,8).map(([k,v])=>[k.slice(0,90), Math.round(v[0]), v[1], Math.round(v[2])]); }")
            print('==', m); [print('   ', x) for x in P]
        B.glisse(pg, B.droite([300,300],[80,300],10), pas=18); pg.wait_for_timeout(1400)
    b.close()
