from playwright.sync_api import sync_playwright
J = r"""([ton,fond])=>{ const W=592, cv=window._haloPelote(W, 0.392*W, W*(296*0.392+5)/296, W*0.392*2*0.08, ton, fond, false); const d=cv.getContext('2d').getImageData(0,0,W,W).data;
  let x0=W,y0=W,x1=0,y1=0,mx=0; for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const a=d[(y*W+x)*4+3]; if(a){ if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; if(a>mx)mx=a; } }
  const prof=[]; for(let r=225;r<285;r+=4){ const x=Math.round(295.5-0.626*r), y=Math.round(295.5-0.778*r); prof.push(r+':'+d[(y*W+x)*4+3]); }
  return {bbox:[x0,y0,x1,y1], max:mx, profil:prof.join(' ')}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    print('clair ', pg.evaluate(J, [[23,121,229],[247,240,222]]))
    print('sombre', pg.evaluate(J, [[237,244,255],[5,3,2]]))
    b.close()
