#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captures §4 — Index et Fil × 2 themes. L'Index est une FEUILLE (#indexSheet),
   pas une vue : window.ouvrirIndex(). Le Fil est setView('fil') -> #feedView."""
import os, sys
from playwright.sync_api import sync_playwright
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT=os.path.join(R,'scratchpad/s4'); os.makedirs(OUT,exist_ok=True)
DUMP=r"""()=>{const dev=document.getElementById('device').getBoundingClientRect();const sc=dev.width/390;
 const out=[];
 document.querySelectorAll('body *').forEach(e=>{const c=getComputedStyle(e);
  if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05)return;
  const r=e.getBoundingClientRect();if(r.width<4||r.height<4)return;
  const y=(r.top-dev.top)/sc, x=(r.left-dev.left)/sc;
  if(y<-30||y>900||x<-30||x>400)return;
  out.push(((e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean).slice(0,2).join('.'))+'').slice(0,30)
   +' @'+Math.round(x)+','+Math.round(y)+' '+Math.round(r.width/sc)+'x'+Math.round(r.height/sc)
   +' «'+(e.childElementCount?'':(e.textContent||'').trim().slice(0,22))+'»');});
 return out.slice(0,90);}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        # INDEX — feuille, deux densités
        pg.evaluate("()=>{window._s4Trois=false;if(window.setView)setView('toile');window.ouvrirIndex();}"); pg.wait_for_timeout(1400)
        pg.query_selector('#device').screenshot(path=os.path.join(OUT,'ix_deux_%s.png'%th))
        pg.evaluate("()=>{window._s4Trois=true;if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(900)
        pg.query_selector('#device').screenshot(path=os.path.join(OUT,'ix_trois_%s.png'%th))
        pg.evaluate("()=>{window._s4Trois=false;if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(400)
        if th=='dark':
            print('=== INDEX (dark) ==='); [print('  ',l) for l in pg.evaluate(DUMP)]
        # FIL
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1400)
        pg.query_selector('#device').screenshot(path=os.path.join(OUT,'fil_%s.png'%th))
        if th=='dark':
            print('=== FIL (dark) ==='); [print('  ',l) for l in pg.evaluate(DUMP)]
        pg.evaluate("()=>{setView('toile');if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
    print('ERREURS JS :', er[:3]); b.close()
