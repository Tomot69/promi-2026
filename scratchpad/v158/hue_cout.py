import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,F)
    pg.evaluate("()=>{ try{setPremium(true)}catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    for m in sys.argv[2].split(','):
        print(m, pg.evaluate("""async (m)=>{ try{ Toile.setTheme(m); }catch(e){} await new Promise(r=>setTimeout(r,2500));
          const out=[]; for(let i=0;i<8;i++){ const t0=performance.now(); Toile.setHue((i*37)%360); const t1=performance.now(); try{ Toile.repaint(document.getElementById('stBg')); }catch(e){} const t2=performance.now();
            const f=await new Promise(r=>requestAnimationFrame(a=>requestAnimationFrame(b=>r(b-a)))); out.push([+(t1-t0).toFixed(1), +(t2-t1).toFixed(1), +f.toFixed(1)]); }
          return out; }""", m))
    b.close()
