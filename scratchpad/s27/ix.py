from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}"); pg.wait_for_timeout(3000)
    print(json.dumps(pg.evaluate(r"""()=>{
      var p=document.querySelector('#indexSheet .enh'); var o={html:p.outerHTML.slice(0,420), enf:[]};
      var cs=getComputedStyle(p); o.plateau={pad:cs.padding, disp:cs.display, ai:cs.alignItems, jc:cs.justifyContent, dir:cs.flexDirection};
      [].forEach.call(p.children,function(e){ var r=e.getBoundingClientRect(); var c=getComputedStyle(e);
        o.enf.push({tag:e.tagName, cls:String(e.className).slice(0,20), y:+r.top.toFixed(1), h:+r.height.toFixed(1),
                    mt:c.marginTop, mb:c.marginBottom, pos:c.position}); });
      var ct=p.querySelector('.ix-count'); if(ct){var r=ct.getBoundingClientRect(); var c=getComputedStyle(ct);
        o.count={y:+r.top.toFixed(1),h:+r.height.toFixed(1),fs:c.fontSize,disp:c.display,mt:c.marginTop,pos:c.position};}
      return o;}"""),indent=1,ensure_ascii=False))
    b.close()
