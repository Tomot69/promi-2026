from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0,'scratchpad')
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','5')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?mesure=1'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); document.getElementById('souffleBtn').click();}")
    pg.wait_for_timeout(27000)
    print(pg.evaluate("()=>document.getElementById('auMesure').textContent"))
    pg.screenshot(path='planche-v125/mesure-banc.png', clip={'x':20,'y':44,'width':390,'height':844})
    b.close()
