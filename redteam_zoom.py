#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_zoom.py — LE ZOOM DE LA TOILE, AU DOIGT (CDP, pincement réel). Réécrit le 24 sept. 2026 (v46) au niveau de la décision
de Tom — « zoomer et dézoomer comme une photo sur iPhone ; dézoomer jusqu'à voir la Toile entière, les encarts s'effacent ;
le zoom persiste d'une page à l'autre et ne revient au défaut qu'à la fermeture, à la création ou à la suppression d'une
dalle ; un double toucher ramène au défaut, qui dépend du nombre de dalles ».
Deux règles de la version d'avant sont RENVERSÉES par cette décision : « le dézoom tient à 0,40 » (le plancher est la Toile
entière, 0,72) et « planter ne reprend pas la vue posée » (planter ramène le défaut). Original : sauvegardes/redteam_zoom-avant-v46.py.
Les valeurs décidées sont écrites EN DUR (§7) : ZMIN 0,72 · ZMAX 5 · défaut(n) = n ≥ 20 → 1 (v47, Tom : « la Toile prend tout l'écran par défaut » ; v46 disait max(0,90 ; 1 − (n − 20) × 0,005)).

  1 · DÉZOOM : pincé loin, relâché → 0,72 ; la Toile ENTIÈRE dans l'écran ; les encarts effacés et hors du doigt
  2 · LE ZOOM PERSISTE : une fiche, puis l'Index, ouverts et fermés → la vue ne bouge pas
  3 · LE ROND « recadrer » apparaît quand la main a posé la vue
  4 · ZOOM AVANT : pincé au-delà, relâché → 5 (l'élastique revient à la borne)
  5 · LE DOUBLE TOUCHER, SUR UNE DALLE, ramène au défaut et n'ouvre pas de fiche
  6 · UN TOUCHER SIMPLE sur une dalle ouvre sa fiche
  7 · PLANTER ramène le zoom par défaut
  8 · SUPPRIMER ramène le zoom par défaut
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_ZOOM', "http://127.0.0.1:8752/app.html")
ZMIN, ZMAX = 0.72, 5.0
def DEFAUT(n): return 1.0 if n >= 20 else None   # v47 (Tom) : le défaut est le plein écran, jamais dézoomé
ok = [0]; ko = []
def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-62s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-62s KO  %s' % (nom, detail))

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);}", th)
        pg.wait_for_timeout(1500)
        cdp = ctx.new_cdp_session(pg)
        D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
        dev = lambda x, y: (D[0] + x * D[2], D[1] + y * D[2])
        vue = lambda: pg.evaluate("()=>Toile.vue()")
        nb = lambda: pg.evaluate("()=>Toile.count()")
        rond = lambda: pg.evaluate("()=>{const r=document.getElementById('accRecadre');return !!r&&getComputedStyle(r).display!=='none';}")
        def touche(x, y):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        def pince(d0, d1):
            cx, cy = dev(195, 440)
            def ev(tp, d):
                pts = [] if tp == 'touchEnd' else [{'x': cx - d / 2, 'y': cy, 'id': 1}, {'x': cx + d / 2, 'y': cy, 'id': 2}]
                cdp.send('Input.dispatchTouchEvent', {'type': tp, 'touchPoints': pts})
            ev('touchStart', d0)
            for i in range(1, 15): ev('touchMove', d0 + (d1 - d0) * i / 14); pg.wait_for_timeout(16)
            ev('touchEnd', d1)
        # 1 · dézoom
        pince(320 * D[2], 40 * D[2]); pg.wait_for_timeout(1800)
        v1 = vue()
        entiere = v1['ox'] >= -0.5 and v1['oy'] >= -0.5 and v1['ox'] + 390 * v1['s'] <= 390.5
        enc = pg.evaluate("()=>['accPlat','accBarre'].map(i=>{const e=document.getElementById(i),c=getComputedStyle(e);return [+c.opacity,c.visibility,c.pointerEvents];})")
        efface = all(o < 0.05 or v == 'hidden' for o, v, _ in enc)
        t('[%s] 1 · dézoom relâché à %.2f, Toile entière, encarts effacés' % (T, ZMIN), abs(v1['s'] - ZMIN) < 0.01 and entiere and efface, 'échelle %.3f · entière %s · encarts %s' % (v1['s'], entiere, enc))

        # 2 · persistance
        pid = pg.evaluate("()=>promises.find(q=>!q.draft&&!q.req).id")
        pg.evaluate("(i)=>openDetail(i)", pid); pg.wait_for_timeout(1300); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const b=document.getElementById('indexBtn'); if(b) b.click();}"); pg.wait_for_timeout(1300); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1500)
        v2 = vue()
        t('[%s] 2 · le zoom persiste (fiche, Index)' % T, abs(v2['s'] - v1['s']) < 0.005 and abs(v2['ox'] - v1['ox']) < 0.5, '%.3f → %.3f' % (v1['s'], v2['s']))
        # 4 · zoom avant
        pince(40 * D[2], 330 * D[2]); pg.wait_for_timeout(400); pince(40 * D[2], 330 * D[2]); pg.wait_for_timeout(400); pince(40 * D[2], 330 * D[2]); pg.wait_for_timeout(2000)
        v4 = vue()
        t('[%s] 4 · zoom avant : l\'élastique revient à %g' % (T, ZMAX), abs(v4['s'] - ZMAX) < 0.01, 'échelle %.3f' % v4['s'])
        # ⚑ assainissement (30 sept.) : le rond se lit À L'ÉCRAN (visible, dans l'appareil), plus dans l'état `_vueMain` que l'app déclare.
        #   Et il se juge quand la main a posé la vue ET que les encarts sont là : à la Toile ENTIÈRE, tous les encarts s'effacent,
        #   le rond compris (`toile-entiere`) — l'ancien contrôle le déclarait « là » à ce moment précis, en lisant l'état : il passait
        #   À VIDE. Original : sauvegardes/redteam_zoom-avant-assainissement.py
        t('[%s] 3 · le rond « recadrer » est là' % T, pg.evaluate("""()=>{const e=document.getElementById('accRecadre'); if(!e) return false;
            const r=e.getBoundingClientRect(), s=getComputedStyle(e), d=document.getElementById('device').getBoundingClientRect();
            return r.width>8 && s.display!=='none' && s.visibility!=='hidden' && +s.opacity>0.5 && r.left>=d.left && r.right<=d.right && r.top>=d.top && r.bottom<=d.bottom; }"""), '')
        # 5 · double toucher sur une dalle
        pince(330 * D[2], 99 * D[2]); pg.wait_for_timeout(1800)   # ×1,5 : des dalles entières dans l'écran
        cible = pg.evaluate("""()=>{const v=Toile.vue();const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
            for(const p of promises.filter(q=>!q.draft&&!q.req)){ const a=Toile.dalleAbs(p.id); if(!a) continue; const sx=v.ox+v.s*(a.minx+a.w/2), sy=v.oy+v.s*(a.miny+a.h/2);
              if(sx<20||sx>370||sy<150||sy>700) continue; const h=Toile.hit(sx,sy); if(!h||h.pid!==p.id) continue; const X=r.left+sx*k, Y=r.top+sy*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv') return [X,Y,p.id]; } return null;}""")
        if cible:
            touche(cible[0], cible[1]); pg.wait_for_timeout(110); touche(cible[0], cible[1]); pg.wait_for_timeout(2500)
        v5 = vue(); n5 = nb(); d5 = DEFAUT(n5)
        fiche5 = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        t('[%s] 5 · double toucher sur une dalle → défaut, pas de fiche' % T, bool(cible) and d5 is not None and abs(v5['s'] - d5) < 0.01 and not fiche5, 'échelle %.3f (défaut %s pour %d) · fiche %s' % (v5['s'], d5, n5, fiche5))
        # 6 · toucher simple
        cible = pg.evaluate("""()=>{const v=Toile.vue();const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
            for(const p of promises.filter(q=>!q.draft&&!q.req)){ const a=Toile.dalleAbs(p.id); if(!a) continue; const sx=v.ox+v.s*(a.minx+a.w/2), sy=v.oy+v.s*(a.miny+a.h/2);
              if(sx<20||sx>370||sy<150||sy>700) continue; const h=Toile.hit(sx,sy); if(!h||h.pid!==p.id) continue; const X=r.left+sx*k, Y=r.top+sy*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv') return [X,Y,p.id]; } return null;}""")
        if cible:
            touche(cible[0], cible[1]); pg.wait_for_timeout(1200)
        ouvre = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        t('[%s] 6 · un toucher simple ouvre la fiche' % T, bool(cible) and ouvre, 'dalle %s · fiche %s' % (cible and cible[2], ouvre))
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1200)
        # 7 · planter
        pince(300 * D[2], 90 * D[2]); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const q=P('juge zoom','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);}"); pg.wait_for_timeout(2800)
        v7 = vue(); n7 = nb(); d7 = DEFAUT(n7)
        t('[%s] 7 · planter ramène le défaut' % T, d7 is not None and abs(v7['s'] - d7) < 0.01, 'échelle %.3f (défaut %s pour %d)' % (v7['s'], d7, n7))
        # 8 · supprimer
        pince(300 * D[2], 90 * D[2]); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{ const ids=promises.filter(q=>!q.draft).map(q=>q.id); Toile.sync(ids.slice(0,-1)); }"); pg.wait_for_timeout(2800)
        v8 = vue(); n8 = nb(); d8 = DEFAUT(n8)
        t('[%s] 8 · supprimer ramène le défaut' % T, d8 is not None and abs(v8['s'] - d8) < 0.01, 'échelle %.3f (défaut %s pour %d)' % (v8['s'], d8, n8))
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
