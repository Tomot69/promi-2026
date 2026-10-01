from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setPremium(false);closeAll();ouvreCercle()}"); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>{const o=[];const w=document.createTreeWalker(document.getElementById('plusScreen'),NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(!t)continue;const e=n.parentElement;const r=e.getBoundingClientRect();const s=getComputedStyle(e);if(r.width&&s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity>0)o.push(e.className+' | '+t+' | '+Math.round(r.top));}return o.join('\\n')}"""))
    pg.screenshot(path='scratchpad/offre.png')
