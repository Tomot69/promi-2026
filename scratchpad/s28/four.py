# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json
JOBS=[('folio-pelote','mosaic',"()=>{window.shPelote=true; window.shareRender();}"),
      ('toile-coin','toile',"()=>{window.shPelote=true; window.shToileCompo='coin'; window.shareRender();}"),
      ('toile-socle','toile',"()=>{window.shPelote=true; window.shToileCompo='socle'; window.shareRender();}"),
      ('panneau','mosaic',"()=>{var sc=document.getElementById('shareScreen'); sc.classList.add('shc-ouvert'); if(window._shcTire)window._shcTire(true); if(window._v13Partage)window._v13Partage(); if(window._v14)window._v14();}")]
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,mode,js in JOBS:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6600)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
        pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(4200)
        pg.evaluate("(m)=>{var b=document.querySelector('#shMode [data-mode='+m+']'); if(b) b.click();}",mode)
        pg.wait_for_timeout(2200)
        pg.evaluate(js); pg.wait_for_timeout(2600)
        open('scratchpad/s28/V14-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
        if nom=='panneau':
            print('PANNEAU', json.dumps(pg.evaluate(r"""()=>{var o={regs:[],mode:[],img:[]};
              function vis(e){var r=e.getBoundingClientRect();var c=getComputedStyle(e);return r.width>1&&r.height>1&&c.display!=='none'&&c.visibility!=='hidden';}
              document.querySelectorAll('#shcPile .shc-reg').forEach(function(c){ if(c.style.display==='none') return; o.regs.push((c.querySelector('.l')||{}).textContent); });
              document.querySelectorAll('#shMode button').forEach(function(b){ if(vis(b)) o.mode.push(b.textContent.trim());});
              document.querySelectorAll('#shNoyauParts button').forEach(function(b){ if(vis(b)) o.img.push(b.textContent.trim());});
              return o;}"""),ensure_ascii=False))
        if nom=='folio-pelote':
            print('FOLIO', json.dumps(pg.evaluate("()=>window._plancheComp&&{n:window._plancheComp.n,pelote:window._plancheComp.pelote,rangees:window._plancheComp.rangees,cols:window._plancheComp.cols}"),ensure_ascii=False))
        if errs: print(nom,'ERR',errs)
        pg.close()
    b.close()
print('ok')
