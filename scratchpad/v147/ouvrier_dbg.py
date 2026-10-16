from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for nom, b in (('webkit', p.webkit.launch()),):
        ctx = b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3)
        ctx.add_init_script("try{ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); }catch(e){}")
        pg = ctx.new_page(); errs=[]; pg.on('console', lambda m: errs.append(m.text[:160]) if m.type in ('error','warning') else None)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        r = pg.evaluate("""async ()=>{ const d=document.createElement('div'); d.style.cssText='position:absolute;left:10px;top:200px;width:340px;font:500 27px/32px Atkinson,system-ui;color:#291547'; d.textContent='Choisis d’abord le monde qui te ressemble, au Studio.'; document.getElementById('device').appendChild(d);
           TraceLettres.mesures.prep.length=0; TraceLettres.mesures.image.length=0; TraceLettres._cache={}; TraceLettres._dbgT=[]; const t0=performance.now(); const c=TraceLettres.trace(d,null,{cps:50}); await c.fin; const t=performance.now()-t0;
           return {duree:Math.round(t), prevue:Math.round(c.duree), ouvrier:String(TraceLettres._ouvrier), prep:TraceLettres.mesures.prep.map(x=>Math.round(x)), image:TraceLettres.mesures.image.map(x=>Math.round(x)), cache:TraceLettres.mesures.cache, dbg:TraceLettres._dbgT}; }""")
        print('  dbg', r['dbg']); print(nom, r['duree'], 'ms (prévue', r['prevue'], ') ouvrier', r['ouvrier'], 'cache', r['cache']); print('  prep', r['prep']); print('  image', r['image']); pass
        b.close()
