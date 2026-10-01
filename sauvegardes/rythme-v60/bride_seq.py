import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1]; BR=[float(x) for x in sys.argv[2].split(',')]
src=open('redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]
SEME="let s=777; Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; "
SEQ=r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; return W.__R.filter(r=>r[0]>=T0).map(r=>[Math.round(r[0]-T0), +r[1].toFixed(1)]); }"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for br in BR:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
        pg.evaluate("m=>{ "+SEME+"Toile.setTheme(m); }", M); pg.wait_for_timeout(3000)
        cdp.send('Emulation.setCPUThrottlingRate',{'rate':br}); pg.wait_for_timeout(1000)
        pg.evaluate(ENREG); pg.evaluate("()=>{window.__arme='add'; window.__t=performance.now(); const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); window.__tsync=performance.now()-window.__t; }")
        pg.wait_for_timeout(5000); s=pg.evaluate(SEQ)
        print('×%g sync %d ms :'%(br, pg.evaluate("()=>window.__tsync")), [x for x in s if x[1]>0.3][:40])
        ctx.close()
    b.close()
