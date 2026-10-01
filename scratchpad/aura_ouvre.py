from playwright.sync_api import sync_playwright
import sys
def ouvre(pg, dark):
    pg.evaluate("()=>{closeAll();setTheme(%s)}"%("'dark'" if dark else "'light'")); pg.wait_for_timeout(800)
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4000)
if __name__=='__main__':
  with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for d in (0,1):
        ouvre(pg,d)
        print(pg.evaluate("""()=>{var c=document.getElementById('auBoule'),r=c.getBoundingClientRect(),s=document.getElementById('auraScreen');return [Math.round(r.x),Math.round(r.y),Math.round(r.width),getComputedStyle(s).backgroundColor, c.parentElement.id, c.parentElement.className]}"""))
        pg.screenshot(path='scratchpad/aura_now%d.png'%d,clip={'x':20,'y':44,'width':390,'height':844})
