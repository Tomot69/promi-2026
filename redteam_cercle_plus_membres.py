#!/usr/bin/env python3
"""redteam_cercle_plus_membres.py — ⚑ v181a (Tom, 6 nov. 2026) — LA FICHE D'UN CERCLE.
C-242 : « un + à droite du disque du Cercle, aligné à droite ; un toucher ouvre Peaufiner directement sur MEMBRES, en glissement doux, les membres bien
espacés ; mêmes codes que les autres + (orange #FB4C0D, zone de toucher de 44 pt) ».
C-243 : « le haut du fil passe sous l'en-tête (CERCLE et X) : aucun recouvrement entre le fil et l'en-tête, en haut et pendant le défilement ».

Banc WebKit ×3, le Cercle « Le potager » (six paroles), 430 × 932 (échelle 1) et 330 × 714 (0,79) :
  A · ⚑ v182b (C-242 suite : « juste après la liste des membres, sur la même ligne, avec un petit écart régulier ») — le + paraît : son encre orange #FB4C0D
      (lue sur l'image) commence 8 pt ± 1,5 après la fin du texte de `#dptQui`, centrée sur sa ligne ± 2, haute comme une capitale de cette ligne ± 1,5 ; sa zone
      de 44 pt (les quatre coins, 2 pt en dedans, rendent le bouton au doigt) ;
  F · ⚑ v182b (C-243 suite : « le fil ne doit pas sauter ») — défilé de 6 pt en 6 pt du haut jusqu'en bas puis remonté : chaque carte du fil se déplace exactement du
      pas (± 1 pt), à chaque pas, dans les deux sens (aucun saut, aucune mise en page qui change sous le doigt) ;
  B · un toucher au doigt : Peaufiner s'ouvre, MEMBRES déplié (la liste des personnes visible) ; le panneau GLISSE (au moins 8 images de défilement, aucun
      pas de plus d'un sixième de la course — le pas le plus long de la courbe prévue, à 34 ms par image ; la durée — 420 ms prévus — se lit dans Safari : les images du banc durent 50 à 70 ms) jusqu'à MEMBRES à 110 pt ± 4 ;
  C · les membres bien espacés : aucune carte, ni le bloc « Ma Parole ! », ne recouvre la carte MEMBRES dépliée (rectangles, et au doigt sur
      « + ajouter quelqu'un ») ;
  D · le fil défilé par pas de 30 pt jusqu'en bas, lu image par image : aucune carte du fil au-dessus de 112 pt (12 pt sous l'encart), la bande 101 → 111 pt
      unie (lue sur l'image) ; au repos (défilement 0) rien n'est rogné ; le + ne paraît jamais sous l'encart ;
  E · aucune erreur de page.
Rouge sur v180b (`--fichier=zz-v180b.html`) : A, B, C, D. Rouge sur v182a (`--fichier=zz-v182a.html`) : A (le + à droite), F (l'état défilé).
"""
import sys, io as _io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
def image(pg): return Image.open(_io.BytesIO(pg.screenshot())).convert('RGB')
def px(pg, im, x, y):
    D = B.dev(pg); s = im.width / pg.viewport_size['width']; return im.getpixel((int((D[0] + x * D[4]) * s), int((D[1] + y * D[4]) * s)))
BTN = """()=>{ const b=document.getElementById('cerclePlusMembres'); if(!b) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=b.getBoundingClientRect(), s=getComputedStyle(b);
  if(s.display==='none'||s.visibility==='hidden'||!r.width) return {vu:false};
  const q=document.getElementById('dptQui'), rg=document.createRange(); rg.selectNodeContents(q); const L=[...rg.getClientRects()].filter(x=>x.width>1&&x.height>1), der=L[L.length-1];
  const coins=[[r.left+2,r.top+2],[r.right-2,r.top+2],[r.left+2,r.bottom-2],[r.right-2,r.bottom-2]].map(p=>{ const e=document.elementFromPoint(p[0],p[1]); return !!(e&&e.closest&&e.closest('#cerclePlusMembres')); });
  const cs=getComputedStyle(q), fs=parseFloat(cs.fontSize), g=document.createElement('canvas').getContext('2d'); g.font=cs.fontStyle+' '+cs.fontWeight+' '+fs+'px '+cs.fontFamily; const mA=g.measureText('A');
  return {vu:true, x:(r.left-D.left)/k, y:(r.top-D.top)/k, w:r.width/k, h:r.height/k, fin:(der.right-D.left)/k, ligne:((der.top+der.bottom)/2-D.top)/k, fs:fs, cap:mA.actualBoundingBoxAscent, capHaut:(der.top-D.top)/k+(mA.fontBoundingBoxAscent-mA.actualBoundingBoxAscent), coins:coins}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        T = '[×%s]' % nom
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)
        pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2800)
        q = pg.evaluate(BTN)
        if q and q.get('vu'):
            im = image(pg)
            xs = [x for x in range(int(q['x']), int(q['x'] + q['w']) + 1) for yy in range(int(q['y']), int(q['y'] + q['h']) + 1, 1) if (lambda c: c[0] > 200 and 50 < c[1] < 110 and c[2] < 60)(px(pg, im, x + 0.5, yy + 0.5))]
            ys = [yy for yy in range(int(q['y']), int(q['y'] + q['h']) + 1) for x in range(int(q['x']), int(q['x'] + q['w']) + 1, 1) if (lambda c: c[0] > 200 and 50 < c[1] < 110 and c[2] < 60)(px(pg, im, x + 0.5, yy + 0.5))]
            if xs and ys:
                g0, h0, cy = min(xs) - q['fin'], max(ys) - min(ys) + 1, (min(ys) + max(ys) + 1) / 2
                # ⚑ v183c (Tom, C-242 suite) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_cercle_plus_membres-avant-v183c.py) : 26 pt après la liste (8 avant) ;
                #   la hauteur d'encre = la hauteur de capitale de « Avec … » (le « A » de sa police rendue), son haut sur le haut des majuscules ; plus gras : la barre
                #   horizontale lue sur l'image fait au moins 0,26 de la hauteur (0,20 avant) ; la couleur ne change pas (#FB4C0D).
                mx = (min(xs) + max(xs)) // 2; colx = int(min(xs) + (max(xs) - min(xs)) * 0.18)
                ep = 0.25 * len([j for j in range(int(q['y']) * 4, int(q['y'] + q['h']) * 4 + 4) if (lambda c: c[0] > 200 and 50 < c[1] < 110 and c[2] < 60)(px(pg, im, colx + 0.5, j / 4 + 0.125))])   # au quart de point : à 0,79, le point entier ne voit pas le trait
                # ⚑ v186b (Tom, Q606 → C-254 suite) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_cercle_plus_membres-avant-v186b.py) : le + n'est plus au bout de la ligne
                #   « Avec … » mais à côté du dernier petit disque, centré sur lui — sa PLACE est jugée par redteam_plus_disque ; ici : son dessin (orange, haut d'une capitale
                #   de la ligne « Avec … », plus gras), sa zone de 44 pt prise à ses quatre coins.
                juge(T + ' A · le + : encre orange, haut d\'une capitale de la ligne « Avec … », plus gras, zone de 44 pt (sa place : redteam_plus_disque)',
                     abs(h0 - q['cap']) <= 1.5 and ep >= 0.26 * q['cap'] - 0.5 and abs(q['w'] - 44) <= .6 and all(q['coins']),
                     {'écart': round(g0, 1), 'hauteur': h0, 'capitale': round(q['cap'], 1), 'haut': min(ys), 'haut des capitales': round(q['capHaut'], 1), 'épaisseur': ep, 'coins': q['coins']})
            else: juge(T + ' A · le + : encre orange lue', False, q)
        else: juge(T + ' A · le + paraît après la liste des membres', False, q)
        # B
        pg.evaluate("()=>{ window.__sc=[]; const t0=performance.now(); (function f(){ const c=document.getElementById('dpdCorps'); window.__sc.push([performance.now()-t0, c?c.scrollTop:-1]); if(performance.now()-t0<1600) requestAnimationFrame(f); })(); }")
        B.tap_sel(pg, '#cerclePlusMembres'); pg.wait_for_timeout(1800)
        sc = pg.evaluate("()=>window.__sc"); st = pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, m=document.getElementById('npMemb'), g=m&&m.querySelector('.gn');
          return {ouv:document.getElementById('detailPoster').classList.contains('s2-ouv'), memb:m?(m.getBoundingClientRect().top-D.top)/k:null, gens:!!(g&&g.offsetHeight>40)}; }""")
        mv = [s for s in sc if s[1] > 0]; fin = sc[-1][1] if sc else 0
        bonds = max([sc[i + 1][1] - sc[i][1] for i in range(len(sc) - 1)] or [0])
        dur = (mv[-1][0] - next(s[0] for s in sc if s[1] > 0)) if mv else 0
        imgs = len({s[1] for s in mv})
        calme = B.charge() < 4
        juge(T + ' B · le toucher ouvre Peaufiner, MEMBRES déplié, glissement doux jusqu\'à MEMBRES (110 ± 4)' + ' [durée lue, non jugée au banc : ses images durent 50 à 70 ms]', st['ouv'] and st['gens'] and st['memb'] is not None and abs(st['memb'] - 110) <= 4 and imgs >= 8 and bonds <= fin / 6 + 1,
             {'membres': st['memb'] and round(st['memb'], 1), 'images': imgs, 'durée': round(dur), 'plus grand pas': round(bonds, 1), 'course': fin, 'liste': st['gens']})
        # C
        rc = pg.evaluate("""()=>{ const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return r.height?[r.top,r.bottom]:null; }; const m=R(document.getElementById('npMemb'));
          const autres=['npFich','npCercle','npDiss','npDesc','npTrait'].map(id=>[id,R(document.getElementById(id))]).filter(x=>x[1]&&x[1][0]<m[1]-1&&x[1][1]>m[0]+1);
          const a=document.querySelector('#npMemb .ph-add'); let doigt=null; if(a){ const r=a.getBoundingClientRect(); const pts=[[r.left+20,r.top+r.height/2],[r.left+r.width/2,r.top+r.height/2],[r.right-20,r.top+r.height/2]]; doigt=pts.map(p=>{ const e=document.elementFromPoint(p[0],p[1]); return !!(e&&e.closest&&e.closest('#npMemb')); }); }
          return {autres:autres, doigt:doigt}; }""")
        juge(T + ' C · rien ne recouvre MEMBRES déplié (cartes, bloc « Ma Parole ! », « + ajouter quelqu\'un » au doigt)', not rc['autres'] and rc['doigt'] and all(rc['doigt']), rc)
        # D
        pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} window._s2Ouvre(false); window._npGensOuvert=false; const d=document.getElementById('detailPoster'); d.scrollTop=0; }"); pg.wait_for_timeout(900)
        rep = pg.evaluate("()=>{ const L=document.querySelector('#dpNueeFil .nf-liste'); return L?(L.style.clipPath||''):'?'; }")
        mauvais = []; dmax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }")
        y = 0
        while True:
            y = min(y + 30, dmax)
            pg.evaluate("y=>{ document.getElementById('detailPoster').scrollTop=y; }", y)
            pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            im = image(pg); lt = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, L=document.querySelector('#dpNueeFil .nf-liste'); return (L.getBoundingClientRect().top-D.top)/k; }")
            for yy in ((101, 104, 107, 110) if lt <= 100 else ()):   # la bande ne porte que le fil quand le haut du fil est passé au-dessus d'elle (au-dessus, la Toile, les Noyaux, le titre défilent : hors de C-243)
                row = [px(pg, im, x, yy) for x in range(30, 361, 6)]
                med = [sorted(c[i] for c in row)[len(row) // 2] for i in range(3)]
                dev = max(max(abs(c[i] - med[i]) for i in range(3)) for c in row)
                if dev > 14: mauvais.append((y, yy, dev)); break
            vis = pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const L=document.querySelector('#dpNueeFil .nf-liste'); const b=document.getElementById('cerclePlusMembres');
              const cs=[...document.querySelectorAll('#dpNueeFil .nf-liste > *')]; let haut=1e9; for(const c of cs){ const r=c.getBoundingClientRect(); if(!r.height) continue; for(let yy=r.top+1; yy<Math.min(r.bottom,D.top+112*k); yy+=3){ const e=document.elementFromPoint(r.left+r.width/2, yy); if(e&&c.contains(e)){ haut=Math.min(haut,(yy-D.top)/k); break; } } }
              const bv=b&&getComputedStyle(b).display!=='none'&&getComputedStyle(b).visibility!=='hidden'?(b.getBoundingClientRect().top-D.top)/k:null; return {haut:haut, plus:bv}; }""")
            if vis['haut'] < 112: mauvais.append((y, 'carte au doigt à', round(vis['haut'], 1)))
            if vis['plus'] is not None and vis['plus'] + 11 < 112: mauvais.append((y, '+ sous l\'encart', round(vis['plus'], 1)))
            if y >= dmax: break
        juge(T + ' D · défilé jusqu\'en bas : rien du fil ni le + sous l\'encart (image et doigt) ; au repos rien n\'est rogné', not mauvais and rep == '', {'repos': rep, 'défauts': mauvais[:4], 'course': dmax})
        pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2600)
        CART = "()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [...document.querySelectorAll('#dpNueeFil .nf-liste > *')].filter(c=>c.getBoundingClientRect().height>20).map(c=>(c.getBoundingClientRect().top-D.top)/k); }"
        dmax = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; }"); sauts = []; prev = pg.evaluate(CART); y = 0
        seq = list(range(6, int(dmax) + 1, 6)) + list(range(int(dmax) - 6, -1, -6))
        for yy in seq:
            pg.evaluate("y=>{ document.getElementById('detailPoster').scrollTop=y; }", yy)
            pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            cur = pg.evaluate(CART); dy = yy - y
            if len(cur) != len(prev): sauts.append((yy, 'cartes', len(prev), len(cur)))
            else:
                for a_, b_ in zip(prev, cur):
                    if abs((a_ - b_) - dy) > 1: sauts.append((yy, round(a_ - b_, 1), dy)); break
            prev, y = cur, yy
        juge(T + ' F · défilé de 6 en 6 pt, aller et retour : chaque carte suit le pas, aucun saut', not sauts and dmax > 30, {'course': dmax, 'sauts': sauts[:4]})
        juge(T + ' E · aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
