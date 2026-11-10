# -*- coding: utf-8 -*-
"""⚑ v192 (C-259 suite ; original : sauvegardes/redteam_jonction-avant-v192.py) : la couche est une BOÎTE COLLANTE (#v192Colle, canevas #v189Jonction) — la tranche haute se lit
 sur son canevas et se replace à la position de la boîte à l'écran ; E lit la boîte. F inchangé (le trait collé du Cercle suit le modèle échantillonné, comme en v190).
⚑ v189 (Tom, Q612 tranchée, C-259) — LE TRAIT DE JONCTION SOUS L'EN-TÊTE.
Banc WebKit (banc_tom), échelles 1 et 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79), fiches Cercle, Promi, Chiche ; la fiche défilée pas à pas de 2 pt
jusqu'à 140 pt puis remontée à 0, chaque pas lu après l'image :
  A · Cercle : avant l'accrochage, rien n'est dessiné (la vraie vague défile) ; après, l'amplitude = (1 − (s − s0)/40) bornée, continue et monotone, la même à l'aller et
      au retour ; Promi, Chiche : l'opacité = s/40 bornée, de même ;
  B · le trait sur la jonction : sa tranche haute (lue sur l'image de la couche) à 112 pt ± 0,5 dès qu'il est plat (Cercle) ou paru (Promi, Chiche) ; au Cercle, accroché,
      le haut de son trait (au sommet de la vague) aussi ;
  C · aucun saut à l'accrochage : l'écran juste avant et juste après (± 1 pt de défilement) diffère de moins de 2 % des pixels dans la bande 100 → 260 pt ;
  D · au repos (défilement 0) : aucune couche, rien de dessiné ;
  E · même couleur et même épaisseur que la vague du Cercle (#0A0415, 10 × _TRAIT_K) ; la couche ne prend pas le doigt.
⚑ v190 (Tom, C-259 ; original : sauvegardes/redteam_jonction-avant-v190.py) :
  F · Cercle — AUCUN TRAIT PARASITE : défilé de 1 pt en 1 pt, aller et retour, de l'accrochage − 6 à + 46 pt ; à chaque image, colonne par colonne, entre le bas de la bande
      (112 − 1,5) et le haut de la vague collée (son enveloppe, − 1,2 pt), sous les dalles du champ (l'enveloppe de la vraie vague) : rien que le champ (± 6) ; sous la vague
      collée (+ 1,2 → + 12 pt) : rien que le corps (± 6). Rouge sur v189 (le trait gris à 112, sur les bosses).
  G · Promi, Chiche — ⚑ v191 : AVANT L'ACCROCHAGE, la zone de la jonction (112 → 212 pt) identique à v190 AU PIXEL à chaque pas, aller et retour (banc_jonction, matière
      exceptée) ; l'accrochage lui-même est jugé par redteam_jonction_fiche. (v190 : identique à v188 à tous les pas, la couche absente.)"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True); return ok
LIT = r"""()=>{ const c=document.getElementById('v189Jonction'); const d=document.getElementById('detailPoster');
  if(!c || getComputedStyle(c).display==='none') return {s:d.scrollTop, v:null};
  const g=c.getContext('2d'), E=c.width/390, a=(c.getAttribute('data-jonction')||'').split(','), Bx=document.getElementById('v192Colle')||c, Dv=document.getElementById('device').getBoundingClientRect(), O=(Bx.getBoundingClientRect().top-Dv.top)/(Dv.width/390);   /* ⚑ v192 : le canevas est dans la boîte collante (#v192Colle) : sa rangée 0 est à O pt à l'écran */
  /* la tranche haute du trait : la première rangée opaque de la couleur du trait, colonnes 60, 195, 330 */
  const haut=x=>{ const col=g.getImageData(Math.round(x*E),0,1,c.height).data; for(let y=0;y<c.height;y++){ const i=y*4; if(col[i+3]>128 && Math.abs(col[i]-10)<24 && Math.abs(col[i+1]-4)<24 && Math.abs(col[i+2]-21)<24) return O+y/E; } return null; };
  const cs=getComputedStyle(Bx);
  return {s:d.scrollTop, v:a[1]!=null?+a[1]:null, kind:a[0], h:[haut(60),haut(195),haut(330)], pe:cs.pointerEvents, z:cs.zIndex}; }"""
def pas(pg, s):
    pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s)
    pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    return pg.evaluate(LIT)
def zone(pg):
    im = Image.open(io.BytesIO(pg.screenshot())).convert('L'); d = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390,devicePixelRatio]; }")
    q = d[3]; return im.crop((int(d[0] * q), int((d[1] + 100 * d[2]) * q), int((d[0] + 390 * d[2]) * q), int((d[1] + 260 * d[2]) * q)))
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 9000); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); if(v){ v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; } }")
    for nat in ('cercle',):
        T = '[%s]' % nat
        if nat == 'cercle': pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }")
        else: pg.evaluate("t=>{ closeAll(); var p=promises.find(x=>x.title===t); p.comments=(p.comments||[]).concat(Array.from({length:6},(_,i)=>({t:'mot '+i, by:'Rachel', d:'2026-11-0'+(i+1)+'T10:00:00Z', vu:true}))); openDetail(p.id); }", 'faire les crêpes' if nat == 'promi' else 'réparer le vélo')
        pg.wait_for_timeout(3200)
        r0 = pas(pg, 0)
        juge(T + ' D · au repos : aucune couche dessinée', r0['v'] is None, r0)
        pas(pg, 1); J = pg.evaluate("()=>window._v189Jonction ? window._v189Jonction() : null") or {}; FF = J.get('F') or {'s0': 9e9}
        smax = min(140, pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }"))
        aller = [pas(pg, s) for s in range(0, int(smax) + 1, 2)]; retour = [pas(pg, s) for s in range(int(smax), -1, -2)]
        def attendu(s):
            if nat == 'cercle':
                if s < FF['s0']: return None
                return max(0.0, 1 - min(1, (s - FF['s0']) / 40))   # amplitude restante
            return min(1.0, s / 40) if s > 0.25 else None
        def lu(r):
            if r['v'] is None: return None
            return (1 - r['v']) if nat == 'cercle' else r['v']
        ec = [(r['s'], lu(r), attendu(r['s'])) for r in aller + retour if (lu(r) is None) != (attendu(r['s']) is None) or (lu(r) is not None and abs(lu(r) - attendu(r['s'])) > 0.012)]
        seq = [lu(r) for r in aller if lu(r) is not None]
        mono = all(seq[i + 1] <= seq[i] + 1e-6 for i in range(len(seq) - 1)) if nat == 'cercle' else all(seq[i + 1] >= seq[i] - 1e-6 for i in range(len(seq) - 1))
        juge(T + ' A · %s en fonction du défilement : la loi, continue et monotone, aller et retour (%d pas)' % ('amplitude' if nat == 'cercle' else 'opacité', len(aller) + len(retour)), not ec and mono and len(seq) > 5, ec[:4])
        hauts = [h for r in aller + retour if r['v'] is not None and ((nat == 'cercle' and r['v'] >= 0.999) or (nat != 'cercle' and r['v'] >= 0.999)) for h in r['h'] if h is not None]
        juge(T + ' B · trait plat : sa tranche haute à 112 pt ± 0,5 (lue sur l\'image)', hauts and all(abs(h - 112) <= 0.5 for h in hauts), (len(hauts), min(hauts or [0]), max(hauts or [0])))
        if nat == 'cercle':
            som = [min(h for h in r['h'] if h is not None) for r in aller if r['v'] is not None and any(h is not None for h in r['h'])]
            juge(T + ' B · accrochée : le haut du trait toujours sur la jonction (≥ 112 − 0,5 ; le sommet de la vague à 112)', som and all(h >= 111.5 for h in som), (min(som or [0]), len(som)))
            # le haut du trait, lu sur l'IMAGE de l'écran (colonnes 60, 195, 330), 1 pt avant et 1 pt après l'accrochage : la vraie vague, puis la vague collée
            def bords(s):
                pas(pg, s); im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); d = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390,devicePixelRatio]; }")
                q = d[3]; out = []
                for x in (60, 195, 330):
                    X = int((d[0] + x * d[2]) * q); y0 = None
                    for Y in range(int((d[1] + 100 * d[2]) * q), int((d[1] + 300 * d[2]) * q)):
                        r_, g_, b_ = im.getpixel((X, Y))
                        if abs(r_ - 10) < 30 and abs(g_ - 4) < 30 and abs(b_ - 21) < 30: y0 = ((Y / q) - d[1]) / d[2]; break
                    out.append(y0)
                return out
            s0 = FF['s0']; av = bords(s0 - 1); ap = bords(s0 + 1)
            sauts = [round(b2 - a2, 2) for a2, b2 in zip(av, ap) if a2 is not None and b2 is not None]
            # sur 2 pt de défilement, un point de la vague monte de 1 pt avant l'accrochage, puis de 1 + (son écart au sommet)/40 pt après (elle s'aplatit) : au plus
            # 2 + (max − min)/40, plus 0,5 pt de lecture ; un saut se compterait en dizaines de points
            lim = 2 + (FF['max'] - FF['min']) / 40 + 0.5
            juge(T + ' C · aucun saut à l\'accrochage (s0 = %.1f pt) : le haut du trait, lu sur l\'écran, bouge au plus de %.2f pt pour 2 pt de défilement' % (s0, lim), sauts and len(sauts) == 3 and all(abs(x) <= lim for x in sauts), (sauts, av, ap))
        rr = pas(pg, 80)
        juge(T + ' E · même couleur et même épaisseur (#0A0415, %.1f pt) ; la couche ne prend pas le doigt, sous l\'en-tête' % (FF.get('lw') or 0), rr['pe'] == 'none' and rr['z'] == '8' and abs((FF.get('lw') or 0) - 10 * pg.evaluate("()=>window._TRAIT_K")) < 0.01, (rr['pe'], rr['z']))
        pas(pg, 0)
    # F · les traits parasites (Cercle), image par image
    pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(3200); pas(pg, 60)
    # la forme de la vraie vague, calculée ICI depuis ce que son peintre déclare (`data-trait` : base, amp) et la courbe partagée (`_onde`) — pas lue dans la couche jugée
    JJ = pg.evaluate("()=>{ const t=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0], +t[1]), P=[]; for(let x=0;x<=390;x+=2) P.push(y(x)); return {P, lw:10*(window._TRAIT_K||1.3)}; }")
    P = JJ['P']; lw = JJ['lw']; r = lw / 2; mn = min(P); s0 = mn - r - 112
    ENr = [min(P[j] - (r * r - ((j - i) * 2) ** 2) ** .5 for j in range(max(0, i - 4), min(len(P), i + 5)) if abs((j - i) * 2) <= r) for i in range(len(P))]
    champ = None; corps = pg.evaluate("()=>getComputedStyle(document.getElementById('detailPoster')).backgroundColor")
    import re; corps = tuple(int(x) for x in re.findall(r'\d+', corps)[:3])
    seq = [s0 - 6 + i for i in range(0, 53)]; seq = seq + seq[::-1]; mauvais = []
    for s in seq:
        rr = pas(pg, s); im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); d = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390,devicePixelRatio]; }")
        q = d[3]; px = im.load(); t = (1 - rr['v']) if rr['v'] is not None else None
        if champ is None: champ = px[int((d[0] + 4 * d[2]) * q), int((d[1] + 108 * d[2]) * q)]
        Y = lambda yy: int((d[1] + yy * d[2]) * q)
        for i in range(2, len(P) - 2, 2):
            x = i * 2; X = int((d[0] + x * d[2]) * q)
            if t is None: continue   # avant l'accrochage : la vraie vague, rien de dessiné
            mine = [112 + r + (P[j] - mn) * t for j in range(max(0, i - 4), min(len(P), i + 5))]
            haut = min(mine[j - max(0, i - 4)] - (r * r - ((j - i) * 2) ** 2) ** .5 for j in range(max(0, i - 4), min(len(P), i + 5)) if abs((j - i) * 2) <= r)
            basm = max(mine[j - max(0, i - 4)] + (r * r - ((j - i) * 2) ** 2) ** .5 for j in range(max(0, i - 4), min(len(P), i + 5)) if abs((j - i) * 2) <= r)
            dal = ENr[i] - s - 2.5
            for yy in range(Y(max(110.5, dal)), Y(haut - 1.2)):
                c = px[X, yy]
                if sum(abs(c[k] - champ[k]) for k in range(3)) > 6: mauvais.append((round(s, 1), x, round((yy / q - d[1]) / d[2], 1), c)); break
            for yy in range(Y(basm + 1.2), Y(basm + 12)):
                c = px[X, yy]
                if sum(abs(c[k] - corps[k]) for k in range(3)) > 6: mauvais.append((round(s, 1), x, round((yy / q - d[1]) / d[2], 1), c, 'corps')); break
    juge('[cercle] F · aucun trait parasite : %d images, aller et retour, rien que le champ au-dessus de la vague collée et le corps dessous' % len(seq), not mauvais, (len(mauvais), mauvais[:4]))
    pas(pg, 0)
    juge('Z · aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    # G · Promi, Chiche : la zone de jonction identique à v188 au pixel, à chaque pas
    import banc_jonction as BJ
    vw, vh = pg.evaluate("()=>[innerWidth, innerHeight]")
    # ⚑ v191 (Tom, C-259 suite ; original : sauvegardes/redteam_jonction-avant-v191.py) : Promi et Chiche s'accrochent eux aussi (jugé par redteam_jonction_fiche) ;
    # G ne garde que ce qui précède l'accrochage : la zone de la jonction identique à v190 (= v188) au pixel, aller et retour, tant que le trait n'est pas accroché.
    for nat in ('promi', 'chiche'):
        R = []
        for f in (F, 'zz-v190.html'):
            cx, pp = BJ.ouvre(b, f, nat, vw, vh)
            if f == F:
                pp.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=1; }"); pp.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
                S0 = pp.evaluate("()=>{ const j=window._v189Jonction&&_v189Jonction(); return j&&j.F?j.F.s0:null; }") or 0
            PAS = [s for s in BJ.PAS if s < S0 - 0.5]; R.append(BJ.images(pp, PAS)); cx.close()
        e = [(x[0], BJ.ecart(x, y)) for x, y in zip(R[0], R[1])]
        juge('[%s] G · avant l\'accrochage (s0 = %.1f) : la zone de la jonction identique à v190 au pixel, %d pas aller et retour' % (nat, S0, len(e)), S0 > 60 and len(e) > 10 and not [z for z in e if z[1]], [z for z in e if z[1]][:4])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
