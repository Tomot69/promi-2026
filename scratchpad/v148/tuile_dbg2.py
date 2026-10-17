import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'x'); pg.wait_for_timeout(400)
    z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100); pg.wait_for_timeout(3200)
    pg.evaluate("()=>{ window.__cl=[]; const cs=document.getElementById('createSheet'); const t0=performance.now(); const L=cs.classList; ['add','remove','toggle'].forEach(m=>{ const o=L[m].bind(L); L[m]=function(){ if(String(arguments[0]).indexOf('pp-choix')>=0 || (m==='remove' && arguments[0]==='pp')) window.__cl.push([Math.round(performance.now()-t0), m+' '+[...arguments].join(','), (new Error()).stack.split(String.fromCharCode(10)).slice(1,5).map(x=>x.trim().slice(0,90)).join(' < ')]); return o.apply(this, arguments); }; }); const ra=cs.removeAttribute.bind(cs), sa=cs.setAttribute.bind(cs); cs.removeAttribute=function(n){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-t0), 'retire data-kind', (new Error()).stack.split(String.fromCharCode(10)).slice(1,6).map(x=>x.trim().slice(0,80)).join(' < ')]); return ra(n); }; cs.setAttribute=function(n,v){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-t0), 'pose data-kind '+v, (new Error()).stack.split(String.fromCharCode(10)).slice(1,4).map(x=>x.trim().slice(0,80)).join(' < ')]); return sa(n,v); };
      closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{ const x=[...document.querySelectorAll('#createSheet .tile')][0]; window.__cl.push([Math.round(performance.now()-t0),'CLIC TUILE']); x&&x.click(); }, 700); }")
    pg.wait_for_timeout(2600); print(F); [print('  ', x) for x in pg.evaluate("()=>window.__cl")]
    b.close()
