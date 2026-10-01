from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const k=Object.keys(NUE||{})[0]; if(k) window.openNueeDetail(k);}"); pg.wait_for_timeout(2800)
    print(pg.evaluate(r"""()=>{const out=[];
      document.querySelectorAll('#detailPoster, #detailPoster *').forEach(e=>{
        if(e.scrollHeight > e.clientHeight+2 && e.clientHeight>40)
          out.push({id:e.id||String(e.className).slice(0,26), top:Math.round(e.scrollTop), sh:e.scrollHeight, ch:e.clientHeight});});
      return out;}"""))
    b.close()
