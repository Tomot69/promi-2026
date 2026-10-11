import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_rappel_n','9'); }catch(e){}"%th)
        pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
        D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        for et in ('studio','plus'):
            L=[]
            pg.evaluate("(q)=>{ _guide.montre(q); }",et); pg.wait_for_timeout(150)
            for ms in (0,400,800,1200,1600):
                pg.evaluate("(ms)=>_guide.figeA(ms)",ms); pg.wait_for_timeout(200)
                im=Image.open(io.BytesIO(pg.screenshot(clip={'x':D[0],'y':D[1],'width':D[2],'height':D[3]}))).convert('RGB'); im.save('planche-v143/guide-%s-%s-%04d.png'%(et,th,ms)); L.append(im.resize((390,844)))
            W=Image.new('RGB',(5*400,844),'white')
            for i,a in enumerate(L): W.paste(a,(i*400,0))
            W.save('scratchpad/v143/gvue-%s-%s.png'%(et,th)); pg.evaluate("()=>_guide.finir()"); pg.wait_for_timeout(700)
        print(th,er, pg.evaluate("()=>JSON.stringify(_guide.etat())")); ctx.close()
    b.close()
