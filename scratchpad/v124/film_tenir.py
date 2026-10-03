import sys, io, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
URL = sys.argv[1] if len(sys.argv) > 1 else 'app.html'; OUT = sys.argv[2] if len(sys.argv) > 2 else 'film'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pid = pg.evaluate("()=>{ const p=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee)[0]; p.status='rate'; return p.id; }")
    pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500); pg.evaluate("()=>{renderDetail()}"); pg.wait_for_timeout(1200)
    r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const b=e.getBoundingClientRect(); return {x:b.left,y:b.top,w:b.width,h:b.height}}")
    y = r['y'] + r['h'] / 2; pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
    for i in range(1, 26): pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
    ims = [(-1, Image.open(io.BytesIO(pg.screenshot(clip={'x': 20, 'y': 44, 'width': 390, 'height': 844}))))]
    t0 = time.time(); pg.mouse.up()
    while time.time() - t0 < 3.4:
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x': 20, 'y': 44, 'width': 390, 'height': 844}))); ims.append((int((time.time() - t0) * 1000), im))
    sel = ims[:1] + ims[1::max(1, len(ims) // 15)][:15]
    W, H = 195, 422; o = Image.new('RGB', (W * 8, (H + 18) * 2), (255, 255, 255)); d = ImageDraw.Draw(o)
    for k, (t, im) in enumerate(sel[:16]):
        o.paste(im.convert('RGB').resize((W, H)), ((k % 8) * W, (k // 8) * (H + 18) + 18)); d.text(((k % 8) * W + 4, (k // 8) * (H + 18) + 2), '%d ms' % t, fill=(0, 0, 0))
    o.save('scratchpad/v124/%s.png' % OUT); print(len(ims), [t for t, _ in ims][:40])
