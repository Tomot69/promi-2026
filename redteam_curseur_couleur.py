#!/usr/bin/env python3
"""redteam_curseur_couleur.py — ⚑ v155 (Tom, C-168) : LA DALLE DE LA JAUGE DES COULEURS S'ATTRAPE.

« Agrandis sa zone tactile, sans changer son dessin : au moins 56 × 56 pt, centrée sur la dalle. Elle ne doit pas voler les touchers des éléments
voisins. Juge : attraper la dalle à 20 pt de son centre fonctionne ; les éléments voisins répondent toujours. »
Banc comme Tom (WebKit 390 × 844 ×3, le doigt) : le Studio, les palettes dépliées (un ton touché).
  A · la zone : ce qui est sous le doigt à ± 27 pt du centre de la dalle (quatre côtés, quatre coins) est la dalle (`elementFromPoint`)
  B · attraper à 20 pt du centre (au-dessus, au-dessous, à gauche, à droite, en diagonale) puis glisser de 60 pt : la dalle ne saute pas au toucher
      (≤ 2 pt) et suit le doigt (+60 pt ± 4) ; la teinte change
  C · de même jauge noir et blanc allumée (la dalle dose le gris)
  D · le dessin ne change pas : la dalle fait toujours 30 × 30 pt
  E · les voisins répondent : une pastille de la dernière rangée change la palette ; le bouton noir et blanc s'allume ; le nom de la palette n'est pas pris
Preuve : `--fichier=zz-av154.html` rougit (A, B).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
R = "(s)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [(r.left-D.left)/k, (r.top-D.top)/k, r.width/k, r.height/k]; }"
def centre(pg, s): r = pg.evaluate(R, s); return (r[0] + r[2] / 2, r[1] + r[3] / 2) if r else None
def sous(pg, x, y): return pg.evaluate("([x,y])=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const e=document.elementFromPoint(D.left+x*k, D.top+y*k); return e?(e.id||e.className||e.tagName):null; }", [x, y])
def ouvre_palettes(b):
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
    return ctx, pg
def milieu(pg):
    s = pg.evaluate(R, '#st3spec'); B.glisse(pg, [[s[0] + s[2] / 2, s[1] + s[3] / 2]], pas=20); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx, pg = ouvre_palettes(b); milieu(pg)
    cx, cy = centre(pg, '#st3thumb'); th = pg.evaluate(R, '#st3thumb')
    pts = [(cx + dx, cy + dy) for dx, dy in ((0, -27), (0, 27), (-27, 0), (27, 0), (-26, -26), (26, -26), (-26, 26), (26, 26))]
    pris = [sous(pg, x, y) for x, y in pts]
    juge('A · à ± 27 pt du centre de la dalle (quatre côtés, quatre coins), le doigt tombe sur la dalle', all(s == 'st3thumb' or (s or '').startswith('st3-thumb') for s in pris), pris)
    juge('D · le dessin ne change pas : la dalle fait 30 × 30 pt', abs(th[2] - 30) < 0.6 and abs(th[3] - 30) < 0.6, '%.1f × %.1f' % (th[2], th[3]))
    for nom, (dx, dy) in (('au-dessus', (0, -20)), ('au-dessous', (0, 20)), ('à gauche', (-20, 0)), ('à droite', (20, 0)), ('en diagonale', (-14, 14))):
        milieu(pg); cx, cy = centre(pg, '#st3thumb'); h0 = pg.evaluate("()=>Toile.mondeCourant().h")
        x0, y0 = cx + dx, cy + dy
        pg.evaluate("()=>{ window.__thx=[]; const th=document.getElementById('st3thumb'); const o=new MutationObserver(()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=th.getBoundingClientRect(); window.__thx.push((r.left-D.left)/k+r.width/k/2); }); o.observe(th,{attributes:true}); window.__tho=o; }")
        B.glisse(pg, [[x0 + 60 * i / 12, y0] for i in range(13)], pas=20); pg.wait_for_timeout(700)
        L = pg.evaluate("()=>{ window.__tho.disconnect(); return window.__thx; }"); h1 = pg.evaluate("()=>Toile.mondeCourant().h")
        L = [v for i, v in enumerate(L) if i == 0 or abs(v - L[i - 1]) > 0.01]   # le glissé (après le lever, la dalle file sur son élan : on lit la position au dernier pas du doigt)
        saut = abs(L[0] - (cx + 5)) if L else 99; cx1 = L[11] if len(L) > 11 else (L[-1] if L else cx)
        juge('B · attrapée à 20 pt %s puis glissée de 60 pt : aucun saut au toucher (le premier pas : 5 pt ± 2), elle suit le doigt (+60 ± 4 au dernier pas), la teinte change' % nom,
             bool(L) and saut <= 2 and abs((cx1 - cx) - 60) <= 4 and h1 != h0, 'saut au toucher %.1f pt · déplacement %.1f pt · teinte %s → %s' % (saut, cx1 - cx, h0, h1))
    # C · noir et blanc
    c = centre(pg, '.stp-nb'); B.tap(pg, c[0], c[1]); pg.wait_for_timeout(600)
    on = pg.evaluate("()=>document.querySelector('.stp-nb').getAttribute('aria-pressed')")
    juge('E · le bouton noir et blanc répond au toucher (il s\'allume)', on == 'true', on)
    milieu(pg); cx, cy = centre(pg, '#st3thumb'); j0 = pg.evaluate("()=>localStorage.getItem('promi_nb_j')")
    B.glisse(pg, [[cx + 60 * i / 12, cy - 20] for i in range(13)], pas=20); pg.wait_for_timeout(600)
    cx1, _ = centre(pg, '#st3thumb'); j1 = pg.evaluate("()=>localStorage.getItem('promi_nb_j')")
    juge('C · noir et blanc allumé : attrapée à 20 pt au-dessus et glissée de 60 pt, elle suit (+60 ± 4) et dose le gris', abs((cx1 - cx) - 60) <= 4 and j1 != j0, 'déplacement %.1f pt · gris %s → %s' % (cx1 - cx, j0, j1))
    c = centre(pg, '.stp-nb'); B.tap(pg, c[0], c[1]); pg.wait_for_timeout(600)
    # E · une pastille de la dernière rangée
    p0 = pg.evaluate("()=>Toile.mondeCourant().p")
    r = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const P=[...document.querySelectorAll('#stpPals .st3-p')]; const e=P.slice(-6).find(x=>!x.classList.contains('on')); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k-3, e.dataset.p]; }")
    B.tap(pg, r[0], r[1]); pg.wait_for_timeout(900)
    p1 = pg.evaluate("()=>Toile.mondeCourant().p")
    juge('E · une pastille de la dernière rangée (touchée à 3 pt de son bas) change la palette', p1 == r[2] and p1 != p0, '%s → %s (visée %s)' % (p0, p1, r[2]))
    s = pg.evaluate(R, '#st3pn'); q = sous(pg, s[0] + 8, s[1] + s[3] / 2)
    juge('E · le nom de la palette, à gauche de la zone, n\'est pas pris par la dalle', q != 'st3thumb', q)
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page', not er, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
