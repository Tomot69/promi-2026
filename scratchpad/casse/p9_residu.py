# -*- coding: utf-8 -*-
"""PASSE 9 — LE GESTE EXACT : j'ouvre Peaufiner sur un Promi, je ferme, j'ouvre un Chiche."""
import sys, os
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright
OUT=R+'/scratchpad/casse/shots2'; os.makedirs(OUT,exist_ok=True)

VISIBLES = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const out=[];
  [...document.body.querySelectorAll('*')].forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim().replace(/\s+/g,' '); if(!t) return;
    const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
    const x=Math.round((r.left-dev.left)/sc), y=Math.round((r.top-dev.top)/sc);
    if(y<-40||y>860||x>60) return;              // la colonne parasite est collée à gauche
    out.push(x+','+y+' '+Math.round(r.width/sc)+'x'+Math.round(r.height/sc)
      +'  «'+t.slice(0,40)+'»  ('+(e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean)[0])+')');});
  return out;}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)

    def etape(t):
        print('\n─── %s'%t)
        v=pg.evaluate(VISIBLES)
        print('    %d nœuds collés au bord gauche'%len(v))
        for l in v[:16]: print('      ',l)

    pg.click('#createBtn'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1100); etape('1 · page + Promi, jamais ouvert Peaufiner')
    pg.query_selector('#device').screenshot(path=OUT+'/residu_1_promi.png')

    pg.evaluate("()=>{const x=document.querySelector('#createSheet #csBotBar,#createSheet .cbb-lab');if(x)x.click();}")
    pg.wait_for_timeout(1400); etape('2 · j\'ouvre Peaufiner')
    pg.query_selector('#device').screenshot(path=OUT+'/residu_2_peauf.png')

    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(700)
    pg.click('#createBtn'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][1];if(t)t.click();}")
    pg.wait_for_timeout(1300); etape('3 · je ferme, je rouvre le + et je choisis CHICHE')
    pg.query_selector('#device').screenshot(path=OUT+'/residu_3_chiche.png')
    print('    classe de #createSheet :', pg.evaluate("()=>document.getElementById('createSheet').className"))

    pg.evaluate("()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}")
    pg.wait_for_timeout(1500); etape('4 · puis j\'ouvre une fiche')
    pg.query_selector('#device').screenshot(path=OUT+'/residu_4_fiche.png')
    print('    classe de #detailPoster :', pg.evaluate("()=>document.getElementById('detailPoster').className"))
    print('\nERREURS JS :', er[:4])
    b.close()
