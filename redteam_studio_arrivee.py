#!/usr/bin/env python3
"""redteam_studio_arrivee.py — ⚑ v160c (Tom, C-175, B2 : « au Studio, Ramage saccade beaucoup ; les autres mondes sont bons : GELÉS »).

Mesuré : à l'arrivée sur Ramage, la silhouette de la jauge (la dalle 64 × 64 rendue par le moteur) est UN bloc de 237 à 308 ms — le premier rendu de
Ramage dans la séance — et il tombait 1,2 s après le dernier toucher, pendant l'arrivée. Corrigé hors du moteur : pour Ramage, la silhouette attend 3 s
sans aucun toucher : elle tombe sur un Studio immobile. Banc comme Tom (WebKit, 390 × 844 ×3, doigt,
Toile de 25 paroles, membre « Ma Parole ! ») :
  A · Ramage : dans les 2,5 s qui suivent le glissé qui y mène, aucun rendu de la silhouette, et aucune image au-delà de 120 ms ;
  B · Ramage : la silhouette arrive ensuite, au calme (dans les 5 s sans toucher) ;
  C · Pochade (gelé) : la silhouette est refaite comme avant, entre 1,2 et 2,5 s après le glissé.
Les durées d'image ne sont qu'indicatives hors du calme (charge ≥ 4) ; A juge le COMPTE des rendus. Preuve : `--fichier=zz-v160b.html` rougit (A).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
ESPION = """()=>{ window.__R=[]; const rd=window._rendDalle; window._rendDalle=function(id,w,h,o){ const t=performance.now(); const r=rd.apply(this,arguments); if(w===64&&h===64) window.__R.push([Math.round(t), Math.round(performance.now()-t)]); return r; };
  window.__D=[]; let av=performance.now(); (function f(t){ window.__D.push([Math.round(t), t-av]); av=t; requestAnimationFrame(f); })(performance.now()); }"""
def vers(pg, voulu):
    for _ in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m == voulu: return True
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1500)
    return False
with sync_playwright() as p:
    b = p.webkit.launch()
    for monde, avant in (('ramage', 'pixel'), ('encre', 'sillons')):
        ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3500)
        pg.evaluate(ESPION)
        ok = vers(pg, avant); pg.wait_for_timeout(3500)
        t0 = pg.evaluate("()=>performance.now()"); B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); t1 = pg.evaluate("()=>performance.now()")
        pg.wait_for_timeout(2500); m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        R = pg.evaluate("()=>window.__R"); D = pg.evaluate("()=>window.__D")
        arr = [r for r in R if r[0] >= t1 - 50 and r[0] <= t1 + 2500]; img = max([d[1] for d in D if t1 <= d[0] <= t1 + 2500] or [0])
        if monde == 'ramage':
            juge('A · Ramage : 2,5 s après le glissé, aucun rendu de la silhouette, aucune image > 120 ms (charge %.1f)' % B.charge(), m == 'ramage' and not arr and img <= 120,
                 'monde %s · rendus %s · plus longue image %.0f ms' % (m, arr, img))
            pg.wait_for_timeout(5000); R2 = pg.evaluate("()=>window.__R")
            juge('B · Ramage : la silhouette arrive ensuite, au calme', any(r[0] > t1 + 2500 for r in R2) or bool(pg.evaluate("()=>window._silhouettes&&window._silhouettes().some(k=>k.indexOf('ramage|')===0)")),
                 'rendus après : %s' % [r for r in R2 if r[0] > t1 + 2500])
        else:
            juge('C · Pochade (gelé) : la silhouette refaite comme avant, 1,2 à 2,5 s après le glissé', m == 'encre' and (any(1200 <= r[0] - t1 <= 2500 for r in arr) or bool(pg.evaluate("()=>window._silhouettes&&window._silhouettes().some(k=>k.indexOf('encre|')===0)"))),
                 'monde %s · rendus %s' % (m, [(r[0] - round(t1), r[1]) for r in arr]))
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('aucune erreur de page (%s)' % monde, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
