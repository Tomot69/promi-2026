#!/usr/bin/env python3
"""redteam_studio_saccade.py — ⚑ v158 (Tom, C-175) : LE STUDIO SACCADE SOUS CERTAINS MONDES (MASCARET D'ABORD).

« Au Studio, Mascaret et quelques autres saccadent. Mesure les 20 mondes sur le vrai chemin (ouvrir le Studio, passer d'un monde à l'autre, faire glisser
le curseur de couleur), liste ceux qui saccadent avec leur cause, corrige en commençant par Mascaret. Compare avant et après à charge égale ; “réglé”
seulement au calme. »

Ce juge compte le TRAVAIL pendant un glissé de la jauge des couleurs — les comptes ne dépendent pas de la charge de la machine (la règle de redteam_pleine) ;
les durées ne sont jugées qu'au calme (charge < 4). Banc comme Tom (WebKit 390 × 844 ×3, doigt, Toile de 25 paroles, membre « Ma Parole ! » : tous les
mondes vivants), Mascaret, Touffe, Madrure, Houle, sur un glissé de 102 mouvements à ≈ 160 par seconde (plusieurs par image, comme sur l'iPhone) :
  A · la teinte s'applique au plus une fois par image (`Toile.setHue` ≤ le nombre d'images du glissé + 2) — elle s'appliquait à chaque mouvement du doigt ;
  B · aucune trame d'un écran caché derrière le Studio n'est repeinte pendant le glissé (l'Aura, l'Index, le Cercle, la fiche, les Réglages) ; elles
      sont repeintes une fois le Studio refermé ;
  C · la dalle de la jauge n'est pas refaite pendant le glissé (sa silhouette ne dépend pas de la teinte) ;
  D · au calme seulement : pendant le glissé, p95 de l'image ≤ 34 ms et aucune image au-delà de 50 ms.
Preuve : `--fichier=zz-av157.html` rougit (A, B, C).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
MONDES = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mondes=')), 'mascaret,touffe,madrure,sillons').split(',')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
ESPION = """()=>{ window.__on=false; window.__C={hue:0, trames:{}, dalleJauge:0, images:0, d:[]};
  const h=Toile.setHue; Toile.setHue=function(){ if(window.__on) window.__C.hue++; return h.apply(this,arguments); };
  ['auTrame','ixTrame','shTrame','dpRefresh','esRefresh','fdRefresh','_trameReglages','promiTrame'].forEach(n=>{ const f=window[n]; if(typeof f!=='function') return;
    window[n]=function(){ const t=performance.now(); const r=f.apply(this,arguments); if(window.__on){ /* compte seulement ce qui a PEINT (plus de 2 ms) */ if(performance.now()-t>2) window.__C.trames[n]=(window.__C.trames[n]||0)+1; } return r; }; });
  const rd=window._rendDalle; if(rd) window._rendDalle=function(id,w,h,o){ if(window.__on && w===64 && h===64) window.__C.dalleJauge++; return rd.apply(this,arguments); };
  let av=performance.now(); (function f(t){ if(window.__on){ window.__C.images++; window.__C.d.push(t-av); } av=t; requestAnimationFrame(f); })(performance.now()); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
    pg.evaluate(ESPION); vus = []
    for i in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m in vus: break
        vus.append(m)
        if m in MONDES:
            pg.wait_for_timeout(1500)
            x, y = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'); const r=e.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
            charge = B.charge()
            pg.evaluate("()=>{ window.__C={hue:0, trames:{}, dalleJauge:0, images:0, d:[]}; window.__on=true; }")
            B.glisse(pg, [[x + 100 * t / 40, y] for t in range(41)] + [[x + 100 - 200 * t / 60, y] for t in range(61)], pas=6); pg.wait_for_timeout(500)   # ≈ 160 mouvements/s, comme le doigt sur l'iPhone (Safari ne les regroupe pas)
            C = pg.evaluate("()=>{ window.__on=false; return window.__C; }")
            juge('[%s] A · la teinte s\'applique au plus une fois par image (%d images)' % (m, C['images']), C['hue'] <= C['images'] + 2, 'setHue × %d' % C['hue'])
            juge('[%s] B · aucune trame d\'un écran caché repeinte pendant le glissé' % m, not C['trames'], C['trames'])
            juge('[%s] C · la dalle de la jauge n\'est pas refaite pendant le glissé' % m, C['dalleJauge'] == 0, 'rendus de la dalle de la jauge : %d' % C['dalleJauge'])
            d = sorted(C['d']); p95 = d[int(0.95 * (len(d) - 1))] if d else 0; n50 = sum(1 for v in d if v > 50)
            calme = charge < 4
            juge('[%s] D · p95 ≤ 34 ms, aucune image > 50 ms%s' % (m, '' if calme else ' — NON JUGÉ (charge %.1f)' % charge), (not calme) or (p95 <= 34 and n50 == 0), 'p95 %.0f ms · %d images > 50 ms · charge %.1f' % (p95, n50, charge))
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1400)
    # refermé : les trames gardées sont repeintes
    pg.evaluate("()=>{ window.__C.trames={}; window.__on=true; const c=document.querySelector('#studioScreen .closeb'); if(c) c.click(); }"); pg.wait_for_timeout(4000)
    apres = pg.evaluate("()=>{ window.__on=false; return [window.__C.trames, window._trameAttente?window._trameAttente():null]; }")
    juge('B · le Studio refermé, les trames gardées sont repeintes, il n\'en reste aucune en attente', apres[1] == [] or apres[1] is None, 'repeintes : %s · en attente : %s' % (apres[0], apres[1]))
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page', not er, er[:2])
    # E · ⚑ v159 (C-175 suite) : la silhouette de la jauge est préparée au repos sur l'accueil — au Studio, d'un monde à l'autre (même famille de semis),
    #     elle n'est plus rendue (un bloc de 50 à 490 ms pendant que l'aperçu bouge)
    ctx = B.contexte(b); B.toile_pleine(ctx, 5)
    ctx.add_init_script("window.__RD=0; window.__RDon=false; (function w(){ if(window._rendDalle && !window._rendDalle.__w){ const f=window._rendDalle; const g=function(id,a,b2,o){ if(window.__RDon && a===64 && b2===64) window.__RD++; return f.apply(this,arguments); }; g.__w=1; Object.keys(f).forEach(k=>g[k]=f[k]); window._rendDalle=g; } setTimeout(w,100); })();")
    pg = B.ouvre(ctx, F); pg.wait_for_timeout(16000)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} window.__RDon=true; document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500); vus = []
    for i in range(7):
        B.glisse(pg, B.droite([300, 420], [90, 420], 10), pas=16); pg.wait_for_timeout(1700); vus.append(pg.evaluate("()=>Toile.getTheme()"))
    n = pg.evaluate("()=>window.__RD")
    juge('E · accueil posé 16 s, puis sept mondes au Studio (%s) : la silhouette de la jauge n\'est jamais rendue au Studio' % ','.join(vus), n == 0, '%d rendus de 64 px au Studio' % n)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
