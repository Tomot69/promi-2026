from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(3000)
    print(json.dumps(pg.evaluate(r"""()=>{
      var o={};
      o.sel=document.querySelectorAll('[data-mode="noyau"]').length;
      o.shmode=document.querySelectorAll('#shMode').length;
      o.ids=document.querySelectorAll('[id=shMode]').length;
      var l=[].slice.call(document.querySelectorAll('#shMode button'));
      o.btns=l.map(function(b){return {m:b.getAttribute('data-mode'), t:b.textContent.trim(), p:(b.parentElement.id||b.parentElement.className)}; });
      /* on retire a la main, tout de suite */
      [].forEach.call(document.querySelectorAll('[data-mode="noyau"]'),function(x){x.parentNode.removeChild(x);});
      o.apres=[].map.call(document.querySelectorAll('#shMode button'),function(b){return b.getAttribute('data-mode');});
      return o;}"""),indent=1,ensure_ascii=False))
    pg.wait_for_timeout(2500)
    print('2,5 s plus tard', pg.evaluate("()=>[].map.call(document.querySelectorAll('#shMode button'),function(b){return b.getAttribute('data-mode');})"))
    b.close()
