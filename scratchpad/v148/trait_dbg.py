import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
for F in sys.argv[1:]:
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
        for k in range(3):
            pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
            pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
            pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'rendre %d' % k); pg.wait_for_timeout(400)
            n0 = pg.evaluate("()=>promises.length"); z = pg.evaluate(ZONE, 'planterZone')
            y = z[1] + z[3] * 0.45
            info = pg.evaluate("(a)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const h=document.elementFromPoint(D.left+a[0]*k, D.top+a[1]*k); return [h?(h.id||String(h.className).slice(0,30)):null, document.getElementById('createSheet').className]; }", [40, y])
            glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100)
            pg.wait_for_timeout(3200); print(F, k, 'zone', [round(v) for v in z], 'sous le doigt', info, 'paroles', n0, '→', pg.evaluate("()=>promises.length"), 'geste', pg.evaluate("()=>window._traitDernier||null"))
        b.close()
