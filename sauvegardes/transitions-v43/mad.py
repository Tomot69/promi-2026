from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    r=pg.evaluate("""async()=>{Toile.setTheme('madrure'); await new Promise(r=>setTimeout(r,4000)); closeAll(); await new Promise(r=>setTimeout(r,1500));
      const ids=promises.filter(p=>!p.draft).map(p=>p.id); return ids.slice(0,12).map(id=>[id,Toile.natureDalle(id),(Toile.dalleAbs(id)||{}).minx|0,(Toile.dalleAbs(id)||{}).miny|0]);}""")
    print(r)
    pg.locator('#toileCv').screenshot(path='toile_madrure.png')
    # quelques dalles seules, à 3 tailles
    u=pg.evaluate("""()=>{const ids=promises.filter(p=>!p.draft).map(p=>p.id).slice(0,6); return ids.map(id=>{const c=document.createElement('canvas'); Toile.dalleTrame(c,id,2); return c.toDataURL();});}""")
    import base64,io
    from PIL import Image
    ims=[Image.open(io.BytesIO(base64.b64decode(x.split(',')[1]))) for x in u]
    W=sum(i.size[0] for i in ims)+10*len(ims); H=max(i.size[1] for i in ims)
    s=Image.new('RGBA',(W,H),(240,230,210,255)); x=0
    for i in ims: s.paste(i,(x,0),i); x+=i.size[0]+10
    s.save('dalles_madrure.png'); print([i.size for i in ims])
    b.close()
