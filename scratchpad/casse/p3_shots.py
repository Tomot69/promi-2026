# -*- coding: utf-8 -*-
"""PASSE 3 — je REGARDE. Captures d'usage, pas de vérification."""
import sys, os
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright
OUT=R+'/scratchpad/casse/shots'; os.makedirs(OUT,exist_ok=True)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)
    def shot(n): pg.query_selector('#device').screenshot(path=OUT+'/'+n+'.png')

    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(400)
        S='_'+th
        # la page + : les trois natures
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(300)
        pg.click('#createBtn'); pg.wait_for_timeout(1100); shot('pp_choix'+S)
        for i,nat in ((0,'promi'),(1,'chiche'),(2,'nuee')):
            pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(300)
            pg.click('#createBtn'); pg.wait_for_timeout(900)
            pg.evaluate("(i)=>{const t=[...document.querySelectorAll('#createSheet .tile')][i]; if(t)t.click();}",i)
            pg.wait_for_timeout(1100); shot('pp_'+nat+S)
            # et son Peaufiner
            pg.evaluate("()=>{const x=document.querySelector('#createSheet #csBotBar,#createSheet .cbb-lab');if(x)x.click();}")
            pg.wait_for_timeout(1200); shot('pp_'+nat+'_peauf'+S)
        # le choix ouvert
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(300)
        pg.click('#createBtn'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0]; if(t)t.click();}")
        pg.wait_for_timeout(900)
        pg.evaluate("()=>{const e=document.querySelector('[data-ph=titre]'); if(e)e.click();}")
        pg.wait_for_timeout(1000); shot('pp_choix_mot'+S)
        # les fiches
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(300)
        ids=pg.evaluate("""()=>{const o={};
          o.promi=(promises.filter(p=>!p.draft&&!p.req&&!p.chiche&&p.status==='encours')[0]||{}).id;
          o.atenir=(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0]||{}).id;
          o.tenu=(promises.filter(p=>!p.draft&&p.status==='tenu')[0]||{}).id;
          o.chiche=(promises.filter(p=>p.chiche)[0]||{}).id;
          o.draft=(promises.filter(p=>p.draft)[0]||{}).id;
          return o;}""")
        print(th,'ids',ids)
        for k,v in ids.items():
            if v is None: print('   PAS DE PROMI pour',k); continue
            pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}",v); pg.wait_for_timeout(1400)
            shot('fiche_'+k+S)
            # et son Peaufiner ouvert
            pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog');if(t)t.click();}")
            pg.wait_for_timeout(1200); shot('fiche_'+k+'_peauf'+S)
        # la Nuée
        pg.evaluate("()=>{if(window.closeAll)closeAll();const k=Object.keys(NUE)[0];if(k)openEssaim(k);}")
        pg.wait_for_timeout(1500); shot('fiche_nuee'+S)
    print('ERREURS JS :', er[:5])
    b.close()
