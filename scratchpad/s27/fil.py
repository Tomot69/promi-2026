# -*- coding: utf-8 -*-
import json,sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3600)
    r=pg.evaluate(r"""()=>{ var o=[];
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d,i){
        var cv=d.querySelector('canvas'); var t=d.querySelector('.s4-ti');
        var g=cv.getContext('2d'), W=cv.width, H=cv.height;
        var im=g.getImageData(0,0,W,H).data;
        // la zone de matiere declaree : 5,40,110,80 en CSS -> x2 (dpr)
        var dpr=W/143;
        var x0=Math.round(5*dpr), y0=Math.round(40*dpr), ww=Math.round(110*dpr), hh=Math.round(80*dpr);
        var n=0, tot=0, cols={};
        for(var y=y0;y<y0+hh;y+=3){ for(var x=x0;x<x0+ww;x+=3){
          var q=(y*W+x)*4; tot++;
          var k=im[q]+','+im[q+1]+','+im[q+2];
          cols[k]=(cols[k]||0)+1;
        }}
        var champ=cv.getAttribute('data-champ')||'';
        // combien de pixels DIFFERENT du champ ?
        var distincts=Object.keys(cols).length;
        var top=Object.keys(cols).sort(function(a,b){return cols[b]-cols[a];}).slice(0,3).map(function(k){return k+' x'+cols[k];});
        o.push({i:i, titre:t.textContent.slice(0,26), champ:champ, tot:tot, distincts:distincts, dominantes:top,
                peint:cv.getAttribute('data-peint'), mat:cv.getAttribute('data-matiere')});
      }); return o; }""")
    print(json.dumps(r,indent=1,ensure_ascii=False))
    print('ERREURS',errs)
    open('scratchpad/s27/fil.png','wb').write(pg.query_selector('#device').screenshot())
    b.close()
