#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_flash_etat.py — PAS DE FLASH ORANGE À L'OUVERTURE D'UNE FICHE « À TENIR » EN SOMBRE (v122, Tom, Q374, 3 oct. 2026).

« À l'ouverture d'une fiche « à tenir » en sombre, l'à-qui, l'échéance et « trace pour tenir » restent 1 à 2 s en orange avant de passer à
la crème. La couleur finale doit être posée dès la première image. Juge : vingt ouvertures, avec une capture à la première image, et aucun
orange sur ces trois éléments. »

Valeurs EN DUR (§7) : la crème #F7F0DE = rgb(247, 240, 222) (décision v16 / Q290 : les textes d'état sur fond sombre passent crème) ;
l'orange d'état #DD4D23 = rgb(221, 77, 35).
Pour chacune des vingt ouvertures (WebKit, sombre, « faire les crêpes ») :
  1 · dans la page, à CHAQUE image depuis `openDetail` jusqu'à 1,5 s, la couleur calculée des trois éléments : aucune n'est l'orange, et la
      première image où ils paraissent les montre déjà crème ;
  2 · une capture prise dès que la fiche paraît : dans le rectangle de chacun des trois éléments, aucun pixel proche de l'orange (ΔRVB ≤ 40).
Preuve (§7) : sur `sauvegardes/app-avant-v122.html` il ROUGIT (orange de ~400 ms à ~1 s, à chaque ouverture).
"""
import os, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image

FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = 20
CREME, ORANGE = 'rgb(247, 240, 222)', 'rgb(221, 77, 35)'
IDS = ['dptQui', 'dptQuand', 'dptTrace']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-74s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


SUIT = r"""(ids)=>new Promise(res=>{ const t0=performance.now(), vu=[]; let premiere=null;
  const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);
  function f(){ const dp=document.getElementById('detailPoster'); const r={t:(performance.now()-t0)|0, c:{}};
    let paru=dp && dp.classList.contains('show') && +getComputedStyle(dp).opacity>0.05;
    ids.forEach(i=>{ const e=document.getElementById(i); if(!e) return; const b=e.getBoundingClientRect(); const cs=getComputedStyle(e);
      if(b.width>2&&b.height>2&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05&&(e.textContent||'').trim()) r.c[i]=cs.webkitTextFillColor||cs.color; });
    if(paru && Object.keys(r.c).length){ vu.push(r); if(!premiere) premiere=r; }
    if(performance.now()-t0<1500) requestAnimationFrame(f); else res({premiere:premiere, vu:vu}); }
  requestAnimationFrame(f); })"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    # ⚠ la fiche GLISSE à l'ouverture : une capture prise quelques ms après la lecture des rectangles tombe sur le trait orange de la vague
    #   qui défile (vu : 6 ouvertures sur 20, rectangles du texte entre y 606 et 655). La couleur ne dépend pas du glissement : pendant ce
    #   juge, la fiche ne glisse pas, et la capture et les rectangles coïncident. Le contrôle 1 (chaque image), lui, garde le vrai chemin.
    ctx.add_init_script("document.addEventListener('DOMContentLoaded',function(){ var s=document.createElement('style'); s.textContent='#detailPoster,#detailPoster *{transition:none!important}'; document.head.appendChild(s); });")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(800)
    oranges = 0; premieres_ko = 0; pix_ko = 0; details = []
    for i in range(N):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        # la capture : on attend, côté Python, la première image où la fiche paraît (au plus vite), puis on capture
        pg.evaluate("()=>{ window.__suit=null; }")
        pg.evaluate("(ids)=>{ window.__suit=(" + SUIT + ")(ids); }", IDS)
        rects = None
        for _ in range(200):
            rects = pg.evaluate("(ids)=>{ const dp=document.getElementById('detailPoster'); if(!(dp&&dp.classList.contains('show')&&+getComputedStyle(dp).opacity>0.05)) return null; const dv=document.getElementById('device').getBoundingClientRect(); const o={}; ids.forEach(i=>{ const e=document.getElementById(i); if(!e||!(e.textContent||'').trim()) return; const rg=document.createRange(); rg.selectNodeContents(e); const b=rg.getBoundingClientRect(); if(b.width>2&&b.height>2) o[i]=[b.left,b.top,b.right,b.bottom]; });   /* le rectangle du TEXTE, pas de la boîte (342 de large, elle attrapait le trait orange de la vague) */ return Object.keys(o).length?o:null; }", IDS)
            if rects: break
            pg.wait_for_timeout(5)
        im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB') if rects else None
        r = pg.evaluate("()=>window.__suit")
        # 1 · chaque image
        o_img = [(v['t'], k) for v in (r or {}).get('vu', []) for k, c in v['c'].items() if c == ORANGE]
        if o_img: oranges += 1; details.append('ouverture %d : orange de %d à %d ms (%s)' % (i + 1, o_img[0][0], o_img[-1][0], ', '.join(sorted(set(k for _, k in o_img)))))
        pr = (r or {}).get('premiere') or {}
        if not pr or any(c != CREME for c in pr.get('c', {}).values()): premieres_ko += 1
        # 2 · la capture
        if im:
            px = im.load(); n_or = 0
            for k, (x0, y0, x1, y1) in rects.items():
                W, H = im.size
                for y in range(max(0, int(y0 * 2)), min(H, int(y1 * 2)), 2):
                    for x in range(max(0, int(x0 * 2)), min(W, int(x1 * 2)), 2):
                        c = px[x, y]
                        if abs(c[0] - 221) + abs(c[1] - 77) + abs(c[2] - 35) <= 40: n_or += 1
            if n_or > 6:
                pix_ko += 1; details.append('ouverture %d : %d pixels orange sur la capture %s' % (i + 1, n_or, str({k: [round(v) for v in r_] for k, r_ in rects.items()})))
                if '--garder' in sys.argv: im.save('scratchpad/v122/flash-%d.png' % (i + 1))
    t('1 · [sombre] aucune image (0 → 1,5 s) ne montre l\'orange sur les trois éléments (%d ouvertures)' % N, oranges == 0, '%d ouverture(s) avec orange' % oranges)
    t('1 · [sombre] la première image où ils paraissent les montre déjà crème', premieres_ko == 0, '%d sur %d' % (premieres_ko, N))
    t('2 · [sombre] la capture à la première image : aucun pixel orange sur eux', pix_ko == 0, '%d sur %d' % (pix_ko, N))
    for d in details[:6]: print('     ', d)
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
