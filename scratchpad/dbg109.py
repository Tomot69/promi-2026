import sys
sys.argv=['x']
exec(open('redteam_notifs.py').read().split("with sync_playwright() as p:")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}"); ctx.add_init_script(FAUX)
    pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000)
    for js in ["()=>document.getElementById('settingsBtn').click()", "()=>document.getElementById('souffleBtn').click()", "()=>document.getElementById('indexBtn').click()"]:
        pg.evaluate("()=>closeAll()"); pg.evaluate(js); pg.wait_for_timeout(700)
    plante(pg,'lire au soleil','moi',4)
    print(pg.evaluate("""()=>{const q=document.getElementById('rapQuestion');const D=document.getElementById('device').getBoundingClientRect();
      const o=[...document.querySelectorAll('.screen.show')].map(e=>{const r=e.getBoundingClientRect();return e.id+' '+Math.round(Math.min(r.bottom,D.bottom)-Math.max(r.top,D.top))+' op'+getComputedStyle(e).opacity+' '+getComputedStyle(e).visibility});
      return [q.className, o, [...document.querySelectorAll('#device .sheet.show, #device .poster.show, #feedView.in')].map(e=>e.id)]}"""))
    pg.screenshot(path='scratchpad/dbg109.png')
    print(pg.evaluate("()=>{const s=document.getElementById('settingsScreen');const c=getComputedStyle(s);return [c.transform,c.zIndex,c.display,s.getBoundingClientRect().top]}"))
