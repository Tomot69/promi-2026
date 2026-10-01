from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
    pg.wait_for_timeout(2600)
    print(pg.evaluate(r"""()=>{
      const cv=document.querySelector('#detailPoster canvas.kr-c'); if(!cv) return 'aucun';
      const W=cv.width, g=cv.getContext('2d'), d=g.getImageData(0,0,W,W).data, cx=W/2;
      const prof=[]; let prev=null;
      for(let x=0;x<W-cx;x++){ const i=((cx|0)*W+((cx|0)+x))*4;
        const s=d[i]+','+d[i+1]+','+d[i+2]+'/'+d[i+3];
        if(s!==prev){ prof.push(x+':'+s); prev=s; } }
      return {W:W, KR_R:window.KR_R, KR_LW:window.KR_LW, R:W*window.KR_R, lw:W*window.KR_LW,
        sombre: window._fondSombreSous?window._fondSombreSous(cv):'?', profil:prof.slice(0,40)};}"""))
    b.close()
