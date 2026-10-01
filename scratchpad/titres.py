from playwright.sync_api import sync_playwright
ECR=[('accueil',"()=>{closeAll();}"),
     ('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}"),
     ('index',"()=>{closeAll(); document.getElementById('indexBtn').click();}"),
     ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}"),
     ('reglages',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}"),
     ('partage',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click(); else if(window.openShare)openShare();}")]
JS=r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const out=[];
  document.querySelectorAll('.scr-t, .enh-t, .enh h2, .enh h1').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<3) return;
    const sv=e.querySelector('svg');
    out.push({txt:(e.textContent||'').trim().slice(0,18), fs:getComputedStyle(e).fontSize,
      ff:getComputedStyle(e).fontFamily.split(',')[0], h:+(r.height/s).toFixed(1),
      svgH:sv?+(sv.getBoundingClientRect().height/s).toFixed(1):null,
      svgW:sv?+(sv.getBoundingClientRect().width/s).toFixed(1):null,
      encart:(()=>{const p=e.closest('.enh'); return p?+(p.getBoundingClientRect().height/s).toFixed(1):null;})(),
      y:+((r.top-dv.top)/s).toFixed(1)});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR:
        try: pg.evaluate(js)
        except Exception as e: print(nom,'??',str(e)[:50]); continue
        pg.wait_for_timeout(2000)
        print('%-9s'%nom, pg.evaluate(JS))
    b.close()
