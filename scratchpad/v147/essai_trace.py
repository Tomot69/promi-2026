import sys; from playwright.sync_api import sync_playwright
OUT=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':760,'height':440}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/scratchpad/v147/essai_trace.html'); pg.wait_for_function('window.pret'); pg.wait_for_timeout(600)
    pg.evaluate("()=>Promise.all([C.a.pret,C.b.pret])")
    for q in [float(x) for x in sys.argv[2].split(',')]:
        pg.evaluate("q=>{ C.a.va(q); C.b.va(q); }", q); pg.wait_for_timeout(120)
        pg.screenshot(path='%s/tr-%03d.png'%(OUT,int(q*1000)))
    b.close()
