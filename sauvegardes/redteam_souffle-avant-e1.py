#!/usr/bin/env python3
"""
redteam_souffle.py — LA PELOTE RESPIRE PAR LA LUMIÈRE DU VELOURS, ET RIEN NE SORT DU CONTOUR (v117, Q364 → A, Tom).

Valeurs DÉCIDÉES, écrites ici (jamais lues dans l'app) : cycle 10 s = 4 s qui monte + 6 s qui redescend ; départ 0,6 s après
l'affichage ; amplitude du velours 0 → 0,55 ; immobile avec « Réduire les animations ».
La boule est FIGÉE (`_aura.fige`) : sur un objet qui tourne on compare à l'angle, jamais à l'instant (§8).
Le temps de référence est l'horloge RÉELLE de la page depuis la PREMIÈRE IMAGE PEINTE de la boule (lue aux pixels) — pas l'horloge du souffle.
  A · entre 0,3 s et 4,6 s après l'affichage, des pixels changent DANS la silhouette (> 200), et AUCUN au-delà (deux thèmes)
  B · la lumière moyenne de la boule, relevée toutes les 0,4 s, culmine à 4,6 s ± 0,8 et revient au bas à 10,6 s ± 1
  C · « Réduire les animations » : deux captures à 5 s d'écart identiques, dedans comme dehors
Rougi : `python3 redteam_souffle.py sauvegardes/app-avant-v117b.html` (le velours y vaut 0 ; le juge le copie à la racine).
"""
import sys, os, io, math, shutil
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat

CYCLE, MONTE, DEPART = 10.0, 4.0, 0.6        # décidés (Tom, Q364 — cycle posé en v115)
S = 2
ARG = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
tmp = None
if '/' in ARG: shutil.copy(ARG, 'zz-souffle.html'); ARG = tmp = 'zz-souffle.html'
ok = [True]


def dit(cond, txt):
    print(('OK ' if cond else '✗  ') + txt); ok[0] = ok[0] and cond


def cap(pg): return Image.open(io.BytesIO(pg.screenshot(clip={'x': 20, 'y': 44, 'width': 390, 'height': 844}))).convert('RGB')


def geo(pg):
    g = pg.evaluate("""()=>{const c=document.getElementById('auBoule').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect();
        return {cx:c.x-d.x+c.width/2, cy:c.y-d.y+c.height/2, w:c.width}}""")
    g['rsil'] = 121.0 / 296.0 * g['w']          # la silhouette (boule + poil 4,5), relevée en v115
    return g


def zones(A, B, g):
    d = ImageChops.difference(A, B).convert('L').point(lambda v: 255 if v > 10 else 0); px = d.load(); dedans = dehors = 0
    for y in range(d.height):
        for x in range(d.width):
            if px[x, y]:
                # ⚑ REPRIS EN v119 (§7). LA RÈGLE ENCODÉE : seule la matière respire, rien ne change au-delà de la silhouette.
                #   LA DÉCISION QUI LA COMPLÈTE (Tom, v119) : le mini halo respire avec la lumière (± 20 %), et il est borné à 0,08 D.
                #   « Au-delà » commence donc à la fin du halo : silhouette + 0,08 D (18,6 pt). Original : sauvegardes/redteam_souffle-avant-v119.py
                #   ⚑ v121 (Tom) : le halo par défaut est le niveau 3, étendue 0,12 D (27,8 pt) — « au-delà » commence là.
                if math.hypot(x / S - g['cx'], y / S - g['cy']) <= g['rsil'] + 0.12 * 232.064 + 1: dedans += 1
                else: dehors += 1
    return dedans, dehors


def lum(img, g):
    r = g['rsil'] * 0.8
    box = tuple(int(v * S) for v in (g['cx'] - r, g['cy'] - r, g['cx'] + r, g['cy'] + r))
    return ImageStat.Stat(img.crop(box).convert('L')).mean[0]


OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0);
   window.__t0=performance.now(); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""

PEINTE = """()=>{const c=document.getElementById('auBoule'); if(!c||!c.width) return false; const g=c.getContext('2d');
   const d=g.getImageData(c.width/2-4,c.height/2-4,8,8).data; for(let i=3;i<d.length;i+=4) if(d[i]>200) return true; return false;}"""


def affiche(pg):
    """l'origine : la PREMIÈRE IMAGE peinte de la boule (pixels opaques au centre du canevas), lue sur la page"""
    for _ in range(400):
        if pg.evaluate(PEINTE):
            pg.evaluate("()=>{window.__t0=performance.now();}"); return True
        pg.wait_for_timeout(10)
    return False


def attend(pg, s):
    while pg.evaluate("()=>(performance.now()-window.__t0)/1000") < s: pg.wait_for_timeout(15)


with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + ARG); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{closeAll();setTheme(t)}", th); pg.wait_for_timeout(800)
        pg.evaluate(OUVRE); pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); affiche(pg)
        attend(pg, 0.3); A = cap(pg); g = geo(pg)
        attend(pg, 4.6); B = cap(pg)
        de, ho = zones(A, B, g)
        dit(de > 200 and ho == 0, '[%s] A · 0,3 s → 4,6 s : %d pixels changés dans la silhouette, %d au-delà' % (th, de, ho))
        if th == 'light':
            pg.evaluate("(t)=>{closeAll();}"); pg.wait_for_timeout(1500)
            pg.evaluate(OUVRE); pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); affiche(pg)
            T, L = [], []
            s = 0.2
            while s <= 11.6 and (not T or T[-1] < 12.0):
                attend(pg, s); im = cap(pg)
                T.append(pg.evaluate("()=>(performance.now()-window.__t0)/1000")); L.append(lum(im, g)); s += 0.4
            prem = [i for i in range(len(L)) if T[i] < 8.5] or [0]      # le PREMIER cycle (la capture peut déborder sur le second)
            # ⚑ v119 (instrument) : au sommet et au creux la courbe est PLATE (la lumière, composée après le rendu, y tient la même valeur
            #   d'écran pendant près d'une seconde) : le premier relevé du plateau n'en est pas le milieu. On prend le MILIEU des relevés
            #   à moins de 0,15 niveau de l'extrême. Original : sauvegardes/redteam_souffle-avant-v119.py
            def milieu(idx, ext): pl = [i for i in idx if abs(L[i] - ext) <= 0.15]; return pl[len(pl) // 2]
            i_max = milieu(prem, max(L[i] for i in prem))
            bas = [i for i in range(len(L)) if 8.5 < T[i] < 12.5]
            i_bas = milieu(bas, min(L[i] for i in bas)) if bas else 0
            amp = max(L) - min(L)
            if '--trace' in sys.argv: print('   ', ' '.join('%.1f:%.2f' % (T[i], L[i]) for i in range(len(L))))
            dit(amp > 1.0 and abs(T[i_max] - (DEPART + MONTE)) <= 0.8 and abs(T[i_bas] - (DEPART + CYCLE)) <= 1.0,
                '[%s] B · lumière de la boule : sommet à %.1f s (décidé %.1f), retour au bas à %.1f s (décidé %.1f), amplitude %.2f niveaux'
                % (th, T[i_max], DEPART + MONTE, T[i_bas], DEPART + CYCLE, amp))
        ctx.close()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + ARG); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800)
    pg.evaluate(OUVRE); affiche(pg); attend(pg, 2.0); g = geo(pg)
    A = cap(pg); attend(pg, 7.0); B = cap(pg)
    de, ho = zones(A, B, g)
    dit(de == 0 and ho == 0, 'C · « Réduire les animations » : pixels changés en 5 s — dedans %d, dehors %d' % (de, ho))
    b.close()
if tmp: os.remove(tmp)
print('✅ la Pelote respire par son velours, et rien d\'autre' if ok[0] else '❌ le souffle ne tient pas sa loi'); sys.exit(0 if ok[0] else 1)
