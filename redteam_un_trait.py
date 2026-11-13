# -*- coding: utf-8 -*-
"""⚑ v200 (Tom, §1, C-267) — UN SEUL TRAIT, JAMAIS COUPÉ, À CHAQUE IMAGE DU DÉFILEMENT. Capture de Tom (iPhone, après un défilement vers le bas puis vers le haut) :
au point de rencontre, le trait « rogné ET doublé ». Le juge ne compare plus des positions : il COMPTE LES TRAITS sur l'image rendue.
Banc WebKit à la densité 3, fenêtre de Tom 390 × 651 (l'appareil ≈ 0,7466) par défaut (`--vue=1` : 390 × 844 ; `--vue=0,79` : 330 × 714). Cercle, Promi, Chiche
(le banc de la jonction : horloge et hasard figés), et le Chiche de la capture (« Hhhh », lancé à soi, un mot).
Pour chaque image d'un défilement LENT (1 pt par image dans la zone de rencontre, 4 ailleurs ; bas puis haut) et d'un défilement LANCÉ (défilement doux natif, chaque
image prise pendant le mouvement), dans chaque colonne de pixels de l'écran, dans la fenêtre du trait (autour de l'axe de la vague à cet instant, et la bande du trait
plat, sous la jonction de 112 pt) :
  A · un seul trait : au CŒUR d'un point (ses colonnes du milieu) et partout sur le trait plein, une seule suite de pixels par colonne — l'encoche de v199 en fait deux ;
      au bord d'un point, la « taille de guêpe » de la rencontre (le 8 accepté par Tom en v197) est permise ;
  B · le trait n'est jamais coupé : sa hauteur ≥ 85 % de celle du repos dans cette colonne (un point qui passe sous la bande, rejoint par le point plat, compte entier).
  D · jamais doublé en épaisseur : sa hauteur ≤ 1,25 × celle du repos (ou du trait plat) + 1 pt.
  C · aucune erreur de page. `--sonde` : l'encoche de v199 posée exprès sous chaque point — il rougit."""
import sys, io, os, json; sys.path.insert(0, '.')
import numpy as np
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['chiche-tom', 'chiche', 'promi', 'cercle'])
VUEN = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--vue=')), 'tom')
VUE = {'tom': (390, 651), '1': (390, 844), '0,79': (330, 714)}[VUEN]
MODES = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--modes=')), ['lent', 'lance'])
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:300]), flush=True); return ok
def ouvre(b, nat):
    if nat != 'chiche-tom': return BJ.ouvre(b, F, nat, *VUE)
    ctx = B.contexte(b, vw=VUE[0], vh=VUE[1]); B.toile_pleine(ctx, 'cercle'); ctx.add_init_script(BJ.AMORCE); pg = B.ouvre(ctx, F, 6000)
    pg.evaluate("""()=>{ closeAll(); var p=promises.find(x=>x.title==='réparer le vélo'); p.title='Hhhh'; p.who='moi'; p.status='encours'; delete p.parts; delete p.tenu; p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche';
      p.comments=[{t:'Cucuc', by:'Tom', d:'2026-11-12T09:00:00Z', vu:true}]; openDetail(p.id); }""")
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(600); return ctx, pg
SONDE = """()=>{ /* le défaut de v199 : sous le trait plat, un aplat du champ descend jusqu'à l'axe + ½ épaisseur, au-dessous des points */
  const d=document.getElementById('detailPoster'), J=_v189Jonction(), f=J.F; if(!f||!f.P) return 0;
  let c=document.getElementById('sondeV199'); if(!c){ c=document.createElement('canvas'); c.id='sondeV199'; d.appendChild(c); }
  const E=3, w=390*E; c.width=w; const H=Math.ceil(f.max+f.lw/2+4); c.height=H*E; const g=c.getContext('2d'); g.fillStyle=getComputedStyle(document.getElementById('dpTrameCv')).getPropertyValue('--x')||'#FFB8D2';
  const px=document.getElementById('dpTrameCv').getContext('2d').getImageData(4*(document.getElementById('dpTrameCv').width/390), Math.max(0,(f.min-f.lw-6))*(document.getElementById('dpTrameCv').width/390),1,1).data; g.fillStyle='rgb('+px[0]+','+px[1]+','+px[2]+')';
  g.beginPath(); g.moveTo(0,0); for(let i=0;i<f.P.length;i++){ g.lineTo(i*2*E, (f.P[i]+f.lw/2-0.7)*E); } g.lineTo(w,0); g.closePath();
  g.save(); g.beginPath(); for(let i=0;i<f.P.length;i++){ g.rect(i*2*E-1, (f.P[i]-f.lw/2+1.6)*E, 2*E+2, (f.lw-2.3)*E); } g.restore(); g.fill();
  c.style.cssText='position:absolute!important;left:0!important;top:0!important;width:390px!important;height:'+H+'px!important;z-index:6!important;pointer-events:none!important;display:block!important;visibility:visible!important;opacity:1!important;margin:0!important;clip-path:polygon(0 0,100% 0,100% 100%,0 100%)';
  /* il ne cache que ce qui est SOUS la vague (le trait plat) : l'aplat ne touche pas la vague (z 7) */
  return 1; }"""
SONDE = """()=>{ const d=document.getElementById('detailPoster'), f=_v189Jonction().F; if(!f||!f.P) return 0;
  const cv=document.getElementById('dpTrameCv'), E0=cv.width/390, px=cv.getContext('2d').getImageData(Math.round(4*E0), Math.max(0,Math.round((f.min-f.lw-6)*E0)),1,1).data;
  let c=document.getElementById('sondeV199'); if(!c){ c=document.createElement('canvas'); c.id='sondeV199'; d.appendChild(c); }
  const E=3, H=Math.ceil(f.max+f.lw/2+2); c.width=390*E; c.height=H*E; const g=c.getContext('2d'); g.fillStyle='rgb('+px[0]+','+px[1]+','+px[2]+')';
  /* une bande de 2,5 pt du champ, juste sous le bas de chaque point (au-dessus de l'axe + ½ épaisseur) : l'encoche de la capture */
  for(let i=0;i<f.P.length;i++){ g.fillRect(i*2*E, (f.P[i]+f.lw/2-2.6)*E, 2*E+0.5, 2.4*E); }
  c.style.cssText='position:absolute!important;left:0!important;top:0!important;width:390px!important;height:'+H+'px!important;z-index:6!important;pointer-events:none!important;display:block!important;visibility:visible!important;opacity:1!important;margin:0!important;max-width:none!important';
  return 1; }"""
GEO = """()=>{ const d=document.getElementById('detailPoster'), D=document.getElementById('device'), R=D.getBoundingClientRect(), k=R.width/(D.offsetWidth||390), f=_v189Jonction().F;
  return {k:k, L:R.left, T:R.top, st:d.scrollTop, smax:d.scrollHeight-d.clientHeight, P:f&&f.P, lw:f&&f.lw, min:f&&f.min, max:f&&f.max}; }"""
def img(pg, G, y0, y1):
    k = G['k']; png = pg.screenshot(clip={'x': G['L'], 'y': G['T'] + y0 * k, 'width': 390 * k, 'height': (y1 - y0) * k})
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def masque(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = np.maximum(np.maximum(r, g), b)
    return (mx < 82) | ((r > 200) & (g < 140) & (b < 90))   # le trait : l'encre sombre de la nature, ou l'orange du départ
def runs(col):
    n = 0; L = 0; prev = False
    for v in col:
        if v and not prev: n += 1
        if v: L += 1
        prev = v
    return n, L
def fenetre(m, G, s, y0, plat=True):
    """le masque de la fenêtre du trait (toutes les colonnes de pixels)"""
    k = G['k'] * 3; H, W = m.shape; P = np.array(G['P']); lw = G['lw']; j0 = int(np.ceil((112 - y0) * k)) + 1
    x = np.arange(W) / k; ax = np.interp(x / 2, np.arange(len(P)), P) - s
    a0 = np.maximum(j0, ((ax - lw / 2 - 4 - y0) * k).astype(int)); a1 = np.minimum(H, ((ax + lw / 2 + 4 - y0) * k).astype(int))
    r = np.arange(H)[:, None]; w = (r >= a0[None, :]) & (r < a1[None, :])
    if plat: w |= (r >= j0) & (r < min(H, int((112 + lw + 0.5 - y0) * k)))
    w[:, :int(3 * k)] = False; w[:, int(387 * k):] = False   # le cadre de l'appareil, aux deux bords, n'est pas le trait
    return w
def composantes(mm):
    """le nombre de TRAITS : les formes d'un seul tenant (8-connexité), par suites de pixels dans chaque colonne reliées d'une colonne à la voisine"""
    H, W = mm.shape; par = []; prev = []
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for x in range(W):
        col = mm[:, x]; d = np.diff(np.concatenate(([0], col.view(np.int8), [0]))); st = np.where(d == 1)[0]; en = np.where(d == -1)[0]; cur = []
        for a, b in zip(st, en):
            i = len(par); par.append(i); cur.append((a, b, i))
            for (pa, pb, pi) in prev:
                if pa <= b and a <= pb: ra, rb = f(i), f(pi); par[ra] = rb
        prev = cur
    return len(set(f(i) for i in range(len(par))))
def compte(a, G, s, y0, plat=True):
    """par colonne d'écran (pas de 2 px) : (nombre de traits, hauteur en px) dans la fenêtre du trait, sous la jonction : autour de l'axe de la vague à cet
    instant (± ½ épaisseur + 4 pt) et, si `plat`, la bande du trait plat (112 → 112 + épaisseur)"""
    k = G['k'] * 3; m = masque(a); H, W = m.shape; P = G['P']; lw = G['lw']; out = []
    j0 = int(np.ceil((112 - y0) * k)) + 1
    for xp in range(6, W - 6, 2):
        x = xp / k; q = min(len(P) - 1, x / 2); i0 = int(q); i1 = min(len(P) - 1, i0 + 1); ax = P[i0] + (P[i1] - P[i0]) * (q - i0) - s
        w = np.zeros(H, bool); a0 = int((ax - lw / 2 - 4 - y0) * k); a1 = int((ax + lw / 2 + 4 - y0) * k); w[max(j0, a0):max(j0, min(H, a1))] = True
        if plat: w[j0:min(H, int((112 + lw + 0.5 - y0) * k))] = True
        out.append(runs(m[:, xp] & w))
    return out
def scrolle(pg, s):
    pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", float(s)); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    return pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
def references(pg, G, y0, y1):
    """au repos : chaque colonne (nombre, hauteur) ; défilé au bout, là où la vague est passée tout entière sous la bande : le trait plat seul"""
    a0 = img(pg, G, y0, y1); R0 = compte(a0, G, 0, y0, plat=False); k = G['k'] * 3; P = G['P']; lw = G['lw']
    s = scrolle(pg, G['smax']); RP = compte(img(pg, G, y0, y1), G, s, y0); scrolle(pg, 0); out = []
    for i, (r0, rp) in enumerate(zip(R0, RP)):
        x = (6 + 2 * i) / k; q = min(len(P) - 1, x / 2); i0 = int(q); i1 = min(len(P) - 1, i0 + 1); ax = P[i0] + (P[i1] - P[i0]) * (q - i0)
        sous = ax + lw / 2 + 5 - s < 112   # la vague, dans cette colonne, tout entière sous la bande : le trait plat seul
        out.append((max(r0[0], rp[0]) if sous else r0[0], min(r0[1], rp[1]) if sous else r0[1], r0[0], max(r0[1], rp[1]) if sous else r0[1], r0[1]))
    # le CŒUR d'un trait : une colonne où, au repos, le trait est presque aussi haut qu'à son plus haut alentour (le milieu d'un point, tout le trait plein)
    rv = int(4 * k / 2) + 1
    return [t + ((t[2] == 1 and t[4] >= 0.8 * max(out[j][4] for j in range(max(0, i - rv), min(len(out), i + rv + 1)))),) for i, t in enumerate(out)]
def elan(v0, smax, sens):
    """un défilement LANCÉ : la décroissance d'iOS (× 0,998 par ms), une image toutes les 16,7 ms ; les positions où l'élan passe"""
    s = 0.0 if sens > 0 else smax; v = v0; L = []
    while v > 0.02:
        s += sens * v * 16.7; v *= 0.998 ** 16.7
        if s <= 0 or s >= smax: L.append(max(0.0, min(smax, s))); break
        L.append(s)
    return L
def juge_nature(b, nat):
    T = '[%s · %s]' % (VUEN, nat); ctx, pg = ouvre(b, nat); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
    G = pg.evaluate(GEO)
    if not G['P']: juge(T + ' la jonction est posée', False, G); ctx.close(); return
    if '--sonde' in sys.argv: pg.evaluate(SONDE)
    y0 = 100; y1 = min(VUE[1] / G['k'] - 2, G['max'] + 30)
    REF = references(pg, G, y0, y1)
    s0 = G['min'] - G['lw'] / 2 - 112; s1 = G['max'] + G['lw'] / 2 - 112 + 4; smax = G['smax']
    juge(T + ' échelle de l\'appareil', True, 'k %.4f · s0 %.1f → %.1f · défilement possible %.1f' % (G['k'], s0, s1, smax))
    if smax < s0 + 6: juge(T + ' la fiche défile jusqu\'à la rencontre', False, smax); ctx.close(); return
    for mode in MODES:
        if mode == 'lent':
            zone = [s for s in np.arange(0, smax + 0.01, 1.0) if s0 - 3 <= s <= s1]; aller = sorted(set([round(x, 2) for x in list(np.arange(0, smax, 4)) + zone + [smax]]))
            seq = aller + aller[::-1]
        else:
            seq = []
            for v0 in (1.5, 3.0, 5.0): seq += elan(v0, smax, 1) + elan(v0, smax, -1)
        mauvais = {'A': [], 'B': [], 'D': []}; n = 0
        for s in seq:
            sr = scrolle(pg, s); a = img(pg, G, y0, y1); n += 1
            if abs(pg.evaluate("()=>document.getElementById('detailPoster').scrollTop") - sr) > 0.01: continue
            C = compte(a, G, sr, y0)
            for i, (nn, L) in enumerate(C):
                if REF[i][2] == 0: continue
                if REF[i][5] and nn > 1: mauvais['A'].append((round(sr, 1), round((6 + 2 * i) / (G['k'] * 3), 1), nn))
                vois = range(max(0, i - 1), min(len(REF), i + 2)); Lmin = min(REF[j][1] for j in vois); Lmax = max(REF[j][3] for j in vois)
                if L < 0.85 * Lmin: mauvais['B'].append((round(sr, 1), round((6 + 2 * i) / (G['k'] * 3), 1), L, Lmin))
                if L > 1.25 * Lmax + 3: mauvais['D'].append((round(sr, 1), round((6 + 2 * i) / (G['k'] * 3), 1), L, Lmax))
        for c, nom in (('A', 'un seul trait : au cœur d\'un point ou du trait plein, une seule suite de pixels (une encoche en fait deux)'), ('B', 'le trait jamais coupé (≥ 85 % de sa hauteur)'), ('D', 'jamais doublé en épaisseur (≤ 1,25 × sa hauteur)')):
            L = mauvais[c]; ss = sorted(set(x[0] for x in L))
            juge('%s %s · %s · %s' % (T, mode, c, nom), not L, '%d images · %d fautes sur %d positions %s · ex. %s' % (n, len(L), len(ss), ss[:8], L[:3]))
    juge(T + ' C · aucune erreur de page', not err, err[:2]); ctx.close()
if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.webkit.launch()
        print('redteam_un_trait — %s, vue %s %s, charge %.1f%s' % (F, VUEN, VUE, B.charge(), ' · SONDE' if '--sonde' in sys.argv else ''), flush=True)
        for nat in NATS: juge_nature(b, nat)
        b.close()
    print('  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
