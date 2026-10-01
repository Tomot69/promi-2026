#!/usr/bin/env python3
"""LE BANC — on trouve la technique AVANT de dessiner."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':1000}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/scratchpad/banc-sphere.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=30000)
    print('%-6s %6s %8s %8s %8s %8s' % ('tech','N','moyen','médian','95e','pire'))
    for N in (800,1600,2400,4000,6000):
        for t in ('T1','T2','T3'):
            r=pg.evaluate("([t,N])=>window.banc(t,N,200)",[t,N])
            print('%-6s %6d %7.3f  %7.3f  %7.3f  %7.3f' % (t,N,r['moy'],r['median'],r['p95'],r['pire']))
        print()
    b.close()
