from playwright.sync_api import sync_playwright
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
E="""()=>{ const D=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('stpPals'); const vis=e=>{const r=e.getBoundingClientRect(), s=getComputedStyle(e); return r.width>0&&s.display!=='none'&&s.visibility!=='hidden'&&+s.opacity>0.05};
  const all=[...document.querySelectorAll('#studioScreen .st3-pals')].map(r=>{const b=r.getBoundingClientRect(); const k=[...r.children]; const kb=k[0]?k[0].getBoundingClientRect():{width:0}; return {dansPanneau:!!r.closest('#stpPals'), vis:vis(r), y:Math.round(b.top-D.top), h:Math.round(b.height), n:k.length, orbe:Math.round(kb.width), teintes:k[0]?k[0].querySelectorAll('.st3-q').length:0}});
  return {cls:document.getElementById('studioScreen').className.replace('screen s-studio',''), rangees:all, noms:[...document.querySelectorAll('#studioScreen #st3pn, #studioScreen .st3-pn')].map(e=>e.textContent+(vis(e)?'':'(caché)')), panneau:P?vis(P):null} }"""
def tap(pg,sel):
    c=pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].filter(x=>x.getBoundingClientRect().width>0)[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}",sel)
    if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1300)
    return bool(c)
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(500)
    def shot(n): pg.screenshot(path=SC+'p2-%s.png'%n, clip={'x':20,'y':44,'width':390,'height':844})
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500); print('ouvert', pg.evaluate(E)); shot('a')
    tap(pg,'#studioScreen .stp-ton'); print('menu', pg.evaluate(E))
    tap(pg,'#stpPals .stp-nb'); print('après clair/sombre', pg.evaluate(E)); shot('b')
    tap(pg,'#stpPals .stp-nb'); print('retour sombre', pg.evaluate(E)); shot('c')
    tap(pg,'#stpPals .stp-retour'); print('RETOUR', pg.evaluate(E)); shot('d')
    # glisser de monde
    pg.mouse.move(300,300); pg.mouse.down(); [pg.mouse.move(300-i*20,300) for i in range(1,10)]; pg.mouse.up(); pg.wait_for_timeout(2500); print('monde suivant', pg.evaluate(E)); shot('e')
    tap(pg,'#studioScreen .stp-ton'); print('menu 2', pg.evaluate(E)); shot('f')
    pg.evaluate("()=>{const c=document.querySelector('#studioScreen .closeb'); if(c) c.click();}"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500); print('rouvert', pg.evaluate(E)); shot('g')
    b.close()
