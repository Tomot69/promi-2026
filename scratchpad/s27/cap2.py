# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json
JOBS=[('aura',"()=>{document.getElementById('souffleBtn').click();}",5600,None),
      ('aura-bas',"()=>{document.getElementById('souffleBtn').click();}",5600,"()=>{var s=document.getElementById('auraScreen'); s.scrollTop=400;}"),
      ('partage',"()=>{document.getElementById('shareBtn').click();}",4200,None),
      ('partage-pelote',"()=>{document.getElementById('shareBtn').click();}",4200,"()=>{var b=document.querySelector('#shMode [data-mode=pelote]'); if(b) b.click();}"),
      ('partage-panneau',"()=>{document.getElementById('shareBtn').click();}",4200,"()=>{var sc=document.getElementById('shareScreen'); sc.classList.add('shc-ouvert'); if(window._shcTire)window._shcTire(true); if(window._v13Partage)window._v13Partage();}"),
      ('index',"()=>{if(window.ouvrirIndex)ouvrirIndex();}",3200,None),
      ('studio-pals',"()=>{document.getElementById('studioBtn').click();}",3000,"()=>{var s=document.getElementById('studioScreen'); s.classList.add('stp-pals'); if(window._studioRetour)window._studioRetour();}")]
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,js,wt,ap in JOBS:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
        pg.evaluate(js); pg.wait_for_timeout(wt)
        if ap: pg.evaluate(ap); pg.wait_for_timeout(2200)
        open('scratchpad/s27/C-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
        if nom=='partage-panneau':
            print('PANNEAU', json.dumps(pg.evaluate(r"""()=>{var o={regs:[],mode:[],parts:[]};
              document.querySelectorAll('#shcPile .shc-reg').forEach(function(c){ if(c.style.display==='none') return;
                o.regs.push((c.querySelector('.l')||{}).textContent); });
              function vis(e){var r=e.getBoundingClientRect();var c=getComputedStyle(e);return r.width>1&&r.height>1&&c.display!=='none'&&c.visibility!=='hidden';}
              document.querySelectorAll('#shMode button').forEach(function(b){ if(vis(b)) o.mode.push(b.textContent.trim());});
              document.querySelectorAll('#shNoyauParts button').forEach(function(b){ if(vis(b)) o.parts.push(b.textContent.trim());});
              return o;}"""),ensure_ascii=False))
        if nom=='partage-pelote':
            print('PELOTE', json.dumps(pg.evaluate(r"""()=>{var cv=document.getElementById('shCanvas');
              var g=cv.getContext('2d'); var d=g.getImageData(0,0,cv.width,cv.height).data;
              var n=0,tot=0; for(var i=3;i<d.length;i+=400){tot++; if(d[i]>10)n++;}
              return {mode:window.shareMode, w:cv.width, h:cv.height, plein:+(n/tot).toFixed(2)};}"""),ensure_ascii=False))
        if errs: print(nom,'ERREURS',errs)
        pg.close()
    b.close()
print('ok')
