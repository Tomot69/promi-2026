# Madrure sous charge : quand les graines cessent-elles de bouger (Toile_probe), et quand la boucle s'arrête-t-elle ?
from playwright.sync_api import sync_playwright
SEME="let s=777; Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; "
REC=r"""()=>{ const W=window; W.__S=[]; const t0=performance.now(); let prev=JSON.stringify(Toile_probe());
 (function f(){ const t=performance.now()-t0; if(t>6000) return; const p=JSON.stringify(Toile_probe()); const st=Toile_state();
   W.__S.push([Math.round(t), p!==prev?1:0, st.running?1:0, W._madGPU?Math.round(W._madGPU.t):0, W._mondeEncore?1:0]); prev=p; requestAnimationFrame(f); })();
 const P=W.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for br in (1,3):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
        pg.evaluate("m=>{ "+SEME+"Toile.setTheme(m); }",'madrure'); pg.wait_for_timeout(3000)
        cdp.send('Emulation.setCPUThrottlingRate',{'rate':br}); pg.wait_for_timeout(800)
        pg.evaluate(REC); pg.wait_for_timeout(7000); S=pg.evaluate("()=>window.__S")
        bouge=[s[0] for s in S if s[1]]; run=[s[0] for s in S if s[2]]; enc=[s[0] for s in S if s[4]]
        print('×%d graines bougent jusqu\'à %s ms · boucle jusqu\'à %s ms · _mondeEncore jusqu\'à %s · GPU %s' % (br, bouge[-1] if bouge else None, run[-1] if run else None, enc[-1] if enc else None, S[-1][3]!=0))
        ctx.close()
    b.close()
