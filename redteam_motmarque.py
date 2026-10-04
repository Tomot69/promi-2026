#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_motmarque.py — LE MOT DE LA NATURE EST CENTRÉ DANS SON ENCART, PAREIL POUR LES TROIS NATURES (v129, Tom, C-046).

« En haut de la fiche d'un Cercle, le mot "CERCLE" est trop haut dans son encart. Il doit être centré exactement comme "PROMI" et
"CHICHE" dans les leurs. […] Juge : la position verticale du mot dans l'encart est identique au demi-point près pour les trois natures,
en clair et en sombre. Il doit rougir sur l'état actuel. »
Le juge lit l'ENCRE (pas la boîte, §8) : capture @3x du plateau (24, 40, 342 × 60), les pixels de l'encre du mot dans sa moitié gauche
(x 54 → 215, hors du contour), haut et bas de l'encre → le milieu de l'encre, face au milieu du plateau (70). Décidé : l'écart entre natures ≤ 0,5 pt
(en dur), dans chaque thème.   Preuve : sauvegardes/app-avant-v129.html → ROUGE.
"""
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
TOL = 0.5
FICHES = [('Promi', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),
          ('Chiche', "()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; openDetail(p.id);}"),
          ('Cercle', "()=>{closeAll(); openEssaim('potager');}")]
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail))
with sync_playwright() as p:
    b = p.webkit.launch(); R = {}
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{ if(document.documentElement.classList.contains('light')!==(t==='light')) setTheme(t) }catch(e){} }", th); pg.wait_for_timeout(800)
        for nom, js in FICHES:
            pg.evaluate(js); pg.wait_for_timeout(3200)
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': 20 + 24, 'y': 44 + 40, 'width': 342, 'height': 60}))).convert('RGB'); px = im.load()
            fond = px[im.width // 2, im.height // 2]; y0 = None; y1 = None
            for y in range(12, im.height - 12):
                for x in range(30 * 3, 191 * 3):
                    q = px[x, y]
                    if abs(q[0] - fond[0]) + abs(q[1] - fond[1]) + abs(q[2] - fond[2]) > 300:
                        if y0 is None: y0 = y
                        y1 = y; break
            haut, bas = 40 + y0 / 3.0, 40 + (y1 + 1) / 3.0
            R[(nom, th)] = (haut, bas, (haut + bas) / 2)
            print('%-7s %-5s encre %.2f → %.2f  (hauteur %.2f)  milieu %.2f  (plateau : 70,00)' % (nom, th, haut, bas, bas - haut, (haut + bas) / 2))
        ctx.close()
    b.close()
for th in ('light', 'dark'):
    m = [R[(n, th)][2] for n, _ in FICHES]; h = [R[(n, th)][0] for n, _ in FICHES]
    juge('[%s] le milieu de l\'encre du mot est à la même hauteur pour les trois natures (± %.1f pt)' % (th, TOL), max(m) - min(m) <= TOL, 'Promi %.2f · Chiche %.2f · Cercle %.2f' % tuple(m))
    juge('[%s] le haut de l\'encre aussi (± %.1f pt)' % (th, TOL), max(h) - min(h) <= TOL, 'Promi %.2f · Chiche %.2f · Cercle %.2f' % tuple(h))
print('\n%d / %d' % (ok, ok + len(ko)))
sys.exit(1 if ko else 0)
