from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3200)
    print(json.dumps(pg.evaluate(r"""()=>{
      var o={comp:window._filComp, feed:(window.FEED||[]).map(function(z){return {pid:z.pid,ev:z.ev,from:z.from};}), cartes:[]};
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d){
        var ti=d.querySelector('.s4-ti'), cv=d.querySelector('canvas');
        o.cartes.push({titre:ti?ti.textContent:'', tiH:ti?+ti.scrollHeight:0, tiBox:ti?+ti.getBoundingClientRect().height.toFixed(1):0,
          fs:ti?getComputedStyle(ti).fontSize:'', champ:cv?cv.getAttribute('data-champ'):null, peint:cv?cv.getAttribute('data-peint'):null});
      });
      return o;}"""),indent=1,ensure_ascii=False))
    b.close()
