# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json,sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'mosaic'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(4200)
    pg.evaluate("(m)=>{var b=document.querySelector('#shMode [data-mode='+m+']'); if(b) b.click();}",MODE)
    pg.wait_for_timeout(2600)
    open('scratchpad/s28/%s.png'%MODE,'wb').write(pg.query_selector('#device').screenshot())
    print(json.dumps(pg.evaluate("()=>({mode:window.shareMode, comp:window._plancheComp&&{n:window._plancheComp.n,noyau:window._plancheComp.noyau,mots:window._plancheComp.mots}})"),ensure_ascii=False)[:900])
    print('ERR',errs)
    b.close()
