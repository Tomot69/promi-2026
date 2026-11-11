# -*- coding: utf-8 -*-
"""⚑ v197 (Tom, 11 nov. 2026, C-267) — LE TRAIT N'EST JAMAIS COUPÉ : « quand on fait défiler puis qu'on lâche, ou qu'on lâche un tracé en cours, le trait est coupé en
haut à droite de sa courbe : il manque 1 à 2 mm ».
Banc WebKit (banc_jonction : horloge et hasard figés), échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79), fenêtre de Tom
(PYTHONPATH=scratchpad/v190/fenetretom PROMI_ECHELLE=tom). Cercle, Promi, Chiche (`--natures=`).
Le trait de v190 au repos (servie à côté, zz-v190.html) : les pixels de l'écran, dans la bande ± 24 pt autour de l'axe de l'onde, proches d'une couleur du trait
(la couleur déclarée, l'orange du départ), érodés de 2 pixels (le lissage des bords est excepté, Q616). Chaque pixel de ce masque doit être du TRAIT sur l'écran jugé
(proche d'une couleur du trait, jamais du champ ni du corps) :
  A · au repos ;  B · après un aller-retour de défilement (jusqu'à l'accrochage + 80 pt, puis 0) ;  C · après un élan simulé (pas de 40 pt) et son retour ;
  D · Promi et Chiche : pendant le retour d'un tracé lâché à 15 % de la seconde moitié (six captures) et une fois revenu ;  E · aucune erreur de page.
`--sonde` coupe le haut de la vague (un clip-path sur la boîte de la jonction, 4 pt) : A rougit."""
import sys, io, os; sys.path.insert(0, '.')
import numpy as np
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
REF = 'zz-v190.html'
NATS0 = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['cercle', 'promi', 'chiche'])
NATS = [n for n in NATS0 if not ('--tom' in sys.argv and n == 'cercle')]
ECH = 'tom-etat' if '--tom' in sys.argv else os.environ.get('PROMI_ECHELLE', '1')
VUE = {'1': (390, 844), '0,79': (330, 714), 'tom': (390, 651)}.get(ECH, (390, 844))
SONDE = '--sonde' in sys.argv
TOM = '--tom' in sys.argv   # A2 : l'état exporté de Tom (sa fenêtre, son stockage) ; Promi « gghh », Chiche « Thyh » (son export n'a pas de Cercle)
TITRES_TOM = {'promi': 'gghh', 'chiche': 'Thyh'}
def ouvre_j(b, f, nat):
    if not TOM: return BJ.ouvre(b, f, nat, *VUE)
    ctx, _ = B.contexte_tom(b); ctx.add_init_script(BJ.AMORCE); pg = B.ouvre(ctx, f, 6000)
    pg.evaluate("t=>{ closeAll(); const p=promises.find(x=>x.title===t); openDetail(p.id); }", TITRES_TOM[nat])
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(600); return ctx, pg
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True); return ok
def hexrgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
INFO = """()=>{ const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0],+t[1]), A=[];
  for(let x=0;x<=390;x++) A.push(y(x)); return {axe:A, col:t[2]||'#0A0415'}; }"""
def lit(pg, y0, y1):
    d = B.dev(pg); k = d[4]
    png = pg.screenshot(clip={'x': d[0], 'y': d[1] + y0 * k, 'width': 390 * k, 'height': (y1 - y0) * k})
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def proche(im, cols, s):
    m = np.zeros(im.shape[:2], bool)
    for c in cols: m |= np.abs(im - np.array(c)).sum(axis=2) < s
    return m
def erode(m, n):
    for _ in range(n):
        e = m.copy(); e[1:] &= m[:-1]; e[:-1] &= m[1:]; e[:, 1:] &= m[:, :-1]; e[:, :-1] &= m[:, 1:]; m = e
    return m
GESTE = open('redteam_retour_trait.py', encoding='utf-8').read().split('GESTE = """', 1)[1].split('"""', 1)[0]
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in NATS:
        ctx2, pg2 = ouvre_j(b, REF, nat); inf = pg2.evaluate(INFO)
        axe = inf['axe']; y0 = max(100, int(min(axe)) - 30); y1 = min(VUE[1] / (B.dev(pg2)[4] or 1) + 0, int(max(axe)) + 30)
        y1 = int(max(axe)) + 30
        ref = lit(pg2, y0, y1); ctx2.close()
        H, W, _ = ref.shape; ppt = W / 390.0
        cols = [hexrgb(inf['col']), hexrgb('#FB4C0D')]
        bande = np.zeros((H, W), bool)
        for x in range(W):
            a = axe[min(390, int(x / ppt))]; r0 = int((a - 24 - y0) * ppt); r1 = int((a + 24 - y0) * ppt)
            bande[max(0, r0):max(0, r1), x] = True
        M = erode(proche(ref, cols, 90) & bande, 2)
        juge('[%s · %s] le trait de v190 est lu (%d pixels)' % (ECH, nat, M.sum()), M.sum() > 400)
        ctx, pg = ouvre_j(b, F, nat); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
        if SONDE: pg.evaluate("()=>{ const s=document.getElementById('v192Colle'); s.style.setProperty('clip-path','inset(%s 0 0 0)','important'); }" % '0px')
        if SONDE: pg.evaluate("a=>{ const S=document.getElementById('v192Colle'), c=document.getElementById('v195Cache'), J=_v189Jonction(); const h=Math.min(...a)-J.F.Ytop; S.style.setProperty('clip-path','inset('+(h-2)+'px 0 0 0)','important'); if(c) c.style.setProperty('display','none','important'); }", axe)
        def manque(nom, extra=''):
            im = lit(pg, y0, y1); ok = proche(im, cols, 140)
            miss = M & ~ok; n = int(miss.sum())
            if n:
                ys, xs = np.nonzero(miss); Image.fromarray(np.where(miss[..., None], [255, 0, 255], im).astype(np.uint8)).save('scratchpad/v197/manque-%s-%s-%s.png' % (ECH, nat, nom.split(' ')[0]))
                extra += ' · x %.0f→%.0f pt, y %.0f→%.0f pt' % (xs.min() / ppt, xs.max() / ppt, ys.min() / ppt + y0, ys.max() / ppt + y0)
            juge('[%s · %s] %s : aucun pixel du trait de v190 ne manque' % (ECH, nat, nom), n == 0, '%d manquants%s' % (n, extra))
        manque('A au repos')
        J = pg.evaluate("()=>_v189Jonction().F"); s0 = J['s0']; smax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }")
        hi = min(smax, s0 + 80)
        for s in list(np.arange(0, hi, 4)) + list(np.arange(hi, -1, -4)) + [0]:
            pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", float(s)); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(r))")
        pg.wait_for_timeout(500); manque('B après défilement')
        for s in list(np.arange(0, hi, 40)) + [hi] + list(np.arange(hi, -1, -40)) + [0]:
            pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", float(s))
        pg.wait_for_timeout(500); manque('C après un élan')
        if nat != 'cercle':
            pg.evaluate("()=>{ window.__PLEIN='()=>0'; }")
            xs = [195 + i * 3 for i in range(0, 12)]
            pg.evaluate(GESTE, ['#tenirCv', xs, False, ECH])
            pg.evaluate("a=>{ window.__fin=null; window.__gp=(%s)(a).then(o=>{ window.__fin=o; }); }" % GESTE, ['#tenirCv', xs, True, ECH])
            for i in range(6): manque('D pendant le retour (%d)' % i)
            pg.wait_for_timeout(900); manque('D revenu')
        juge('[%s · %s] E aucune erreur de page' % (ECH, nat), not err, err[:2]); ctx.close()
    b.close()
print('\n%d/%d' % (sum(res), len(res)))
