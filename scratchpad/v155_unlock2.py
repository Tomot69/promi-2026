import sys, time, json, base64; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
SONDE="""()=>{ window.__fr=[]; const t0=performance.now(); const st=document.getElementById('studioScreen');
  function cvs(){ return [...st.querySelectorAll('canvas')].filter(c=>c.width>4 && c.getBoundingClientRect().width>4); }
  function h(c){ try{ const s=document.createElement('canvas'); s.width=24; s.height=24; const g=s.getContext('2d'); g.drawImage(c,0,0,24,24); const d=g.getImageData(0,0,24,24).data; let x=0; for(let i=0;i<d.length;i+=4) x=(x*31+d[i]+d[i+1]*3+d[i+2]*7)>>>0; return [x, s.toDataURL()]; }catch(e){ return [0,null]; } }
  const der={};
  (function f(){ const t=performance.now()-t0; cvs().forEach(c=>{ const k=c.id||c.className||'?'; const r=c.getBoundingClientRect(); const [x,u]=h(c); if(der[k]!==x){ der[k]=x; window.__fr.push([Math.round(t), k, Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height), u]); } });
    if(t<2500) requestAnimationFrame(f); })(); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    for i in range(12):
        lk=pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')")
        if lk: break
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1500)
    print(pg.evaluate("()=>[...document.getElementById('studioScreen').querySelectorAll('canvas')].map(c=>(c.id||c.className)+':'+c.width+'x'+c.height+':'+Math.round(c.getBoundingClientRect().top))"))
    c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.evaluate(SONDE); pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(3000)
    fr=pg.evaluate("()=>window.__fr")
    import os; os.makedirs('scratchpad/v155/fr',exist_ok=True)
    for i,f in enumerate(fr):
        print(f[:6])
        if f[6]: open('scratchpad/v155/fr/%03d_%s_%d.png'%(i,f[1].replace(' ','_')[:20],f[0]),'wb').write(base64.b64decode(f[6].split(',')[1]))
    b.close()
