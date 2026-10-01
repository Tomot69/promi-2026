from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('indexBtn').click();}"); pg.wait_for_timeout(2600)
    print(pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const out=[];
      document.querySelectorAll('#indexList .s4-carte').forEach((c,i)=>{
        if(i>3) return; const rc=c.getBoundingClientRect();
        const kid=[...c.children].map(e=>{const r=e.getBoundingClientRect(); const cs=getComputedStyle(e);
          return {cl:String(e.className).slice(0,18), y:+((r.top-rc.top)/s).toFixed(1), h:+(r.height/s).toFixed(1),
            fs:cs.fontSize, ov:cs.overflow, clamp:cs.webkitLineClamp, t:(e.textContent||'').trim().slice(0,22)};});
        out.push({h:+(rc.height/s).toFixed(1), w:+(rc.width/s).toFixed(1), ov:getComputedStyle(c).overflow, kid:kid});});
      return out;}"""))
    b.close()
