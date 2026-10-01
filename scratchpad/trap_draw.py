from playwright.sync_api import sync_playwright
PIEGE="""(()=>{ window.__dr=[]; const P=CanvasRenderingContext2D.prototype, f=P.drawImage;
  P.drawImage=function(src){ try{ if(this.canvas&&this.canvas.id==='shCanvas'){ const a=arguments, n=a.length, T=this.getTransform();
      let dx,dy,dw,dh; if(n>=9){dx=a[5];dy=a[6];dw=a[7];dh=a[8];} else if(n>=5){dx=a[1];dy=a[2];dw=a[3];dh=a[4];} else {dx=a[1];dy=a[2];dw=src.width;dh=src.height;}
      window.__dr.push({src:(src.id||src.className||src.tagName||'?')+'', pel:!!src.__pelote, x:T.a*dx+T.e, y:T.d*dy+T.f, w:T.a*dw, h:T.d*dh}); } }catch(e){} return f.apply(this,arguments); }; })();"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.add_init_script(PIEGE); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>openShare()"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{document.querySelector('#shMode [data-mode=mosaic]').click();}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{window.shPelote=true; window.shPelBR=1; window.shPelBC=0; window.__dr=[]; shareRender();}"); pg.wait_for_timeout(1500)
    D=pg.evaluate("()=>window.__dr"); print(len(D)); 
    from collections import Counter; print(Counter(d['src'][:30] for d in D))
    for d in D[:6]: print(d)
    print(pg.evaluate("()=>{const C=window._plancheComp; return {bloc:C.bloc, c0:C.cases[0], G:{W:C.grille.W,H:C.grille.H}}}"))
