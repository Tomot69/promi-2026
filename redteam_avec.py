#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_avec.py — LA LIGNE « AVEC … » D'UN CERCLE NE DISPARAÎT PLUS (v183c, Tom, 7 nov. 2026 — C-252).
« Après un aller-retour dans le fil, la ligne « Avec … » disparaît (défaut existant depuis v181b). Corrige. Juge : 10 allers-retours, la ligne reste présente
à chaque fois. »
Banc WebKit (390 × 844 et 330 × 714) : la fiche d'un Cercle de six paroles ; dix allers-retours du haut jusqu'en bas du fil (défilement par pas, jusqu'à l'état
défilé et retour à 0) ; 1,5 s après chaque retour, la ligne est affichée (display, hauteur, texte « Avec … ») et son + des membres aussi. Rouge sur v183b.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %s  %s' % ('OK' if ok else 'KO', nom, str(d)[:200]), flush=True)
Q = """()=>{ const q=document.getElementById('dptQui'), b=document.getElementById('cerclePlusMembres'); const cs=getComputedStyle(q), r=q.getBoundingClientRect();
  return {vu: cs.display!=='none' && cs.visibility!=='hidden' && r.height>5 && /^Avec /.test((q.textContent||'').trim()), plus: !!(b && getComputedStyle(b).display!=='none' && getComputedStyle(b).visibility!=='hidden'), t:(q.textContent||'').trim().slice(0,28)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in ((390, 844, '×0,93'), (330, 714, '×0,79')):
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(3000)
        e0 = pg.evaluate(Q); juge('[%s] à l\'ouverture : la ligne « Avec … » est là' % nom, e0['vu'], e0)
        ok = 0; vus = []
        for i in range(10):
            for st in (60, 200, 400, 800, 400, 200, 60, 0):
                pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", st); pg.wait_for_timeout(180)
            pg.wait_for_timeout(1500); e = pg.evaluate(Q); vus.append(e['vu'] and e['plus']); ok += 1 if (e['vu'] and e['plus']) else 0
        juge('[%s] 10 allers-retours : la ligne « Avec … » et son + présents à chaque retour (%d / 10)' % (nom, ok), ok == 10, vus)
        ctx.close()
    b.close()
print('\n%d / %d' % (sum(res), len(res)))
