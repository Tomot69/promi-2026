#!/usr/bin/env python3
"""
redteam_ritournelle.py — RITOURNELLE, CE QU'ON VOIT AU DÉPART (v143, Tom, 12 oct. 2026 — C-088, RÉCIDIVE). Réécrit ; l'original de v142 :
sauvegardes/redteam_ritournelle-avant-v143.py (« de 1 à 3 paroles, aucune cellule vide, même en partie » — obtenu en ne peignant plus les
cellules vides : les premières dalles prenaient tout l'écran, et la Toile sans parole devenait un aplat, noir en sombre).

LES CIBLES DE TOM, EN DUR, dans la zone visible entre le plateau et la barre (y 100 → 710, 390 pt de large) :
  · 1 parole : sa dalle entière, centrée, entre 50 et 60 % de la largeur (195 à 234 pt), avec un peu de Toile autour — des bords de cellules
    vides, pas une cellule vide entière ;
  · 2 et 3 paroles : toutes entières, ensemble entre 70 et 85 % de la largeur (273 à 331,5 pt), un peu de Toile autour ;
    ⚠ deux dalles l'une AU-DESSUS de l'autre ne peuvent pas faire 70 % de large sans sortir de la zone : l'ensemble fait alors entre 70 et 85 %
    de la HAUTEUR de la zone (427 à 518 pt) — c'est la même cible sur l'autre axe, et le juge dit lequel il a jugé ;
  · 4 paroles : toutes entières, deux ou trois cellules vides entières au plus ;
  · 6 paroles : peu de vides, proportionnellement (cinq cellules vides entières au plus) ;
  · sans parole : la Toile est PEINTE (des cellules vides partout), en clair et en sombre — jamais un aplat.
Par le banc « comme Tom » (WebKit, 390 × 844 ×3, Toile vide, paroles plantées par le +, app ROUVERTE avant chaque mesure). Le verdict vient de la
CAPTURE : une dalle est une tache de bleu Promi ; une cellule vide est une tache qui se détache du fond (la couleur la plus fréquente de la
zone) et ne porte pas de bleu ; elle est « entière » si sa boîte ne touche aucun bord de la zone.
Captures annotées (cotes) : planche-v143/rit-<fichier>-<n>.png.     Usage : python3 redteam_ritournelle.py [fichier.html]
"""
import sys, io
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
Y0, Y1 = 102, 708
ZH = Y1 - Y0
VIDES_ENTIERES_MAX = {1: 0, 2: 2, 3: 2, 4: 3, 6: 5}
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def bleu(c): return abs(c[0] - 130) < 34 and abs(c[1] - 174) < 34 and abs(c[2] - 248) < 30
def composantes(px, test, pas=2):
    vu = {}; out = []
    for y in range(Y0, Y1, pas):
        for x in range(0, 390, pas):
            if (x, y) in vu or not test(px[x, y]): continue
            pile = [(x, y)]; vu[(x, y)] = 1; b = [x, x, y, y]; n = 0
            while pile:
                cx, cy = pile.pop(); n += 1
                if cx < b[0]: b[0] = cx
                if cx > b[1]: b[1] = cx
                if cy < b[2]: b[2] = cy
                if cy > b[3]: b[3] = cy
                for dx, dy in ((pas, 0), (-pas, 0), (0, pas), (0, -pas)):
                    q = (cx + dx, cy + dy)
                    if 0 <= q[0] < 390 and Y0 <= q[1] < Y1 and q not in vu and test(px[q[0], q[1]]): vu[q] = 1; pile.append(q)
            out.append((b, n * pas * pas))
    return out
def lit(im):
    """rend (dalles, cellules vides, cellules vides entières) — des boîtes [x0, x1, y0, y1] en points de l'appareil"""
    px = im.load(); H = {}
    for y in range(Y0, Y1, 3):
        for x in range(0, 390, 3): c = px[x, y]; k = (c[0] // 6, c[1] // 6, c[2] // 6); H[k] = H.get(k, 0) + 1
    k = max(H, key=H.get); fond = (k[0] * 6 + 3, k[1] * 6 + 3, k[2] * 6 + 3)
    D = [b for b, n in composantes(px, bleu) if n >= 600]
    # un titre qui déborde de son cœur traverse l'anneau bleu et le coupe en deux taches : deux taches superposées, séparées par autre chose que
    # le FOND (le titre, le cœur crème), sont la même dalle — deux dalles voisines, elles, sont séparées par le fond
    est_fond = lambda c: abs(c[0] - fond[0]) + abs(c[1] - fond[1]) + abs(c[2] - fond[2]) <= 16
    fini = False
    while not fini:
        fini = True
        for i in range(len(D)):
            for j in range(i + 1, len(D)):
                a_, b_ = D[i], D[j]; ox0 = max(a_[0], b_[0]); ox1 = min(a_[1], b_[1])
                if ox1 - ox0 < 0.6 * min(a_[1] - a_[0], b_[1] - b_[0]): continue
                haut, bas = (a_, b_) if a_[2] <= b_[2] else (b_, a_); gap = bas[2] - haut[3]
                if gap > 26 or gap <= 0: continue          # deux boîtes qui se chevauchent en hauteur sont deux dalles voisines, jamais les moitiés d'une dalle coupée par son titre
                if any(est_fond(px[int(ox0 + (ox1 - ox0) * q), y]) for q in (0.25, 0.5, 0.75) for y in range(haut[3] + 1, bas[2])): continue
                D[i] = [min(a_[0], b_[0]), max(a_[1], b_[1]), min(a_[2], b_[2]), max(a_[3], b_[3])]; del D[j]; fini = False; break
            if not fini: break
    def vide(c): return (not bleu(c)) and abs(c[0] - fond[0]) + abs(c[1] - fond[1]) + abs(c[2] - fond[2]) > 16
    dedans = lambda b: any(b[0] >= d[0] and b[1] <= d[1] and b[2] >= d[2] and b[3] <= d[3] for d in D)
    V = [b for b, n in composantes(px, vide) if n >= 500 and not dedans(b)]
    # une cellule « entière » fait au moins 56 pt de côté : plus petite, c'est le CŒUR d'une cellule dont le pourtour a la couleur du fond
    # (mesuré : 46 × 40 pt — une cellule de Ritournelle fait 80 pt et plus, même à six paroles)
    E = [b for b in V if b[0] > 1 and b[1] < 388 and b[2] > Y0 and b[3] < Y1 - 2 and (b[1] - b[0]) >= 56 and (b[3] - b[2]) >= 56]
    return D, V, E, fond
def annote(pg, chemin, D, V, E, texte):
    im = Image.open(io.BytesIO(capture(pg))).convert('RGB'); k = im.width / 390.0; g = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(11 * k))
    except Exception: f = None
    g.line([(0, 100 * k), (im.width, 100 * k)], fill=(221, 77, 35), width=2); g.line([(0, 710 * k), (im.width, 710 * k)], fill=(221, 77, 35), width=2)
    for b in E: g.rectangle([b[0] * k, b[2] * k, b[1] * k, b[3] * k], outline=(221, 77, 35), width=3)
    if D:
        x0 = min(d[0] for d in D); x1 = max(d[1] for d in D); y0 = min(d[2] for d in D); y1 = max(d[3] for d in D)
        g.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=(32, 25, 8), width=3)
        g.rectangle([x0 * k, (y1 + 4) * k, (x0 + 250) * k, (y1 + 20) * k], fill=(247, 240, 222)); g.text(((x0 + 3) * k, (y1 + 5) * k), texte, fill=(32, 25, 8), font=f)
    im.save(chemin)
def verdict(n, pg, quand=''):
    D, V, E, fond = lit(image(pg)); nom = '%d parole(s)%s' % (n, quand)
    ent = len(D) == n and all(d[0] > 1 and d[1] < 388 and d[2] > Y0 and d[3] < Y1 - 2 for d in D)
    juge('%s : on voit %d dalle(s), entière(s), entre le plateau et la barre' % (nom, n), ent, '%d dalle(s) : %s' % (len(D), D))
    if not D: return
    x0 = min(d[0] for d in D); x1 = max(d[1] for d in D); y0 = min(d[2] for d in D); y1 = max(d[3] for d in D); w = x1 - x0; h = y1 - y0; cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    txt = '%d × %d pt · %.0f %% de la largeur · %d vide(s) entière(s)' % (w, h, w / 3.9, len(E))
    if n == 1:
        juge('%s : sa dalle fait entre 50 et 60 %% de la largeur (195 à 234 pt)' % nom, 195 <= w <= 234, 'largeur peinte %d pt (%.0f %%)' % (w, w / 3.9))
        juge('%s : elle est centrée (à 20 pt près en largeur, 40 en hauteur de la zone)' % nom, abs(cx - 195) <= 20 and abs(cy - (Y0 + Y1) / 2) <= 40, 'centre (%.0f, %.0f) pour (195, %d)' % (cx, cy, (Y0 + Y1) / 2))
    elif n in (2, 3):
        enL = 273 <= w <= 331.5; enH = 0.70 * ZH <= h <= 0.85 * ZH
        juge('%s : ensemble entre 70 et 85 %% de la largeur — ou, empilées, de la hauteur de la zone' % nom, (enL and h <= 0.85 * ZH) or (enH and w <= 331.5), 'ensemble %d × %d pt : %.0f %% de la largeur, %.0f %% de la hauteur de la zone — jugé sur %s' % (w, h, w / 3.9, 100.0 * h / ZH, 'la largeur' if enL else 'la hauteur'))
    if n in (1, 2, 3):
        juge('%s : un peu de Toile autour (au moins deux cellules vides visibles en partie)' % nom, len(V) >= 2, '%d cellule(s) vide(s) visibles, dont %d entière(s)' % (len(V), len(E)))
    juge('%s : %s' % (nom, 'aucune cellule vide ENTIÈRE' if VIDES_ENTIERES_MAX[n] == 0 else 'au plus %d cellules vides entières' % VIDES_ENTIERES_MAX[n]), len(E) <= VIDES_ENTIERES_MAX[n], '%d entière(s) : %s' % (len(E), E[:6]))
    annote(pg, 'planche-v143/rit-%s-%d%s.png' % (F.replace('.html', ''), n, '-rouverte' if quand else ''), D, V, E, txt)
TITRES = ['boire un verre', 'appeler Mamie', 'courir dimanche', 'ranger le garage', 'écrire à Paul', 'lire un livre', 'faire les crêpes', 'planter un arbre', 'réparer le vélo']
with sync_playwright() as p:
    b = p.webkit.launch()
    # sans parole : la Toile est peinte, dans les deux thèmes
    for sombre in (False, True):
        ctx = contexte(b, sombre=sombre); pg = ouvre(ctx, F)
        pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(2500)
        D, V, E, fond = lit(image(pg))
        juge('sans parole [%s] : la Toile est peinte (au moins huit cellules vides visibles), jamais un aplat' % ('sombre' if sombre else 'clair'), len(V) >= 8, '%d cellule(s) vide(s) · fond %s' % (len(V), fond))
        capture(pg, 'planche-v143/rit-%s-0-%s.png' % (F.replace('.html', ''), 'sombre' if sombre else 'clair')); ctx.close()
    ctx = contexte(b); pg = ouvre(ctx, F)
    pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(1500)
    for i, t in enumerate(TITRES):
        plante(pg, t); pg.wait_for_timeout(3200); n = i + 1
        if n in VIDES_ENTIERES_MAX:
            verdict(n, pg)
            pg.reload(); pg.wait_for_timeout(7500); verdict(n, pg, ' (app rouverte)')
        if n == 9: pg.reload(); pg.wait_for_timeout(7500); capture(pg, 'planche-v143/rit-%s-9.png' % F.replace('.html', ''))
    juge('aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    ctx.close(); b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
