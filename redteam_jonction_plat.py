# -*- coding: utf-8 -*-
"""⚑ v195 (Tom, 11 nov. 2026, C-259, Q617 tranchée : « TRAIT PLAT COLLÉ ») — LE TRAIT DE JONCTION PAR LA SEULE GÉOMÉTRIE, JUGÉ SUR L'ÉCRAN.
Remplace, pour le contrat de la jonction, les juges de l'aplatissement (redteam_jonction A–G, redteam_jonction_fiche A–C, qui jugeaient l'onde (base', k·amp) de v190–v194).
Banc WebKit (banc_tom) ; échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) et la fenêtre de Tom (PYTHONPATH=scratchpad/v190/fenetretom
PROMI_ECHELLE=tom). Cercle, Promi, Chiche (`--natures=`). La fiche défilée de 0 à l'arrivée de la vague + 60 pt (1 pt par pas autour du contact, 2 ailleurs), puis remontée.
Chaque pas : l'écran (l'appareil, rangées 104 → 340 pt), lu après deux images.
  A · AU REPOS : la zone 104 → 340 pt identique à v190 servie à côté (`banc_jonction.ecart_bords`, Q616 : le lissage des bords excepté ; la matière des dalles exceptée).
  B0 · défilé au bout, le trait plat est à la jonction (son haut entre 112 et 112 + ½ épaisseur : le haut d'un point est plus bas que celui du trait plein).
  B · LE CONTRAT, colonne par colonne (tous les 8 pt) : tant que le haut de la vague (son haut au repos − le défilement) est sous celui du trait plat, le haut visible du trait
      est celui de la vague, à sa place — aucun trait plat au-dessus d'elle ; la vague passée sous la bande, c'est celui du trait plat ; au contact, entre la jonction et le
      bas de la vague (le trait plat se découvre sous la vague qui monte) ; ± 1 pixel de l'appareil + 0,5 pt. Le trait se reconnaît à
      SA couleur, relevée au repos dans la colonne (la couleur déclarée et l'orange du départ servent à le trouver ; le verdict vient des pixels).
  C · LE RETOUR : l'écran au même défilement est le même à l'aller et au retour (≤ 0,2 % des pixels à plus de 24 niveaux).
  D · GELÉ : le même aller-retour, `requestAnimationFrame`, `setTimeout`, `setInterval` et `queueMicrotask` coupés pendant tout le défilement — B tient sans script.
  E · aucune erreur de page.
Rouge sur v194 (B : en mode gelé l'image accrochée reste celle du repos — la chronologie n'est pas en cause au banc, mais le contrat de la vague qui monte jusqu'à la jonction,
oui : v194 aplatissait)."""
import sys, io, os; sys.path.insert(0, '.')
import numpy as np
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['cercle', 'promi', 'chiche'])
ECH = os.environ.get('PROMI_ECHELLE', '1'); J = 112
VUE = {'1': (390, 844), '0,79': (330, 714), 'tom': (390, 651)}.get(ECH, (390, 844)); Y0, Y1 = 104, 340
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:300]), flush=True); return ok
GELE = """()=>{ if(window.__gel) return; window.__gel={r:window.requestAnimationFrame, t:window.setTimeout, i:window.setInterval, q:window.queueMicrotask};
  window.requestAnimationFrame=function(){ return 0; }; window.setTimeout=function(){ return 0; }; window.setInterval=function(){ return 0; }; window.queueMicrotask=function(){}; }"""
DEGELE = """()=>{ var g=window.__gel; if(!g) return; window.requestAnimationFrame=g.r; window.setTimeout=g.t; window.setInterval=g.i; window.queueMicrotask=g.q; window.__gel=null; }"""
def lit(pg, d):
    k = d[4]; png = pg.screenshot(clip={'x': d[0], 'y': d[1] + Y0 * k, 'width': 390 * k, 'height': (Y1 - Y0) * k})
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def pose(pg, s, gele=False):
    pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s)
    if not gele: pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    else: pg.wait_for_timeout(40)
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in NATS:
        ctx, pg = BJ.ouvre(b, F, nat, *VUE)        # horloge et hasard figés (banc_jonction : la matière du Cercle ne bouge pas d'une image à l'autre)
        d = B.dev(pg); k = d[4]
        im0 = lit(pg, d); H, W, _ = im0.shape; ppt = H / (Y1 - Y0)          # pixels de l'image par point de l'appareil
        jn = pg.evaluate("()=>window._v189Jonction?_v189Jonction():null") or {}
        s0 = (jn.get('F') or {}).get('s0'); smax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }")
        if s0 is None: juge('[%s · %s] la jonction est posée' % (ECH, nat), False, jn); ctx.close(); continue
        hi = min(smax, s0 + 60)
        q = lambda x: round(x * k * 3) / (k * 3)     # par pixels entiers de l'écran : la même trame qu'au repos (un défilement fractionnaire relisse le trait)
        S = sorted(set(q(x) for x in [round(x, 1) for x in list(np.arange(0, max(0, s0 - 6), 2)) + list(np.arange(max(0, s0 - 6), min(hi, s0 + 45), 1)) + list(np.arange(min(hi, s0 + 45), hi, 2)) + [hi]]))
        # A · au repos, contre v190 servie à côté
        if os.path.exists('zz-v190.html'):
            ctx2, pg2 = BJ.ouvre(b, 'zz-v190.html', nat, *VUE); r0 = lit(pg2, B.dev(pg2)); ctx2.close()
            a = (None, Image.fromarray(im0.astype(np.uint8)), Image.new('L', (W, H), 0)); rr = (None, Image.fromarray(r0.astype(np.uint8)), Image.new('L', (W, H), 0))
            ya = pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0], +t[1]), X=[]; for(let x=0;x<=390;x++) X.push(y(x)); return X; }")
            ch = im0[int((J + 3 - Y0) * ppt), 4].astype(int); mat = np.zeros((H, W), bool)   # la MATIÈRE : au-dessus de la vague, ce qui n'est pas le champ (les dalles) — §8 bis
            for x in range(W):
                yt = int((ya[min(390, int(x * 390 / W))] - 14 - Y0) * ppt)
                if yt > 0: mat[:yt, x] = (np.abs(im0[:yt, x] - ch).sum(axis=1) > 40) | (np.abs(r0[:yt, x] - ch).sum(axis=1) > 40)
            for _ in range(2):   # élargie de 2 pixels (le lissage autour d'une dalle)
                m2 = mat.copy(); m2[1:] |= mat[:-1]; m2[:-1] |= mat[1:]; m2[:, 1:] |= mat[:, :-1]; m2[:, :-1] |= mat[:, 1:]; mat = m2
            a = (None, Image.fromarray(im0.astype(np.uint8)), Image.fromarray((mat * 255).astype(np.uint8))); rr = (None, Image.fromarray(r0.astype(np.uint8)), Image.fromarray((mat * 255).astype(np.uint8)))
            n = BJ.ecart_bords(a, rr) if im0.shape == r0.shape else -1
            juge('[%s · %s] A · au repos, la zone 104 → 340 pt identique à v190 (bords exceptés, Q616 ; la matière des dalles exceptée, §8 bis)' % (ECH, nat), n == 0, '%s pixels' % n)
        # les colonnes : le haut du trait au repos et sa couleur
        cols = []
        DT = pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0], +t[1]), X=[]; for(let x=6;x<386;x+=8) X.push(y(x)); const h=(t[2]||'#0A0415').replace('#',''); return {y:X, col:[parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)], lw:10*(window._TRAIT_K||1.3)}; }")
        TC = [np.array(DT['col']), np.array([251, 76, 13])]   # la couleur déclarée du trait (un pointeur pour trouver) et l'orange du départ ; le verdict vient des pixels
        for i, xpt in enumerate(range(6, 386, 8)):
            x = int(xpt * W / 390); col = im0[:, x, :]; ya = DT['y'][i]
            for y in range(int((J + 2 - Y0) * ppt), H - 3):
                yy = Y0 + y / ppt
                if yy < ya - DT['lw'] * 2 - 6: continue
                if yy > ya + DT['lw']: break
                if any(np.abs(col[y] - tc).sum() < 90 and np.abs(col[y + 2] - tc).sum() < 90 for tc in TC):
                    cols.append((xpt, x, yy, col[y + 2].copy(), None)); break
        def hauts(im):
            out = []
            for xpt, x, t0, c, ch in cols:
                col = im[:, x, :]; t = None
                for y in range(int((J - 1.5 - Y0) * ppt), H):
                    if np.abs(col[y] - c).sum() < 60: t = Y0 + y / ppt; break
                out.append(t)
            return out
        h0 = hauts(im0); cols = [(xpt, x, t, c, ch) for (xpt, x, t0, c, ch), t in zip(cols, h0) if t is not None]   # le haut au repos, lu par la même mesure que pendant le défilement
        tol = 1.0 / (k * 3) + 0.5 + 1.0 / ppt
        def verdict(s, hs, KO, tag):
            for (xpt, x, t0, c, ch), t, ft in zip(cols, hs, FT):
                w = t0 - s
                if w > Y1 - 4: continue
                if w > ft + tol: ok = t is not None and abs(t - w) <= tol; e = w                           # avant le contact : la vague, à sa place (aucun trait plat au-dessus d'elle)
                elif w + DT['lw'] < J and ft <= J + DT['lw']: ok = t is not None and abs(t - ft) <= tol; e = ft   # la vague passée sous la bande : le trait plat de cette colonne
                elif ft <= J + DT['lw']: e = (J, max(ft, w + DT['lw'])); ok = t is not None and J - tol <= t <= max(ft, w + DT['lw']) + tol   # au contact : entre la jonction et le bas de la vague (le trait plat se découvre sous elle)
                else: continue                                                                                    # une colonne sans trait plat (entre deux points), après le contact
                if not ok: KO.append((tag, s, xpt, round(t0, 1), None if t is None else round(t, 2), e))
        for mode in ['vivant', 'gele']:
            if mode == 'gele': pose(pg, 0); pg.evaluate(GELE)
            if mode == 'vivant':
                pose(pg, hi); FT = [t if (t is not None and t <= J + DT['lw']) else 1e9 for t in hauts(lit(pg, d))]   # le haut du trait plat, colonne par colonne, défilé au bout
                FTj = [t for t in FT if t < 1e9]
                juge('[%s · %s] B0 · défilé au bout, le trait plat est à la jonction : son haut entre 112 et 112 + ½ épaisseur (%d colonnes)' % (ECH, nat, len(FTj)),
                     len(FTj) > 10 and all(J - tol <= t <= J + DT['lw'] / 2 + tol for t in FTj), [round(t, 2) for t in FTj[:12]])
            KO = []; aller = {}
            for s in S:
                pose(pg, s, mode == 'gele'); im = lit(pg, d); aller[s] = im; verdict(s, hauts(im), KO, 'a')
            DIF = []
            for s in reversed(S):
                pose(pg, s, mode == 'gele'); im = lit(pg, d)
                if s in aller:
                    n = int((np.abs(im - aller[s]).max(axis=2) > 24).sum())
                    if n > 0.002 * W * H: DIF.append((s, n))
                    verdict(s, hauts(im), KO, 'r')
            if mode == 'gele': pg.evaluate(DEGELE)
            juge('[%s · %s · %s] B · colonne par colonne (%d colonnes, %d pas aller et retour) : la vague à sa place jusqu\'au contact, puis le trait plat ; ± %.2f pt'
                 % (ECH, nat, mode, len(cols), len(S), tol), not KO and len(cols) > 20, (len(KO), KO[:5]))
            juge('[%s · %s · %s] C · le retour : au même défilement, le même écran qu\'à l\'aller' % (ECH, nat, mode), not DIF, DIF[:5])
        juge('[%s · %s] E · aucune erreur de page' % (ECH, nat), not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
