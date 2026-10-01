#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""« PEAUFINER » — il doit être IDENTIQUE partout, quel que soit le chemin d'ouverture.
   Tom : « il variait déjà selon le chemin d'ouverture il y a quelques lots »."""
import sys
from playwright.sync_api import sync_playwright
CHEMINS=[
 ("fiche Promi · par la Toile",
  "()=>{if(window.closeAll)closeAll();setView('toile');var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){delete p.chiche;openDetail(p.id);}}"),
 ("fiche Promi · par l'Index",
  "()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){delete p.chiche;openDetail(p.id);}}"),
 ("fiche Chiche",
  "()=>{if(window.closeAll)closeAll();setView('toile');var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){p.chiche=true;openDetail(p.id);}}"),
 ("fiche Nuée",
  "()=>{if(window.closeAll)closeAll();setView('toile');var k=null;for(var q in NUE){k=q;break;}if(k)openNueeDetail(k);}"),
 ("page + Promi",
  "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"promi\"]');if(t)t.click();}"),
 ("page + Chiche",
  "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"chiche\"]');if(t)t.click();}"),
 ("page + Nuée",
  "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"nuee\"]');if(t)t.click();}"),
]
Q=r"""()=>{var out=[];
  document.querySelectorAll('.dpd-mot,.cbb-lab').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width<10) return;
    var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden') return;
    var bar=e.closest('.dpd-tog,#csBotBar,.cbb'); var br=bar?bar.getBoundingClientRect():r;
    out.push({sel:(e.className||'').toString().split(' ')[0],
              police:cs.fontFamily.split(',')[0].replace(/["']/g,''),
              taille:Math.round(parseFloat(cs.fontSize)*10)/10, graisse:cs.fontWeight,
              interlettre:cs.letterSpacing,
              largeur:Math.round(r.width*10)/10, hauteurBarre:Math.round(br.height*10)/10});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(f"{'chemin':30}{'élément':10}{'police':10}{'taille':>7}{'gr.':>6}{'largeur':>9}{'barre':>7}")
    vals=set()
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        for nom,js in CHEMINS:
            pg.evaluate(js); pg.wait_for_timeout(1900)
            for o in pg.evaluate(Q):
                print(f"  {nom+' ['+th[0]+']':28}{o['sel']:10}{o['police']:10}{o['taille']:>7}{o['graisse']:>6}{o['largeur']:>9}{o['hauteurBarre']:>7}")
                vals.add((o['police'],o['taille'],o['graisse']))
            pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(300)
    print(f"\n  → {len(vals)} combinaison(s) police/taille/graisse distincte(s) : {sorted(vals)}")
    b.close()
