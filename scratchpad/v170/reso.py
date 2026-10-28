import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); i=src.index('ENREG = """'); j=src.index('"""', i+11); ENREG=src[i+11:j].replace('\\\\','\\')
with sync_playwright() as p:
    b=p.webkit.launch()
    for vw,vh in ((390,651),(390,844),(330,714)):
        ctx=B.contexte(b,vw=vw,vh=vh); pg=B.ouvre(ctx,'app.html',attente=7000,q='?tlv=0.05')
        pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
        pg.evaluate(ENREG); pg.evaluate("()=>_guide.montre('reste')"); pg.wait_for_timeout(4000)
        r=pg.evaluate("""()=>{ const cv=document.querySelector('canvas[data-trace]'); if(!cv) return null; const q=cv.getBoundingClientRect(), d=devicePixelRatio, dv=document.getElementById('device').getBoundingClientRect();
          return {W:cv.width,H:cv.height, rw:q.width*d, rh:q.height*d, left:q.left*d, top:q.top*d, dpr:d, ech:dv.width/390, css:cv.style.width}; }""")
        print(vw,vh,r); ctx.close()
    b.close()
