#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QUI ÉCRIT SUR UN CHAMP, ET AVEC QUELLE ENCRE — et qui écrit en couleur de nature sur le corps.
   On ne devine aucun sélecteur : on parcourt le DOM, on remonte au premier fond opaque,
   et on mesure l'écart de LUMINOSITÉ (§3, seuil 42)."""
import sys, json
from playwright.sync_api import sync_playwright
sys.path.insert(0,'scratchpad'); from couleurs_lab import *

CHAMPS = ['#82AEF8','#FFB8D2','#C9A8F5','#291547']
ETATS  = ['#8FE08F','#FFD447','#DD4D23']          # tenu · en cours · à tenir
SIGNAL = CHAMPS + ETATS
SONDE = r"""()=>{
  function rgb(s){var m=(s||'').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);
    return m?{r:+m[1],g:+m[2],b:+m[3],a:m[4]==null?1:+m[4]}:null;}
  function fond(el){var n=el;while(n&&n!==document.documentElement){var c=rgb(getComputedStyle(n).backgroundColor);
    if(c&&c.a>=0.92)return c; n=n.parentElement;} return null;}
  var out=[];
  document.querySelectorAll('*').forEach(function(el){
    var t=(el.textContent||'').trim(); if(!t||t.length>60)return;
    if(el.children.length)return;
    var r=el.getBoundingClientRect(); if(r.width<4||r.height<4)return;
    var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.opacity==='0')return;
    var f=fond(el); if(!f)return;
    var c=rgb(cs.color)||{r:0,g:0,b:0};
    out.push({sel:(el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.className&&el.className.baseVal===undefined?'.'+String(el.className).trim().split(/\s+/).join('.'):'')),
              mot:t.slice(0,28), fond:[f.r,f.g,f.b], encre:[c.r,c.g,c.b]});
  });
  return out;}"""

def h(t): return rgb2hex(*t)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    PLUS=r"""(n)=>{if(window.closeAll)closeAll();setView('toile');
      document.getElementById('createBtn').click();
      var t=document.querySelector('.tiles-track .tile[data-kind="'+n+'"]'); if(t)t.click(); return 1;}"""
    OUV=r"""(n)=>{function tr(f){try{return promises.filter(q=>!q.draft).find(f);}catch(e){return null;}}
      if(window.closeAll)closeAll();var p=null;
      if(n==='promi'){p=tr(q=>q.status==='encours');if(p){delete p.chiche;p.who='Rachel';}}
      else if(n==='chiche'){p=tr(q=>q.status==='encours');if(p){p.chiche=true;p.who='Marion';}}
      else if(n==='nuee'){var k=null;for(var q in NUE){k=q;break;}if(k){openNueeDetail(k);return 1;}return 0;}
      if(!p)return 0; openDetail(p.id); return 1;}"""
    surchamp={}; surcorps={}
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        for ouvreur,prefixe in ((OUV,'fiche'),(PLUS,'page +')):
          for ecr in ('promi','chiche','nuee'):
            if not pg.evaluate(ouvreur,ecr): continue
            pg.wait_for_timeout(1600)
            for o in pg.evaluate(SONDE):
                f=h(o['fond']); e=h(o['encre']); d=dlum(f,e)
                cle=(o['sel'],f,e)
                if f.upper() in CHAMPS: surchamp[cle]=(o['mot'],d,th,prefixe+' '+ecr)
                elif e.upper() in SIGNAL or min(de(e,c) for c in SIGNAL)<12:
                    if d<42: surcorps[cle]=(o['mot'],d,th,prefixe+' '+ecr)
          pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}")
    b.close()

print(f"\n═══ A · LE TEXTE POSÉ SUR UN CHAMP — {len(surchamp)} ═══")
for (sel,f,e),(mot,d,th,ecr) in sorted(surchamp.items(), key=lambda x:x[1][1]):
    print(f"  Δlum {d:5.1f}  champ {f}  encre {e}   {sel[:44]:44} « {mot} »  [{ecr}/{th}]")
print(f"\n═══ B · LE TEXTE EN COULEUR DE NATURE OU D'ÉTAT SUR LE CORPS, SOUS LE SEUIL 42 — {len(surcorps)} ═══")
for (sel,f,e),(mot,d,th,ecr) in sorted(surcorps.items(), key=lambda x:x[1][1]):
    print(f"  Δlum {d:5.1f}  fond  {f}  encre {e}   {sel[:44]:44} « {mot} »  [{ecr}/{th}]")
