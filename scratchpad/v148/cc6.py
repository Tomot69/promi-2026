from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 430, 'height': 932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    print(pg.evaluate("""async ()=>{ const cs=document.getElementById('createSheet'); const L=[]; const ob=new MutationObserver(()=>L.push([Math.round(performance.now()), cs.className])); ob.observe(cs,{attributes:true,attributeFilter:['class']});
      closeAll(); await new Promise(r=>setTimeout(r,300)); const a=cs.className; window._couleurAPlanter={ci:3,lit:0};
      document.getElementById('createBtn').click(); await new Promise(r=>setTimeout(r,400)); const t=[...document.querySelectorAll('#createSheet .tile')][0]; const bb=t&&t.querySelector('button,.tg,.hname'); if(bb)bb.click(); else if(t)t.click();
      await new Promise(r=>setTimeout(r,1400)); ob.disconnect(); return {apresClose:a, fin:cs.className, couleur:window._couleurAPlanter, L:L.slice(0,8)}; }"""))
    b.close()
