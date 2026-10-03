#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_plein.py — LA PELOTE EST PLEINE (v120, Tom, 2 oct. 2026).

« L'intérieur est opaque, toujours, dans les deux thèmes et à tous les paliers du régulateur. On ne doit jamais voir le fond à travers. »

Le juge lit le CANEVAS de la boule (#auBoule) et exige alpha = 255 sur tout pixel situé en retrait de 4 % de D à l'intérieur de la
silhouette — les cotes sont écrites EN DUR ici (§7) : D = 232,064 pt, silhouette = 121 pt, boîte du canevas = 296 pt ; donc tout pixel
à moins de 121 − 0,04 × 232,064 = 111,72 pt du centre. Dans les deux thèmes, à CHACUN des paliers du régulateur, sur quatre palettes
(Ingénu, Candide, Irascible, Taciturne), et aux trois densités de `?densite=`.
Il vérifie aussi que la silhouette n'a pas bougé : aucun pixel peint au-delà de 121 + 4 pt (le halo éteint).

  python3 redteam_plein.py
Preuve (§7) : `APP=http://127.0.0.1:8752/<copie de sauvegardes/app-avant-v120.html à la racine> python3 redteam_plein.py` ROUGIT
(alpha jusqu'à 109 au palier réduit).
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
D_PT, SILHOUETTE_PT, BOITE_PT, RETRAIT = 232.064, 121.0, 296.0, 0.04      # la décision, en dur
R_PLEIN = SILHOUETTE_PT - RETRAIT * D_PT                                   # 111,72 pt
PALETTES = ['signal', 'candide', 'irascible', 'taciturne']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-78s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}"""
MESURE = """([rp, rs, boite])=>{ const cv=document.getElementById('auBoule'), W=cv.width, k=W/boite, c=(W-1)/2, d=cv.getContext('2d').getImageData(0,0,W,W).data;
  let n=0, trous=0, amin=255, dehors=0; const R2=(rp*k)*(rp*k), S2=((rs+4)*k)*((rs+4)*k);
  for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const q=(x-c)*(x-c)+(y-c)*(y-c), a=d[(y*W+x)*4+3];
    if(q<=R2){ n++; if(a<255){ trous++; if(a<amin) amin=a; } } else if(q>S2 && a>8) dehors++; }
  return {W:W, n:n, trous:trous, amin:amin, dehors:dehors, palier:(()=>{try{return _aura.etat().palier}catch(e){return null}})()}; }"""

with sync_playwright() as p:
    b = p.webkit.launch()
    for dens in ('', '?densite=2', '?densite=3'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, reduced_motion='reduce')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
        pg.goto(APP + dens); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        npal = None
        for th in ('light', 'dark'):
            for pal in (PALETTES if not dens else PALETTES[:1]):
                pg.evaluate("([t,p])=>{ try{closeAll()}catch(e){} setTheme(t); try{Toile.setPalette(p)}catch(e){} }", [th, pal]); pg.wait_for_timeout(500)
                pg.evaluate(OUVRE); pg.wait_for_timeout(3200)
                for _ in range(40):          # un semis plus dense met plus longtemps à se bâtir : on attend que la boule soit PEINTE
                    if pg.evaluate("()=>{const c=document.getElementById('auBoule'); try{ return !!(c && c.width>400 && _aura.etat().pret); }catch(e){ return false; }}"): break
                    pg.wait_for_timeout(500)
                if npal is None: npal = pg.evaluate("()=>{try{return _aura.PALIERS.length}catch(e){return 3}}")
                for i in range(npal):
                    pg.evaluate("(i)=>{ window._peloteSansHalo=true; try{_aura.fige(true); _aura.palier(i);}catch(e){} }", i); pg.wait_for_timeout(2600)
                    m = pg.evaluate(MESURE, [R_PLEIN, SILHOUETTE_PT, BOITE_PT])
                    tag = '[%s · %s · %s · palier %s]' % (dens or 'densité 1', 'clair' if th == 'light' else 'sombre', pal, m['palier'])
                    t(tag + ' alpha = 255 en retrait de 4 % de D', m['trous'] == 0 and m['n'] > 10000, '%d pixels sous 255 sur %d%s' % (m['trous'], m['n'], (' · le plus bas : %d' % m['amin']) if m['trous'] else ''))
                    t(tag + ' la silhouette n\'a pas bougé (rien au-delà de 121 + 4 pt)', m['dehors'] == 0, '%d pixels' % m['dehors'])
        t('[%s] aucune erreur de page' % (dens or 'densité 1'), not er, '; '.join(er[:2]))
        ctx.close()
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:6]))
sys.exit(1 if ko else 0)
