from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const k=Object.keys(NUE||{})[0]; window.openNueeDetail(k);}"); pg.wait_for_timeout(3000)
    print(pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const out=[];
      document.querySelectorAll('#detailPoster *').forEach(e=>{
        const r=e.getBoundingClientRect(); if(r.width<20||r.height<8) return;
        const t=(e.textContent||'').trim().slice(0,22);
        if(!t) return;
        out.push({cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,22),
          y:+((r.top-dv.top)/s).toFixed(0), h:+(r.height/s).toFixed(0), t:t});});
      return out.slice(0,26);}"""))
    b.close()
