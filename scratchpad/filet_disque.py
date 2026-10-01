from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for lab,js in (('tenue',"()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"),
                   ('à tenir',"()=>{closeAll(); const p=promises.find(p=>p.status!=='tenu'&&!p.nuee&&!p.draft); if(p) openDetail(p.id);}")):
        pg.evaluate(js); pg.wait_for_timeout(2400)
        print(lab, pg.evaluate(r"""()=>{
          const out=[];
          document.querySelectorAll('#detailPoster canvas.kr-c').forEach(cv=>{
            const W=cv.width, g=cv.getContext('2d'), d=g.getImageData(0,0,W,W).data, cx=W/2;
            const R=W*window.KR_R, lw=W*window.KR_LW;
            const ray=[];
            for(let x=Math.floor(cx);x<W;x++){const i=((cx|0)*W+x)*4;
              ray.push([x-cx, d[i],d[i+1],d[i+2],d[i+3]]);}
            /* on ne garde que la zone autour du bord extérieur de l'anneau */
            const b0=Math.round(R+lw/2)-5, b1=Math.round(R+lw/2)+5;
            out.push({w:W, R:Math.round(R), lw:Math.round(lw), classes:String(document.getElementById('detailPoster').className),
              ferme:!!cv.closest('#detailPoster.f-tenue'),
              bord:ray.filter(r=>r[0]>=b0&&r[0]<=b1).map(r=>r[0]+':'+r[1]+','+r[2]+','+r[3]+'/'+r[4])});});
          return out;}"""))
    b.close()
