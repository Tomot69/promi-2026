#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ÉTAT TYPOGRAPHIQUE, ÉCRAN PAR ÉCRAN — police, taille, graisse, et la BOÎTE qui rogne.
   On mesure le débordement vertical : `scrollHeight > clientHeight` sur un texte, c'est un
   jambage coupé."""
import sys, json
from playwright.sync_api import sync_playwright
ECR=[("accueil","()=>{if(window.closeAll)closeAll();setView('toile');}"),
 ("Index","()=>{if(window.closeAll)closeAll();ouvrirIndex();}"),
 ("Fil","()=>{if(window.closeAll)closeAll();setView('fil');}"),
 ("Aura","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('souffleBtn').click();}"),
 ("Studio","()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();setView('toile');document.getElementById('studioBtn').click();}"),
 ("Réglages","()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();var s=document.getElementById('settingsScreen');if(s)s.classList.add('show');}"),
 ("Partage","()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();var s=document.getElementById('shareScreen');if(s)s.classList.add('show');}"),
 ("fiche Promi","()=>{if(window.closeAll)closeAll();setView('toile');var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){delete p.chiche;openDetail(p.id);}}"),
 ("fiche Nuée","()=>{if(window.closeAll)closeAll();setView('toile');var k=null;for(var q in NUE){k=q;break;}if(k)openNueeDetail(k);}"),
 ("page + choix","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();}"),
 ("page + Promi","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"promi\"]');if(t)t.click();}"),
]
Q=r"""()=>{var out=[];
 var CIB='.scr-t,.scr-ti,.enh-t,.stp-t,.cs-mark,.acc-mm,#stpNom,.dpt-nat,.dpt-titre,.s4-ti,'
        +'.closeb,.cb-mot,.dpd-mot,.cbb-lab,.ph-txt,.cs-quest-big,.hname,.hsub,h1,h2,#dptTitre';
 document.querySelectorAll(CIB).forEach(function(e){
   var r=e.getBoundingClientRect(); if(r.width<6||r.height<4) return;
   var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0') return;
   var t=(e.textContent||'').trim(); if(!t) return;
   out.push({sel:e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className?'.'+e.className.trim().split(/\s+/).slice(0,2).join('.'):''),
             mot:t.slice(0,22), ff:cs.fontFamily.split(',')[0].replace(/["']/g,''),
             fs:Math.round(parseFloat(cs.fontSize)*10)/10, fw:cs.fontWeight,
             h:Math.round(r.height*10)/10, sh:e.scrollHeight, ch:e.clientHeight,
             lh:cs.lineHeight, ov:cs.overflow,
             rogne:(e.scrollHeight>e.clientHeight+1 && cs.overflow!=='visible'),
             svg:!!e.querySelector('svg.titre-dessin')});});
 return out;}"""
vus={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR:
        pg.evaluate(js); pg.wait_for_timeout(1800)
        for o in pg.evaluate(Q):
            k=(nom,o['sel'],o['mot'])
            if k not in vus: vus[k]=o
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();setView('toile');}")
        pg.wait_for_timeout(300)
    b.close()
print(f"{'écran':14}{'élément':26}{'mot':22}{'police':11}{'taille':>7}{'gr.':>5}  rogné/dessin")
for (ecr,sel,mot),o in vus.items():
    mark=''
    if o['rogne']: mark=' ⚠ ROGNÉ (%d>%d)'%(o['sh'],o['ch'])
    if o['svg']: mark+=' [dessin]'
    if o['ff'] not in ('Gilbert','Atkinson','Fraunces') and not o['svg']: mark+=' ⚠ POLICE '+o['ff']
    print(f"  {ecr:12}{sel[:24]:26}{mot[:20]:22}{o['ff']:11}{o['fs']:>7}{o['fw']:>5}{mark}")
