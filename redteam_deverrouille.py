#!/usr/bin/env python3
"""redteam_deverrouille.py — ⚑ v155 (Tom, C-170) : DÉVERROUILLER UN MONDE PAYANT, JAMAIS UNE IMAGE PÉRIMÉE.

« Quand on déverrouille un monde payant, pendant le court chargement, une ANCIENNE Toile apparaît. Le passage au nouveau monde se fait de façon fluide,
dans le langage des transitions de l'app, sans fondu. Jamais une image périmée. Juge : déverrouiller chaque monde payant ; aucune image de Toile périmée,
à aucune image. »
La cause (écrite dans lot-V155-DEVERROUILLE) : sous le Studio la Toile de l'accueil ne peint pas ; elle gardait l'image de l'ancien monde, que le Studio
découvrait en se refermant. Banc comme Tom (WebKit 390 × 844 ×3, une Toile de 25 paroles relue de la sauvegarde), chaque monde payant, au doigt :
  A · le passage : l'aperçu flouté s'ouvre EN FLAQUES sur le monde net (une couverture `mode ouvre` qui va de 0 à 1) ; le flou de `#stBg` ne passe par
      AUCUNE valeur intermédiaire (pas de fondu de filtre)
  B · au moment où le Studio se referme, la Toile de l'accueil est déjà rendue dans le monde déverrouillé ; pendant la fermeture, image par image, elle ne
      ressemble jamais à l'image d'avant le déverrouillage (écart moyen ≥ moitié de l'écart entre l'avant et l'après)
Preuve : `--fichier=zz-av154.html` rougit (A, B).
"""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
MAX = int(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--n=')), '12'))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
PETIT = "()=>{ const c=document.getElementById('toileCv'); const s=document.createElement('canvas'); s.width=48; s.height=104; const g=s.getContext('2d'); g.drawImage(c,0,0,48,104); return Array.from(g.getImageData(0,0,48,104).data); }"
SONDE_V = """()=>{ window.__flou=[]; window.__cv=[]; const bg=document.getElementById('stBg'); const t0=performance.now();
  (function f(){ const t=performance.now()-t0; const fl=getComputedStyle(bg).filter; window.__flou.push(fl); const c=document.getElementById('stDeverrou'); window.__cv.push(c?[c.getAttribute('data-mode'), c.getAttribute('data-u')]:null); if(t<1600) requestAnimationFrame(f); })(); }"""
SONDE_F = """(av)=>{ window.__fe=[]; const c=document.getElementById('toileCv'); const s=document.createElement('canvas'); s.width=48; s.height=104; const g=s.getContext('2d'); const t0=performance.now();
  window.__rendu0=window._accueilRenduMonde||null;
  (function f(){ const t=performance.now()-t0; g.clearRect(0,0,48,104); g.drawImage(c,0,0,48,104); const d=g.getImageData(0,0,48,104).data; let e=0; for(let i=0;i<d.length;i+=4) e+=Math.abs(d[i]-av[i])+Math.abs(d[i+1]-av[i+1])+Math.abs(d[i+2]-av[i+2]);
    window.__fe.push(e/(48*104*3)); if(t<1500) requestAnimationFrame(f); })(); }"""
def ecart(a, b): return sum(abs(a[i] - b[i]) for i in range(len(a)) if i % 4 != 3) / (48 * 104 * 3)
with sync_playwright() as p:
    b = p.webkit.launch(); vus = []
    ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); }"); pg.wait_for_timeout(400)
    for tour in range(40):
        if len(vus) >= MAX: break
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
        w = None
        for i in range(24):
            w = pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')?window._lockedWorld:null")
            if w and w not in vus: break
            B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500); w = None
        if not w: break
        vus.append(w); av = pg.evaluate(PETIT)
        c = pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
        pg.evaluate(SONDE_V); pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(2600)
        fl = pg.evaluate("()=>window.__flou"); cvs = [x for x in pg.evaluate("()=>window.__cv") if x]
        inter = sorted(set(x for x in fl if x not in ('none', 'blur(1.4px)')))
        us = [float(x[1]) for x in cvs if x[1] is not None]
        juge('[%s] A · le passage s\'ouvre en flaques (0 → 1) ; le flou ne passe par aucune valeur intermédiaire' % w,
             bool(us) and min(us) < 0.15 and max(us) > 0.85 and all(x[0] == 'ouvre' for x in cvs) and not inter, 'flaques %s → %s (%d images) · flous intermédiaires %s' % (us and round(min(us), 2), us and round(max(us), 2), len(us), inter[:3]))
        pg.evaluate(SONDE_F, av); B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(1700)
        fe = pg.evaluate("()=>window.__fe"); ap = pg.evaluate(PETIT); ref = ecart(av, ap); r0 = pg.evaluate("()=>window.__rendu0"); m = pg.evaluate("()=>Toile.mondeCourant().m+'|'+Toile.mondeCourant().p")
        juge('[%s] B · à la fermeture du Studio, la Toile de l\'accueil est déjà dans le monde déverrouillé ; jamais l\'image d\'avant' % w,
             r0 == m and fe and min(fe) >= 0.5 * ref, 'rendue %s (monde %s) · écart à l\'avant : au plus près %.1f, avant → après %.1f (%d images)' % (r0, m, min(fe) if fe else -1, ref, len(fe)))
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page (%d mondes payants déverrouillés : %s)' % (len(vus), ', '.join(vus)), not er and len(vus) >= min(MAX, 12), er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
