# C-155 : le coût des morceaux du gestionnaire de lever de la page + (WebKit).
import sys, os; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
with sync_playwright() as p:
    b = p.webkit.launch()
    for essai in range(3):
        ctx = contexte(b); pg = ouvre(ctx, F)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'arroser les tomates'); pg.wait_for_timeout(900)
        pg.evaluate("""()=>{ window.__T=[]; const W=(o,k,n)=>{ const f=o[k]; if(typeof f!=='function') return; o[k]=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally { window.__T.push([n, +(performance.now()-t).toFixed(1)]); } }; };
          W(window,'_ppTout','_ppTout'); const bp=document.getElementById('addPromi'); const o=bp.onclick; bp.onclick=function(){ const t=performance.now(); try{ return o.apply(this,arguments); } finally { window.__T.push(['onclick addPromi', +(performance.now()-t).toFixed(1)]); } };
          W(window,'printTirage','printTirage');
          document.addEventListener('touchend',()=>{ window.__t0=performance.now(); },true);
          window.addEventListener('touchend',()=>{ window.__T.push(['touchend total (fenêtre)', +(performance.now()-window.__t0).toFixed(1)]); },false);
          requestAnimationFrame(function f(){ if(window.__t0 && !window.__img){ window.__img=performance.now()-window.__t0; } requestAnimationFrame(f); }); }""")
        z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
        glisse(pg, [[40 + 200 * i / 10, y] for i in range(11)], pas=30, tenue=0); pg.wait_for_timeout(1500)
        print(essai, pg.evaluate("()=>window.__T"), 'première image après le lever : %.0f ms' % pg.evaluate("()=>window.__img||-1"))
        ctx.close()
    b.close()
