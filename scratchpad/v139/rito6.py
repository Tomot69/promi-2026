import sys
from playwright.sync_api import sync_playwright
from PIL import Image
f=sys.argv[1]; pre=sys.argv[2]; N=[int(x) for x in sys.argv[3].split(',')]
M=(sys.argv[4] if len(sys.argv)>4 else 'ritournelle,bobinette,esquille,madrure,halin,brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage').split(',')
with sync_playwright() as p:
    b=p.webkit.launch(); W=Image.new('RGB',(len(M)*200,len(N)*428),'white')
    for j,n in enumerate(N):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:120])); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
        pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} }",n)
        for i,m in enumerate(M):
            pg.evaluate("(m)=>{Toile.setTheme(m); Toile.sync(promises.map(p=>p.id));}",m); pg.wait_for_timeout(3500)
            r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
            pg.screenshot(path='/tmp/rn.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); W.paste(Image.open('/tmp/rn.png').convert('RGB').resize((195,422)),(i*200,j*428))
            print(n,m,pg.evaluate("()=>JSON.stringify(Toile.graines())"),er[-1:] )
        ctx.close()
    W.save('planche-v139/%s.png'%pre); b.close()
