import sys
from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(500)
        pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500)
        c=pg.evaluate("()=>{const t=document.querySelector('#studioScreen .stp-ton'); const r=t.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}"); pg.touchscreen.tap(*c); pg.wait_for_timeout(1200)
        print(th, pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('stpPals'); const r=P.getBoundingClientRect(), cs=getComputedStyle(P);
          const O=[...P.querySelectorAll('.st3-pals > *')].map(e=>{const q=e.getBoundingClientRect(); return [Math.round(q.left-dv.left),Math.round(q.top-dv.top),Math.round(q.width),Math.round(q.height)]});
          return {panneau:[Math.round(r.left-dv.left),Math.round(r.top-dv.top),Math.round(r.width),Math.round(r.height)], of:cs.overflow+'/'+cs.overflowY, sh:P.scrollHeight, ch:P.clientHeight, n:O.length, rangs:P.querySelectorAll('.st3-pals').length, premiers:O.slice(0,7), derniers:O.slice(-3), nom:(document.getElementById('st3pn')||{}).textContent, enfants:[...P.children].map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,20))}; }"""))
        pg.screenshot(path=SC+'pal-%s.png'%th, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(SC+'pal-%s.png'%th)
        pg.evaluate("()=>{const P=document.getElementById('stpPals'); P.scrollTop=P.scrollHeight; const q=P.querySelector('.st3-pals'); if(q) q.scrollTop=q.scrollHeight;}"); pg.wait_for_timeout(500)
        pg.screenshot(path=SC+'pal-%s-bas.png'%th, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(SC+'pal-%s-bas.png'%th)
        ctx.close()
    L=[Image.open(f) for f in ims]; P=Image.new('RGB',(400*len(L),844),(255,255,255))
    for i,im in enumerate(L): P.paste(im.resize((390,844)),(i*400,0))
    P.save(SC+'pal.png'); b.close()
