import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'encre'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':680}, device_scale_factor=2)
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('http://127.0.0.1:8752/scratchpad/vraie_toile.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=60000)
    pg.evaluate("(m)=>{Toile.setTheme(m);}",M); pg.wait_for_timeout(1600)
    pg.query_selector('#toileCv').screenshot(path='scratchpad/pav/_toile_%s.png'%M)
    print("err",e[:2],"->",'scratchpad/pav/_toile_%s.png'%M)
    b.close()
