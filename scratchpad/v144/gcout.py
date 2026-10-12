import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
for moteur in ('chromium','webkit'):
  with sync_playwright() as p:
    b=getattr(p,moteur).launch(); ctx=B.contexte(b); pg=B.ouvre(ctx); B.plante(pg,'rendre le livre'); pg.wait_for_timeout(2500)
    r=pg.evaluate("""async ()=>{ const out={}; let t=performance.now(); _guide.montre('studio'); out.montre=performance.now()-t; await new Promise(r=>setTimeout(r,2200));
      window.__lt=[]; try{ new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime-window.__t0),Math.round(e.duration)]))).observe({entryTypes:['longtask']}); }catch(e){}
      window.__t0=performance.now(); t=performance.now(); _guide.glisse(); out.glisse=performance.now()-t; await new Promise(r=>setTimeout(r,1500)); out.longues=window.__lt; out.n=document.querySelectorAll('#guideLoupeIn *').length; return out; }""")
    print(moteur, r); b.close()
