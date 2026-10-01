from playwright.sync_api import sync_playwright
PIEGE="""(()=>{ window.__txt=[]; const P=CanvasRenderingContext2D.prototype, f=P.fillText, s=P.strokeText;
  P.fillText=function(t){ try{ window.__txt.push({c:(this.canvas&&this.canvas.id)||'?', t:String(t), s:String(this.fillStyle)}); }catch(e){} return f.apply(this,arguments); };
  P.strokeText=function(t){ try{ window.__txt.push({c:(this.canvas&&this.canvas.id)||'?', t:String(t), s:'stroke:'+String(this.strokeStyle)}); }catch(e){} return s.apply(this,arguments); }; })();"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.add_init_script(PIEGE); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(5200)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}"); pg.wait_for_timeout(2000)
    pg.evaluate("()=>{window.__txt=[]; document.getElementById('shNyOn').click(); window.shChiffre=true; shareToile._key=null; shareRender();}"); pg.wait_for_timeout(1500)
    L=pg.evaluate("()=>window.__txt.filter(x=>x.c==='shCanvas')")
    print(len(L), L[:8]); print(pg.evaluate("()=>[window._sigEncres, window._noyauSig]"))
