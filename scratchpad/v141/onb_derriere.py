# « Toi, c'est ? » : aucune dalle derrière le texte — part des pixels clairs (cellule) dans la boîte de la phrase, N chargements
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 6
with sync_playwright() as p:
    b=p.webkit.launch(); pire=0
    for n in range(N):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        r=pg.evaluate("()=>{var e=document.getElementById('onbPh'); var rg=document.createRange(); rg.selectNodeContents(e); var r=rg.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        im=Image.open(io.BytesIO(pg.screenshot(clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}))).convert('RGB'); px=im.load(); c=0; t=0
        for y in range(0,im.height,2):
            for x in range(0,im.width,2):
                q=px[x,y]; t+=1
                if q[0]+q[1]+q[2]>300 and (abs(q[0]-223)+abs(q[1]-202)+abs(q[2]-164))>9: c+=1
        pc=100.0*c/t; pire=max(pire,pc); print(n,'boîte',[round(v) for v in r],'cellule derrière : %.1f %%'%pc)
        if pc>1: im.save('scratchpad/v141/derriere-%d.png'%n)
        ctx.close()
    print('pire %.1f %%'%pire); b.close()
