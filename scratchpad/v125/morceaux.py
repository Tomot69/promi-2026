from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for mot in ('chromium','webkit'):
        b = p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']) if mot=='chromium' else p.webkit.launch()
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} const p=promises.filter(x=>x.title==='planter un arbre')[0]; openDetail(p.id);}"); pg.wait_for_timeout(3000)
        print(mot, pg.evaluate("""()=>{ const T=(f)=>{ const a=[]; for(let i=0;i<5;i++){ const t=performance.now(); f(); document.body.offsetHeight; a.push(performance.now()-t); } a.sort((x,y)=>x-y); return +a[2].toFixed(1); };
          return {corps:T(()=>_tenirCorps()), poseBase:T(()=>_fichePoseBase()), pose:T(()=>_fichePose()), cotes:T(()=>_ficheCotes()), trait:T(()=>_ficheTrait()), repasse:T(()=>_repasseSombre()), renderDetail:T(()=>renderDetail())}; }"""))
        b.close()
