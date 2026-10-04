# C-009 — Ramage au Studio : filmer 14 s (une image toutes les ~90 ms), mesurer ce qui change d'une image à l'autre et où
import sys, io, json, math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG = sys.argv[2] if len(sys.argv)>2 else 'a'; MOT = sys.argv[3] if len(sys.argv)>3 else 'webkit'
with sync_playwright() as p:
    b=(p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    d=pg.evaluate("()=>{var d=document.getElementById('device').getBoundingClientRect();return [d.left,d.top,d.width,d.height];}")
    clip={'x':d[0],'y':d[1]+110,'width':d[2],'height':430}
    ims=[]; ts=[]
    import time; t0=time.time()
    while time.time()-t0<14:
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')); ts.append(time.time()-t0)
    print(len(ims),'images'); res=[]
    for i in range(1,len(ims)):
        df=ImageChops.difference(ims[i-1],ims[i]).convert('L').point(lambda v:255 if v>14 else 0); bb=df.getbbox()
        n=sum(1 for v in df.resize((df.size[0]//4,df.size[1]//4)).getdata() if v>0)
        res.append((round(ts[i],2), n, bb))
    json.dump(res, open('scratchpad/v126/ramage-%s.json'%TAG,'w'))
    actifs=[r for r in res if r[1]>30]
    print('images qui bougent :', len(actifs), '· instants :', ' '.join('%.1f'%r[0] for r in actifs[:60]))
    # planche : huit images du premier mouvement, et l'écart de chacune avec l'image posée d'après
    if actifs:
        i0=next(i for i,r in enumerate(res) if r[1]>30); sel=list(range(i0, min(len(ims)-1, i0+16), 2))[:8]
        W,H=ims[0].size; o=Image.new('RGB',(4*(W//2)+30, 2*(H//2)+10),(128,128,128))
        for k,i in enumerate(sel): o.paste(ims[i+1].resize((W//2,H//2)), ((k%4)*(W//2+10), (k//4)*(H//2+10)))
        o.save('scratchpad/v126/ramage-film-%s.png'%TAG); print('planche', o.size, 'à partir de', ts[i0+1])
        for k,i in enumerate(sel[:8]): ims[i+1].save('scratchpad/v126/rf-%s-%d.png'%(TAG,k))
    b.close()
