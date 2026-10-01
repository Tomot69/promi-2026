from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(pg.evaluate(r"""async()=>{ await document.fonts.ready;
      var c=document.createElement('canvas').getContext('2d'); var o={};
      [['Fi',27],['Inde',27],['Fi',33],['Inde',33]].forEach(function(a){
        c.font='400 '+a[1]+'px PromiLate'; o[a[0]+'@'+a[1]]=+c.measureText(a[0]).width.toFixed(1); });
      return o; }"""))
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3200)
    print('fil   ', pg.evaluate("()=>{var e=document.querySelector('#feedView .fd-h2'); var cs=getComputedStyle(e); return {fs:cs.fontSize, ff:cs.fontFamily, inline:e.getAttribute('style'), tr:cs.transform};}"))
    pg.evaluate("()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}"); pg.wait_for_timeout(3000)
    print('index ', pg.evaluate("()=>{var e=document.querySelector('#indexSheet .scr-ti'); var cs=getComputedStyle(e); return {fs:cs.fontSize, ff:cs.fontFamily, inline:e.getAttribute('style'), tr:cs.transform};}"))
    b.close()
