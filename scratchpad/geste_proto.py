from playwright.sync_api import sync_playwright
NOYAU = """async()=>{ const cv=document.getElementById('shCanvas'); const pn=performance.now; performance.now=()=>424242;
  const lire=()=>cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
  try{ document.getElementById('shNyOff').click(); shareRender(); await new Promise(r=>setTimeout(r,350)); const a=lire();
       document.getElementById('shNyOn').click(); shareRender(); await new Promise(r=>setTimeout(r,350)); const b=lire();
       let n=0,sx=0,sy=0; const W=cv.width;
       for(let i=0;i<a.length;i+=4){ if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>60){ const p=i/4; n++; sx+=p%W; sy+=(p/W)|0; } }
       return {n, cx: n? sx/n/W : null, cy: n? sy/n/cv.height : null}; }
  finally{ performance.now=pn; } }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(5200)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}"); pg.wait_for_timeout(2000)
    pg.evaluate("()=>{const t=document.getElementById('shTrayBtn'); if(t)t.click();}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{document.getElementById('shNyOn').click();}"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const w=document.getElementById('shTrayWrap');if(w)w.classList.remove('open');document.body.click();}"); pg.wait_for_timeout(900)
    for x,y in ((0.5,0.55),(0.3,0.32),(0.5,0.84)):
        pg.evaluate("a=>{window.shNyX=a[0];window.shNyY=a[1];shareRender();}",[x,y]); pg.wait_for_timeout(700)
        for k in range(2): print((x,y), pg.evaluate(NOYAU))
