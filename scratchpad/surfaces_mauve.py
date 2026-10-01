#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES SURFACES QUI RENDENT ENCORE #291547 — on mesure le RENDU, pas les règles.
   Une règle peut être écrasée par une autre : seul ce qui se peint compte."""
import sys, json
from playwright.sync_api import sync_playwright
ECRANS=[
 ("fiche Nuée","()=>{if(window.closeAll)closeAll();var k=null;for(var q in NUE){k=q;break;}if(k)openNueeDetail(k);}"),
 ("fiche Nuée · Peaufiner","()=>{var b=document.getElementById('dpdTog')||document.querySelector('.dpd-tog');if(b)b.click();}"),
 ("page + Nuée","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"nuee\"]');if(t)t.click();}"),
 ("page + Nuée · créneau","()=>{var m=document.querySelector('#nueePhrase [data-ph],#csPhrase [data-ph]');if(m)m.click();}"),
 ("page + choix","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();}"),
 ("page + Promi en Nuée","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var cs=document.getElementById('createSheet');if(cs)cs.classList.add('cs-nuee');}"),
 ("Index","()=>{if(window.closeAll)closeAll();setView('toile');window.ouvrirIndex();}"),
 ("Fil","()=>{if(window.closeAll)closeAll();setView('fil');}"),
 ("Cercle","()=>{if(window.closeAll)closeAll();document.getElementById('plusScreen').classList.add('show');}"),
 ("Aura","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('souffleBtn').click();}"),
]
Q=r"""()=>{var out=[];
 function bg(el,ps){var c=getComputedStyle(el,ps||null).backgroundColor;
   var m=(c||'').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);
   if(!m) return null; if(m[4]!=null && +m[4]<0.9) return null;
   return (+m[1]===41 && +m[2]===21 && +m[3]===71);}
 document.querySelectorAll('*').forEach(function(el){
   var r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
   var cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0') return;
   [null,'::before','::after'].forEach(function(ps){
     if(!bg(el,ps)) return;
     if(ps){ var c2=getComputedStyle(el,ps); if(c2.content==='none') return;
             var r2=c2.width; if(r2==='auto'||parseFloat(r2)<4) return; }
     out.push({sel:(el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.trim().split(/\s+/).slice(0,3).join('.'):''))+(ps||''),
               w:Math.round(r.width), h:Math.round(r.height), aire:Math.round(r.width*r.height),
               enfants:el.querySelectorAll('*').length, txt:(el.textContent||'').trim().slice(0,28)});});});
 return out;}"""
vus={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        for nom,js in ECRANS:
            pg.evaluate(js); pg.wait_for_timeout(1700)
            for o in pg.evaluate(Q):
                k=o['sel']
                if k not in vus or o['aire']>vus[k]['aire']:
                    o['ou']=nom+' · '+th; vus[k]=o
            if 'Peaufiner' not in nom and 'créneau' not in nom:
                pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();setView('toile');}")
                pg.wait_for_timeout(300)
    b.close()
print(f"{len(vus)} surfaces rendent encore #291547\n")
print(f"{'boîte':>12}{'aire':>9}{'enfants':>9}   élément et contenu")
for k in sorted(vus,key=lambda x:-vus[x]['aire']):
    o=vus[k]
    print(f"  {o['w']:>4}×{o['h']:<5}{o['aire']:>9}{o['enfants']:>9}   {k[:52]:52} « {o['txt']} »   ({o['ou']})")
json.dump(vus,open('scratchpad/surfaces_mauve.json','w'),ensure_ascii=False,indent=1)
