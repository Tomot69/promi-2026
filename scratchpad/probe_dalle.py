from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':500,'height':700})
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('http://127.0.0.1:8752/scratchpad/vraie_toile.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=60000)
    r=pg.evaluate("""()=>{
      var out={};
      out.count=Toile.count();
      out.abs=[];
      for(var pid=1;pid<=6;pid++){var D=null;try{D=Toile.dalleAbs(pid);}catch(x){}
        out.abs.push(D?[pid,Math.round(D.w),Math.round(D.h)]:[pid,'null']);}
      out.mondes={};
      ['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'].forEach(function(m){
        var cv=document.createElement('canvas');
        try{Toile.dalleTrame(cv,1,1,{m:m,p:'signal',h:0});}catch(x){out.mondes[m]='ERR '+x;return;}
        var g=cv.getContext('2d'),d=g.getImageData(0,0,cv.width,cv.height).data,n=0;
        for(var i=3;i<d.length;i+=4)if(d[i]>8)n++;
        out.mondes[m]=[cv.width,cv.height,Math.round(100*n/(cv.width*cv.height))+'% plein'];});
      return out;}""")
    print("Toile.count :",r['count'])
    print("dalleAbs    :",r['abs'])
    for k,v in r['mondes'].items(): print("  %-9s"%k, v)
    print("erreurs :",e[:2])
    b.close()
