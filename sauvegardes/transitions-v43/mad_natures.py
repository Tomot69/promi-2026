# Combien de nœuds de Madrure ont un œil ? python3 mad_natures.py
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(pg.evaluate("""async()=>{ Toile.setTheme('madrure'); await new Promise(r=>setTimeout(r,5000)); const o={}; const ids=promises.filter(p=>!p.draft).map(p=>p.id);
      ids.forEach(id=>{ const n=Toile.natureDalle(id); o[n]=(o[n]||0)+1; }); return o; }"""))
    b.close()
