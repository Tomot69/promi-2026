from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>document.getElementById('indexBtn')?document.getElementById('indexBtn').click():null"); pg.wait_for_timeout(2000)
    print(pg.evaluate("""async()=>{await document.fonts.ready;const r={};document.querySelectorAll('.s4-natlab').forEach(e=>{r[e.textContent.trim()]=e.getBoundingClientRect().width});
      const c=document.createElement('canvas').getContext('2d');c.font='400 13px PromiLate';const m={};['Promi','Chiche','Nuée','Cercle'].forEach(t=>m[t]=c.measureText(t).width);return {dom:r,canvas:m}}"""))
