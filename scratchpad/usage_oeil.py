#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage_oeil.py — LE PASSAGE D'USAGE À L'ŒIL.

Celui qui avait produit CASSE.md : on plante, on remplit, on touche, on enchaîne, dans les
deux thèmes, et ON REGARDE. Les chiffres disent que tout est vert ; ce script fabrique les
images qui disent s'ils disent vrai. Il n'affirme rien : il joue un parcours et capture.
"""
import os
import sys
from playwright.sync_api import sync_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else 'scratchpad/usage'
os.makedirs(OUT, exist_ok=True)
APP = "http://127.0.0.1:8752/app.html"


def geste(pg, sel):
    r = pg.evaluate("(s)=>{const e=document.querySelector(s);if(!e)return null;"
                    "const b=e.getBoundingClientRect();if(b.width<10)return null;"
                    "return {x:b.x,y:b.y,w:b.width,h:b.height};}", sel)
    if not r:
        return False
    yy = r['y'] + r['h'] / 2
    pg.mouse.move(r['x'] + 12, yy)
    pg.mouse.down()
    for i in range(1, 26):
        pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, yy + (6 if i % 2 else -6))
        pg.wait_for_timeout(12)
    pg.mouse.up()
    pg.wait_for_timeout(1400)
    return True


with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        er = []
        pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>setTheme(t)", th)
        pg.wait_for_timeout(400)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        n = [0]

        def shot(nom):
            n[0] += 1
            pg.query_selector('#device').screenshot(
                path=os.path.join(OUT, '%s_%02d_%s.png' % (th, n[0], nom)))

        shot('toile')
        # ── 1 · planter ──
        pg.evaluate("()=>document.getElementById('createBtn').click()")
        pg.wait_for_timeout(900)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];if(x)x.click();}")
        pg.wait_for_timeout(1100)
        shot('page-plus')
        pg.evaluate("""()=>{const f=document.getElementById('fTitle');
          if(f){f.value='aller voir la mer'; f.dispatchEvent(new Event('input',{bubbles:true}));}
          if(window._phrase){window._phrase.titre='aller voir la mer';
            if(window._phraseRendu)_phraseRendu();}}""")
        pg.wait_for_timeout(700)
        shot('page-plus-remplie')
        n0 = pg.evaluate("()=>promises.length")
        geste(pg, '#planterCv')
        n1 = pg.evaluate("()=>promises.length")
        shot('apres-plantation')
        print(th, 'planté :', n0, '->', n1)
        # ── 2 · la fiche, un mot, le geste ──
        pid = pg.evaluate("()=>{const p=promises[promises.length-1]; if(p)p.status='rate'; return p?p.id:null;}")
        pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid)
        pg.wait_for_timeout(1500)
        shot('fiche')
        pg.evaluate("""()=>{const i=document.querySelector('#detailPoster input');
          if(i){i.value='elles étaient bonnes'; i.dispatchEvent(new Event('input',{bubbles:true}));}}""")
        pg.wait_for_timeout(600)
        shot('fiche-mot')
        geste(pg, '#tenirCv')
        st = pg.evaluate("(i)=>{const p=promises.find(x=>x.id===i);return p?p.status:null;}", pid)
        shot('fiche-tenue')
        print(th, 'tenue au geste :', st)
        # ── 3 · Peaufiner ──
        pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t)t.click();}")
        pg.wait_for_timeout(1300)
        shot('peaufiner')
        pg.evaluate("()=>{const c=document.querySelector('#detailPoster .dpd-corps'); if(c)c.scrollTop=660;}")
        pg.wait_for_timeout(700)
        shot('peaufiner-bas')
        # ── 4 · Index, Fil ──
        pg.evaluate("()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex();}")
        pg.wait_for_timeout(1800)
        shot('index')
        pg.evaluate("()=>{if(window.closeAll)closeAll(); setView('fil');}")
        pg.wait_for_timeout(1800)
        shot('fil')
        # ── 5 · la Nuée, son Peaufiner, son défilé ──
        pg.evaluate("()=>{if(window.closeAll)closeAll(); const k=Object.keys(NUE)[0]; if(k)openEssaim(k);}")
        pg.wait_for_timeout(1900)
        shot('nuee')
        pg.evaluate("()=>{if(window._nueeDefile)window._nueeDefile(true);}")
        pg.wait_for_timeout(1000)
        shot('nuee-defile')
        pg.evaluate("()=>{if(window._nueeDefile)window._nueeDefile(false);}")
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t)t.click();}")
        pg.wait_for_timeout(1300)
        shot('nuee-peaufiner')
        pg.evaluate("()=>{const c=document.getElementById('dpdCorps'); if(c)c.scrollTop=760;}")
        pg.wait_for_timeout(700)
        shot('nuee-peaufiner-p2')
        print(th, 'erreurs JS :', er[:3])
        pg.close()
    b.close()
print('captures dans', OUT)
