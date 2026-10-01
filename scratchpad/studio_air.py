from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2600)
    print(pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
      const pan=document.querySelector('#stcCadre .st-panneau, #studioScreen .st-panneau, #studioBody')
        || [...document.querySelectorAll('#studioScreen *')].filter(e=>{const r=e.getBoundingClientRect();
             return r.height>180 && r.height<330 && r.width>330;}).pop();
      if(!pan) return 'pas de panneau';
      const rp=pan.getBoundingClientRect();
      const kids=[...pan.querySelectorAll('*')].map(e=>{const r=e.getBoundingClientRect();
        return r.height>2&&r.width>2 ? {cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,20),
          y:+((r.top-rp.top)/s).toFixed(1), b:+((r.bottom-rp.top)/s).toFixed(1), t:(e.textContent||'').trim().slice(0,14)} : null;}).filter(Boolean);
      const hb=Math.min(...kids.map(k=>k.y)), bb=Math.max(...kids.map(k=>k.b));
      return {panneau:{y:+((rp.top-dv.top)/s).toFixed(1), h:+(rp.height/s).toFixed(1), cl:(pan.id?'#'+pan.id:'.'+String(pan.className).split(' ')[0])},
        premierHaut:hb, dernierBas:bb, airHaut:+hb.toFixed(1), airBas:+(rp.height/s-bb).toFixed(1), n:kids.length};}"""))
    b.close()
