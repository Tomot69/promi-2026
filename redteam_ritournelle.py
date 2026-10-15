#!/usr/bin/env python3
"""
redteam_ritournelle.py — RITOURNELLE : LA RÈGLE DES 75 %, LE BUG À UNE DALLE (v146, Tom, 14 oct. 2026 — C-088 rouvert à sa demande).
« À 1 dalle, la Toile est vide, il y a juste un texte qui flotte. À 3 dalles, on ne voit même pas 10 % de chaque dalle. C'est joli, mais dézoome
  légèrement. » La règle, EN DUR :
  · de 1 à 9 paroles : chaque dalle de parole est visible sur au moins 75 % de sa surface ; les dalles de paroles couvrent au moins 75 % de l'écran ;
    pas de couronne de dalles vides autour ;
  · à partir de 10 : AUCUN saut — pas de « pof », pas de gros dézoom d'un coup ; le dézoom est progressif, parole après parole, et la règle des 75 %
    s'applique autant que la place le permet ;
  · le caractère arty du cadrage restauré (grandes formes) est gardé.
Réécrit au niveau de cette décision ; l'original de v145 : sauvegardes/redteam_ritournelle-avant-v146.py (il portait le cadrage d'E1 et constatait,
sans le juger, qu'une parole seule ne peignait rien).

Par le banc « comme Tom » (WebKit, 390 × 844 ×3, Toile vide, paroles plantées par le +), de 1 à 15 paroles, après chaque plantation :
  A · la Toile n'a que ses paroles (autant de graines que de paroles, aucune cellule vide) — pas de couronne ;
  B · « l'écran » est la zone visible, du bas du plateau (y 100) au haut de la barre (y 710). La SURFACE d'une dalle est sa coulée peinte : le peintre
      publie son contour (`window._ritFormes`, 48 points par coulée) ; la part visible = ce qui en reste dans la zone, sous les coulées peintes après
      elle (deux paroles confondues sur une même graine : la première est à 0 %) sur son aire entière ;
      la couverture = la part de la zone sous l'union des contours. Seuils EN DUR : 75 % et 75 % de 1 à 9 ; de 10 à 15, 70 % et 70 % (« autant que
      la place le permet » : un plancher, pas une cible) ;
  C · la couverture se vérifie AUSSI sur l'image : la part de la zone qui n'est pas le fond de la Toile ;
  D · une parole seule PEINT sa coulée (≥ 75 % de la zone hors du fond, lu sur l'image) ;
  E · aucun saut : d'une parole à la suivante, l'échelle de la vue ne change pas de plus de 8 % (9 → 10 compris), et la surface moyenne d'une coulée
      ne baisse jamais de plus de 15 points au-delà du partage attendu (n/(n+1) : la même zone partagée en une parole de plus) — elle baisse parole
      après parole, sans « pof » ;
  F · toucher une dalle ouvre sa fiche (au point de chaque graine visible, à 6 et à 12 paroles).
La planche : planche-v146/PLANCHE-10-ritournelle-1-15.png (les quinze captures, dans l'ordre).
Preuve (§7) : `zz-avant-v146.html` (le moteur de v145) — D rougit (rien n'est peint à une parole), B rougit (3 à 40 % de chaque coulée à l'écran).
Usage : python3 redteam_ritournelle.py [fichier.html] [--n=15]
"""
import sys
sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
NMAX = int(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--n=')), '15'))
Z = (0, 100, 390, 710)
VIS, COUV, VIS10, COUV10, PAS_ECHELLE, BAISSE = 0.75, 0.75, 0.70, 0.70, 0.08, 0.15
TITRES = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche', 'appeler mamie', 'finir la maquette', 'ranger le garage', 'faire les crêpes', 'réparer le vélo',
          'trier les photos', 'semer les radis', 'nager le mardi', 'lire Proust', 'planter un arbre', 'écrire à Paul', 'peindre la porte']
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def aire(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2
def coupe(P, x0, y0, x1, y1):
    def clip(P, dedans, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if dedans(b):
                if not dedans(a): out.append(inter(a, b))
                out.append(b)
            elif dedans(a): out.append(inter(a, b))
        return out
    ix = lambda xv: (lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / ((b[0] - a[0]) or 1e-9)))
    iy = lambda yv: (lambda a, b: (a[0] + (b[0] - a[0]) * (yv - a[1]) / ((b[1] - a[1]) or 1e-9), yv))
    for d, it in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        P = clip(P, d, it)
        if not P: return []
    return P
def formes(e):
    """part VISIBLE de chaque coulée — dans la zone ET non recouverte par une coulée peinte après elle (l'ordre du peintre) —, couverture de la zone
    par leur union, aire moyenne (points²). Rastérisé à 2 px par point sur [-30, 420] × [50, 760] : les coulées y tiennent (le cadre est −6 → 396, 88 → 716)."""
    s, ox, oy = e['vue']; K = 2; X0, Y0, X1, Y1 = -30, 50, 420, 760; Wd, Hd = (X1 - X0) * K, (Y1 - Y0) * K
    im = Image.new('I', (Wd, Hd), 0); d = ImageDraw.Draw(im); aires = []; tot = []
    for k, f in enumerate(e['formes']):
        p = f['pts']; P = [((ox + s * p[i] - X0) * K, (oy + s * p[i + 1] - Y0) * K) for i in range(0, len(p), 2)]
        one = Image.new('L', (Wd, Hd), 0); ImageDraw.Draw(one).polygon(P, fill=1); tot.append(sum(one.getdata())); aires.append(aire(P) / (K * K))
        d.polygon(P, fill=k + 1)
    px = im.load(); vu = [0] * len(tot); couv = 0; zx0, zy0, zx1, zy1 = (Z[0] - X0) * K, (Z[1] - Y0) * K, (Z[2] - X0) * K, (Z[3] - Y0) * K
    for y in range(zy0, zy1):
        for x in range(zx0, zx1):
            v = px[x, y]
            if v: couv += 1; vu[v - 1] += 1
    vis = [vu[k] / float(tot[k]) if tot[k] else 0.0 for k in range(len(tot))]
    return vis, couv / float((zx1 - zx0) * (zy1 - zy0)), (sum(aires) / len(aires) if aires else 0)
def matiere(im):
    """la part de la zone visible qui n'est pas le fond de la Toile (#DFCAA4 en clair)"""
    px = im.load(); n = t = 0
    for y in range(Z[1], Z[3], 3):
        for x in range(Z[0], Z[2], 3):
            c = px[x, y]; t += 1
            if abs(c[0] - 223) + abs(c[1] - 202) + abs(c[2] - 164) > 30: n += 1
    return n / float(t)
def touche(pg, g):
    ouvertes = essais = 0
    for q in g:
        x, y = q[1], q[2]
        if not (120 < y < 690 and 12 < x < 378): continue
        essais += 1; pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500); B.tap(pg, x, y); pg.wait_for_timeout(1400)
        if pg.evaluate("()=>{ var d=document.getElementById('detailPoster'); return !!(d && d.classList.contains('show')); }"): ouvertes += 1
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
    return ouvertes, essais
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500); L = []; IM = []
    for i in range(NMAX):
        B.plante(pg, TITRES[i]); pg.wait_for_timeout(5200)
        q = "()=>{ var v=Toile.vue(); return {vue:[v.s,v.ox,v.oy], formes:(window._ritFormes||[]).slice(), g:Toile_graines(), neuf:(Toile.semisNeuf?Toile.semisNeuf():null), n:promises.filter(p=>!p.draft).length}; }"
        e = pg.evaluate(q)
        if len(e['formes']) != e['n']: pg.wait_for_timeout(1800); e = pg.evaluate(q)
        n = e['n']; im = B.image(pg); IM.append(im); vis, cov, am = formes(e) if e['formes'] else ([0.0], 0.0, 0)
        mat = matiere(im); L.append({'n': n, 's': e['vue'][0], 'am': am})
        juge('A · %2d parole(s) : la Toile n\'a que ses paroles — aucune cellule vide, pas de couronne' % n, n == i + 1 and len(e['g']) == n and e['neuf'] is True and all(g[3] != 'gray' for g in e['g']), '%d graine(s)' % len(e['g']))
        v0, c0 = (VIS, COUV) if n <= 9 else (VIS10, COUV10)
        juge('B · %2d parole(s) : chaque coulée visible à ≥ %d %%, et les coulées couvrent ≥ %d %% de l\'écran (plateau → barre)' % (n, v0 * 100, c0 * 100), len(e['formes']) == n and min(vis) >= v0 and cov >= c0,
             'visible : la moindre %.0f %%, médiane %.0f %% · couverture %.0f %% · échelle %.3f' % (100 * min(vis), 100 * sorted(vis)[len(vis) // 2], 100 * cov, e['vue'][0]))
        juge('C · %2d parole(s) : sur l\'image, la matière couvre ≥ %d %% de la zone' % (n, c0 * 100), mat >= c0, '%.0f %% hors du fond' % (100 * mat))
        if n == 1: juge('D · une parole seule PEINT sa coulée (≥ 75 % de la zone, lu sur l\'image) — plus de « texte qui flotte »', mat >= 0.75, '%.0f %% hors du fond' % (100 * mat))
        if n in (6, 12):
            o, es = touche(pg, e['g']); juge('F · %d paroles : toucher une dalle ouvre sa fiche (au point de chaque graine visible)' % n, es >= 2 and o == es, '%d sur %d' % (o, es))
    for a, c in zip(L, L[1:]):
        ech = abs(c['s'] / a['s'] - 1) if a['s'] else 9; baisse = 1 - c['am'] / a['am'] if a['am'] else 1; att = 1 - a['n'] / float(c['n'])
        juge('E · %2d → %2d paroles : aucun saut — l\'échelle change de ≤ %d %%, la surface moyenne d\'une coulée baisse au plus de 15 points de plus que le partage attendu (%.0f %%)%s' % (a['n'], c['n'], PAS_ECHELLE * 100, att * 100, ' (le passage à dix)' if c['n'] == 10 else ''),
             ech <= PAS_ECHELLE and baisse <= att + BAISSE, 'échelle %.3f → %.3f · coulée moyenne %.0f → %.0f pt² (%+.0f %%)' % (a['s'], c['s'], a['am'], c['am'], -100 * baisse))
    juge('aucune erreur de page', not pg.erreurs, str(pg.erreurs[:2]))
    if IM:
        w, h = 260, 563; P = Image.new('RGB', (5 * (w + 10), 3 * (h + 10)), 'white')
        for k, im in enumerate(IM): P.paste(im.convert('RGB').resize((w, h)), ((k % 5) * (w + 10), (k // 5) * (h + 10)))
        P.save('planche-v146/PLANCHE-10-ritournelle-1-15%s.png' % ('' if F == 'app.html' else '-' + F.split('.')[0]))
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:900])
sys.exit(0 if ok == len(res) else 1)
