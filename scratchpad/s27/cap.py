# -*- coding: utf-8 -*-
import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    info=pg.evaluate("()=>promises.filter(function(p){return p.chiche;}).map(function(p){return {id:p.id,t:p.title,st:p.status,avec:p.avec,who:p.who,from:p.from};})")
    print(json.dumps(info,ensure_ascii=False))
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(700)
        for nom,js,wt in (
          ('chiche-tenu',"()=>{closeAll(); var q=promises.find(function(p){return p.chiche&&p.status==='tenu';}); if(q) openDetail(q.id);}",3600),
          ('chiche-encours',"()=>{closeAll(); var q=promises.find(function(p){return p.chiche&&p.status!=='tenu';}); if(q) openDetail(q.id);}",3600),
          ('promi-tenu',"()=>{closeAll(); var q=promises.find(function(p){return !p.chiche&&!p.nuee&&p.status==='tenu';}); if(q) openDetail(q.id);}",3600),
          ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}",5400),
          ('partage',"()=>{closeAll(); var b=document.getElementById('shareBtn'); if(b) b.click();}",4000),
          ('index',"()=>{closeAll(); if(window.ouvrirIndex) ouvrirIndex();}",3000),
          ('reglages',"()=>{closeAll(); document.getElementById('settingsBtn').click();}",2600)):
            pg.evaluate(js); pg.wait_for_timeout(wt)
            open('scratchpad/s27/%s-%s.png'%(nom,th),'wb').write(pg.query_selector('#device').screenshot())
            pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(600)
    b.close()
print('ok')
