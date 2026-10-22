import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw,vh in ((390,844),(330,714),(390,664),(393,852)):
        ctx = contexte(b, vw=vw, vh=vh); toile_pleine(ctx, 5); pg = ouvre(ctx, 'app.html', attente=5000)
        print(vw,vh, pg.evaluate("()=>{var t=document.getElementById('toileCv');return [Toile.taille(), t.width,t.height, devicePixelRatio, document.getElementById('device').getBoundingClientRect().width]}"))
        ctx.close()
    b.close()
