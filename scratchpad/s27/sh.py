from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(4200)
    open('scratchpad/s27/SH1.png','wb').write(pg.query_selector('#device').screenshot())
    # ouvrir le tiroir
    pg.evaluate("()=>{var sc=document.getElementById('shareScreen'); sc.classList.add('shc-ouvert'); if(window._shcTire)window._shcTire(true);}")
    pg.wait_for_timeout(1600)
    open('scratchpad/s27/SH2.png','wb').write(pg.query_selector('#device').screenshot())
    print(json.dumps(pg.evaluate(r"""()=>{
      var o={classes:document.getElementById('shareScreen').className, regs:[]};
      document.querySelectorAll('#shcPile .shc-reg').forEach(function(c){
        var r=c.getBoundingClientRect();
        o.regs.push({lab:(c.querySelector('.l')||{}).textContent, y:+r.top.toFixed(0), h:+r.height.toFixed(0)});
      });
      o.mode=[].map.call(document.querySelectorAll('#shMode *'),function(e){return (e.textContent||'').trim().slice(0,20);}).slice(0,12);
      o.parts=[].map.call(document.querySelectorAll('#shNoyauParts *'),function(e){return (e.textContent||'').trim().slice(0,24);}).slice(0,20);
      return o;}"""),ensure_ascii=False,indent=1))
    b.close()
