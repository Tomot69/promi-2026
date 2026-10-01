#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_zoom.py — LE ZOOM DE LA TOILE TIENT (Q212, Tom 13 sept. 2026). AU DOIGT (CDP, pincement réel).

  1 · LE DÉZOOM TIENT — pincé à 0,40, relâché, 1,5 s puis une fiche ouverte et fermée : la vue reste à 0,40 (plus de ressort à 0,48)
  2 · PLANTER NE REPREND PAS UNE VUE POSÉE PAR LA MAIN — après `Toile.addPromi`, l'échelle ne revient pas au cadrage
  3 · LE ROND « RECADRER » N'EXISTE QU'AU BESOIN — absent au repos, absent après un simple toucher, présent après un pincement
  4 · RECADRER RAMÈNE AU CADRAGE DE DÉPART — le rond (au doigt) remet la vue au cadrage automatique et disparaît
  5 · LE DOUBLE TOUCHER SUR UNE CASE VIDE RECADRE AUSSI
  6 · UN TOUCHER SUR UNE DALLE OUVRE TOUJOURS SA FICHE (le double toucher ne vole rien)

Preuve (§7) : `APP_ZOOM=http://127.0.0.1:8752/sauvegardes/app-avant-lot-zoom.html` doit ROUGIR.
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_ZOOM', "http://127.0.0.1:8752/app.html")
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-58s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-58s KO  %s' % (nom, detail))


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
        rond = lambda: pg.evaluate("()=>{const r=document.getElementById('accRecadre');return !!r&&getComputedStyle(r).display!=='none';}")

        def touche(x, y, duree=0):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
            if duree: pg.wait_for_timeout(duree)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

        def pince(d0, d1):
            cx, cy = dev(195, 440)
            def ev(tp, d):
                pts = [] if tp == 'touchEnd' else [{'x': cx - d / 2, 'y': cy, 'id': 1}, {'x': cx + d / 2, 'y': cy, 'id': 2}]
                cdp.send('Input.dispatchTouchEvent', {'type': tp, 'touchPoints': pts})
            ev('touchStart', d0)
            for i in range(1, 15): ev('touchMove', d0 + (d1 - d0) * i / 14)
            ev('touchEnd', d1)

        t('[%s] 3 · pas de rond « recadrer » au repos' % T, not rond(), '')
        # un toucher sur une case vide, loin des dalles
        vide = pg.evaluate("""()=>{const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
            for(let y=200;y<700;y+=17)for(let x=30;x<360;x+=17){ if(!Toile.hit(x,y)){ const e=document.elementFromPoint(r.left+x*k,r.top+y*k); if(e&&e.id==='toileCv') return [r.left+x*k,r.top+y*k]; } } return null;}""")
        if vide:
            touche(*vide); pg.wait_for_timeout(700)
        t('[%s] 3 · pas de rond après un simple toucher' % T, not rond(), 'case vide %s' % bool(vide))
        pince(300 * D[2], 60 * D[2]); pg.wait_for_timeout(1500)
        v1 = vue()
        t('[%s] 3 · le rond apparaît après un pincement' % T, rond(), 'échelle %.2f' % v1['s'])
        # 1 · le dézoom tient
        pid = pg.evaluate("()=>{const p=promises.find(q=>!q.draft&&!q.req);return p.id;}")
        pg.evaluate("(i)=>openDetail(i)", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1800)
        v2 = vue()
        t('[%s] 1 · le dézoom tient à 0,40 (relâché, fiche ouverte et fermée)' % T, abs(v1['s'] - 0.40) < 0.02 and abs(v2['s'] - 0.40) < 0.02, '%.2f → %.2f' % (v1['s'], v2['s']))
        # 2 · planter
        pg.evaluate("()=>{const q=P('juge zoom','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);}")
        pg.wait_for_timeout(2500)
        v3 = vue()
        t('[%s] 2 · planter ne reprend pas la vue posée' % T, abs(v3['s'] - v2['s']) < 0.02, '%.2f → %.2f' % (v2['s'], v3['s']))
        # 4 · le rond, au doigt
        pt = pg.evaluate("()=>{const r=document.getElementById('accRecadre');if(!r)return null;const b=r.getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2];}")
        if pt:
            touche(*pt); pg.wait_for_timeout(2500)
        v4 = vue()
        att = pg.evaluate("()=>{ window._vueMain=false; window._recadreDemande=true; return 1; }")  # rien : on compare au cadrage calculé ci-dessous
        t('[%s] 4 · recadrer ramène au cadrage et le rond disparaît' % T, bool(pt) and v4['s'] >= 0.99 and not rond(), 'échelle %.2f · rond %s' % (v4['s'], rond()))
        # 5 · double toucher sur une case vide
        pince(300 * D[2], 90 * D[2]); pg.wait_for_timeout(1500)
        vide2 = pg.evaluate("""()=>{const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
            for(let y=150;y<720;y+=11)for(let x=20;x<370;x+=11){ if(!Toile.hit(x,y)){ const e=document.elementFromPoint(r.left+x*k,r.top+y*k); if(e&&e.id==='toileCv') return [r.left+x*k,r.top+y*k]; } } return null;}""")
        if vide2:
            touche(*vide2); pg.wait_for_timeout(120); touche(*vide2); pg.wait_for_timeout(2500)
        v5 = vue()
        t('[%s] 5 · le double toucher sur une case vide recadre' % T, bool(vide2) and v5['s'] >= 0.99, 'échelle %.2f' % v5['s'])
        # 6 · un toucher sur une dalle ouvre sa fiche
        cible = pg.evaluate("""()=>{const v=Toile.vue();const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
            for(const p of promises.filter(q=>!q.draft&&!q.req)){ const a=Toile.dalleAbs(p.id); if(!a) continue; const sx=v.ox+v.s*(a.minx+a.w/2), sy=v.oy+v.s*(a.miny+a.h/2);
              const h=Toile.hit(sx,sy); if(!h||h.pid!==p.id) continue; const X=r.left+sx*k, Y=r.top+sy*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv') return [X,Y,p.id]; } return null;}""")
        if cible:
            touche(cible[0], cible[1]); pg.wait_for_timeout(1500)
        ouvre = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        t('[%s] 6 · un toucher sur une dalle ouvre sa fiche' % T, bool(cible) and ouvre, 'dalle %s · fiche %s' % (cible and cible[2], ouvre))
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
