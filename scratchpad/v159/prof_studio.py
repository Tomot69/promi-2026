import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
PIEGE="""()=>{ window.__T={}; const W=(o,n,lab)=>{ const f=o[n]; if(typeof f!=='function'||f.__p) return; const g=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally{ const d=performance.now()-t; const e=window.__T[lab]||(window.__T[lab]=[0,0,0]); e[0]++; e[1]+=d; e[2]=Math.max(e[2],d); } }; g.__p=1; Object.keys(f).forEach(k=>{try{g[k]=f[k]}catch(_){}}); o[n]=g; };
  ['auTrame','ixTrame','shTrame','csDalles','shFond','fdRefresh','stRefresh','dpRefresh','esRefresh','peintMinis','_trameReglages','promiTrame','_paintBuyBg','_placeLockCard','render','buildStudio','syncAll','_rendDalle','toast'].forEach(n=>W(window,n,n));
  ['setTheme','setPalette','setHue','repaintWorld','repaint','preview','apercuImage','apercuPrepare','apercuPrepareProchain','apercuCompose','renderTo','dalleTrame','sync'].forEach(n=>W(window.Toile,n,'Toile.'+n));
  window.__G=[]; let av=performance.now(); (function f(t){ if(window.__on) window.__G.push(Math.round(t-av)); av=t; requestAnimationFrame(f); })(performance.now()); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,F); pg.wait_for_timeout(int(sys.argv[2]) if len(sys.argv)>2 else 0)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3500)
    pg.evaluate(PIEGE); pg.evaluate("()=>{window.__on=true}")
    seq=[]
    for i in range(10):
        B.glisse(pg, B.droite([300,420],[90,420],10), pas=16); pg.wait_for_timeout(1600); seq.append(pg.evaluate("()=>Toile.getTheme()"))
    pg.evaluate("()=>{window.__on=false}")
    T=pg.evaluate("()=>window.__T"); G=pg.evaluate("()=>window.__G")
    print('mondes', seq)
    for k,v in sorted(T.items(), key=lambda kv:-kv[1][1]): print('%-28s n %4d  total %7.0f ms  max %6.0f ms' % (k, v[0], v[1], v[2]))
    G2=sorted(G); print('images', len(G), 'p50', G2[len(G2)//2], 'p95', G2[int(len(G2)*.95)], '>50 ms', sum(1 for x in G if x>50), 'max', max(G))
    b.close()
