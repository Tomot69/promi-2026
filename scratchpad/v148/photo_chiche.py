from playwright.sync_api import sync_playwright
J = """()=>{ const b=[...document.querySelectorAll('#createSheet .ph-photo')].find(x=>x.getBoundingClientRect().width>4); if(!b) return 'pas de bouton'; const r=b.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
  const pc=document.getElementById('planterCv'), q=pc?pc.getBoundingClientRect():null; return {sur:h?(h.id||h.className):null, bouton:[r.left,r.top,r.width,r.height].map(Math.round), planterCv:q?[q.left,q.top,q.width,q.height].map(Math.round):null, pcStyle:pc?[getComputedStyle(pc).zIndex,getComputedStyle(pc).pointerEvents,getComputedStyle(pc).visibility,getComputedStyle(pc).opacity, pc.parentElement.id||pc.parentElement.className]:null}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for F in ('app.html', 'zz-av147.html'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932})
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][1]; if(x)x.click();},300);}"); pg.wait_for_timeout(3500)
        print(F, pg.evaluate(J))
        pg.evaluate("()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{ if(window._nueeDefile) window._nueeDefile(true); },900);}"); pg.wait_for_timeout(3500)
        print('  nuee', pg.evaluate("()=>{ const it=[...document.querySelectorAll('#dpNueeFil .nf-item')].slice(0,3).map(e=>{ const r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return [Math.round(r.top), Math.round(r.height), h?(h.id||String(h.className).slice(0,20)):null]; }); const m=document.getElementById('dpMain').getBoundingClientRect(); return {items:it, dpMain:[m.top,m.height].map(Math.round), cls:document.getElementById('detailPoster').className}; }"))
        ctx.close()
    b.close()
