import sys, subprocess
sys.path.insert(0,'scratchpad/v127')
from onb_dalle import joue
from playwright.sync_api import sync_playwright
F=sys.argv[1]; N=int(sys.argv[2])
with sync_playwright() as p:
    b=p.webkit.launch()
    for i in range(N):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_theme','light')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000); joue(pg)
        for t in (0,1500):
            pg.wait_for_timeout(t); f='scratchpad/v127/pos-%s-%d-%d.png'%(F[:6],i,t); pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844})
            print(subprocess.run(['python3','scratchpad/v127/bleu.py',f],capture_output=True,text=True).stdout.strip())
        ctx.close()
    b.close()
