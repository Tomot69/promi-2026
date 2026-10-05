#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_zone.py — RIEN NE PEINT DERRIÈRE LA PELOTE, HORS LE HALO ET L'OMBRE ; ET LE HALO N'A PAS DE SECOND BORD (v125, Tom, 3 oct. 2026).

« La double zone derrière la Pelote, en sombre. Juge : trente ouvertures dans chaque thème, et hors silhouette, halo et ombre, chaque
pixel égal au fond. Il doit rougir sur l'état actuel. »
CE QUI A ÉTÉ MESURÉ AVANT D'ÉCRIRE LE JUGE : hors du halo et de l'ombre, rien ne peignait (aucun reste d'écho, de couronne ni de flaque à
l'écran — la flaque était du code mort). La « seconde zone » était le halo lui-même : coupé en 10° au quart inférieur, il dessinait
deux épaules — le bord d'un second disque. Le juge porte donc DEUX règles, sur l'image rendue (capture d'écran, pas le DOM) :
  A · hors de la silhouette, du halo (rayon ≤ 156 pt du centre : la silhouette 126,5 + l’étendue 0,12 D = 29) et de l'ombre, chaque
      pixel est le fond (à 2 niveaux près), de la bande sous le plateau jusqu'au bouton ;
  B · le halo n'a pas de bord dans son tour : sur le cercle à 131 pt du centre, la lumière ne change jamais de plus de 30 % de son
      maximum en 6° (l'épaule d'avant : 55 %).
Les valeurs sont en dur. Trente ouvertures par thème (`--n=`), chacune avec son tirage de sol et de corps.
Preuve : sur l'état d'avant (une copie de `sauvegardes/app-avant-v125.html` à la racine), B rougit dans les deux thèmes.
"""
import sys, io, math
from playwright.sync_api import sync_playwright
from PIL import Image
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 30))
R_HALO, R_CERCLE, SAUT_MAX, TOL, DSF = 156.0, 131.0, 0.30, 2, 2
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail))
GEO = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const R=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left,r.top,r.right,r.bottom]};
  return {dv:[dv.left,dv.top,dv.right,dv.bottom], bo:R('#auBoule'), om:R('#auPeloteOmbre'), pl:R('#auraScreen .enh'), bt:R('#auPartage'), prete:!!(window._aura&&_aura.etat&&document.getElementById('auBoule').width>300)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('dark', 'light'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=DSF, reduced_motion='reduce')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}", th); pg.wait_for_timeout(500)
        horsA = 0; pireA = ''; pireB = 0.0; exB = ''; lus = 0
        for i in range(N):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); }"); pg.wait_for_timeout(350)
            pg.evaluate("()=>{ document.querySelectorAll('.screen.show').forEach(s=>{ if(s.id!=='auraScreen'&&s.id!=='studioScreen') s.classList.remove('show'); }); document.getElementById('souffleBtn').click(); }")
            pg.wait_for_timeout(1700 if i else 4500)
            g = pg.evaluate(GEO)
            if not g['bo'] or not g['bt']: continue
            x0, y0 = g['dv'][0], g['pl'][3] + 2; x1, y1 = g['dv'][2], g['bt'][1] - 2
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': x0, 'y': y0, 'width': x1 - x0, 'height': y1 - y0}))).convert('RGB'); px = im.load(); W, H = im.size
            cx = ((g['bo'][0] + g['bo'][2]) / 2 - x0) * DSF; cy = ((g['bo'][1] + g['bo'][3]) / 2 - y0) * DSF
            fond = px[3, int(cy)]
            om = [(g['om'][0] - x0 - 1) * DSF, (g['om'][1] - y0 - 1) * DSF, (g['om'][2] - x0 + 1) * DSF, (g['om'][3] - y0 + 1) * DSF] if g['om'] else [0, 0, 0, 0]
            lus += 1; n = 0
            for y in range(0, H):
                for x in range(0, W):
                    if (x - cx) ** 2 + (y - cy) ** 2 <= (R_HALO * DSF) ** 2: continue
                    if om[0] <= x <= om[2] and om[1] <= y <= om[3]: continue
                    c = px[x, y]
                    if abs(c[0] - fond[0]) > TOL or abs(c[1] - fond[1]) > TOL or abs(c[2] - fond[2]) > TOL:
                        n += 1
                        if not pireA: pireA = 'ouverture %d : (%.0f, %.0f) pt du coin · %s au lieu de %s' % (i + 1, x / DSF, y / DSF, c, fond)
            horsA += n
            # B · le tour du halo, à 131 pt
            L = []
            for a in range(0, 360, 3):
                s = 0; k = 0
                for da in (-1.5, -0.75, 0, 0.75, 1.5):
                    for dr in (-2, -1, 0, 1, 2):
                        t = math.radians(a + da); r = (R_CERCLE + dr) * DSF; x = int(cx + r * math.cos(t)); y = int(cy + r * math.sin(t))
                        if 0 <= x < W and 0 <= y < H:
                            c = px[x, y]; s += max(abs(c[0] - fond[0]), abs(c[1] - fond[1]), abs(c[2] - fond[2])); k += 1
                L.append(s / max(1, k))
            mx = max(L) or 1
            for j in range(len(L)):
                d = abs(L[(j + 2) % len(L)] - L[j]) / mx
                if mx >= 3 and d > pireB: pireB = d; exB = 'ouverture %d, vers %d° (0° = à droite, 90° = en bas) : %.1f → %.1f niveaux (maximum du tour %.1f)' % (i + 1, j * 3, L[j], L[(j + 2) % len(L)], mx)
        juge('[%s] les %d ouvertures sont lues' % (th, N), lus == N, '%d' % lus)
        juge('A · [%s] hors silhouette, halo et ombre : chaque pixel est le fond' % th, lus > 0 and horsA == 0, '%d pixel(s) · %s' % (horsA, pireA))
        juge('B · [%s] le halo n\'a pas de second bord (≤ %d %% de son maximum en 6°)' % (th, SAUT_MAX * 100), lus > 0 and pireB <= SAUT_MAX, 'le pire : %.0f %% · %s' % (pireB * 100, exB))
        juge('[%s] aucune erreur de page' % th, not er, '; '.join(er[:2]))
        ctx.close()
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
sys.exit(1 if ko else 0)
