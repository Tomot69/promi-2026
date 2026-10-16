from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    for nom, b in (('chromium', p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])), ('webkit', p.webkit.launch())):
        ctx = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True)
        ctx.add_init_script("try{ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); }catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} TraceLettres.mesures.prep.length=0; TraceLettres.mesures.image.length=0; _guide.montre('studio'); }")
        pg.wait_for_timeout(9000)
        m = pg.evaluate("()=>({prep:TraceLettres.mesures.prep.slice(), image:TraceLettres.mesures.image.slice()})")
        pr = sorted(m['prep']); im = sorted(m['image'])
        f = lambda L, q: round(L[min(len(L)-1, int(q*len(L)))], 1) if L else None
        print(nom, 'prep n', len(pr), 'médiane', f(pr,.5), 'p90', f(pr,.9), 'max', f(pr,1), '| image n', len(im), 'médiane', f(im,.5), 'p95', f(im,.95), 'max', f(im,1))
        b.close()
