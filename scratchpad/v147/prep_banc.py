from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for nom, b in (('webkit', p.webkit.launch()), ('chromium', p.chromium.launch())):
        ctx = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3)
        pg = ctx.new_page(); ctx.add_init_script("try{ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); }catch(e){}"); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        for sm in (4, 3, 2, 1):
            r = pg.evaluate("""async (sm)=>{ TraceLettres.supMax=sm; const d=document.createElement('div'); d.style.cssText='position:fixed;left:10px;top:200px;width:340px;font:500 27px/32px Atkinson,system-ui;color:#291547'; d.textContent='Choisis d’abord le monde qui te ressemble, au Studio.'; document.body.appendChild(d);
               await document.fonts.ready; TraceLettres.mesures.prep.length=0; const t0=performance.now(); const c=TraceLettres.trace(d,null,{cps:50, manuel:true}); await c.pret; TraceLettres.mesures.prep.length=0; const t0b=performance.now(); for(let k=1;k<=400;k++) c.va(k/401); const t=performance.now()-t0b; const pr=TraceLettres.mesures.prep.slice().sort((a,b)=>a-b); d.remove(); return {total:Math.round(t), n:pr.length, med:Math.round(pr[pr.length>>1]), max:Math.round(pr[pr.length-1])}; }""", sm)
            print(nom, 'supMax', sm, r)
        b.close()
