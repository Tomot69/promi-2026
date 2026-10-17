import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
PIEGE = r"""()=>{ window.__cl=[]; const cs=document.getElementById('createSheet'); window.__t0=performance.now(); const t0=window.__t0; const NL=String.fromCharCode(10);
  const pile=()=> (new Error()).stack.split(NL).slice(2,5).map(x=>x.trim().slice(0,60)).join(' < ');
  if(!cs.__pi){ cs.__pi=1; const ra=cs.removeAttribute.bind(cs), sa=cs.setAttribute.bind(cs);
  cs.removeAttribute=function(n){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-window.__t0), 'retire', pile()]); return ra(n); };
  cs.setAttribute=function(n,v){ if(n==='data-kind') window.__cl.push([Math.round(performance.now()-window.__t0), 'pose '+v]); return sa(n,v); };
  const L=cs.classList, o=L.toggle.bind(L); L.toggle=function(){ if(String(arguments[0])==='pp-choix') window.__cl.push([Math.round(performance.now()-window.__t0), 'pp-choix '+arguments[1]]); return o.apply(L, arguments); }; } }"""
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    def page_plus(t, log=False):
        if log: pg.evaluate(PIEGE)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        if log: pg.evaluate("()=>window.__cl.push([Math.round(performance.now()-window.__t0),'CLIC'])")
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", t); pg.wait_for_timeout(400)
    def tr(dx, pas):
        z = pg.evaluate(ZONE, 'planterZone')
        if not z: return False
        y = z[1] + z[3] * 0.45; glisse(pg, [[40 + dx * i / 10, y] for i in range(11)], pas=pas); return True
    for k in range(4):
        page_plus('rendre %d' % k, log=True); ok = tr(70, 12 if k % 2 else 100); pg.wait_for_timeout(3200)
        print(F, k, 'zone', ok, 'paroles', pg.evaluate("()=>promises.length"), pg.evaluate("()=>window.__cl"))
    b.close()
