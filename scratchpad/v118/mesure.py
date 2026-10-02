import sys
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for moteur, S in (('webkit', 3), ('chromium', 3)):
        b = p.webkit.launch() if moteur == 'webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); reqs = []; pg.on('request', lambda r: reqs.append(r.url))
        pg.goto('http://127.0.0.1:8752/app.html?mesure=1'); pg.wait_for_timeout(7000)
        ouvre(pg, 0); pg.wait_for_timeout(3000)
        print(moteur, '· en cours :', pg.evaluate("()=>(document.getElementById('auMesure')||{}).textContent"))
        pg.wait_for_timeout(24000 if moteur == 'chromium' else 40000)
        print(pg.evaluate("()=>(document.getElementById('auMesure')||{}).textContent"))
        print('diag-studio chargé :', any('diag-studio' in u for u in reqs))
        pg.screenshot(path='scratchpad/v118/mesure-%s.png' % moteur, clip={'x':20,'y':44,'width':390,'height':844})
        # sans le paramètre : aucun cadre
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000); ouvre(pg, 0); pg.wait_for_timeout(1500)
        print('sans ?mesure=1 → cadre :', pg.evaluate("()=>!!document.getElementById('auMesure')"))
        b.close()
