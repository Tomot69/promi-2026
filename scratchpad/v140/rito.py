import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
N=[1,2,3,4,9]; FILES=[('zz-av140.html','v139'),('app.html','v140')]; M=sys.argv[1] if len(sys.argv)>1 else 'ritournelle'
with sync_playwright() as p:
    b=p.webkit.launch(); P=Image.new('RGB',(len(N)*400,len(FILES)*880),'white'); dr=ImageDraw.Draw(P)
    for j,(f,lab) in enumerate(FILES):
        for i,n in enumerate(N):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
            pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} }",n)
            pg.evaluate("(m)=>{Toile.setTheme(m); Toile.sync([]); }",M); pg.wait_for_timeout(1200)
            for k in range(1,n+1):
                pg.evaluate("(k)=>{ Toile.sync(promises.slice(0,k).map(p=>p.id)); }",k); pg.wait_for_timeout(500)
            pg.evaluate("()=>{ try{Toile_recadre()}catch(e){} }"); pg.wait_for_timeout(4500)
            r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
            pg.screenshot(path='/tmp/rn.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); P.paste(Image.open('/tmp/rn.png').convert('RGB'),(i*400,j*880+30)); dr.text((i*400+8,j*880+8),'%s — %s, %d parole(s)'%(lab,M,n),fill=(0,0,0))
            ctx.close()
    P.save('planche-v140/PLANCHE-6-%s.png'%M); P.resize((P.width//2,P.height//2)).save('scratchpad/v140/p6-%s.png'%M); b.close()
