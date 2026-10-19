import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
pol, gr, car = sys.argv[1], sys.argv[2], sys.argv[3]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.wait_for_timeout(300)
    r = pg.evaluate("""async a=>{ const [pol,gr,car]=a; TraceLettres._debug=1; TraceLettres._cache={}; let el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:80px;font:'+gr+' 150px/180px '+pol+';color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
      await document.fonts.load(gr+' 150px '+pol); const c=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await c.pret; c.va(0.5); const d=TraceLettres._derniere; return {coins:d.coins, bouts:d.bouts}; }""", [pol, gr, car])
    print(json.dumps(r)[:1500]); b.close()
