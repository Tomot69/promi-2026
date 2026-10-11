#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_barre.py — CHAQUE ENTRÉE DE LA BARRE OUVRE SA PAGE (v143, Tom, 12 oct. 2026 — C-106 : « toucher STUDIO ouvre parfois l'Aura »).

LA CAUSE NOMMÉE : chaque entrée faisait 90 pt de large pour des centres à 54 pt — STUDIO (x 25 → 115) et AURA (79 → 169) se chevauchaient de
36 pt, AURA au-dessus : la moitié droite du mot STUDIO ouvrait l'Aura (de même INDEX / FIL).

Comme Tom (banc_tom : WebKit, 390 × 844 ×3, vrai toucher), CINQUANTE touchers par entrée, répartis sur TOUT ce qu'on en voit — la boîte de son
icône et de son mot, 3 pt de marge — et non sur son centre : c'est au bord du mot que le défaut vivait. Chaque toucher doit ouvrir la bonne
page (lue sur ce qui est DEVANT, au milieu de l'écran). 50 sur 50, EN DUR.
Preuve : rouge sur v142 (python3 redteam_barre.py zz-av143.html).     --n=20 pour une passe courte.
"""
import sys, random
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 50))
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:300]), flush=True)
VU = """(id)=>{ const e=document.getElementById(id); if(!e) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
  const L=id==='createBtn'?[e]:[...e.querySelectorAll('svg, .l')]; L.forEach(n=>{ const r=n.getBoundingClientRect(); if(r.width<2) return; x0=Math.min(x0,r.left); x1=Math.max(x1,r.right); y0=Math.min(y0,r.top); y1=Math.max(y1,r.bottom); });
  return [(x0-D.left)/k,(x1-D.left)/k,(y0-D.top)/k,(y1-D.top)/k]; }"""
DEVANT = """()=>{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); if(!h) return 'rien';
  const ch=document.getElementById('accChoix'); if(ch&&ch.classList.contains('ouvert')) return 'plus';
  const s=h.closest('.screen, .sheet, .poster, #feedView, #indexSheet, #createSheet'); return s? s.id : 'accueil'; }"""
FERME = """()=>{ try{ const c=document.getElementById('accChoix'); if(c) c.classList.remove('ouvert'); }catch(e){}
  try{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); const s=h&&h.closest('.screen, #feedView, #indexSheet');
    const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{ closeAll(); }catch(e){} }"""
ATTENDU = {'studioBtn': ('studioScreen',), 'souffleBtn': ('auraScreen',), 'createBtn': ('plus', 'createSheet'), 'indexBtn': ('indexSheet',), 'filBtn': ('feedView',)}
random.seed(143)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    for t in ('arroser le figuier', 'écrire à Lou'): plante(pg, t)
    pg.evaluate(FERME); pg.wait_for_timeout(600)
    for bid, att in ATTENDU.items():
        bx = pg.evaluate(VU, bid)
        if not bx: juge('%s : l\'entrée est dans la barre' % bid, False); continue
        ok = 0; faux = []
        for i in range(N):
            if bid == 'createBtn':
                import math
                a = random.random() * 6.283; r = 30 * math.sqrt(random.random()); x = (bx[0] + bx[1]) / 2 + r * math.cos(a); y = (bx[2] + bx[3]) / 2 + r * math.sin(a)
            else:
                x = random.uniform(bx[0] - 3, bx[1] + 3); y = random.uniform(bx[2] - 3, bx[3] + 3)
            tap(pg, x, y); pg.wait_for_timeout(900); d = pg.evaluate(DEVANT)
            if d in att: ok += 1
            else: faux.append((round(x), round(y), d))
            pg.evaluate(FERME); pg.wait_for_timeout(700)
            d0 = pg.evaluate(DEVANT)
            if d0 != 'accueil': pg.evaluate(FERME); pg.wait_for_timeout(900)
        juge('%s : %d touchers sur ce qu\'on en voit (x %d → %d, y %d → %d) ouvrent sa page, %d sur %d' % (bid, N, bx[0] - 3, bx[1] + 3, bx[2] - 3, bx[3] + 3, N, N), ok == N, '%d sur %d · à côté : %s' % (ok, N, faux[:8]))
    Z = pg.evaluate("()=>['studioBtn','souffleBtn','indexBtn','filBtn'].map(i=>{const r=document.getElementById(i).getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [Math.round((r.left-D.left)/k), Math.round((r.right-D.left)/k)]})")
    juge('les zones de toucher voisines ne se chevauchent pas (STUDIO / AURA, INDEX / FIL)', Z[0][1] <= Z[1][0] + 0.5 and Z[2][1] <= Z[3][0] + 0.5, Z)
    juge('aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    ctx.close(); b.close()
n = sum(1 for _, c in res if c); print('\n%d/%d' % (n, len(res)))
if n < len(res): sys.exit(1)
