#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
squelette.py — de la police au GRAPHE de la ligne médiane (C-125, le tracé des lettres).

Pour un glyphe : contours (fontTools) → image pleine → amincissement (Zhang-Suen, numpy) → graphe (nœuds : bouts et embranchements ;
arêtes : chaînes de points) → élagage des barbes → coins vifs (découpe + remise au carré) → lissage → redressement des droites.
Tout est rendu en UNITÉS DE POLICE (y vers le haut, origine du glyphe sur la ligne de base).
Ni scipy ni scikit-image : tout est écrit en numpy.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from fontTools.pens.recordingPen import DecomposingRecordingPen

U = 2.0          # unités de police par pixel de l'image de travail
MARGE = 12       # pixels de marge autour du glyphe

# ───────────────────────────── contours ─────────────────────────────
def _cubique(p0, p1, p2, p3, n=14):
    t = np.linspace(0, 1, n + 1)[1:, None]
    a, b, c, d = map(np.array, (p0, p1, p2, p3))
    return ((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d).tolist()
def _quad(p0, p1, p2, n=10):
    t = np.linspace(0, 1, n + 1)[1:, None]
    a, b, c = map(np.array, (p0, p1, p2))
    return ((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c).tolist()
def contours(police, nom):
    """les contours d'un glyphe, aplatis en polygones (unités de police)"""
    gs = police.getGlyphSet(); pen = DecomposingRecordingPen(gs); gs[nom].draw(pen)
    out, cur = [], []
    for op, args in pen.value:
        if op == 'moveTo':
            if len(cur) > 2: out.append(cur)
            cur = [list(args[0])]
        elif op == 'lineTo': cur.append(list(args[0]))
        elif op == 'curveTo':
            if len(args) == 3: cur += _cubique(cur[-1], *args)
            else:   # super-bézier : rare, on passe par les points
                for a in args: cur.append(list(a))
        elif op == 'qCurveTo':
            pts = list(args); p0 = cur[-1]
            for i in range(len(pts) - 1):
                c = pts[i]; f = pts[i + 1] if i == len(pts) - 2 else [(pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2]
                cur += _quad(p0, c, f); p0 = f
        elif op in ('closePath', 'endPath'):
            if len(cur) > 2: out.append(cur)
            cur = []
    if len(cur) > 2: out.append(cur)
    return out

def image(cts):
    """l'image pleine (règle du nombre d'enroulement non nul) ; rend (img bool, x0, y1) : px=(x-x0)/U, py=(y1-y)/U"""
    xs = [p[0] for c in cts for p in c]; ys = [p[1] for c in cts for p in c]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    x0 -= MARGE * U; y1 += MARGE * U
    W = int(math.ceil((x1 - x0) / U)) + MARGE; H = int(math.ceil((y1 - y0) / U)) + MARGE
    acc = np.zeros((H, W), np.int16)
    for c in cts:
        aire = sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c)))
        im = Image.new('L', (W, H), 0)
        ImageDraw.Draw(im).polygon([((p[0] - x0) / U, (y1 - p[1]) / U) for p in c], fill=1)
        acc += (1 if aire > 0 else -1) * np.asarray(im, np.int16)
    return acc != 0, x0, y1

# ───────────────────────────── amincissement ─────────────────────────────
def amincit(img):
    I = np.pad(img.astype(np.uint8), 1)
    while True:
        chg = False
        for etape in (0, 1):
            P2 = I[:-2, 1:-1]; P3 = I[:-2, 2:]; P4 = I[1:-1, 2:]; P5 = I[2:, 2:]; P6 = I[2:, 1:-1]; P7 = I[2:, :-2]; P8 = I[1:-1, :-2]; P9 = I[:-2, :-2]
            C = I[1:-1, 1:-1]
            B = P2.astype(np.int16) + P3 + P4 + P5 + P6 + P7 + P8 + P9
            s = [P2, P3, P4, P5, P6, P7, P8, P9, P2]
            A = sum(((s[i] == 0) & (s[i + 1] == 1)).astype(np.int16) for i in range(8))
            if etape == 0: m = (C == 1) & (B >= 2) & (B <= 6) & (A == 1) & (P2 * P4 * P6 == 0) & (P4 * P6 * P8 == 0)
            else: m = (C == 1) & (B >= 2) & (B <= 6) & (A == 1) & (P2 * P4 * P8 == 0) & (P2 * P6 * P8 == 0)
            if m.any(): C[m] = 0; chg = True
        if not chg: break
    # les marches d'escalier : un point qui a deux voisins directs en équerre et rien en face est de trop
    for _ in range(2):
        for (a, b, c) in (((-1, 0), (0, 1), (1, -1)), ((0, 1), (1, 0), (-1, -1)), ((1, 0), (0, -1), (-1, 1)), ((0, -1), (-1, 0), (1, 1))):
            C = I[1:-1, 1:-1]; H, W = C.shape
            v = lambda d: I[1 + d[0]:1 + d[0] + H, 1 + d[1]:1 + d[1] + W]
            m = (C == 1) & (v(a) == 1) & (v(b) == 1) & (v(c) == 0)
            if m.any(): C[m] = 0
    return I[1:-1, 1:-1].astype(bool)

VOIS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
def composantes(img):
    """étiquette les composantes 8-connexes (parcours simple)"""
    H, W = img.shape; lab = np.zeros((H, W), np.int32); n = 0
    ys, xs = np.nonzero(img)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if lab[y, x]: continue
        n += 1; pile = [(y, x)]; lab[y, x] = n
        while pile:
            cy, cx = pile.pop()
            for dy, dx in VOIS:
                yy, xx = cy + dy, cx + dx
                if 0 <= yy < H and 0 <= xx < W and img[yy, xx] and not lab[yy, xx]: lab[yy, xx] = n; pile.append((yy, xx))
    return lab, n

def rayon(img, pts_px):
    """la distance au bord (en pixels) de quelques points : au plus près des points du fond"""
    bord = img & ~(np.roll(img, 1, 0) & np.roll(img, -1, 0) & np.roll(img, 1, 1) & np.roll(img, -1, 1))
    by, bx = np.nonzero(bord); B = np.stack([bx, by], 1).astype(np.float32)
    P = np.asarray(pts_px, np.float32).reshape(-1, 2); out = np.zeros(len(P), np.float32)
    for i in range(0, len(P), 256):
        d = P[i:i + 256, None, :] - B[None, :, :]; out[i:i + 256] = np.sqrt((d ** 2).sum(2).min(1))
    return out + 0.5

# ───────────────────────────── graphe ─────────────────────────────
class Graphe:
    """noeuds : liste de [x, y] (pixels flottants) ; aretes : liste de dict {a, b, pts (Nx2 px, de a vers b), boucle}"""
    def __init__(self): self.noeuds = []; self.aretes = []
    def degre(self, n): return sum((e['a'] == n) + (e['b'] == n) for e in self.aretes)
    def incid(self, n): return [(i, 0) for i, e in enumerate(self.aretes) if e['a'] == n] + [(i, 1) for i, e in enumerate(self.aretes) if e['b'] == n]

def graphe(sk):
    H, W = sk.shape; P = np.pad(sk, 1).astype(np.uint8)
    nb = sum(P[1 + dy:1 + dy + H, 1 + dx:1 + dx + W] for dy, dx in VOIS) * sk
    jonc = sk & (nb >= 3)
    labj, nj = composantes(jonc)
    G = Graphe(); idn = {}
    for k in range(1, nj + 1):
        ys, xs = np.nonzero(labj == k); G.noeuds.append([float(xs.mean()), float(ys.mean())]); idn[k] = len(G.noeuds) - 1
    reste = sk & ~jonc
    labc, nc = composantes(reste)
    for k in range(1, nc + 1):
        ys, xs = np.nonzero(labc == k); pix = set(zip(ys.tolist(), xs.tolist()))
        def vs(p): return [(p[0] + dy, p[1] + dx) for dy, dx in VOIS if (p[0] + dy, p[1] + dx) in pix]
        bouts = [p for p in pix if len(vs(p)) <= 1]
        if not bouts:   # un anneau sans nœud
            dep = next(iter(pix)); ch = [dep]; vu = {dep}
            while True:
                nx = [q for q in vs(ch[-1]) if q not in vu]
                if not nx: break
                # préférer le voisin direct (4-connexe) pour ne pas sauter une marche
                nx.sort(key=lambda q: abs(q[0] - ch[-1][0]) + abs(q[1] - ch[-1][1])); ch.append(nx[0]); vu.add(nx[0])
            G.aretes.append({'a': None, 'b': None, 'pts': np.array([[p[1], p[0]] for p in ch], float), 'boucle': True}); continue
        dep = bouts[0]; ch = [dep]; vu = {dep}
        while True:
            nx = [q for q in vs(ch[-1]) if q not in vu]
            if not nx: break
            nx.sort(key=lambda q: abs(q[0] - ch[-1][0]) + abs(q[1] - ch[-1][1])); ch.append(nx[0]); vu.add(nx[0])
        def attache(p, autre):
            """le nœud d'un bout de chaîne : l'embranchement voisin, sinon un bout libre"""
            js = set()
            for dy, dx in VOIS:
                yy, xx = p[0] + dy, p[1] + dx
                if 0 <= yy < H and 0 <= xx < W and labj[yy, xx]: js.add(idn[labj[yy, xx]])
            if js:
                js = sorted(js, key=lambda n: (G.noeuds[n][0] - p[1]) ** 2 + (G.noeuds[n][1] - p[0]) ** 2)
                if autre is not None and len(js) > 1 and js[0] == autre and len(ch) < 3: return js[1]
                return js[0]
            G.noeuds.append([float(p[1]), float(p[0])]); return len(G.noeuds) - 1
        a = attache(ch[0], None); b = attache(ch[-1], a if len(ch) < 3 else None)
        pts = [G.noeuds[a]] + [[p[1], p[0]] for p in ch] + [G.noeuds[b]]
        # un bout libre : le nœud EST le premier point
        pts = np.array(pts, float)
        d = np.abs(np.diff(pts, axis=0)).sum(1); garde = np.concatenate([[True], d > 1e-6])
        G.aretes.append({'a': a, 'b': b, 'pts': pts[garde], 'boucle': False})
    return G

def longueur(pts): return float(np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)).sum()) if len(pts) > 1 else 0.0
def reechant(pts, pas):
    """rééchantillonne une ligne brisée à pas constant (bouts gardés)"""
    pts = np.asarray(pts, float)
    if len(pts) < 2: return pts.copy()
    d = np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)); s = np.concatenate([[0], np.cumsum(d)]); L = s[-1]
    if L < 1e-9: return pts[:1].copy()
    n = max(1, int(round(L / pas))); t = np.linspace(0, L, n + 1)
    return np.stack([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])], 1)
def lisse(pts, demi):
    """moyenne glissante, bouts fixes (on prolonge par symétrie centrale autour de chaque bout)"""
    pts = np.asarray(pts, float); n = len(pts)
    if n < 4 or demi < 1: return pts.copy()
    demi = min(demi, n - 2)
    av = 2 * pts[0] - pts[1:demi + 1][::-1]; ap = 2 * pts[-1] - pts[-demi - 1:-1][::-1]
    Q = np.concatenate([av, pts, ap]); k = np.ones(2 * demi + 1) / (2 * demi + 1)
    out = np.stack([np.convolve(Q[:, 0], k, 'valid'), np.convolve(Q[:, 1], k, 'valid')], 1)
    out[0] = pts[0]; out[-1] = pts[-1]; return out
def rdp(pts, tol):
    pts = np.asarray(pts, float)
    if len(pts) < 3: return pts
    garde = np.zeros(len(pts), bool); garde[0] = garde[-1] = True; pile = [(0, len(pts) - 1)]
    while pile:
        a, b = pile.pop()
        if b <= a + 1: continue
        v = pts[b] - pts[a]; n = math.hypot(*v)
        q = pts[a + 1:b] - pts[a]
        d = np.abs(q[:, 0] * v[1] - q[:, 1] * v[0]) / n if n > 1e-9 else np.sqrt((q ** 2).sum(1))
        i = int(d.argmax())
        if d[i] > tol: garde[a + 1 + i] = True; pile += [(a, a + 1 + i), (a + 1 + i, b)]
    return pts[garde]
def ecart_corde(pts):
    pts = np.asarray(pts, float); v = pts[-1] - pts[0]; n = math.hypot(*v)
    if n < 1e-9 or len(pts) < 3: return 0.0
    q = pts[1:-1] - pts[0]; return float((np.abs(q[:, 0] * v[1] - q[:, 1] * v[0]) / n).max())
def tangente(pts, bout, dist):
    """la direction SORTANTE à un bout (0 : début, 1 : fin), mesurée sur `dist` de longueur"""
    pts = np.asarray(pts, float)
    if bout == 0: pts = pts[::-1]
    d = np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)); s = np.concatenate([[0], np.cumsum(d)]); L = s[-1]
    t = max(L - dist, 0.0); p = np.array([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])])
    v = pts[-1] - p; n = math.hypot(*v)
    return v / n if n > 1e-9 else np.array([1.0, 0.0])

def elague(G, img, R):
    """retire les barbes : une arête qui finit en bout libre et dont le disque du bout tient dans celui de l'embranchement"""
    while True:
        fait = False
        for i, e in enumerate(G.aretes):
            if e['boucle'] or e['a'] == e['b']: continue
            da, db = G.degre(e['a']), G.degre(e['b'])
            if (da == 1) == (db == 1): continue
            libre, emb = (e['a'], e['b']) if da == 1 else (e['b'], e['a'])
            L = longueur(e['pts']); rl, re = rayon(img, [G.noeuds[libre], G.noeuds[emb]])
            if L + rl <= re * 1.25 + 1.5 or L < 0.45 * R:
                G.aretes.pop(i); fait = True; break
        if not fait: break
    fusionne(G)
def fusionne(G):
    """recolle les arêtes à travers un nœud de degré 2 ; un nœud de degré 2 sur une boucle fermée la rend à l'état d'anneau"""
    while True:
        fait = False
        for n in range(len(G.noeuds)):
            inc = G.incid(n)
            if len(inc) != 2: continue
            (i, bi), (j, bj) = inc
            if i == j:
                e = G.aretes[i]; e['a'] = e['b'] = None; e['boucle'] = True; e['pts'] = e['pts'][:-1]; fait = True; break
            ei, ej = G.aretes[i], G.aretes[j]
            pi = ei['pts'] if bi == 1 else ei['pts'][::-1]; pj = ej['pts'] if bj == 0 else ej['pts'][::-1]
            a = ei['a'] if bi == 1 else ei['b']; b = ej['b'] if bj == 0 else ej['a']
            neuf = {'a': a, 'b': b, 'pts': np.concatenate([pi, pj[1:]]), 'boucle': False}
            for k in sorted((i, j), reverse=True): G.aretes.pop(k)
            G.aretes.append(neuf); fait = True; break
        if not fait: break
