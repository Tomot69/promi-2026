#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_vol_dalle.py — LA DALLE QUI NAÎT AU DEMI-TRAIT ARRIVE SUR LA TOILE, ET C'EST TOUT (v183b, Tom, 7 nov. 2026 — C-237 suite, C-241 suite).
« À la fin du vol il y a encore un coup : pas de substitution visible, pas de flash, pas de changement de taille, de forme ni de couleur au moment où elle se pose. »
« À tout instant, une seule dalle de la nouvelle parole est visible à l'écran. »
Banc WebKit 430 × 932 ×3, Toile de dix paroles, page + d'un Promi au doigt, la moitié du trait tracée ; mondes : Pochade sous Ingénu (la palette par défaut),
Esquille (une Toile faite de ses paroles), Touffe, Tesselle :
  A · UNE SEULE DALLE, image par image (relevé dans la page) : jamais la dalle qui vole ET la page + qui montre encore la sienne ;
  B · L'ATTERRISSAGE : l'image de la dalle qui vole, gardée au moment où elle est collée dans l'image de la Toile d'avant (sa boîte rendue), puis comparée,
      une fois la Toile d'avant retirée, aux pixels de l'écran à la même place : ≤ 4 % de pixels écartés de plus de 40 niveaux (le titre que la Toile écrit
      sur sa dalle compris) — ni place, ni taille, ni forme, ni couleur ne changent quand elle se pose.
`?onbLent=4` ralentit le retrait (les photographies tombent au début de lui, pas au milieu). Usage : python3 redteam_vol_dalle.py [fichier.html] [mondes…]
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
exec(open('redteam_moitie.py').read().split('REF = None')[0].split('from playwright.sync_api import sync_playwright')[1])
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
MONDES = [a for a in sys.argv[1:] if not a.endswith('.html') and not a.startswith('--')] or ['encre', 'esquille', 'touffe', 'mosaique']
NOMS = {'encre': 'Pochade · Ingénu', 'esquille': 'Esquille', 'touffe': 'Touffe', 'mosaique': 'Tesselle'}
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %s  %s' % ('OK' if ok else 'KO', nom, str(d)[:220]), flush=True)
REC = r"""()=>{ window.__vol=[]; const t0=performance.now(); (function f(){ const dc=document.querySelector('#ppNait .onbv-dalle'), cs=document.getElementById('createSheet');
   const pageDalle=!!(cs && cs.classList.contains('show') && !cs.classList.contains('cs-coupe') && getComputedStyle(cs).visibility!=='hidden' && !window._ppSansDalle);
   window.__vol.push([Math.round(performance.now()-t0), !!dc, pageDalle]); if(performance.now()-t0<7000) requestAnimationFrame(f); })(); }"""
PIEGE = r"""()=>{ const o=window._retireFondFlaques; window.__fini=false; window.__dc=null; window._retireFondFlaques=function(fond, dc, fin){ window._retireFondFlaques=o;
   try{ if(dc && dc.width){ const r=dc.getBoundingClientRect(); window.__dc={u:dc.toDataURL(), r:[r.left,r.top,r.width,r.height]}; } }catch(_){ }
   return o(fond, dc, function(){ window.__fini=true; fin(); }); }; }"""
def zone(im, r, S=3, m=24): return im.crop((int(r[0]*S)-m, int(r[1]*S)-m, int((r[0]+r[2])*S)+m, int((r[1]+r[3])*S)+m))
def change(a, c): d = ImageChops.difference(a, c).convert('L'); h = d.histogram(); return 100 * sum(h[40:]) / max(1, sum(h))
with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MONDES:
        ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, 7000, q='?onbLent=4')
        pg.evaluate("m=>{ Toile.setTheme(m); window._vivantOff=true; }", m); pg.wait_for_timeout(9000)
        ouvre_nature(pg, 'promi'); remplit(pg, 'promi', 'arroser les tomates')
        pg.evaluate(REC); pg.evaluate(PIEGE)
        B.glisse(pg, points(pg, list(range(44, 212, 12))), pas=18, tenue=40)
        for _ in range(120):
            pg.wait_for_timeout(100)
            if pg.evaluate("()=>window.__fini"): break
        pg.wait_for_timeout(1200)
        c = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        d = pg.evaluate("()=>window.__dc")
        V = pg.evaluate("()=>window.__vol"); deux = [v[0] for v in V if v[1] and v[2]]
        juge('A · [%s] une seule dalle à chaque image (%d images, %d avec la dalle qui vole)' % (NOMS.get(m, m), len(V), sum(1 for v in V if v[1])), not deux and any(v[1] for v in V), ('images doubles à', deux[:6]))
        if not d: juge('B · [%s] la dalle arrive' % NOMS.get(m, m), False, 'aucune dalle au collage'); ctx.close(); continue
        r = d['r']; im = Image.open(io.BytesIO(__import__('base64').b64decode(d['u'].split(',')[1]))).convert('RGBA')
        S = 3; W, H = max(1, round(r[2] * S)), max(1, round(r[3] * S)); X, Y = round(r[0] * S), round(r[1] * S); im = im.resize((W, H))
        n = tot = fort = 0
        for j in range(0, H, 2):
            for i in range(0, W, 2):
                q = im.getpixel((i, j))
                if q[3] < 250: continue
                s = c.getpixel((min(c.width - 1, X + i), min(c.height - 1, Y + j))); dd = max(abs(q[k] - s[k]) for k in range(3)); n += 1; fort += dd > 40
        pc = 100 * fort / max(1, n)
        juge('B · [%s] la dalle qui vole, au collage, est la dalle de la Toile vivante : même place, taille, forme, couleur (%.1f %% de pixels écartés de plus de 40)' % (NOMS.get(m, m), pc), pc <= 4.0, ([round(x) for x in r], n))
        pl = Image.new('RGB', (W * 2 + 10, H), 'white'); bg = Image.new('RGBA', (W, H), (230, 220, 200, 255)); bg.alpha_composite(im); pl.paste(bg.convert('RGB'), (0, 0)); pl.paste(c.crop((X, Y, X + W, Y + H)), (W + 10, 0)); pl.save('scratchpad/v183/vol-%s.png' % m)
        juge('Z · [%s] aucune erreur de page' % NOMS.get(m, m), not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
        ctx.close()
    b.close()
print('\n%d / %d' % (sum(res), len(res)))
