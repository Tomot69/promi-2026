"""v209 (C-300) — la vraie veille dans les conditions de l'app : la coquille (appareil à 1, sans coins) et la forme de l'écran déclarée (encoche du 16e) ;
le fond couvre l'écran entier, l'obstacle est posé, le logo ne passe jamais dans la découpe (relevé à chaque image pendant 20 s)."""
import json
from playwright.sync_api import sync_playwright
CSS = open('scratchpad/v209/coquille_v209.css').read()
FORME = {'modele': 'iPhone17,5', 'source': 'table', 'decoupe': {'x': 114, 'y': 0, 'w': 162, 'h': 33}}
ok = tot = 0
def juge(c, m, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + m + ('   ' + d if d else ''))
with sync_playwright() as pw:
    b = pw.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    ctx.add_init_script("window.__ecranForme=%s; document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=%s;document.head.appendChild(s);});" % (json.dumps(FORME), json.dumps(CSS)))
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?veille=3', wait_until='load')
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.wait_for_timeout(6000)
    v = pg.evaluate('()=>window._veille()')
    juge(v['active'], 'la veille est partie')
    C = v['cadre']; juge(abs(C['left']) < 0.5 and abs(C['top']) < 0.5 and abs(C['width'] - 390) < 0.5 and abs(C['height'] - 844) < 0.5, "le fond couvre l'écran entier", '%s' % {k: round(C[k], 1) for k in ('left', 'top', 'width', 'height')})
    juge(len(v['bornes'].get('obs') or []) == 1, "l'encoche est un obstacle", json.dumps(v['bornes'].get('obs')))
    juge(v['bornes']['y0'] == 0 and v['bornes']['x0'] == 0, 'aucune zone sûre retranchée', 'x0 %s y0 %s' % (v['bornes']['x0'], v['bornes']['y0']))
    pts = pg.evaluate("""()=>new Promise(r=>{ const L=[]; const t0=performance.now(); (function f(){ const v=window._veille(); if(v.logo) L.push(v.logo); if(performance.now()-t0<20000) requestAnimationFrame(f); else r(L); })(); })""")
    dans = [p for p in pts if p[0] + p[2] > 114.5 and p[0] < 275.5 and p[1] < 32.5]
    juge(len(pts) > 300 and not dans, 'le logo ne passe jamais dans la découpe', '%d images, %d dedans ; au plus haut %.1f pt' % (len(pts), len(dans), min(p[1] for p in pts)))
    b.close()
print('\n  %s  %d / %d' % ('✅' if ok == tot else '❌', ok, tot))
