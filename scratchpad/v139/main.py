import sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:150])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} openDetail(promises.find(q=>q.title==='faire les crêpes').id)}")
    pg.wait_for_function("()=>!!GesteFantome.etat()",timeout=15000); t0=pg.evaluate("()=>performance.now()"); ims=[]
    r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}")
    for ms in (250,1000,1500,2100):
        pg.wait_for_function("(t)=>performance.now()>=t",arg=t0+ms); pg.screenshot(path='/tmp/m.png',clip={'x':r[0],'y':r[1]+180,'width':390,'height':230}); ims.append(Image.open('/tmp/m.png').convert('RGB'))
    W=Image.new('RGB',(1170,4*700),'white')
    for i,im in enumerate(ims): W.paste(im,(0,i*700))
    W.save('planche-v139/main-tenir.png'); print(er, pg.evaluate("()=>JSON.stringify(GesteFantome.regle)")); b.close()
