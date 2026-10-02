import sys, io
sys.path.insert(0,'.'); 
from playwright.sync_api import sync_playwright
from PIL import Image, ImageStat
S=3
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800); pg.evaluate(OUVRE); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(5000)
    print('carte', pg.evaluate("()=>{const c=_peloteLumiere.carte(); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0,sa=0,mx=0,h={}; for(let i=0;i<d.length;i+=4){ if(d[i+3]){ n++; sa+=d[i+3]; if(d[i+3]>mx)mx=d[i+3]; } } const k=((c.width>>1)*c.width+(c.width>>1))*4; return {n:c.width, pleins:n, alphaMoy:+(sa/Math.max(1,n)).toFixed(1), alphaMax:mx, centre:[d[k],d[k+1],d[k+2],d[k+3]]}}"))
    pg.evaluate("(t)=>{closeAll();}"); pg.wait_for_timeout(1500); pg.evaluate(OUVRE); pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); pg.wait_for_timeout(1500); print('carte', pg.evaluate("()=>{const c=_peloteLumiere.carte(); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0,sa=0,mx=0,h={}; for(let i=0;i<d.length;i+=4){ if(d[i+3]){ n++; sa+=d[i+3]; if(d[i+3]>mx)mx=d[i+3]; } } const k=((c.width>>1)*c.width+(c.width>>1))*4; return {n:c.width, pleins:n, alphaMoy:+(sa/Math.max(1,n)).toFixed(1), alphaMax:mx, centre:[d[k],d[k+1],d[k+2],d[k+3]]}}")); print('--- seconde ouverture')
    for i in range(3):
        pg.wait_for_timeout(330)
        e=pg.evaluate("()=>{const s=_peloteLumiere.etat(); return [+(_peloteSouffle.t()||0).toFixed(2), +s.u.toFixed(3), s.calibrages, _aura.etat().pret, _aura.etat().tick]}")
        im=Image.open(io.BytesIO(pg.screenshot(clip={'x':20+195-70,'y':44+270-70,'width':140,'height':140}))).convert('L')
        print(e, round(ImageStat.Stat(im).mean[0],2))
    b.close()
