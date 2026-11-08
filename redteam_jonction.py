# -*- coding: utf-8 -*-
"""⚑ v189 (Tom, Q612 tranchée, C-259) — LE TRAIT DE JONCTION SOUS L'EN-TÊTE.
Banc WebKit (banc_tom), échelles 1 et 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79), fiches Cercle, Promi, Chiche ; la fiche défilée pas à pas de 2 pt
jusqu'à 140 pt puis remontée à 0, chaque pas lu après l'image :
  A · Cercle : avant l'accrochage, rien n'est dessiné (la vraie vague défile) ; après, l'amplitude = (1 − (s − s0)/40) bornée, continue et monotone, la même à l'aller et
      au retour ; Promi, Chiche : l'opacité = s/40 bornée, de même ;
  B · le trait sur la jonction : sa tranche haute (lue sur l'image de la couche) à 112 pt ± 0,5 dès qu'il est plat (Cercle) ou paru (Promi, Chiche) ; au Cercle, accroché,
      le haut de son trait (au sommet de la vague) aussi ;
  C · aucun saut à l'accrochage : l'écran juste avant et juste après (± 1 pt de défilement) diffère de moins de 2 % des pixels dans la bande 100 → 260 pt ;
  D · au repos (défilement 0) : aucune couche, rien de dessiné ;
  E · même couleur et même épaisseur que la vague du Cercle (#0A0415, 10 × _TRAIT_K) ; la couche ne prend pas le doigt."""
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
  const g=c.getContext('2d'), E=c.width/390, a=(c.getAttribute('data-jonction')||'').split(',');
  /* la tranche haute du trait : la première rangée opaque de la couleur du trait, colonnes 60, 195, 330 */
  const haut=x=>{ const col=g.getImageData(Math.round(x*E),0,1,c.height).data; for(let y=0;y<c.height;y++){ const i=y*4; if(col[i+3]>128 && Math.abs(col[i]-10)<24 && Math.abs(col[i+1]-4)<24 && Math.abs(col[i+2]-21)<24) return y/E; } return null; };
  const cs=getComputedStyle(c);
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
    for nat in ('cercle', 'promi', 'chiche'):
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
    juge('Z · aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
