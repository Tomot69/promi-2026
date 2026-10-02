import sys
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
J = r"""()=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data, R=0.392*W, c=W/2; const h={}; 
  for(const [a,b,nom] of [[0,0.5,'coeur'],[0.5,0.9,'milieu'],[0.9,0.985,'bord'],[0.985,1.0,'limbe'],[1.0,1.06,'poil']]){ let n=0,s=0,p=0,mn=255; for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const r=Math.hypot(x-c,y-c)/R; if(r<a||r>=b) continue; const al=d[(y*W+x)*4+3]; n++; s+=al; if(al>=255) p++; if(al<mn) mn=al; } h[nom]={moy:+(s/n).toFixed(1), pleins:+(100*p/n).toFixed(1), min:mn}; }
  return h; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for d in (0, 1):
        ouvre(pg, d); pg.wait_for_timeout(2500); print('sombre' if d else 'clair', pg.evaluate(J))
        pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    b.close()
