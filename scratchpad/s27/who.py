from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll(); openDetail(133);}"); pg.wait_for_timeout(3000)
    print(json.dumps(pg.evaluate(r"""()=>{var o=[];
      document.querySelectorAll('#detailPoster *').forEach(function(e){
        var t=(e.textContent||'').trim();
        if(e.children.length) return;
        if(!/trace pour tenir|LANC|Au groupe/.test(t)) return;
        o.push({txt:t.slice(0,24), cls:String(e.className).slice(0,24), id:e.id,
          style:(e.getAttribute('style')||'').slice(0,200), lis:e.getAttribute('data-lis'),
          col:getComputedStyle(e).color});});
      return o;}"""),indent=1,ensure_ascii=False))
    b.close()
