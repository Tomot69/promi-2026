# -*- coding: utf-8 -*-
"""⚑ v199 (Tom, §2, C-267) — LE TRAIT REVENU EN HAUT EST EXACTEMENT À SA PLACE D'OUVERTURE. « On défile vers le bas puis vers le haut, et le trait reste
tronqué parce qu'il ne redescend pas tout à fait à sa place de repos. » Piste de Tom : la marge de 30 pt (14 avant) au-dessus de la courbe a déplacé le haut de la
boîte ; au-dessus du seuil d'accrochage (112 pt), elle resterait accrochée.
Banc WebKit (banc_jonction : horloge et hasard figés), Cercle, Promi, Chiche ; échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79), fenêtre
de Tom (PROMI_ECHELLE=tom) ; `--tom` : l'état exporté de Tom (Promi « gghh », Chiche « Thyh »). À l'ouverture : la place de chaque calque de la jonction (la vague
`#v192Colle`, le trait plat `#v195Plat`, le cache `#v195Cache`, la bande `#v187Bande`) et les pixels de la bande du trait (± 30 pt autour de l'onde). Puis, après 1,
3 et 10 allers-retours LENTS (pas de 4 pt, une image chacun) et LANCÉS (le défilement doux natif, `scrollTo smooth`, puis par sauts : WebKit mobile n'a pas de molette), revenu en haut :
  A · le haut de la boîte de la vague n'est jamais au-dessus de la jonction (112 pt) ; B · chaque calque à sa place d'ouverture (écart 0 pt, au 1/100) ;
  C · les pixels du trait identiques à l'ouverture (aucun pixel écarté de plus de 24 niveaux) ; D · aucune erreur de page."""
import sys, io, os; sys.path.insert(0, '.')
import numpy as np
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
NATS0 = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['cercle', 'promi', 'chiche'])
TOM = '--tom' in sys.argv
NATS = [n for n in NATS0 if not (TOM and n == 'cercle')]
ECH = 'tom-etat' if TOM else os.environ.get('PROMI_ECHELLE', '1')
VUE = {'1': (390, 844), '0,79': (330, 714), 'tom': (390, 651)}.get(ECH, (390, 844))
TITRES_TOM = {'promi': 'gghh', 'chiche': 'Thyh'}
def ouvre_j(b, f, nat):
    if not TOM: return BJ.ouvre(b, f, nat, *VUE)
    ctx, _ = B.contexte_tom(b); ctx.add_init_script(BJ.AMORCE); pg = B.ouvre(ctx, f, 6000)
    # ses paroles n'ont pas de mot : la fiche ne défilerait pas ; on y pose les trois mots du banc de la jonction (BJ.MOTS), rien d'autre de son état ne change
    pg.evaluate("a=>{ closeAll(); const p=promises.find(x=>x.title===a[0]); p.comments=a[1].map((x,i)=>({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); openDetail(p.id); }", [TITRES_TOM[nat], BJ.MOTS])
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(600); return ctx, pg
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True); return ok
CALQUES = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/(document.getElementById('device').offsetWidth||390), o={};
  ['v192Colle','v195Plat','v195Cache','v187Bande'].forEach(id=>{ const e=document.getElementById(id); if(!e){ o[id]=null; return; } const r=e.getBoundingClientRect(); o[id]=[Math.round((r.left-D.left)/k*100)/100, Math.round((r.top-D.top)/k*100)/100, Math.round(r.width/k*100)/100, Math.round(r.height/k*100)/100]; });
  const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), y=_onde.onde(+t[0],+t[1]); let mn=1e9, mx=-1e9; for(let x=0;x<=390;x+=2){ mn=Math.min(mn,y(x)); mx=Math.max(mx,y(x)); }
  o.onde=[mn,mx]; o.st=document.getElementById('detailPoster').scrollTop; return o; }"""
def lit(pg, y0, y1):
    d = B.dev(pg); k = d[4]
    png = pg.screenshot(clip={'x': d[0], 'y': d[1] + y0 * k, 'width': 390 * k, 'height': (y1 - y0) * k})
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def repos(pg):
    for _ in range(30): pg.evaluate("()=>{ window.__horloge && window.__horloge(50); }"); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(r))")
    pg.wait_for_timeout(300)
with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_trait_retour — %s, échelle %s, charge %.1f' % (F, ECH, B.charge()))
    for nat in NATS:
        T = '[%s · %s]' % (ECH, nat)
        ctx, pg = ouvre_j(b, F, nat); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
        repos(pg); O = pg.evaluate(CALQUES); y0 = max(0, int(O['onde'][0]) - 30); y1 = int(O['onde'][1]) + 30; im0 = lit(pg, y0, y1)
        juge(T + ' A · à l\'ouverture, le haut de la boîte de la vague est sous la jonction (≥ 112 pt)', O['v192Colle'] and O['v192Colle'][1] >= 112, 'boîte %s · onde %s' % (O['v192Colle'], [round(v, 1) for v in O['onde']]))
        smax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }"); hi = smax
        if hi < 40: juge(T + ' la fiche défile (assez de contenu)', False, 'défilement possible %.1f pt' % hi); ctx.close(); continue
        n_fait = 0
        for mode in ('lents', 'lancés'):
            n_fait = 0
            for n in (1, 3, 10):
                while n_fait < n:
                    if mode == 'lents':
                        for s in list(np.arange(0, hi, 4)) + [hi] + list(np.arange(hi, -1, -4)) + [0]:
                            pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", float(s)); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(r))")
                    else:   # lancé : le défilement doux NATIF du moteur (WebKit mobile n'a pas de molette), à grands pas, aller et retour
                        pg.evaluate("h=>{ document.getElementById('detailPoster').scrollTo({top:h, behavior:'smooth'}); }", float(hi)); pg.wait_for_timeout(700)
                        pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTo({top:0, behavior:'smooth'}); }"); pg.wait_for_timeout(700)
                        for s in [hi, hi * 0.5, 0]: pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", float(s))
                    n_fait += 1
                pg.wait_for_timeout(400); repos(pg); R = pg.evaluate(CALQUES); im = lit(pg, y0, y1)
                ec = {k: (O[k], R[k]) for k in ('v192Colle', 'v195Plat', 'v195Cache', 'v187Bande') if O[k] != R[k]}
                juge(T + ' B · après %d allers-retours %s, revenu en haut : chaque calque à sa place d\'ouverture (0 pt)' % (n, mode), R['st'] == 0 and not ec, 'défilé %s · %s' % (R['st'], ec or 'identiques'))
                dif = int((np.abs(im - im0).max(axis=2) > 24).sum()) if im.shape == im0.shape else -1
                juge(T + ' C · après %d allers-retours %s : les pixels du trait = l\'ouverture' % (n, mode), dif == 0, '%d pixels écartés' % dif)
        juge(T + ' D · aucune erreur de page', not err, err[:2]); ctx.close()
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
