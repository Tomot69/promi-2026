#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chemins.py — LE GÉNÉRATEUR DES CHEMINS DU TRACÉ DES LETTRES (C-125).

Pour chaque glyphe d'une police OTF : sa LIGNE MÉDIANE (squelette.py), puis le PARCOURS de cette ligne selon les règles de Tom :
  R1  on évite de revenir en arrière ; un repassage est invisible et ne dure qu'un instant ;
  R2  un mouvement vers la gauche est permis s'il s'enchaîne ; chaque lettre FINIT vers la droite ;
  R3  une lettre commence du côté (haut / bas) où la précédente a fini ; quand le glyphe le permet elle finit du côté opposé ;
  R4  (le « h ») la barre d'abord, puis repassage jusqu'à la naissance du pont, le pont, la jambe ;
  R5  lettres en plusieurs morceaux : le saut est instantané et invisible ; le dernier morceau finit à droite.
Chaque glyphe reçoit donc DEUX variantes quand c'est possible : « h » (départ en haut) et « b » (départ en bas).
« haut » / « bas » : au-dessus ou au-dessous de la mi-hauteur d'x (la main est en haut ou en bas de la ligne).

Le parcours est une marche CONTINUE sur le graphe de la ligne médiane : chaque arête est tracée une fois (visible) ; pour rejoindre une arête
qui reste, on revient sur ses pas le long de ce qui est déjà tracé (repassage, invisible). Entre deux morceaux : un saut.
On cherche la marche de moindre coût (programmation dynamique sur l'ensemble des arêtes tracées) ; les poids sont en tête de fichier.
Une table de corrections À LA MAIN (CORRECTIONS) reprend les glyphes qui résistent.

Usage :  python3 chemins.py gilbert [--planche] [--seul=abc]        python3 chemins.py promilate
Sorties : ../../../variantes/trace-chemins-<police>.js   et   planche-<police>-N.png (avec --planche)
"""
import sys, os, io, json, math, itertools, time
import numpy as np
from fontTools.ttLib import TTFont
import squelette as S

ICI = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.normpath(os.path.join(ICI, '..', '..', '..'))
POLICES = {
    'gilbert': dict(nom='Gilbert', fichier=os.path.join(ICI, 'police', 'Gilbert-Bold Preview5.otf'), sortie='trace-chemins-gilbert.js'),
    'promilate': dict(nom='PromiLate', fichier=os.path.join(RACINE, 'Polices Promi', 'PromiLate-Regular.otf'), sortie='trace-chemins-promilate.js'),
    # v147 (C-138) : le texte de l'onboarding et du guide passe en Atkinson — la graisse 500, celle du texte (une ligne médiane par famille)
    'atkinson': dict(nom='Atkinson', fichier=os.path.join(ICI, 'police', 'Atkinson-500.otf'), sortie='trace-chemins-atkinson.js'),
}
# ── les poids du parcours (en « cadratins de repassage ») ──
W_RET = 1.0      # un cadratin de repassage
W_R2 = 10.0      # finir à gauche (pleine pénalité quand on finit au bord gauche)
W_MEME = 0.12    # finir du même côté (haut / bas) qu'on a commencé
W_TOUR = 0.25    # un demi-tour enchaîné (au carré de l'angle)
W_CASSE = 1.0    # quitter une ligne droite qui continuait (par cadratin de la plus courte des deux moitiés)
W_GAUCHE = 0.35  # une droite tracée vers la gauche (par cadratin) ; ×0,4 si elle s'enchaîne
W_SAUT = 0.3     # un saut entre deux morceaux (par cadratin)
ANGLE_FONDU = 48 # en deçà, deux arêtes enchaînées forment un seul trait (le rouleau tourne) ; au-delà, deux traits (un coin)

def seuil(boite, mi):
    """le seuil haut / bas d'un glyphe : le milieu de sa hauteur d'encre ; ce qui vit tout en haut de la ligne (apostrophe, accent seul) est
    toujours « haut », ce qui vit tout en bas (virgule, point) toujours « bas »"""
    if boite[1] >= mi: return -1e9
    if boite[3] <= mi: return 1e9
    return (boite[1] + boite[3]) / 2.0
def cote(y, mi): return 'h' if y >= mi else 'b' 

# ───────────────────────────── du glyphe aux morceaux ─────────────────────────────
class Morceau:
    """un morceau connexe : noeuds [np(x,y)] en unités, aretes [dict a,b,pts,R,L,droit,boucle,blob]"""
    def __init__(self): self.noeuds = []; self.aretes = []

def _coins(q, k, seuil=50.0):
    """les indices des coins vifs d'une chaîne (pas de 1 px) : l'angle entre la corde d'avant et celle d'après, sur k points"""
    n = len(q)
    if n < 2 * k + 3: return []
    a = q[k:n - k] - q[0:n - 2 * k]; b = q[2 * k:n] - q[k:n - k]
    na = np.hypot(a[:, 0], a[:, 1]); nb = np.hypot(b[:, 0], b[:, 1])
    c = np.clip((a * b).sum(1) / np.maximum(na * nb, 1e-9), -1, 1); th = np.degrees(np.arccos(c))
    idx = []
    ordre = np.argsort(-th)
    for i in ordre:
        if th[i] < seuil: break
        if all(abs(i - j) >= k for j in idx): idx.append(int(i))
    return sorted(i + k for i in idx)
def _inter(p1, d1, p2, d2):
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-6: return None
    t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
    return np.array([p1[0] + t * d1[0], p1[1] + t * d1[1]])

def morceaux(police, nom, journal=None):
    """le glyphe → (liste de Morceau, boîte d'encre en unités, R médian en unités)"""
    cts = S.contours(police, nom)
    if not cts: return [], None, 0
    img, x0, y1 = S.image(cts); H, W = img.shape
    if not img.any(): return [], None, 0
    U = S.U
    def unites(p): p = np.asarray(p, float); return np.stack([x0 + p[..., 0] * U, y1 - p[..., 1] * U], -1)
    ys, xs = np.nonzero(img); boite = (x0 + xs.min() * U, y1 - (ys.max() + 1) * U, x0 + (xs.max() + 1) * U, y1 - ys.min() * U)
    sk = S.amincit(img); G = S.graphe(sk)
    sy, sx = np.nonzero(sk)
    Rpx = float(np.median(S.rayon(img, np.stack([sx, sy], 1)[::5]))) if len(sx) else 3.0
    S.elague(G, img, Rpx)
    # les fourches de bout : deux barbes courtes au bout d'un trait coupé en biais → un seul bout
    while True:
        fait = False
        for n in range(len(G.noeuds)):
            inc = G.incid(n)
            if len(inc) != 3: continue
            court = []
            for (i, b) in inc:
                e = G.aretes[i]; autre = e['b'] if b == 0 else e['a']
                if autre != n and G.degre(autre) == 1 and S.longueur(e['pts']) <= 1.3 * Rpx: court.append(i)
            if len(court) == 2:
                for i in sorted(court, reverse=True): G.aretes.pop(i)
                fait = True; break
        if not fait: break
    # une barbe courte plantée dans un COIN (l'onglet d'un angle aigu) : elle n'est pas un trait
    while True:
        fait = False
        for n in range(len(G.noeuds)):
            inc = G.incid(n)
            if len(inc) != 3: continue
            for (i, b) in inc:
                e = G.aretes[i]; autre = e['b'] if b == 0 else e['a']
                if autre == n or G.degre(autre) != 1 or S.longueur(e['pts']) > 1.7 * Rpx: continue
                (j, bj), (k_, bk) = [x for x in inc if x[0] != i]
                tj = -S.tangente(G.aretes[j]['pts'], bj, 1.5 * Rpx); tk = -S.tangente(G.aretes[k_]['pts'], bk, 1.5 * Rpx)
                if float(tj @ tk) > -math.cos(math.radians(40)): G.aretes.pop(i); fait = True; break
            if fait: break
        if not fait: break
    S.fusionne(G)
    # une arête minuscule entre deux embranchements : un seul embranchement
    while True:
        fait = False
        for i, e in enumerate(G.aretes):
            if e['boucle'] or e['a'] == e['b'] or G.degre(e['a']) < 3 or G.degre(e['b']) < 3 or S.longueur(e['pts']) > 1.0 * Rpx: continue
            a, b = e['a'], e['b']; mid = ((np.array(G.noeuds[a]) + np.array(G.noeuds[b])) / 2)
            G.aretes.pop(i)
            for e2 in G.aretes:
                if e2['boucle']: continue
                if e2['a'] in (a, b): e2['a'] = a; e2['pts'] = np.concatenate([[mid], e2['pts'][1:]]) if len(e2['pts']) > 2 else np.array([mid, e2['pts'][-1]])
                if e2['b'] in (a, b): e2['b'] = a; e2['pts'] = np.concatenate([e2['pts'][:-1], [mid]]) if len(e2['pts']) > 2 else np.array([e2['pts'][0], mid])
            G.noeuds[a] = mid.tolist(); fait = True; break
        if not fait: break
    lab, nlab = S.composantes(img)
    # les coins vifs : on coupe l'arête et on remet le coin au carré
    k = max(6, int(round(0.5 * Rpx)))
    def coupe(e):
        """rend la liste des morceaux d'arête (dict) après découpe aux coins"""
        q = S.lisse(S.reechant(e['pts'], 1.0), 2)
        if e['boucle']:
            n = len(q); qq = np.concatenate([q[-2 * k:], q, q[:2 * k]]); cs = [c - 2 * k for c in _coins(qq, k) if 2 * k <= c < n + 2 * k]
            if not cs: return [e]
            c0 = cs[0]; q = np.concatenate([q[c0:], q[:c0 + 1]])
            G.noeuds.append(q[0].tolist()); nn = len(G.noeuds) - 1
            return coupe({'a': nn, 'b': nn, 'pts': q, 'boucle': False, 'ferme': True})
        cs = _coins(q, k)
        # un « coin » tout près d'un embranchement n'en est pas un : c'est la ligne médiane qui se tord en y arrivant
        garde_a = 1.7 * Rpx if (e['a'] is not None and e['a'] in jonc0) else k; garde_b = 1.7 * Rpx if (e['b'] is not None and e['b'] in jonc0) else k
        cs = [c for c in cs if c >= garde_a and len(q) - 1 - c >= garde_b]
        if not cs: e = dict(e); e['pts'] = q; return [e]
        # le coin le plus au milieu d'abord, puis on recommence sur chaque moitié
        i = min(cs, key=lambda c: abs(c - len(q) / 2)); n = len(q)
        ia, ib = max(0, i - k), min(n - 1, i + k); ia2, ib2 = max(0, i - 2 * k), min(n - 1, i + 2 * k)
        X = None
        if ia2 < ia and ib2 > ib:
            X = _inter(q[ia], q[ia] - q[ia2], q[ib], q[ib2] - q[ib])
            if X is not None and (np.hypot(*(X - q[i])) > 1.4 * Rpx or not (0 <= int(round(X[1])) < H and 0 <= int(round(X[0])) < W and img[int(round(X[1])), int(round(X[0]))])): X = None
        if X is None: g, d, X = q[:i + 1], q[i:], q[i]
        else: g, d = np.concatenate([q[:ia + 1], [X]]), np.concatenate([[X], q[ib:]])
        G.noeuds.append(X.tolist()); nn = len(G.noeuds) - 1
        return coupe({'a': e['a'], 'b': nn, 'pts': g, 'boucle': False}) + coupe({'a': nn, 'b': e['b'], 'pts': d, 'boucle': False})
    jonc0 = set(n for n in range(len(G.noeuds)) if G.degre(n) >= 3)
    neuves = []
    for e in G.aretes: neuves += coupe(e)
    G.aretes = [e for e in neuves if e['boucle'] or S.longueur(e['pts']) > 0.3 * Rpx or e['a'] != e['b']]
    # lissage, prolongement des bouts libres jusqu'au bord
    dem = max(2, int(round(0.3 * Rpx)))
    for e in G.aretes:
        q = S.reechant(e['pts'], 1.0)
        if e['boucle']:
            n = len(q); d = min(dem, n // 6); kk = np.ones(2 * d + 1) / (2 * d + 1); Q = np.concatenate([q[-d:], q, q[:d]])
            q = np.stack([np.convolve(Q[:, 0], kk, 'valid'), np.convolve(Q[:, 1], kk, 'valid')], 1)
        else: q = S.lisse(q, min(dem, max(1, len(q) // 5)))
        e['pts'] = q
    def dans(p): xi, yi = int(round(p[0])), int(round(p[1])); return 0 <= yi < H and 0 <= xi < W and img[yi, xi]
    for n in range(len(G.noeuds)):
        inc = G.incid(n)
        if len(inc) != 1: continue
        i, b = inc[0]; e = G.aretes[i]
        if e['boucle'] or e['a'] == e['b']: continue
        q = e['pts'] if b == 1 else e['pts'][::-1]; L = S.longueur(q)
        autre = e['a'] if b == 1 else e['b']
        if L < 1.7 * Rpx and G.degre(autre) >= 3:
            A0 = np.array(G.noeuds[autre]); sd = q[-1] - q[0]; sd = sd / max(math.hypot(*sd), 1e-9); mb = None
            for (j, bj) in G.incid(autre):
                if j == i or G.aretes[j]['boucle']: continue
                t = S.tangente(G.aretes[j]['pts'], bj, 2.5 * Rpx); c = float(t @ sd)
                if mb is None or c > mb[0]: mb = (c, t)
            if mb and mb[0] > math.cos(math.radians(50)):
                X = A0.copy()
                for _ in range(int(6 * Rpx) + 8):
                    if not dans(X + mb[1] * 0.5): break
                    X = X + mb[1] * 0.5
                q2 = np.array([A0, X]); e['pts'] = q2 if b == 1 else q2[::-1]; G.noeuds[n] = X.tolist(); continue
        if L < 2.4 * Rpx and G.degre(autre) == 2:
            A0 = np.array(G.noeuds[autre]); sd = q[-1] - q[0]; a0 = math.atan2(sd[1], sd[0])
            def larg(P, v, maxi=2.6 * Rpx):
                d_ = 0.0; X_ = P.copy()
                while d_ < maxi and dans(X_ + v * 0.5): X_ = X_ + v * 0.5; d_ += 0.5
                return d_
            def essai(A_, ang):
                v = np.array([math.cos(ang), math.sin(ang)]); nr = np.array([-v[1], v[0]]); lg = larg(A_, v, 6 * Rpx)
                if lg < 0.8 * Rpx: return None
                ds = [(larg(A_ + v * t, nr), larg(A_ + v * t, -nr)) for t in np.linspace(min(0.9 * Rpx, lg * 0.5), max(lg - 0.3 * Rpx, lg * 0.6), 6)]
                eg = float(np.std([g_ for g_, d_ in ds])); ed = float(np.std([d_ for g_, d_ in ds])); sc = min(eg, ed) + 0.3 * max(eg, ed); return sc, float(np.median([(g_ - d_) / 2 for g_, d_ in ds])), v, nr, lg
            for _tour in range(2):
                axes = [math.degrees(ax - a0) for ax in (0, math.pi / 2, math.pi, -math.pi / 2)]; axes = [((d_ + 180) % 360) - 180 for d_ in axes]
                r = [(essai(A0, a0 + math.radians(da)), da) for da in list(np.arange(-40, 40.1, 2.5)) + [d_ for d_ in axes if abs(d_) <= 62]]; r = [x for x in r if x[0]]
                if not r: break
                (sc, dec, v, nr, lg), da = min(r, key=lambda x: x[0][0] + 0.004 * abs(x[1]) - (0.6 if min(abs(x[0][2][0]), abs(x[0][2][1])) < 1e-6 else 0))
                if abs(dec) > 0.6 * Rpx: break
                A0 = A0 + nr * dec; a0 = math.atan2(v[1], v[0])
            else:
                X = A0.copy()
                while dans(X + v * 0.5): X = X + v * 0.5
                dA = A0 - np.array(G.noeuds[autre])
                # le nœud d'en face suit : les autres arêtes qui y aboutissent gardent leur bout sur lui
                for (j, bj) in G.incid(autre):
                    pj = G.aretes[j]['pts']
                    if bj == 0: pj[0] = A0
                    else: pj[-1] = A0
                G.noeuds[autre] = A0.tolist()
                q2 = np.array([A0, X]); e['pts'] = q2 if b == 1 else q2[::-1]; G.noeuds[n] = X.tolist(); continue
        if L < 1.9 * Rpx and G.degre(autre) >= 2:
            A0 = np.array(G.noeuds[autre]); sd = q[-1] - q[0]; ang = math.degrees(math.atan2(sd[1], sd[0])); cands = []
            def larg2(P, v, maxi=2.6 * Rpx):
                d_ = 0.0; X_ = P.copy()
                while d_ < maxi and dans(X_ + v * 0.5): X_ = X_ + v * 0.5; d_ += 0.5
                return d_
            occupe = [-S.tangente(G.aretes[j]['pts'], bj, 1.5 * Rpx) for (j, bj) in G.incid(autre) if j != i and not G.aretes[j]['boucle']]
            for axe in (0.0, 90.0, 180.0, -90.0):
                ecart = abs(((ang - axe + 180) % 360) - 180)
                if ecart > 62: continue
                v = np.array([math.cos(math.radians(axe)), math.sin(math.radians(axe))]); nr = np.array([-v[1], v[0]]); lg = larg2(A0, v, 6 * Rpx)
                if any(float(v @ t_) > math.cos(math.radians(35)) for t_ in occupe): continue      # un autre trait part déjà par là
                if lg < 0.9 * Rpx: continue
                ds = [(larg2(A0 + v * t, nr), larg2(A0 + v * t, -nr)) for t in np.linspace(min(1.0 * Rpx, lg * 0.6), max(lg - 0.3 * Rpx, lg * 0.7), 5)]
                eg = float(np.std([g_ for g_, d_ in ds])); ed = float(np.std([d_ for g_, d_ in ds])); lgm = float(np.mean([g_ + d_ for g_, d_ in ds]))
                cands.append((min(eg, ed) + 0.3 * max(eg, ed) + 0.5 * abs(lgm - 2 * Rpx) + 0.02 * ecart, v, lg))
            if cands:
                sc, v, lg = min(cands, key=lambda c: c[0])
                if sc < 0.8 * Rpx:
                    X = A0 + v * lg; q2 = np.array([A0, X]); e['pts'] = q2 if b == 1 else q2[::-1]; G.noeuds[n] = X.tolist(); continue
        d = np.sqrt((np.diff(q, axis=0) ** 2).sum(1)); s = np.concatenate([[0], np.cumsum(d)])
        def pt(t): t = min(max(t, 0), L); return np.array([np.interp(t, s, q[:, 0]), np.interp(t, s, q[:, 1])])
        if L < 1.2 * Rpx: pres, loin, garde = q[-1], q[0], len(q)
        else:
            pres, loin = pt(L - 0.4 * Rpx), pt(L - min(2.0 * Rpx, L)); garde = int(np.searchsorted(s, L - 0.4 * Rpx))
        v = pres - loin; nv = math.hypot(*v)
        if nv < 1e-6: continue
        v /= nv; X = pres.copy()
        for _ in range(int(4 * Rpx) + 8):
            if not dans(X + v * 0.5): break
            X = X + v * 0.5
        q2 = np.concatenate([q[:max(garde, 1)], [pres], [X]]) if L >= 1.2 * Rpx else np.concatenate([q, [X]])
        e['pts'] = q2 if b == 1 else q2[::-1]; G.noeuds[n] = X.tolist()
    def bord(p, v, maxi):
        """la distance (unités) du point p (unités) au bord de l'encre, dans la direction v (unités, y vers le haut)"""
        X = np.array([(p[0] - x0) / U, (y1 - p[1]) / U]); w = np.array([v[0], -v[1]]) * 0.5; d = 0.0
        if not dans(X): return 0.0
        while d < maxi / U:
            if not dans(X + w): break
            X = X + w; d += 0.5
        return d * U
    # par morceau d'encre
    M = {}
    Rloc = {}
    for i, e in enumerate(G.aretes):
        p = e['pts'][len(e['pts']) // 2]; l = int(lab[min(H - 1, max(0, int(round(p[1])))), min(W - 1, max(0, int(round(p[0]))))])
        if l == 0:
            for p in e['pts']:
                l = int(lab[min(H - 1, max(0, int(round(p[1])))), min(W - 1, max(0, int(round(p[0]))))])
                if l: break
        M.setdefault(l, []).append(i)
    out = []
    for l in range(1, nlab + 1):
        ys, xs = np.nonzero(lab == l)
        if len(xs) < 6: continue
        bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        m = Morceau(); ids = M.get(l, [])
        Lsk = sum(S.longueur(G.aretes[i]['pts']) for i in ids)
        # le rayon du morceau : la distance au bord du point le plus enfoui (pris sur un semis du morceau)
        semis = np.stack([xs, ys], 1)[::max(1, len(xs) // 400)]; Rc = float(S.rayon(lab == l, semis).max())
        larg, haut = bx1 - bx0, by1 - by0
        if not ids or (Lsk <= 1.5 * Rc and max(larg, haut) <= 1.45 * min(larg, haut)):
            # une pastille (point, tréma) : un trait horizontal, de gauche à droite, large comme elle
            cy = float(ys.mean()); a = unites([bx0, cy]); b = unites([bx1, cy])
            m.noeuds = [a, b]; m.aretes = [dict(a=0, b=1, pts=np.array([a, b]), R=haut * U / 2, boucle=False, blob=True, droit=True, L=float(larg * U))]
            out.append(m); continue
        idn = {}
        for i in ids:
            e = G.aretes[i]; pts = unites(e['pts'])
            # la demi-largeur du trait : la distance au bord, prise le long de l'arête, loin de ses bouts (un bout libre touche le bord, un
            # embranchement est plus large que le trait)
            qq = S.reechant(e['pts'], 2.0); nq = len(qq); ia = max(1, int(nq * 0.25)); ib = max(ia + 1, int(math.ceil(nq * 0.75)))
            R = float(np.median(S.rayon(img, qq[ia:ib] if nq >= 5 else qq))) * U
            if nq < 5 or R < 0.6 * Rpx * U: R = max(R, min(Rpx * U, float(S.rayon(img, qq).max()) * U))
            if e['boucle']: m.aretes.append(dict(a=None, b=None, pts=pts, R=R, boucle=True, blob=False)); continue
            for kx in ('a', 'b'):
                if e[kx] not in idn: idn[e[kx]] = len(m.noeuds); m.noeuds.append(unites(G.noeuds[e[kx]]))
            pts[0] = m.noeuds[idn[e['a']]]; pts[-1] = m.noeuds[idn[e['b']]]
            m.aretes.append(dict(a=idn[e['a']], b=idn[e['b']], pts=pts, R=R, boucle=False, blob=False))
        redresse(m, bord, Rpx * U)
        out.append(m)
    out.sort(key=lambda m: min(float(e['pts'][:, 0].min()) for e in m.aretes))
    morceaux.bord = bord
    return out, boite, Rpx * U

def redresse(m, bord, Rg):
    """les droites deviennent des droites : un fût qui traverse des embranchements est UNE droite, recentrée entre ses deux bords ;
    verticales et horizontales exactes"""
    def deplace(n, neuf):
        d = np.asarray(neuf, float) - m.noeuds[n]
        if np.hypot(*d) < 1e-6: return
        for e in m.aretes:
            if e['boucle'] or e.get('fige'): continue
            p = e['pts']; L = S.longueur(p)
            if L < 1e-6: continue
            port = min(L * 0.5, 1.5 * e['R'] + 20) if e['a'] != e['b'] else min(L * 0.25, 1.5 * e['R'] + 20)
            s = np.concatenate([[0], np.cumsum(np.sqrt((np.diff(p, axis=0) ** 2).sum(1)))])
            if e['a'] == n: w = np.clip(1 - s / port, 0, 1)[:, None]; p += w * d
            if e['b'] == n: w = np.clip(1 - (L - s) / port, 0, 1)[:, None]; p += w * d
        m.noeuds[n] = m.noeuds[n] + d
    A = m.aretes
    for e in A: e['droit'] = bool(e.get('blob'))
    if any(e.get('blob') for e in A): 
        for e in A: e['L'] = S.longueur(e['pts'])
        return
    # 1 · les couples « tout droit » à chaque embranchement, puis les chaînes
    parent = list(range(len(A)))
    def racine(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for n in range(len(m.noeuds)):
        inc = [(i, 0) for i, e in enumerate(A) if not e['boucle'] and e['a'] == n and e['a'] != e['b']] + [(i, 1) for i, e in enumerate(A) if not e['boucle'] and e['b'] == n and e['a'] != e['b']]
        if len(inc) < 2: continue
        cands = []
        for (i, bi), (j, bj) in itertools.combinations(inc, 2):
            ti = S.tangente(A[i]['pts'], bi, min(S.longueur(A[i]['pts']), 2.5 * Rg)); tj = S.tangente(A[j]['pts'], bj, min(S.longueur(A[j]['pts']), 2.5 * Rg))
            c = float(ti @ tj)
            if c < -math.cos(math.radians(20)): cands.append((c, i, j))
        pris = set()
        for c, i, j in sorted(cands):
            if i in pris or j in pris: continue
            pris.add(i); pris.add(j); parent[racine(i)] = racine(j)
    groupes = {}
    for i, e in enumerate(A):
        if not e['boucle'] and e['a'] != e['b']: groupes.setdefault(racine(i), []).append(i)
    for ids in groupes.values():
        # les deux bouts de la chaîne : les nœuds qui n'y paraissent qu'une fois
        cpt = {}
        for i in ids:
            for n in (A[i]['a'], A[i]['b']): cpt[n] = cpt.get(n, 0) + 1
        bouts = [n for n, c in cpt.items() if c == 1]
        if len(bouts) != 2: continue
        P0, P1 = m.noeuds[bouts[0]].copy(), m.noeuds[bouts[1]].copy(); w = P1 - P0; L = np.hypot(*w)
        if L < 12: continue
        u = w / L; nrm = np.array([-u[1], u[0]])
        ec = max(float(np.abs((A[i]['pts'] - P0) @ nrm).max()) for i in ids)
        if len(ids) == 1 and ec > max(3.0, 0.035 * L):
            if L < 2.5 * Rg or ec > 0.55 * Rg: continue
            q = S.reechant(A[ids[0]]['pts'], 2.0); n4 = len(q) // 4; mil = q[n4:len(q) - n4]
            if len(mil) < 6 or S.ecart_corde(mil) > max(2.0, 0.02 * S.longueur(mil)): continue
            wm = mil[-1] - mil[0]; wm = wm / np.hypot(*wm); sens = 1 if (q[0] - m.noeuds[bouts[0]]) @ (q[0] - m.noeuds[bouts[0]]) < 1 else -1
            a0_, a1_ = (mil[0] + wm * float((P0 - mil[0]) @ wm), mil[0] + wm * float((P1 - mil[0]) @ wm))
            P0, P1 = a0_, a1_; w = P1 - P0; L = np.hypot(*w); u = w / L; nrm = np.array([-u[1], u[0]])
        elif ec > (max(3.0, 0.035 * L) if len(ids) == 1 else 0.38 * Rg): continue
        # 2 · recentrer la droite entre ses deux bords (là où la coupe est franche), sinon sur le bord le plus proche
        offs, un, demi = [], {1: [], -1: []}, []
        for t in np.linspace(0.08, 0.92, 15):
            p = P0 + w * t; dg = bord(p, nrm, 2.6 * Rg); dd = bord(p, -nrm, 2.6 * Rg)
            if dg <= 0 or dd <= 0: continue
            if abs(dg + dd - 2 * Rg) <= 0.2 * Rg: offs.append((dg - dd) / 2); demi.append((dg + dd) / 2)
            if dg <= 1.25 * Rg: un[1].append(dg - Rg)
            if dd <= 1.25 * Rg: un[-1].append(Rg - dd)
        dec = None
        if len(offs) >= 3: dec = float(np.median(offs))
        else:
            sgn = 1 if len(un[1]) >= len(un[-1]) else -1
            if len(un[sgn]) >= 5: dec = float(np.median(un[sgn]))
        if dec is not None and abs(dec) <= 0.45 * Rg: P0 = P0 + nrm * dec; P1 = P1 + nrm * dec
        # 3 · verticale ou horizontale exacte (à 1,6° près)
        w = P1 - P0
        if abs(w[0]) <= L * 0.028: xm = (P0[0] + P1[0]) / 2; P0[0] = P1[0] = xm
        elif abs(w[1]) <= L * 0.028: ym = (P0[1] + P1[1]) / 2; P0[1] = P1[1] = ym
        w = P1 - P0
        # un bout libre va jusqu'au bord de l'encre, le long de la droite
        degm = lambda n: sum((e['a'] == n) + (e['b'] == n) for e in A)
        Lw = float(np.hypot(*w)); uw = w / Lw
        if degm(bouts[0]) == 1: q0 = P0 + uw * min(1.5 * Rg, Lw * 0.4); P0 = q0 - uw * bord(q0, -uw, 4 * Rg)
        if degm(bouts[1]) == 1: q1 = P1 - uw * min(1.5 * Rg, Lw * 0.4); P1 = q1 + uw * bord(q1, uw, 4 * Rg)
        w = P1 - P0
        for n in cpt:
            t = float((m.noeuds[n] - P0) @ w) / float(w @ w)
            if n == bouts[0]: t = 0.0
            if n == bouts[1]: t = 1.0
            deplace(n, P0 + t * w)
        for i in ids:
            A[i]['droit'] = True; A[i]['fige'] = True
            if len(demi) >= 3: A[i]['R'] = float(np.median(demi))
    degn = lambda n: sum((x['a'] == n) + (x['b'] == n) for x in A)
    for e in A:
        if e['boucle']: e['pts'] = S.rdp(np.concatenate([e['pts'], e['pts'][:1]]), 0.5)[:-1]
        elif e['droit']: e['pts'] = np.array([m.noeuds[e['a']], m.noeuds[e['b']]])
        else:
            e['pts'][0] = m.noeuds[e['a']]; e['pts'][-1] = m.noeuds[e['b']]; p = e['pts']
            s_ = np.concatenate([[0], np.cumsum(np.sqrt((np.diff(p, axis=0) ** 2).sum(1)))]); L_ = s_[-1]; port = min(1.1 * e['R'], 0.3 * L_)
            garde = np.ones(len(p), bool)
            if degn(e['a']) >= 3: garde &= ~((s_ > 1e-6) & (s_ < port))
            if degn(e['b']) >= 3: garde &= ~((s_ < L_ - 1e-6) & (s_ > L_ - port))
            e['pts'] = S.rdp(p[garde], 0.5)
    for e in A:
        e['L'] = S.longueur(e['pts']) if not e['boucle'] else S.longueur(np.concatenate([e['pts'], e['pts'][:1]]))

# ───────────────────────────── le parcours d'un morceau ─────────────────────────────
def _tan(pts, bout, dist):
    """direction de DÉPART quand on quitte ce bout en suivant l'arête"""
    t = S.tangente(pts, bout, dist); return -t
def solutions(m, boite, mi, EM):
    """toutes les façons utiles de tracer le morceau : liste de dict {dep, fin (points), cout, pas} — une par couple (nœud de départ, nœud d'arrivée).
    pas : liste de ('t', i, sens) (arête tracée, sens 0 : a→b) et ('r', [(i, sens), …], longueur) (repassage)"""
    A = m.aretes
    if len(A) == 1 and A[0]['boucle']:
        # un anneau : un seul trait fermé. Départ en haut à droite (sens inverse des aiguilles), ou en bas à droite (sens des aiguilles).
        p = A[0]['pts']; c = p.mean(0); sols = []
        for sgn, nomv in ((1, 'h'), (-1, 'b')):
            d = np.array([math.cos(math.radians(45)), sgn * math.sin(math.radians(45))]); v = p - c
            i = int(np.argmax((v @ d) / np.maximum(np.hypot(v[:, 0], v[:, 1]), 1e-9)))
            q = np.concatenate([p[i:], p[:i + 1]])
            aire = float((q[:-1, 0] * q[1:, 1] - q[1:, 0] * q[:-1, 1]).sum())      # > 0 : sens inverse des aiguilles (y vers le haut)
            if (aire > 0) != (sgn > 0): q = q[::-1]
            sols.append(dict(dep=q[0], fin=q[-1], cout=0.0, pas=[('a', q)], ret=0.0))
        return sols
    N = len(m.noeuds); E = len(A)
    tg = [[_tan(e['pts'], 0, min(e['L'] * 0.5, 0.8 * e['R'] + 12)), _tan(e['pts'], 1, min(e['L'] * 0.5, 0.8 * e['R'] + 12))] for e in A]
    def dep_n(i, s): return A[i]['a'] if s == 0 else A[i]['b']
    def arr_n(i, s): return A[i]['b'] if s == 0 else A[i]['a']
    def dir_dep(i, s): return tg[i][s]
    def dir_arr(i, s): return -tg[i][1 - s]
    def angle(u, v): return math.degrees(math.acos(max(-1, min(1, float(u @ v)))))
    deg = [sum((e['a'] == n) + (e['b'] == n) for e in A) for n in range(N)]
    # les couples « tout droit » : (arête i, bout bi) ↔ (arête j, bout bj) au même nœud, tangentes opposées à 25° près
    couple = {}
    for n in range(N):
        inc = [(i, 0) for i, e in enumerate(A) if e['a'] == n and e['a'] != e['b']] + [(i, 1) for i, e in enumerate(A) if e['b'] == n and e['a'] != e['b']]
        if len(inc) < 3: continue
        cands = sorted((float(tg[i][bi] @ tg[j][bj]), (i, bi), (j, bj)) for (i, bi), (j, bj) in itertools.combinations(inc, 2))
        for c, x, y in cands:
            if c < -math.cos(math.radians(25)) and x not in couple and y not in couple: couple[x] = y; couple[y] = x
    memo_d = {}
    def dist(mask):
        if mask in memo_d: return memo_d[mask]
        D = np.full((N, N), np.inf); P = [[None] * N for _ in range(N)]
        for n in range(N): D[n, n] = 0
        for i, e in enumerate(A):
            if mask >> i & 1 and e['a'] != e['b']:
                if e['L'] < D[e['a'], e['b']]:
                    D[e['a'], e['b']] = D[e['b'], e['a']] = e['L']; P[e['a']][e['b']] = [(i, 0)]; P[e['b']][e['a']] = [(i, 1)]
        for k in range(N):
            for a in range(N):
                for b in range(N):
                    if D[a, k] + D[k, b] < D[a, b] - 1e-9: D[a, b] = D[a, k] + D[k, b]; P[a][b] = P[a][k] + P[k][b]
        memo_d[mask] = (D, P); return memo_d[mask]
    PLEIN = (1 << E) - 1
    def visites(mask, n0):
        v = {n0}
        for i, e in enumerate(A):
            if mask >> i & 1: v.add(e['a']); v.add(e['b'])
        return v
    def gauche(i, s):
        e = A[i]
        if not e.get('droit'): return 0.0
        d = (e['pts'][-1] - e['pts'][0]) * (1 if s == 0 else -1)
        return e['L'] / EM if d[0] < -abs(d[1]) * 0.6 and d[0] < -8 else 0.0
    sols = []
    for n0 in range(N):
        memo = {}
        def f(mask, dern):
            """rend {nœud d'arrivée : (coût, pas)} pour finir depuis cet état"""
            cle = (mask, dern)
            if cle in memo: return memo[cle]
            cur = n0 if dern is None else arr_n(*dern)
            if mask == PLEIN: memo[cle] = {cur: (0.0, [])}; return memo[cle]
            vis = visites(mask, n0); D, P = dist(mask); res = {}
            for i in range(E):
                if mask >> i & 1: continue
                for s in ((0,) if A[i]['a'] == A[i]['b'] and False else (0, 1)):
                    d0 = dep_n(i, s)
                    if d0 not in vis or not np.isfinite(D[cur, d0]): continue
                    ret = float(D[cur, d0]); c = W_RET * ret / EM
                    enchaine = ret < 1e-6 and dern is not None
                    if enchaine:
                        phi = angle(dir_arr(*dern), dir_dep(i, s)); c += W_TOUR * (phi / 180.0) ** 2 if deg[cur] >= 3 else 0.0
                        # quitter une droite qui continuait
                        for j in range(E):
                            if j == i or mask >> j & 1: continue
                            for s2 in (0, 1):
                                if dep_n(j, s2) == cur and angle(dir_arr(*dern), dir_dep(j, s2)) < 22 and phi > 40:
                                    c += W_CASSE * min(A[dern[0]]['L'], A[j]['L']) / EM
                    elif ret > 1e-6: c += 0.04
                    c += W_GAUCHE * gauche(i, s) * (0.4 if enchaine else 1.0)
                    # la seconde moitié d'une droite : elle doit suivre la première, dans le même geste
                    for bout in (0, 1):
                        par = couple.get((i, bout))
                        if par is None or not (mask >> par[0] & 1): continue
                        suit = bout == s and enchaine and dern[0] == par[0]
                        if not suit: c += W_CASSE * min(A[i]['L'], A[par[0]]['L']) / EM
                    suite = f(mask | (1 << i), (i, s))
                    pas = ([('r', P[cur][d0], ret)] if ret > 1e-6 else []) + [('t', i, s)]
                    for nf, (cf, pf) in suite.items():
                        if nf not in res or c + cf < res[nf][0] - 1e-9: res[nf] = (c + cf, pas + pf)
            memo[cle] = res; return res
        for nf, (c, pas) in f(0, None).items():
            ret = sum(p[2] for p in pas if p[0] == 'r')
            sols.append(dict(dep=m.noeuds[n0].copy(), fin=m.noeuds[nf].copy(), cout=c + (0.08 if deg[n0] > 1 else 0), pas=pas, ret=ret, n0=n0, nf=nf))
    return sols

def variantes(ms, boite, mi, EM):
    mi = seuil(boite, mi)
    """les deux variantes du glyphe (départ haut, départ bas) : pour chacune, l'ordre des morceaux et le parcours de chacun"""
    if not ms: return {}
    S_ = [solutions(m, boite, mi, EM) for m in ms]
    x0, _, x1, _ = boite; larg = max(x1 - x0, 1.0)
    def xf(p): return (p[0] - x0) / larg
    out = {}
    ordres = list(itertools.permutations(range(len(ms)))) if len(ms) <= 4 else [tuple(range(len(ms)))]
    for V in ('h', 'b'):
        best = None
        for o in ordres:
            # programmation dynamique le long de l'ordre : état = solution choisie pour le morceau courant
            cur = []
            for s in S_[o[0]]:
                if cote(s['dep'][1], mi) != V: continue
                ysm = np.concatenate([e['pts'][:, 1] for e in ms[o[0]].aretes]); haut = (ysm.max() - s['dep'][1]) / EM if V == 'h' else (s['dep'][1] - ysm.min()) / EM
                cur.append((s['cout'] + 0.05 * xf(s['dep']) + 1.0 * haut, [s]))
            for k in o[1:]:
                nxt = []
                for s in S_[k]:
                    b = None
                    for (c, ch) in cur:
                        cc = c + s['cout'] + W_SAUT * float(np.hypot(*(s['dep'] - ch[-1]['fin']))) / EM + 0.1
                        if b is None or cc < b[0]: b = (cc, ch + [s])
                    if b: nxt.append(b)
                cur = nxt
            for (c, ch) in cur:
                fin = ch[-1]['fin']; x = xf(fin)
                etroit = larg < 1.2 * 2 * max([e['R'] for m in ms for e in m.aretes if not e.get('blob')] or [larg])       # un glyphe étroit (l, i, !) : la droite n'a pas de sens
                c += 0 if etroit else W_R2 * max(0.0, 0.5 - x) * 2 - 0.2 * x
                c += W_MEME if cote(fin[1], mi) == V else 0.0
                if best is None or c < best[0] - 1e-9: best = (c, o, ch, x, etroit)
        if best: out[V] = dict(cout=best[0], ordre=best[1], sols=best[2], xfin=best[3], etroit=best[4])
    if len(out) == 2:
        mauvais = [V for V in out if not out[V]['etroit'] and out[V]['xfin'] < 0.4]
        if len(mauvais) == 1: out[mauvais[0]]['retire'] = 'finit à gauche (R2)'; out['sans'] = {mauvais[0]: out.pop(mauvais[0])}
    return out

# ───────────────────────────── les corrections à la main ─────────────────────────────
# Par police, puis par caractère. Clés :
#   'h' / 'b' : le parcours imposé, une liste de pas : entier signé = arête (1-basée, signe = sens : +3 de a vers b, −3 de b vers a),
#               telle que la planche la numérote ; 'r' = repassage (le chemin est recalculé), 's' = saut.
#   'sans'    : 'h' ou 'b' — la variante n'existe pas pour ce glyphe (exception à R3, avec sa raison dans 'pourquoi').
CORRECTIONS = {'atkinson': {}, 'gilbert': {
    'z': {'sans': 'b', 'pourquoi': "depuis le bas, le z ne finit à droite qu'au prix d'un repassage de 71 % : il n'a qu'un tracé, depuis le haut"},
    'Z': {'sans': 'b', 'pourquoi': "comme le z"},
    'J': {'sans': 'h', 'pourquoi': "depuis le haut, le J finit en bas à gauche (sa crosse) : il n'a qu'un tracé, depuis la crosse", 'bras': {2: 180}},
    'G': {'bras': {1: 180}},
    '7': {'sans': 'b', 'pourquoi': "depuis le bas, le 7 finit en haut à gauche, au bout de sa barre"},
    '2': {'sans': 'b', 'pourquoi': "depuis le bas, le 2 ne finit à droite qu'au prix d'un repassage de 76 %"},
    '?': {'bras': {2: -90}},
    'S': {'sans': 'h', 'pourquoi': "comme le s : depuis le haut il finit en bas à gauche", 'retire': [2]},
}, 'promilate': {}}

# ───────────────────────────── assemblage et écriture ─────────────────────────────
def assemble(ms, var, mi):
    """une variante → les arêtes globales (polylignes) et la liste des pas : [0, refs…] trait, [1, refs…] repassage, [2] saut"""
    base = []; n = 0
    for m in ms: base.append(n); n += len(m.aretes)
    pas = []; anneaux = []
    for rang, (k, s) in enumerate(zip(var['ordre'], var['sols'])):
        m = ms[k]
        if rang > 0: pas.append([2])
        trait = None; dern = None
        for p in s['pas']:
            if p[0] == 'a': anneaux.append(p[1]); pas.append([0, ('A', len(anneaux) - 1)]); continue
            if p[0] == 'r': pas.append([1] + [(base[k] + i + 1) * (1 if sn == 0 else -1) for (i, sn) in p[1]]); trait = None; dern = None; continue
            _, i, sn = p; ref = (base[k] + i + 1) * (1 if sn == 0 else -1); e = m.aretes[i]
            fondu = False
            if trait is not None and dern is not None:
                ed, sd = dern; pd = ms[k].aretes[ed]['pts'] if sd == 0 else ms[k].aretes[ed]['pts'][::-1]; pn = e['pts'] if sn == 0 else e['pts'][::-1]
                u = S.tangente(pd, 1, min(S.longueur(pd) * 0.5, 30)); v = -S.tangente(pn, 0, min(S.longueur(pn) * 0.5, 30))
                fondu = math.degrees(math.acos(max(-1, min(1, float(u @ v))))) < ANGLE_FONDU
            if fondu: trait.append(ref)
            else: trait = [0, ref]; pas.append(trait)
            dern = (i, sn)
    return pas, anneaux

def poly_ref(ms, ref):
    n = 0
    for m in ms:
        for e in m.aretes:
            n += 1
            if n == abs(ref): return e['pts'] if ref > 0 else e['pts'][::-1]
    raise KeyError(ref)

def analyse(police, ch, nom, mi, EM, corr):
    ms, boite, R = morceaux(police, nom)
    if not ms: return None
    if corr.get('retire'):
        # retirer des arêtes (numérotées comme sur la planche) : une barbe que l'amincissement a laissée au bout d'un trait coupé en biais
        k = 0
        for m in ms:
            garde = []
            for e in m.aretes:
                k += 1
                if k not in corr['retire']: garde.append(e)
            m.aretes = garde
    if corr.get('bras'):
        # un bras court dont l'amincissement a perdu la direction : on la donne (en degrés, 0 = vers la droite, 90 = vers le haut) ; il part de
        # l'embranchement et va jusqu'au bord de l'encre
        k = 0
        for m in ms:
            for e in m.aretes:
                k += 1
                if k not in corr['bras']: continue
                deg = lambda n: sum((x['a'] == n) + (x['b'] == n) for x in m.aretes)
                anc, lib = (e['a'], e['b']) if deg(e['a']) >= deg(e['b']) else (e['b'], e['a'])
                ang = math.radians(corr['bras'][k]); v = np.array([math.cos(ang), math.sin(ang)]); P = m.noeuds[anc]
                X = P + v * morceaux.bord(P + v * 2.0, v, 8 * R); m.noeuds[lib] = X
                e['pts'] = np.array([P, X]) if e['a'] == anc else np.array([X, P]); e['droit'] = True; e['L'] = float(np.hypot(*(X - P))); e['R'] = max(e['R'], 0.97 * R)
    vs = variantes(ms, boite, mi, EM)
    if corr.get('sans') in vs and len([k for k in vs if k in 'hb']) == 2:
        v0 = vs.pop(corr['sans']); v0['retire'] = corr.get('pourquoi', ''); vs.setdefault('sans', {})[corr['sans']] = v0
    return dict(ms=ms, boite=boite, R=R, vs=vs, cts=S.contours(police, nom))

def ecrit(cle, glyphes, upm, mi, sortie):
    P = POLICES[cle]; lignes = []
    def nb(v): v = round(float(v), 1); return str(int(v)) if v == int(v) else ('%.1f' % v)
    for ch in sorted(glyphes):
        g = glyphes[ch]; ms = g['ms']
        ar = []
        for m in ms:
            for e in m.aretes: ar.append('[' + nb(e['R']) + ',' + ','.join(nb(v) for v in (e['pts'].round().flatten() if True else [])) + ']')
        vtxt = []
        for V in ('h', 'b'):
            if V not in g['vs']: continue
            var = g['vs'][V]; pas, anneaux = assemble(ms, var, mi)
            # un anneau a sa propre polyligne par variante : on l'ajoute aux arêtes
            for i, q in enumerate(anneaux):
                R = max(e['R'] for m in ms for e in m.aretes if e['boucle']) if any(e['boucle'] for m in ms for e in m.aretes) else g['R']
                ar.append('[' + nb(R) + ',' + ','.join(nb(v) for v in q.round().flatten()) + ']'); idx = len(ar)
                for p in pas:
                    for j in range(1, len(p)):
                        if p[j] == ('A', i): p[j] = idx
            fin = var['sols'][-1]['fin']
            vtxt.append('%s:{f:"%s",t:%s}' % (V, cote(fin[1], seuil(g['boite'], mi)), json.dumps(pas, separators=(',', ':'))))
        lignes.append('%s:{a:%s,bo:[%s],e:[%s],%s}' % (json.dumps(ch, ensure_ascii=False), nb(g['av']), ','.join(nb(v) for v in g['boite']), ','.join(ar), ','.join(vtxt)))
    txt = ("/* trace-chemins-%s.js — LES CHEMINS DU TRACÉ DES LETTRES pour la police %s (C-125).\n"
           "   ENGENDRÉ par scratchpad/v146/trace/chemins.py — on corrige le générateur (ou sa table CORRECTIONS), jamais ce fichier.\n"
           "   Par glyphe : a = chasse ; bo = boîte d'encre [x0,y0,x1,y1] ; e = arêtes de la ligne médiane [demi-largeur, x,y, x,y, …] (unités de police,\n"
           "   y vers le haut, origine du glyphe sur la ligne de base) ; h / b = la variante « départ en haut » / « départ en bas » (haut, bas : de part\n   et d'autre du milieu de la hauteur d'encre du glyphe ; ce qui vit tout en haut de la ligne est toujours « haut », tout en bas toujours « bas ») :\n"
           "   f = le côté où elle finit ; t = les pas : [0, réf…] un trait (arêtes enchaînées ; réf = numéro d'arête à partir de 1, négatif = à rebours),\n"
           "   [1, réf…] un repassage (invisible), [2] un saut (invisible). La police n'est pas modifiée : ses glyphes sont DÉVOILÉS le long de ces lignes. */\n"
           "(function(){ var D={nom:%s,upm:%d,mi:%d,g:{\n%s\n}};\n  var R=(typeof window!=='undefined'?window:globalThis); (R.TraceLettresChemins=R.TraceLettresChemins||{})[D.nom]=D; })();\n") % (
        cle, P['nom'], json.dumps(P['nom']), upm, mi, ',\n'.join(lignes))
    io.open(os.path.join(RACINE, 'variantes', sortie), 'w', encoding='utf-8').write(txt)
    return len(txt)

def principal():
    cle = next((a for a in sys.argv[1:] if not a.startswith('--')), 'gilbert'); P = POLICES[cle]
    arg = lambda k, d=None: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
    police = TTFont(P['fichier']); cm = police.getBestCmap(); upm = police['head'].unitsPerEm
    xh = getattr(police['OS/2'], 'sxHeight', 0) or 0.5 * upm; mi = int(round(xh / 2))
    seul = arg('seul'); t0 = time.time(); glyphes = {}
    codes = sorted(cm) if not seul else [ord(c) for c in seul]
    if cle == 'atkinson' and not seul: codes = [c for c in codes if c < 0x180 or c in (0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x2013, 0x2014, 0x20AC)]   # v147 : le latin du produit
    for code in codes:
        ch = chr(code)
        if ch.isspace() or code < 33 or code == 0xAD: continue
        try: g = analyse(police, ch, cm[code], mi, upm, CORRECTIONS[cle].get(ch, {}))
        except Exception as ex:
            print('ERREUR', repr(ch), ex); continue
        if not g or not g['vs']: print('VIDE', repr(ch)); continue
        g['av'] = police['hmtx'][cm[code]][0]; glyphes[ch] = g
    print('%d glyphes en %.1f s' % (len(glyphes), time.time() - t0))
    if not seul: print('écrit', P['sortie'], ecrit(cle, glyphes, upm, mi, P['sortie']), 'octets')
    if '--planche' in sys.argv:
        import planche; planche.planches(cle, glyphes, mi, upm)
    return glyphes

if __name__ == '__main__': principal()
