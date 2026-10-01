# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json
ECR=[('fil','#feedView .enh',"()=>{document.getElementById('filBtn').click();}",3200),
     ('studio','#stpHaut',"()=>{document.getElementById('studioBtn').click();}",2800),
     ('index','#indexSheet .enh',"()=>{if(window.ouvrirIndex)ouvrirIndex();}",3000),
     ('aura','#auraScreen .enh',"()=>{document.getElementById('souffleBtn').click();}",5200),
     ('partage','#shareScreen .enh',"()=>{document.getElementById('shareBtn').click();}",4000),
     ('reglages','#settingsScreen .enh',"()=>{document.getElementById('settingsBtn').click();}",2600)]
BUD=r"""(sel)=>{
  function encre(el){ var r=document.createRange(); r.selectNodeContents(el); var b=r.getBoundingClientRect();
    return [+b.left.toFixed(1),+b.right.toFixed(1)]; }
  var p=document.querySelector(sel); if(!p) return null;
  var ti=p.querySelector('.scr-t,.scr-ti,.stp-t,.fd-h2'), cl=p.querySelector('.closeb,[data-close]');
  var cnt=p.querySelector('.ix-count');
  return {titre:ti?{txt:ti.textContent.trim().slice(0,14), fs:getComputedStyle(ti).fontSize, encre:encre(ti),
                    boite:(function(){var r=ti.getBoundingClientRect();return [+r.top.toFixed(0),+r.height.toFixed(1)];})()}:null,
          fermer:cl?encre(cl)[0]:null,
          compte:cnt?{fs:getComputedStyle(cnt).fontSize, boite:(function(){var r=cnt.getBoundingClientRect();return [+r.top.toFixed(1),+r.height.toFixed(1),+r.width.toFixed(1)];})()}:null,
          plateau:(function(){var r=p.getBoundingClientRect();return [+r.top.toFixed(0),+r.height.toFixed(0)];})()};
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,sel,js,wt in ECR:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
        pg.evaluate(js); pg.wait_for_timeout(wt)
        print('%-9s'%nom, json.dumps(pg.evaluate(BUD,sel),ensure_ascii=False), errs)
        open('scratchpad/s27/F-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
        pg.close()
    b.close()
