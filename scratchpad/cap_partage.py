from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(400)
    ok=pg.evaluate("()=>{closeAll(); const b=document.getElementById('shareBtn')||document.querySelector('[data-open=\"share\"]'); if(b){b.click(); return 'btn';} if(window.openShare){openShare(); return 'fn';} return 'non';}")
    print('ouverture:',ok); pg.wait_for_timeout(3200)
    open('scratchpad/partage.png','wb').write(pg.query_selector('#device').screenshot())
    print(pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const out=[];
      document.querySelectorAll('#shareScreen *').forEach(e=>{
        const r=e.getBoundingClientRect(); if(r.width<12||r.height<8) return;
        const t=(e.textContent||'').trim().slice(0,24); if(!t) return;
        out.push({cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,20), y:+((r.top-dv.top)/s).toFixed(0), t:t});});
      return out.slice(0,34);}"""))
    b.close()
