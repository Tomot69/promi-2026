#!/usr/bin/env python3
"""redteam_cercle_plus_membres.py — ⚑ v181a (Tom, 6 nov. 2026) — LA FICHE D'UN CERCLE.
C-242 : « un + à droite du disque du Cercle, aligné à droite ; un toucher ouvre Peaufiner directement sur MEMBRES, en glissement doux, les membres bien
espacés ; mêmes codes que les autres + (orange #FB4C0D, zone de toucher de 44 pt) ».
C-243 : « le haut du fil passe sous l'en-tête (CERCLE et X) : aucun recouvrement entre le fil et l'en-tête, en haut et pendant le défilement ».

Banc WebKit ×3, le Cercle « Le potager » (six paroles), 430 × 932 (échelle 1) et 330 × 714 (0,79) :
  A · le + paraît : son encre orange #FB4C0D (lue sur l'image), son bord droit à 366 pt ± 1, centré sur le disque du Cercle ± 1,5 ; sa zone de 44 pt (les
      quatre coins, 2 pt en dedans, rendent le bouton au doigt) ;
  B · un toucher au doigt : Peaufiner s'ouvre, MEMBRES déplié (la liste des personnes visible) ; le panneau GLISSE (au moins 8 images de défilement, aucun
      pas de plus d'un sixième de la course — le pas le plus long de la courbe prévue, à 34 ms par image ; la durée — 420 ms prévus — se lit dans Safari : les images du banc durent 50 à 70 ms) jusqu'à MEMBRES à 110 pt ± 4 ;
  C · les membres bien espacés : aucune carte, ni le bloc « Ma Parole ! », ne recouvre la carte MEMBRES dépliée (rectangles, et au doigt sur
      « + ajouter quelqu'un ») ;
  D · le fil défilé par pas de 30 pt jusqu'en bas, lu image par image : aucune carte du fil au-dessus de 112 pt (12 pt sous l'encart), la bande 101 → 111 pt
      unie (lue sur l'image) ; au repos (défilement 0) rien n'est rogné ; le + ne paraît jamais sous l'encart ;
  E · aucune erreur de page.
Rouge sur v180b (`--fichier=zz-v180b.html`) : A, B, C, D.
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
  const w=[...document.querySelectorAll('#dAura .kring .kr-wrap')][1].getBoundingClientRect();
  const coins=[[r.left+2,r.top+2],[r.right-2,r.top+2],[r.left+2,r.bottom-2],[r.right-2,r.bottom-2]].map(p=>{ const e=document.elementFromPoint(p[0],p[1]); return !!(e&&e.closest&&e.closest('#cerclePlusMembres')); });
  return {vu:true, x:(r.left-D.left)/k, y:(r.top-D.top)/k, w:r.width/k, h:r.height/k, disque:(w.top+w.height/2-D.top)/k, coins:coins}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        T = '[×%s]' % nom
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)
        pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2800)
        q = pg.evaluate(BTN)
        if q and q.get('vu'):
            im = image(pg)
            enc = [x for x in range(int(q['x']), int(q['x'] + q['w'])) if (lambda c: c[0] > 200 and 50 < c[1] < 110 and c[2] < 60)(px(pg, im, x + 0.5, q['disque']))]
            droit = max(enc) + 1 if enc else None
            juge(T + ' A · le + : encre orange, bord droit 366 ± 1, centré sur le disque du Cercle, zone de 44 pt', enc and abs(droit - 366) <= 1.2 and abs(q['y'] + 22 - q['disque']) <= 1.5 and abs(q['w'] - 44) <= .6 and all(q['coins']),
                 {'droit': droit, 'centre': round(q['y'] + 22, 1), 'disque': round(q['disque'], 1), 'w': round(q['w'], 1), 'coins': q['coins']})
        else: juge(T + ' A · le + paraît à droite du disque du Cercle', False, q)
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
        juge(T + ' E · aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
