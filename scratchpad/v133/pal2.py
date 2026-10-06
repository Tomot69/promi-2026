import sys
from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for vp,th in (((390,700),'dark'),((390,700),'light'),((430,932),'dark')):
        ctx=b.new_context(viewport={'width':vp[0],'height':vp[1]},device_scale_factor=2,has_touch=True,is_mobile=True)
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{setPremium(false)}catch(e){} }", th); pg.wait_for_timeout(500)
        pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500)
        def tap(sel,i=0):
            c=pg.evaluate("([s,i])=>{const t=[...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().width>0)[i]; if(!t) return null; const r=t.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", [sel,i])
            if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(900)
            return c
        tap('#studioScreen .stp-ton'); pg.screenshot(path=SC+'p2-%d.png'%len(ims)); ims.append(SC+'p2-%d.png'%len(ims))
        for i in (5,13,20):
            tap('#stpPals .st3-pals > *', i); pg.screenshot(path=SC+'p2-%d.png'%len(ims)); ims.append(SC+'p2-%d.png'%len(ims))
        print(vp, th, pg.evaluate("()=>[document.getElementById('studioScreen').className, Toile.getPalette(), !!document.querySelector('#murPhrase.leve')]"))
        ctx.close()
    L=[Image.open(f) for f in ims]; h=max(i.size[1] for i in L)//2; P=Image.new('RGB',(sum(i.size[0]//2+8 for i in L),h),(255,255,255)); x=0
    for im in L: P.paste(im.resize((im.size[0]//2,im.size[1]//2)),(x,0)); x+=im.size[0]//2+8
    P.save(SC+'pal2.png'); print(P.size); b.close()
