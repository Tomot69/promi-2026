import sys, io; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from playwright.sync_api import sync_playwright
for vw,vh in ((390,844),(430,932)):
  with sync_playwright() as p:
    b=p.webkit.launch(); cx,pg=BJ.ouvre(b,'app.html','promi',vw,vh)
    pg.evaluate("()=>{document.getElementById('detailPoster').scrollTop=150}"); pg.wait_for_timeout(300)
    print(vw, pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const f=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [+((r.top-D.top)/k).toFixed(3), +((r.bottom-D.top)/k).toFixed(3), +((r.left-D.left)/k).toFixed(3)]; };
      return {k, layer:f(document.getElementById('v189Jonction')), bande:f(document.getElementById('v187Bande')), enh:f(document.querySelector('#detailPoster > .enh')), dev:[D.left,D.top], off:[document.getElementById('device').offsetLeft, document.getElementById('device').offsetTop]}; }"""))
    b.close()
