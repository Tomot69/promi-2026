from playwright.sync_api import sync_playwright
import json,sys
URL=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3600)
    print(json.dumps(pg.evaluate(r"""()=>{var o=[];
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d,i){
        var ev=d.querySelector('.s4-ev'), et=d.querySelector('.s4-et'), ti=d.querySelector('.s4-ti');
        var re=ev.getBoundingClientRect(), rt=et.getBoundingClientRect(), ri=ti.getBoundingClientRect();
        o.push({i:i, evTop:+re.top.toFixed(1), evH:+re.height.toFixed(1), etTop:+rt.top.toFixed(1), etH:+rt.height.toFixed(1),
                tiTop:+ri.top.toFixed(1), tiH:+ri.height.toFixed(1)});});
      return o;}"""),ensure_ascii=False))
    b.close()
