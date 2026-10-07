from playwright.sync_api import sync_playwright
import sys
TAG=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(1200)
        print(th, pg.evaluate("""()=>{const D=document.getElementById('device').getBoundingClientRect(); const q=e=>{const r=e.getBoundingClientRect(); return [r.left-D.left,r.top-D.top,r.width,r.height].map(v=>Math.round(v*10)/10)};
          const B=document.querySelector('.acc-barre'); return {barre:q(B), plus:q(document.getElementById('createBtn')), svg:q(document.querySelector('#createBtn svg')), enfants:[...B.children].map(c=>(c.id||c.className)+' '+q(c).join(','))}}"""))
        pg.screenshot(path='scratchpad/v136/plus-%s-%s.png'%(TAG,th), clip={'x':20,'y':44,'width':390,'height':844}); ctx.close()
    b.close()
