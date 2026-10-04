import sys, json
sys.path.insert(0,'scratchpad/v127')
from onb_dalle import joue, BOITE
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for w in [float(x) for x in sys.argv[1:]]:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("window._onbPoids=%s; try{localStorage.setItem('promi_theme','light')}catch(e){}"%w)
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        joue(pg); r=pg.evaluate(BOITE); print(w, len(r['voisines']), r['principale'])
        g=pg.evaluate("()=>{try{return Toile_graines?0:0}catch(e){return 0}}")
        pg.screenshot(path='scratchpad/v127/poids-%s.png'%w, clip={'x':20,'y':44,'width':390,'height':844}); ctx.close()
    b.close()
