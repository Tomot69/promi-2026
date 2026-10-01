from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu-vsync','--disable-frame-rate-limit'])
    pg=b.new_page(viewport={'width':700,'height':700}, device_scale_factor=1)
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    import sys as _s; pg.goto('http://127.0.0.1:8752/scratchpad/banc_poils.html#'+(_s.argv[1] if len(_s.argv)>1 else '1'))
    pg.wait_for_function("()=>window.__pret===true",timeout=300000)
    print("err",e[:3]); print("  pixels par poil :",pg.evaluate("()=>window.__px"))
    for r in pg.evaluate("()=>window.__res"): print("  ",r['t'])
    b.close()
