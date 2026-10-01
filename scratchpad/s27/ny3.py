from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(4200)
    for t in (0,2500):
        if t: pg.wait_for_timeout(t)
        print(t, json.dumps(pg.evaluate(r"""()=>{
          function vis(e){var r=e.getBoundingClientRect(); var c=getComputedStyle(e);
            return (r.width>1&&r.height>1&&c.display!=='none'&&c.visibility!=='hidden');}
          return {sujet:[].filter.call(document.querySelectorAll('#shMode button'),vis).map(function(b){return b.textContent.trim();}),
                  parts:[].filter.call(document.querySelectorAll('#shNoyauParts button'),vis).map(function(b){return b.textContent.trim();})};}"""),ensure_ascii=False))
    b.close()
