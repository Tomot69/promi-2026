from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}"); pg.wait_for_timeout(3000)
    print(json.dumps(pg.evaluate(r"""()=>{
      var t=document.querySelector('#indexSheet .enh>.scr-ti');
      var c=document.querySelector('#indexSheet .enh .ix-count');
      return {t:{style:t?t.getAttribute('style'):null, top:t?getComputedStyle(t).top:null, pos:t?getComputedStyle(t).position:null},
              c:{style:c?c.getAttribute('style'):null, top:c?getComputedStyle(c).top:null, pos:c?getComputedStyle(c).position:null,
                 parent:c?c.parentElement.className:null}};}"""),indent=1,ensure_ascii=False))
    b.close()
