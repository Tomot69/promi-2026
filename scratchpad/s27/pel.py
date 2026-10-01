from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(json.dumps(pg.evaluate(r"""()=>{
      var cv=window._aura.pelote();
      var g=cv.getContext('2d'); var d=null, n=0, tot=0;
      try{ d=g.getImageData(0,0,cv.width,cv.height).data;
        for(var i=3;i<d.length;i+=400){tot++; if(d[i]>10)n++;} }catch(e){}
      return {w:cv.width,h:cv.height, rect:cv.getBoundingClientRect().width, plein:tot?+(n/tot).toFixed(2):null,
              err:window._auraErreur||null, etat:window._aura.etat().pret};}"""),indent=1,ensure_ascii=False))
    b.close()
