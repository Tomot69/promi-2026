#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES NEUF ÉCRANS QUE PERSONNE N'A REGARDÉS — la bascule les a traversés, aucune planche ni
   aucune sonde ne les a ouverts. On les ouvre un par un, on capture, et on MESURE au passage
   ce qui rend encore une ancienne couleur ou un texte sous le seuil 42."""
import sys, os, json
from playwright.sync_api import sync_playwright
sys.path.insert(0,'scratchpad'); from couleurs_lab import *
OUT='planche-identite'; os.makedirs(OUT,exist_ok=True)

ECRANS = [
 ("onboarding",     "()=>{var o=document.getElementById('promiOnb'); if(!o) return 0; o.classList.remove('gone'); o.style.display=''; o.style.opacity='1'; return 1;}"),
 ("tutoriel",       "()=>{var t=document.getElementById('tutoOv'); if(!t) return 0; t.classList.add('show'); t.style.display=''; t.style.opacity='1'; return 1;}"),
 ("Langue",         "()=>{var s=document.getElementById('langScreen'); if(!s) return 0; s.classList.add('show'); return 1;}"),
 ("Confidentialite","()=>{var s=document.getElementById('privScreen'); if(!s) return 0; s.classList.add('show'); return 1;}"),
 ("essaim",         "()=>{var s=document.getElementById('essaimSheet'); if(!s) return 0; if(window.openSheet)openSheet(s); else s.classList.add('show'); return 1;}"),
 ("apercu",         "()=>{try{ openPreview(state.structure||'encre', state.mood||0); return 1;}catch(e){ return 0; }}"),
 ("tri",            "()=>{if(window.closeAll)closeAll(); setView('toile'); window.ouvrirIndex(); var s=document.getElementById('ixSort'); if(!s) return 0; s.style.display='flex'; return 1;}"),
 ("fiche personne", "()=>{try{ var n=null; for(var i=0;i<promises.length;i++){var p=promises[i]; if(p.who&&p.who!=='moi'&&p.who!=='Moi'&&p.who!=='le groupe'){n=p.who;break;}} if(!n) return 0; openPerson(n); return 1;}catch(e){return 0;}}"),
 ("partage",        "()=>{var s=document.getElementById('shareScreen'); if(!s) return 0; s.classList.add('show'); try{if(window.shareRender)shareRender();}catch(e){} return 1;}"),
]
VIEUX = ['#3A54FF','#FA2258','#D0B0FF','#8FA0FF','#2BE88C','#F4EEE1','#16171B','#8A5CF0','#0B0C12',
         '#06231A','#C0533A','#F3EFE6','#83858C','#6E685C','#E7E5DF','#E4CEFD','#ECE6D9',
         '#F6F1E3','#89857E','#6D685C','#EAE7DC','#EFE8D6','#B33638']
MESURE = r"""(VIEUX)=>{
  function hex(c){var m=(c||'').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);
    if(!m) return null; if(m[4]!=null && +m[4]<0.9) return null;
    return '#'+[1,2,3].map(function(i){return ('0'+(+m[i]).toString(16)).slice(-2);}).join('').toUpperCase();}
  var anciennes=[], textes=[];
  document.querySelectorAll('*').forEach(function(el){
    var r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    var cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0') return;
    var b=hex(cs.backgroundColor), c=hex(cs.color);
    [[b,'aplat'],[c,'texte']].forEach(function(x){
      if(x[0] && VIEUX.indexOf(x[0])>=0)
        anciennes.push({v:x[0], quoi:x[1], sel:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.trim().split(/\s+/)[0]:''), w:Math.round(r.width), h:Math.round(r.height)});});
    if(el.children.length===0){var t=(el.textContent||'').trim();
      if(t && t.length<60 && c){
        var n=el, f=null;
        while(n&&n!==document.documentElement){var q=hex(getComputedStyle(n).backgroundColor); if(q){f=q;break;} n=n.parentElement;}
        if(f) textes.push({mot:t.slice(0,32), encre:c, fond:f,
          sel:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.trim().split(/\s+/)[0]:'')});}}
  });
  return {anciennes:anciennes, textes:textes};}"""

rap={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    for th in ('light','dark'):
        for nom,js in ECRANS:
            pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6500)
            if nom!='onboarding':
                pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
            ok=pg.evaluate(js)
            if not ok: rap[nom+'/'+th]={'etat':'PAS OUVERT'}; continue
            pg.wait_for_timeout(2200)
            pg.query_selector('#device').screenshot(path=f"{OUT}/neuf_{nom.replace(' ','-')}_{th}.png")
            m=pg.evaluate(MESURE, VIEUX)
            mauv=[t for t in m['textes'] if dlum(t['encre'],t['fond'])<42 and t['encre']!=t['fond']]
            rap[nom+'/'+th]={'etat':'ouvert','anciennes':m['anciennes'],
                             'textes_sous_42':sorted(mauv,key=lambda t:dlum(t['encre'],t['fond']))[:6]}
    print('erreurs JS :', er[:3] if er else 'aucune')
    b.close()
json.dump(rap,open('scratchpad/neuf_ecrans.json','w'),ensure_ascii=False,indent=1)
print()
for k,v in rap.items():
    if v['etat']!='ouvert': print(f"  {k:26} {v['etat']}"); continue
    a=v['anciennes']; t=v['textes_sous_42']
    print(f"  {k:26} anciennes couleurs : {len(a):3}   textes sous 42 : {len(t):3}")
    for x in a[:3]: print(f"        ⚠ {x['v']} en {x['quoi']} — {x['sel'][:40]} {x['w']}×{x['h']}")
    for x in t[:3]: print(f"        · {dlum(x['encre'],x['fond']):5.1f}  {x['encre']} sur {x['fond']}  {x['sel'][:30]:30} « {x['mot'][:26]} »")
