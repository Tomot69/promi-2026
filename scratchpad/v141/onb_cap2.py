import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]; out=sys.argv[2]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.click('#onbPh'); pg.wait_for_timeout(300); pg.keyboard.type('Tom',delay=80); pg.wait_for_timeout(1800)
    r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
    pg.screenshot(path=out,clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); b.close()
