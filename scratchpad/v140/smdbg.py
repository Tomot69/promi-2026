#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_studio_mur.py — AU STUDIO, LA PHRASE DU MUR PARAÎT SUR LE FLOU TOUCHÉ (v140, Tom, 10 oct. 2026, C-092).

« Quand on touche une zone floutée du Studio (le choix des palettes, avec son texte), la phrase de Ma Parole ! apparaît en haut de
l'écran au lieu d'apparaître sur la zone floutée, en bas. Elle doit paraître sur le flou touché, lisible. Vérifie tous les murs du Studio. »

Chromium, au vrai doigt (CDP), gratuit, sur un monde de Ma Parole ! (on y glisse depuis Pochade). Pour CHAQUE mur du Studio — les tons,
les libellés, les disques, les barrettes ; puis, le panneau des palettes ouvert, les pastilles, le nom, la jauge — un toucher :
  · la phrase paraît ;
  · elle est ENTIÈRE dans le panneau flouté (la réunion des zones floutées, à 6 pt près) — jamais sur le nom du monde ni sur le plateau ;
  · le point touché est flouté (un filtre de flou sur lui ou un ancêtre).
Preuve : rouge sur l'état d'avant (python3 redteam_studio_mur.py zz-av140.html).
"""
import sys, json
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
REL = """([x,y])=>{ const D=document.getElementById('device').getBoundingClientRect(), st=document.getElementById('studioScreen'); let u=null;
  st.querySelectorAll('#stpTons,#stpLab,#stpVue,#stpDots,#stpPals').forEach(e=>{ const f=getComputedStyle(e).filter, r=e.getBoundingClientRect(); if(f&&f.indexOf('blur')>=0&&r.width>4&&r.height>1){ u=u?[Math.min(u[0],r.top-D.top),Math.max(u[1],r.bottom-D.top)]:[r.top-D.top,r.bottom-D.top]; } });
  let fl=false; for(let e=document.elementFromPoint(D.left+x,D.top+y); e&&e.id!=='device'; e=e.parentElement){ const f=getComputedStyle(e).filter; if(f&&f.indexOf('blur')>=0&&e.id!=='stBg'){ fl=true; break; } }
  if(!fl){ st.querySelectorAll('#stpTons,#stpLab,#stpVue,#stpDots,#stpPals').forEach(e=>{ const f=getComputedStyle(e).filter, r=e.getBoundingClientRect(); if(f&&f.indexOf('blur')>=0&&D.left+x>=r.left&&D.left+x<=r.right&&D.top+y>=r.top-2&&D.top+y<=r.bottom+2) fl=true; }); }
  const m=document.getElementById('murPhrase'); let ph=null; if(m&&m.classList.contains('leve')){ const r=m.getBoundingClientRect(); ph=[r.top-D.top, r.bottom-D.top]; }
  return {zone:u, phrase:ph, flou:fl, offre:!!document.querySelector('#cercleScreen.show')}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    def session(pals):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now()}));}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(6000)
        d = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
        def tap(x, y):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': d['x'] + x, 'y': d['y'] + y}]}); pg.wait_for_timeout(60); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        def glisse():
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': d['x'] + 320, 'y': d['y'] + 300}]})
            for i in range(1, 11): pg.wait_for_timeout(16); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': d['x'] + 320 - i * 24, 'y': d['y'] + 300}]})
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1500)
        if pals: tap(75, 620); pg.wait_for_timeout(1500)
        for k in range(14):
            glisse()
            if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
        pg.wait_for_timeout(2500)
        return ctx, pg, tap
    ctx, pg, tap = session(False)
    E="()=>{const m=document.getElementById('murPhrase'); return [document.getElementById('studioScreen').className, m?m.className:null, m?getComputedStyle(m).display:null, [].map.call(document.querySelectorAll('.screen.show,.sheet.show'),e=>e.id), localStorage.getItem('promi_murs')]}"
    print(pg.evaluate(E)); tap(75,620); pg.wait_for_timeout(700); print(pg.evaluate(E))
    for i in range(8): pg.wait_for_timeout(1000); print(i, pg.evaluate(E))
    tap(110,671); pg.wait_for_timeout(700); print(pg.evaluate(E)); pg.wait_for_timeout(1500); print(pg.evaluate(E))
    b.close()
