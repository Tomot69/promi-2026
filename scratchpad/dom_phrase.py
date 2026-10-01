from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{const t=document.querySelector('.tile'); if(t) t.click();}"); pg.wait_for_timeout(2200)
    print(pg.evaluate(r"""()=>{const t=document.querySelector('.ph-txt');
      const av=t.style.whiteSpace; t.style.setProperty('white-space','nowrap','important');
      const w=t.scrollWidth; t.style.removeProperty('white-space'); if(av)t.style.whiteSpace=av;
      return {html:t.innerHTML.slice(0,700), nowrapW:w, boite:Math.round(t.getBoundingClientRect().width)};}"""))
    b.close()
