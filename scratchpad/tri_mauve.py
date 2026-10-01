#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE TRI DES 41 RÈGLES EN #291547 — la loi de Tom, 17 septembre 2026 :
   « si la règle peint un CHAMP — la surface qui dit la nature — elle passe au lilas #C9A8F5 ;
     si elle peint un TRAIT, un TEXTE ou un ACCENT posé sur ce champ, elle reste au violet ».
   On ne devine pas : on ouvre les écrans, on mesure la surface peinte, et on regarde si
   l'élément PORTE du contenu (un champ en porte) ou s'il EST le contenu (un accent)."""
import sys, json
from playwright.sync_api import sync_playwright

ECRANS = [
 ("fiche Nuée",   "()=>{if(window.closeAll)closeAll();var k=null;for(var q in NUE){k=q;break;}if(k)openNueeDetail(k);}"),
 ("page + Nuée",  "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var t=document.querySelector('.tiles-track .tile[data-kind=\"nuee\"]');if(t)t.click();}"),
 ("page + choix", "()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();}"),
 ("page + Promi en Nuée","()=>{if(window.closeAll)closeAll();setView('toile');document.getElementById('createBtn').click();var cs=document.getElementById('createSheet');if(cs)cs.classList.add('cs-nuee');}"),
 ("Index",        "()=>{if(window.closeAll)closeAll();setView('toile');window.ouvrirIndex();}"),
 ("Cercle",       "()=>{if(window.closeAll)closeAll();document.getElementById('plusScreen').classList.add('show');}"),
]
COLLECTE = r"""()=>{var out=[];
 for(var i=0;i<document.styleSheets.length;i++){var sh=document.styleSheets[i],rs;try{rs=sh.cssRules;}catch(e){continue;}
  for(var j=0;j<rs.length;j++){var r=rs[j];if(!r.selectorText||!r.style)continue;
   var bg=(r.style.getPropertyValue('background')||'')+' '+(r.style.getPropertyValue('background-color')||'');
   if(!/--c-mauve12\b/.test(bg)) continue;
   r.selectorText.split(',').forEach(function(s){
     s=s.trim(); var pseudo=/::?(before|after)$/.test(s);
     var base=s.replace(/::?(before|after)$/,'');
     var els=[]; try{ els=[].slice.call(document.querySelectorAll(base)); }catch(e){}
     els.forEach(function(el){
       var r2=el.getBoundingClientRect(); if(r2.width<3||r2.height<3) return;
       var cs=getComputedStyle(el, pseudo?'::'+RegExp.$1:null);
       if(cs.display==='none'||cs.visibility==='hidden') return;
       /* PORTE-T-IL DU CONTENU ? un champ en porte ; un accent EST le contenu. */
       var enfants=el.querySelectorAll('*').length;
       var txt=(el.textContent||'').trim().length;
       out.push({sel:s, aire:Math.round(r2.width*r2.height), w:Math.round(r2.width), h:Math.round(r2.height),
                 enfants:enfants, txt:txt, pseudo:pseudo, id:(sh.ownerNode&&sh.ownerNode.id)||''});});});}}
 return out;}"""

vus={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o)o.style.display='none';}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        for nom,js in ECRANS:
            pg.evaluate(js); pg.wait_for_timeout(1700)
            for o in pg.evaluate(COLLECTE):
                k=o['sel']
                if k not in vus or o['aire']>vus[k]['aire']:
                    o['ou']=nom; vus[k]=o
            pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();setView('toile');}")
            pg.wait_for_timeout(300)
    b.close()

def verdict(o):
    # un CHAMP : grande surface qui PORTE du contenu (des enfants, ou un pseudo de fond)
    if o['pseudo'] and o['aire']>40000: return 'CHAMP'
    if o['aire']>=30000 and o['enfants']>=3: return 'CHAMP'
    if o['aire']>=12000 and o['enfants']>=2 and o['txt']<40: return 'CHAMP'
    return 'accent'
print(f"{len(vus)} sélecteurs atteints\n")
for k in sorted(vus, key=lambda x:-vus[x]['aire']):
    o=vus[k]; v=verdict(o)
    print(f"  {v:7} {o['w']:>4}×{o['h']:<4} aire {o['aire']:>7}  enfants {o['enfants']:>3}  txt {o['txt']:>3}  "
          f"[{o['id'][:16]:16}] {k[:64]}   ({o['ou']})")
json.dump({k:dict(vus[k], verdict=verdict(vus[k])) for k in vus}, open('scratchpad/tri_mauve.json','w'), ensure_ascii=False, indent=1)
