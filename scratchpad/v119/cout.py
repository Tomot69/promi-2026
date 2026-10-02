import sys
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for moteur in ('webkit','chromium'):
        b = p.webkit.launch() if moteur == 'webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        ouvre(pg, 0); pg.wait_for_timeout(5000)
        pg.evaluate("()=>{window._peloteU=1}")
        r=[pg.evaluate("()=>_peloteLumiere.cout(200)") for _ in range(5)]
        print(moteur, 'passage de lumière, ms par image (5 × 200 passages) :', ['%.3f'%x for x in r], pg.evaluate("()=>_peloteLumiere.etat().cle"))
        b.close()
