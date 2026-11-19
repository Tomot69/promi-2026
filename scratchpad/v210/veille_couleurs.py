"""v210 (C-300 suite) — la veille : à chaque capture, la couleur du logo est une couleur EXACTE de la palette (à 1,5 près, le cœur des lettres), y compris juste
après un rebond (le changement de couleur) ; la vitesse est 91,8 pt/s (×1,5). Ingénu (en clair aucun ton n'atteint 3:1 : c'est là que l'ancien repli ternissait)
et Truculent, clair et sombre, dans les conditions de l'app (la coquille, l'encoche). python3 scratchpad/v210/veille_couleurs.py [--fichier=]"""
import json, io, sys
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
CSS = open('scratchpad/v209/coquille_v209.css').read()
FORME = {'modele': 'iPhone17,5', 'source': 'table', 'decoupe': {'x': 114, 'y': 0, 'w': 162, 'h': 33}}
PALS = {'signal': [[130,174,248],[255,184,210],[201,168,245],[239,227,199]], 'truculent': [[255,62,0],[0,229,255],[86,0,214],[246,255,0]]}
AMANDE = [143, 224, 143]
ok = tot = 0
def juge(c, m, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + m + ('   ' + d if d else ''))
def coeur(im):
    """les pixels du cœur des lettres : identiques à leurs 8 voisins (loin du bord anticrénelé)"""
    W, H = im.size; p = im.load(); L = []
    for y in range(1, H - 1, 2):
        for x in range(1, W - 1, 2):
            c = p[x, y]
            if all(p[x + dx, y + dy] == c for dx in (-1, 0, 1) for dy in (-1, 0, 1)): L.append(c)
    return L
with sync_playwright() as pw:
    b = pw.webkit.launch()
    for pal in ('signal', 'truculent'):
        for th in ('light', 'dark'):
            ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, color_scheme=th)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s');localStorage.setItem('promi_palette','%s');}catch(e){}" % (th, pal))
            ctx.add_init_script("window.__ecranForme=%s; document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=%s;document.head.appendChild(s);});" % (json.dumps(FORME), json.dumps(CSS)))
            pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/%s?veille=3' % F, wait_until='load')
            pg.evaluate("(k)=>{ try{ Toile.setPalette(k); }catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }", pal)
            pg.wait_for_timeout(6000)
            v = pg.evaluate('()=>window._veille()')
            if not v['active']: juge(False, '%s %s : la veille est partie' % (pal, th)); ctx.close(); continue
            tons = [[int(h[i:i+2], 16) for i in (1, 3, 5)] for h in pg.evaluate("()=>{ const T=[]; return (window._veilleDerniere||{}).couleurs||T; }") or []]
            fd = v['fond']; FOND = [int(fd[i:i+2], 16) for i in (1, 3, 5)]   # le fond, visible entre les lettres
            pal_ok = PALS[pal] + [AMANDE]
            # les tons tirés : chacun exactement un ton de la palette (ou l'amande des coins)
            vt = pg.evaluate("()=>{ const v=window._veille(); return v; }")
            # les captures : 28 au fil de l'eau, puis une rafale juste après deux rebonds
            mauvais = []; vus = 0
            def capture():
                global vus
                v = pg.evaluate('()=>window._veille()'); lg = v['logo']; C = v['cadre']
                if not lg: return
                png = pg.screenshot(clip={'x': C['left'] + lg[0], 'y': C['top'] + lg[1], 'width': lg[2], 'height': lg[3]})
                im = Image.open(io.BytesIO(png)).convert('RGB'); L = coeur(im)
                if len([c for c in L if not all(abs(c[i] - FOND[i]) <= 1.5 for i in range(3))]) < 20: return
                vus += 1
                for c in set(L):
                    if all(abs(c[i] - FOND[i]) <= 1.5 for i in range(3)): continue
                    if not any(all(abs(c[i] - q[i]) <= 1.5 for i in range(3)) for q in pal_ok): mauvais.append(c)
            for i in range(28): capture(); pg.wait_for_timeout(180)
            for _ in range(2):
                r0 = pg.evaluate('()=>window._veille().rebonds'); t = 0
                while pg.evaluate('()=>window._veille().rebonds') == r0 and t < 60: pg.wait_for_timeout(40); t += 1
                for i in range(6): capture()
            juge(vus >= 30 and not mauvais, '%-9s %-5s : le cœur du logo est un ton exact de la palette, à chaque capture (dont juste après un rebond)' % (pal, th),
                 '%d captures ; hors palette : %s' % (vus, sorted(set(mauvais))[:4]))
            # la vitesse, entre deux rebonds, en pt/s (la cadre en pt : k = 1 dans la coquille)
            pts = pg.evaluate("""()=>new Promise(r=>{ const L=[]; const t0=performance.now(); (function f(){ const v=window._veille(); if(v.logo) L.push([performance.now(), v.logo[0], v.logo[1], v.rebonds]); if(performance.now()-t0<3000) requestAnimationFrame(f); else r(L); })(); })""")
            vs = [((b2[1]-a[1])**2 + (b2[2]-a[2])**2) ** 0.5 / ((b2[0]-a[0]) / 1000) for a, b2 in zip(pts, pts[1:]) if a[3] == b2[3] and b2[0] - a[0] > 8]
            vs.sort(); med = vs[len(vs)//2] if vs else 0
            juge(abs(med - 91.8) <= 3, '%-9s %-5s : la vitesse 91,8 pt/s (×1,5)' % (pal, th), 'médiane %.1f pt/s' % med)
            ctx.close()
    b.close()
print('\n  %s  %d / %d' % ('✅' if ok == tot else '❌', ok, tot))
