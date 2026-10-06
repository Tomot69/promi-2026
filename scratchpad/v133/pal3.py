from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); try{setPremium(false)}catch(e){} }"); pg.wait_for_timeout(500)
    def tap(sel,i=0):
        c=pg.evaluate("([s,i])=>{const t=[...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().width>0)[i]; if(!t) return null; const r=t.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", [sel,i])
        if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1000)
        return c
    def prise(lab):
        pg.screenshot(path=SC+'p3-%d.png'%len(ims), clip={'x':20,'y':44,'width':390,'height':844}); ims.append(SC+'p3-%d.png'%len(ims))
        print(lab, pg.evaluate("()=>{const sc=document.getElementById('studioScreen'), P=document.getElementById('stpPals'); return [sc.className, Toile.getTheme(), Toile.getPalette(), P?P.querySelectorAll('.st3-pals').length:null, P?P.querySelectorAll('.st3-pals > *').length:null, P?getComputedStyle(P).filter:null, [...document.querySelectorAll('#studioScreen [id^=stp]')].filter(e=>e.getBoundingClientRect().width>0).map(e=>e.id+':'+getComputedStyle(e).filter).join(' ')]}"))
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500)
    mondes=pg.evaluate("()=>{try{return Toile.themes?Toile.themes():null}catch(e){return null}}"); print('mondes', mondes)
    for m in ('ramage','madrure','houle' if False else 'sillons','chamade'):
        pg.evaluate("(m)=>{ try{ if(window.stSetWorld) stSetWorld(m); else Toile.setTheme(m); if(typeof buildStudio==='function') buildStudio(); }catch(e){ console.log(e) } }", m); pg.wait_for_timeout(2500)
        prise('monde '+m); tap('#studioScreen .stp-ton'); prise('menu sous '+m); tap('#stpPals .st3-pals > *', 7); prise('pastille 8 sous '+m)
        tap('#stpPals .stp-retour'); 
    L=[Image.open(f) for f in ims]; P=Image.new('RGB',(400*len(L),844),(255,255,255))
    for i,im in enumerate(L): P.paste(im,(i*400,0))
    P.resize((P.size[0]//2,422)).save(SC+'pal3.png'); b.close()
