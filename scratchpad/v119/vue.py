import sys, io
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image
pal = sys.argv[1] if len(sys.argv) > 1 else 'signal'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er=[]; pg.on('pageerror', lambda e: er.append(str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    ims=[]
    for d in (0, 1):
        pg.evaluate("(p)=>{Toile.setPalette(p); window.__R=Math.random; Math.random=function(){return 0.125;};}", pal)
        ouvre(pg, d); pg.evaluate("()=>{Math.random=window.__R}"); pg.wait_for_timeout(4000); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(600)
        print('sombre' if d else 'clair', pg.evaluate("()=>JSON.stringify([_peloteLumiere.etat(), window._auraErreur||null])"))
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44+90,'width':390,'height':420}))).convert('RGB'))
        pg.evaluate("()=>{_aura.fige(false); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    w,h=ims[0].size; pl=Image.new('RGB',(2*w+30,h),(128,128,128)); pl.paste(ims[0],(0,0)); pl.paste(ims[1],(w+30,0)); pl.save('scratchpad/v119/vue-%s.png'%pal)
    pl.resize(((2*w+30)//2, h//2)).save('scratchpad/v119/vue-%s-petit.png'%pal); print('err', er)
    b.close()
