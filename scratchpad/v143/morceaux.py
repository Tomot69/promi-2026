import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter'].forEach(k=>localStorage.setItem('geste_vu_'+k,'1'));localStorage.setItem('geste_v','143');}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    for k in range(3):
        pg.evaluate("""()=>{ closeAll(); const p=promises.filter(q=>q.status!=='tenu'&&!q.draft&&!q.nuee&&!q.req)[0]; openDetail(p.id); }"""); pg.wait_for_timeout(2500)
        pg.evaluate("""()=>{ window.__T=[]; if(!window.__enf){ window.__enf=1; ['_tenirCorps','_fichePoseBase','_lot7Fiche','_ficheTrait','_ficheCotes','_fichePose','_repasseSombre','renderDetail','_ficheDalle','syncAll'].forEach(n=>{ const f=window[n]; if(typeof f!=='function') return; window[n]=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally { window.__T.push([n, Math.round(t-window.__c), Math.round((performance.now()-t)*10)/10]); } }; }); }
          window.__c=performance.now(); document.querySelector('#segStatus button[data-st="tenu"]').click(); }"""); pg.wait_for_timeout(3600)
        print([e for e in pg.evaluate("()=>window.__T") if e[2]>=4])
    b.close()
