#!/usr/bin/env python3
"""
redteam_tenir.py — TENIR : LA MARÉE (v146, Tom, 14 oct. 2026 — C-118, variante A corrigée).
« Plus de liseré, de filet, ni de jour ouvert sous le trait. Le trait EST le fond du bas en mode célébration. Aucune séparation entre le trait et le vert
  de même couleur : c'est une seule matière. Ce qui descend (le vert en rideau) avance EN FLAQUES, vite, vers le bas. L'instant reste à environ 2 s.
  Ni fondu, ni transparence, ni dégradé. Pas de changement d'écran. »
Banc comme Tom (banc_tom : WebKit, 390 × 844 ×3, Toile vide, une parole plantée par l'app, sa fiche, le trait tracé au doigt), clair et sombre, un Promi
et un Chiche. La couche de la marée est relevée DANS LA PAGE, image par image (`_mareeReleve`) ; le verdict se lit sur ses pixels (l'opacité, la part
couverte, la forme du bord) et sur la capture (le champ, la fiche à la fin).
  A · elle paraît, et elle part : la fiche reste ouverte, aucun autre écran ; la parole est tenue ;
  B · une seule matière : dès que la nappe descend, juste sous le trait (de son bord haut à 24 pt en dessous) TOUT est couvert, sur toute la largeur ;
  C · (v147) un rideau d'un seul tenant : la part couverte monte sans jamais redescendre ; aucune colonne trouée ; le front ondule à peine (1 à 6 pt) — avant : en flaques (les bas
      des colonnes s'écartent de ≥ 8 pt) ; la nappe atteint la barre ;
  D · ni fondu, ni transparence : sur la couche, ≤ 2 % des pixels peints sont entre 10 et 245 d'opacité (le lissage du bord) ;
  E · la durée : la descente finie en 0,5 à 1,0 s ; de la marée qui paraît à la marée partie, 2,1 à 2,8 s (« environ 2 s ») ;
  F · le champ garde la couleur de sa nature pendant tout l'instant (plus de champ amande) — rien ne saute au passage à « juste après ».
Preuve (§7) : `--fichier=zz-avant-v146.html` — il rougit (aucune couche).
"""
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
import os
CHARGE = float(os.popen('sysctl -n vm.loadavg').read().split()[1])
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-112s %s' % ('✅' if c else '❌', nom, str(d)[:240]), flush=True)
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null; }"
SONDE = """()=>{ window.__mr=[]; window.__t0=0; window._mareeReleve=function(g, cv, t, u, T, N){
    const k=cv.width/390, d=g.getImageData(0,0,cv.width,cv.height).data, W=cv.width; let n=0, mid=0, tot=0, bas=[], sous=0, sousN=0;
    let trous=0; for(let x=4; x<390; x+=8){ const ty=T.y(x)+6; let lo=-1, fin=false, trou=false; for(let y=Math.ceil(ty); y<760; y+=3){ const a=d[((Math.round(y*k))*W+Math.round(x*k))*4+3]; tot++; if(a>200 && fin) trou=true; if(a<=200 && lo>0) fin=true; if(a>200){ n++; lo=y; } else if(a>10) mid++; if(y<ty+24){ sousN++; if(a>200) sous++; } } bas.push(lo); if(trou) trous++; }
    window.__mr.push({t:Math.round(t), u:+u.toFixed(3), part:n/Math.max(1,tot), mid:mid/Math.max(1,n+mid), bas:bas, sous:sous/Math.max(1,sousN), trous:trous}); }; }"""
CHAMP = "()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [d.left+30*k, d.top+150*k]; }"
def un(b, th, nature):
    T = '%s, %s' % ('clair' if th == 'light' else 'sombre', nature); print('\n── %s' % T)
    ctx = contexte(b, sombre=(th == 'dark')); pg = ouvre(ctx, F)
    if nature == 'chiche': plante_doigt(pg, 'courir dimanche', nature=1)
    else: plante(pg, 'rendre le livre')
    pg.wait_for_timeout(800); pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    pg.evaluate(SONDE)
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    pg.evaluate("()=>{ window.__champ=[]; window.__fiche=[]; const t0=performance.now(); (function f(){ const dp=document.getElementById('detailPoster'); let ch=null; try{ const c=document.getElementById('dpTrameCv'), k=c.width/390, d=c.getContext('2d').getImageData(Math.round(30*k), Math.round(150*k), 1, 1).data; ch=[d[0],d[1],d[2]]; }catch(e){} window.__fiche.push([Math.round(performance.now()-t0), dp.classList.contains('show'), [...document.querySelectorAll('.screen.show,.sheet.show')].length, !!document.getElementById('tenirMaree'), ch]); if(performance.now()-t0<9000) requestAnimationFrame(f); })(); }")
    pg.evaluate("()=>{ window.__lever=0; const t0=performance.now(); document.addEventListener('touchend', function(){ if(!window.__lever) window.__lever=Math.round(performance.now()-t0); }, {capture:true, once:true}); }")
    glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    pg.wait_for_timeout(3400)   # aucune capture pendant l'instant : une capture d'écran WebKit bloque la page (elle allongeait la mesure de 600 ms)
    # ⚑ v147 — la machine chargée (une autre session) étire l'instant : on attend que la nappe soit PARTIE (8 s au plus), au lieu d'une fenêtre fixe
    for _ in range(23):
        if pg.evaluate("()=>{ const F=window.__fiche||[]; return F.length>0 && !F[F.length-1][3]; }"): break
        pg.wait_for_timeout(200)
    R = pg.evaluate("()=>window.__mr||[]"); FI = pg.evaluate("()=>window.__fiche||[]"); st = pg.evaluate("()=>promises[promises.length-1].status")
    lev = pg.evaluate("()=>window.__lever||0"); vu = [f for f in FI if f[3]]; t_on = vu[0][0] if vu else None; t_off = next((f[0] - lev for f in FI if t_on is not None and f[0] > t_on and not f[3]), None)
    juge('[%s] A · la marée paraît et part ; la fiche reste ouverte du début à la fin, aucun autre écran ; la parole est tenue' % T, bool(R) and t_on is not None and t_off is not None and all(f[1] and f[2] == 0 for f in FI) and st == 'tenu', '%d images relevées · statut %s' % (len(R), st))
    if not R: ctx.close(); return
    D = [r for r in R if r['u'] > 0.02 and r['t'] < 1900]; desc = [r for r in R if r['t'] < 1900]
    juge('[%s] B · une seule matière : sous le trait (son bord → 24 pt dessous) tout est couvert dès que la nappe descend (u ≥ 0,15)' % T, D and min(r['sous'] for r in D if r['u'] >= 0.15) >= 0.985, 'la moindre couverture sous le trait : %.1f %%' % (100 * min([r['sous'] for r in D if r['u'] >= 0.15] or [0])))
    parts = [r['part'] for r in desc]; mono = all(b_ >= a - 0.003 for a, b_ in zip(parts, parts[1:]))
    mi = min(D, key=lambda r: abs(r['part'] - 0.5)) if D else None; ec = 0
    if mi: B = [v for v in mi['bas'] if v > 0]; m_ = sum(B) / max(1, len(B)); ec = (sum((v - m_) ** 2 for v in B) / max(1, len(B))) ** 0.5
    # ⚑ v147 (Tom, C-118, récidive) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_tenir-avant-v147.py). « Un rideau qui
    #   descend d'un seul tenant ; l'abstrait n'est qu'aux bords : un front légèrement irrégulier, et rien d'autre. Ce ne sont pas des flaques séparées. »
    tr = max((r['trous'] for r in desc), default=99)
    juge('[%s] C · un rideau d\'un seul tenant vers le bas : la part couverte monte sans redescendre ; aucune colonne n\'a de trou (couverte du trait au front, pas de flaque séparée) ; le front ondule à peine (écart des bas de 1 à 6 pt) ; il atteint la barre' % T,
         mono and tr == 0 and 1 <= ec <= 6 and max(parts or [0]) >= 0.97,
         'monotone %s · colonnes trouées (au pire) %s · écart à mi-descente %.1f pt · part maximale %.0f %%' % (mono, tr, ec, 100 * max(parts or [0])))
    RD = [r for r in R if r['part'] >= 0.10]
    juge('[%s] D · ni fondu ni transparence : ≤ 2 %% de pixels à demi opaques (le lissage du bord), sur chaque image où la nappe couvre ≥ 10 %% (une nappe naissante a plus de bord que de surface)' % T, RD and max(r['mid'] for r in RD) <= 0.02, 'au plus %.2f %% sur %d images' % (100 * max([r['mid'] for r in RD] or [1]), len(RD)))
    t_plein = next((r['t'] for r in R if r['part'] >= 0.97), None)
    duree = (t_off + lev - t_on) if (t_off is not None and t_on is not None) else None
    if CHARGE >= 4: print('      (non jugé : durées, charge du Mac %.1f ≥ 4 — C-137 ; relevé : pleine à %s ms, instant %s ms)' % (CHARGE, t_plein, duree))
    else: juge('[%s] E · la descente finie en 0,5 à 1,0 s ; l\'instant (de la marée qui paraît à la marée partie) dure 2,1 à 2,8 s — « environ 2 s »' % T, t_plein is not None and 500 <= t_plein <= 1000 and duree is not None and 2100 <= duree <= 2800, 'pleine à %s ms · durée %s ms · paraît %s ms après le lever' % (t_plein, duree, (t_on - lev) if t_on is not None else None))
    champs = [f[4] for f in FI if f[4] and f[0] >= lev]; c0 = champs[0] if champs else (0, 0, 0); ecart = max([sum(abs(c[i] - c0[i]) for i in range(3)) for c in champs] or [999])
    juge('[%s] F · le champ garde sa couleur de nature pendant tout l\'instant (plus de champ amande, rien ne saute à 2 s)' % T, ecart <= 18 and not (abs(c0[0] - 143) + abs(c0[1] - 224) + abs(c0[2] - 143) < 30), 'champ %s · écart maximal %d sur %d images (lu dans le canevas de la fiche)' % (tuple(c0), ecart, len(champs)))
    capture(pg, 'planche-v146/tenir-fin-%s-%s.png' % ('clair' if th == 'light' else 'sombre', nature))
    juge('[%s] aucune erreur de page' % T, not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        for nat in ('promi', 'chiche'): un(b, th, nat)
    b.close()
print('\n  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
