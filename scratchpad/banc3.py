#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':1000}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/scratchpad/banc3.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=30000)
    print('  Couverture CONSTANTE 60 000 px de trait — on découpe plus ou moins fin')
    print('  %-8s %7s %5s %8s %8s %8s' % ('mode','N','long','moyen','médian','>20ms'))
    for (N,LG) in [(15000,4),(7500,8),(3750,16),(1875,32),(940,64)]:
        r=pg.evaluate("([N,LG,nt,d,m,ms])=>window.essai(N,LG,nt,d,m,ms)",[N,LG,4,2,'lignes',2200])
        print('  %-8s %7d %5d %7.2f  %7.2f  %4d/%d'%('lignes',r['N'],r['LG'],r['moy'],r['med'],r['sup20'],r['im']))
    print()
    print('  Nombre de segments à longueur fixe 10 px')
    for N in [1200,2400,3600,5000,7000]:
        r=pg.evaluate("([N,LG,nt,d,m,ms])=>window.essai(N,LG,nt,d,m,ms)",[N,10,4,2,'lignes',2200])
        print('  %-8s %7d %5d %7.2f  %7.2f  %4d/%d'%('lignes',r['N'],r['LG'],r['moy'],r['med'],r['sup20'],r['im']))
    print()
    for N in [3600,7000,13000]:
        r=pg.evaluate("([N,LG,nt,d,m,ms])=>window.essai(N,LG,nt,d,m,ms)",[N,10,4,2,'points',2200])
        print('  %-8s %7d %5s %7.2f  %7.2f  %4d/%d'%('points',r['N'],'-',r['moy'],r['med'],r['sup20'],r['im']))
    b.close()
