import io
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 892}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-invite-variantes.html'); pg.wait_for_timeout(9000)
    pg.evaluate("()=>{ _invite.v('B'); _invite.ouvre(); }"); pg.wait_for_timeout(1500)
    ims = []
    for i in range(10):
        pg.wait_for_timeout(180); ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': 150, 'y': 48 + 255, 'width': 200, 'height': 110}))))
    w, h = ims[0].size; o = Image.new('RGB', (w * 2 + 10, h * 5 + 40), (255, 255, 255))
    for i, im in enumerate(ims): o.paste(im, ((i % 2) * (w + 10), (i // 2) * (h + 10)))
    o = o.resize((o.width // 2, o.height // 2)); o.save('scratchpad/v148/invite_B.png')
    b.close()
