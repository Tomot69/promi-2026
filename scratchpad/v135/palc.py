from playwright.sync_api import sync_playwright
import sys
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
ETAT="""()=>{ const D=document.getElementById('device').getBoundingClientRect(); const st=document.getElementById('studioScreen'); const P=document.getElementById('stpPals');
  const q=e=>{ if(!e) return null; const r=e.getBoundingClientRect(), s=getComputedStyle(e); return {x:Math.round(r.left-D.left), y:Math.round(r.top-D.top), w:Math.round(r.width), h:Math.round(r.height), d:s.display, v:s.visibility, o:s.opacity}; };
  const pals=P?[...P.querySelectorAll('.st3-pals > *')]:[];
  return {cls:st.className, stpPals:q(P), n:pals.length, p0:pals[0]?{...q(pals[0]), html:pals[0].outerHTML.slice(0,300), bg:getComputedStyle(pals[0]).backgroundImage.slice(0,120), bgc:getComputedStyle(pals[0]).backgroundColor}:null,
    rangees:P?[...P.children].map(c=>(c.id||c.className)+' '+JSON.stringify(q(c))):[], dots:q(document.getElementById('stpDots')), nom:(document.getElementById('st3pn')||{}).textContent} }"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(500)
        for k in (1,2,3):
            pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500)
            c=pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
            if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1200)
            e=pg.evaluate(ETAT); print(th,k,{x:e[x] for x in ('stpPals','n','nom','dots')}); 
            if k==1 and th=='dark': print(e['p0']); print(e['rangees']); print(e['cls'])
            pg.screenshot(path=SC+'palc-%s-%d.png'%(th,k), clip={'x':20,'y':44,'width':390,'height':844})
            pg.evaluate("()=>{const c=document.querySelector('#studioScreen .closeb'); if(c) c.click();}"); pg.wait_for_timeout(1200)
        ctx.close()
    b.close()
