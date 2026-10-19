import sys
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000)
    for x in pg.evaluate("()=>promises.filter(p=>!p.draft).map(p=>[p.title,p.status,p.due,p.dueISO||null,(p.ech&&p.ech.iso)||null,p.from||''])"): print(' ', x)
    b.close()
