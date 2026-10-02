import sys, io
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{Toile.setPalette('signal'); window.__R=Math.random; Math.random=function(){return 0.125;};}")
    ouvre(pg, 0); pg.evaluate("()=>{Math.random=window.__R}"); pg.wait_for_timeout(4000); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(600)
    print(pg.evaluate("""()=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data; const o=[]; 
      for(const [x,y] of [[100,150],[60,120],[150,90],[20,20],[296,20],[560,296]]) o.push([x,y,d[(y*W+x)*4],d[(y*W+x)*4+1],d[(y*W+x)*4+2],d[(y*W+x)*4+3]]);
      return {W:W, css:cv.getBoundingClientRect().width, px:o, autres:[...document.querySelectorAll('#auCadre canvas')].map(c=>c.id+' '+c.className+' '+c.width+'×'+c.height+' '+getComputedStyle(c).display)}; }"""))
    print(pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('#auCadre > *, #auCadre .au-bo > *')].map(e=>{const r=e.getBoundingClientRect(), c=getComputedStyle(e); return (e.id||e.className||e.tagName)+' '+Math.round(r.left-dv.left)+','+Math.round(r.top-dv.top)+' '+Math.round(r.width)+'×'+Math.round(r.height)+' bg:'+c.backgroundImage.slice(0,40)+' '+c.backgroundColor+' sh:'+c.boxShadow.slice(0,30)+' r:'+c.borderRadius}).slice(0,12)}"))
    import base64
    u = pg.evaluate("()=>document.getElementById('auBoule').toDataURL('image/png')"); open('scratchpad/v119/cv-clair.png','wb').write(base64.b64decode(u.split(',')[1]))
    print(pg.evaluate("()=>{const cv=document.getElementById('auBoule'), W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data; let x0=W,y0=W,x1=0,y1=0,n=0; for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const r=Math.hypot(x-295.5,y-295.5); if(r<246) continue; const a=d[(y*W+x)*4+3]; if(a){ n++; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } } return ['hors silhouette', n, x0,y0,x1,y1]; }"))
    for h in ('#auBoule',):
        pg.evaluate("(s)=>{document.querySelector(s).style.visibility='hidden'}", h); pg.wait_for_timeout(300)
        pg.screenshot(path='scratchpad/v119/dbg-sans.png', clip={'x':20,'y':134,'width':390,'height':330})
    pg.screenshot(path='scratchpad/v119/dbg-clair.png', clip={'x':20,'y':134,'width':390,'height':330})
    b.close()
