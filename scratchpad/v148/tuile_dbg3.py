import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
PIEGE = r"""()=>{ window.__cl=[]; const cs=document.getElementById('createSheet'); const t0=performance.now(); const NL=String.fromCharCode(10);
  const pile=()=> (new Error()).stack.split(NL).slice(2,6).map(x=>x.trim().slice(0,70)).join(' < ');
  const ra=cs.removeAttribute.bind(cs), sa=cs.setAttribute.bind(cs);
  cs.removeAttribute=function(n){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-t0), 'retire data-kind', pile()]); return ra(n); };
  cs.setAttribute=function(n,v){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-t0), 'pose data-kind '+v, pile()]); return sa(n,v); };
  const L=cs.classList, o=L.toggle.bind(L); L.toggle=function(){ if(String(arguments[0])==='pp-choix') window.__cl.push([Math.round(performance.now()-t0), 'toggle pp-choix '+arguments[1], pile()]); return o.apply(L, arguments); };
  closeAll(); document.getElementById('createBtn').click();
  setTimeout(()=>{ const x=[...document.querySelectorAll('#createSheet .tile')][0]; window.__cl.push([Math.round(performance.now()-t0),'CLIC TUILE', String(x&&x.getBoundingClientRect().width)]); x&&x.click(); }, 700); }"""
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'x'); pg.wait_for_timeout(400)
    z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100); pg.wait_for_timeout(3200)
    pg.evaluate(PIEGE); pg.wait_for_timeout(2600)
    print(F, pg.evaluate("()=>document.getElementById('createSheet').className")); [print('  ', x) for x in pg.evaluate("()=>window.__cl")]
    b.close()
