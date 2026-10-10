import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'; monde=sys.argv[2] if len(sys.argv)>2 else 'ritournelle'; pre=sys.argv[3] if len(sys.argv)>3 else 'rn'
from PIL import Image
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for n in (1,2,3,4,6,9):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
        o=pg.evaluate("([m,n])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} Toile.setTheme(m); Toile.sync(promises.map(p=>p.id)); return [promises.length, JSON.stringify(Toile.graines())]}",[monde,n]); pg.wait_for_timeout(4000)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='/tmp/rn.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('/tmp/rn.png').convert('RGB').resize((260,563)))
        print(n,o,pg.evaluate("()=>JSON.stringify([Toile.vue(),Toile.graines()])")); ctx.close()
    W=Image.new('RGB',(6*266,563),'white')
    for i,im in enumerate(ims): W.paste(im,(i*266,0))
    W.save('planche-v139/%s-%s.png'%(pre,monde)); b.close()
