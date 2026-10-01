# -*- coding: utf-8 -*-
"""PASSE 8 — la pile de nœuds orphelins à x≈0. Sur quels écrans, et combien ?"""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

PILE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const out=[];
  [...document.body.querySelectorAll('*')].forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim().replace(/\s+/g,' '); if(!t) return;
    const r=e.getBoundingClientRect();
    if(r.width<1||r.height<1) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    if(y<-40||y>860) return;
    if(x>=-2) return;                       // on ne garde QUE ce qui sort par la gauche
    out.push(Math.round(x)+','+Math.round(y)+'  «'+t.slice(0,44)+'»  ('
      +(e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean)[0])+')');});
  return out;}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)
    ecrans=[('Toile (au repos)',"()=>{if(window.closeAll)closeAll();setView('toile');}"),
            ('page + · choix',"()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();}"),
            ('page + · Promi',"()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}"),
            ('page + · Chiche',"()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const t=[...document.querySelectorAll('#createSheet .tile')][1];if(t)t.click();},500);}"),
            ('fiche Promi',"()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}"),
            ('Index',"()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"),
            ('Fil',"()=>{if(window.closeAll)closeAll();setView('fil');}")]
    for nom,js in ecrans:
        pg.evaluate(js); pg.wait_for_timeout(1700)
        pile=pg.evaluate(PILE)
        print('\n═══ %s ═══  %d nœuds hors cadre par la GAUCHE'%(nom,len(pile)))
        for l in pile[:18]: print('   ',l)
        if len(pile)>18: print('    … et %d autres'%(len(pile)-18))
    print('\nERREURS JS :', er[:4])
    b.close()
