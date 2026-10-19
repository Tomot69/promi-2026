# v153 C-125 — sonde géométrique : à chaque pas, le dévoilé est-il un préfixe du chemin, le front perpendiculaire, l'alpha franc ?
import sys, json, math, io; sys.path.insert(0, '.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
CAS = [('Gilbert', '700', 'o'), ('Gilbert', '700', 's'), ('Gilbert', '700', 'g'), ('Atkinson', '500', 'o'), ('Atkinson', '500', 's'), ('Atkinson', '500', 'g')]
SEUL = next((a.split('=')[1] for a in sys.argv if a.startswith('--seul=')), None)
if SEUL: CAS = [c for c in CAS if c[0][0] + c[2] == SEUL]
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), '60'))
PREP = """async a=>{ const [pol, gr, car]=a; let el=document.getElementById('gEl'); if(el) el.remove(); document.querySelectorAll('canvas[data-trace]').forEach(c=>c.remove());
  el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:60px;top:80px;width:300px;font:'+gr+' 150px/180px '+pol+';color:#291547;background:none;z-index:60'; el.textContent=car; document.body.appendChild(el);
  await document.fonts.load(gr+' 150px '+pol); await document.fonts.ready;
  window.GC=TraceLettres.trace(el, null, {manuel:true, respecteReduire:false}); await GC.pret;
  const cv=GC.canevas, cr=cv.getBoundingClientRect(), er=el.getBoundingClientRect(), d=devicePixelRatio, g=GC.glyphes[0];
  const gx=(er.left+g.x-cr.left)*d, gy=(er.top+g.y-cr.top)*d;
  const R=document.createElement('canvas'); R.width=cv.width; R.height=cv.height; const x=R.getContext('2d'); x.setTransform(d,0,0,d,gx,gy); x.font=gr+' 150px '+pol; x.fillStyle='#291547'; x.textBaseline='alphabetic'; x.fillText(car,0,0);
  const A=x.getImageData(0,0,R.width,R.height).data, ref=[]; for(let i=3;i<A.length;i+=4) ref.push(A[i]);
  const pc=TraceLettres.parcours(pol, car, g.variante), u=g.ech*d;
  return {w:cv.width, h:cv.height, ref, traits:pc.traits.map(t=>({R:t.R*u, pts:t.pts.map(q=>[gx+q[0]*u, gy-q[1]*u])})), v:g.variante, duree:GC.duree}; }"""
LIT = """f=>{ GC.va(f); const cv=GC.canevas; const D=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; const o=new Array(D.length/4); for(let i=0;i<o.length;i++) o[i]=D[4*i+3]; return o; }"""
def chaikin(P):
    import math as m
    a0, b0 = P[0], P[-1]; Lk = m.hypot(b0[0] - a0[0], b0[1] - a0[1]); ec = 0
    for q in P[1:-1]:
        if Lk > 0: ec = max(ec, abs((q[0] - a0[0]) * (b0[1] - a0[1]) - (q[1] - a0[1]) * (b0[0] - a0[0])) / Lk)
    if len(P) < 3 or (Lk > 0 and ec < 0.6): return P
    for _ in range(int(next((a.split('=')[1] for a in sys.argv if a.startswith('--lissage=')), '2'))):
        Q = [P[0]]
        for j in range(len(P) - 1):
            u0, u1 = P[j], P[j + 1]
            if j > 0: Q.append([0.75 * u0[0] + 0.25 * u1[0], 0.75 * u0[1] + 0.25 * u1[1]])
            if j < len(P) - 2: Q.append([0.25 * u0[0] + 0.75 * u1[0], 0.25 * u0[1] + 0.75 * u1[1]])
        Q.append(P[-1]); P = Q
    return P
def projette(traits, w, h):
    ys, xs = np.mgrid[0:h, 0:w]; px = xs + 0.5; py = ys + 0.5
    best = np.full((h, w), np.inf); S = np.zeros((h, w)); K = np.zeros((h, w), int); s0 = 0.0; bornes = []
    for k, t in enumerate(traits):
        P = t['pts']; acc = 0.0
        for i in range(len(P) - 1):
            ax, ay = P[i]; bx, by = P[i + 1]; vx, vy = bx - ax, by - ay; L = math.hypot(vx, vy)
            if L < 1e-9: continue
            u = np.clip(((px - ax) * vx + (py - ay) * vy) / (L * L), 0, 1); dx = px - (ax + u * vx); dy = py - (ay + u * vy); d2 = dx * dx + dy * dy
            m = d2 < best; best[m] = d2[m]; S[m] = s0 + acc + u[m] * L; K[m] = k; acc += L
        bornes.append((s0, s0 + acc)); s0 += acc
    return S, np.sqrt(best), K, bornes, s0
def point(P, s):
    acc = 0.0
    for i in range(len(P) - 1):
        L = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
        if acc + L >= s and L > 0: u = (s - acc) / L; return (P[i][0] + u * (P[i + 1][0] - P[i][0]), P[i][1] + u * (P[i + 1][1] - P[i][1]))
        acc += L
    return tuple(P[-1])
def tangente(traits, bornes, s):
    for k, t in enumerate(traits):
        a, b = bornes[k]
        if a <= s <= b:
            R = t['R']; p0 = point(t['pts'], max(0, s - a - R)); p1 = point(t['pts'], min(b - a, s - a + R)); dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1
            return k, (dx / L, dy / L), min(s - a, b - s)
    return None, None, 0
FILM = []
def analyse(info, lit):
    w, h = info['w'], info['h']; ref = np.array(info['ref'], float).reshape(h, w); T = info['traits']
    for t in T: t['pts'] = chaikin(t['pts'])
    S, dist, K, bornes, Ltot = projette(T, w, h); Rm = max(t['R'] for t in T)
    autre = np.full((h, w), np.inf)
    for kk in range(len(T)):
        if len(T) == 1: break
        Sx, dx_, Kx, _, _ = projette([t for j, t in enumerate(T) if j != kk], w, h); m_ = (K == kk); autre[m_] = dx_[m_]
    refx = np.array(info['ref'], float).reshape(h, w); ref = np.array(lit(0.99999), float).reshape(h, w)
    out0 = int((np.abs(refx - ref) > 40).sum())
    # les zones ambiguës : autour des bouts de chaque trait (fermeture d'une boucle, jonction, embranchement)
    ys, xs = np.mgrid[0:h, 0:w]; amb = np.zeros((h, w), bool)
    for t in T:
        for q in (t['pts'][0], t['pts'][-1]): amb |= np.hypot(xs + 0.5 - q[0], ys + 0.5 - q[1]) < 1.3 * t['R'] + 3
    out = {'ecart_texte': out0, 'pas': 0, 'hors': 0, 'trous': 0, 'avance': 0, 'partiels_loin': 0, 'angles': [], 'interm_max': 0}
    core = ref > 200; ink = ref > 127
    for i in range(1, N):
        cur = np.array(lit(i / N), float).reshape(h, w)
        hors = int(((cur > ref + 10)).sum()); out['hors'] += hors
        rev = core & (cur >= ref - 10); unr = ink & (cur <= 10)
        if '--film' in sys.argv: FILM.append(np.stack([ (ref // 3).astype(np.uint8), cur.astype(np.uint8), np.zeros((h, w), np.uint8)], 2))
        if rev.sum() < 30 or unr.sum() < 30: continue
        out['pas'] += 1
        if '--ilots' in sys.argv:
            from collections import deque
            u_ = core & (cur <= 10); lab = np.zeros((h, w), int); nl = 0
            for y0, x0 in zip(*np.nonzero(u_)):
                if lab[y0, x0]: continue
                nl += 1; lab[y0, x0] = nl; dq = deque([(y0, x0)])
                while dq:
                    y1, x1 = dq.popleft()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            y2, x2 = y1 + dy, x1 + dx
                            if 0 <= y2 < h and 0 <= x2 < w and u_[y2, x2] and not lab[y2, x2]: lab[y2, x2] = nl; dq.append((y2, x2))
            if u_.sum() > 0.1 * core.sum():
                for j in range(1, nl + 1):
                    sz = int((lab == j).sum())
                    if 12 <= sz <= 0.015 * core.sum():
                        yy_, xx_ = np.nonzero(lab == j); print('   pas %d îlot %d px vers (%d,%d)' % (i, sz, int(xx_.mean()), int(yy_.mean())))
                        im = np.zeros((h, w, 3), np.uint8); im[..., 1] = cur.astype(np.uint8); im[..., 0] = (ref // 3).astype(np.uint8); im[lab == j] = (255, 0, 0)
                        Image.fromarray(im).save('scratchpad/v153/ilot-%s-%d.png' % (info.get('nom'), i))
        tol = Rm + 3; zone = core & ~amb & (dist < Rm * 1.6)
        Sz = S[zone]; Rz = rev[zone]; o_ = np.argsort(Sz); lab = Rz[o_]
        # la coupe qui sépare le mieux dévoilé (avant) et non dévoilé (après)
        err = np.concatenate([[0], np.cumsum(~lab)]) + np.concatenate([np.cumsum(lab[::-1])[::-1], [0]])
        j = int(np.argmin(err)); sf = float(Sz[o_][min(j, len(o_) - 1)]) if len(o_) else 0
        trous = int((zone & ~rev & (S < sf - tol)).sum()); avance = int((zone & rev & (S > sf + tol)).sum())
        out['trous'] = max(out['trous'], trous); out['avance'] = max(out['avance'], avance)
        part = (ref > 0) & (cur > 10) & (cur < ref - 10)
        # un partiel doit toucher (à 2 px) de l'encre non dévoilée
        from numpy.lib.stride_tricks import sliding_window_view as sw
        rat = np.where(ref > 127, cur / np.maximum(ref, 1), 9.0); padr = np.pad(rat, 2, constant_values=9.0); mn = sw(padr, (5, 5)).min(axis=(2, 3))
        pad = np.pad(unr, 2); voisin = sw(pad, (5, 5)).any(axis=(2, 3)) | (mn < np.where(ref > 0, cur / np.maximum(ref, 1), 0) - 0.05)
        loin = int((part & ~voisin).sum()); out['partiels_loin'] = max(out['partiels_loin'], loin); out['interm_max'] = max(out['interm_max'], int(part.sum()))
        if loin and '--loin' in sys.argv:
            yy_, xx_ = np.nonzero(part & ~voisin); print('   pas %d loin : %s' % (i, [(int(x), int(y), int(cur[y, x]), int(ref[y, x])) for y, x in zip(yy_[:8], xx_[:8])]))
        k, tg, marge = tangente(T, bornes, sf)
        if tg is None or marge < 2.5 * T[k]['R']: continue
        padu = np.pad(unr & core, 1); vu = sw(padu, (3, 3)).any(axis=(2, 3))
        bord = rev & vu & (np.abs(S - sf) <= tol) & (K == k) & (autre > T[k]['R'] * 2.5)
        ys, xs = np.nonzero(bord)
        if len(xs) < max(6, 0.8 * T[k]['R']): continue
        k, tg, marge = tangente(T, bornes, float(np.median(S[bord])))
        if tg is None or marge < 2.5 * T[k]['R']: continue
        pts = np.stack([xs, ys], 1).astype(float); pts -= pts.mean(0); _, _, vt = np.linalg.svd(pts, full_matrices=False); d = vt[0]
        ang = math.degrees(math.acos(min(1, abs(d[0] * tg[0] + d[1] * tg[1]))))   # angle front / tangente : 90° = perpendiculaire
        out['angles'].append(round(90 - ang, 1))
        if abs(90 - ang) > 10 and '--img' in sys.argv:
            im = np.zeros((h, w, 3), np.uint8); im[..., 0] = (ref).astype(np.uint8) // 3; im[..., 1] = cur.astype(np.uint8); im[bord] = (255, 0, 0)
            for t in T:
                for q in t['pts']:
                    x_, y_ = int(q[0]), int(q[1])
                    if 0 <= x_ < w and 0 <= y_ < h: im[y_, x_] = (0, 120, 255)
            Image.fromarray(im).save('scratchpad/v153/angle-%s-%d.png' % (info.get('nom', 'x'), i)); print('   pas %d : sf %.0f trait %d marge %.0f R %.1f angle %.1f' % (i, sf, k, marge, T[k]['R'], 90 - ang))
    return out
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.wait_for_timeout(300)
    L_ = next((a.split('=')[1] for a in sys.argv if a.startswith('--lissage=')), None)
    if L_: pg.evaluate('n=>{ TraceLettres.lissage=n; }', int(L_))
    if '--proche' in sys.argv: pg.evaluate('()=>{ TraceLettres.segProche=1; }')
    for pol, gr, car in CAS:
        info = pg.evaluate(PREP, [pol, gr, car]); info['nom'] = pol[0] + car
        o = analyse(info, lambda f: pg.evaluate(LIT, f))
        A = o['angles']
        print('%-9s %s  écart au texte %d  var %s  pas %d  hors-glyphe %d  trous-derrière %d  avance-devant %d  partiels loin du bord %d (max partiels %d)  angle au perpendiculaire : n %d, max %.1f°, méd %.1f°' % (
            pol, car, o['ecart_texte'], info['v'], o['pas'], o['hors'], o['trous'], o['avance'], o['partiels_loin'], o['interm_max'], len(A), max(map(abs, A)) if A else -1, float(np.median(np.abs(A))) if A else -1))
    b.close()
    if FILM:
        hh, ww = FILM[0].shape[:2]; n = len(FILM); cols = 10; rows = (n + cols - 1) // cols; P = np.zeros((rows * hh, cols * ww, 3), np.uint8)
        for i, f in enumerate(FILM): P[(i // cols) * hh:(i // cols + 1) * hh, (i % cols) * ww:(i % cols + 1) * ww] = f
        Image.fromarray(P).resize((cols * ww // 2, rows * hh // 2)).save('scratchpad/v153/film.png')
