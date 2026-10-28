import sys, base64, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
car=sys.argv[1]; fr=[float(x) for x in sys.argv[2].split(',')]
JS="""async a=>{ const [car,fr]=a; const el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:60px;width:300px;font:400 '+(window.__FZ||150)+'px/1.2 PromiLate;color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
 await document.fonts.load('400 40px PromiLate'); const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret; const cv=C.canevas; const out=[];
 for(const f of fr){ C.va(f); out.push(cv.toDataURL()); } C.stop(); el.remove(); return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000); pg.evaluate('f=>window.__FZ=f', float(__import__('os').environ.get('FZ','150')))
    r=pg.evaluate(JS,[car,fr]); ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))) for u in r]
    W=sum(i.width for i in ims); H=ims[0].height; o=Image.new('RGBA',(W,H),'white'); x=0
    for i in ims:
        bg=Image.new('RGBA',i.size,'white'); bg.alpha_composite(i); o.paste(bg,(x,0)); x+=i.width
    o.save('scratchpad/v170/frame.png'); print(ims[0].size)
    b.close()
