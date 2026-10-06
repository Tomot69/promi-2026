from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
def n(pg,i): pg.evaluate("(i)=>{window._murBaisse&&_murBaisse(); localStorage.setItem('promi_murs',JSON.stringify({n:i,t:Date.now(),der:i-1,decouvert:1}))}", i)
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); setPremium(false);}",th); pg.wait_for_timeout(500)
        # 1 · Peaufiner d'une fiche Promi — phrase 3
        pg.evaluate("()=>{closeAll(); openDetail(128);}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
        c=pg.evaluate("()=>{const q=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        n(pg,2); pg.touchscreen.tap(*c); pg.wait_for_timeout(1100); f=SC+'mur-%s-1.png'%th; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        # 2 · Aura — phrase 8
        n(pg,7); pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
        a=pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2')||document.querySelector('#auraScreen .au-gr2');const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        n(pg,7); pg.touchscreen.tap(*a); pg.wait_for_timeout(1300); f=SC+'mur-%s-2.png'%th; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        # 3 · les teintes du dessin — phrase 2
        pg.evaluate("()=>{window._murBaisse&&_murBaisse(); closeAll(); openDetail(127);}"); pg.wait_for_timeout(2400)
        pg.evaluate("()=>window._dessin.ouvre()"); pg.wait_for_timeout(400)
        pg.mouse.move(120,300); pg.mouse.down(); [pg.mouse.move(120+i*9,300+(i%6)*11) for i in range(22)]; pg.mouse.up(); pg.wait_for_timeout(200)
        pg.touchscreen.tap(20+24+3*58+22, 44+754+22); pg.wait_for_timeout(400)
        n(pg,1); pg.touchscreen.tap(20+195, 44+680); pg.wait_for_timeout(1100); f=SC+'mur-%s-3.png'%th; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        print(th, pg.evaluate("()=>document.getElementById('murPhrase').textContent"))
        ctx.close()
    W,H=1170,2532; P=Image.new('RGB',(3*W+4*60,2*H+3*60),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f),(60+(i%3)*(W+60),60+(i//3)*(H+60)))
    P.save('planche-v133/murs.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v133/murs-tel.png'); b.close()
