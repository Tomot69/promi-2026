#!/usr/bin/env python3
"""redteam_ramage_jauge.py — ⚑ v164b (Tom, Q581, C-175) : RAMAGE AU STUDIO, LA SILHOUETTE DE LA JAUGE PRÉPARÉE À L'AVANCE.

« La silhouette de la jauge est préparée à l'avance, au repos, hors moteur. Aucun bloc au-delà de 50 ms dans les 5 s qui suivent l'arrivée. « Réglé »
seulement au calme. » Banc comme Tom (WebKit, 390 × 844 ×3, doigt), membre « Ma Parole ! » :
  D · un monde de la même famille de semis (Mascaret, 25 paroles) : l'accueil au repos 12 s prépare la silhouette de Ramage ; au Studio, dans les 5 s qui
      suivent le glissé qui arrive sur Ramage, aucun rendu de la silhouette, et aucune image au-delà de 50 ms (jugé au calme seulement) ;
  T · l'état exporté de Tom (A2) : même chose ;
  E · un ancien monde (Pochade, une autre famille : la Toile se ressème en arrivant sur Ramage, la silhouette ne peut pas être prête) : aucun rendu dans
      les 5 s, aucune image au-delà de 50 ms (au calme) ; la silhouette vient ensuite, au calme.
Une durée d'image n'est jugée que sous une charge < 4 (C-137) ; au-dessus elle est écrite « NON JUGÉ » et ne compte pas comme verte.
Preuve : `--fichier=zz-v164a.html` rougit (D, T : la silhouette rendue au Studio 3 s après l'arrivée).
"""
import sys, glob, json, io
sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
def duree(nom, img):
    ch = B.charge()
    if ch >= 4: print('  ·  NON JUGÉ (charge %.1f) — %s : plus longue image %.0f ms' % (ch, nom, img), flush=True); return
    juge('%s : aucune image au-delà de 50 ms (charge %.1f)' % (nom, ch), img <= 50, 'plus longue image %.0f ms' % img)
ESPION = """()=>{ window.__R=[]; const rd=window._rendDalle; window._rendDalle=function(id,w,h,o){ const t=performance.now(); const r=rd.apply(this,arguments); if(w===64&&h===64) window.__R.push([Math.round(t), Math.round(performance.now()-t), (o&&o.monde&&o.monde.m)||'courant']); return r; };
  window.__D=[]; let av=performance.now(); (function f(t){ window.__D.push([Math.round(t), t-av]); av=t; requestAnimationFrame(f); })(performance.now()); }"""
MONDE = "()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')"
def vers(pg, voulu, sens):
    for _ in range(24):
        if pg.evaluate(MONDE) == voulu: return True
        B.glisse(pg, B.droite([300, 300], [80, 300], 10) if sens > 0 else B.droite([80, 300], [300, 300], 10), pas=18); pg.wait_for_timeout(1500)
    return False
def arrivee(pg, nom):
    """au Studio : le monde juste avant Ramage, puis le glissé qui y arrive ; ce qui se passe dans les 5 s qui suivent"""
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3500)
    ok = vers(pg, 'pixel', 1) or vers(pg, 'pixel', -1); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{ window.__R=[]; window.__D=[]; }")
    t1 = pg.evaluate("()=>performance.now()"); B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); t1 = pg.evaluate("()=>performance.now()")
    pg.wait_for_timeout(5000)
    m = pg.evaluate(MONDE); R = pg.evaluate("()=>window.__R"); D = pg.evaluate("()=>window.__D")
    arr = [r for r in R if t1 - 50 <= r[0] <= t1 + 5000]; img = max([d[1] for d in D if t1 <= d[0] <= t1 + 5000] or [0])
    juge('%s · arrivé sur Ramage ; dans les 5 s, aucun rendu de la silhouette' % nom, ok and m == 'ramage' and not arr, 'monde %s · rendus %s' % (m, [(r[0] - round(t1), r[1], r[2]) for r in arr]))
    duree('%s · les 5 s qui suivent l\'arrivée' % nom, img)
    return t1
with sync_playwright() as p:
    b = p.webkit.launch()
    # ── D · même famille : Mascaret, 25 paroles ──
    ctx = B.contexte(b, stockage={'promi_studio': '{"m":"mascaret","p":"signal","h":0}'}); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate(ESPION); pg.wait_for_timeout(13000)
    pret = pg.evaluate("()=>(window._silhouettes?window._silhouettes():[]).filter(k=>k.indexOf('ramage|')===0)")
    acc = [r for r in pg.evaluate("()=>window.__R") if r[2] == 'ramage']
    juge('D · l\'accueil au repos a préparé la silhouette de Ramage', bool(pret), '%s · bloc sur l\'accueil %s ms' % (pret, [r[1] for r in acc]))
    arrivee(pg, 'D · Mascaret (même famille)')
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('D · aucune erreur de page', False, er[:2])
    ctx.close()
    # ── T · l'état exporté de Tom (A2) ──
    L = [f for f in sorted(glob.glob('etats/tom-*.json')) if json.loads(json.load(io.open(f, encoding='utf-8')).get('ls', {}).get('promi_state', '{}') or '{}').get('promises')]
    if not L: juge("T · l'état exporté de Tom existe", False, 'aucun')
    else:
        ctx, d = B.contexte_tom(b, L[-1]); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000)
        pg.wait_for_timeout(3000); pg.evaluate(ESPION); pg.wait_for_timeout(13000)
        pret = pg.evaluate("()=>(window._silhouettes?window._silhouettes():[]).filter(k=>k.indexOf('ramage|')===0)")
        juge('T · %s (%s) : l\'accueil au repos a préparé la silhouette de Ramage' % (L[-1].split('/')[-1], d['toile'].get('monde')), bool(pret), pret)
        arrivee(pg, 'T · l\'état de Tom')
        ctx.close()
    # ── E · un ancien monde : Pochade ──
    ctx = B.contexte(b, stockage={'promi_studio': '{"m":"encre","p":"signal","h":0}'}); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate(ESPION); pg.wait_for_timeout(4000)
    t1 = arrivee(pg, 'E · Pochade (autre famille)')
    pg.wait_for_timeout(4000)
    R = pg.evaluate("()=>window.__R"); apres = [r for r in R if r[0] > t1 + 5000]
    juge('E · la silhouette vient ensuite, au calme', bool(apres) or bool(pg.evaluate("()=>(window._silhouettes?window._silhouettes():[]).some(k=>k.indexOf('ramage|')===0)")),
         'rendus après 5 s : %s' % [(r[0] - round(t1), r[1]) for r in apres])
    ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
