#!/usr/bin/env python3
"""redteam_centre_validation.py — ⚑ v155 (Tom, C-167) : LA PHRASE DE VALIDATION EST CENTRÉE SUR L'ÉCRAN.

« Tom pense que la phrase de validation est encore alignée à gauche. Vérifie-le pour toutes les phrases de validation, sur Promi, Chiche et Cercle, en
clair et en sombre. Juge : centre de la phrase = centre de l'écran à ±1 pt. »
Banc comme Tom (WebKit 390 × 844 ×3, le trait tracé au doigt). La phrase est PEINTE dans la nappe : on lit son ENCRE sur les pixels du canevas de la
nappe (les pixels sombres sur le vert, dans la bande de la phrase), 1 s après le lever — jamais une boîte que l'app déclare.
Cas : Promi (« Parole tenue ! »), Chiche (« Défi relevé ! »), un Promi planté dans un Cercle ; clair et sombre ; et deux dans la hauteur visible de
Safari (390 × 664 : l'appareil réduit, comme sur l'iPhone).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
SONDE = """()=>{ window.__lever=0; window.__ink=null;
  document.addEventListener('touchend', function(){ if(!window.__lever) window.__lever=performance.now(); }, {capture:true, once:true});
  window._mareeReleve=function(g, cv, t, u, T){ if(window.__ink || !window.__lever || performance.now()-window.__lever<1000) return;
    const k=cv.width/390, d=g.getImageData(0,0,cv.width,cv.height).data, W=cv.width, H=cv.height; let x0=1e9, x1=-1e9, y0=1e9, y1=-1e9, n=0;
    for(let y=Math.round(300*k); y<Math.min(H, Math.round(520*k)); y++){ for(let x=0; x<W; x++){ const i=4*(y*W+x); if(d[i+3]<200) continue; const L=0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2]; if(L<90){ n++; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } } }
    const it=document.getElementById('instTenue');
    window.__ink={n:n, x0:x0/k, x1:(x1+1)/k, y0:y0/k, y1:(y1+1)/k, txt:it?it.textContent:null, aria:cv.getAttribute('aria-label')}; }; }"""
def cas(b, sombre, nature, vh=844):
    ctx = B.contexte(b, sombre=sombre, vh=vh); pg = B.ouvre(ctx, F)
    B.plante(pg, 'rendre le livre', nature=1 if nature == 'chiche' else 0); pg.wait_for_timeout(500)
    if nature == 'cercle':
        pg.evaluate("()=>{ const p=promises[promises.length-1]; p.nuee='famille'; try{ saveState(); }catch(e){} try{ syncAll(); }catch(e){} }"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    pg.evaluate(SONDE)
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    y = z[1] + z[3] * 0.45
    B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    for _ in range(30):
        pg.wait_for_timeout(150)
        if pg.evaluate("()=>!!window.__ink"): break
    ink = pg.evaluate("()=>window.__ink"); er = [x for x in pg.erreurs if 'version.json' not in x]; ctx.close()
    T = '%s, %s%s' % ('sombre' if sombre else 'clair', nature, '' if vh == 844 else ', Safari 390 × %d' % vh)
    if not ink or ink['n'] < 50:
        juge('[%s] la phrase de validation est peinte dans la nappe' % T, False, ink); return
    c = (ink['x0'] + ink['x1']) / 2
    juge('[%s] « %s » : centre de l\'encre = centre de l\'écran (195 pt) à ± 1 pt' % (T, ink['aria']), abs(c - 195) <= 1.0,
         'encre de %.1f à %.1f pt → centre %.2f pt (écart %+.2f) · %d pixels' % (ink['x0'], ink['x1'], c, c - 195, ink['n']))
    if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        for nat in ('promi', 'chiche', 'cercle'): cas(b, sombre, nat)
    cas(b, False, 'promi', 664); cas(b, True, 'chiche', 664)   # la hauteur visible de Safari sur l'iPhone 16e : l'appareil est réduit (× 0,79)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
