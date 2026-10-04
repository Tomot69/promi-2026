from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':900},device_scale_factor=3); pg=ctx.new_page()
    for th in ('light','dark'):
        for v in ('E1','E2'):
            pg.goto('http://127.0.0.1:8752/scratchpad/v127/dessin/trait.html?v=%s&th=%s'%(v,th)); pg.wait_for_function("()=>window._pret",timeout=20000); pg.wait_for_timeout(300)
            pg.screenshot(path='scratchpad/v127/dessin/trait-%s-%s.png'%(v,th), full_page=True)
    b.close()
from PIL import Image
for th in ('light','dark'):
    a=Image.open('scratchpad/v127/dessin/trait-E1-%s.png'%th); c=Image.open('scratchpad/v127/dessin/trait-E2-%s.png'%th); Q=Image.new('RGB',(a.width*2+60,max(a.height,c.height)),(240,236,226) if th=='light' else (16,13,11)); Q.paste(a,(0,0)); Q.paste(c,(a.width+60,0)); Q.save('planche-v127/dessin-C-trait-%s.png'%('clair' if th=='light' else 'sombre'))
