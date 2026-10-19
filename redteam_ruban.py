#!/usr/bin/env python3
"""redteam_ruban.py — ⚑ v148 (Tom, 16 oct. 2026, C-148) : « Quand on trace pour valider, sur une fiche ou dans la page +, le bandeau vert amande
est un rectangle droit : ça fait artificiel, c'est cheap. Il devient ondulé et suit la courbe du trait. Il est plus fin (15 à 25 % moins épais),
pour moins recouvrir. Ses contours sont légèrement irréguliers, sans excès : il garde une allure lisse qui suit le trait à tracer. S'il est
transparent aujourd'hui, c'est contraire à la règle A2 : passe-le en aplat amande #8FE08F. »

Banc comme Tom (WebKit, 390 × 844 ×3), clair et sombre : la fiche d'un Promi, d'un Chiche, la page + d'un Promi. Le doigt trace, et pendant qu'il
est posé, une fois le seuil de 60 pt passé (C-107), on lit :
  A · plus de rectangle : la zone du geste n'a aucun fond (alpha 0)
  B · un ruban est peint, en AMANDE #8FE08F, PLEIN : ≥ 97 % de ses pixels à l'opacité 255 et à ΔE ≤ 3 de #8FE08F (le reste : le lissage du bord)
  C · son épaisseur, colonne par colonne, fait 75 à 85 % de 118 pt (le rectangle d'avant) — médiane
  D · il SUIT LA COURBE DU TRAIT : son milieu, colonne par colonne, suit l'onde du trait (écart-type du résidu ≤ 4 pt), alors qu'un rectangle
      droit aurait un résidu égal à l'onde elle-même (≥ 8 pt)
  E · ses bords sont légèrement irréguliers, sans excès : l'écart de chaque bord à l'onde décalée est de 0,4 à 3,5 pt (écart-type)
  F · le mot du trait n'est pas coupé en deux par le ruban : il est soit entier, soit entièrement découpé (clip) pendant que le ruban est là
Preuve : `--fichier=zz-av147.html` rougit (A, B).
⚑ v149 (Tom, 18 oct. 2026, C-154) — « La vague de création prend la couleur de l'état dans lequel entre la parole (« à tenir » ou « en cours », selon le
code). L'amande est réservée à la célébration. » B, sur la page + : le ruban est plein, à la couleur de l'état « en cours » #291547 (toute parole plantée
entre « en cours ») ; sur la fiche, il reste amande. Original : sauvegardes/redteam_ruban-avant-v149.py. `--fichier=zz-av148.html` rougit (B, page +).
⚑ v150 (Tom, C-154) — « la vague de création passe en orange, la couleur de l'état « à tenir », #DD4D23 ; ce n'est pas l'orange d'action #FB4C0D ».
B, sur la page + : #DD4D23. Original : sauvegardes/redteam_ruban-avant-v150.py.
⚑ v151 (Tom, C-154) — « une parole créée est « en cours » : la vague prend la couleur de l'état réel, #291547 » (l'orange de v150 reposait sur une
prémisse fausse). B, sur la page + : #291547. Original : sauvegardes/redteam_ruban-avant-v151.py. `--fichier=zz-av150.html` rougit (B, page +). `--fichier=zz-av149.html` rougit (B, page +).
"""
import sys, math; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(ok); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)

LIT = """(a)=>{ const [zid, att]=a; const z=document.getElementById(zid), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const bg=getComputedStyle(z).backgroundColor, al=(bg.match(/[\\d.]+/g)||[0,0,0,0]); const fond=(al.length===4?+al[3]:(bg==='transparent'?0:1));
  const cv=document.getElementById('tenirRuban'); let geo=null;
  if(zid==='tenirZone'){ const v=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','); geo={base:+v[0], amp:+v[1]}; }
  else { const e=_ppEcran(); geo={base:e.base, amp:e.amp}; }
  const y=_onde.onde(geo.base, geo.amp), Y=[]; for(let x=10;x<=380;x+=10) Y.push(y(x));
  if(!cv) return {fond:fond, ruban:false, Y:Y};
  const r=cv.getBoundingClientRect(), top=(r.top-D.top)/k, s=cv.width/(r.width/k), d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, W=cv.width, H=cv.height;
  let n=0, plein=0, juste=0; for(let i=0;i<d.length;i+=4*3){ if(d[i+3]>8){ n++; if(d[i+3]>=250){ plein++; if(Math.abs(d[i]-att[0])<=4 && Math.abs(d[i+1]-att[1])<=4 && Math.abs(d[i+2]-att[2])<=4) juste++; } } }
  const col=[]; for(let x=10;x<=380;x+=10){ const X=Math.round(x*s); let a0=-1, a1=-1; for(let j=0;j<H;j++){ if(d[(j*W+X)*4+3]>128){ if(a0<0) a0=j; a1=j; } } col.push(a0<0?null:[top+a0/s, top+a1/s]); }
  /* le mot du trait */
  const mot=zid==='tenirZone'?document.getElementById('dptTrace'):document.querySelector('#createSheet .pp-trace'); let motEtat=null;
  if(mot){ const cp=getComputedStyle(mot).clipPath||getComputedStyle(mot).webkitClipPath||'none', mr=mot.getBoundingClientRect(); const m=/inset\\(0(?:px)? 0(?:px)? 0(?:px)? ([\\d.]+)%/.exec(cp); const pc=m?+m[1]:0;
    const mt=(mr.top-D.top)/k, mb=(mr.bottom-D.top)/k, ml=(mr.left-D.left)/k, mrr=(mr.right-D.left)/k; let couvre=0, tot=0;
    for(let x=Math.ceil(ml);x<=mrr;x+=4){ const X=Math.round(x*s); if(X<0||X>=W) continue; for(let yy=mt+2;yy<=mb-2;yy+=3){ const J=Math.round((yy-top)*s); if(J<0||J>=H) continue; tot++; if(d[(J*W+X)*4+3]>128) couvre++; } }
    motEtat={pc:pc, part:tot?couvre/tot:0, vis:getComputedStyle(mot).visibility!=='hidden' && getComputedStyle(mot).display!=='none' && mr.width>4}; }
  return {fond:fond, ruban:true, n:n, plein:plein, juste:juste, col:col, Y:Y, mot:motEtat}; }"""

def sd(v):
    m = sum(v) / len(v); return (sum((a - m) ** 2 for a in v) / len(v)) ** 0.5
def un(b, th, ecran, nature):
    T = '[%s, %s %s]' % ('clair' if th == 'light' else 'sombre', ecran, ['Promi', 'Chiche'][nature])
    ctx = B.contexte(b, sombre=(th == 'dark')); pg = B.ouvre(ctx, F)
    if ecran == 'fiche':
        if nature == 1: B.plante_doigt(pg, 'courir dimanche', qui='Marion', nature=1)
        else: B.plante(pg, 'rendre le livre', qui='Marion')
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2800)
        zid = 'tenirZone'; z = pg.evaluate("()=>{ const v=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','); return +v[0]; }"); x0 = 200
    else:
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ document.getElementById('fTitle').value='lire un livre'; }")
        zid = 'planterZone'; z = pg.evaluate("()=>_ppEcran().base"); x0 = 60
    P = [list(B.pt(pg, x0 + 150 * i / 16, z + 8)) for i in range(17)]
    pg.evaluate("(a)=>{ window.__gl=(" + B.GLISSE + ")(a); return 1; }", [P, 95, 380, 11, 11])
    fond0 = 0
    for _ in range(30):   # le doigt posé, avant le seuil : la zone ne porte aucun rectangle non plus
        pg.wait_for_timeout(40)
        f_ = pg.evaluate("(z)=>{ const e=document.getElementById(z); if(!e.classList.contains('ouvert')) return null; const al=(getComputedStyle(e).backgroundColor.match(/[\\d.]+/g)||[0,0,0,0]); return al.length===4?+al[3]:1; }", zid)
        if f_ is not None: fond0 = f_; break
    for _ in range(60):   # le seuil passé : le ruban paraît ; on le lit 320 ms plus tard, le doigt toujours posé
        pg.wait_for_timeout(80)
        if pg.evaluate("()=>!!(window._ruban && window._ruban.etat().actif) || !!document.querySelector('#tenirZone.atteint,#planterZone.atteint')"): break
    pg.wait_for_timeout(320)
    att = (143, 224, 143) if zid == 'tenirZone' else (41, 21, 71)   # v151 (C-154) : la fiche, l'amande ; la page +, l'état « en cours » où entre la parole (#291547, jamais #FB4C0D)
    r = pg.evaluate(LIT, [zid, list(att)])
    juge('%s A · plus de rectangle : la zone du geste n\'a aucun fond, ni doigt posé ni seuil passé' % T, r['fond'] == 0 and fond0 == 0, 'alpha du fond %.2f (doigt posé : %.2f)' % (r['fond'], fond0))
    if not r['ruban']:
        juge('%s B · un ruban est peint' % T, False, 'aucun ruban'); ctx.close(); return
    pp = r['juste'] / max(1, r['n'])
    juge('%s B · le ruban est un aplat plein, %s (≥ 97 %% des pixels)' % (T, 'amande #8FE08F (la célébration)' if zid == 'tenirZone' else '#291547 (l\'état « en cours », C-154 v151)'), pp >= 0.97, '%.1f %% justes, %.1f %% pleins' % (100 * pp, 100 * r['plein'] / max(1, r['n'])))
    C = [(c, y) for c, y in zip(r['col'], r['Y']) if c]
    ep = sorted(c[1] - c[0] for c, y in C); epm = ep[len(ep) // 2] if ep else 0
    juge('%s C · plus fin : épaisseur médiane à 75–85 %% des 118 pt d\'avant' % T, 0.75 * 118 <= epm <= 0.85 * 118, '%.1f pt (%.0f %%)' % (epm, 100 * epm / 118))
    mil = [((c[0] + c[1]) / 2) - y for c, y in C]; amp_onde = sd([y for c, y in C])
    juge('%s D · il suit la courbe du trait : écart-type du milieu autour de l\'onde ≤ 4 pt' % T, sd(mil) <= 4 and amp_onde >= 8, '%.1f pt (l\'onde elle-même : %.1f pt)' % (sd(mil), amp_onde))
    ht = [c[0] - y for c, y in C]; bs = [c[1] - y for c, y in C]
    juge('%s E · bords légèrement irréguliers, sans excès (0,4 à 3,5 pt autour de l\'onde décalée)' % T, 0.4 <= sd(ht) <= 3.5 and 0.4 <= sd(bs) <= 3.5, 'haut %.2f · bas %.2f pt' % (sd(ht), sd(bs)))
    m = r.get('mot')
    juge('%s F · le mot du trait n\'est pas coupé en deux : entier ou entièrement découpé' % T, (m is None) or (not m['vis']) or m['part'] < 0.03 or m['pc'] >= 99, m)
    pg.wait_for_timeout(2500); ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        for ecran, nat in (('fiche', 0), ('fiche', 1), ('page +', 0)): un(b, th, ecran, nat)
    b.close()
ok = sum(1 for c in res if c); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
