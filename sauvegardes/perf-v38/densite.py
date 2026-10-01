# Le régulateur de densité de la Pelote sous ×6 : combien d'images ordinaires par seconde, et quand décide-t-il ?
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for essai in range(3):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{localStorage.removeItem('promi_pelote_palier')}catch(e){} closeAll(); document.getElementById('souffleBtn').click();}")
        pg.wait_for_timeout(5000)
        e0=pg.evaluate("()=>_aura.etat()"); pg.evaluate("()=>_aura.palier(0)")
        cdp=ctx.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':6})
        L=pg.evaluate("""()=>new Promise(res=>{ const t0=performance.now(), out=[]; let n=0, last=0;
          (function f(t){ n++; const e=_aura.etat(); if(t-last>2000){ last=t; out.push([Math.round((t-t0)/100)/10, n, e.frames, e.ms&&Math.round(e.ms), e.cede, e.vise, e.palier]); }
            if(t-t0>40000) return res(out); requestAnimationFrame(f); })(performance.now()); })""")
        cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
        print('essai',essai,'palier au départ',e0['palier'])
        for r in L: print('   t %5.1fs  rAF %4d  ordinaires %4d  médiane %s ms  cède %s  vise %s  palier %s' % tuple(r))
        ctx.close()
    b.close()
