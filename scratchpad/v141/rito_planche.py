from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
N=[1,2,3,4,9]; FILES=[('zz-av141.html','v140'),('app.html','v141')]
with sync_playwright() as p:
    b=p.webkit.launch(); P=Image.new('RGB',(len(N)*400*2,len(FILES)*(844*2+60)),'white'); dr=ImageDraw.Draw(P)
    for j,(f,lab) in enumerate(FILES):
        for i,n in enumerate(N):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
            pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} Toile.setTheme('ritournelle'); Toile.sync([]); }",n); pg.wait_for_timeout(1200)
            for k in range(1,n+1): pg.evaluate("(k)=>{ Toile.sync(promises.slice(0,k).map(p=>p.id)); }",k); pg.wait_for_timeout(500)
            pg.evaluate("()=>{ try{Toile_recadre()}catch(e){} }"); pg.wait_for_timeout(4500)
            r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
            pg.screenshot(path='/tmp/rn.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); P.paste(Image.open('/tmp/rn.png').convert('RGB'),(i*800,j*(1688+60)+50)); dr.text((i*800+12,j*(1688+60)+16),'%s — Ritournelle, %d parole(s)'%(lab,n),fill=(0,0,0))
            ctx.close()
    P.save('planche-v141/PLANCHE-10-ritournelle.png'); b.close()
