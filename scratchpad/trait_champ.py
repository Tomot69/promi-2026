#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE TRAIT SUR SON CHAMP — §2.1 bis. On mesure le trait RENDU, pas la constante déclarée :
   la vague est peinte en SVG/canevas, et deux moteurs (fiche, page +) ne s'accordent pas."""
import sys, collections
from playwright.sync_api import sync_playwright
sys.path.insert(0,'scratchpad'); from couleurs_lab import *
from PIL import Image

ECR = [
 ("fiche Promi",  "()=>{if(window.closeAll)closeAll();var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){delete p.chiche;p.who='Rachel';openDetail(p.id);}return 1;}"),
 ("fiche Chiche", "()=>{if(window.closeAll)closeAll();var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){p.chiche=true;p.who='Marion';openDetail(p.id);}return 1;}"),
 ("fiche Nuée",   "()=>{if(window.closeAll)closeAll();var k=null;for(var q in NUE){k=q;break;}if(k)openNueeDetail(k);return 1;}"),
 ("page + Promi", "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"promi\"]');if(t)t.click();return 1;}"),
 ("page + Chiche","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"chiche\"]');if(t)t.click();return 1;}"),
 ("page + Nuée",  "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"nuee\"]');if(t)t.click();return 1;}"),
]
CHAMPS = {'#82AEF8':'Promi', '#FFB8D2':'Chiche', '#C9A8F5':'Nuée'}

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(f"{'écran':15}{'thème':7}{'champ':10}{'le trait rendu':>16}{'Δlum':>7}{'ΔE':>7}   §2.1 bis")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        for nom,js in ECR:
            pg.evaluate(js); pg.wait_for_timeout(1900)
            pg.query_selector('#device').screenshot(path='scratchpad/_tc.png')
            im=Image.open('scratchpad/_tc.png').convert('RGB')
            W,H=im.size
            # on descend la colonne centrale : le champ, puis le TRAIT, puis le corps
            col=[rgb2hex(*im.getpixel((W//2, y))) for y in range(0,H,2)]
            champ=None
            for h in col:
                if h.upper() in CHAMPS: champ=h.upper(); break
            if not champ: print(f"  {nom:13}{th:7}{'(pas de champ trouvé)':>33}"); continue
            i=col.index(champ)
            # le premier ton qui n'est ni le champ ni une dalle : c'est le trait
            suite=[h for h in col[i:] if h.upper()!=champ]
            trait=None
            for h in suite:
                if de(h,champ)>18: trait=h; break
            if not trait: print(f"  {nom:13}{th:7}{champ:10}{'(pas de trait)':>16}"); continue
            d,e=dlum(champ,trait),de(champ,trait)
            print(f"  {nom:13}{th:7}{champ:10}{trait:>16}{d:7.1f}{e:7.1f}   "
                  + ('OK' if e>=15 else '⚠ sous ΔE 15'))
            pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(300)
    b.close()
