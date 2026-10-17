import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F); er=[]; pg.on('pageerror', lambda e: er.append(str(e)[:300]))
    def page_plus(t):
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        print('  tuiles', pg.evaluate("()=>[...document.querySelectorAll('#createSheet .tile')].map(t=>[t.getAttribute('data-kind'), t.getBoundingClientRect().width>0])"), pg.evaluate("()=>document.getElementById('createSheet').className"))
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        print('  après tuile', pg.evaluate("()=>document.getElementById('createSheet').className"))
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", t); pg.wait_for_timeout(400)
    page_plus('rendre le livre')
    z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100); pg.wait_for_timeout(3200)
    print('planté', pg.evaluate("()=>promises.length"), pg.evaluate("()=>document.getElementById('createSheet').className"))
    page_plus('écrire à Lou')
    print('erreurs', er[:5]); b.close()
