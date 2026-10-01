from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.on('console', lambda m: print('CONSOLE', m.type, m.text[:300]))
    pg.on('pageerror', lambda e: print('PAGEERR', str(e)[:400]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3200)
    print(json.dumps(pg.evaluate(r"""()=>{
      var out={};
      out.p127 = (promises.filter(function(q){return q.id===127;})[0]||null);
      if(out.p127) out.p127={id:out.p127.id,title:out.p127.title,status:out.p127.status,kind:out.p127.kind,from:out.p127.from,who:out.p127.who,draft:out.p127.draft};
      out.items=[].map.call(document.querySelectorAll('#feedView .fd-item'),function(it){return it.getAttribute('data-pid');});
      out.cartes=[].map.call(document.querySelectorAll('#feedList .s4-carte'),function(d){return (d.querySelector('.s4-ti')||{}).textContent;});
      out.grH=(document.querySelector('#feedList > div')||{}).style&&document.querySelector('#feedList > div').style.height;
      return out;}"""),indent=1,ensure_ascii=False))
    b.close()
