#!/usr/bin/env python3
"""redteam_veille_bords.py — ⚑ v163 (Tom, C-181 §3) : LA VEILLE TOUCHE LES BORDS VISIBLES, SES FLAQUES DURENT 350 ms.

« Le logo doit toucher les bords haut et bas VISIBLES (visualViewport) sur mon écran (fenêtre exportée 390 × 651, Safari avec ses barres). Les flaques
d'entrée et de sortie plus rapides, ≈ 350 ms chacune. Juge : l'encre au bord visible ± 1 pt sur les quatre bords, à ma fenêtre et aux échelles 1 et 0,79. »

Banc WebKit ×3, `?veille=2`. Le logo est posé (boucle d'images arrêtée) sur chacune de ses quatre bornes ; l'ENCRE est lue sur l'image (pixels qui
diffèrent du fond) et comparée au bord de la zone visible :
  A · haut, bas, gauche, droite : l'encre à 1 pt au plus du bord (pas plus loin, pas au-delà), à 390 × 651, 430 × 932 (échelle 1), 330 × 714 (≈ 0,79) ;
  B · l'entrée et la sortie passent par `_passageFlaques` en 350 ms (± 30) chacune.
Preuve : `--fichier=zz-v162.html` rougit (la gauche à 1,3 pt ; les flaques à 1 100 et 900 ms).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
PIEGE = """(()=>{ window.__pf=[]; let f; Object.defineProperty(window,'_passageFlaques',{configurable:true, get:()=>f ? function(h,o){ window.__pf.push([o&&o.mode, o&&o.duree]); return f.apply(this, arguments); } : f, set:v=>{ f=v; }}); })();"""
def encre(pg, vw, vh):
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = im.size[0] / vw; W, H = im.size; px = im.load()
    fond = px[W - 3, 3]; xs = []; ys = []   # un coin : jamais sous le logo posé au milieu d'un bord
    for yy in range(H):
        for xx in range(W):
            q = px[xx, yy]
            if sum(abs(a - b) for a, b in zip(q, fond)) > 120: xs.append(xx); ys.append(yy)
    return (min(xs) / k, max(xs + [0]) / k + 1 / k, min(ys) / k, max(ys + [0]) / k + 1 / k) if xs else None
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ((390, 651), (430, 932), (330, 714)):
        ctx = B.contexte(b, vw=vw, vh=vh); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, F, q='?veille=2', attente=1500)
        pg.wait_for_timeout(4500); v = pg.evaluate("()=>_veille()") or {}
        if not v.get('active'):
            juge('[%d×%d] la veille a démarré' % (vw, vh), False, v); ctx.close(); continue
        pg.evaluate("()=>{ window.__raf=window.requestAnimationFrame; window.requestAnimationFrame=function(){ return 0; }; }"); pg.wait_for_timeout(250)
        Bn = v['bornes']; C = v['cadre']; mx = (Bn['x0'] + Bn['x1']) / 2; my = (Bn['y0'] + Bn['y1']) / 2
        for nom, x, y, bord in (('haut', mx, Bn['y0'], 2), ('bas', mx, Bn['y1'], 3), ('gauche', Bn['x0'], my, 0), ('droite', Bn['x1'], my, 1)):
            pg.evaluate("a=>{ const c=document.querySelector('#promiVeille canvas'); c.style.transform='translate('+a[0]+'px,'+a[1]+'px)'; }", [x, y]); pg.wait_for_timeout(120)
            e = encre(pg, vw, vh); cible = (0, C['width'], 0, C['height'])[bord]
            d = None if not e else (e[bord] - cible if bord in (0, 2) else cible - e[bord])
            juge('[%d×%d] A · l\'encre touche le bord %s visible (≤ 1 pt)' % (vw, vh, nom), d is not None and -0.4 <= d <= 1.0,
                 'encre %s · bord %.1f · écart %s pt' % (e and [round(t, 1) for t in e], cible, d if d is None else round(d, 2)))
        pg.evaluate("()=>{ window.requestAnimationFrame=window.__raf; }"); pg.wait_for_timeout(200)
        B.tap(pg, vw / 2, vh / 2); pg.wait_for_timeout(800)
        pf = pg.evaluate("()=>window.__pf")
        ok = any(m == 'couvre' and abs((d or 0) - 350) <= 30 for m, d in pf) and any(m == 'ouvre' and abs((d or 0) - 350) <= 30 for m, d in pf)
        juge('[%d×%d] B · l\'entrée et la sortie en flaques, 350 ms chacune' % (vw, vh), ok, pf)
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
