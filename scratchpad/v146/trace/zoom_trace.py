# zoom_trace.py — un glyphe en très grand, seize instants du tracé :  python3 zoom_trace.py f h [sortie.png]
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
car = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else 'h'; sortie = sys.argv[3] if len(sys.argv) > 3 else 'zoomt.png'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/scratchpad/v146/trace/essai.html'); pg.wait_for_timeout(900)
    pg.evaluate("""a=>{ document.body.innerHTML='<div id="z" style="position:absolute;left:0;top:0;width:160px;height:200px;font:700 150px/200px Gilbert;text-align:center;color:#291547"></div>'; document.getElementById('z').textContent=a; }""", car)
    info = pg.evaluate("async v=>{ window.c=TraceLettres.trace(document.getElementById('z'), null, {manuel:true, depart:v, respecteReduire:false}); await c.pret; const g=c.glyphes[0]; const pc=TraceLettres.parcours('Gilbert', g.car, g.variante); return [g.variante, pc.traits.map(t=>[t.b0,t.b1,t.pts.length,Math.round(t.L)]), pc.ordre]; }", V)
    print(info); ims = []
    for i in range(16):
        pg.evaluate("f=>c.va(f)", (i + 1) / 16.0); pg.wait_for_timeout(50)
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 0, 'width': 160, 'height': 200}))).convert('RGB'))
    b.close()
w, h = ims[0].size; out = Image.new('RGB', (8 * w // 2, 2 * h // 2), 'white')
for i, im in enumerate(ims): out.paste(im.resize((w // 2, h // 2), Image.LANCZOS), ((i % 8) * w // 2, (i // 8) * h // 2))
out.save(sortie); print(sortie, out.size)
