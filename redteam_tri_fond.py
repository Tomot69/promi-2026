#!/usr/bin/env python3
"""redteam_tri_fond.py — ⚑ v162 (Tom, C-185) : « le bouton Réglages du Fil et de l'Index fait passer le fond en marron ».

Le bouton est celui de trier et filtrer (⇅, `.ix-tri`). Cause : `#indexSheet .ix-menu::before, #feedView .ix-menu::before` posait sur toute la page l'encre du
mode à 60 % (`rgba(--c-brun09, .6)`, depuis août) : en clair la crème passait au brun, en sombre la seiche s'éteignait encore. Décision : derrière le menu,
la page garde sa teinte. Banc comme Tom (WebKit, ×3, doigt), Toile de 10 paroles, 3 mondes × 2 palettes × 2 thèmes, l'Index et le Fil :
  A · menu ouvert, la marge de la page (hors du panneau) a la même couleur qu'avant le toucher (≤ 3 niveaux par canal, lu sur l'image) ;
  B · (le Fil) un toucher hors du panneau le referme. Dans l'Index il ne se referme pas au doigt — déjà en v161, hors du lot (Q578).
Preuve : `--fichier=zz-v161.html` rougit.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
MONDES = ['encre', 'touffe', 'mosaique']; PALS = ['signal', 'truculent']
def marge(pg):
    D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390]}")
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = D[2] * 3
    px = [im.getpixel((int((D[0] + 6 * D[2]) * 3), int((D[1] + y * D[2]) * 3))) for y in range(420, 700, 20)]
    return tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        for m in MONDES:
            for pal in PALS:
                ctx = B.contexte(b, sombre=sombre, stockage={'promi_studio': '{"m":"%s","p":"%s","h":0,"libre":true,"acquis":{}}' % (m, pal)})
                B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
                for porte, tri, menu in (('#indexBtn', '#ixTriBtn', '#ixMenu'), ('#filBtn', '#fdTriBtn', '#fdMenu')):
                    T = '%s · %s · %s · %s' % ('sombre' if sombre else 'clair', m, pal, 'Index' if porte == '#indexBtn' else 'Fil')
                    pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(900); B.tap_sel(pg, porte); pg.wait_for_timeout(2400)
                    av = marge(pg); B.tap_sel(pg, tri); pg.wait_for_timeout(1200)
                    ouvert = pg.evaluate("s=>{const e=document.querySelector(s+' .ix-menu-p');if(!e)return false;const r=e.getBoundingClientRect();return r.width>100&&getComputedStyle(e).visibility!=='hidden'&&+getComputedStyle(document.querySelector(s)).opacity>0.5}", menu)
                    ap = marge(pg); d = max(abs(a - c) for a, c in zip(av, ap))
                    juge('[%s] A · menu ouvert, la page garde sa teinte' % T, ouvert and d <= 3, 'avant %s · après %s · écart %d · menu %s' % (av, ap, d, ouvert))
                    B.tap(pg, 10, 560); pg.wait_for_timeout(900)
                    ferme = pg.evaluate("s=>getComputedStyle(document.querySelector(s)).display==='none'", menu)
                    if porte == '#filBtn': juge('[%s] B · un toucher hors du panneau referme le menu' % T, ferme)
                    else: pg.evaluate("s=>{ const m=document.querySelector(s); m.classList.remove('on'); }", menu)   # Index : il ne se referme pas au doigt, déjà en v161 (Q578) — hors du lot
                er = [x for x in pg.erreurs if 'version.json' not in x]
                if er: juge('aucune erreur de page', False, er[:2])
                ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
