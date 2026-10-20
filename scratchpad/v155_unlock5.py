import sys, time, json, base64, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
SONDE="""()=>{ window.__fr=[]; const t0=performance.now(); 
  function cvs(){ return [...document.querySelectorAll('#studioScreen canvas, #toileCv')].filter(c=>c.width>40 && c.getBoundingClientRect().width>40); }
  function h(c){ try{ const s=document.createElement('canvas'); s.width=48; s.height=96; const g=s.getContext('2d'); g.drawImage(c,0,0,48,96); const d=g.getImageData(0,0,48,96).data; let x=0; for(let i=0;i<d.length;i+=4) x=(x*31+d[i]+d[i+1]*3+d[i+2]*7)>>>0; return [x, s.toDataURL()]; }catch(e){ return [0,null]; } }
  const der={};
  (function f(){ const t=performance.now()-t0; cvs().forEach(c=>{ const k=c.id||c.className||'?'; const [x,u]=h(c); const cs=getComputedStyle(c); const v=cs.opacity+'|'+cs.visibility+'|'+cs.filter+'|'+cs.display; const kk=x+'/'+v; if(der[k]!==kk){ der[k]=kk; window.__fr.push([Math.round(t), k, v, u]); } });
    if(t<3000) requestAnimationFrame(f); })(); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx, 25); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    os.makedirs('scratchpad/v155/fr5',exist_ok=True); vus=set()
    for i in range(24):
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1800)
        w=pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')?window._lockedWorld:null")
        if not w or w in vus: continue
        vus.add(w)
        c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
        pg.evaluate(SONDE); pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(3300)
        fr=pg.evaluate("()=>window.__fr")
        print(w, [(f[0],f[1],f[2]) for f in fr])
        for j,f in enumerate(fr):
            if f[3]: open('scratchpad/v155/fr5/%s_%02d_%s_%d.png'%(w,j,f[1],f[0]),'wb').write(base64.b64decode(f[3].split(',')[1]))
    b.close()
