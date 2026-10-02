from playwright.sync_api import sync_playwright
M = r"""()=>{ const o={}; for(const s of ['#detailPoster #dptNat','#detailPoster .closeb','#detailPoster .enh']){ const e=document.querySelector(s); if(!e){o[s]=null;continue;} const c=getComputedStyle(e); o[s]=c.color+' / fond '+c.backgroundColor+' / op '+c.opacity; } o.dev=document.getElementById('device').className; return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, timezone_id='Europe/Paris')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    for sens, t1, t2 in (('clair→nuit', '2026-12-21T15:00:00+01:00', '2026-12-21T19:00:00+01:00'), ('nuit→clair', '2026-12-21T19:00:00+01:00', '2026-12-22T10:00:00+01:00')):
        pg.evaluate("(iso)=>{ window.__t=Date.parse(iso); window._zzzMaintenant=()=>window.__t; setTheme('light'); _zzz.regle(true); closeAll(); }", t1); pg.wait_for_timeout(1500)
        pg.evaluate("(iso)=>{ window.__t=Date.parse(iso); const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.chiche&&q.status!=='tenu'); openDetail(p.id); }", t2); pg.wait_for_timeout(2500)
        print(sens, pg.evaluate(M)); pg.screenshot(path='scratchpad/v118/zzz-fiche-%s.png' % sens[:5], clip={'x':20,'y':44,'width':390,'height':500})
    b.close()
