# -*- coding: utf-8 -*-
import json
from playwright.sync_api import sync_playwright
OUT={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:220]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    # 1 · le Fil
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3600)
    OUT['fil']=pg.evaluate(r"""()=>{var o=[];
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d){
        var t=d.querySelector('.s4-ti'), cv=d.querySelector('canvas');
        var g=cv.getContext('2d'), W=cv.width, dpr=W/143;
        var im=g.getImageData(0,0,W,cv.height).data;
        var ch=(cv.getAttribute('data-champ')||'').match(/\d+/g); ch=ch?ch.slice(0,3).map(Number):null;
        function lum(c){return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
        var x0=Math.round(5*dpr),y0=Math.round(40*dpr),ww=Math.round(110*dpr),hh=Math.round(80*dpr);
        var dmax=0;
        for(var y=y0;y<y0+hh;y+=3)for(var x=x0;x<x0+ww;x+=3){var q=(y*W+x)*4;
          if(im[q+3]<40) continue; var c=[im[q],im[q+1],im[q+2]];
          if(ch){var dd=Math.abs(lum(c)-lum(ch)); if(dd>dmax)dmax=dd;}}
        o.push({titre:t.textContent.slice(0,26), fs:getComputedStyle(t).fontSize,
                cote:d.getAttribute('data-titre-cote'), champ:cv.getAttribute('data-champ'),
                dalleDelta:+dmax.toFixed(1), top:t.style.top, ev:(d.querySelector('.s4-ev')||{}).style&&d.querySelector('.s4-ev').style.top});
      }); return o;}""")
    open('scratchpad/s27/V13-fil.png','wb').write(pg.query_selector('#device').screenshot())
    # 2 · le Chiche
    for nom,idp in (('chiche-groupe',133),('chiche-tenu',129)):
        pg.evaluate("(i)=>{closeAll(); openDetail(i);}",idp); pg.wait_for_timeout(3400)
        OUT[nom]=pg.evaluate(r"""()=>{
          function lum(c){return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
          function rgb(s){var m=(s||'').match(/-?\d+(\.\d+)?/g);return m?m.slice(0,3).map(Number):null;}
          function fond(el){var n=el;while(n&&n.nodeType===1){var b=getComputedStyle(n).backgroundColor,c=rgb(b);
            var a=b.match(/rgba?\([^)]*?,\s*([\d.]+)\)/); if(c&&(!a||parseFloat(a[1])>0.85))return c; n=n.parentNode;} return null;}
          var o={filet:null, textes:[]};
          var cv=document.getElementById('dpTrameCv'); if(cv) o.filet=cv.getAttribute('data-filet-trait');
          document.querySelectorAll('#detailPoster *').forEach(function(el){
            if(el.children.length) return; var t=(el.textContent||'').trim(); if(!t) return;
            var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
            var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
            var c=rgb(cs.webkitTextFillColor||cs.color), f=fond(el); if(!c||!f) return;
            o.textes.push({txt:t.slice(0,26), col:cs.color, d:+Math.abs(lum(c)-lum(f)).toFixed(1), lis:el.getAttribute('data-lis')});
          });
          o.textes.sort(function(a,b){return a.d-b.d;}); o.textes=o.textes.slice(0,6);
          return o;}""")
        open('scratchpad/s27/V13-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
    # 3 · la Pelote
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5600)
    OUT['pelote1']=pg.evaluate("()=>window._aura.sol()")
    OUT['aura_col']=pg.evaluate("()=>window._aura.etat().col")
    open('scratchpad/s27/V13-aura.png','wb').write(pg.query_selector('#device').screenshot())
    sols=[]
    for i in range(6):
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(1400)
        sols.append(pg.evaluate("()=>window._aura.sol().idx"))
    OUT['sols']=sols
    OUT['erreurs']=errs
    b.close()
print(json.dumps(OUT,indent=1,ensure_ascii=False))
