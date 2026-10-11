import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
OU=open('redteam_deplace.py',encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for k in range(3):
        ctx=B.contexte(b); pg=B.ouvre(ctx,F); B.plante(pg,'rendre le livre'); B.plante(pg,'écrire à Lou'); pg.wait_for_timeout(1500)
        G=pg.evaluate(OU); a=list(G)[0]; B.tap(pg,G[a][0],G[a][1]); pg.wait_for_timeout(2500)
        pg.evaluate("""()=>{ window.__T={}; ['renderDetail','render','caption','syncAll','feedAdd','relayout','saveState','_fichePose','_ficheTrait','_ficheDalle','peintMinis'].forEach(n=>{ const f=window[n]; if(typeof f!=='function') return; window[n]=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally { const d=performance.now()-t; (window.__T[n]=window.__T[n]||[]).push([Math.round(t-(window.__lever||t)), Math.round(d*10)/10]); } }; });
          document.addEventListener('touchend',()=>{ if(!window.__lever) window.__lever=performance.now(); },true); }""")
        z=pg.evaluate("()=>{const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]}")
        B.glisse(pg,[[200+130*i/12,z[1]+z[3]*0.45] for i in range(13)],pas=22,tenue=380); pg.wait_for_timeout(2500)
        print(k, pg.evaluate("()=>JSON.stringify(window.__T)")[:900]); ctx.close()
    b.close()
