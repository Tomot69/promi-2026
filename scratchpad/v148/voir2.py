import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
def shot(pg, y0=0, y1=844):
    d = dev(pg); k = d[2] / 390.0
    return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1] + y0 * k, 'width': d[2], 'height': (y1 - y0) * k})))
page = sys.argv[1]; th = sys.argv[2]; out = sys.argv[3]; actions = sys.argv[4:]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s');}catch(e){}" % th)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + page); pg.wait_for_timeout(6500)
    ims = []
    for a in actions:
        if a.startswith('js:'): pg.evaluate("()=>{" + a[3:] + "}"); pg.wait_for_timeout(2600)
        elif a == 'shot': ims.append(shot(pg))
        elif a.startswith('wait:'): pg.wait_for_timeout(int(a[5:]))
    w, h = ims[0].size; o = Image.new('RGB', (w * len(ims) + 20 * (len(ims) - 1), h), (255, 255, 255))
    for i, im in enumerate(ims): o.paste(im, (i * (w + 20), 0))
    o = o.resize((o.width * 2 // 5, o.height * 2 // 5)); o.save(out); print(out, o.size)
    b.close()
