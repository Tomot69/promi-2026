from playwright.sync_api import sync_playwright
from PIL import Image
SC='scratchpad/v135/'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_studio_glisse','1')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); setPremium(true)}",th); pg.wait_for_timeout(500)
        def cap(n): f=SC+'d-%s-%s.png'%(n,th); pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        pg.evaluate("()=>{closeAll(); openDetail(128);}"); pg.wait_for_timeout(3000); cap('fiche')
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1700); cap('peauf')
        pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click()}"); pg.wait_for_timeout(3000); cap('studio')
        ctx.close()
    W,H=1170,2532; P=Image.new('RGB',(6*W+7*50,H+100),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f),(50+i*(W+50),50))
    P.save('planche-v135/divers.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v135/divers-tel.png'); b.close()
