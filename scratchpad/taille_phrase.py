from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for k in ('promi','chiche','nuee'):
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1800)
        pg.evaluate("(k)=>{const t=[...document.querySelectorAll('.tile')].find(x=>x.getAttribute('data-kind')===k)||document.querySelector('.tile'); if(t) t.click();}", k)
        pg.wait_for_timeout(2200)
        print(k, pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
          const out=[];
          document.querySelectorAll('.ph-txt').forEach(t=>{const r=t.getBoundingClientRect(); if(r.width<2) return;
            out.push({fs:getComputedStyle(t).fontSize, w:Math.round(r.width/s), txt:t.textContent.trim().slice(0,40)});});
          const h=[...document.querySelectorAll('.ph-hint')].find(x=>x.getBoundingClientRect().width>2);
          return {phrase:out, aide:h?{fs:getComputedStyle(h).fontSize, w:Math.round(h.getBoundingClientRect().width/s), txt:h.textContent.trim().slice(0,45)}:null};}"""))
    b.close()
