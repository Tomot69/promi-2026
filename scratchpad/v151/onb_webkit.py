# l'onboarding en WebKit (le moteur de Safari), sombre : la page du trait — la couleur calculée de « trace pour planter » et les pixels de son encre
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
from collections import Counter
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
TH = sys.argv[2] if len(sys.argv) > 2 else 'sombre'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, sombre=(TH=='sombre'), onb=False, guide=False); pg=B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000)
    r = pg.evaluate("""()=>{ const e=document.getElementById('onbTrace'); if(!e) return null; const c=getComputedStyle(e); const d=document.getElementById('device');
      const g=document.createRange(); g.selectNodeContents(e); const b=g.getBoundingClientRect(); return {col:c.color, fill:c.webkitTextFillColor, vis:c.visibility, disp:c.display, light:d.classList.contains('light'), box:[b.left,b.top,b.right,b.bottom], html:e.innerHTML.slice(0,160)}; }""")
    print(TH, r)
    pg.screenshot(path='scratchpad/v151/onb_wk_%s.png' % TH)
    if r:
        im=Image.open('scratchpad/v151/onb_wk_%s.png' % TH).convert('RGB'); k=im.width/390
        x0,y0,x1,y1=[int(v*im.width/pg.viewport_size['width']) for v in r['box']]
        C=Counter(im.getpixel((x,y)) for y in range(y0,y1) for x in range(x0,x1))
        print('pixels les plus fréquents dans la boîte du mot :', C.most_common(4))
    b.close()
