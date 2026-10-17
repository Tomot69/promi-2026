import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
ST = "()=>({n:promises.length, cs:document.getElementById('createSheet').className, z:(document.getElementById('planterZone')||{}).className, d:window._traitDernier||null, rub:(window._ruban&&_ruban.etat()), tir:!!window._tirageActive, titre:(document.getElementById('fTitle')||{}).value, ph:(window._phrase||{}).titre})"
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F); er=[]; pg.on('pageerror', lambda e: er.append(str(e)[:200])); pg.on('console', lambda m: er.append('console:'+m.text[:150]) if m.type=='error' else None)
    def page_plus(t):
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", t); pg.wait_for_timeout(400)
    def tr(dx, pas):
        z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
        return glisse(pg, [[40 + dx * i / 10, y] for i in range(11)], pas=pas)
    page_plus('rendre le livre'); tr(30, 30); pg.wait_for_timeout(1500); print('30', pg.evaluate(ST))
    tr(70, 100); pg.wait_for_timeout(3200); print('lent', pg.evaluate(ST))
    page_plus('écrire à Lou'); print('page+ 2', pg.evaluate(ST))
    tr(70, 12)
    for t in (100, 400, 800, 1500, 3200):
        pg.wait_for_timeout(t - (0 if t == 100 else [100, 400, 800, 1500][[400, 800, 1500, 3200].index(t)])); print(t, pg.evaluate(ST))
    print('erreurs', er[:5]); b.close()
