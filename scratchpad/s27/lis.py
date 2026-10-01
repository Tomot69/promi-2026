# -*- coding: utf-8 -*-
import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        for tour in (1,2):
            pg.evaluate("()=>{closeAll(); openDetail(133);}"); pg.wait_for_timeout(2600)
            r=pg.evaluate(r"""()=>{var o={lis:[],lisb:[],pires:[]};
              function lum(c){return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
              function rgb(s){var m=(s||'').match(/-?\d+(\.\d+)?/g);return m?m.slice(0,3).map(Number):null;}
              function fond(el){var n=el;while(n&&n.nodeType===1){var b=getComputedStyle(n).backgroundColor,c=rgb(b);
                var a=b.match(/rgba?\([^)]*?,\s*([\d.]+)\)/); if(c&&(!a||parseFloat(a[1])>0.85))return c; n=n.parentNode;} return null;}
              document.querySelectorAll('#detailPoster [data-lis]').forEach(function(e){o.lis.push([(e.textContent||'').trim().slice(0,22),e.getAttribute('data-lis')]);});
              document.querySelectorAll('#detailPoster [data-lisb]').forEach(function(e){o.lisb.push([String(e.className).slice(0,18),e.getAttribute('data-lisb')]);});
              document.querySelectorAll('#detailPoster *').forEach(function(el){
                if(el.children.length) return; var t=(el.textContent||'').trim(); if(!t) return;
                var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
                var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
                var c=rgb(cs.webkitTextFillColor||cs.color), f=fond(el); if(!c||!f) return;
                o.pires.push([+Math.abs(lum(c)-lum(f)).toFixed(1), t.slice(0,24)]);});
              o.pires.sort(function(a,b){return a[0]-b[0];}); o.pires=o.pires.slice(0,4);
              return o;}""")
            print(th,'tour',tour,json.dumps(r,ensure_ascii=False))
        open('scratchpad/s27/LIS-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
    print('ERREURS',errs)
    b.close()
