#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accueil_audit2.py — (1) la friction pour planter chaque nature depuis l'accueil, au doigt ;
(2) l'atteignabilité des dalles quand la Toile est pleine (n ≥ 20 : cadrage automatique = Toile entière)."""
import json
from playwright.sync_api import sync_playwright
exec(open('scratchpad/accueil_audit.py').read().split('CMDS = [')[0])  # INV_JS, MASK_JS, REACH_JS
APP = "http://127.0.0.1:8752/app.html"
OUT = {}
VIS = r"""(sel)=>[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect();const c=getComputedStyle(e);return r.width>4&&r.height>4&&c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>0.05;}).map(e=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390,r=e.getBoundingClientRect();return {t:(e.innerText||'').trim().slice(0,40),k:e.dataset.kind||'',x:+((r.left-D.left)/k).toFixed(0),y:+((r.top-D.top)/k).toFixed(0),w:+(r.width/k).toFixed(0),h:+(r.height/k).toFixed(0)};})"""
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.wait_for_timeout(800)
    D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
    clip = {'x': D[0], 'y': D[1], 'width': 390*D[2], 'height': 844*D[2]}
    F = OUT['friction'] = {}
    pg.locator('#createBtn').tap(); pg.wait_for_timeout(1400)
    F['apres_plus'] = {'tuiles': pg.evaluate(VIS, '#createSheet .tile'), 'kind': pg.evaluate("()=>document.getElementById('createSheet').dataset.kind"),
                       'phrase_visible': pg.evaluate(VIS, '#csPhrase'), 'classes': pg.evaluate("()=>document.getElementById('createSheet').className")}
    pg.screenshot(path='scratchpad/acc_plus_1.png', clip=clip)
    for kind in ['promi', 'chiche', 'nuee']:
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(700)
        pg.locator('#createBtn').tap(); pg.wait_for_timeout(1400)
        tl = pg.evaluate(VIS, '#createSheet .tile[data-kind=%s]' % kind)
        F[kind] = {'tuile_visible_sans_glisser': tl}
        if not tl:
            # glisser la piste
            for i in range(3):
                pg.evaluate("()=>{}")
                x0, y0 = D[0] + 300*D[2], D[1] + 400*D[2]
                cdp = ctx.new_cdp_session(pg)
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]})
                for s in range(1, 10):
                    cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 - 22*s*D[2], 'y': y0}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
                pg.wait_for_timeout(700)
                tl = pg.evaluate(VIS, '#createSheet .tile[data-kind=%s]' % kind)
                if tl and 20 < tl[0]['x'] < 200: break
            F[kind]['glisses'] = i + 1; F[kind]['tuile'] = tl
        try:
            pg.locator('#createSheet .tile[data-kind=%s]' % kind).first.tap(timeout=3000, force=True)
        except Exception as e:
            F[kind]['erreur'] = str(e)[:100]
        pg.wait_for_timeout(1300)
        F[kind]['apres_tuile'] = {'kind': pg.evaluate("()=>document.getElementById('createSheet').dataset.kind"),
                                  'phrase': pg.evaluate(VIS, '#csPhrase .ph-pill, #csPhrase [data-slot], #csPhrase')[:6],
                                  'focus': pg.evaluate("()=>document.activeElement&&(document.activeElement.id||document.activeElement.tagName)")}
        pg.screenshot(path='scratchpad/acc_plus_%s.png' % kind, clip=clip)
    pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800)
    # (2) Toile pleine
    for n in [30, 60]:
        pg.evaluate("""(n)=>{const base=promises.filter(p=>!p.draft&&!p.req);let k=0;
            while(promises.filter(p=>!p.draft&&!p.req).length<n){const s=base[k++%base.length];const c=JSON.parse(JSON.stringify(s));c.id=nid++;c.title=(s.title||'')+' ·'+c.id;promises.push(c);}
            Toile.sync(promises.filter(p=>!p.draft&&!p.req).map(p=>p.id)); if(window.caption)caption();}""", n)
        pg.wait_for_timeout(5000)
        m = pg.evaluate(MASK_JS)
        A = pg.evaluate(REACH_JS, [m['rows'], [0.48, 0.6, 0.8, 0.9, 1.0, 1.25, 1.5, 2, 3, 5]])
        OUT['plein_%d' % n] = {'vue': A['v0'], 'sansPoly': len(A['sansPoly']), 'zooms': {s: {'n': z['n'], 'inatteignables': len(z['inatteignables']), 'ids': z['inatteignables'], 'sansDeplacer': len(z['sansDeplacer'])} for s, z in A['zooms'].items()}}
        pg.screenshot(path='scratchpad/acc_plein_%d.png' % n, clip=clip)
    b.close()
json.dump(OUT, open('scratchpad/accueil_audit2.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(OUT, ensure_ascii=False, indent=1)[:6000])
