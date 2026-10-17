import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
ST = "()=>({n:promises.length, cs:document.getElementById('createSheet').className, z:(document.getElementById('planterZone')||{}).className, d:window._traitDernier||null, rub:(window._ruban&&_ruban.etat())})"
for F in sys.argv[1:]:
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'rendre le livre'); pg.wait_for_timeout(400)
        z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
        glisse(pg, [[40 + 30 * i / 10, y] for i in range(11)], pas=30); pg.wait_for_timeout(1500); print(F, '30 pt', pg.evaluate(ST))
        z2 = pg.evaluate(ZONE, 'planterZone'); print('   zone après', z2)
        glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100); pg.wait_for_timeout(3200); print(F, '70 pt lent', pg.evaluate(ST))
        b.close()
