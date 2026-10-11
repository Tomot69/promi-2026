#!/usr/bin/env python3
"""
redteam_ritournelle.py — RITOURNELLE, CE QU'ON VOIT AU DÉPART (v142, Tom, 11 oct. 2026 — C-088, RÉCIDIVE). Réécrit ; l'original de v141 :
sauvegardes/redteam_ritournelle-avant-v142.py.

« Les cibles se mesurent sur la zone réellement visible, entre le plateau du haut et la barre du bas, pas sur tout l'écran :
  de 1 à 3 paroles : on ne voit que ces dalles, aucune cellule vide, même en partie ; à 4 : deux ou trois cellules vides au plus ;
  ensuite, des vides en petit nombre, proportionnellement. »

POURQUOI LE JUGE DE v141 ÉTAIT VERT : il posait des paroles du jeu de démonstration par `Toile.sync`, appelait lui-même `Toile_recadre`, à
l'échelle 1, et comptait les cellules vides ENTIÈREMENT visibles. Tom plante au +, sur une Toile vide, et voit les cellules même en partie.

Ce juge passe par le banc « comme Tom » (banc_tom.py : WebKit, 390 × 844 ×3, navigateur non déclaré piloté, Toile vide, paroles plantées par
le +). Le verdict vient de la CAPTURE, dans la zone visible (y 100 → 710) : on y cherche les taches qui ne sont pas le fond ; une tache qui
porte le bleu d'un Promi est une dalle, une tache sans bleu est une cellule vide. Seuils EN DUR.

Usage : python3 redteam_ritournelle.py [fichier.html] [--planche]
"""
import sys, io
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
Y0, Y1 = 102, 708                      # la zone visible : sous le plateau (40 → 100), au-dessus de la barre (710 → 810)
VIDES_MAX = {1: 0, 2: 0, 3: 0, 4: 3, 6: 4}   # Tom : aucune de 1 à 3 ; « deux ou trois au plus » à 4 ; « en petit nombre, proportionnellement » ensuite
LARGEUR_MIN_1 = 234                    # une parole : sa dalle fait au moins 60 % de la largeur (v141, gardé)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def bleu(c): return abs(c[0] - 130) < 34 and abs(c[1] - 174) < 34 and abs(c[2] - 248) < 30
def taches(im):
    """les taches (composantes) qui ne sont pas le fond, dans la zone visible ; rend [(boîte, surface, porte du bleu)]"""
    px = im.load(); fond = px[4, Y0 + 2]; W, PAS = 390, 2
    def plein(x, y): c = px[x, y]; return abs(c[0] - fond[0]) + abs(c[1] - fond[1]) + abs(c[2] - fond[2]) > 30
    vu = {}; out = []
    for y in range(Y0, Y1, PAS):
        for x in range(0, W, PAS):
            if (x, y) in vu or not plein(x, y): continue
            pile = [(x, y)]; vu[(x, y)] = 1; b = [x, x, y, y]; n = 0; nb = 0
            while pile:
                cx, cy = pile.pop(); n += 1
                if bleu(px[cx, cy]): nb += 1
                if cx < b[0]: b[0] = cx
                if cx > b[1]: b[1] = cx
                if cy < b[2]: b[2] = cy
                if cy > b[3]: b[3] = cy
                for dx, dy in ((PAS, 0), (-PAS, 0), (0, PAS), (0, -PAS)):
                    q = (cx + dx, cy + dy)
                    if 0 <= q[0] < W and Y0 <= q[1] < Y1 and q not in vu and plein(*q): vu[q] = 1; pile.append(q)
            if n >= 12: out.append((b, n * PAS * PAS, nb > n * 0.05))
    return out
TITRES = ['boire un verre', 'appeler Mamie', 'courir dimanche', 'ranger le garage', 'écrire à Paul', 'lire un livre']
def verdict(n, im, quand):
    T = taches(im); D = [t for t in T if t[2]]; V = [t for t in T if not t[2]]
    juge('%d parole(s)%s : on voit %d dalle(s), entière(s), entre le plateau et la barre' % (n, quand, n),
         len(D) == n and all(t[0][0] > 1 and t[0][1] < 388 and t[0][2] > Y0 and t[0][3] < Y1 - 2 for t in D),
         '%d dalle(s) vue(s) : %s' % (len(D), [t[0] for t in D]))
    juge('%d parole(s)%s : %s' % (n, quand, 'aucune cellule vide, même en partie' if VIDES_MAX[n] == 0 else 'au plus %d cellules vides, même en partie' % VIDES_MAX[n]),
         len(V) <= VIDES_MAX[n], '%d cellule(s) vide(s) dans la zone visible : %s' % (len(V), [(t[0], t[1]) for t in V][:6]))
    if n == 1 and D: w = D[0][0][1] - D[0][0][0]; juge('une parole%s : sa dalle fait au moins 60 %% de la largeur' % quand, w >= LARGEUR_MIN_1, 'largeur peinte %d pt (%.0f %%)' % (w, w / 3.9))
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False,):
        ctx = contexte(b, sombre=sombre); pg = ouvre(ctx, F)
        pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(1500)
        for i, t in enumerate(TITRES):
            plante(pg, t); pg.wait_for_timeout(3200); n = i + 1
            if n in VIDES_MAX:
                im = image(pg); verdict(n, im, '')
                if '--planche' in sys.argv: capture(pg, 'planche-v142/rit-%s-%d.png' % (F.replace('.html', ''), n))
            if n == 3:      # et comme Tom la retrouve en rouvrant l'app
                pg.reload(); pg.wait_for_timeout(8000); verdict(3, image(pg), ' (app rouverte)')
        ctx.close()
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
