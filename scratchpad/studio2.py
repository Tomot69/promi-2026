from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2600)
    print(pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const out=[];
      document.querySelectorAll('#studioScreen *').forEach(e=>{
        const r=e.getBoundingClientRect(); if(r.width<40||r.height<10) return;
        const y=(r.top-dv.top)/s, h=r.height/s;
        if(y<520 || y>830) return;
        out.push({cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,22),
          y:+y.toFixed(1), h:+h.toFixed(1), b:+(y+h).toFixed(1), t:(e.textContent||'').trim().slice(0,16)});});
      return out;}"""))
    b.close()
