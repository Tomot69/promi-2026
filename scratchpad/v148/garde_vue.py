from playwright.sync_api import sync_playwright
J = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const B=s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); const c=getComputedStyle(e); return [Math.round((r.top-D.top)/k), Math.round(r.height/k), c.display, c.visibility, c.color, e.className]; };
  return {garder:B('#createSheet .pp-garder'), pinceau:B('#createSheet .pc-t.on'), bar:B('#csBotBar'), sheet:document.getElementById('createSheet').className}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for F in ('app.html', 'zz-av147.html'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932})
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"); pg.wait_for_timeout(3500)
        print(F, pg.evaluate(J)); pg.screenshot(path='scratchpad/v148/garde_%s.png' % F.split('.')[0]); ctx.close()
    b.close()
