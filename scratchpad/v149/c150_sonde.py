import os, sys
from importlib.machinery import SourceFileLoader
from playwright.sync_api import sync_playwright
J = SourceFileLoader("j", "releve-S3-page-plus.py").load_module()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); setPremium(true);}")
    pg.wait_for_timeout(600)
    pg.evaluate(J.SCENE, 'pp_promi_rachel'); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{closeAll(); const q=P('juge page plus','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);}"); pg.wait_for_timeout(2000)
    print('après closeAll, show ?', pg.evaluate("()=>document.getElementById('createSheet').className"))
    pg.evaluate("""()=>{ window.__log=[]; const cs=document.getElementById('createSheet'); new MutationObserver(()=>window.__log.push([Math.round(performance.now()), cs.classList.contains('show'), String(window._couleurAPlanter&&JSON.stringify(window._couleurAPlanter))])).observe(cs,{attributes:true,attributeFilter:['class']}); window._couleurAPlanter={ci:3,lit:0}; }""")
    pg.evaluate(J.SCENE, 'pp_promi_vide'); pg.wait_for_timeout(1400)
    print('valeur :', pg.evaluate("()=>JSON.stringify(window._couleurAPlanter)"))
    print('journal :', pg.evaluate("()=>window.__log.slice(0,12)"))
    b.close()
