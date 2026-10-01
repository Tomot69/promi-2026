from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>new Promise(res=>{ const L=[]; const t0=performance.now(); let k=null; for(const q in NUE){k=q;break;} closeAll(); openNueeDetail(k);
      (function f(){ const t=performance.now()-t0; const D=Toile.dalleAbs(131); const c=Toile.colorOf&&Toile.colorOf(131);
        const s=D?[D.minx,D.miny,D.w,D.h].map(v=>Math.round(v*10)).join(','):'-'; const e=s+'|'+c+'|'+JSON.stringify(Toile_state());
        if(!L.length||L[L.length-1][1]!==e) L.push([Math.round(t),e]); if(t<3200) requestAnimationFrame(f); else res(L); })(); })"""))
    b.close()
