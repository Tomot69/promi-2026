import sys, base64, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
SONDE="""()=>{ window.__fr=[]; const t0=performance.now(); const c=document.getElementById('toileCv'); let der=null;
  function h(){ const s=document.createElement('canvas'); s.width=48; s.height=96; const g=s.getContext('2d'); g.drawImage(c,0,0,48,96); const d=g.getImageData(0,0,48,96).data; let x=0; for(let i=0;i<d.length;i+=4) x=(x*31+d[i]+d[i+1]*3+d[i+2]*7)>>>0; return [x,s.toDataURL()]; }
  (function f(){ const t=performance.now()-t0; const st=document.getElementById('studioScreen'), D=document.getElementById('device').getBoundingClientRect(); const top=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.4); const vu=top&&(top.id==='toileCv'||!st.contains(top));
    const [x,u]=h(); if(x!==der){ der=x; window.__fr.push([Math.round(t), vu, u]); } else if(window.__fr.length && window.__fr[window.__fr.length-1][1]!==vu) window.__fr.push([Math.round(t), vu, null]);
    if(t<3000) requestAnimationFrame(f); })(); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,25); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    for i in range(12):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1800)
    w=pg.evaluate("()=>window._lockedWorld"); print('monde', w, pg.evaluate("()=>Toile.mondeCourant().m"))
    c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(300)
    if '--rend' in sys.argv: print('renderTo', pg.evaluate("()=>{ const c=document.getElementById('toileCv'); const t0=performance.now(); const ok=Toile.renderTo(c, c.width/390, null, {vue:true}); return [ok, Math.round(performance.now()-t0), c.width, c.height]; }"))
    pg.wait_for_timeout(1200)
    pg.evaluate(SONDE); B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(3200)
    fr=pg.evaluate("()=>window.__fr"); os.makedirs('scratchpad/v155/fr6',exist_ok=True)
    for j,f in enumerate(fr):
        print(f[0], f[1], bool(f[2]))
        if f[2]: open('scratchpad/v155/fr6/%02d_%d.png'%(j,f[0]),'wb').write(base64.b64decode(f[2].split(',')[1]))
    b.close()
