# C-155 : ce qui tourne autour du lever (planter et tenir) — chaque rappel chronométré (WebKit, banc_tom, vrai doigt).
import sys, os; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
PROF = open('scratchpad/v143/profil.py', encoding='utf-8').read().split('PROF = r"""')[1].split('"""')[0]
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
QUOI = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--quoi=')), 'planter')
print('charge', os.popen('sysctl -n vm.loadavg').read().strip())
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
ARME = "()=>{ window.__Pon(true); window.__lever=0; document.addEventListener('touchend',()=>{ if(!window.__lever) window.__lever=performance.now(); },true); }"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = contexte(b); ctx.add_init_script(PROF); pg = ouvre(ctx, F)
    if QUOI == 'tenir':
        plante(pg, 'rendre le livre'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
        z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
        pg.evaluate(ARME)
        glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    else:
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'arroser les tomates'); pg.wait_for_timeout(900)
        z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
        pg.evaluate(ARME)
        glisse(pg, [[40 + 200 * i / 10, y] for i in range(11)], pas=30, tenue=0)
    pg.wait_for_timeout(2500)
    R = pg.evaluate("()=>({lev:window.__lever, r:window.__P.slice(), f:window.__F.slice()})")
    L = R['lev']
    print(QUOI.upper(), '— rappels de 4 ms et plus, de −60 à +700 ms du lever')
    for t, d, n in sorted(R['r']):
        if d >= 4 and -60 <= t - L <= 700: print('  %+5d  %5.1f ms  %s' % (t - L, d, n[:200]))
    fr = [x for x in R['f'] if -60 <= x - L <= 700]
    print('  images :', ' '.join('%+d' % (x - L) for x in fr[:40]))
    b.close()
