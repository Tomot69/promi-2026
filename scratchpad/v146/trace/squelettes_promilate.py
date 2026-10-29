#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
squelettes_promilate.py — v170 (C-125) : LES LIGNES MÉDIANES DES CAPITALES DE PromiLate, DESSINÉES.

Pourquoi : PromiLate est une police très grasse (des traits de 300 unités pour 700 de haut). L'amincissement automatique (squelette.py) y
perd des traits entiers — l'élagage prend pour une « barbe » tout bras plus court que l'épaisseur du trait : la barre du T, la jambe droite
du N, la moitié du W — ou les emmêle (le M). Les pixels sans chemin se rattachaient au trait le plus proche et paraissaient d'un bloc.

Ici chaque capitale est décrite par son GRAPHE : des nœuds (bouts, embranchements, coins) et des arêtes (polylignes, en unités de police,
y vers le haut). Les points sont posés à la main à partir des coupes de l'encre (scratchpad/v170/runs.py), puis :
  · chaque point d'une arête est RECENTRÉ entre les deux bords de l'encre, perpendiculairement à l'arête (deux passes), puis lissé ;
  · un bout libre est prolongé jusqu'au bord de l'encre le long de sa direction ;
  · la demi-largeur R d'une arête est la distance au bord, médiane le long de l'arête (loin de ses bouts) ;
  · les droites passent par `chemins.redresse` (droites exactes, recentrées), comme pour les deux autres polices.
Le parcours (R1, R2, variantes h / b) reste celui de chemins.py : rien n'est imposé ici que la géométrie.
"""
import math
import numpy as np
import squelette as S

# nœud : (x, y) ; arête : [a, [points intermédiaires], b] ; 'courbes' : indices d'arêtes à recentrer (les autres sont des droites) ;
# 'boucle' : une arête fermée sans nœud (l'anneau du O)
RK_M = 1.0
RK_ANNEAU = 1.3
RK_SP = 1.0
RK_H = 1.1
RK_A = 0.65
RK_JA = 1.3
DESSINS = {
 'A': dict(n=dict(L0=(196, -8), R0=(822, -8), BL=(276, 240), BR=(752, 240), AP=(530, 640), Bd=(560, 240)),
           # v170b : la barre centrée sur l'encre qu'elle seule couvre — de l'encoche du bas (y 151) au bas du contre-poinçon (y 328) ; `brut` : pas de
           # redressement (il la remontait à y 286 : elle dépassait le contre-poinçon et manquait le bas)
           # la barre finit au bord du contre-poinçon (x 560), sans prolongement (`fixe`, `nx`) : jusqu'à l'axe du jambage droit, elle dévoilait ce jambage
           # avant lui et touchait en biseau le bord du jambage gauche (une pointe pincée)
           e=[['L0', [], 'BL'], ['BL', [(344, 375)], 'AP'], ['AP', [(706, 375)], 'BR'], ['BR', [], 'R0'], ['BL', [], 'Bd']], rk={0: RK_JA, 1: RK_JA, 2: RK_JA, 3: RK_JA, 4: RK_A}, brut=True,
           fixe=('Bd',), nx=[[5, 1]]),
 'B': dict(n=dict(Sb=(184, 97), Sm=(184, 388), St=(184, 631)),   # sans bouts de fût : les coins du haut et du bas se prolongent jusqu'au bord
           e=[['St', [], 'Sm'], ['Sm', [], 'Sb'],
              ['St', [(400, 632), (540, 615), (585, 560), (570, 450), (420, 392)], 'Sm'],
              ['Sm', [(470, 386), (620, 340), (662, 230), (620, 130), (480, 98)], 'Sb']], courbes=[2, 3]),
 'C': dict(n=dict(T=(700, 560), B=(700, 150)),
           e=[['T', [(600, 560), (470, 570), (330, 535), (230, 450), (193, 350), (225, 245), (320, 160), (460, 140), (600, 150)], 'B']], courbes=[0]),
 'D': dict(n=dict(S0=(182, -1), B=(182, 144), T=(182, 578), S1=(182, 711)),
           e=[['S0', [], 'B'], ['B', [], 'T'], ['T', [], 'S1'],
              ['T', [(400, 578), (540, 550), (612, 460), (616, 360), (575, 240), (470, 160), (330, 144)], 'B']], courbes=[3]),
 'E': dict(n=dict(T=(198, 605), M=(198, 350), Bo=(198, 100), TR=(740, 605), MR=(654, 350), BR=(710, 100)),
           e=[['T', [], 'M'], ['M', [], 'Bo'], ['T', [], 'TR'], ['M', [], 'MR'], ['Bo', [], 'BR']]),
 'F': dict(n=dict(S0=(203, -4), M=(203, 350), T=(203, 612), TR=(742, 612), MR=(654, 350)),
           e=[['S0', [], 'M'], ['M', [], 'T'], ['T', [], 'TR'], ['M', [], 'MR']]),
 'G': dict(n=dict(T=(790, 544), K=(690, 290), X=(452, 290)),   # le bas-droit est un bloc plein : l'arc y entre, remonte, et finit par le haut du bloc vers la gauche
           e=[['T', [(680, 541), (560, 560), (430, 568), (310, 535), (225, 450), (200, 340), (230, 230), (320, 160), (450, 150), (590, 160), (680, 205)], 'K'], ['K', [], 'X']], courbes=[0]),
 'H': dict(n=dict(L0=(205, -1), L1=(205, 705), R0=(582, -1), R1=(582, 705), ML=(205, 367), MR=(582, 367)),
           e=[['L0', [], 'ML'], ['ML', [], 'L1'], ['R0', [], 'MR'], ['MR', [], 'R1'], ['ML', [], 'MR']], rk={3: RK_H}),
 'I': dict(n=dict(S0=(214, 1), S1=(214, 703)), e=[['S0', [], 'S1']]),
 'J': dict(n=dict(T=(577, 712), H=(176, 378)),
           e=[['T', [(577, 520), (577, 360), (560, 240), (480, 160), (360, 135), (250, 175), (190, 270)], 'H']], courbes=[0]),
 'K': dict(n=dict(S0=(207, -9), S1=(207, 703), J=(207, 370), X=(480, 370), UP=(660, 703), DN=(650, -9)),
           e=[['S0', [], 'J'], ['J', [], 'S1'], ['J', [], 'X'], ['X', [(583, 575)], 'UP'], ['X', [(592, 125)], 'DN']]),
 'L': dict(n=dict(S1=(211, 712), C=(211, 122), E=(712, 122)), e=[['S1', [], 'C'], ['C', [], 'E']]),   # le coin franc (essayé arrondi : la zone hors des bandes paraissait d'un bloc)
 'M': dict(n=dict(L0=(200, -8), L1=(200, 640), V=(452, 240), R1=(695, 640), R0=(695, -8)),
           e=[['L0', [], 'L1'], ['L1', [], 'V'], ['V', [], 'R1'], ['R1', [], 'R0']], rk={0: 1.15, 2: 1.1}),
 'N': dict(n=dict(L0=(202, -8), L1=(202, 640), R0=(588, 60), R1=(582, 704)),
           e=[['L0', [], 'L1'], ['L1', [], 'R0'], ['R0', [], 'R1']]),
 'O': dict(n={}, boucle=[(430, 566), (580, 545), (661, 455), (661, 350), (610, 210), (430, 123), (250, 210), (194, 350), (225, 470), (300, 545)]),
 'P': dict(n=dict(S0=(191, -13), Mi=(191, 316), T=(191, 597), S1=(191, 699)),
           e=[['S0', [], 'Mi'], ['Mi', [], 'T'], ['T', [], 'S1'],
              ['T', [(420, 597), (555, 570), (608, 470), (575, 360), (430, 318)], 'Mi']], courbes=[3]),
 'Q': dict(n=dict(Q=(650, 175), Z=(860, -75)),
           e=[['Q', [(679, 300), (660, 455), (580, 545), (430, 567), (300, 545), (225, 470), (199, 350), (240, 210), (430, 124), (560, 140)], 'Q'],
              ['Q', [], 'Z']], courbes=[0]),
 'R': dict(n=dict(S0=(192, -13), Mi=(192, 311), T=(192, 593), S1=(192, 695), X=(470, 311), DN=(650, -13)),
           e=[['S0', [], 'Mi'], ['Mi', [], 'T'], ['T', [], 'S1'],
              ['T', [(420, 593), (565, 565), (621, 470), (590, 370)], 'X'], ['X', [], 'Mi'], ['X', [(587, 125)], 'DN']], courbes=[3]),
 'S': dict(n=dict(T=(745, 520), A=(255, 440), C=(640, 300), B=(60, 195)),   # trois tronçons : l'épine est deux fois plus fine que les panses
           e=[['T', [(625, 562), (470, 598), (330, 585), (225, 510)], 'A'], ['A', [(320, 395), (425, 367), (525, 338)], 'C'],
              ['C', [(705, 215), (650, 110), (525, 93), (425, 102), (325, 114), (175, 155)], 'B']], courbes=[0, 1, 2], rk={0: RK_SP, 2: RK_SP}, brut=True),   # v170b : brut — le redressement déplaçait C et faisait un crochet (un angle vif)
 'T': dict(n=dict(BL=(46, 552), J=(464, 552), BR=(882, 552), S0=(464, -5)),
           e=[['BL', [], 'J'], ['J', [], 'BR'], ['J', [], 'S0']]),
 'U': dict(n=dict(L=(200, 705), R=(577, 705)),
           e=[['L', [(200, 500), (200, 330), (240, 200), (390, 129), (530, 190), (577, 330), (577, 500)], 'R']], courbes=[0]),
 'V': dict(n=dict(L=(192, 700), B=(487, 60), R=(785, 700)),
           e=[['L', [(308, 375)], 'B'], ['B', [(668, 375)], 'R']]),
 'W': dict(n=dict(L=(190, 699), V1=(443, 30), P=(653, 600), V2=(858, 30), R=(1115, 699)),
           e=[['L', [(263, 425)], 'V1'], ['V1', [], 'P'], ['P', [], 'V2'], ['V2', [(1036, 425)], 'R']]),
 'X': dict(n=dict(C=(455, 380), TL=(199, 699), TR=(705, 699), BL=(195, -21), BR=(703, -21)),
           e=[['TL', [], 'C'], ['C', [], 'BR'], ['TR', [], 'C'], ['C', [], 'BL']], rk={0: 1.5, 1: 1.5, 2: 1.5, 3: 1.5}),
 'Y': dict(n=dict(TL=(205, 700), TR=(700, 700), J=(446, 300), S0=(446, -12)),
           e=[['TL', [], 'J'], ['TR', [], 'J'], ['J', [], 'S0']]),
 'Z': dict(n=dict(TL=(64, 598), TR=(655, 598), BL=(258, 105), BR=(874, 105)),
           e=[['TL', [], 'TR'], ['TR', [], 'BL'], ['BL', [], 'BR']]),
}

import os
# la bande d'un trait, un peu plus large que sa demi-largeur mesurée : sur une police aussi grasse, les zones qu'aucune bande ne couvre étaient comblées
# par un voisin tardif et attendaient, isolées (des éclats). Mesuré lettre par lettre (scratchpad/v170/diag-R100.txt, diag-R115.txt) : × 1,15 règle
# G, H, L, M, R, W, Z ; il dégrade B, K, X, F, qui gardent × 1.
R_K = float(os.environ.get('R_K', '1.15'))
R_K_LETTRE = {'B': 1.0, 'K': 1.0, 'X': 1.0, 'F': 1.0, 'S': 1.0, 'U': 1.0}

def _catmull(P, pas=4.0):
    """une courbe lisse passant par les points (Catmull-Rom centripète simplifiée), rééchantillonnée"""
    P = np.asarray(P, float)
    if len(P) < 3: return S.reechant(P, pas)
    Q = [P[0]]
    ext = np.concatenate([[2 * P[0] - P[1]], P, [2 * P[-1] - P[-2]]])
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        n = max(2, int(np.hypot(*(p2 - p1)) / pas))
        for t in np.linspace(0, 1, n + 1)[1:]:
            t2, t3 = t * t, t * t * t
            Q.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return np.array(Q)

def morceaux(police, nom, ch, chemins):
    """le glyphe dessiné → (liste de Morceau, boîte, R) au format de chemins.morceaux"""
    D = DESSINS[ch]
    cts = S.contours(police, nom); img, x0, y1 = S.image(cts); H, W = img.shape; U = S.U
    ys, xs = np.nonzero(img); boite = (x0 + xs.min() * U, y1 - (ys.max() + 1) * U, x0 + (xs.max() + 1) * U, y1 - ys.min() * U)
    def px(p): return np.array([(p[0] - x0) / U, (y1 - p[1]) / U])
    def dans_u(p):
        q = px(p); xi, yi = int(round(q[0])), int(round(q[1])); return 0 <= yi < H and 0 <= xi < W and img[yi, xi]
    def bord(p, v, maxi):
        """distance (unités) de p au bord de l'encre dans la direction v ; 0 si p est dehors"""
        if not dans_u(p): return 0.0
        d = 0.0; st = U * 0.5
        while d < maxi:
            if not dans_u(p + v * (d + st)): break
            d += st
        return d
    def R_de(pts):
        q = S.reechant(pts, 4.0); n = len(q); a, b = int(n * 0.25), max(int(n * 0.25) + 1, int(math.ceil(n * 0.75)))
        sel = q[a:b] if n >= 5 else q
        return float(np.median(S.rayon(img, np.stack([(sel[:, 0] - x0) / U, (y1 - sel[:, 1]) / U], 1)))) * U
    def recentre(q, fixes=(), passes=3):
        q = q.copy()
        for _ in range(passes):
            for i in range(len(q)):
                if i in fixes: continue
                a, b = q[max(0, i - 3)], q[min(len(q) - 1, i + 3)]; t = b - a; nt = np.hypot(*t)
                if nt < 1e-6: continue
                t /= nt; n = np.array([-t[1], t[0]])
                if not dans_u(q[i]): continue
                dg, dd = bord(q[i], n, 400), bord(q[i], -n, 400)
                q[i] = q[i] + n * (dg - dd) / 2 * 0.8
            # lissage léger (les bouts restent)
            k = 3
            if len(q) > 2 * k + 2:
                L = q.copy()
                for i in range(1, len(q) - 1):
                    if i in fixes: continue
                    j0, j1 = max(0, i - k), min(len(q), i + k + 1); L[i] = q[j0:j1].mean(0)
                q = L
        return q
    def ancres(P, cyc=False, fixes=(), journal=None):
        """recentre les points d'ancrage eux-mêmes (la tangente prise sur leurs voisins), quatre passes : la courbe lisse passera par eux"""
        P = [np.array(p, float) for p in P]; n = len(P)
        for _ in range(4):
            Q = [p.copy() for p in P]
            for i in range(n):
                if i in fixes: continue
                if cyc: a, b = P[(i - 1) % n], P[(i + 1) % n]
                else: a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
                t = b - a; nt = np.hypot(*t)
                if nt < 1e-6 or not dans_u(P[i]): continue
                t /= nt; nr = np.array([-t[1], t[0]])
                dg, dd = bord(P[i], nr, 500), bord(P[i], -nr, 500)
                if dg + dd > 380: continue                       # la coupe ne traverse pas le trait (un trait fait au plus 340) : on ne bouge pas
                Q[i] = P[i] + nr * float(np.clip((dg - dd) / 2, -25, 25))
            P = Q
        return P
    m = chemins.Morceau()
    if 'boucle' in D:
        A_ = ancres(D['boucle'], cyc=True)
        q = _catmull(A_ + [A_[0]], 4.0)[:-1]
        # v170b : l'anneau prend le facteur de sa lettre (sa bande couvre l'anneau d'encre entier ; le surplus tombe dans le contre-poinçon ou dehors)
        m.aretes.append(dict(a=None, b=None, pts=q, R=R_de(q) * R_K_LETTRE.get(ch, RK_ANNEAU), boucle=True, blob=False, droit=False, L=S.longueur(np.concatenate([q, q[:1]]))))
        return [m], boite, m.aretes[0]['R']
    noms = list(D['n']); idx = {k: i for i, k in enumerate(noms)}
    m.noeuds = [np.array(D['n'][k], float) for k in noms]
    deg = {k: 0 for k in noms}
    for a, _, b in D['e']: deg[a] += 1; deg[b] += 1
    courbes = set(D.get('courbes', []))
    for i, (a, mil, b) in enumerate(D['e']):
        P = [D['n'][a]] + list(mil) + [D['n'][b]]
        if i in courbes:
            fx = set()
            if deg[a] != 1 or a == b: fx.add(0)
            if deg[b] != 1 or a == b: fx.add(len(P) - 1)
            q = _catmull(ancres(P, fixes=fx), 4.0)
        else:
            q = np.array(P, float)
            if len(q) > 2: q = S.reechant(q, 4.0)
        m.aretes.append(dict(a=idx[a], b=idx[b], pts=q, R=0.0, boucle=False, blob=False))
    # les bouts libres : au centre du trait (perpendiculairement), puis jusqu'au bord le long de la direction d'arrivée
    for k in noms:
        if deg[k] != 1 or k in D.get('fixe', ()): continue
        n_ = idx[k]
        for e in m.aretes:
            if e['a'] == n_ or e['b'] == n_:
                q = e['pts'] if e['b'] == n_ else e['pts'][::-1]
                Lq = S.longueur(q); ds = min(120.0, 0.45 * Lq)
                d = np.sqrt((np.diff(q, axis=0) ** 2).sum(1)); s = np.concatenate([[0], np.cumsum(d)])
                p0 = np.array([np.interp(Lq - ds, s, q[:, 0]), np.interp(Lq - ds, s, q[:, 1])]); v = q[-1] - p0; v /= max(np.hypot(*v), 1e-9)
                X = p0 + v * bord(p0, v, 600)
                q2 = np.concatenate([q[s <= Lq - ds], [p0], [X]]) if len(q) > 2 else np.array([q[0], X])
                e['pts'] = q2 if e['b'] == n_ else q2[::-1]; m.noeuds[n_] = X
                break
    rk = DESSINS[ch].get('rk', {})   # un facteur de rayon par arête, quand une seule bande est trop étroite pour l'encre qu'elle doit couvrir
    for i_, e in enumerate(m.aretes):
        e['pts'][0] = m.noeuds[e['a']]; e['pts'][-1] = m.noeuds[e['b']]
        e['R'] = R_de(e['pts']) * R_K_LETTRE.get(ch, R_K)
    Rg = float(np.median([e['R'] for e in m.aretes]))
    droites = [i for i in range(len(m.aretes)) if i not in courbes]
    # les droites : chemins.redresse (exactes, recentrées) ; les courbes restent telles quelles (« fige »)
    for i, e in enumerate(m.aretes):
        if i in courbes: e['fige'] = True
    if D.get('brut'):   # v170b : le dessin tel quel (pas de redressement : il déplace les nœuds partagés)
        for e in m.aretes: e['droit'] = len(e['pts']) == 2; e['fige'] = True; e['L'] = S.longueur(e['pts'])
    else: chemins.redresse(m, bord, Rg)
    for i_, f in rk.items(): m.aretes[i_]['R'] *= f   # après le redressement : une droite y reprend sa demi-largeur mesurée
    for i in courbes:
        e = m.aretes[i]; e['pts'] = S.rdp(e['pts'], 0.6); e['pts'][0] = m.noeuds[e['a']]; e['pts'][-1] = m.noeuds[e['b']]
        e['L'] = S.longueur(e['pts'])
    chemins.morceaux.bord = bord
    return [m], boite, Rg
