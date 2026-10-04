import sys, subprocess
sys.path.insert(0,'scratchpad/v127')
from onb_dalle import joue
from playwright.sync_api import sync_playwright
INIT=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_theme','light')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000); pg.evaluate(INIT); joue(pg)
    f='scratchpad/v127/exp.png'; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844})
    print(subprocess.run(['python3','scratchpad/v127/bleu.py',f],capture_output=True,text=True).stdout.strip())
    b.close()
