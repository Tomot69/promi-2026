#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""planche.py — les planches de relecture des chemins : pour chaque glyphe, ses deux variantes (départ haut, départ bas).
Trait plein coloré = un trait visible, dans l'ordre (1, 2, 3…), avec sa flèche ; tirets gris = repassage ; pointillés = saut ;
rond vert = départ, carré rouge = arrivée ; petits chiffres gris = numéros d'arête (pour la table CORRECTIONS)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import squelette as S, chemins as C

COUL = [(214, 48, 49), (9, 132, 227), (0, 148, 100), (225, 135, 0), (140, 70, 200), (0, 150, 160), (230, 60, 150), (90, 90, 90), (150, 110, 60), (60, 60, 200)]
CW, CH, ECH = 330, 400, 0.33
def _police(t):
    for p in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc'):
        if os.path.exists(p): return ImageFont.truetype(p, t)
    return ImageFont.load_default()
F12, F10, F16 = _police(12), _police(10), _police(15)

def cellule(ch, g, V, mi, upm):
    im = Image.new('RGB', (CW, CH), (255, 255, 255)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = g['boite']; ech = min(ECH, (CW - 30) / max(x1 - x0, 1), (CH - 60) / max(y1 - y0 + 1, 1))
    ox = (CW - (x1 - x0) * ech) / 2 - x0 * ech; oy = 34 + (CH - 50 - (y1 - y0) * ech) / 2 + y1 * ech
    P = lambda p: (ox + p[0] * ech, oy - p[1] * ech)
    acc = np.zeros((CH, CW), np.int16)
    for c in g['cts']:
        aire = sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c)))
        m = Image.new('L', (CW, CH), 0); ImageDraw.Draw(m).polygon([P(p) for p in c], fill=1); acc += (1 if aire > 0 else -1) * np.asarray(m, np.int16)
    a = np.asarray(im).copy(); a[acc != 0] = (222, 222, 222); im = Image.fromarray(a); d = ImageDraw.Draw(im)
    mi = C.seuil(g['boite'], mi)
    if abs(mi) < 1e8: yl = oy - mi * ech; d.line([(4, yl), (CW - 4, yl)], fill=(190, 210, 255))
    if V not in g['vs']:
        d.text((6, 4), '%s  %s : PAS DE VARIANTE' % (ch, V.upper()), fill=(200, 0, 0), font=F12); return im
    var = g['vs'][V]; ms = g['ms']; pas, anneaux = C.assemble(ms, var, mi)
    def poly(ref):
        if isinstance(ref, tuple): return anneaux[ref[1]]
        return C.poly_ref(ms, ref)
    n = 0; Ltr = 0.0; Lret = 0.0; prec = None; dep = None
    for p in pas:
        if p[0] == 2: continue
        pts = np.concatenate([poly(r) if i == 0 else poly(r)[1:] for i, r in enumerate(p[1:])])
        if p[0] == 1:
            Lret += S.longueur(pts); q = S.reechant(pts, 14 / ech / 5)
            for i in range(0, len(q) - 1, 2): d.line([P(q[i] + 0), P(q[i + 1])], fill=(60, 60, 60), width=1)
            continue
        if prec is not None and np.hypot(*(pts[0] - prec)) > 2 and pas[pas.index(p) - 1][0] == 2:
            q = S.reechant(np.array([prec, pts[0]]), 6 / ech)
            for qq in q: x, y = P(qq); d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(120, 120, 120))
        col = COUL[n % len(COUL)]; n += 1; Ltr += S.longueur(pts)
        d.line([P(q) for q in pts], fill=col, width=3)
        # flèches : au milieu et près du bout
        s = np.concatenate([[0], np.cumsum(np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)))]); L = s[-1]
        for t in ([0.5 * L, L - 18 / ech * 0.2] if L > 60 else [0.6 * L]):
            a_ = np.array([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])]); b_ = np.array([np.interp(min(L, t + 6), s, pts[:, 0]), np.interp(min(L, t + 6), s, pts[:, 1])])
            v = b_ - a_; nv = math.hypot(*v)
            if nv < 1e-6: continue
            v = v / nv; w = np.array([-v[1], v[0]]); T = 7 / ech
            d.polygon([P(a_ + v * T), P(a_ - v * T * 0.3 + w * T * 0.7), P(a_ - v * T * 0.3 - w * T * 0.7)], fill=col)
        x, y = P(pts[0]); d.text((x + 5, y - 13), str(n), fill=col, font=F12)
        if dep is None: dep = pts[0]
        prec = pts[-1]
    if dep is not None:
        x, y = P(dep); d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(0, 140, 0), width=2)
        x, y = P(prec); d.rectangle([x - 4, y - 4, x + 4, y + 4], outline=(220, 0, 0), width=2)
    # numéros d'arête
    k = 0
    for m in ms:
        for e in m.aretes:
            k += 1; q = e['pts'][len(e['pts']) // 2] if len(e['pts']) > 2 else (e['pts'][0] + e['pts'][-1]) / 2; x, y = P(q); d.text((x - 10, y + 2), str(k), fill=(130, 130, 130), font=F10)
    bx0, _, bx1, _ = g['boite']; xfin = (prec[0] - bx0) / max(bx1 - bx0, 1) if prec is not None else 0
    d.text((6, 4), '%s  %s→%s' % (ch, V.upper(), C.cote(prec[1], mi).upper()), fill=(0, 0, 0), font=F16)
    d.text((6, 20), 'repass. %d %%   fin x=%.2f   coût %.2f' % (round(100 * Lret / max(Ltr, 1)), xfin, var['cout']), fill=(70, 70, 70), font=F10)
    return im

def planches(cle, glyphes, mi, upm, par=15, prefixe=None):
    chars = sorted(glyphes); cols = 6; noms = []
    for n in range(0, len(chars), par):
        lot = chars[n:n + par]; rangs = (len(lot) * 2 + cols - 1) // cols
        out = Image.new('RGB', (cols * CW, rangs * CH), (255, 255, 255)); d = ImageDraw.Draw(out)
        for i, ch in enumerate(lot):
            for j, V in enumerate('hb'):
                c = cellule(ch, glyphes[ch], V, mi, upm); k = i * 2 + j; out.paste(c, ((k % cols) * CW, (k // cols) * CH))
        for x in range(0, cols * CW, 2 * CW): d.line([(x, 0), (x, rangs * CH)], fill=(170, 170, 170))
        nom = os.path.join(C.ICI, '%s-%s-%d.png' % (prefixe or 'planche', cle, n // par + 1)); out.save(nom); noms.append(nom)
    print('planches :', len(noms)); return noms
