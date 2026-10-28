import sys, io, os, base64; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image
import banc_tom as B
cars=os.environ.get('CARS','MWSU'); out=os.environ.get('OUT','scratchpad/v170/strip.png'); fic=os.environ.get('FIC','app.html')
fr=[float(x) for x in os.environ.get('FR','0.15,0.3,0.45,0.6,0.75,0.9').split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+fic, timeout=300000); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
    rows=[]
    for c in cars:
        pg.evaluate("""async c=>{ document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
          const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:60px;top:40px;width:300px;font:400 170px/200px PromiLate;color:#291547;z-index:60'; el.textContent=c; document.body.appendChild(el);
          await document.fonts.load('400 170px PromiLate'); window.C=TraceLettres.trace(el, null, {manuel:true, respecteReduire:false}); await C.pret; }""", c)
        ims=[]
        for f in fr+[0.99999]:
            u=pg.evaluate("f=>{ C.va(f); const cv=C.canevas; const o=document.createElement('canvas'); o.width=cv.width; o.height=cv.height; const g=o.getContext('2d'); g.fillStyle='#F7F0DE'; g.fillRect(0,0,o.width,o.height); g.drawImage(cv,0,0); return o.toDataURL(); }", f)
            ims.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'))
        pg.evaluate("()=>C.stop()")
        h=max(i.height for i in ims); row=Image.new('RGB',(sum(i.width for i in ims)+10*len(ims),h),'white'); x=0
        for i in ims: row.paste(i,(x,0)); x+=i.width+10
        rows.append(row)
    W=max(r.width for r in rows); im=Image.new('RGB',(W,sum(r.height+10 for r in rows)),'white'); y=0
    for r in rows: im.paste(r,(0,y)); y+=r.height+10
    s=float(os.environ.get('SC','0.4')); im=im.resize((int(im.width*s),int(im.height*s))); im.save(out); print(out, im.size)
    b.close()
